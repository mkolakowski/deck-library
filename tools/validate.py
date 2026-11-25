#!/usr/bin/env python3
"""Check every deck in decks/manifest.json.

    python tools/validate.py                      # deck-building rules and manifest checks
    python tools/validate.py --playmat ../playmat  # also check each [SET:NUM] exists in a Playmat (XMage) checkout

Rules checked: Constructed decks have 60+ main cards, at most 15 sideboard cards and at most 4 copies of a card
(basic lands excepted); Commander decks have exactly 100 cards including the commander(s), one copy of each card
(basic lands excepted). With --playmat, each printing must appear on a live (not commented-out) SetCardInfo line
in Mage.Sets/src/mage/sets, which is what Playmat needs to import the .dck.
Exits 1 if anything fails.
"""
import argparse, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASICS = {'Plains', 'Island', 'Swamp', 'Mountain', 'Forest', 'Wastes',
          'Snow-Covered Plains', 'Snow-Covered Island', 'Snow-Covered Swamp', 'Snow-Covered Mountain', 'Snow-Covered Forest'}
FORMATS = {'Standard', 'Pioneer', 'Modern', 'Legacy', 'Vintage', 'Commander', 'Pauper', 'Other'}
LINE = re.compile(r'^(SB:\s*)?(\d+)\s+\[([^:\]]+):([^\]]+)\]\s+(.+)$')


def parse(path):
    cards, name, bad = [], None, []
    for n, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith('NAME:'):
            name = line[5:].strip()
            continue
        m = LINE.match(line)
        if not m:
            bad.append(f'line {n}: not "QTY [SET:NUM] Name": {line}')
            continue
        cards.append({'side': bool(m.group(1)), 'q': int(m.group(2)), 'set': m.group(3), 'num': m.group(4), 'name': m.group(5)})
    return name, cards, bad


def playmat_index(root):
    live = {}
    for f in glob.glob(os.path.join(root, 'Mage.Sets', 'src', 'mage', 'sets', '*.java')):
        text = open(f, encoding='utf-8', errors='ignore').read()
        code = re.search(r'super\("[^"]*", "([^"]+)"', text)
        if not code:
            continue
        for line in text.splitlines():
            if 'SetCardInfo(' in line and not line.strip().startswith('//'):
                m = re.search(r'SetCardInfo\("([^"]+)", "?([\w*]+)"?', line)
                if m:
                    live.setdefault((code.group(1).upper(), m.group(2)), set()).add(m.group(1))
    return live


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--playmat', help='path to a Playmat (or XMage) source checkout')
    args = ap.parse_args()
    errors, warnings = [], []
    manifest = json.load(open(os.path.join(ROOT, 'decks', 'manifest.json'), encoding='utf-8'))
    live = playmat_index(args.playmat) if args.playmat else None
    if args.playmat and not live:
        sys.exit(f'No Mage.Sets set files found under {args.playmat}')
    ids = set()
    listed = set()
    for d in manifest:
        tag = d.get('id', '?')
        for k in ('id', 'title', 'format', 'pitch', 'file', 'colors', 'added', 'updated'):
            if k not in d:
                errors.append(f'{tag}: manifest entry missing "{k}"')
        if d.get('id') in ids:
            errors.append(f'{tag}: duplicate id')
        ids.add(d.get('id'))
        if not re.fullmatch(r'[a-z0-9-]+', d.get('id', '')):
            errors.append(f'{tag}: id must be lowercase letters, digits and hyphens')
        if d.get('format') not in FORMATS:
            errors.append(f'{tag}: format must be one of {sorted(FORMATS)}')
        tags = d.get('tags', [])
        if not isinstance(tags, list) or not all(isinstance(t, str) and re.fullmatch(r'[a-z0-9-]+', t) for t in tags):
            errors.append(f'{tag}: tags must be a list of lowercase words (letters, digits, hyphens)')
        if not re.fullmatch(r'[WUBRG]*', d.get('colors', '')):
            errors.append(f'{tag}: colors must use only W U B R G')
        path = os.path.join(ROOT, 'decks', d.get('file', ''))
        listed.add(os.path.basename(path))
        if not os.path.isfile(path):
            errors.append(f'{tag}: file decks/{d.get("file")} not found')
            continue
        _, cards, bad = parse(path)
        errors += [f'{tag}: {b}' for b in bad]
        main_ = [c for c in cards if not c['side']]
        side = [c for c in cards if c['side']]
        copies = {}
        for c in cards:
            copies[c['name']] = copies.get(c['name'], 0) + c['q']
        if d.get('format') == 'Commander':
            total = sum(c['q'] for c in cards)
            if total != 100:
                errors.append(f'{tag}: Commander deck has {total} cards (needs 100 including commanders on SB: lines)')
            if not side:
                errors.append(f'{tag}: no commander (put the commander on an SB: line)')
            errors += [f'{tag}: {n} x{q} breaks singleton' for n, q in copies.items() if q > 1 and n not in BASICS]
        else:
            nm, ns = sum(c['q'] for c in main_), sum(c['q'] for c in side)
            if nm < 60:
                errors.append(f'{tag}: main deck has {nm} cards (needs 60+)')
            if ns > 15:
                errors.append(f'{tag}: sideboard has {ns} cards (max 15)')
            errors += [f'{tag}: {n} x{q} (max 4)' for n, q in copies.items() if q > 4 and n not in BASICS]
        if not os.path.isfile(os.path.join(ROOT, 'decks', 'guides', d.get('id', '') + '.json')):
            warnings.append(f'{tag}: no play guide at decks/guides/{d.get("id")}.json')
        if 'face' in d and not any(c['set'] == d['face']['set'] and c['num'] == d['face']['num'] for c in cards):
            warnings.append(f'{tag}: face card {d["face"]} is not a printing in the deck')
        if live is not None:
            for c in cards:
                names = live.get((c['set'].upper(), c['num']))
                if not names:
                    errors.append(f'{tag}: [{c["set"]}:{c["num"]}] {c["name"]} is not in Playmat')
                elif c['name'] not in names:
                    errors.append(f'{tag}: [{c["set"]}:{c["num"]}] is {sorted(names)} in Playmat, not "{c["name"]}"')
    for f in glob.glob(os.path.join(ROOT, 'decks', '*.dck')):
        if os.path.basename(f) not in listed:
            warnings.append(f'decks/{os.path.basename(f)} is not in manifest.json')
    for w in warnings:
        print('warning:', w)
    for e in errors:
        print('error:', e)
    print(f'{len(manifest)} decks checked, {len(errors)} errors, {len(warnings)} warnings'
          + (' (with Playmat printings)' if live is not None else ''))
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()

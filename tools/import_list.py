#!/usr/bin/env python3
"""Turn a plain decklist ("4 Lightning Bolt" lines, optional "Sideboard" section) into a Playmat .dck file.

    python tools/import_list.py list.txt --playmat ../playmat --name "Deck Title" [--prefer TMT,TLA] [-o decks/id.dck]

For each card it picks a printing from a live (uncommented) SetCardInfo line in Playmat's set files:
a set listed in --prefer first, otherwise the newest regular expansion or core set printing (non-variant art
where there is a choice). Prints the chosen printing per card and exits 1 if any card isn't in Playmat.
"""
import argparse, datetime, glob, os, re, sys

SET_RE = re.compile(r'super\("([^"]+)", "([^"]+)", ExpansionSet\.buildDate\((\d+), (\d+), (\d+)\), SetType\.(\w+)')
CARD_RE = re.compile(r'SetCardInfo\("([^"]+)", "?([\w*]+)"?, Rarity\.\w+, mage\.cards\.[\w.]+\.class([^)]*)\)')
REGULAR = ('EXPANSION', 'CORE', 'SUPPLEMENTAL_MODERN_LEGAL')


def index(playmat):
    cards = {}
    for f in glob.glob(os.path.join(playmat, 'Mage.Sets', 'src', 'mage', 'sets', '*.java')):
        text = open(f, encoding='utf-8', errors='ignore').read()
        m = SET_RE.search(text)
        if not m:
            continue
        title, code, y, mo, d, typ = m.groups()
        for line in text.splitlines():
            if line.strip().startswith('//'):
                continue
            c = CARD_RE.search(line)
            if c and c.group(2).isdigit():
                cards.setdefault(c.group(1), []).append({'set': code, 'num': c.group(2), 'date': (int(y), int(mo), int(d)),
                                                         'type': typ, 'variant': 'VARIOUS' in c.group(3), 'title': title})
    return cards


def norm(s):
    return s.replace('’', "'").replace('û', 'u').replace('é', 'e').replace('É', 'E').strip().lower()


def pick(prints, prefer):
    for code in prefer:
        own = [p for p in prints if p['set'] == code]
        if own:
            return sorted(own, key=lambda p: (p['variant'], int(p['num'])))[0]
    today = datetime.date.today().timetuple()[:3]
    prints = [p for p in prints if p['date'] <= today] or prints  # skip sets Playmat lists before release
    pool = [p for p in prints if p['type'] in REGULAR] or prints
    best = max(pool, key=lambda p: (not p['variant'], p['date']))
    same = [p for p in pool if p['set'] == best['set']]
    return sorted(same, key=lambda p: (p['variant'], int(p['num'])))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('list'); ap.add_argument('--playmat', required=True); ap.add_argument('--name', required=True)
    ap.add_argument('--prefer', default=''); ap.add_argument('-o', '--out')
    a = ap.parse_args()
    cards = index(a.playmat)
    by_norm = {norm(k): k for k in cards}
    prefer = [p.strip().upper() for p in a.prefer.split(',') if p.strip()]
    out, missing, side = [f'NAME:{a.name}'], [], False
    for raw in open(a.list, encoding='utf-8'):
        line = raw.strip()
        if not line:
            continue
        if line.lower().rstrip(':') in ('sideboard', 'sb'):
            side = True
            continue
        if line.lower().rstrip(':') in ('deck', 'main', 'maindeck', 'commander'):
            continue
        m = re.match(r'^(SB:\s*)?(\d+)x?\s+(.+?)(?:\s+\(\w+\)\s*\S*)?$', line)
        if not m:
            print('skip:', line); continue
        q, name = int(m.group(2)), m.group(3)
        real = by_norm.get(norm(name))
        if not real:
            missing.append(name); continue
        p = pick(cards[real], prefer)
        out.append(('SB: ' if side or m.group(1) else '') + f'{q} [{p["set"]}:{p["num"]}] {real}')
        print(f'{q:2} {real:42} {p["set"]:>4} #{p["num"]:<5} {p["title"]} {p["date"][0]}')
    if missing:
        print('NOT IN PLAYMAT:', missing)
        sys.exit(1)
    text = '\n'.join(out) + '\n'
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(text)
    else:
        print(text)


if __name__ == '__main__':
    main()

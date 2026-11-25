# Deck Library: notes for Claude

A static GitHub Pages site listing Magic: The Gathering decks built for Matthew's self-hosted **Playmat** server
(a browser client for the XMage rules engine). Each deck is a `.dck` file. The page reads those files and pulls
card data and images live from the Scryfall API, so there is no build step and no art to commit.

## Layout

- `index.html`: the whole site (one file: styles, markup, script).
- `decks/manifest.json`: one entry per deck, in the order they were added.
- `decks/<id>.dck`: the deck itself, in XMage's .dck format.
- `decks/guides/<id>.json`: the deck's "How to play" notes.
- `tools/validate.py`: deck-rule and printing checks. Run it before every commit.
- `tools/import_list.py`: turns a plain list (`4 Lightning Bolt`, or `4x ...`, `SB:` / `Sideboard` sections) into a
  `.dck` with Playmat printings: `python tools/import_list.py list.txt --playmat <playmat> --name "Title" [--prefer SET] -o decks/<id>.dck`.
  It picks the preferred set, else the newest released regular printing. Review its choices (swap in themed art) afterwards.

## Adding a deck

1. **Build the list** for the format asked for (Standard, Modern, Commander and so on).
   - Constructed: 60+ main, at most 15 sideboard, max 4 of a card except basic lands.
   - Commander: exactly 100 including the commander(s), singleton except basic lands, every card within the
     commander's color identity. Commander-only sets (TRC, 40K, WHO, M3C and similar) are not Modern or Standard legal.
   - Check current ban lists and recent results on the web when legality or strength matters.
2. **Choose printings Playmat knows.** Each line is `QTY [SET:NUM] Card Name`, where SET and NUM come from a live
   (uncommented) `SetCardInfo` line in Playmat's `Mage.Sets/src/mage/sets/*.java`. Playmat's code is at
   https://github.com/arcanite24/playmat (shallow, sparse clone `Mage.Sets/src/mage/sets` to search it).
   Cards commented out there are not implemented yet: don't use them. Prefer printings with themed or premium art
   (extended art, borderless, showcase, Star Trek LCARS lands and so on) when the deck has a theme.
3. **Write `decks/<id>.dck`:** first line `NAME:<Title>`, then the main deck. Sideboard lines start with `SB: `.
   In Commander decks the commander goes on an `SB:` line.
4. **Add the manifest entry** to `decks/manifest.json`:
   ```json
   {
     "id": "kebab-case-id",
     "title": "Deck Title",
     "format": "Modern",
     "pitch": "One sentence on how the deck wins.",
     "file": "kebab-case-id.dck",
     "colors": "WR",
     "face": {"set": "TRK", "num": "7"},
     "tags": ["mytodayforever"],
     "added": "YYYY-MM-DD",
     "updated": "YYYY-MM-DD"
   }
   ```
   `colors` is the deck's color identity in WUBRG order. `face` is the printing whose art shows on the deck's box:
   the commander, or the deck's signature card. `tags` are lowercase words (letters, digits, hyphens) that group decks
   on the library page; each tag gets a filter chip. Current tags: `mytodayforever` (the original decks) and `terrafirma`.
   Ask which tag a new deck belongs under if the request doesn't say. When a deck changes, update its `.dck` and its `updated` date.
5. **Write the play guide** at `decks/guides/<id>.json`, shown on the deck page under "How to play":
   ```json
   {
     "wins": "One or two sentences on how the deck wins.",
     "plan": [["Turns 1–2", "What to do"], ["Turn 3", "..."], ["Win", "..."]],
     "keys": [["Exact Card Name", "Why it matters"]],
     "tips": ["Rules reminders and play tips"],
     "mulligan": "What a keepable hand looks like.",
     "sideboard": [["Opponent type", "Cards to bring in"]]
   }
   ```
   Names in `keys` become click-to-zoom links when they match a card in the deck (a short name before a comma,
   like "Captain Jean-Luc Picard", is fine). `sideboard` only for decks that have one. Update the guide when the
   list changes.
6. **Validate:** `python tools/validate.py --playmat <path to playmat checkout>` must report 0 errors.
7. **Commit and push to `main`.** GitHub Pages publishes within a minute or two.

## Things to keep

- The site must keep working with no build step: plain HTML, CSS and JavaScript, no frameworks.
- Card data comes from `https://api.scryfall.com/cards/collection` (batches of 75, by set and collector number,
  falling back to name), images from `cards.scryfall.io`. Respect Scryfall's guidance: keep the page's request rate
  low (it batches and caches in localStorage for 14 days), and keep the footer credit.
- XMage set codes are Scryfall's codes in upper case (`40K` is Scryfall's `40k`).
- Values from Scryfall and the .dck files are text, never markup: they go through `esc()` before joining HTML.

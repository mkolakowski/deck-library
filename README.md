# Deck Library

Magic: The Gathering decks built for a self-hosted [Playmat](https://github.com/arcanite24/playmat) server.
Each deck has its card art, a mana curve, a sortable card list, a click-to-zoom view, and a `.dck` download
that imports straight into Playmat.

Card data and images load live from [Scryfall](https://scryfall.com). Magic: The Gathering and its card art
are © Wizards of the Coast. This is an unofficial fan page.

## Decks

| Deck | Format | Tags |
|---|---|---|
| Starfleet Bridge Crew | Standard | mytodayforever |
| Section 31 Tactical Command | Standard | mytodayforever |
| Worf's Away Team | Commander | mytodayforever |
| Abaddon's Black Legion | Commander | mytodayforever |
| The Doctor's TARDIS Crew | Commander | mytodayforever |
| Living End | Modern | mytodayforever |
| Hammer Time | Modern | mytodayforever |
| Fleet Command | Modern | mytodayforever |
| Cryptid Sightings | Modern | mytodayforever |
| DS9: Defend the Station | Modern | mytodayforever |
| LOTR: Ride of the Rohirrim | Modern | mytodayforever |
| Gryffindor Courage | Modern | terrafirma |
| Leo's Squad (TMNT) | Standard | terrafirma |
| Pyromancer's Inferno | Modern | terrafirma |
| Team Avatar Allies | Standard | terrafirma |
| Whispering Hollow | Modern | terrafirma |
| Call of the Deep Dark | Modern | terrafirma |
| For the Horde | Modern | terrafirma |
| Scholomance Necromancers | Modern | terrafirma |
| Forest Friends Starter | Modern | terrafirma |

## Publishing with GitHub Pages

1. In the repository, go to **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**, branch **main**, folder **/ (root)**, and save.
3. The site appears at `https://<your-user>.github.io/<repo-name>/` a minute or two later.

## Adding or changing a deck

Drop the `.dck` into `decks/`, add an entry to `decks/manifest.json`, run the checks, commit and push.
`CLAUDE.md` has the full steps, so Claude Code can do all of it:

```bash
python tools/validate.py --playmat ../playmat   # 0 errors before pushing
```

To preview locally, serve the folder (opening `index.html` directly from disk won't load the decks):

```bash
python -m http.server 8000   # then open http://localhost:8000
```

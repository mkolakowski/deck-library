# Deck Library

**Browse the decks: [mkolakowski.github.io/deck-library/](https://mkolakowski.github.io/deck-library/)**

Magic: The Gathering decks built for a self-hosted [Playmat](https://github.com/arcanite24/playmat) server.
Each deck has its card art, a mana curve, a sortable card list, a click-to-zoom view, and a `.dck` download
that imports straight into Playmat.

Card data and images load live from [Scryfall](https://scryfall.com). Magic: The Gathering and its card art
are © Wizards of the Coast. This is an unofficial fan page.

## Decks

| Deck | Format | Tags | File |
|---|---|---|---|
| [Starfleet Bridge Crew](https://mkolakowski.github.io/deck-library/#starfleet-bridge-crew) | Standard | mytodayforever | [.dck](decks/starfleet-bridge-crew.dck) |
| [Section 31 Tactical Command](https://mkolakowski.github.io/deck-library/#section-31-tactical-command) | Standard | mytodayforever | [.dck](decks/section-31-tactical-command.dck) |
| [Worf's Away Team](https://mkolakowski.github.io/deck-library/#worf-s-away-team) | Commander | mytodayforever | [.dck](decks/worf-s-away-team.dck) |
| [Abaddon's Black Legion](https://mkolakowski.github.io/deck-library/#abaddon-s-black-legion) | Commander | mytodayforever | [.dck](decks/abaddon-s-black-legion.dck) |
| [The Doctor's TARDIS Crew](https://mkolakowski.github.io/deck-library/#the-doctor-s-tardis-crew) | Commander | mytodayforever | [.dck](decks/the-doctor-s-tardis-crew.dck) |
| [Living End](https://mkolakowski.github.io/deck-library/#living-end) | Modern | mytodayforever | [.dck](decks/living-end.dck) |
| [Hammer Time](https://mkolakowski.github.io/deck-library/#hammer-time) | Modern | mytodayforever | [.dck](decks/hammer-time.dck) |
| [Fleet Command](https://mkolakowski.github.io/deck-library/#fleet-command) | Modern | mytodayforever | [.dck](decks/fleet-command.dck) |
| [Cryptid Sightings](https://mkolakowski.github.io/deck-library/#cryptid-sightings) | Modern | mytodayforever | [.dck](decks/cryptid-sightings.dck) |
| [DS9: Defend the Station](https://mkolakowski.github.io/deck-library/#ds9-defend-the-station) | Modern | mytodayforever | [.dck](decks/ds9-defend-the-station.dck) |
| [LOTR: Ride of the Rohirrim](https://mkolakowski.github.io/deck-library/#lotr-ride-of-the-rohirrim) | Modern | mytodayforever | [.dck](decks/lotr-ride-of-the-rohirrim.dck) |
| [Gryffindor Courage](https://mkolakowski.github.io/deck-library/#gryffindor-courage) | Modern | terrafirma | [.dck](decks/gryffindor-courage.dck) |
| [Leo's Squad (TMNT)](https://mkolakowski.github.io/deck-library/#leos-squad-tmnt) | Standard | terrafirma | [.dck](decks/leos-squad-tmnt.dck) |
| [Pyromancer's Inferno](https://mkolakowski.github.io/deck-library/#pyromancers-inferno) | Modern | terrafirma | [.dck](decks/pyromancers-inferno.dck) |
| [Team Avatar Allies](https://mkolakowski.github.io/deck-library/#team-avatar-allies) | Standard | terrafirma | [.dck](decks/team-avatar-allies.dck) |
| [Whispering Hollow](https://mkolakowski.github.io/deck-library/#whispering-hollow) | Modern | terrafirma | [.dck](decks/whispering-hollow.dck) |
| [Call of the Deep Dark](https://mkolakowski.github.io/deck-library/#call-of-the-deep-dark) | Modern | terrafirma | [.dck](decks/call-of-the-deep-dark.dck) |
| [For the Horde](https://mkolakowski.github.io/deck-library/#for-the-horde) | Modern | terrafirma | [.dck](decks/for-the-horde.dck) |
| [Scholomance Necromancers](https://mkolakowski.github.io/deck-library/#scholomance-necromancers) | Modern | terrafirma | [.dck](decks/scholomance-necromancers.dck) |
| [Forest Friends Starter](https://mkolakowski.github.io/deck-library/#forest-friends-starter) | Modern | terrafirma | [.dck](decks/forest-friends-starter.dck) |

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

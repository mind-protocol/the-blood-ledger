# World Scraping — Design Patterns

**Version:** 1.0
**Status:** DESIGNING

---

## Core Principle

**The world existed before you. It will exist after. You are entering a story already in motion.**

---

## Pattern: Authentic England 1067

The player enters a world that was there before them.
Real geography. Real politics. Real people in real places.
Not generated — discovered.

### Feelings Created

- **"This place is real"** — York is where York should be
- **"History happened here"** — The Harrying was last year
- **"I'm small in something large"** — 200+ places, 100+ people
- **"The world doesn't need me"** — Politics, tensions, events predate player

### Anti-Patterns

- Generic fantasy geography
- Empty world waiting to be filled
- Player as center of all events
- Historically implausible situations

---

## Behaviors: What The Player Experiences

### Geography Feels Real

**Pattern:** York is north of London. The Humber is a real barrier.

**Evidence:**
- Travel times match real distances
- Rivers block routes where rivers exist
- Roman roads are faster (they were)
- Terrain matches landscape (moors, fens, forests)

### Politics Make Sense

**Pattern:** Norman lords hold castles. Saxons are dispossessed.

**Evidence:**
- Malet holds York (he did)
- Saxon thegns lost their lands (they did)
- Church retains some power (it did)
- Resistance centers match history (North)

### Characters Belong

**Pattern:** People are where they should be, doing what they would do.

**Evidence:**
- Historical figures in correct locations
- Political relationships match 1067
- Motivations follow from history
- Minor characters fit their contexts

### Time Is Grounded

**Pattern:** One year after Hastings. The Harrying just ended.

**Evidence:**
- Recent events referenced correctly
- Political situation matches moment
- Wounds are fresh (burned villages)
- Future events can be foreshadowed

---

## Target Density

| Data Type | Target Count |
|-----------|--------------|
| Places | ~215 |
| Routes | ~400 |
| Characters | ~120 (70 historical) |
| Narratives | ~250 |
| Beliefs | ~800 |
| Tensions | ~50 |

---

## Related Documents

- `ALGORITHM_Pipeline.md` — Five-phase scraping pipeline
- `ALGORITHM_Geography.md` — Phase 1: Places & Routes
- `ALGORITHM_Political.md` — Phase 2: Who Holds What
- `ALGORITHM_Events.md` — Phase 3: What Happened
- `ALGORITHM_Narratives.md` — Phase 4: Stories & Knowledge
- `ALGORITHM_Tensions.md` — Phase 5: What's About To Break
- `VERIFICATION_Tests.md` — How we know it worked
- `SYNC_World_Scraping.md` — Current state & progress

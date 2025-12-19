# World Scraping — Design Patterns

**Version:** 1.0
**Status:** DESIGNING

---

## CHAIN

```
THIS:            PATTERNS_World_Scraping.md (you are here)
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
TEST:            ./TEST_World_Scraping.md
SYNC:            ./SYNC_World_Scraping.md
IMPL:            data/scripts/scrape/phase1_geography.py
```

---

## Core Principle

**The world existed before you. It will exist after. You are entering a story already in motion.**

---

## The Problem

The game needs a believable 1067 England that feels authored by history, not
by the player or procedural noise, and it must be consistent enough to support
travel, politics, and social tension without constant manual repair.

---

## The Pattern

Use a phase-based scraping pipeline that captures real geography, political
control, people, narratives, and tensions as YAML sources, then inject the
resulting records into the graph to seed a coherent world state.

---

## Principles

- Prefer real historical anchors (places, dates, actors) over invented ones.
- Treat geography as constraint, not decoration, so routes feel inevitable.
- Encode social context (holdings, narratives, tensions) alongside locations.
- Preserve auditability through YAML intermediates before injection.

---

## Dependencies

- `data/scripts/scrape/**` phase scripts for gathering and transforming data.
- `data/world/**` YAML outputs as the canonical intermediate artifacts.
- `data/scripts/inject_world.py` for loading YAML into FalkorDB.
- External sources (OSM/Nominatim, historical references) for accuracy.

---

## Inspirations

- Domesday-era historiography that grounds who holds what, where, and why.
- Cartographic realism from medieval atlases and river/road constraints.
- Narrative worldbuilding that emphasizes pre-existing conflicts and scars.

---

## Scope

In scope: scraping and compiling 1067 England geography, holdings, people,
events, narratives, beliefs, and tensions into YAML outputs that seed the
graph. Out of scope: live web scraping at runtime, alternate eras, or
procedural world generation beyond the curated dataset.

---

## Gaps / Ideas / Questions

- Need a clear provenance rule for multi-source claims per record.
- OpenDomesday API outage remains a risk to future updates.
- Consider a lightweight validation script for cross-file consistency.

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

- `ALGORITHM_Pipeline.md` — Five-phase scraping pipeline (all phases consolidated)
- `VALIDATION_World_Scraping.md` — How we know it worked
- `IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` — Pipeline code layout and data flow
- `TEST_World_Scraping.md` — Test coverage and gaps
- `SYNC_World_Scraping.md` — Current state & progress

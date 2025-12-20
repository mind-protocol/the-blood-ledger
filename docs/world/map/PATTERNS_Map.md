# Map System — Patterns: Why This Design

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Core Insight

**The map is not a GPS; it is a traveler’s knowledge.**
The map expands with discovery and reflects belief, not omniscience.

---

## THE PROBLEM

Players need spatial orientation and travel intent without breaking the
story's uncertainty. A literal, complete map collapses mystery and makes
exploration feel solved before it starts, while no map leaves players lost
and reduces willingness to take narrative travel risks.

---

## THE PATTERN

Represent the map as a knowledge artifact that grows with discovery and
rumor. The UI renders only what the player has earned, using layered
parchment visuals to keep the map legible without claiming certainty, and
the semantic search layer supports discovery without implying omniscience.

---

## PRINCIPLES

### Principle 1: Knowledge over certainty

The map mirrors what the player knows, not what exists. This preserves
curiosity and keeps discovery meaningful across long playthroughs.

### Principle 2: Scale hierarchy

Places nest by scale so traversal decisions stay clear. This keeps travel
choices grounded in narrative scale rather than raw coordinates.

### Principle 3: Routes are real

Travel uses explicit routes with distance and difficulty. This anchors time
costs and ensures travel feels like a deliberate narrative beat.

### Principle 4: Hand-drawn, layered rendering

Layered rendering separates static parchment detail from dynamic fog and
markers, keeping performance stable while preserving the hand-drawn tone
that signals the map is interpretive rather than exact.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `engine/infrastructure/embeddings/**` | Provides query embeddings for semantic search. |
| Graph runtime (ngram repo) | Supplies graph queries for place and route records (see `data/ARCHITECTURE — Cybernetic Studio.md`). |
| `docs/frontend/map/` | Defines canvas rendering and interaction contracts. |

---

## INSPIRATIONS

Hand-drawn tabletop maps, fog-of-war exploration in RPGs, and narrative
travel systems where uncertainty is a feature. The aesthetic borrows from
parchment atlases and annotated expedition charts.

---

## SCOPE

### In Scope

- Knowledge-driven visibility and rumor rendering.
- Route-based travel intent and selection signals.
- Layered rendering decisions for legibility and cacheability.

### Out of Scope

- Real-time pathfinding or GPS-style precision; see physics movement systems.
- Full world simulation or automatic travel animation; travel is narrated.
- Authoritative world state editing; the map is read-only by design.

---

## What the Map Is Not

- **Not a mini-game**: it serves story flow.
- **Not real-time**: travel is narrated, not animated continuously.
- **Not complete**: fog of war and rumor inaccuracies remain.

---

## System Boundaries

### Graph
- Places and routes are stored as nodes/links.
- The map reads from the graph but does not mutate it.

### Narrator / World Runner
- Map emits selection/travel intents.
- Narrator decides the story response and triggers travel.

### Visibility State
- Player-specific knowledge is stored per playthrough.
- Visibility controls rendering, not underlying data truth.

---

## Summary

The map is a narrative instrument: it rewards exploration, respects uncertainty,
and remains legible through layered, hand-crafted rendering.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide how rumor confidence decays over time and reflects in UI styling.
- [ ] Define the visibility data contract that feeds the frontend map renderer.
- IDEA: Add a lightweight legend overlay that surfaces route difficulty cues.
- QUESTION: Where should per-playthrough visibility state live server-side?

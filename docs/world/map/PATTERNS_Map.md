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

## Design Principles (Canonical)

1. **Knowledge over certainty**
   - Unknown places do not appear.
   - Rumors appear faded and imprecise.

2. **Scale hierarchy**
   - Region → settlement → district → building → room.
   - Movement within a settlement is free; between settlements requires routes.

3. **Routes are real**
   - Routes are polylines with distance, time, and difficulty.
   - Travel time is consistent and narrative-relevant.

4. **Hand-drawn aesthetic**
   - Parchment texture, wobbled lines, seeded randomness.

5. **Layered rendering**
   - Each canvas layer has one responsibility.
   - Static layers cached; dynamic layers re-render.

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


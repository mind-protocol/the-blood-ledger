# Map System — Algorithm: Overview

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
RENDERING:       ./ALGORITHM/ALGORITHM_Rendering_Pipeline.md
PLACES:          ./ALGORITHM/ALGORITHM_Places.md
ROUTES:          ./ALGORITHM/ALGORITHM_Routes.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Purpose

Define the canonical logic for map rendering, place/route representation, and movement rules.
This overview is the entry point; see part files for details.

---

## Rendering Summary

1. Build static layers once: parchment, coastline, routes.
2. Build dynamic layers per frame: fog, markers, overlay UI.
3. Apply projection for all coordinates.
4. Use seeded jitter for hand-drawn effect (deterministic per feature).
5. Cache static layers; redraw dynamic layers each frame.

See: `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md`.

---

## Places and Routes Summary

### Places
- Places are graph nodes with coordinates, scale, type, and descriptive fields.
- Places form a containment hierarchy via `CONTAINS` links.
- Visibility level controls display, not data truth.

### Routes
- Routes are graph links with waypoints and road metadata.
- Distance computed from waypoint polyline (haversine per segment).
- Travel time derived from distance and road type speed.

See:
- `docs/world/map/ALGORITHM/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Routes.md`

---

## Inputs and Outputs

**Inputs:** place nodes, route links, player visibility state, player location.
**Outputs:** canvas layers + interaction events (select, hover, travel request).

---

## Constraints

- Rendering is layered; each layer has one responsibility.
- Map shows player knowledge, not omniscience.
- Routes exist only when endpoints are known or traveled.

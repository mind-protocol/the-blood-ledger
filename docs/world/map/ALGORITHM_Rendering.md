# Map System — Algorithm: Rendering

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
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md
THIS:            ./ALGORITHM_Rendering.md

IMPL:            engine/world/map/semantic.py
---

## OVERVIEW

This document summarizes the rendering algorithm for the map UI so the
pipeline remains discoverable from the root map docs. The detailed, canonical
step ordering lives in `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md`
while this file captures the template-required structure and intent.

---

## DATA STRUCTURES

Rendering uses a layered canvas model: `RenderLayer` records the draw order,
cache key, and dependency flags (static vs dynamic). `MapFeature` encapsulates
place or route geometry with visibility metadata, while `VisibilityState`
provides per-playthrough discovery and rumor levels. A `ProjectionBounds`
structure stores min/max lat-lng and canvas scale to convert coordinates
consistently across layers.

---

## ALGORITHM: RenderMapFrame

1. Load place and route features plus the current visibility state.
2. Build or reuse cached static layers (parchment, coastline, routes).
3. Project all features into canvas space with the shared bounds.
4. Render dynamic layers (fog, markers, labels, overlays) each frame.
5. Store projected positions for hit testing and UI interactions.

---

## KEY DECISIONS

- Layered rendering keeps visual responsibilities isolated and cacheable.
- Deterministic jitter uses stable seeds to keep the hand-drawn look without
  frame-to-frame flicker.
- Visibility is a render-time filter; hidden places remain in data but are
  suppressed in draw passes and hit tests.

---

## DATA FLOW

Graph-derived features (places/routes) and playthrough visibility feed the
projection stage, which produces cached static layers and per-frame dynamic
layers. The renderer outputs a composed canvas plus a set of projected points
used by the UI for hover, selection, and travel intent events.

---

## COMPLEXITY

Per-frame work is roughly O(P + R) for places and routes; cached static layers
reduce repeated work when underlying data is unchanged. Hit testing is O(P)
with a simple radius check; a spatial index can reduce this if needed.

---

## HELPER FUNCTIONS

- `ProjectLatLngToCanvas(bounds, latLng)` maps coordinates into canvas space.
- `BuildStaticLayers(features)` renders parchment, coastline, and route layers.
- `DrawFogOfWar(state)` fills unrevealed areas with the fog mask.
- `DrawPlaceIcons(features)` renders icons and labels based on visibility.
- `HitTestPlace(projectedPoints, cursor)` resolves hover/select targets.

---

## INTERACTIONS

The renderer consumes semantic map data from `engine/world/map/semantic.py`
queries and surfaces hover/select/travel events to the frontend map UI.
It does not mutate graph state; travel intent is forwarded to narrator/world
runner systems for actual story progression.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm the authoritative data contract for visibility and rumor states.
- [ ] Decide whether route hit testing should be added for richer UI feedback.
- IDEA: Add a shared cache key strategy so backend and frontend agree on when
  static layers can be reused.

# Map System — Sync: Current State

```
STATUS: DESIGNING
UPDATED: 2025-12-20
```

## MATURITY

STATUS: DESIGNING

What's canonical (v1):
- Semantic search entry points and graph query hooks are implemented.
- Documentation chain exists and is kept within size limits via archives.

## CURRENT STATE

### Implemented
- **Semantic search** via `engine/world/map/semantic.py`.
- **FalkorDB integration** through GraphQueries.

### Not Implemented
- Visual map rendering (canvas layers, fog, icons).
- Visibility/knowledge tracking per playthrough.

## RECENT CHANGES

### 2025-12-20: Consolidated Map Rendering Algorithms

- **What:** Removed `docs/world/map/ALGORITHM_Rendering.md` and kept
  `docs/world/map/ALGORITHM_Map.md` plus
  `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md` as the canonical
  rendering algorithm docs.
- **Why:** Eliminate duplicate ALGORITHM docs in the map folder.
- **Impact:** Rendering algorithm now has a single authoritative location.

### 2025-12-20: Consolidated Map Syncs

- **What:** Removed `docs/frontend/map/SYNC_Map_View.md` and repointed the
  frontend map patterns to this canonical sync.
- **Why:** Keep a single source of truth for map status and avoid duplicate
  SYNC entries.
- **Impact:** Frontend map view patterns now link here for status updates.

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Map_Code_Architecture.md` and updated `TEST_Map_Test_Coverage.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** Map module documentation is now compliant; Health checks are anchored to semantic search results.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code. Focus on keeping the map doc chain aligned with `engine/world/map/semantic.py` and plan the visibility state contract before wiring the frontend map to live data.

## TODO

- [ ] Define the map visibility/knowledge storage location and schema.
- [ ] Implement visual map rendering (frontend canvas layers).

## POINTERS

- `docs/world/map/PATTERNS_Map.md` for the core "traveler's knowledge" insight.
- `docs/frontend/map/PATTERNS_Parchment_Map_View.md` for the parchment map UI
  view pattern.
- `engine/world/map/semantic.py` for the current implementation.

## CHAIN

```
THIS:            SYNC_Map.md (you are here)
PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
```

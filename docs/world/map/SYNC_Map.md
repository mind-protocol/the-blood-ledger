# Map System — Sync: Current State

```
LAST_UPDATED: 2025-12-19
STATUS: Partial implementation - semantic search complete, visual map pending
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
THIS:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Current State

### Implemented
- **Semantic search** via `engine/world/map/semantic.py`.
- **FalkorDB integration** through GraphQueries.

### Not Implemented
- Visual map rendering (canvas layers, fog, icons).
- Visibility/knowledge tracking per playthrough.
- Place/route data loading for the frontend map UI.

Frontend map UI exists under `frontend/components/map` but is static demo data.

---

## Documentation Status

| Doc | Purpose | Status |
|-----|---------|--------|
| `PATTERNS_Map.md` | Why this design | Updated, concise |
| `BEHAVIORS_Map.md` | Visibility, interaction | Updated, concise |
| `ALGORITHM_Map.md` | Entry point | New split |
| `ALGORITHM/ALGORITHM_Rendering_Pipeline.md` | Rendering pipeline | New split |
| `ALGORITHM/ALGORITHM_Places.md` | Places | New split |
| `ALGORITHM/ALGORITHM_Routes.md` | Routes | New split |
| `VALIDATION_Map_Invariants.md` | Semantic search invariants | Current |
| `IMPLEMENTATION_Map_Code_Architecture.md` | Code architecture | Current |
| `TEST_Map_Test_Coverage.md` | Test coverage | Current |
| `SYNC_Map.md` | Current state | This file |

---

## Recent Changes

### 2025-12-19: Reduced map documentation size

- Split large algorithm doc into focused parts.
- Removed duplicated and verbose sections; kept canonical logic.
- Updated CHAIN references to new algorithm entry point.

Files:
- `docs/world/map/ALGORITHM_Map.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Routes.md`
- `docs/world/map/PATTERNS_Map.md`
- `docs/world/map/BEHAVIORS_Map.md`
- `docs/world/map/SYNC_Map.md`

### 2025-12-19: Expanded flaky test note

- Expanded the FLAKY TESTS section in `docs/world/map/TEST_Map_Test_Coverage.md`
  to meet the template length requirement without changing test status.

### 2025-12-19: Expanded test coverage template note

- Clarified the flaky test tracking status in the map test coverage doc.

Files:
- `docs/world/map/TEST_Map_Test_Coverage.md`

---

## Agent Observations

### Remarks
- The algorithm spec was duplicated and overly verbose, obscuring canonical rules.

### Suggestions
- [ ] Add automated tests for semantic search to match VALIDATION invariants.
- [ ] Revisit frontend map integration once backend visibility state exists.

### Propositions
- Consider a shared map data loader service to connect graph data to UI.

---

## ARCHIVE

Older content archived to: `docs/world/map/archive/SYNC_archive_2024-12.md`

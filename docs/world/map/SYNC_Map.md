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

## MATURITY

STATUS: DESIGNING

What's canonical (v1):
- Semantic search entry points and graph query hooks are implemented.
- Documentation chain exists and is kept within size limits via archives.

What's still being designed:
- Player-visible map rendering and knowledge/visibility persistence.
- Backend-to-frontend contract for map discovery state.

What's proposed (v2):
- Unified map data loader service shared by backend and UI layers.

---

## CURRENT STATE

### Implemented
- **Semantic search** via `engine/world/map/semantic.py`.
- **FalkorDB integration** through GraphQueries (ngram repo graph runtime).

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
| `ALGORITHM_Map.md` | Canonical algorithm | Consolidated |
| `ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md` | Rendering pipeline | Reference stub |
| `ALGORITHM/places/ALGORITHM_Places.md` | Places | Reference stub |
| `ALGORITHM/routes/ALGORITHM_Routes.md` | Routes | Reference stub |
| `VALIDATION_Map_Invariants.md` | Semantic search invariants | Current |
| `IMPLEMENTATION_Map_Code_Architecture.md` | Code architecture | Current |
| `TEST_Map_Test_Coverage.md` | Test coverage | Current |
| `SYNC_Map.md` | Current state | This file |

---

## RECENT CHANGES

### 2025-12-20: Note graph runtime location in map docs

- **What:** Updated GraphQueries references to call out the ngram repo graph runtime.
- **Why:** The graph runtime was moved out of this repo.
- **Impact:** Map docs now reference the authoritative runtime location.

### 2025-12-20: Add HEALTH doc for semantic search

- **What:** Added `HEALTH_Map.md` for semantic search verification.
- **Why:** Close the doc chain gap flagged by `ngram validate`.
- **Impact:** Map module now has a HEALTH doc placeholder with manual checks.

### 2025-12-20: Reorganized map algorithm subdocs

- **What:** Moved map algorithm subdocs into `docs/world/map/ALGORITHM/{places,routes,rendering}/` and updated CHAIN links.
- **Why:** Resolve duplicate ALGORITHM docs in a single folder.
- **Impact:** Map algorithm references now point to subfolder paths.

### 2025-12-20: Consolidated Rendering Algorithm Docs

- **What:** Moved the rendering algorithm details into the rendering pipeline doc and trimmed the overview to a pointer summary.
- **Why:** Remove duplicate ALGORITHM content between the overview and rendering-specific docs.
- **Files:** `docs/world/map/ALGORITHM_Map.md`, `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`

### 2025-12-20: Map rendering algorithm consolidation

- Removed `docs/world/map/ALGORITHM_Rendering.md` so rendering docs live in
  `docs/world/map/ALGORITHM_Map.md` and
  `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`.

### 2025-12-20: Consolidated map algorithm docs

- Merged Places, Routes, and Rendering algorithms into `docs/world/map/ALGORITHM_Map.md`.
- Converted part files into reference stubs to eliminate duplicate ALGORITHM docs.

## IN PROGRESS

- Aligning the map module SYNC template with required sections while keeping
  the implementation status unchanged; visual map rendering remains pending.

## Agent Observations

### Remarks
- The algorithm spec was duplicated and overly verbose, obscuring canonical rules.
- The map patterns doc now follows the template without redundant sections.

### Suggestions
- [ ] Add automated tests for semantic search to match VALIDATION invariants.
- [ ] Revisit frontend map integration once backend visibility state exists.

### Propositions
- Consider a shared map data loader service to connect graph data to UI.

---

## GAPS

- Completed: Expanded `docs/world/map/PATTERNS_Map.md` with missing template
  sections and recorded the change here for repair #16.
- Remaining: Commit the doc updates once the worktree scope is clarified.
- Blocker: Pre-existing uncommitted changes make it unsafe to commit without
  confirmation on which files to include.

---

## ARCHIVE

Older content archived to: `docs/world/map/archive/SYNC_archive_2024-12.md`

---

## KNOWN ISSUES

- No functional regressions noted, but the visual map is still a static demo
  on the frontend and the backend visibility state remains unimplemented.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code. Focus on keeping the map doc chain
aligned with `engine/world/map/semantic.py` and plan the visibility state
contract before wiring the frontend map to live data.

## HANDOFF: FOR HUMAN

No immediate decision required, but confirm whether visibility state should
live in the graph or in a per-playthrough store before backend work begins.

## TODO

- [ ] Define the map visibility/knowledge storage location and schema so the
  frontend can transition from demo data to live graph-backed responses.

## CONSCIOUSNESS TRACE

The module feels stable at the semantic search layer, but uncertainty remains
around where discovery state should live; that decision gates integration.

## POINTERS

- Implementation entry: `engine/world/map/semantic.py` for current map queries.
- Frontend surface: `frontend/components/map/MapClient.tsx` for UI integration.


---

## ARCHIVE

Older content archived to: `SYNC_Map_archive_2025-12.md`

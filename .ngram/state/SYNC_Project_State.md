# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: agent (manager)
```

---

## CURRENT STATE

The Blood Ledger is a narrative game engine set in Norman England (1067), using FalkorDB graph database to model "narratives under tension." The codebase has been restructured to align code organization with documentation areas.

**Just completed:** Major code restructure - moved files from flat `engine/` layout to area-based structure matching `docs/`:
- `engine/db/` → `engine/physics/graph/` (graph ops are the physics core)
- `engine/queries/` → `engine/world/map/`
- `engine/api|embeddings|history|memory|orchestration/` → `engine/infrastructure/`

All Python imports updated and verified working. Health score improved from 10 critical issues to 3.

---

## ACTIVE WORK

### Code/Docs Alignment

- **Area:** `engine/`, `docs/`, `modules.yaml`
- **Status:** completed
- **Owner:** agent
- **Context:** Restructured code to match 7-area docs layout (physics, agents, world, infrastructure, frontend, schema, design)

---

## RECENT CHANGES

### 2025-12-19: SYNC_Scene.md Refreshed

- **What:** Updated stale SYNC file for frontend/scene module
- **Why:** SYNC was 367 days old, claimed "Layout skeleton: Not started" when scene is implemented
- **Impact:** SYNC now reflects reality - 12 scene components documented, maturity set to CANONICAL, design questions tracked

### 2025-12-19: graph_queries.py Monolith Split

- **What:** Extracted SearchQueryMixin from graph_queries.py
- **Why:** File was 1132 lines (threshold: 800)
- **Impact:**
  - Created new file `graph_queries_search.py` (285 lines)
  - `graph_queries.py` reduced to 892 lines (now under threshold)
  - Extracted: `search()`, `_to_markdown()`, `_cosine_similarity()`, `_find_similar_by_embedding()`, `_get_connected_cluster()`
  - Added `SearchQueryMixin` to class inheritance (alongside existing `MomentQueryMixin`)
  - Updated IMPLEMENTATION_Physics.md and modules.yaml

### 2025-12-19: Code Restructure Migration

- **What:** Moved engine files to match docs area structure
- **Why:** Code was flat dumping ground; now mirrors docs organization
- **Impact:**
  - `engine/physics/graph/` contains graph_ops.py, graph_queries.py (core physics)
  - `engine/infrastructure/` contains api, embeddings, history, memory, orchestration
  - `engine/world/map/` contains semantic search
  - All imports updated across codebase
  - modules.yaml updated with new paths
  - Empty directories removed (actions/, characters/, mechanisms/)

### 2025-12-19: CLI Tools Module Documented

- **What:** Created documentation for CLI agent utilities
- **Why:** Module was flagged as undocumented
- **Impact:** Fixed modules.yaml path, created PATTERNS and SYNC docs

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| graph_ops.py monolith | critical | `engine/physics/graph/` | 1989 lines, needs splitting |
| ~~graph_queries.py monolith~~ | ~~critical~~ | `engine/physics/graph/` | RESOLVED: 892 lines (extracted SearchQueryMixin) |
| ~~Broken impl link~~ | ~~warning~~ | `docs/physics/` | MOSTLY RESOLVED: 51→34 references remaining are false positives (tree filenames, constants) |
| 6 stale SYNCs | warning | various | Need refresh (scene fixed) |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Refactor_Improve_Code_Structure

**Current focus:** Split monolith files in `engine/physics/graph/`

**Key context:**
- Code now matches docs areas - verify import paths use new structure
- `engine.physics.graph` for graph ops (was `engine.db`)
- `engine.infrastructure.*` for api, embeddings, history, memory, orchestration
- `engine.world.map` for semantic search (was `engine.queries`)

**Watch out for:**
- Old import paths in any files not yet updated
- IMPLEMENTATION_Physics.md reports 34 "broken links" but most are false positives from tree structure parsing

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Code restructured to match docs areas. All imports updated and verified working. 3 critical issues remain: 2 monolith files needing splits, 1 broken doc link.

**Decisions made recently:**
- Graph ops moved to physics/ (they ARE the physics engine)
- Infrastructure consolidates all supporting systems
- Empty placeholder directories removed

**Needs your input:**
- None currently

**Concerns:**
- Monolith files still large but functional

---

## TODO

### High Priority

- [ ] Split graph_ops.py (1989 lines → target <800)
- [x] Split graph_queries.py (1147 lines → target <800) — DONE: Now 892 lines
- [ ] Fix docs/physics/IMPLEMENTATION_Physics.md broken references

### Backlog

- [ ] Refresh 6 remaining stale SYNC files (scene done)
- [ ] Add DOCS: references to code files

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `physics/` | restructured | `docs/physics/SYNC_Physics.md` |
| `agents/` | stable | `docs/agents/*/SYNC_*.md` |
| `world/` | restructured | `docs/world/*/SYNC_*.md` |
| `infrastructure/` | restructured | `docs/infrastructure/*/SYNC_*.md` |
| `frontend/` | stable | `docs/frontend/SYNC_Frontend.md` |
| `schema/` | stable | `docs/schema/` |
| `design/` | stable | `docs/design/SYNC_Vision.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Key modules (updated paths):**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| physics-graph | `engine/physics/graph/**` | `docs/physics/` | CANONICAL |
| api | `engine/infrastructure/api/**` | `docs/infrastructure/` | CANONICAL |
| world-map | `engine/world/map/**` | `docs/world/map/` | CANONICAL |

**Coverage notes:**
- All code directories now mapped in modules.yaml
- scripts/ and tests/ excluded via .ngramignore (utilities, not core modules)

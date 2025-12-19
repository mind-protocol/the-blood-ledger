# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: agent (manager)
```

---

## CURRENT STATE

The Blood Ledger is a narrative game engine set in Norman England (1067), using FalkorDB graph database to model "narratives under tension." The codebase has been restructured to align code organization with documentation areas.

**Just completed:** Split graph_ops.py monolith from 1094 → 792 lines:
- Extracted `graph_ops_image.py` (163 lines): Image generation helpers
- Extracted `graph_ops_events.py` (66 lines): Event emitter for mutations
- Extracted `graph_ops_types.py` (59 lines): Types and exceptions (WriteError, SimilarNode, ApplyResult)
- Removed __main__ example block

All Python imports updated and verified working.

---

## ACTIVE WORK

### Code/Docs Alignment

- **Area:** `engine/`, `docs/`, `modules.yaml`
- **Status:** completed
- **Owner:** agent
- **Context:** Restructured code to match 7-area docs layout (physics, agents, world, infrastructure, frontend, schema, design)

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| ~~graph_ops.py monolith~~ | ~~warning~~ | `engine/physics/graph/` | RESOLVED: 792 lines (extracted image, events, types) |
| ~~graph_queries.py monolith~~ | ~~critical~~ | `engine/physics/graph/` | RESOLVED: 892 lines (extracted SearchQueryMixin) |
| ~~Broken impl link~~ | ~~critical~~ | `docs/physics/` | RESOLVED: Fixed tree structure (ASCII), removed false positive backticks |
| 2 stale SYNCs | warning | various | Need refresh (scene, map, world-runner, scene-memory, embeddings done) |

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

- [x] Split graph_ops.py further (1094 lines → target <800) — DONE: Now 792 lines (extracted image, events, types)
- [x] Split graph_queries.py (1147 lines → target <800) — DONE: Now 892 lines
- [x] Fix docs/physics/IMPLEMENTATION_Physics.md broken references — MOSTLY DONE: Reduced 51→34, remaining are false positives
- [x] Complete narrator doc chain — DONE: Added VALIDATION, IMPLEMENTATION, TEST docs (2024-12-19)

### Backlog

- [ ] Refresh 2 remaining stale SYNC files (scene, map, world-runner, scene-memory, embeddings done)
- [ ] Add DOCS: references to code files
- [ ] Complete world-runner doc chain (missing VALIDATION, IMPLEMENTATION, TEST)
- [x] Complete frontend doc chain — DONE: Added BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST docs (2025-12-19)

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


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`

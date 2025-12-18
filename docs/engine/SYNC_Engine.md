# Engine — Sync

```
LAST_UPDATED: 2024-12-17
UPDATED_BY: Codex agent
STATUS: Specification ahead of implementation
```

---

## Document Chain

| Doc | Purpose |
|-----|---------|
| PATTERNS_Engine.md | Architecture philosophy (graph-first, orchestrators) |
| BEHAVIORS_Engine.md | Observable guarantees (fast startup, deterministic ops) |
| ALGORITHM_Engine.md | Request + startup flow |
| TEST_Engine.md | Coverage + gaps |
| SYNC_Engine.md | State + handoffs |

---

## Current State

- FastAPI app + GraphOps/GraphQueries exist and reference documentation.
- **Moment Graph Phase 1 COMPLETE**: Core graph operations, queries, traversal, and surface mechanics implemented.
- New `/api/moments/*` endpoints available alongside legacy scene.json endpoints.
- Infrastructure readiness: FalkorDB docker container, local `run.py` helper, SSE scaffolding.

### Moment Graph Implementation
| Component | Status | Location |
|-----------|--------|----------|
| MomentQueries | DONE | `engine/moment_graph/queries.py` |
| MomentTraversal | DONE | `engine/moment_graph/traversal.py` |
| MomentSurface | DONE | `engine/moment_graph/surface.py` |
| API Endpoints | DONE | `engine/api/moments.py` |
| Frontend Components | DONE | `frontend/components/moment/` |
| useMoments Hook | DONE | `frontend/hooks/useMoments.ts` |

---

## Open Questions

1. When to cut over from scene.json to moment graph queries?
2. How should orchestrator caches survive process restarts (persisted vs in-memory)?
3. What load testing strategy ensures FalkorDB stays under latency budgets?

---

## Work Queue

| Priority | Task | Owner | Status / Notes |
|----------|------|-------|----------------|
| P0 | Implement `get_current_view` + `/api/view` endpoint | Backend | ✅ `GraphQueries.get_player_location` + FastAPI route |
| P0 | Ensure GraphOps covers moment helpers | Backend | ✅ Already available (`add_moment`, `add_can_lead_to`, etc.) |
| P1 | Integration tests for API + GraphOps | Backend QA | ✅ `engine/tests/test_moments_api.py` |
| P1 | SSE stream for moment updates | Backend | ✅ `engine/api/moments.py` GET /stream/{id} |
| P1 | Mount moments router fully in app.py | Backend | ✅ Mounted at `/api/moments/*` in app.py:204 |
| P2 | Deprecate legacy `/api/scene/*` endpoints | Backend | TODO – Remove after frontend migration |
| P2 | Update Narrator to output moments | Backend | TODO – Phase 2 integration |

Update owners/ETA when tasks assigned or complete.
```

# Moment Graph Architecture Review

```
REVIEWED: 2024-12-17
STATUS: Implementation complete, refactoring recommendations included
```

---

## Current Architecture Overview

The Moment Graph system is implemented across multiple layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  frontend/types/moment.ts          TypeScript definitions        │
│  frontend/components/moment/       UI components                  │
│  frontend/hooks/useMoments.ts      State management               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  engine/api/app.py                 Main FastAPI app              │
│  engine/api/moments.py             Moments router (mounted)      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Engine Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  engine/moment_graph/              Specialized package           │
│    ├── queries.py                  MomentQueries class           │
│    ├── traversal.py                MomentTraversal class         │
│    └── surface.py                  MomentSurface class           │
│                                                                   │
│  engine/db/                        Core database layer           │
│    ├── graph_ops.py                GraphOps (2491 lines)         │
│    └── graph_queries.py            GraphQueries (1719 lines)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                 │
├─────────────────────────────────────────────────────────────────┤
│  FalkorDB (Redis-based graph database)                          │
│  Moment nodes, CAN_SPEAK/ATTACHED_TO/CAN_LEAD_TO links          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Locations

### Core Graph Operations (engine/db/graph_ops.py)

| Method | Lines | Purpose |
|--------|-------|---------|
| `add_moment()` | 1372-1466 | Create Moment node |
| `add_can_speak()` | 1552-1580 | CHARACTER -> MOMENT link |
| `add_attached_to()` | 1582-1619 | MOMENT -> Target link |
| `add_can_lead_to()` | 1621-1693 | MOMENT -> MOMENT traversal |
| `handle_click()` | 1695-1840 | Hot path click handler |
| `update_moment_weight()` | 1842-1905 | Weight manipulation |
| `propagate_embedding_energy()` | 1907-1985 | Semantic propagation |

### Core Graph Queries (engine/db/graph_queries.py)

| Method | Lines | Purpose |
|--------|-------|---------|
| `get_current_view()` | 1347-1408 | Main view query |
| `get_live_moments()` | 1410-1490 | Presence-gated query |
| `resolve_speaker()` | 1492-1524 | Speaker resolution |
| `get_available_transitions()` | 1526-1562 | CAN_LEAD_TO query |
| `get_clickable_words()` | 1564-1601 | Word extraction |

### Specialized Package (engine/moment_graph/)

| Class | File | Purpose |
|-------|------|---------|
| `MomentQueries` | queries.py | Higher-level view queries |
| `MomentTraversal` | traversal.py | Click handling, status transitions |
| `MomentSurface` | surface.py | Weight management, surfacing logic |

---

## Architectural Observations

### 1. Duplication Between Layers

**Issue:** Some functionality is duplicated between `engine/db/` and `engine/moment_graph/`.

| Operation | graph_ops.py | moment_graph/traversal.py |
|-----------|--------------|---------------------------|
| Handle click | `handle_click()` | `handle_click()` |
| Update status | (inline in methods) | `_update_status()` |
| Boost weight | (inline) | `_boost_weight()` |

**Recommendation:** Consolidate to single source of truth. Either:
- Option A: `engine/db/` handles all graph ops, `engine/moment_graph/` is thin wrapper
- Option B: Move all moment logic to `engine/moment_graph/`, keep `engine/db/` generic

### 2. File Size Concerns

| File | Lines | Concern |
|------|-------|---------|
| graph_ops.py | 2491 | Single file doing too much |
| graph_queries.py | 1719 | Approaching maintenance threshold |
| app.py | 1468 | Many inline endpoints |

**Recommendation:** Split by domain:
```
engine/db/
├── base.py          # Connection, base query
├── node_ops.py      # Character, Place, Thing, Narrative
├── link_ops.py      # Belief, Presence, Geography
├── moment_ops.py    # All moment operations
└── query_base.py    # Core query helpers
```

### 3. Consistent API Patterns

**Current State:** Two API patterns exist:
- `/api/moment/*` endpoints in app.py (lines 458-550)
- `/api/moments/*` router in moments.py

**Recommendation:** Unify under single pattern:
- Use `/api/moments/*` (plural, RESTful)
- Deprecate singular `/api/moment/*`

### 4. Hot Path Performance

**Good:** Click handler designed for <50ms target.

**Concerns:**
- Multiple database round-trips in some paths
- No caching layer for frequent queries
- Embedding similarity calculation inline

**Recommendation:** Add caching:
```python
@lru_cache(maxsize=1000)
def get_clickable_words(moment_id: str) -> List[str]:
    # Cache frequently accessed data
```

### 5. Error Handling Patterns

**Observed Patterns:**
- Some methods return `None` on error
- Some methods raise exceptions
- Some methods log and return empty collections

**Recommendation:** Standardize:
```python
# For queries: return Optional[T] or empty collection
def get_moment(id: str) -> Optional[Dict]: ...

# For operations: raise on failure
def handle_click(...) -> ClickResult:
    if not found:
        raise MomentNotFoundError(moment_id)
```

---

## Dependency Map

```
engine/api/moments.py
    ├── engine/moment_graph/queries.py (MomentQueries)
    ├── engine/moment_graph/traversal.py (MomentTraversal)
    ├── engine/moment_graph/surface.py (MomentSurface)
    └── engine/db/graph_queries.py (GraphQueries)

engine/moment_graph/queries.py
    └── engine/db/graph_queries.py (GraphQueries)

engine/moment_graph/traversal.py
    ├── engine/db/graph_ops.py (GraphOps)
    └── engine/moment_graph/queries.py (MomentQueries)

engine/moment_graph/surface.py
    ├── engine/db/graph_ops.py (GraphOps)
    └── engine/db/graph_queries.py (GraphQueries)
```

---

## Frontend Integration Points

| Component | Consumes | Produces |
|-----------|----------|----------|
| `useMoments` | API responses, SSE events | State for components |
| `ClickableText` | clickable_words | onClick callbacks |
| `MomentDisplay` | Moment data | Rendered UI |
| `MomentStream` | Moment arrays | Scrollable list |
| `MomentDebugPanel` | Full moment state | Debug visualization |

---

## Recommended Next Steps

### Immediate (Phase 2)
1. **Add integration tests** for moment graph operations
2. **Add SSE endpoint** for moment events in moments.py router
3. **Document API** in OpenAPI/Swagger

### Short-term
1. **Consolidate click handlers** - remove duplication between layers
2. **Add caching** for frequent queries (clickable_words, speaker resolution)
3. **Split large files** following domain boundaries

### Long-term
1. **Migrate from scene.json** entirely
2. **Narrator integration** - output moments directly
3. **Performance benchmarks** - ensure <50ms click path

---

## Bidirectional Link Support

**Status:** Implemented in `add_can_lead_to()` with `bidirectional: true` parameter.

**Usage:**
```yaml
links:
  - type: can_lead_to
    from: moment_a
    to: moment_b
    bidirectional: true  # Creates both A→B and B→A
```

**Query Handling:** `get_available_transitions()` returns both directions when querying from an active moment.

---

## Summary

The Moment Graph implementation is **functionally complete** for Phase 1:
- All node types and link types defined
- View queries with presence gating working
- Click traversal with weight transfer implemented
- Frontend components and hook ready

**Key refactoring opportunities:**
1. Reduce duplication between layers
2. Split large files
3. Standardize error handling
4. Add caching for hot paths

---

*"The architecture serves the experience. Keep the hot path fast."*

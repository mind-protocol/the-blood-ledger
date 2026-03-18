# Engine Moments — Sync: Current State

<!-- CHAIN: OBJECTIFS_Engine_Moments.md → PATTERNS_Engine_Moments.md → SYNC_Engine_Moments.md -->

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: agent
STATUS: DESIGNING
```

---

## Current State

Moment definitions and surfacing logic are implemented across physics and infrastructure layers. This module documents the patterns.

## Implementation Location

- `engine/physics/graph/graph_ops_moments.py` — Moment CRUD
- `engine/physics/graph/graph_queries_moments.py` — Moment queries
- `engine/infrastructure/world_builder/query_moment.py` — Moment surfacing

## Tests

- `engine/tests/test_moment_standalone.py`

## Recent Changes

- Moment query helpers added to world builder

## Known Issues

- Surfacing algorithm not fully documented
- Moment types need formal schema

## Next Steps

- Document surfacing algorithm
- Define moment type schema
- Add relevance scoring documentation

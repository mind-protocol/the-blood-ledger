# Engine Models — Sync: Current State

<!-- CHAIN: OBJECTIFS_Engine_Models.md → PATTERNS_Engine_Models.md → SYNC_Engine_Models.md -->

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: agent
STATUS: DESIGNING
```

---

## Current State

Model types are defined inline in physics layer files. This documentation module captures the conceptual patterns.

## Implementation Location

Types are primarily defined in:
- `engine/physics/graph/graph_ops_types.py`

## Recent Changes

- Type definitions consolidated in physics layer

## Known Issues

- Models not yet extracted into dedicated module
- Consider creating `engine/models/` directory

## Next Steps

- Extract type definitions to dedicated module
- Add schema validation utilities
- Document all node/link types

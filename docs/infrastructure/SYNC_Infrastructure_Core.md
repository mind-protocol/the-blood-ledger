# Infrastructure Core — Sync: Current State

<!-- CHAIN: OBJECTIFS_Infrastructure_Core.md → PATTERNS_Infrastructure_Core.md → SYNC_Infrastructure_Core.md -->

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: agent
STATUS: CANONICAL
```

---

## Current State

Infrastructure Core serves as the parent module for all infrastructure services. Individual services are documented in their respective subdirectories.

## Active Services

| Service | Path | Status |
|---------|------|--------|
| Canon | `engine/infrastructure/canon/` | Active |
| History | `engine/infrastructure/history/` | Active |
| Tempo | `engine/infrastructure/tempo/` | Active |
| World Builder | `engine/infrastructure/world_builder/` | Active |
| Orchestration | `engine/infrastructure/orchestration/` | Active |
| Embeddings | `engine/infrastructure/embeddings/` | Active |

## Recent Changes

- Added orchestration module for agent CLI
- Embeddings service extracted

## Known Issues

None at core level. See individual service docs for service-specific issues.

## Next Steps

See individual service SYNC files for detailed next steps.

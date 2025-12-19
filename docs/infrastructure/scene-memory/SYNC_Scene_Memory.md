# Scene Memory System — Sync

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: CANONICAL
```

===============================================================================
## DOCUMENT CHAIN
===============================================================================

| Document | Status | Purpose |
|----------|--------|---------|
| PATTERNS_Scene_Memory.md | Deprecated | Legacy design summary (Scene Memory → Moment Graph) |
| BEHAVIORS_Scene_Memory.md | Deprecated | Legacy behaviors summary |
| ALGORITHM_Scene_Memory.md | Deprecated | Legacy processing outline |
| VALIDATION_Scene_Memory.md | Deprecated | Legacy invariants summary |
| IMPLEMENTATION_Scene_Memory.md | Current | MomentProcessor architecture and data flow |
| TEST_Scene_Memory.md | Draft | Test coverage for moment processing |
| SYNC_Scene_Memory.md | Current | This file — state tracking |
| archive/SYNC_archive_2024-12.md | Archived | Legacy Scene Memory detail summary |

**Canonical references:**
- `docs/engine/moments/`
- `docs/engine/moment-graph-engine/`
- `docs/physics/`

===============================================================================
## ARCHITECTURE EVOLUTION
===============================================================================

**Original Design (2024-12):** Scene-based memory with Scene containers holding Moments

**Current Design (2025):** Moment Graph architecture
- Moments are first-class nodes with lifecycle states
- Weight-based surfacing replaces scene containers
- Click traversal targets <50ms response
- Transcript.json preserves full text history

===============================================================================
## IMPLEMENTATION STATUS
===============================================================================

| Component | Status | Location |
|-----------|--------|----------|
| Moment model | CANONICAL | `engine/models/nodes.py:189` |
| MomentProcessor | CANONICAL | `engine/infrastructure/memory/moment_processor.py` |
| Graph moment ops | CANONICAL | `engine/physics/graph/graph_ops.py:792` |
| Moment lifecycle | CANONICAL | `engine/physics/graph/graph_ops_moments.py` |
| Moment queries | CANONICAL | `engine/physics/graph/graph_queries_moments.py` |
| Moment Graph engine | CANONICAL | `engine/moment_graph/` |
| API endpoints | CANONICAL | `engine/infrastructure/api/moments.py` |
| Tests | CANONICAL | `engine/tests/test_moment*.py` (5 files) |

===============================================================================
## REPAIR LOG (2025-12-19)
===============================================================================

- Reduced legacy doc size by replacing long-form 2024-12 content with concise
  summaries and pointing to canonical Moment Graph docs.
- Added `docs/infrastructure/scene-memory/archive/SYNC_archive_2024-12.md` to
  preserve legacy summary context.
- Trimmed IMPLEMENTATION doc to focus on current code structure and entry points.
- Ran `ngram validate`; pre-existing failures remain in schema/embeddings/network
  and missing VIEW files.

===============================================================================
## OPEN QUESTIONS
===============================================================================

- [ ] Should the deprecated legacy docs be removed entirely after a future
      migration sign-off?

===============================================================================
## Agent Observations
===============================================================================

### Remarks
- The module was dominated by legacy Scene Memory docs that are superseded by
  Moment Graph documentation.

### Suggestions
- [ ] Consider moving remaining legacy Scene Memory docs into the archive folder
      entirely once no longer needed for historical reference.

### Propositions
- Centralize Scene Memory references in a single pointer doc to reduce drift.

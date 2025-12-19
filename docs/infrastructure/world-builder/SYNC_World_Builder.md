# World Builder — SYNC

```
STATUS: CANONICAL
UPDATED: 2025-12-19
IMPL: engine/infrastructure/world_builder/
```

---

## Current State

**World Builder is fully implemented.**

All core files are complete and ready for integration testing:

| File | Status | Notes |
|------|--------|-------|
| `query.py` | DONE | Universal query with async/sync variants |
| `query_moment.py` | DONE | Query → moment recording |
| `sparsity.py` | DONE | Semantic sparsity detection |
| `world_builder.py` | DONE | LLM enrichment service |
| `enrichment.py` | DONE | Prompt builder + graph mutations |
| `__init__.py` | DONE | Clean exports |

---

## Recent Changes

### 2025-12-19 — Repair revalidation (world_builder.py, current run)

- Rechecked `_hash_query` and `clear_cache` in `engine/infrastructure/world_builder/world_builder.py`; implementations already present, so no code changes were required for this repair run.

### 2025-12-19 — Repair revalidation (world_builder.py)

- Rechecked `_hash_query` and `clear_cache` in `engine/infrastructure/world_builder/world_builder.py`; both are already implemented, so no code changes were needed for this repair run.

### 2025-12-19 — Repair verification (world_builder.py)

- Verified `_hash_query` and `clear_cache` implementations in `engine/infrastructure/world_builder/world_builder.py`; repair task was stale and required no code changes.

### 2025-12-19 — Added agent CLI wrapper path for enrichment

- Added a shared agent CLI wrapper (`engine/infrastructure/orchestration/agent_cli.py`) and wired World Builder to use it exclusively (no SDK path).
- Updated implementation docs to reflect the CLI-only dependency.

### 2025-12-19 — Tests Implemented

- Created `tests/infrastructure/world_builder/test_world_builder.py`
- 49 unit tests passing covering all modules
- Test categories: sparsity, query moment, world builder, enrichment, query interface, edge cases, invariants

### 2025-12-19 — Documentation Complete

- Created VALIDATION_World_Builder.md with 8 invariants, 5 properties, 6 error conditions
- Created TEST_World_Builder.md with comprehensive test plan
- All docs in chain now exist

### 2025-12-19 — Initial Implementation

- Created complete module structure
- Implemented semantic sparsity detection with 4 metrics
- Implemented query moment recording (queries as thoughts)
- Implemented LLM enrichment with YAML parsing
- Implemented universal `query()` and `query_sync()` functions
- All created content marked with `generated: true`
- Enriched content links back to query moment via ABOUT

---

## Integration Points

### Consumes

| Service | How | For |
|---------|-----|-----|
| `SemanticSearch` | `engine.world.map.semantic` | Vector search |
| `GraphQueries` | `engine.physics.graph` | Graph operations |
| `Embeddings` | `engine.infrastructure.embeddings` | Sparsity check |
| `Claude/Codex CLI` | `engine/infrastructure/orchestration/agent_cli.py` | LLM enrichment (CLI only) |

### Provides

| Export | Purpose |
|--------|---------|
| `query()` | Async universal query with enrichment |
| `query_sync()` | Sync query without enrichment |
| `WorldBuilder` | Enrichment service class |
| `is_sparse()` | Sparsity detection |
| `SparsityResult` | Sparsity metrics dataclass |

---

## Usage Example

```python
from engine.infrastructure.world_builder import query, query_sync

# Async with enrichment (creates content if sparse)
results = await query(
    "What do I know about Edmund?",
    graph,
    char_id="char_aldric",
    place_id="place_camp"
)

# Sync without enrichment (just search + record)
results = query_sync(
    "memories of home",
    graph,
    char_id="char_player"
)
```

---

## Configuration

| Setting | File | Default | Description |
|---------|------|---------|-------------|
| `SPARSITY_PROXIMITY_THRESHOLD` | `sparsity.py` | 0.6 | Min similarity |
| `SPARSITY_MIN_CLUSTER` | `sparsity.py` | 2 | Min results |
| `SPARSITY_MIN_DIVERSITY` | `sparsity.py` | 0.3 | Min variety |
| `SPARSITY_MIN_CONNECTEDNESS` | `sparsity.py` | 1.5 | Min avg links |
| `QUERY_MOMENT_WEIGHT` | `query_moment.py` | 0.2 | Moment weight |
| `QUERY_MOMENT_ENERGY` | `query_moment.py` | 0.3 | Energy source |
| `ENRICHMENT_CACHE_SECONDS` | `world_builder.py` | 60 | Cache window |
| `LLM_MODEL` | `world_builder.py` | claude-sonnet-4-20250514 | Model |
| `MAX_TOKENS` | `world_builder.py` | 2048 | Response limit |

---

## Next Steps

### For Integration

1. **Test with real graph** — Run against FalkorDB with seeded data
2. **Verify energy flow** — Confirm physics distributes energy from query moments
3. **Monitor LLM calls** — Watch for cache hits, recursion prevention

### For Production

1. **Add rate limiting** — Per-playthrough LLM call limits
2. **Content review** — UI to mark generated content for human review
3. **Quality metrics** — Track enrichment acceptance rate

---

## Known Issues

None yet — module is newly implemented.

---

## Handoff Notes

**For next agent:**

World Builder is complete but untested with real infrastructure. To verify:

1. Start FalkorDB with seeded graph
2. Run a query through `query()` function
3. Verify:
   - Query moment created in graph
   - ABOUT links to results
   - Sparsity correctly detected
   - Enrichment creates nodes with `generated: true`
   - All enriched content links back to query moment

The semantic search integration depends on `engine.world.map.semantic.SemanticSearch` which should already be working.

---

## Chain

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM_World_Builder.md
VALIDATION:      ./VALIDATION_World_Builder.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Builder.md
TEST:            ./TEST_World_Builder.md
THIS:            SYNC_World_Builder.md
```

## Agent Observations

### Remarks
- Repair task flagged empty helpers, but `_hash_query` and `clear_cache` already have concrete implementations.

### Suggestions
- [ ] Restore missing `PATTERNS_World_Builder.md` and `BEHAVIORS_World_Builder.md` to resolve CHAIN gaps noted in validation.

### Propositions
- Run `ngram validate` after doc chain restoration to confirm world-builder CHAIN links are resolved.

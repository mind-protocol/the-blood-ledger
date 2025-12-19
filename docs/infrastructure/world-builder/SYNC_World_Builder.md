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

## Documentation Updates

- Split large docs into focused folders: `ALGORITHM/`, `IMPLEMENTATION/`, `VALIDATION/`, `TEST/`.
- Added concise overviews plus detail files and updated all CHAIN references.
- Archived trimmed details in `archive/SYNC_archive_2024-12.md`.

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

- Test run failed locally: missing `pytest_xprocess` plugin (pytest bootstrap error).
- `ngram validate` reports missing VIEW and doc chain gaps in other modules (not world-builder specific).

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

Doc chain entry points now live under `docs/infrastructure/world-builder/ALGORITHM/`, `IMPLEMENTATION/`, `VALIDATION/`, and `TEST/`.

---

## Chain

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:      ./VALIDATION/VALIDATION_Overview.md
IMPLEMENTATION:  ./IMPLEMENTATION/IMPLEMENTATION_Overview.md
TEST:            ./TEST/TEST_Overview.md
THIS:            SYNC_World_Builder.md
```

## Agent Observations

### Remarks
- Repair task flagged empty helpers, but `_hash_query` and `clear_cache` already have concrete implementations.
- Reconfirmed cache helper implementations during the latest repair verification; no code changes were required.
- Reduced doc size by splitting and trimming verbose sections into summary docs.

### Suggestions
- [x] Doc chain already includes PATTERNS/BEHAVIORS; no restoration needed for this repair.
- [ ] Consider regenerating `docs/map.md` if tooling relies on it for navigation.

### Propositions
- Run `ngram validate` after doc chain restoration to confirm world-builder CHAIN links are resolved.
- Add a lightweight doc size check to prevent future drift over 50K.


---

## ARCHIVE

Older content archived to: `SYNC_World_Builder_archive_2025-12.md`

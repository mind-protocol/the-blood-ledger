# World Builder — Implementation Overview

```
STATUS: CANONICAL
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_World_Builder.md
BEHAVIORS:       ../BEHAVIORS_World_Builder.md
ALGORITHM:       ../ALGORITHM_World_Builder.md
VALIDATION:      ../VALIDATION_World_Builder.md
THIS:            IMPLEMENTATION_Overview.md (you are here)
DETAILS:         ./IMPLEMENTATION_Flow.md
TEST:            ../TEST_World_Builder.md
SYNC:            ../SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/
```

---

## Code Structure

```
engine/infrastructure/world_builder/__init__.py     # Exports query(), WorldBuilder
engine/infrastructure/world_builder/query.py        # Universal query + query_sync
engine/infrastructure/world_builder/query_moment.py # Record query moments and ABOUT links
engine/infrastructure/world_builder/sparsity.py     # Semantic sparsity detection
engine/infrastructure/world_builder/world_builder.py # Enrichment service and caching
engine/infrastructure/world_builder/enrichment.py   # Prompt building + apply enrichment
```

### File Responsibilities (Concise)

| File | Purpose | Key Functions | Status |
|------|---------|---------------|--------|
| `engine/infrastructure/world_builder/__init__.py` | Package exports | `query`, `WorldBuilder` | IMPL |
| `engine/infrastructure/world_builder/query.py` | Query flow | `query`, `query_sync` | IMPL |
| `engine/infrastructure/world_builder/query_moment.py` | Record moments | `record_query_moment`, `link_results_to_moment` | IMPL |
| `engine/infrastructure/world_builder/sparsity.py` | Sparse detection | `is_sparse`, `SparsityResult` | IMPL |
| `engine/infrastructure/world_builder/world_builder.py` | LLM enrichment | enrich (WorldBuilder) | IMPL |
| `engine/infrastructure/world_builder/enrichment.py` | Graph mutations | `build_enrichment_prompt`, `apply_enrichment` | IMPL |

---

## Dependencies

### Internal

- Graph runtime (ngram repo) for graph queries and writes (see `data/ARCHITECTURE — Cybernetic Studio.md`)
- `engine/world/map/semantic.py` for semantic search
- engine/infrastructure/orchestration/agent_cli.py for LLM calls (missing in repo; see GAPS)

### External

- `numpy` for cosine similarity
- `pyyaml` for parsing LLM output

---

## Configuration (Key Settings)

| Setting | Default | Source |
|---------|---------|--------|
| `SPARSITY_PROXIMITY_THRESHOLD` | 0.6 | `engine/infrastructure/world_builder/sparsity.py` |
| `SPARSITY_MIN_CLUSTER` | 2 | `engine/infrastructure/world_builder/sparsity.py` |
| `SPARSITY_MIN_DIVERSITY` | 0.3 | `engine/infrastructure/world_builder/sparsity.py` |
| `SPARSITY_MIN_CONNECTEDNESS` | 1.5 | `engine/infrastructure/world_builder/sparsity.py` |
| `QUERY_MOMENT_WEIGHT` | 0.2 | `engine/infrastructure/world_builder/query_moment.py` |
| `QUERY_MOMENT_ENERGY` | 0.3 | `engine/infrastructure/world_builder/query_moment.py` |
| `ENRICHMENT_CACHE_SECONDS` | 60 | `engine/infrastructure/world_builder/world_builder.py` |
| `LLM_MODEL` | claude-sonnet-4-20250514 | `engine/infrastructure/world_builder/world_builder.py` |

---

## Archive Note

Full code listings and large diagrams were trimmed; see `docs/infrastructure/world-builder/archive/SYNC_archive_2024-12.md`.

---

## GAPS / IDEAS / QUESTIONS

- @ngram:escalation Missing `engine/infrastructure/orchestration/agent_cli.py` referenced by `engine/infrastructure/world_builder/world_builder.py`; decide whether to restore the module or update World Builder to the current orchestration path.

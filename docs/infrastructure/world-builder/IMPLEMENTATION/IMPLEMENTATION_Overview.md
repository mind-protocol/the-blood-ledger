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
ALGORITHM:       ../ALGORITHM/ALGORITHM_Overview.md
VALIDATION:      ../VALIDATION/VALIDATION_Overview.md
THIS:            IMPLEMENTATION_Overview.md (you are here)
DETAILS:         ./IMPLEMENTATION_Flow.md
TEST:            ../TEST/TEST_Overview.md
SYNC:            ../SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/
```

---

## Code Structure

```
engine/infrastructure/world_builder/
├── __init__.py            # Exports query(), WorldBuilder
├── query.py               # Universal query + query_sync
├── query_moment.py        # Record query moments and ABOUT links
├── sparsity.py            # Semantic sparsity detection
├── world_builder.py       # Enrichment service and caching
└── enrichment.py          # Prompt building + apply enrichment
```

### File Responsibilities (Concise)

| File | Purpose | Key Functions | Status |
|------|---------|---------------|--------|
| `__init__.py` | Package exports | `query`, `WorldBuilder` | IMPL |
| `query.py` | Query flow | `query`, `query_sync` | IMPL |
| `query_moment.py` | Record moments | `record_query_moment`, `link_results_to_moment` | IMPL |
| `sparsity.py` | Sparse detection | `is_sparse`, `SparsityResult` | IMPL |
| `world_builder.py` | LLM enrichment | `WorldBuilder.enrich` | IMPL |
| `enrichment.py` | Graph mutations | `build_enrichment_prompt`, `apply_enrichment` | IMPL |

---

## Dependencies

### Internal

- `engine/physics/graph/**` for graph queries and writes
- `engine/world/map/semantic.py` for semantic search
- `engine/infrastructure/orchestration/agent_cli.py` for LLM calls

### External

- `numpy` for cosine similarity
- `pyyaml` for parsing LLM output

---

## Configuration (Key Settings)

| Setting | Default | Source |
|---------|---------|--------|
| `SPARSITY_PROXIMITY_THRESHOLD` | 0.6 | `sparsity.py` |
| `SPARSITY_MIN_CLUSTER` | 2 | `sparsity.py` |
| `SPARSITY_MIN_DIVERSITY` | 0.3 | `sparsity.py` |
| `SPARSITY_MIN_CONNECTEDNESS` | 1.5 | `sparsity.py` |
| `QUERY_MOMENT_WEIGHT` | 0.2 | `query_moment.py` |
| `QUERY_MOMENT_ENERGY` | 0.3 | `query_moment.py` |
| `ENRICHMENT_CACHE_SECONDS` | 60 | `world_builder.py` |
| `LLM_MODEL` | claude-sonnet-4-20250514 | `world_builder.py` |

---

## Archive Note

Full code listings and large diagrams were trimmed; see `../archive/SYNC_archive_2024-12.md`.

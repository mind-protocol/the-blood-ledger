# World Builder — Implementation Flow

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
THIS:            IMPLEMENTATION_Flow.md (you are here)
OVERVIEW:        ./IMPLEMENTATION_Overview.md
TEST:            ../TEST_World_Builder.md
SYNC:            ../SYNC_World_Builder.md
```

---

## Query Flow (Module Boundaries)

1. `query()` in `engine/infrastructure/world_builder/query.py` receives the request.
2. `record_query_moment()` in `engine/infrastructure/world_builder/query_moment.py` creates the thought moment and context links.
3. Semantic search executes through `engine/world/map/semantic.py` (`SemanticSearch.find()`).
4. `link_results_to_moment()` in `engine/infrastructure/world_builder/query_moment.py` records ABOUT links with similarity weights.
5. `is_sparse()` in `engine/infrastructure/world_builder/sparsity.py` decides whether to enrich.
6. `WorldBuilder.enrich()` in `engine/infrastructure/world_builder/world_builder.py` runs LLM enrichment and caching guards.
7. `apply_enrichment()` in `engine/infrastructure/world_builder/enrichment.py` writes nodes/links/moments back to the graph.
8. `query()` in `engine/infrastructure/world_builder/query.py` re-runs search and returns results.

---

## Enrichment Application Notes

- All created nodes are marked `generated: true`.
- All created nodes and moments receive ABOUT links from the query moment.
- Enriched moments are linked to speaker/place context when provided.

---

## Error Handling Summary

- Search failures return an empty list but still create the query moment.
- LLM failures return `None` and skip enrichment (original results returned).

---

## Archive Note

Detailed code examples and extended prompts were trimmed; see `docs/infrastructure/world-builder/archive/SYNC_archive_2024-12.md`.

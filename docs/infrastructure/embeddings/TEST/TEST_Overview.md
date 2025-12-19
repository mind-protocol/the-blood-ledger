# Embeddings — Test Overview

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Embeddings.md
BEHAVIORS:      ../BEHAVIORS_Embeddings.md
ALGORITHM:      ../ALGORITHM/ALGORITHM_Overview.md
VALIDATION:     ../VALIDATION_Embeddings.md
THIS:           TEST/TEST_Overview.md
CASES:          ./TEST_Cases.md
IMPLEMENTATION: ../IMPLEMENTATION_Embeddings.md
SYNC:           ../SYNC_Embeddings.md
IMPL:           ../../../../engine/infrastructure/embeddings/service.py
```

---

## TEST STRATEGY

1. **Unit tests** for embedding and indexing helpers
2. **Invariant tests** for vector dimensions, determinism, and length thresholds
3. **Integration tests** for index → search cycles

Priority is unit coverage for core behaviors, then integration for vector index queries.

---

## CORE UNIT TESTS (Planned)

- `test_embed_basic` → 768-dim vector
- `test_embed_empty` → defined behavior for empty text
- `test_index_node_detail` → detail > 20 embeds and assigns
- `test_index_node_name_fallback` → name used when detail short
- `test_index_link_detail` → detail > 20 embeds
- `test_search_limit_respected` → returns <= limit

---

## INTEGRATION TESTS (Planned)

- Full index-search cycle for narrative nodes
- Link detail embedding searchable by similarity
- Batch world indexing completes within expected time

---

## HOW TO RUN

```bash
pytest engine/tests/test_embeddings.py -v
```

---

## ARCHIVED DETAILS

Detailed fixtures, performance tests, and extended coverage lists are archived in
`archive/SYNC_archive_2024-12.md`.

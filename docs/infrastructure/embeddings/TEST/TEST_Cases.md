# Embeddings — Test Cases

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
OVERVIEW:       ./TEST_Overview.md
THIS:           TEST/TEST_Cases.md
IMPLEMENTATION: ../IMPLEMENTATION_Embeddings.md
SYNC:           ../SYNC_Embeddings.md
IMPL:           ../../../../engine/infrastructure/embeddings/service.py
```

---

## UNIT TESTS

### Embedding Generation

| Test | Expected | Status |
|------|----------|--------|
| `test_embed_basic` | 768-dim vector | pending |
| `test_embed_empty` | Zero vector | pending |
| `test_embed_unicode` | Valid vector | pending |
| `test_embed_long_text` | Truncated, valid vector | pending |
| `test_embed_deterministic` | Identical vectors | pending |

### Node Indexing

| Test | Expected | Status |
|------|----------|--------|
| `test_index_node_detail` | node.embedding set | pending |
| `test_index_node_name_fallback` | embedding from name | pending |
| `test_index_node_no_qualifying` | returns None | pending |
| `test_index_node_detail_priority` | detail preferred | pending |
| `test_index_node_upsert` | embedding overwritten | pending |

### Link Indexing

| Test | Expected | Status |
|------|----------|--------|
| `test_index_link_detail` | link.embedding set | pending |
| `test_index_link_no_detail` | returns None | pending |
| `test_index_link_no_name_fallback` | no embedding | pending |

### Search

| Test | Expected | Status |
|------|----------|--------|
| `test_search_empty_index` | empty list | pending |
| `test_search_exact_match` | score > 0.9 | pending |
| `test_search_semantic_match` | score > 0.5 | pending |
| `test_search_limit_respected` | <= limit | pending |
| `test_search_score_ordering` | descending scores | pending |

---

## INTEGRATION TESTS

| Scenario | Expected | Status |
|----------|----------|--------|
| Full cycle: node index + search | result includes node | pending |
| Full cycle: link index + search | result includes link | pending |
| World indexing | embeddings created for eligible content | pending |

---

## EDGE CASES

| Case | Expected | Status |
|------|----------|--------|
| Very long detail | truncation handled | pending |
| Special characters | no encoding errors | pending |
| Duplicate index calls | upsert, no duplicates | pending |
| Deleted source after index | get_full_context returns None | pending |
| Concurrent index calls | thread-safe | pending |
| Model not loaded | lazy load works | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| EmbeddingService.embed() | Existing | engine/infrastructure/embeddings/service.py |
| EmbeddingService.embed_batch() | Existing | engine/infrastructure/embeddings/service.py |
| index_node() | 0% | detail > 20 (fallback name), set attribute |
| index_link() | 0% | detail > 20, set attribute |
| search() | Partial | needs vector index queries |

---

## KNOWN TEST GAPS

- [ ] Property-based tests for embedding consistency
- [ ] Stress test with thousands of embeddings
- [ ] Concurrent indexing tests
- [ ] Model version compatibility tests
- [ ] Index corruption recovery tests

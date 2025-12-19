# Map System — Test: Semantic Search Coverage

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
THIS:            TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            tests/world/test_map_semantic.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

Focus on semantic search correctness and fallback behavior. Use integration tests with FalkorDB when available, and unit tests with stubbed GraphQueries for deterministic results.

---

## UNIT TESTS

### Semantic Search Behavior

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_find_filters_min_similarity` | query + min_similarity | results all >= threshold | pending |
| `test_find_respects_limit` | query + limit | results <= limit | pending |
| `test_find_similar_excludes_self` | node_id | no result with node_id | pending |
| `test_vector_search_fallback` | exception in vector query | fallback results | pending |

---

## INTEGRATION TESTS

### FalkorDB Vector Index

```
GIVEN:  FalkorDB running with vector index
WHEN:   SemanticSearch.find is called
THEN:   Results returned in similarity order
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Empty query string | `test_find_empty_query` | pending |
| Node without embedding | `test_find_similar_missing_embedding` | pending |
| Graph connection failure | `test_graph_query_failure_returns_empty` | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `SemanticSearch.find` | 0% | No tests yet |
| `SemanticSearch.find_similar` | 0% | No tests yet |
| `_vector_search` fallback | 0% | No tests yet |

---

## HOW TO RUN

```bash
# No tests exist yet.
# Suggested:
pytest tests/world/test_map_semantic.py
```

---

## KNOWN TEST GAPS

- [ ] No automated tests for semantic search.
- [ ] No integration tests for vector index behavior.

---

## FLAKY TESTS

None tracked.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add fixtures for GraphQueries + embedding service.
- IDEA: Use a lightweight in-memory graph for unit tests.
- QUESTION: Should semantic search tests mock embeddings or use real vectors?

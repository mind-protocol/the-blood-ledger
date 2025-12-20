# Map System — Validation: Semantic Search Invariants

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against workspace
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
THIS:            VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
SYNC:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

These must ALWAYS be true:

### V1: Queries Always Embed Before Search

```
SemanticSearch.find() must generate a query embedding and use it to search.
```

**Checked by:** Manual inspection of `SemanticSearch.find`.

### V2: Similarity Threshold Filters Results

```
find() returns only results with similarity >= min_similarity.
```

**Checked by:** Manual inspection of the filtering list comprehension.

### V3: find_similar Excludes the Source Node

```
find_similar() must not return the source node_id in its results.
```

**Checked by:** Manual inspection of the post-filter and limit.

---

## PROPERTIES

For property-based testing:

### P1: Result Limits Are Respected

```
FORALL query, limit:
    len(find(query, limit=limit)) <= limit
```

**Tested by:** NOT YET TESTED — no tests in repo.

### P2: Fallback Similarity Ordering

```
FORALL embeddings:
    _fallback_search results are sorted by similarity desc
```

**Tested by:** NOT YET TESTED — no tests in repo.

---

## ERROR CONDITIONS

### E1: Vector Index Missing

```
WHEN:    FalkorDB vector index is missing or query fails
THEN:    _vector_search falls back to _fallback_search
SYMPTOM: Warning log emitted, results still returned
```

**Tested by:** NOT YET TESTED — no automated coverage.

### E2: Graph Query Failure

```
WHEN:    GraphQueries (ngram repo graph runtime) fails in _fallback_search or _get_node_with_embedding
THEN:    Return [] or None without raising
SYMPTOM: Empty results, no crash
```

**Tested by:** NOT YET TESTED — no automated coverage.

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Queries embed before search | — | ⚠ NOT YET TESTED |
| V2: Similarity threshold filters results | — | ⚠ NOT YET TESTED |
| V3: find_similar excludes source node | — | ⚠ NOT YET TESTED |
| P1: Result limits | — | ⚠ NOT YET TESTED |
| E1: Vector index fallback | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — read SemanticSearch.find implementation
[ ] V2 holds — confirm min_similarity filter in find()
[ ] V3 holds — confirm find_similar excludes node_id
[ ] Fallback search returns results when vector search fails
[ ] No unhandled exceptions from graph query failures
```

### Automated

```bash
# No automated tests yet for world map semantic search.
# Suggested location: tests/world/test_map_semantic.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: engine/world/map/semantic.py (workspace)
    test: tests/world/test_map_semantic.py (missing)
VERIFIED_BY: Codex (repair agent)
RESULT:
    V1: PASS (manual)
    V2: PASS (manual)
    V3: PASS (manual)
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add automated tests for semantic search filtering and fallback paths.
- [ ] Add integration test with FalkorDB vector index enabled.
- QUESTION: Should similarity thresholds be configurable per node type?

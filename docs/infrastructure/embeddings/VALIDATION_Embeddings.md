# Embeddings — Validation: Invariants and Verification

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Embeddings.md
BEHAVIORS:   ./BEHAVIORS_Embeddings.md
ALGORITHM:   ./ALGORITHM_Embeddings.md
THIS:        VALIDATION_Embeddings.md (you are here)
TEST:        ./TEST_Embeddings.md
SYNC:        ./SYNC_Embeddings.md
IMPL:        ../../engine/embeddings/service.py
```

---

## INVARIANTS

These must ALWAYS be true:

### V1: One Embedding Per Node

```
Each node has at most one embedding.
Stored as node.embedding attribute.
```

**Checked by:** `test_one_embedding_per_node` — verify no duplicate embeddings

### V2: Source Reference Validity

```
Every embedding's source reference points to existing content:
- Nodes: source_id exists in graph
- Links: link_from and link_to exist in graph
- Conversations: source_file and source_section exist
```

**Checked by:** `test_source_reference_validity` — validate each embedding's references

### V3: Vector Dimension Consistency

```
All embedding vectors have the same dimension.
Dimension matches the model's output (768 for all-mpnet-base-v2).
```

**Checked by:** `test_vector_dimensions` — verify all vectors have correct length

### V4: Text-Vector Correspondence

```
Embedding the same text always produces the same vector.
(Deterministic embedding model)
```

**Checked by:** `test_embedding_determinism` — embed same text twice, compare vectors

### V5: Minimum Length Threshold

```
No embedding exists where both detail <= 20 AND name <= 20.
detail > 20 OR name > 20 required for embedding.
```

**Checked by:** `test_minimum_length_threshold` — verify no short-text embeddings exist

---

## PROPERTIES

For property-based testing:

### P1: Search Returns Source Info

```
FORALL query:
    results = search(query, limit=N)
    FORALL result IN results:
        result.source_type IS NOT NULL
        result.source_id IS NOT NULL OR result.source_file IS NOT NULL
```

**Tested by:** `test_search_returns_source_info` | NOT YET TESTED

### P2: Index-Then-Search Finds Content

```
FORALL text WHERE len(text) > 20:
    index_node({"id": "test", "type": "narrative", "detail": text})
    results = search(text, limit=1)
    results[0].id == "test"
```

**Tested by:** `test_index_then_search` | NOT YET TESTED

### P3: Score Ordering

```
FORALL results = search(query):
    FOR i IN range(len(results) - 1):
        results[i].score >= results[i+1].score
```

**Tested by:** `test_score_ordering` | NOT YET TESTED

### P4: Limit Respected

```
FORALL query, limit:
    results = search(query, limit)
    len(results) <= limit
```

**Tested by:** `test_limit_respected` | NOT YET TESTED

---

## ERROR CONDITIONS

### E1: No Qualifying String Fields

```
WHEN:    Node passed to index_node() with no string fields > 20 chars
THEN:    Returns empty list (no embeddings created)
SYMPTOM: Function returns [], no error raised
```

**Tested by:** `test_no_qualifying_fields` | NOT YET TESTED

### E2: Invalid Source ID in Search Result

```
WHEN:    Source node/link was deleted after embedding created
THEN:    get_full_context() returns None
SYMPTOM: Search result exists but source retrieval fails gracefully
```

**Tested by:** `test_deleted_source` | NOT YET TESTED

### E3: Vector Index Not Created

```
WHEN:    search() called before vector index exists
THEN:    Raises informative error
SYMPTOM: Error message indicates index needs creation
```

**Tested by:** `test_missing_vector_index` | NOT YET TESTED

### E4: Model Load Failure

```
WHEN:    sentence-transformers not installed
THEN:    Raises ImportError with installation instructions
SYMPTOM: Clear error message about missing dependency
```

**Tested by:** `test_model_load_failure` | NOT YET TESTED

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: One per node | `test_one_embedding_per_node` | NOT YET TESTED |
| V2: Source validity | `test_source_reference_validity` | NOT YET TESTED |
| V3: Vector dimensions | `test_vector_dimensions` | NOT YET TESTED |
| V4: Determinism | `test_embedding_determinism` | NOT YET TESTED |
| V5: Min length | `test_minimum_length_threshold` | NOT YET TESTED |
| P1: Source info | `test_search_returns_node` | NOT YET TESTED |
| P2: Index-search | `test_index_then_search` | NOT YET TESTED |
| P3: Score order | `test_score_ordering` | NOT YET TESTED |
| P4: Limit | `test_limit_respected` | NOT YET TESTED |
| E1: No qualifying text | `test_no_qualifying_text` | NOT YET TESTED |
| E2: Deleted source | `test_deleted_source` | NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Index node with detail > 20 — node.embedding set from detail
[ ] Index node with detail < 20, name > 20 — node.embedding set from name
[ ] Index node with both < 20 — no embedding, returns None
[ ] Index link with detail > 20 — link.embedding set
[ ] Search for indexed content — returns matching node
[ ] Search for non-existent content — returns empty list
[ ] Check vector dimensions match model (768)
[ ] Verify deterministic embedding (same text = same vector)
```

### Automated

```bash
# Run embedding tests
pytest engine/tests/test_embeddings.py -v

# Run with coverage
pytest engine/tests/test_embeddings.py --cov=engine/embeddings

# Check index integrity
python scripts/verify_embedding_index.py
```

---

## INTEGRATION TESTS

### I1: Full Index-Search Cycle

```
GIVEN:  Empty embedding index
WHEN:   Create node with detail "Aldric watched his brother die"
AND:    index_node(node)
AND:    search("brother death")
THEN:   Results include the indexed node
AND:    Score > 0.5 (semantically related)
STATUS: NOT YET TESTED
```

### I2: Link Embedding Retrieval

```
GIVEN:  BELIEVES link with detail "Told by the fire, voice breaking"
WHEN:   index_link(link)
AND:    search("emotional conversation")
THEN:   Results include link
AND:    Result has correct link_from, link_to, link_type
STATUS: NOT YET TESTED
```

### I3: Batch World Indexing

```
GIVEN:  World with 100 nodes, 50 links
WHEN:   index_world()
THEN:   ~100 node.embedding attributes set (varies by detail/name presence)
AND:    All searchable via vector index
AND:    Completes in < 60 seconds
STATUS: NOT YET TESTED
```

---

## PERFORMANCE BENCHMARKS

| Operation | Expected | Actual |
|-----------|----------|--------|
| Single embed() | < 100ms | TBD |
| index_node() | < 150ms | TBD |
| search(limit=10) | < 500ms | TBD |
| index_world() (1000 items) | < 60s | TBD |

---

## SYNC STATUS

```
LAST_VERIFIED: Not yet verified
VERIFIED_AGAINST: N/A (spec not fully implemented)
VERIFIED_BY: N/A
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
    V4: NOT RUN
    V5: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Property-based testing with Hypothesis
- [ ] Performance regression tests
- [ ] Index corruption detection
- IDEA: Automated nightly index verification
- IDEA: Embedding drift detection (model version changes)
- QUESTION: How to test vector similarity quality?

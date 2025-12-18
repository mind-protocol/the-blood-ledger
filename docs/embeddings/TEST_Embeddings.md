# Embeddings — Test: Test Cases and Coverage

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
VALIDATION:  ./VALIDATION_Embeddings.md
THIS:        TEST_Embeddings.md (you are here)
SYNC:        ./SYNC_Embeddings.md
IMPL:        ../../engine/embeddings/service.py
```

---

## TEST STRATEGY

The embedding system is foundational for semantic search. Testing strategy:

1. **Unit tests** — Individual functions (embed, index_node, index_link)
2. **Invariant tests** — ID uniqueness, vector dimensions, source validity
3. **Integration tests** — Full index-search cycles with real model
4. **Performance tests** — Latency and throughput benchmarks

Priority: Unit tests first (core logic), then integration (real model), then performance.

---

## UNIT TESTS

### Embedding Generation

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_embed_basic` | "Hello world" | 768-dim vector | pending |
| `test_embed_empty` | "" | Zero vector | pending |
| `test_embed_unicode` | "日本語テスト" | Valid vector | pending |
| `test_embed_long_text` | 10000 char string | Truncated, valid vector | pending |
| `test_embed_deterministic` | Same text twice | Identical vectors | pending |

### Node Indexing

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_index_node_detail` | Node with detail > 20 chars | node.embedding set | pending |
| `test_index_node_name_fallback` | Node with detail < 20, name > 20 | node.embedding from name | pending |
| `test_index_node_no_qualifying` | Node with both < 20 chars | Returns None, no embedding | pending |
| `test_index_node_detail_priority` | Node with both > 20 | Uses detail, not name | pending |
| `test_index_node_upsert` | Same node twice | Embedding overwritten | pending |

### Link Indexing

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_index_link_detail` | BELIEVES link with detail > 20 | link.embedding set | pending |
| `test_index_link_no_detail` | Link with detail < 20 | Returns None | pending |
| `test_index_link_no_name_fallback` | Link with no detail, long type | No embedding (no fallback) | pending |

### Search

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_search_empty_index` | Any query | Empty list | pending |
| `test_search_exact_match` | Indexed text | Score > 0.9 | pending |
| `test_search_semantic_match` | Related concept | Score > 0.5 | pending |
| `test_search_limit_respected` | limit=5 | <= 5 results | pending |
| `test_search_score_ordering` | Any query | Descending scores | pending |

---

## INTEGRATION TESTS

### Full Cycle: Node

```
GIVEN:  Clean embedding index
WHEN:   Create narrative with detail "The rebellion began at dawn"
AND:    index_node(narrative)
AND:    search("uprising morning")
THEN:   Results contain the narrative
AND:    source_type == "narrative"
AND:    source_id == narrative.id
AND:    source_field == "detail"
STATUS: pending
```

### Full Cycle: Link

```
GIVEN:  Clean embedding index
AND:    BELIEVES link with detail "Aldric told me, voice shaking"
WHEN:   index_link(link)
AND:    search("emotional conversation")
THEN:   Results contain the link
AND:    source_type == "link"
AND:    link_from, link_to, link_type populated
STATUS: pending
```

### World Indexing

```
GIVEN:  World with 50 narratives, 30 characters, 20 places, 100 links
AND:    ~60% have detail > 20 (or name > 20 for nodes)
WHEN:   index_world()
THEN:   ~120 node.embedding attributes set
AND:    All searchable by vector similarity
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Very long detail (10K chars) | Truncation handled | pending |
| Special characters in text | No encoding errors | pending |
| Duplicate index calls | Upsert, no duplicates | pending |
| Deleted source after index | get_full_context returns None | pending |
| Concurrent index calls | Thread-safe | pending |
| Model not loaded yet | Lazy load works | pending |

---

## TEST FIXTURES

### Mock Embedding Service

```python
class MockEmbeddingService:
    """Fast mock for unit tests without loading real model."""

    def embed(self, text: str) -> List[float]:
        # Deterministic fake embedding based on text hash
        import hashlib
        h = hashlib.md5(text.encode()).hexdigest()
        return [int(h[i:i+2], 16) / 255.0 for i in range(0, 32, 2)] * 48  # 768 dims

    def similarity(self, v1, v2) -> float:
        return sum(a * b for a, b in zip(v1, v2)) / len(v1)
```

### Sample Nodes

```python
@pytest.fixture
def sample_narrative_with_detail():
    # detail > 20: uses detail for embedding
    return {
        "id": "narr_test",
        "type": "narrative",
        "name": "The Oath",  # 8 chars
        "detail": "The rebellion began at dawn. Robert Cumin died in flames."  # 56 chars
    }
    # Expected: embedding from detail

@pytest.fixture
def sample_narrative_name_fallback():
    # detail < 20, name > 20: falls back to name
    return {
        "id": "narr_test2",
        "type": "narrative",
        "name": "The Oath of Blood Sworn at Durham",  # 33 chars
        "detail": "Short."  # 6 chars
    }
    # Expected: embedding from name

@pytest.fixture
def sample_character_no_embed():
    # Both < 20: no embedding
    return {
        "id": "char_test",
        "type": "character",
        "name": "Aldric",  # 6 chars
        "detail": "A soldier."  # 10 chars
    }
    # Expected: None

@pytest.fixture
def sample_link():
    # detail > 20: uses detail
    return {
        "id": "link_test",
        "type": "BELIEVES",
        "from_id": "char_player",
        "to_id": "narr_test",
        "detail": "Aldric told me by the fire, voice breaking as he spoke."  # 55 chars
    }
    # Expected: embedding from detail
```

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| EmbeddingService.embed() | Existing | In engine/embeddings/service.py |
| EmbeddingService.embed_batch() | Existing | In engine/embeddings/service.py |
| index_node() | 0% | detail > 20 (fallback name), set attribute |
| index_link() | 0% | detail > 20, set attribute |
| search() | Partial | Needs vector index queries |

---

## HOW TO RUN

```bash
# Run all embedding tests
pytest engine/tests/test_embeddings.py -v

# Run with real model (slow)
pytest engine/tests/test_embeddings.py -v -m "not mock"

# Run only unit tests (fast, mocked)
pytest engine/tests/test_embeddings.py -v -m "mock"

# Run with coverage
pytest engine/tests/test_embeddings.py --cov=engine/embeddings --cov-report=html

# Run specific test
pytest engine/tests/test_embeddings.py::test_index_node_with_detail -v
```

---

## KNOWN TEST GAPS

- [ ] Property-based tests for embedding consistency
- [ ] Stress test with thousands of embeddings
- [ ] Concurrent indexing tests
- [ ] Model version compatibility tests
- [ ] Index corruption recovery tests

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| None yet | - | - | - |

---

## PERFORMANCE TESTS

### Embedding Latency

```python
def test_embed_latency():
    """Single embedding should complete in < 100ms."""
    service = EmbeddingService()
    text = "Test text for embedding latency measurement."

    start = time.time()
    service.embed(text)
    elapsed = time.time() - start

    assert elapsed < 0.1, f"Embedding took {elapsed:.3f}s, expected < 0.1s"
```

### Batch Embedding Throughput

```python
def test_batch_throughput():
    """Should embed 100 texts in < 5 seconds."""
    service = EmbeddingService()
    texts = ["Sample text number " + str(i) for i in range(100)]

    start = time.time()
    service.embed_batch(texts)
    elapsed = time.time() - start

    assert elapsed < 5.0, f"Batch took {elapsed:.3f}s, expected < 5s"
```

### Search Latency

```python
def test_search_latency():
    """Search should complete in < 500ms."""
    # ... index some content first ...

    start = time.time()
    results = search("test query", limit=10)
    elapsed = time.time() - start

    assert elapsed < 0.5, f"Search took {elapsed:.3f}s, expected < 0.5s"
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] How to test embedding quality (semantic correctness)?
- [ ] Should we compare against a "golden" set of expected matches?
- [ ] Integration tests with actual FalkorDB vector index
- IDEA: Use sentence similarity benchmarks (STS-B) for quality testing
- IDEA: Record search results for regression testing
- QUESTION: What's acceptable false positive/negative rate?

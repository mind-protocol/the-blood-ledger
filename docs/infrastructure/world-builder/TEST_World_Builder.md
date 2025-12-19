# World Builder — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM_World_Builder.md
VALIDATION:      ./VALIDATION_World_Builder.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Builder.md
THIS:            TEST_World_Builder.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            tests/infrastructure/test_world_builder.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

**Isolation First:** Unit tests mock external dependencies (graph, LLM, embeddings) to test logic in isolation.

**Integration Later:** Integration tests use real FalkorDB to verify full pipeline.

**Key Focus Areas:**
1. Query moment creation and linking
2. Sparsity detection accuracy
3. Enrichment application correctness
4. Error handling and graceful degradation

---

## UNIT TESTS

### Sparsity Detection

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_empty_results_sparse` | `is_sparse("query", [])` | `SparsityResult(sparse=True, reason='no_results')` | pending |
| `test_single_result_sparse` | `is_sparse("query", [1 result])` | `sparse=True` (cluster_size < 2) | pending |
| `test_low_proximity_sparse` | results with similarity < 0.6 | `sparse=True` | pending |
| `test_low_diversity_sparse` | similar results | `sparse=True` (diversity < 0.3) | pending |
| `test_low_connectedness_sparse` | isolated nodes | `sparse=True` (connectedness < 1.5) | pending |
| `test_rich_results_not_sparse` | 5+ diverse, connected results | `sparse=False` | pending |
| `test_cosine_similarity` | two vectors | correct similarity score | pending |
| `test_node_to_text_detail` | node with detail | returns detail | pending |
| `test_node_to_text_name` | node without detail | returns name | pending |
| `test_node_to_text_fallback` | node with only id | returns id | pending |

### Query Moment Recording

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_record_query_moment_creates_node` | query text, char_id | Moment node created | pending |
| `test_moment_type_thought` | query with char_id | `type='thought'` | pending |
| `test_moment_type_query` | query without char_id | `type='query'` | pending |
| `test_moment_energy` | any query | `energy=0.3` | pending |
| `test_moment_weight` | any query | `weight=0.2` | pending |
| `test_moment_links_to_character` | query with char_id | ATTACHED_TO and CAN_SPEAK links | pending |
| `test_moment_links_to_place` | query with place_id | OCCURRED_AT link | pending |
| `test_link_results_to_moment` | moment + results | ABOUT links created | pending |
| `test_link_weight_from_similarity` | results with similarity | link.weight = similarity | pending |

### WorldBuilder Class

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_init_with_api_key` | explicit key | `self.api_key` set | pending |
| `test_init_from_env` | env var set | uses ANTHROPIC_API_KEY | pending |
| `test_init_no_key_warning` | no key | logs warning | pending |
| `test_cache_key_generation` | query + char_id | unique hash | pending |
| `test_cache_hit_within_window` | same query < 60s | returns None | pending |
| `test_cache_miss_after_window` | same query > 60s | calls LLM | pending |
| `test_recursion_prevention` | concurrent calls | second returns None | pending |
| `test_parse_yaml_block` | response with ```yaml | extracts YAML | pending |
| `test_parse_plain_yaml` | response without fence | parses directly | pending |
| `test_parse_invalid_yaml` | malformed YAML | returns None | pending |
| `test_clear_cache` | after caching | cache emptied | pending |

### Enrichment Application

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_apply_characters` | enrichment with characters | Character nodes created | pending |
| `test_apply_places` | enrichment with places | Place nodes created | pending |
| `test_apply_things` | enrichment with things | Thing nodes created | pending |
| `test_apply_narratives` | enrichment with narratives | Narrative nodes created | pending |
| `test_apply_links` | enrichment with links | links created | pending |
| `test_apply_moments` | enrichment with moments | Moment nodes created | pending |
| `test_generated_flag` | any enriched node | `generated=True` | pending |
| `test_link_to_query_moment` | all created nodes | ABOUT links to query moment | pending |
| `test_moment_speaker_link` | moment with speaker_id | ATTACHED_TO + CAN_SPEAK | pending |
| `test_moment_place_link` | moment with place_id | ATTACHED_TO place | pending |

### Query Interface

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_query_records_moment` | any query | moment created | pending |
| `test_query_executes_search` | any query | semantic_search called | pending |
| `test_query_links_results` | query with results | ABOUT links created | pending |
| `test_query_checks_sparsity` | sparse results | is_sparse called | pending |
| `test_query_enriches_sparse` | sparse results | enrich called | pending |
| `test_query_requery_after_enrich` | enrichment applied | search called again | pending |
| `test_query_sync_no_enrichment` | query_sync | no LLM calls | pending |

---

## INTEGRATION TESTS

### I1: Full Query-Enrich-Return Cycle

```
GIVEN:  FalkorDB with minimal content
AND:    ANTHROPIC_API_KEY set
WHEN:   query("Who are my relatives?", graph, char_id="char_player")
THEN:   Query moment created
AND:    WorldBuilder called (sparse results)
AND:    New characters created in graph
AND:    ABOUT links from query moment to new content
AND:    Re-queried results include new characters
STATUS: pending
```

### I2: Energy Flow Through Physics

```
GIVEN:  Query moment with energy=0.3
AND:    5 ABOUT links with weight=0.8
WHEN:   Physics tick runs
THEN:   Linked nodes receive energy
AND:    Energy proportional to link weight
STATUS: pending
```

### I3: Cache Prevents Duplicate Enrichment

```
GIVEN:  Query "test query" enriched successfully
WHEN:   Same query called 30 seconds later
THEN:   No LLM call made
AND:    Returns immediately
STATUS: pending
```

### I4: Graceful LLM Failure

```
GIVEN:  Invalid API key
WHEN:   query() triggers enrichment
THEN:   No crash
AND:    Returns original sparse results
AND:    Error logged
STATUS: pending
```

### I5: Semantic Search Integration

```
GIVEN:  Graph with narrative about Edmund
AND:    Embeddings indexed
WHEN:   query("What do I know about Edmund?")
THEN:   Results include Edmund narrative
AND:    Similarity score > 0.5
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Empty query string | `test_empty_query` | pending |
| Very long query (>1000 chars) | `test_long_query` | pending |
| Query with special characters | `test_special_chars_query` | pending |
| Unicode in query | `test_unicode_query` | pending |
| Null char_id | `test_null_char_id` | pending |
| Invalid char_id (not in graph) | `test_invalid_char_id` | pending |
| Graph connection failure | `test_graph_disconnected` | pending |
| Embedding service unavailable | `test_no_embeddings` | pending |
| LLM returns empty response | `test_empty_llm_response` | pending |
| LLM returns non-YAML | `test_non_yaml_response` | pending |
| Duplicate node IDs in enrichment | `test_duplicate_ids` | pending |
| Self-referential links in enrichment | `test_self_links` | pending |
| Concurrent queries same char_id | `test_concurrent_queries` | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `sparsity.py` | ~80% | 8 unit tests passing |
| `query_moment.py` | ~70% | 7 unit tests passing |
| `world_builder.py` | ~75% | 11 unit tests passing |
| `enrichment.py` | ~80% | 10 unit tests passing |
| `query.py` | ~70% | 5 unit tests + 3 edge cases passing |

**Total:** 49 tests passing

**Target:** 80% line coverage for core logic

---

## HOW TO RUN

```bash
# Run all world builder tests
pytest tests/infrastructure/test_world_builder.py -v

# Run with coverage
pytest tests/infrastructure/test_world_builder.py --cov=engine/infrastructure/world_builder --cov-report=term-missing

# Run specific test category
pytest tests/infrastructure/test_world_builder.py -k sparsity -v
pytest tests/infrastructure/test_world_builder.py -k enrichment -v
pytest tests/infrastructure/test_world_builder.py -k query -v

# Run integration tests only (requires FalkorDB)
pytest tests/infrastructure/test_world_builder.py -m integration -v
```

---

## TEST FIXTURES

### Mock Graph

```python
@pytest.fixture
def mock_graph():
    """Mock GraphQueries for unit tests."""
    graph = Mock(spec=GraphQueries)
    graph.query.return_value = []
    graph.get_character.return_value = {'id': 'char_test', 'name': 'Test'}
    graph.get_place.return_value = {'id': 'place_test', 'name': 'Test Place'}
    return graph
```

### Mock Semantic Search

```python
@pytest.fixture
def mock_search():
    """Mock SemanticSearch for unit tests."""
    search = Mock(spec=SemanticSearch)
    search.find.return_value = [
        {'id': 'node_1', 'name': 'Result 1', 'similarity': 0.8},
        {'id': 'node_2', 'name': 'Result 2', 'similarity': 0.7},
    ]
    return search
```

### Mock LLM Response

```python
@pytest.fixture
def mock_enrichment_response():
    """Mock LLM YAML response."""
    return """```yaml
characters:
  - id: char_test_relative
    name: Test Relative
    backstory: A test relative
    character_type: minor

moments:
  - text: "I remember them."
    type: thought
    weight: 0.5
    speaker_id: char_player
```"""
```

### Real FalkorDB (Integration)

```python
@pytest.fixture
def real_graph():
    """Real FalkorDB for integration tests."""
    graph = GraphQueries(graph_name="blood_ledger_test")
    yield graph
    # Cleanup test data
    graph.query("MATCH (n) WHERE n.id STARTS WITH 'test_' DETACH DELETE n")
```

---

## KNOWN TEST GAPS

- [x] Unit tests implemented — 49 tests passing
- [ ] No property-based tests (Hypothesis)
- [ ] No performance benchmarks
- [ ] No LLM quality validation (enrichment coherence)
- [ ] No concurrent access tests
- [ ] No stress tests (many queries rapidly)
- [ ] No integration tests with real FalkorDB

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| (none yet) | — | — | — |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Create test file at `tests/infrastructure/test_world_builder.py`
- [ ] Add pytest-asyncio for async test support
- [ ] Mock anthropic client properly
- IDEA: Use VCR.py to record/replay LLM responses
- IDEA: Snapshot testing for enrichment application
- QUESTION: How to test embedding quality in sparsity detection?
- QUESTION: Should we test actual LLM responses in CI? (cost, flakiness)

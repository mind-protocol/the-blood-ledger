# World Builder — Validation: Invariants and Verification

```
STATUS: CANONICAL
CREATED: 2025-12-19
VERIFIED: Not yet verified
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM_World_Builder.md
THIS:            VALIDATION_World_Builder.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_World_Builder.md
TEST:            ./TEST_World_Builder.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

These must ALWAYS be true:

### V1: Every Query Creates a Moment

```
FORALL query(text, graph, char_id, place_id):
    EXISTS moment IN graph WHERE
        moment.text == text AND
        moment.type == 'thought' AND
        moment.status == 'possible' AND
        moment.energy == 0.3
```

**Checked by:** `test_query_creates_moment` — verify moment exists after query

### V2: Query Moments Link to Results via ABOUT

```
FORALL query(text) RETURNING results:
    moment = query_moment_for(text)
    FORALL result IN results[:5]:
        EXISTS link WHERE
            link.from == moment.id AND
            link.to == result.id AND
            link.type == 'ABOUT' AND
            link.weight == result.similarity
```

**Checked by:** `test_query_links_results` — verify ABOUT links exist with correct weights

### V3: Enriched Content Links Back to Query Moment

```
FORALL enrichment APPLIED TO query_moment:
    FORALL node IN enrichment.{characters, places, things, narratives}:
        EXISTS link WHERE
            link.from == query_moment.id AND
            link.to == node.id AND
            link.type == 'ABOUT'
```

**Checked by:** `test_enrichment_links_to_query_moment` — verify all created nodes link back

### V4: Generated Content Marked as Generated

```
FORALL node CREATED BY enrichment:
    node.generated == true
```

**Checked by:** `test_generated_content_marked` — verify `generated: true` property

### V5: All Moments Are Type "thought"

```
FORALL moment CREATED BY world_builder:
    moment.type == 'thought'
```

**Checked by:** `test_moments_always_thought_type` — verify no other types created

### V6: Sparsity Detection Threshold Consistency

```
is_sparse(query, results) == true IFF:
    proximity < 0.6 OR
    cluster_size < 2 OR
    diversity < 0.3 OR
    connectedness < 1.5
```

**Checked by:** `test_sparsity_thresholds` — verify thresholds match constants

### V7: Cache Prevents Repeated Enrichment

```
FORALL query_hash:
    IF enriched_at(query_hash) < 60 seconds ago:
        enrich(query_hash) RETURNS None
```

**Checked by:** `test_enrichment_cache` — verify cache prevents re-enrichment within window

### V8: Recursion Prevention

```
FORALL query_hash CURRENTLY BEING ENRICHED:
    enrich(query_hash) RETURNS None (immediate)
```

**Checked by:** `test_recursion_prevention` — verify concurrent enrichment blocked

---

## PROPERTIES

For property-based testing:

### P1: Query Always Returns List

```
FORALL query_text, graph, char_id, place_id:
    result = query(query_text, graph, char_id, place_id)
    isinstance(result, list)
```

**Tested by:** `test_query_returns_list` | NOT YET TESTED

### P2: Sparsity Result Complete

```
FORALL query_text, results:
    sparsity = is_sparse(query_text, results)
    sparsity.sparse IS bool
    sparsity.proximity IS float IN [0, 1]
    sparsity.cluster_size IS int >= 0
    sparsity.diversity IS float IN [0, 1]
    sparsity.connectedness IS float >= 0
```

**Tested by:** `test_sparsity_result_complete` | NOT YET TESTED

### P3: Empty Results Always Sparse

```
FORALL query_text:
    is_sparse(query_text, []).sparse == True
    is_sparse(query_text, []).reason == 'no_results'
```

**Tested by:** `test_empty_results_sparse` | NOT YET TESTED

### P4: Enrichment YAML Parseable

```
FORALL valid_llm_response:
    parse_response(response) IS Dict OR None
    (never raises exception)
```

**Tested by:** `test_yaml_parsing_safe` | NOT YET TESTED

### P5: Character Linking Bidirectional

```
FORALL moment WITH char_id:
    EXISTS (moment)-[:ATTACHED_TO]->(character)
    EXISTS (character)-[:CAN_SPEAK]->(moment)
```

**Tested by:** `test_character_linking_bidirectional` | NOT YET TESTED

---

## ERROR CONDITIONS

### E1: No API Key

```
WHEN:    WorldBuilder initialized without API key
THEN:    enrich() returns None, logs warning
SYMPTOM: No enrichment occurs, query returns original results
```

**Tested by:** `test_no_api_key` | NOT YET TESTED

### E2: LLM Call Failure

```
WHEN:    Anthropic API returns error
THEN:    enrich() returns None, logs error
SYMPTOM: Query returns original sparse results
```

**Tested by:** `test_llm_failure` | NOT YET TESTED

### E3: Invalid YAML Response

```
WHEN:    LLM returns unparseable YAML
THEN:    _parse_response() returns None, logs warning
SYMPTOM: No enrichment applied, query returns original results
```

**Tested by:** `test_invalid_yaml` | NOT YET TESTED

### E4: Semantic Search Failure

```
WHEN:    SemanticSearch.find() raises exception
THEN:    query() returns empty list, logs warning
SYMPTOM: No results, but moment still created
```

**Tested by:** `test_search_failure` | NOT YET TESTED

### E5: Graph Query Failure

```
WHEN:    Graph query fails (connection, syntax)
THEN:    Function logs warning, continues gracefully
SYMPTOM: Partial operation - moment may exist without links
```

**Tested by:** `test_graph_failure` | NOT YET TESTED

### E6: Missing Embeddings

```
WHEN:    embed_fn returns None for all inputs
THEN:    is_sparse() uses heuristics (cluster_size only)
SYMPTOM: Sparsity detection degrades to count-based
```

**Tested by:** `test_missing_embeddings` | NOT YET TESTED

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Query creates moment | `test_query_creates_moment` | NOT YET TESTED |
| V2: ABOUT links | `test_query_links_results` | NOT YET TESTED |
| V3: Enrichment links back | `test_enrichment_links_to_query_moment` | NOT YET TESTED |
| V4: Generated marked | `test_generated_content_marked` | NOT YET TESTED |
| V5: Thought type | `test_moments_always_thought_type` | NOT YET TESTED |
| V6: Sparsity thresholds | `test_sparsity_thresholds` | NOT YET TESTED |
| V7: Cache | `test_enrichment_cache` | NOT YET TESTED |
| V8: Recursion | `test_recursion_prevention` | NOT YET TESTED |
| P1: Returns list | `test_query_returns_list` | NOT YET TESTED |
| P2: Sparsity complete | `test_sparsity_result_complete` | NOT YET TESTED |
| P3: Empty sparse | `test_empty_results_sparse` | NOT YET TESTED |
| E1: No API key | `test_no_api_key` | NOT YET TESTED |
| E2: LLM failure | `test_llm_failure` | NOT YET TESTED |
| E3: Invalid YAML | `test_invalid_yaml` | NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — query creates moment with correct properties
[ ] V2 holds — results linked via ABOUT with similarity weights
[ ] V3 holds — enriched content links back to query moment
[ ] V4 holds — generated content has generated: true
[ ] V5 holds — all moments are type 'thought'
[ ] V6 holds — sparsity thresholds match constants
[ ] V7 holds — cache prevents re-enrichment within 60s
[ ] V8 holds — recursive enrichment blocked
[ ] All error conditions handled gracefully
```

### Automated

```bash
# Run world builder tests
pytest tests/infrastructure/test_world_builder.py -v

# Run with coverage
pytest tests/infrastructure/test_world_builder.py --cov=engine/infrastructure/world_builder

# Run sparsity tests only
pytest tests/infrastructure/test_world_builder.py -k sparsity -v
```

---

## INTEGRATION TESTS

### I1: Full Query-Enrich Cycle

```
GIVEN:  Graph with seeded content
AND:    Query "Who are my relatives?" with char_id="char_player"
WHEN:   Results are sparse (no relatives exist)
THEN:   WorldBuilder enriches with new characters
AND:    New characters have RELATED_TO links to player
AND:    Query moment links to all created content
STATUS: NOT YET TESTED
```

### I2: Physics Energy Flow

```
GIVEN:  Query moment with energy=0.3
AND:    ABOUT links to results with weight
WHEN:   Physics tick runs
THEN:   Energy flows from moment to linked nodes
AND:    Linked nodes gain energy proportional to weight
STATUS: NOT YET TESTED
```

### I3: Cache Behavior

```
GIVEN:  Query "test" enriched at T=0
WHEN:   Same query at T=30s
THEN:   Returns cached (no LLM call)
WHEN:   Same query at T=70s
THEN:   Triggers new enrichment
STATUS: NOT YET TESTED
```

### I4: Semantic Search Integration

```
GIVEN:  Graph with narrative "Edmund betrayed the king"
WHEN:   Query "What do I know about Edmund?"
THEN:   Results include the narrative
AND:    Similarity score > 0.5
STATUS: NOT YET TESTED
```

---

## PERFORMANCE BENCHMARKS

| Operation | Expected | Actual |
|-----------|----------|--------|
| `is_sparse()` (10 results) | < 100ms | TBD |
| `record_query_moment()` | < 50ms | TBD |
| `link_results_to_moment()` (5 links) | < 100ms | TBD |
| `apply_enrichment()` (10 nodes) | < 500ms | TBD |
| Full `query()` without enrichment | < 1s | TBD |
| Full `query()` with enrichment | < 10s | TBD |

---

## SYNC STATUS

```
LAST_VERIFIED: Not yet verified
VERIFIED_AGAINST: N/A (newly implemented)
VERIFIED_BY: N/A
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
    V4: NOT RUN
    V5: NOT RUN
    V6: NOT RUN
    V7: NOT RUN
    V8: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Property-based testing with Hypothesis for sparsity detection
- [ ] Integration test with real FalkorDB
- [ ] LLM response quality validation (is enrichment coherent?)
- [ ] Performance regression tests
- IDEA: Validate enrichment against world lore consistency
- IDEA: Track enrichment acceptance rate for quality metrics
- QUESTION: Should we validate node IDs don't conflict with existing?
- QUESTION: How to test energy flow through physics tick?

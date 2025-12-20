# Map System — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the Map System, specifically the semantic search and discovery layers. It ensures that players can consistently find places and narratives using natural language and that the search results remain relevant and schema-compliant.

What it protects:
- **Discovery Accuracy**: Relevance of semantic search results for player queries.
- **Failover Reliability**: Proper degradation to fallback search when vector indices fail.
- **Data Integrity**: Consistency of coordinates and descriptive fields in search results.

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

IMPL:            engine/world/map/semantic.py
```

> **Contract:** HEALTH checks verify intent and result ordering without modifying search logic.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: semantic_search
    purpose: Provide discovery results based on player intent.
    triggers:
      - type: manual
        source: UI Search Bar
    frequency:
      expected_rate: 0.5/min
      peak_rate: 5/min
      burst_behavior: Limited by embedding service latency.
    risks:
      - Irrelevant results (low similarity)
      - Missing entities due to stale indices
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: search_relevance
    flow_id: semantic_search
    priority: high
    rationale: Core discovery mechanic must work for natural language.
  - name: fallback_availability
    flow_id: semantic_search
    priority: med
    rationale: Keyword search must work if the vector index is unavailable.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: stdout
  result:
    representation: score
    value: 0.90
    updated_at: 2025-12-20T10:20:00Z
    source: manual_search_check
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: similarity_threshold_validator
    purpose: Ensure results respect min_similarity bounds.
    status: active
    priority: med
  - name: vector_index_monitor
    purpose: Detect and alert on vector query failures.
    status: pending
    priority: high
```

---

## INDICATOR: search_relevance

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: search_relevance
  client_value: Allows players to find story content by describing it.
  validation:
    - validation_id: V2 (Map)
      criteria: find() returns results above similarity threshold.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: search_input
    method: engine.world.map.semantic.SemanticSearch.find
    location: engine/world/map/semantic.py:65
  output:
    id: search_output
    method: engine.world.map.semantic.SemanticSearch.find
    location: engine/world/map/semantic.py:115
```

---

## KNOWN GAPS

- [ ] Automated regression for vector index failures.
- [ ] Relevance benchmarking against a golden set of queries.
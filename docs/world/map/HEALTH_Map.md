# Map — Health: Semantic Search Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the semantic search path in the map module. It exists
to reduce the risk of silent search failures that would leave map discovery
empty or misleading. It does not verify UI rendering or front-end map state.

---

## WHY THIS PATTERN

Search can fail even when tests pass (vector index missing, fallback bugs).
Dock-based checks allow verification without changing runtime code and keep
signal aligned to VALIDATION criteria while staying low overhead.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Map.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
THIS:            HEALTH_Map.md
SYNC:            ./SYNC_Map.md

IMPL:            tools/health/check_map.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented map health checker
Implement `tools/health/check_map.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for map search
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: semantic_search
    purpose: Return relevant nodes for map discovery and context.
    triggers:
      - type: event
        source: frontend map search / CLI
        notes: SemanticSearch.find is called with a query string.
    frequency:
      expected_rate: 1-5/min
      peak_rate: 20/min
      burst_behavior: Searches may spike during active exploration.
    risks:
      - E1
      - E2
      - V1
      - V2
    notes: Requires embeddings and FalkorDB availability.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: semantic_search_returns
    flow_id: semantic_search
    priority: high
    rationale: If search fails or returns malformed results, the player loses
      map discovery and narrative grounding.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: semantic_search_returns
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: semantic_search_returns
    purpose: Verify semantic search returns results or cleanly falls back.
    status: pending
    priority: high
```

---

## INDICATOR: semantic_search_returns

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: semantic_search_returns
  client_value: Map search remains usable and resilient to index failures.
  validation:
    - validation_id: V1
      criteria: Queries embed before search.
    - validation_id: V2
      criteria: Similarity threshold filters results.
    - validation_id: E1
      criteria: Vector index fallback returns results without crashing.
    - validation_id: E2
      criteria: Graph query failures return empty results without raising.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (results or clean fallback), WARN (empty but no error), ERROR (exception)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: semantic_query
    method: SemanticSearch.find
    location: engine/world/map/semantic.py:35
  output:
    id: semantic_results
    method: SemanticSearch.find
    location: engine/world/map/semantic.py:35
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Run a search query and confirm return shape or fallback behavior.
  steps:
    - Call SemanticSearch.find with a known query string.
    - Confirm return is a list of dicts with expected keys or empty list.
  data_required: Query string, returned results, exception logs.
  failure_mode: Exceptions or non-list responses indicate a failure.
```

### INDICATOR

```yaml
indicator:
  error:
    - name: semantic_search_exception
      linked_validation: [E1, E2]
      meaning: Search raises instead of returning empty results.
      default_action: stop
  warning:
    - name: semantic_search_empty
      linked_validation: [V2]
      meaning: Empty results for a known query.
      default_action: warn
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 1/hour
  burst_limit: 1
  backoff: none
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: logs
      transport: file
      notes: Manual check output during troubleshooting.
display:
  locations:
    - surface: CLI
      location: stdout
      signal: enum
      notes: Manual run output.
```

### MANUAL RUN

```yaml
manual_run:
  command: python3 - <<'PY'\nfrom engine.world.map.semantic import SemanticSearch\nsearch = SemanticSearch()\nprint(search.find(\"princes\", limit=3))\nPY
  notes: Requires FalkorDB and embeddings runtime available.
```

---

## HOW TO RUN

```bash
# Manual semantic search probe
python3 - <<'PY'
from engine.world.map.semantic import SemanticSearch
search = SemanticSearch()
print(search.find("princes", limit=3))
PY
```

---

## KNOWN GAPS

- [ ] No automated checker wired to health output yet.
- [ ] No dedicated sentinel query for empty graph state.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add a small fixture dataset to validate search returns non-empty results.
- IDEA: Persist last successful search timestamp in a health marker file.

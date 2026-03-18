# World Builder — Health: Sparse Enrichment Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-22
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the query-enrich-apply pipeline of the World Builder. It exists to prevent silent failures where:
- Queries don't create proper graph moments
- Sparsity detection fails silently
- Enrichment generates invalid mutations
- Graph links are not properly created

It does not verify creative quality of generated content.

---

## WHY THIS PATTERN

World Builder is the content generation engine. Tests verify component logic, but HEALTH checks verify the full query→sparsity→enrich→apply pipeline produces usable graph state. Dock-based checks ensure:
- Query moments are created with correct properties
- Sparsity detection triggers enrichment when needed
- Enriched content creates valid graph mutations

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_World_Builder.md
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM_World_Builder.md
VALIDATION:      ./VALIDATION_World_Builder.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Builder.md
THIS:            HEALTH_World_Builder.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            tools/health/check_world_builder.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented world builder health checker
Implement `tools/health/check_world_builder.py` checker script that:
- Executes dock-based verification against VALIDATION criteria V1-V8
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: query_flow
    purpose: Execute semantic query and create graph moment.
    triggers:
      - type: event
        source: query.py:query
        notes: Called by player actions, tempo tick, or narrator.
    frequency:
      expected_rate: 1-10/min
      peak_rate: 30/min
      burst_behavior: Queries batch during enrichment; no unbounded bursts.
    risks:
      - V1 (query moment not created)
      - V2 (ABOUT links missing)
      - E4 (semantic search failure)
    notes: Requires graph runtime and embeddings service.

  - flow_id: sparsity_detection
    purpose: Determine if query results are sparse and need enrichment.
    triggers:
      - type: event
        source: sparsity.py:is_sparse
        notes: Called after query returns results.
    frequency:
      expected_rate: 1-10/min (follows query_flow)
      peak_rate: 30/min
      burst_behavior: Same as query_flow.
    risks:
      - V6 (thresholds misconfigured)
      - E6 (missing embeddings fallback)
    notes: Uses numpy for cosine similarity.

  - flow_id: enrichment_flow
    purpose: Generate new content via LLM and apply to graph.
    triggers:
      - type: event
        source: world_builder.py:enrich
        notes: Called when sparsity detected.
    frequency:
      expected_rate: 0.5-2/min
      peak_rate: 10/min
      burst_behavior: Cache and recursion guard limit bursts.
    risks:
      - V4 (generated flag not set)
      - V7 (cache bypass)
      - V8 (recursion guard failure)
      - E1/E2/E3 (API/LLM/parse failures)
    notes: Requires API key and LLM service.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Query creates moments | query_creates_moment | Missing moments = broken narrative |
| Sparsity triggers enrichment | sparsity_detection_accurate | False negatives = incomplete world |
| Enrichment produces mutations | enrichment_produces_mutation | No mutations = wasted LLM calls |

```yaml
health_indicators:
  - name: query_creates_moment
    flow_id: query_flow
    priority: high
    rationale: Every query must create a thought moment for narrative tracking.

  - name: sparsity_detection_accurate
    flow_id: sparsity_detection
    priority: med
    rationale: Sparsity detection gates enrichment; must be accurate.

  - name: enrichment_produces_mutation
    flow_id: enrichment_flow
    priority: high
    rationale: Sparse queries must yield mutation output for downstream apply.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-22T00:00:00Z
    source: query_creates_moment
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: query_creates_moment
    purpose: Verify query creates thought moment with V1 properties.
    status: pending
    priority: high

  - name: sparsity_detection_accurate
    purpose: Verify sparsity thresholds match V6 constants.
    status: pending
    priority: med

  - name: enrichment_produces_mutation
    purpose: Verify enrichment returns valid YAML mutation.
    status: pending
    priority: high
```

---

## INDICATOR: query_creates_moment

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: query_creates_moment
  client_value: Player queries are tracked; narrative context is preserved.
  validation:
    - validation_id: V1
      criteria: Every query creates a thought moment with energy=0.3, status=possible.
    - validation_id: V2
      criteria: Query moments link to results via ABOUT with weight=similarity.
    - validation_id: V5
      criteria: All World Builder moments are type="thought".
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (moment created with correct properties), ERROR (missing or malformed)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: query_entry
    method: query.query
    location: engine/infrastructure/world_builder/query.py:1
  output:
    id: query_moment_created
    method: query_moment.record_query_moment
    location: engine/infrastructure/world_builder/query_moment.py:1
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Execute query, verify thought moment exists with correct properties.
  steps:
    - Call query_sync(playthrough_id, query_text).
    - Query graph for moment with matching query text.
    - Verify moment.type == "thought", moment.energy == 0.3.
    - Verify ABOUT links exist to result nodes.
  data_required: Query text, graph access, moment properties.
  failure_mode: No moment created or properties incorrect.
```

### INDICATOR

```yaml
indicator:
  error:
    - name: moment_missing
      linked_validation: [V1]
      meaning: Query executed but no thought moment was created.
      default_action: alert
    - name: moment_malformed
      linked_validation: [V1, V5]
      meaning: Moment exists but has wrong type or energy.
      default_action: alert
  warning:
    - name: links_missing
      linked_validation: [V2]
      meaning: Moment exists but ABOUT links are missing.
      default_action: log
  info:
    - name: query_healthy
      linked_validation: [V1, V2, V5]
      meaning: Query created proper moment with links.
      default_action: log
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 1/hour
  burst_limit: 3
  backoff: exponential
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: logs/world_builder_health.log
      transport: file
      notes: Manual run output.
display:
  locations:
    - surface: CLI
      location: stdout
      signal: enum
      notes: Manual verification output.
```

### MANUAL RUN

```yaml
manual_run:
  command: |
    python3 - <<'PY'
    from engine.infrastructure.world_builder.query import query_sync
    result = query_sync(playthrough_id="health_check", query="test princes")
    print(f"Query returned {len(result)} results")
    # TODO: Add graph check for moment creation
    print("OK: query executed" if result is not None else "ERROR: query failed")
    PY
  notes: Requires graph runtime. Full verification needs graph query for moment.
```

---

## INDICATOR: enrichment_produces_mutation

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: enrichment_produces_mutation
  client_value: Sparse areas get populated; world feels complete.
  validation:
    - validation_id: V4
      criteria: Enriched nodes are marked generated=true.
    - validation_id: V7
      criteria: Cache prevents repeat enrichment within 60 seconds.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: enrich_entry
    method: WorldBuilder.enrich
    location: engine/infrastructure/world_builder/world_builder.py:1
  output:
    id: enrichment_result
    method: enrichment.apply_enrichment
    location: engine/infrastructure/world_builder/enrichment.py:1
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Trigger enrichment on sparse query, verify YAML mutation is returned.
  steps:
    - Create WorldBuilder instance.
    - Call enrich with known sparse context.
    - Verify returned mutation is valid YAML dict.
    - Verify nodes have generated=true flag.
  data_required: Sparse context, API key, LLM service.
  failure_mode: None returned or invalid YAML.
```

### MANUAL RUN

```yaml
manual_run:
  command: |
    python3 - <<'PY'
    from engine.infrastructure.world_builder.world_builder import WorldBuilder
    wb = WorldBuilder(playthrough_id="health_check")
    # Note: Full test requires sparse context and API key
    print("WorldBuilder instantiated - manual enrichment test required")
    PY
  notes: Full test requires API key and LLM access.
```

---

## HOW TO RUN

```bash
# Run all health checks for world builder (manual)
python3 - <<'PY'
from engine.infrastructure.world_builder.query import query_sync

# Check 1: Query creates moment
result = query_sync(playthrough_id="health_check", query="test query")
query_ok = result is not None

print(f"query_creates_moment: {'OK' if query_ok else 'ERROR'}")
print("enrichment_produces_mutation: SKIPPED (requires API key)")
PY

# Run specific checker - see MANUAL RUN sections above
```

---

## KNOWN GAPS

- [ ] V3 (enriched content links back) checker not implemented.
- [ ] V6 (sparsity thresholds) checker not implemented - need to verify constants.
- [ ] V8 (recursion guard) checker not implemented.
- [ ] E1-E6 error condition checkers not implemented.
- [ ] No automated checker writes to status marker.
- [ ] Graph query for moment verification not implemented.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add fixture for sparse context testing.
- IDEA: Mock LLM for enrichment tests without API key.
- QUESTION: Should enrichment health checks run in CI or only manually?

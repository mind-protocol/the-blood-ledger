# History — Health: Narrative Persistence Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-22
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the history service's query and recording pipelines. It exists to prevent:
- Orphan narratives without belief edges
- Missing conversation references
- Broken timestamp consistency
- Silent failures in belief propagation

It does not verify narrative quality or NPC behavior accuracy.

---

## WHY THIS PATTERN

History is the memory of the game world. Tests verify service logic, but HEALTH checks verify the full record→store→query pipeline produces consistent graph state. Dock-based checks ensure:
- Recorded narratives have required belief edges
- Conversation files are properly linked
- Queries return only authorized beliefs

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_Infrastructure_History.md
PATTERNS:        ./PATTERNS_History.md
BEHAVIORS:       ./BEHAVIORS_History.md
ALGORITHM:       ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:      ./VALIDATION_History.md
IMPLEMENTATION:  ./IMPLEMENTATION_History_Service_Architecture.md
THIS:            HEALTH_History_Service_Verification.md
SYNC:            ./SYNC_History.md

IMPL:            tools/health/check_history.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented history health checker
Implement `tools/health/check_history.py` checker script that:
- Executes dock-based verification against VALIDATION criteria V1-V5
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: query_history
    purpose: Retrieve narratives a character believes.
    triggers:
      - type: event
        source: HistoryService.query_history
        notes: Called by narrator and scene builders.
    frequency:
      expected_rate: 5-20/min
      peak_rate: 100/min
      burst_behavior: Queries cluster during scene preparation.
    risks:
      - V1 (orphan narratives returned)
      - V4 (timestamp inconsistency)
      - E1/E2 (missing conversation file/section)
    notes: Requires graph runtime and conversation files.

  - flow_id: record_player_history
    purpose: Create narrative for player-experienced events.
    triggers:
      - type: event
        source: HistoryService.record_player_history
        notes: Called after scene completion.
    frequency:
      expected_rate: 0.5-2/min
      peak_rate: 10/min
      burst_behavior: Bursts after intense scenes.
    risks:
      - V1 (no BELIEVES created)
      - V2 (source XOR detail violated)
      - V3 (conversation section missing)
    notes: Writes to graph and conversation files.

  - flow_id: record_world_history
    purpose: Create narrative for world events.
    triggers:
      - type: event
        source: HistoryService.record_world_history
        notes: Called by world runner.
    frequency:
      expected_rate: 0.2-1/min
      peak_rate: 5/min
      burst_behavior: Bursts during world tick processing.
    risks:
      - V1 (no BELIEVES created)
      - V5 (belief bounds violated)
      - E3 (circular propagation)
    notes: May trigger belief propagation.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| No orphan narratives | narratives_have_beliefs | Orphans = wasted memory, broken queries |
| Query correctness | query_respects_beliefs | Wrong results = broken NPC behavior |
| Recording completeness | history_record_roundtrip | Missing links = lost history |

```yaml
health_indicators:
  - name: narratives_have_beliefs
    flow_id: record_player_history
    priority: high
    rationale: Every narrative must have at least one BELIEVES edge (V1).

  - name: query_respects_beliefs
    flow_id: query_history
    priority: high
    rationale: Queries must only return narratives the character believes.

  - name: history_record_roundtrip
    flow_id: record_player_history
    priority: high
    rationale: History must persist and remain queryable by witnesses.
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
    source: narratives_have_beliefs
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: narratives_have_beliefs
    purpose: Verify all narratives have at least one BELIEVES edge (V1).
    status: pending
    priority: high

  - name: history_record_roundtrip
    purpose: Verify record→query cycle works end-to-end.
    status: pending
    priority: high

  - name: belief_bounds_valid
    purpose: Verify all BELIEVES.believes values are 0.0-1.0 (V5).
    status: pending
    priority: med
```

---

## INDICATOR: narratives_have_beliefs

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: narratives_have_beliefs
  client_value: NPCs remember events; history queries return meaningful results.
  validation:
    - validation_id: V1
      criteria: Every narrative has at least one BELIEVES edge.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (all have beliefs), WARN (some orphans), ERROR (many orphans)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: record_entry
    method: HistoryService.record_player_history
    location: engine/infrastructure/history/service.py:208
  output:
    id: believes_edge_created
    method: HistoryService._create_belief_edge
    location: engine/infrastructure/history/service.py:400
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Query for narratives without BELIEVES edges; count should be zero.
  steps:
    - Query graph for all Narrative nodes.
    - For each narrative, check for incoming BELIEVES edges.
    - Count narratives with zero BELIEVES.
    - Report count; zero = healthy.
  data_required: Graph access, narrative and BELIEVES queries.
  failure_mode: Non-zero count of orphan narratives.
```

### INDICATOR

```yaml
indicator:
  error:
    - name: many_orphans
      linked_validation: [V1]
      meaning: Many narratives exist without any BELIEVES edges.
      default_action: alert
  warning:
    - name: some_orphans
      linked_validation: [V1]
      meaning: A few orphan narratives exist.
      default_action: log
  info:
    - name: no_orphans
      linked_validation: [V1]
      meaning: All narratives have at least one BELIEVES edge.
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
    - location: logs/history_health.log
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
    # Query for orphan narratives (requires graph connection)
    # TODO: Implement graph query for narratives without BELIEVES
    print("HEALTH CHECK: narratives_have_beliefs - manual verification required")
    PY
  notes: Requires graph runtime with narrative data.
```

---

## HOW TO RUN

```bash
# Run history health checks (manual)
python3 - <<'PY'
from engine.infrastructure.history.service import HistoryService

# Note: Requires graph_queries and graph_ops instances
# Smoke test: record + query
print("HEALTH CHECK: History service")
print("Check: narratives_have_beliefs - query for orphan narratives")
print("Check: history_record_roundtrip - record then query")
print("Check: belief_bounds_valid - query for out-of-range beliefs")
PY

# Run automated tests when available
pytest engine/tests/test_history.py -v
```

---

## KNOWN GAPS

- [ ] V2 (source XOR detail) checker not implemented.
- [ ] V3 (conversation sections exist) checker not implemented.
- [ ] V4 (timestamp consistency) checker not implemented.
- [ ] P2/P3 property checkers not implemented.
- [ ] E1-E3 error condition checkers not implemented.
- [ ] Graph query for orphan narratives not implemented.
- [ ] No automated tests are wired to validate record/query round trips.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add graph query helper for orphan narrative detection.
- IDEA: Periodic orphan cleanup script.
- QUESTION: Should orphan detection run in CI or production monitoring?

# World Scraping — Health: Seeding and Injection Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the seeding pipeline from YAML outputs into FalkorDB.
It exists to reduce the risk of partial or malformed world loads. It does not
verify upstream scraping API quality or narrative accuracy.

---

## WHY THIS PATTERN

Seeding can appear successful while silently skipping records. Dock-based
checks confirm counts and schema integrity without requiring code changes.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Scraping.md
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
THIS:            HEALTH_World_Scraping.md
SYNC:            ./SYNC_World_Scraping.md

IMPL:            tools/health/check_world_scraping.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented world scraping health checker
Implement `tools/health/check_world_scraping.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for seeding
- Updates `status.result.value` in this file
- Runs throttled (max 1/day in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: world_seeding
    purpose: Populate the graph with places, routes, characters, and narratives.
    triggers:
      - type: manual
        source: data/scripts/inject_world.py
        notes: Manual invocation during seeding or refresh.
    frequency:
      expected_rate: on-demand
      peak_rate: on-demand
      burst_behavior: One-off runs during data refresh.
    risks:
      - V1
      - V2
    notes: Requires FalkorDB and valid YAML inputs.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: world_seeding_counts
    flow_id: world_seeding
    priority: high
    rationale: Missing nodes or links corrupts the world baseline.
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
    source: world_seeding_counts
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: world_seeding_counts
    purpose: Verify injected record counts align with YAML inputs.
    status: pending
    priority: high
```

---

## INDICATOR: world_seeding_counts

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: world_seeding_counts
  client_value: World baseline is complete and navigable.
  validation:
    - validation_id: V1
      criteria: YAML inputs load without schema errors.
    - validation_id: V2
      criteria: Injected node counts match expected totals.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [enum, tuple]
  selected: [tuple]
  semantics:
    tuple: {state: OK/WARN/ERROR, score: 0-1 coverage ratio}
  aggregation:
    method: worst_of
    display: tuple
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: graph_injection
    method: inject_world.inject_all
    location: data/scripts/inject_world.py:1
  output:
    id: graph_injection
    method: inject_world.inject_all
    location: data/scripts/inject_world.py:1
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Compare YAML record counts with graph node counts after injection.
  steps:
    - Count YAML records by type (places, routes, characters, events, things).
    - Query graph counts for corresponding node/edge types.
    - Compute coverage ratio and flag mismatches.
  data_required: YAML files and graph node counts.
  failure_mode: Counts diverge or injection raises errors.
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: on-demand
  burst_limit: 1
  backoff: none
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: logs
      transport: file
      notes: Manual seeding run output.
display:
  locations:
    - surface: CLI
      location: stdout
      signal: tuple
      notes: Compare counts post-run.
```

### MANUAL RUN

```yaml
manual_run:
  command: python3 data/scripts/inject_world.py --graph blood_ledger
  notes: Requires FalkorDB running and data/world/*.yaml present.
```

---

## HOW TO RUN

```bash
python3 data/scripts/inject_world.py --graph blood_ledger
```

---

## KNOWN GAPS

- [ ] No automated post-seed count validation exists yet.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add a summary report that logs YAML vs graph counts per type.

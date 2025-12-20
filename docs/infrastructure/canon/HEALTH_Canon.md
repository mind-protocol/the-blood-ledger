# Canon Holder — Health: Canon Recording Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the canon recording flow that turns moments into
spoken history and emits SSE updates. It exists to prevent silent failures
that would desync canon state and player output. It does not verify narration
quality or UI rendering.

---

## WHY THIS PATTERN

Canon recording can partially succeed (status flipped, but no SSE broadcast).
Dock-based checks ensure the full sequence completes without changing code.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Canon.md
BEHAVIORS:       ./BEHAVIORS_Canon.md
ALGORITHM:       ./ALGORITHM_Canon_Holder.md
VALIDATION:      ./VALIDATION_Canon.md
IMPLEMENTATION:  ./IMPLEMENTATION_Canon.md
THIS:            HEALTH_Canon.md
SYNC:            ./SYNC_Canon.md

IMPL:            engine/infrastructure/canon/canon_holder.py
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: canon_recording
    purpose: Promote moments to spoken canon and emit SSE events.
    triggers:
      - type: event
        source: CanonHolder.record_to_canon
        notes: Called after narration or tick processing.
    frequency:
      expected_rate: 1-10/min
      peak_rate: 50/min
      burst_behavior: Spikes during combat or high-tension scenes.
    risks:
      - V1
      - V2
    notes: Requires graph runtime and SSE broadcast support.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: canon_recording_pipeline
    flow_id: canon_recording
    priority: high
    rationale: Canon state must match what players see.
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
    source: canon_recording_pipeline
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: canon_recording_pipeline
    purpose: Validate status flip, energy cost, and SSE emission.
    status: pending
    priority: high
```

---

## INDICATOR: canon_recording_pipeline

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: canon_recording_pipeline
  client_value: Spoken moments are consistent and visible to the player.
  validation:
    - validation_id: V1
      criteria: Moment status flips to spoken with tick_spoken.
    - validation_id: V2
      criteria: THEN chain and SAID link are created when applicable.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [enum]
  selected: [enum]
  semantics:
    enum: OK (all steps complete), ERROR (missing graph or SSE step)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: canon_input
    method: CanonHolder.record_to_canon
    location: engine/infrastructure/canon/canon_holder.py:55
  output:
    id: canon_output
    method: broadcast_moment_event
    location: engine/infrastructure/api/sse_broadcast.py:1
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Record a moment and verify status, links, and SSE emission.
  steps:
    - Call record_to_canon for a known moment.
    - Confirm moment status is spoken and THEN/SAID links exist.
    - Confirm SSE broadcast fires for the same moment.
  data_required: Moment data, graph links, SSE logs.
  failure_mode: Missing links or no SSE emission.
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
      notes: Manual run output for troubleshooting.
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
  command: python3 - <<'PY'\nfrom engine.infrastructure.canon.canon_holder import CanonHolder\ncanon = CanonHolder(\"default\")\nprint(canon.record_to_canon(\"mom_example\"))\nPY
  notes: Requires FalkorDB, graph runtime, and SSE broadcast support.
```

---

## HOW TO RUN

```bash
python3 - <<'PY'
from engine.infrastructure.canon.canon_holder import CanonHolder
canon = CanonHolder("default")
print(canon.record_to_canon("mom_example"))
PY
```

---

## KNOWN GAPS

- [ ] SSE broadcast implementation file is missing from this repo.
- [ ] No automated checker writes a status marker.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add a canonical fixture moment for manual health checks.

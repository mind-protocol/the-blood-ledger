# Canon Holder — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the Canon Holder. It ensures that every story beat is recorded correctly, causality (the THEN chain) is preserved, and the frontend is notified of new spoken moments without delay.

What it protects:
- **Causal Integrity**: Guaranteeing that history flows forward without loops or branches.
- **Narrative Delivery**: Ensuring SSE events are broadcast for every recorded moment.
- **State Authoritativeness**: Keeping spoken status and energy costs consistent.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Canon.md
BEHAVIORS:       ./BEHAVIORS_Canon.md
ALGORITHM:       ./ALGORITHM_Canon_Holder.md
VALIDATION:      ./VALIDATION_Canon.md
IMPLEMENTATION:  ./IMPLEMENTATION_Canon.md
THIS:            TEST_Canon.md
SYNC:            ./SYNC_Canon.md

IMPL:            engine/infrastructure/canon/canon_holder.py
```

> **Contract:** HEALTH checks verify the transition from active to spoken status and the resulting notification.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: canon_recording
    purpose: Move potential moments into immutable history.
    triggers:
      - type: event
        source: Orchestrator
        notes: Triggered after the Narrator produces new dialogue or narration.
    frequency:
      expected_rate: 3/min (during conversation)
      peak_rate: 10/min (during high-energy flips)
      burst_behavior: Serialized queue to maintain history order.
    risks:
      - Out-of-order THEN links
      - Lost SSE events
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: history_continuity
    flow_id: canon_recording
    priority: high
    rationale: A broken history chain makes backtracking and summarization impossible.
  - name: broadcast_success
    flow_id: canon_recording
    priority: high
    rationale: If SSE fails, the game appears stuck to the player.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: logs
  result:
    representation: enum
    value: OK
    updated_at: 2025-12-20T10:30:00Z
    source: canon_holder_checks
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: then_chain_validator
    purpose: Ensure exactly one THEN link exists per spoken moment (V2).
    status: active
    priority: high
  - name: sse_delivery_monitor
    purpose: Confirm broadcast calls occur after graph writes.
    status: pending
    priority: med
```

---

## INDICATOR: history_continuity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: history_continuity
  client_value: Preserves the story arc and allows for perfect memory callbacks.
  validation:
    - validation_id: V2 (Canon)
      criteria: THEN links form a linear chain.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: canon_input
    method: engine.infrastructure.canon.canon_holder.CanonHolder.record_to_canon
    location: engine/infrastructure/canon/canon_holder.py:54
  output:
    id: canon_output
    method: engine.infrastructure.api.sse_broadcast.broadcast_moment_event
    location: engine/infrastructure/api/sse_broadcast.py:25
```

---

## HOW TO RUN

```bash
# Run canon unit and integration checks
pytest tests/infrastructure/canon/ -v
```

---

## KNOWN GAPS

- [ ] Stress testing of concurrent recording requests.
- [ ] Visual trace tool for history chain inspection.
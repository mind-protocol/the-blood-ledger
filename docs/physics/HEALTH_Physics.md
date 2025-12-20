# Physics — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2024-12-18
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the Physics module. It safeguards the "living world" metabolism, ensuring that energy flows correctly, narratives flip as intended, and the system remains near a critical threshold for dramatic interest.

What it protects:
- **Narrative Metabolism**: Correct energy flow and decay across the graph.
- **Dramatic Momentum**: Proper flip detection and handler triggering.
- **State Integrity**: Consistency of weight, energy, and status properties.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Physics.md
BEHAVIORS:       ./BEHAVIORS_Physics.md
ALGORITHM:       ./ALGORITHM_Physics.md
VALIDATION:      ./VALIDATION_Physics.md
IMPLEMENTATION:  ./IMPLEMENTATION_Physics.md
THIS:            HEALTH_Physics.md
SYNC:            ./SYNC_Physics.md

IMPL:            engine/physics/tick.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: physics_tick
    purpose: Ensure the world metabolism is active and proportional.
    triggers:
      - type: schedule
        source: Orchestrator.run
        notes: Typically every 5+ game minutes.
    frequency:
      expected_rate: 1/min (real-time)
      peak_rate: 10/min (during speed 3x)
      burst_behavior: Ticks may be skipped if elapsed time is too small.
    risks:
      - Energy stagnation (no flips)
      - Energy explosion (infinite runaway)
      - Delayed consequences (broken cascades)
    notes: Core metabolism of the system.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: energy_momentum
    flow_id: physics_tick
    priority: high
    rationale: If energy doesn't flow, the world feels dead.
  - name: flip_consistency
    flow_id: physics_tick
    priority: high
    rationale: Flips are the primary source of drama; missed flips mean missed story.
  - name: decay_integrity
    flow_id: physics_tick
    priority: med
    rationale: Prevents energy accumulation that causes "everything happening at once".
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: stdout
  result:
    representation: tuple
    value: {status: OK, score: 0.95}
    updated_at: 2025-12-20T10:00:00Z
    source: GraphTick.run
```

---

## DOCK TYPES (COMPLETE LIST)

- `graph_ops` (graph operations or traversal)
- `api` (HTTP/RPC boundary)

---

## CHECKER INDEX

```yaml
checkers:
  - name: energy_balance_checker
    purpose: Verify energy conservation and expected decay (I7).
    status: active
    priority: high
  - name: flip_threshold_checker
    purpose: Ensure flips occur at deterministic thresholds (I8).
    status: active
    priority: high
```

---

## INDICATOR: energy_momentum

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: energy_momentum
  client_value: Ensures the world feels alive and responsive to player focus.
  validation:
    - validation_id: I7
      criteria: Energy in = energy out + decay losses.
    - validation_id: I2
      criteria: Graph never stops thinking.
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - float_0_1
  semantics:
    float_0_1: 1.0 = healthy flow, 0.0 = stagnant or exploded.
  aggregation:
    method: weighted_average
    display: CLI
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: tick_input
    method: engine.physics.tick.GraphTick.run
    location: engine/physics/tick.py:68
  output:
    id: flip_output
    method: engine.physics.tick.GraphTick.run
    location: engine/physics/tick.py:126
```

---

## TRACE SCENARIOS (VERIFICATION)

See original `TEST_Physics.md` for detailed walk-throughs of these scenarios.

### Trace 1: Simple Exchange
- **Input:** Player question (energy injection).
- **Expectation:** Target character's weight increases and flips.
- **Verification:** `TickResult.flips` contains the expected moment.

### Trace 2: Silence
- **Input:** Irrelevant player input.
- **Expectation:** Energy returns to player character.
- **Verification:** Player character observation moment flips after N ticks.

---

## HOW TO RUN

```bash
# Run physics tests (unit and integration)
pytest engine/tests/test_moment_graph.py -v
```

---

## KNOWN GAPS

- [ ] Automated check for "The Snap" transition display rules.
- [ ] Real-time monitoring of energy levels across large graph clusters.
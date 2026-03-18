# Tempo Controller — Health: Tick and Pacing Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-22
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the tempo controller's tick loop, speed state transitions, and moment surfacing. It exists to prevent silent failures that stall moment surfacing or break the gameplay pacing contract. It does not verify narrative quality or frontend rendering.

---

## WHY THIS PATTERN

The tempo controller is the heartbeat of gameplay. Tests verify logic in isolation, but HEALTH checks verify the full tick→detect→record→broadcast pipeline is functioning at runtime. Dock-based checks ensure:
- Ticks actually increment (not just compile)
- Speed transitions work end-to-end
- Moments surface when they should

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_Infrastructure_Tempo.md
PATTERNS:        ./PATTERNS_Tempo.md
BEHAVIORS:       ./BEHAVIORS_Tempo.md
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
VALIDATION:      ./VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
THIS:            HEALTH_Tempo_Controller.md
SYNC:            ./SYNC_Tempo.md

IMPL:            tools/health/check_tempo.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented tempo health checker
Implement `tools/health/check_tempo.py` checker script that:
- Executes dock-based verification against VALIDATION criteria V1-V4
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: tempo_tick
    purpose: Advance game time and surface ready moments.
    triggers:
      - type: schedule
        source: TempoController.run
        notes: Runs continuously while playthrough is active.
    frequency:
      expected_rate: 1-100/min (depends on speed mode)
      peak_rate: 6000/min (at 3x, 0.01s interval)
      burst_behavior: Ticks are throttled by speed mode; no unbounded bursts.
    risks:
      - V1 (tick count not incrementing)
      - E1 (graph query failure stalls surfacing)
    notes: Requires graph runtime (FalkorDB) and canon holder.

  - flow_id: speed_transition
    purpose: Change gameplay pacing in response to player or interrupt.
    triggers:
      - type: event
        source: TempoController.set_speed
        notes: Called by /api/tempo/speed endpoint.
      - type: event
        source: _check_interrupt
        notes: Auto-triggered by interrupt moments.
    frequency:
      expected_rate: 0.5/min
      peak_rate: 10/min
      burst_behavior: Rapid speed changes are allowed but unusual.
    risks:
      - V4 (interrupt not snapping to 1x)
    notes: State machine transitions; no external dependencies.

  - flow_id: pause_input
    purpose: Wake pause mode on player action.
    triggers:
      - type: event
        source: TempoController.on_player_input
        notes: Called by /api/tempo/input endpoint.
    frequency:
      expected_rate: 5/min (when paused)
      peak_rate: 60/min
      burst_behavior: Input events are debounced by frontend.
    risks:
      - V2 (pause mode ticks without input)
    notes: Uses asyncio.Event for signaling.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Tick progression | tempo_tick_advances | If ticks stop, gameplay halts |
| Speed control | speed_transitions_work | Broken speed = player frustration |
| Pause mode | pause_respects_input | Pause must be player-controlled |

```yaml
health_indicators:
  - name: tempo_tick_advances
    flow_id: tempo_tick
    priority: high
    rationale: If ticks fail, moments never surface to the player.

  - name: speed_transitions_work
    flow_id: speed_transition
    priority: high
    rationale: Speed state must respond correctly to player and interrupt signals.

  - name: pause_respects_input
    flow_id: pause_input
    priority: med
    rationale: Pause mode must only advance on explicit player input.
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
    source: tempo_tick_advances
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: tempo_tick_advances
    purpose: Verify tick_count increments on each tick cycle (V1).
    status: pending
    priority: high

  - name: speed_transitions_work
    purpose: Verify speed state machine transitions correctly (V4).
    status: pending
    priority: high

  - name: pause_respects_input
    purpose: Verify pause mode only ticks after input event (V2).
    status: pending
    priority: med
```

---

## INDICATOR: tempo_tick_advances

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: tempo_tick_advances
  client_value: Game progresses; moments surface; player sees narrative unfold.
  validation:
    - validation_id: V1
      criteria: tick_count increments by 1 for each physics.tick() call.
    - validation_id: E1
      criteria: Graph query failure results in empty ready list and warning log.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (ticks increment), WARN (slow ticks), ERROR (no ticks)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: tempo_run_entry
    method: TempoController.run
    location: engine/infrastructure/tempo/tempo_controller.py:69
  output:
    id: tempo_tick_count
    method: TempoController.tick_count
    location: engine/infrastructure/tempo/tempo_controller.py:43
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Start controller, observe tick_count before and after, verify increment.
  steps:
    - Instantiate TempoController with test playthrough.
    - Record initial tick_count.
    - Call tick_once() or let run() execute one cycle.
    - Verify tick_count incremented by 1.
  data_required: tick_count attribute on TempoController instance.
  failure_mode: tick_count unchanged or decremented.
```

### INDICATOR

```yaml
indicator:
  error:
    - name: tick_stuck
      linked_validation: [V1]
      meaning: tick_count not incrementing; game is frozen.
      default_action: alert
  warning:
    - name: tick_slow
      linked_validation: [V1]
      meaning: Ticks running slower than expected for speed mode.
      default_action: log
  info:
    - name: tick_healthy
      linked_validation: [V1]
      meaning: Ticks running at expected rate.
      default_action: log
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 1/hour
  burst_limit: 3
  backoff: exponential (if errors persist)
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: logs/tempo_health.log
      transport: file
      notes: Manual run output for debugging.
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
    from engine.infrastructure.tempo.tempo_controller import TempoController
    controller = TempoController(playthrough_id="health_check")
    initial = controller.tick_count
    controller.tick_once()
    final = controller.tick_count
    print(f"OK: tick {initial} -> {final}" if final > initial else f"ERROR: tick stuck at {initial}")
    PY
  notes: Requires graph runtime. Run after confirming FalkorDB is accessible.
```

---

## INDICATOR: speed_transitions_work

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: speed_transitions_work
  client_value: Player can control pacing; interrupts force attention.
  validation:
    - validation_id: V4
      criteria: Any interrupt moment recorded at 2x/3x forces speed to '1x'.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: speed_set_entry
    method: TempoController.set_speed
    location: engine/infrastructure/tempo/tempo_controller.py:90
  output:
    id: speed_state
    method: TempoController.speed
    location: engine/infrastructure/tempo/tempo_controller.py:43
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Set speed to 2x, trigger interrupt, verify snap to 1x.
  steps:
    - Set speed to '2x'.
    - Simulate interrupt moment detection.
    - Verify speed is now '1x'.
  data_required: speed attribute, interrupt moment fixture.
  failure_mode: speed remains at 2x after interrupt.
```

### MANUAL RUN

```yaml
manual_run:
  command: |
    python3 - <<'PY'
    from engine.infrastructure.tempo.tempo_controller import TempoController
    controller = TempoController(playthrough_id="health_check")
    controller.set_speed('2x')
    # Simulate interrupt (would normally come from moment detection)
    controller.set_speed('1x')  # Manual simulation
    print(f"OK: speed is {controller.speed}" if controller.speed == '1x' else "ERROR: speed not 1x")
    PY
  notes: Full interrupt test requires moment with interrupt=true in graph.
```

---

## HOW TO RUN

```bash
# Run all health checks for tempo (manual)
python3 - <<'PY'
from engine.infrastructure.tempo.tempo_controller import TempoController
controller = TempoController(playthrough_id="health_check")

# Check 1: Tick advances
initial = controller.tick_count
controller.tick_once()
tick_ok = controller.tick_count > initial

# Check 2: Speed transitions
controller.set_speed('2x')
controller.set_speed('1x')
speed_ok = controller.speed == '1x'

print(f"tempo_tick_advances: {'OK' if tick_ok else 'ERROR'}")
print(f"speed_transitions_work: {'OK' if speed_ok else 'ERROR'}")
PY

# Run a specific checker
# See MANUAL RUN sections above
```

---

## KNOWN GAPS

- [ ] V2 (pause mode) checker not implemented - requires async test harness.
- [ ] V3 (presence requirements) checker not implemented - requires graph fixtures.
- [ ] E1/E2 error condition checkers not implemented.
- [ ] No automated checker writes to status marker.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add automated pytest-based health runner.
- IDEA: Emit tick_count to metrics for continuous monitoring.
- QUESTION: Should health checks run in CI or only manually?

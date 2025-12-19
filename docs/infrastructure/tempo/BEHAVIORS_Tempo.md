# Tempo Controller — Behaviors: Speed-Driven Surfacing

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against local tree
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tempo.md
THIS:            BEHAVIORS_Tempo.md (you are here)
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
VALIDATION:      ./VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
TEST:            ./TEST_Tempo.md
SYNC:            ./SYNC_Tempo.md

IMPL:            engine/infrastructure/tempo/tempo_controller.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Pause Mode Waits For Input And Ticks Once

```
GIVEN:  speed == 'pause' and controller is running
WHEN:   player input arrives
THEN:   controller ticks exactly once and records at most one ready moment
AND:    controller returns to waiting state
```

### B2: Continuous Modes Tick On Interval And Record Ready Moments

```
GIVEN:  speed in {'1x', '2x', '3x'} and controller is running
WHEN:   tick interval elapses
THEN:   physics.tick() runs and ready moments are recorded to canon (max 3)
```

### B3: Interrupts Snap Fast Speeds Back To 1x

```
GIVEN:  speed in {'2x', '3x'}
WHEN:   a recorded moment is flagged interrupt == true
THEN:   speed changes to '1x' and a speed_changed event is broadcast
```

### B4: Player Input Interrupts 3x

```
GIVEN:  speed == '3x'
WHEN:   player input is received
THEN:   speed changes to '1x' with reason 'player_input'
```

### B5: Backpressure Slows 1x When Queue Is Large

```
GIVEN:  speed == '1x'
WHEN:   display_queue_size > BACKPRESSURE_LIMIT
THEN:   controller sleeps briefly before next tick
```

---

## INPUTS / OUTPUTS

### Primary Function: `TempoController.on_player_input()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Player input text to store as a moment |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| `status` | `str` | `"ok"` when queued |
| `moment_id` | `str` | Newly created moment id |

**Side Effects:**

- Creates a `Moment` node in the graph with status `possible`.
- Signals pause mode to tick once.
- Forces speed to 1x when input arrives at 3x.

---

## EDGE CASES

### E1: Invalid Queue Size Report

```
GIVEN:  queue size is non-integer or negative
THEN:   controller ignores or clamps the value to 0 and continues
```

### E2: Ready-Moment Query Failure

```
GIVEN:  graph query throws an exception
THEN:   controller logs a warning and proceeds with no ready moments
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Pause Mode Should Not Tick Without Input

```
GIVEN:   speed == 'pause' and no input received
WHEN:    time advances
MUST NOT: physics.tick() or canon.record_to_canon() run
INSTEAD:  controller waits on the input event
```

### A2: Presence Requirements Must Not Be Ignored

```
GIVEN:   a moment has presence_required attachments not at player location
WHEN:    ready moments are detected
MUST NOT: moment be recorded to canon
INSTEAD:  moment is filtered out of the ready list
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Clarify frontend display filtering at 2x/3x (not enforced server-side).
- QUESTION: Should pause mode surface more than one moment per input?

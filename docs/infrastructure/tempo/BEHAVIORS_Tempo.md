# Tempo Controller — Behaviors: Speed-Controlled Moment Surfacing

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against local worktree
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tempo.md
THIS:            BEHAVIORS_Tempo.md
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

### B1: Pause mode ticks once per input

```
GIVEN:  speed == 'pause'
WHEN:   player input arrives
THEN:   exactly one physics tick runs
AND:    at most one ready moment is recorded to canon
```

### B2: Continuous ticking respects the current interval

```
GIVEN:  speed in {'1x', '2x', '3x'}
WHEN:   run loop executes
THEN:   ticks occur no faster than the interval for the current speed
```

### B3: Interrupt moments snap back to 1x

```
GIVEN:  speed in {'2x', '3x'}
WHEN:   a ready moment has interrupt == true
THEN:   speed changes to '1x'
AND:    a speed_changed event is broadcast
```

### B4: Backpressure slows 1x when the queue is large

```
GIVEN:  speed == '1x'
WHEN:   display_queue_size > BACKPRESSURE_LIMIT
THEN:   the loop sleeps to let the frontend catch up
```

---

## INPUTS / OUTPUTS

### Primary Function: `on_player_input()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Player-entered text |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| `result` | `Dict[str, Any]` | `{status, moment_id}` for the created player moment |

**Side Effects:**

- Creates a player `Moment` node in the graph
- Signals pause-mode input event
- May change speed from 3x to 1x

---

## EDGE CASES

### E1: Invalid queue size updates

```
GIVEN:  queue_size is not an int or is negative
THEN:   size is ignored or clamped to 0 without crashing
```

### E2: Graph query failures

```
GIVEN:  graph queries raise exceptions
THEN:   the controller logs a warning and continues without surfacing moments
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Ticking without input in pause mode

```
GIVEN:   speed == 'pause'
WHEN:    no input has arrived
MUST NOT: run physics ticks
INSTEAD: wait on the input event
```

### A2: Speed changes without notification

```
GIVEN:   speed is changed
WHEN:    set_speed is called
MUST NOT: skip SSE broadcast
INSTEAD: emit speed_changed with reason
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define expected behavior when pause-mode input arrives while running is false
- [ ] Clarify whether interrupt detection expands beyond `moment.interrupt`
- IDEA: Emit a tempo shutdown event for the frontend UI
- QUESTION: Should 2x/3x still record non-displayed moments to canon?

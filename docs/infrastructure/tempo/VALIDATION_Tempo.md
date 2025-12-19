# Tempo Controller — Validation: Pacing Invariants and Safety Checks

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against local worktree
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tempo.md
BEHAVIORS:       ./BEHAVIORS_Tempo.md
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
THIS:            VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
TEST:            ./TEST_Tempo.md
SYNC:            ./SYNC_Tempo.md

IMPL:            engine/infrastructure/tempo/tempo_controller.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

These must ALWAYS be true:

### V1: Speed is one of the allowed values

```
TempoController.speed in {'pause', '1x', '2x', '3x'}
```

**Checked by:** manual inspection; future unit test should assert speed transitions.

### V2: Pause mode never ticks without input

```
If speed == 'pause' and no input event occurs, then no physics tick runs.
```

**Checked by:** manual reasoning; add unit test with mocked Event.

### V3: Display queue size is non-negative

```
TempoController.display_queue_size >= 0
```

**Checked by:** `update_display_queue_size` normalization.

---

## PROPERTIES

For property-based testing:

### P1: Tick count only increments on physics ticks

```
FORALL tick cycles:
    tick_count increments exactly once per physics.tick() call
```

**Tested by:** NOT YET TESTED — requires mocking GraphTick.

### P2: Interrupt flips speed to 1x

```
FORALL moments with interrupt == true at 2x/3x:
    speed becomes '1x' after processing
```

**Tested by:** NOT YET TESTED — requires deterministic loop control.

---

## ERROR CONDITIONS

### E1: Graph query failure during surfacing

```
WHEN:    GraphQueries raises an exception
THEN:    ready moment detection returns [] and logs a warning
SYMPTOM: no moment surfacing for that tick
```

**Tested by:** NOT YET TESTED — needs mocked queries.

### E2: Invalid queue size input

```
WHEN:    queue_size is non-numeric
THEN:    value is ignored and controller continues
SYMPTOM: warning log, no crash
```

**Tested by:** NOT YET TESTED — needs unit test.

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: speed values | — | ⚠ NOT YET TESTED |
| V2: pause tick gating | — | ⚠ NOT YET TESTED |
| V3: non-negative queue size | — | ⚠ NOT YET TESTED |
| P1: tick_count increment | — | ⚠ NOT YET TESTED |
| P2: interrupt snap | — | ⚠ NOT YET TESTED |
| E1: query failure | — | ⚠ NOT YET TESTED |
| E2: invalid queue size | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — inspect speed transitions in `set_speed`
[ ] V2 holds — pause waits on input event
[ ] V3 holds — queue size clamped in `update_display_queue_size`
[ ] All behaviors from BEHAVIORS_Tempo.md are met
[ ] All edge cases handled without crashing
```

### Automated

```bash
# No dedicated tempo tests exist yet
pytest engine/tests/test_*.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: engine/infrastructure/tempo/tempo_controller.py @ local worktree
    test: none
VERIFIED_BY: manual inspection
RESULT:
    V1: PASS (manual)
    V2: PASS (manual)
    V3: PASS (manual)
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add unit tests with mocked GraphTick/GraphQueries/CanonHolder
- [ ] Add integration test that runs tempo loop with a fake backend
- IDEA: Property tests for speed transition sequences
- QUESTION: Should backpressure apply at 2x as well?

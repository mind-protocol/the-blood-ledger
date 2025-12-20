# Tempo Controller — Validation: Pacing Invariants

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against local tree
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tempo.md
BEHAVIORS:       ./BEHAVIORS_Tempo.md
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
THIS:            VALIDATION_Tempo.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
TEST:            ./TEST_Tempo.md
SYNC:            ./SYNC_Tempo.md

IMPL:            engine/infrastructure/tempo/tempo_controller.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

These must ALWAYS be true:

### V1: Tick Count Is Monotonic

```
tick_count increments by 1 for each physics.tick() call.
```

**Checked by:** Manual inspection during debug logging (no automated test yet).

### V2: Pause Mode Ticks Only On Input

```
If speed == 'pause', ticks occur only after input event is set.
```

**Checked by:** Manual run with pause speed and observing tick logs.

### V3: Presence Requirements Are Respected

```
Moments with presence_required attachments are surfaced only when all required
characters are at the player location.
```

**Checked by:** Manual graph inspection via queries (no automated test yet).

### V4: Interrupts Snap To 1x

```
Any interrupt moment recorded at 2x/3x forces speed to '1x'.
```

**Checked by:** Manual run with interrupt moment flag.

---

## PROPERTIES

For property-based testing:

### P1: Backpressure Never Makes Queue Negative

```
FORALL queue_size:
    update_display_queue_size(queue_size) >= 0
```

**Tested by:** NOT YET TESTED — no property tests exist.

---

## ERROR CONDITIONS

### E1: Graph Query Failure

```
WHEN:    GraphQueries.query throws (ngram repo runtime)
THEN:    ready list is empty and a warning is logged
SYMPTOM: ticks continue without surfacing new moments
```

**Tested by:** NOT YET TESTED — no error tests exist.

### E2: Invalid Queue Size Report

```
WHEN:    frontend reports a non-integer or negative queue size
THEN:    value is ignored or clamped, no exception thrown
SYMPTOM: log warning, backpressure remains stable
```

**Tested by:** NOT YET TESTED — no error tests exist.

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Tick count monotonic | — | ⚠ NOT YET TESTED |
| V2: Pause mode gating | — | ⚠ NOT YET TESTED |
| V3: Presence requirements | — | ⚠ NOT YET TESTED |
| V4: Interrupt snap | — | ⚠ NOT YET TESTED |
| P1: Backpressure clamp | — | ⚠ NOT YET TESTED |
| E1: Graph query failure | — | ⚠ NOT YET TESTED |
| E2: Invalid queue size | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — watch tick_count increment with logs
[ ] V2 holds — pause mode ticks only on input
[ ] V3 holds — presence-required moments stay hidden when characters are absent
[ ] V4 holds — interrupt moment sets speed to 1x
[ ] All behaviors from BEHAVIORS_Tempo.md work
[ ] All edge cases handled
[ ] All anti-behaviors prevented
```

### Automated

```bash
# No automated tests yet for tempo.
# Planned: pytest engine/tests/test_tempo.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: engine/infrastructure/tempo/tempo_controller.py @ local tree
    test: engine/tests/test_tempo.py @ not yet created
VERIFIED_BY: manual inspection
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
    V4: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add unit tests for speed transitions, pause mode, and queue size handling.
- [ ] Add integration tests for API endpoints + SSE speed_changed events.

# Tempo Controller — Test: Tempo Loop Coverage

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tempo.md
BEHAVIORS:       ./BEHAVIORS_Tempo.md
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
VALIDATION:      ./VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
THIS:            TEST_Tempo.md
SYNC:            ./SYNC_Tempo.md

IMPL:            engine/tests/test_tempo.py (not yet created)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

Tempo logic is time-based and depends on GraphTick/GraphQueries/CanonHolder.
Unit tests should mock those dependencies and run the loop with controlled
clock advancement. Integration tests should exercise the API endpoints and
validate SSE broadcasts.

---

## UNIT TESTS

### TempoController core

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_pause_ticks_once` | input event in pause | one tick, one record | pending |
| `test_speed_change_broadcasts` | set_speed calls | speed_changed emitted | pending |
| `test_backpressure_sleep` | queue_size > limit at 1x | sleep invoked | pending |
| `test_interrupt_snaps_to_1x` | interrupt moment at 2x | speed == 1x | pending |
| `test_queue_size_normalization` | invalid values | clamp/ignore | pending |

---

## INTEGRATION TESTS

### Tempo API flow

```
GIVEN:  a playthrough id
WHEN:   /api/tempo/start then /api/tempo/speed then /api/tempo/stop
THEN:   controller exists, speed updates, and stop cancels the task
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| graph query failure | mock queries to raise | pending |
| controller stop while paused | stop during wait | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `TempoController` | 0% | No tests yet |
| Tempo API router | 0% | Needs integration coverage |

---

## HOW TO RUN

```bash
# No dedicated tempo tests yet
pytest engine/tests/test_*.py
```

---

## KNOWN TEST GAPS

- [ ] No unit tests for tempo loop, speed transitions, or backpressure
- [ ] No integration tests for tempo API endpoints
- [ ] No SSE broadcast verification

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| None | - | - | - |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide where to host tempo unit tests (engine/tests vs infra/tempo)
- IDEA: Use a fake clock to test tick intervals deterministically
- QUESTION: Should tempo tests run without a live graph backend?

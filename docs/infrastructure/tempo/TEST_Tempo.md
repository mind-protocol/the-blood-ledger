# Tempo Controller — Test: Coverage Plan

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

IMPL:            engine/tests/test_tempo.py (planned)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

Tempo needs unit tests around the controller state machine and API endpoints,
plus a minimal integration test to confirm ticks surface moments through canon.
No automated tests exist yet.

---

## UNIT TESTS

### Controller State Machine

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_pause_ticks_once` | pause + input | one tick, one moment max | pending |
| `test_speed_change_broadcasts` | set_speed('2x') | speed_changed event emitted | pending |
| `test_interrupt_snaps_to_1x` | interrupt moment at 2x | speed == '1x' | pending |
| `test_queue_size_clamps` | invalid queue size | queue >= 0, no crash | pending |

---

## INTEGRATION TESTS

### Tempo API + Controller Lifecycle

```
GIVEN:  a new playthrough id
WHEN:   POST /api/tempo/start/{id} then POST /api/tempo/stop/{id}
THEN:   controller is created, run task starts, and then stops cleanly
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Graph query failure | mock GraphQueries.query to raise | pending |
| Player input at 3x | set_speed('3x') then input | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| TempoController | 0% | No automated tests yet |
| Tempo API | 0% | No automated tests yet |

---

## HOW TO RUN

```bash
# No automated tests yet for tempo.
# Planned:
pytest engine/tests/test_tempo.py
```

---

## KNOWN TEST GAPS

- [ ] No unit tests for speed transitions.
- [ ] No integration tests for API endpoints.
- [ ] No SSE broadcast verification.

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| — | — | — | — |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide if tempo tests should stub FalkorDB or use a lightweight test graph.

# Engine Tests — Health: Test Suite Coverage

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-22
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the engine test suite execution. It exists to:
- Catch regressions that break core engine invariants
- Verify test isolation (unit tests don't require external services)
- Ensure integration tests handle missing dependencies gracefully

It does not verify frontend behavior.

---

## WHY THIS PATTERN

Test suites are the first line of defense against regressions. Tests verify logic, but HEALTH checks verify the test infrastructure itself is working. Dock-based checks ensure:
- Tests actually run (not silently skipped)
- Test isolation is maintained
- Coverage stays above threshold

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_Engine_Tests.md
PATTERNS:        ./PATTERNS_Spec_Linked_Test_Suite.md
BEHAVIORS:       ./BEHAVIORS_Test_Coverage_Layers.md
ALGORITHM:       ./ALGORITHM_Test_Run_Flow.md
VALIDATION:      ./VALIDATION_Test_Suite_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Test_File_Layout.md
THIS:            HEALTH_Engine_Test_Suite.md
SYNC:            ./SYNC_Engine_Test_Suite.md

IMPL:            tools/health/check_engine_tests.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented engine tests health checker
Implement `tools/health/check_engine_tests.py` checker script that:
- Executes dock-based verification against VALIDATION criteria INV1-INV4
- Updates `status.result.value` in this file
- Runs throttled (max 10/day in CI)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: test_run
    purpose: Execute test suite and report pass/fail.
    triggers:
      - type: manual
        source: pytest engine/tests
        notes: Run by developers and CI.
    frequency:
      expected_rate: 1-10/day
      peak_rate: 50/day (active development)
      burst_behavior: CI runs on every push.
    risks:
      - INV1 (tests require external services)
      - INV2 (integration tests don't skip gracefully)
    notes: Should complete in < 60 seconds for unit tests.

  - flow_id: integration_test_run
    purpose: Execute integration tests with database.
    triggers:
      - type: manual
        source: pytest engine/tests -m integration
        notes: Run when database is available.
    frequency:
      expected_rate: 0.5-5/day
      peak_rate: 20/day
      burst_behavior: May be skipped if DB unavailable.
    risks:
      - Database connection failures
      - Test data corruption
    notes: Should skip gracefully when DB missing.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Tests pass | engine_tests_pass | Failing tests = broken invariants |
| Tests isolated | unit_tests_isolated | External deps = flaky tests |
| Suite runs | test_suite_executes | Silently skipped = false confidence |

```yaml
health_indicators:
  - name: engine_tests_pass
    flow_id: test_run
    priority: high
    rationale: Core engine invariants rely on passing tests.

  - name: unit_tests_isolated
    flow_id: test_run
    priority: med
    rationale: Unit tests must not require external services (INV1).

  - name: test_suite_executes
    flow_id: test_run
    priority: high
    rationale: Tests must actually run, not be silently skipped.
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
    source: engine_tests_pass
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: engine_tests_pass
    purpose: Verify all tests pass.
    status: active
    priority: high

  - name: unit_tests_isolated
    purpose: Verify unit tests run without external services (INV1).
    status: pending
    priority: med

  - name: integration_tests_skip
    purpose: Verify integration tests skip gracefully when DB missing (INV2).
    status: pending
    priority: med
```

---

## INDICATOR: engine_tests_pass

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: engine_tests_pass
  client_value: Core engine logic works correctly; no regressions.
  validation:
    - validation_id: INV4
      criteria: Suite can be executed from repo root via pytest engine/tests.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (all pass), WARN (some skip), ERROR (failures)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: pytest_invoke
    method: pytest
    location: engine/tests/__init__.py
  output:
    id: pytest_result
    method: pytest exit code
    location: stdout
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Run pytest, check exit code and output.
  steps:
    - Run pytest engine/tests -v
    - Check exit code (0 = pass, non-zero = fail)
    - Parse output for failures/skips
  data_required: pytest, test files
  failure_mode: Non-zero exit code or test failures.
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 10/day
  burst_limit: none
  backoff: none
```

### MANUAL RUN

```yaml
manual_run:
  command: pytest engine/tests -v
  notes: Run from repo root.
```

---

## HOW TO RUN

```bash
# Run all engine tests
pytest engine/tests -v

# Run unit tests only (no external services)
pytest engine/tests -v -m "not integration"

# Run integration tests only
pytest engine/tests -v -m integration

# Run with coverage
pytest engine/tests --cov=engine
```

---

## KNOWN GAPS

- [ ] INV1 (isolation) automated verification not implemented.
- [ ] INV2 (graceful skip) automated verification not implemented.
- [ ] INV3 (docstring coverage) automated verification not implemented.
- [ ] Test coverage is incomplete; failing tests may not cover all invariants.
- [ ] No CI integration for automated health checks.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add coverage threshold enforcement.
- IDEA: Add pytest plugin for isolation verification.
- QUESTION: Should health checks run in CI or only locally?

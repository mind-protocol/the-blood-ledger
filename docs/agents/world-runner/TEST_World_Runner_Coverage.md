# World Runner — Test: Coverage and Gaps

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
THIS:            TEST_World_Runner_Coverage.md
SYNC:            ./SYNC_World_Runner.md

IMPL:            tests/agents/world_runner/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

No automated tests are present for the World Runner service. The current strategy is manual inspection of CLI behavior and fallback output.

---

## UNIT TESTS

### WorldRunnerService

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_process_flips_success` | valid CLI JSON | parsed output dict | pending |
| `test_process_flips_nonzero_exit` | CLI non-zero exit | fallback response | pending |
| `test_process_flips_timeout` | timeout | fallback response | pending |
| `test_process_flips_parse_error` | invalid JSON | fallback response | pending |

---

## INTEGRATION TESTS

### Agent CLI Round-Trip

```
GIVEN:  a known flip payload and deterministic CLI stub
WHEN:   WorldRunnerService.process_flips runs
THEN:   output matches WorldRunnerOutput schema
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| CLI outputs fenced code block | `test_process_flips_fenced_json` | pending |
| Empty flips list | `test_process_flips_empty` | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `WorldRunnerService` | 0% | No automated tests present |

---

## HOW TO RUN

```bash
# No test suite currently exists for this module.
# Proposed location:
# pytest tests/agents/world_runner/
```

---

## KNOWN TEST GAPS

- [ ] No unit tests for fallback paths.
- [ ] No schema validation tests against TOOL_REFERENCE.
- [ ] No integration tests for CLI response parsing.

---

## GAPS / IDEAS / QUESTIONS

- IDEA: Add a JSON schema validation step using TOOL_REFERENCE before returning output.

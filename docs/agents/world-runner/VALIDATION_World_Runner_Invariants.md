# World Runner — Validation: Service Invariants and Failure Behavior

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against working tree (manual review only)
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
THIS:            VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
SYNC:            ./SYNC_World_Runner.md

IMPL:            engine/infrastructure/orchestration/world_runner.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: Output Schema Is Always Returned

```
WorldRunnerService.process_flips() returns a dict containing:
  - thinking: string
  - graph_mutations: dict
  - world_injection: dict
```

**Checked by:** Manual review of `_call_claude()` and `_fallback_response()` in `engine/infrastructure/orchestration/world_runner.py`.

### V2: Runner Calls Are Stateless

```
Agent CLI is invoked without --continue, and calls do not depend on
prior state outside the graph/context passed in the prompt.
```

**Checked by:** Manual review of `_call_claude()` CLI arguments.

### V3: Failures Degrade Safely

```
On non-zero exit, timeout, JSON parse error, or missing CLI,
the service returns a safe fallback response with empty mutations.
```

**Checked by:** Manual review of `_call_claude()` error handlers.

---

## PROPERTIES

### P1: Error Paths Always Return Valid Output

```
FORALL error in {timeout, parse_error, cli_missing, nonzero_exit}:
    process_flips(...) returns V1-compliant output
```

**Tested by:** NOT YET TESTED — no automated tests present.

---

## ERROR CONDITIONS

### E1: Agent CLI Returns Non-Zero

```
WHEN:    subprocess.run() returns returncode != 0
THEN:    fallback response is returned
SYMPTOM: logged error "[WorldRunnerService] Agent CLI failed"
```

**Tested by:** NOT YET TESTED — manual review only.

### E2: Invalid JSON Response

```
WHEN:    response_text cannot be parsed as JSON
THEN:    fallback response is returned
SYMPTOM: logged error "[WorldRunnerService] Failed to parse response"
```

**Tested by:** NOT YET TESTED — manual review only.

### E3: CLI Timeout or Missing Binary

```
WHEN:    subprocess.TimeoutExpired OR FileNotFoundError
THEN:    fallback response is returned
SYMPTOM: logged timeout or "Agent CLI not found"
```

**Tested by:** NOT YET TESTED — manual review only.

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Output schema | — | ⚠ NOT YET TESTED |
| V2: Stateless calls | — | ⚠ NOT YET TESTED |
| V3: Safe fallback | — | ⚠ NOT YET TESTED |
| P1: Error path output | — | ⚠ NOT YET TESTED |
| E1: Non-zero exit | — | ⚠ NOT YET TESTED |
| E2: Invalid JSON | — | ⚠ NOT YET TESTED |
| E3: Timeout/CLI missing | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — inspect _call_claude() and _fallback_response()
[ ] V2 holds — verify no --continue in CLI invocation
[ ] V3 holds — inspect exception handlers and fallback path
[ ] Error logging present for E1/E2/E3
```

### Automated

```bash
# No automated tests for World Runner service yet.
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: engine/infrastructure/orchestration/world_runner.py (working tree)
    test: none
VERIFIED_BY: manual review
RESULT:
    V1: PASS (manual)
    V2: PASS (manual)
    V3: PASS (manual)
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add unit tests for error handling and schema compliance.
- [ ] Add a contract test that validates WorldRunnerOutput against TOOL_REFERENCE schema.

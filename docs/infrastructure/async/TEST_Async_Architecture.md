# Async Architecture — Tests

```
CREATED: 2024-12-17
STATUS: TODO
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Async_Architecture.md
BEHAVIORS:   ./BEHAVIORS_Travel_Experience.md
ALGORITHM:   ./ALGORITHM_Async_Architecture.md
VALIDATION:  ./VALIDATION_Async_Architecture.md
IMPLEMENTATION: ./IMPLEMENTATION_Async_Architecture.md
THIS:        TEST_Async_Architecture.md (you are here)
SYNC:        ./SYNC_Async_Architecture.md
```

---

## Planned Coverage

| Test | Target | Description |
|------|--------|-------------|
| `tests/async/test_runner_protocol.py` | Runner protocol | Simulate travel->arrival->fetch loops and verify waypoint creation payloads. |
| `tests/async/test_sse_queue.py` | Graph SSE | Ensure queue overflow fallback works and SSE events remain ordered. |
| `tests/async/test_hook_injection.py` | Hook injection | Validate plugin hooks register/execute and ignore non-interrupt events. |

---

## Test Strategy

Focus on contract-level coverage for async handoffs: runner outputs, SSE fanout,
and hook-based interruptions. Favor thin mocks around graph writes while
asserting queue file formats and TaskOutput payload structure to keep tests
stable as implementations evolve.

---

## Unit Tests

Unit tests should isolate queue parsing, runner result shaping, and hook
serialization. Prioritize deterministic inputs for JSONL and JSON queue readers,
plus validation of TaskOutput payload fields to avoid brittle end-to-end runs.

---

## Integration Tests

Integration tests should start the API layer, emit a travel request, and verify
SSE events plus hook injection handling across processes. Include a minimal
runner stub that writes to the graph and exits to exercise TaskOutput flow.

---

## Edge Cases

Cover malformed injection queue entries, duplicate hook payloads, and runner
completion arriving before narration finishes. Ensure SSE reconnection does not
drop queued events, and that stop-button injections short-circuit travel safely.

---

## Test Coverage

The planned tests focus on runner protocol, SSE queue behavior, and hook
injection. Coverage should explicitly include JSONL queue parsing, TaskOutput
payload validation, and SSE reconnection handling once those components exist.

---

## How To Run

Execute `pytest tests/async -k async` for unit coverage, then run the full async
suite with any required environment variables configured for API and graph
access. Manual runs should include the narrator and runner logs for timing.

--- 

## Manual Verification

- Launch narrator and runner concurrently; inspect logs for stuck tasks, hook
  interrupts, and duplicate TaskOutput reads during travel completion.
- Fire mock webhooks (see `ALGORITHM_Async_Architecture.md`) and confirm GraphOps (ngram repo graph runtime)
  mutations apply once and emit an SSE event without queue stalls.

---

## Known Test Gaps

No automated coverage currently exists for SSE reconnection, live map updates,
or image generation events. Multi-agent timing and background runner failures
are not yet exercised outside manual testing.

---

## Flaky Tests

None tracked yet. When concurrency timing tests are added, document any timing-
sensitive failures here with repro notes and stabilization ideas.

---

## Gaps

- Need integration harness for multi-agent tests that coordinates narrator,
  runner, and SSE so timing-dependent flows can be exercised deterministically.
- SSE stream is currently only manually monitored; no automated assertions
  confirm event ordering or reconnect behavior.

---

## Gaps / Ideas / Questions

- Should the async suite run against a local graph fixture or a mocked adapter?
- Do we need a dedicated harness for TaskOutput timing to reproduce hook races?
- What is the desired policy for duplicate injection queue entries?
```

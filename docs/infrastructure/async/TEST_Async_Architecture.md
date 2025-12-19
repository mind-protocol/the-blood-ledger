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
| `tests/async/test_runner_protocol.py` | Runner protocol | Simulate travel->arrival->fetch loops |
| `tests/async/test_sse_queue.py` | Graph SSE | Ensure queue overflow fallback works |
| `tests/async/test_hook_injection.py` | Hook injection | Validate plugin hooks register/execute |

---

## Manual Verification

- Launch narrator + runner concurrently; inspect logs for stuck tasks.
- Fire mock webhooks (see `ALGORITHM_Async_Architecture.md`) and confirm GraphOps mutations apply once.

---

## Gaps

- Need integration harness for multi-agent tests.
- SSE stream currently only manually monitored.
```

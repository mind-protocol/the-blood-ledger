# Engine — Test Coverage

```
STATUS: DRAFT
CREATED: 2024-12-17
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Engine.md
BEHAVIORS:   ./BEHAVIORS_Engine.md
ALGORITHM:   ./ALGORITHM_Engine.md
THIS:        TEST_Engine.md (you are here)
SYNC:        ./SYNC_Engine.md
```

---

## Existing Suites

| Path | Purpose |
|------|---------|
| `engine/tests/test_history.py` | Validates history timestamp + conversation parsing |
| `engine/tests/test_moment.py` | Placeholder moment tests (model + CLI) |
| `engine/tests/test_moment_standalone.py` | Sandboxed moment CLI check |
| `engine/tests/test_moment.py::TestMomentModel` | Ensures Pydantic model behavior |

---

## Gaps

1. No automated tests for FastAPI endpoints (needs TestClient fixtures).
2. GraphOps/GraphQueries rely on FalkorDB; we need integration harness or mocks.
3. SSE/debug stream behavior untested.

---

## Plan

- Add `tests/api/test_health.py` using FastAPI TestClient referencing docs/engine/moments/BEHAVIORS.
- Stand up FalkorDB docker fixture for GraphOps smoke tests.
- Instrument mutation listener broadcasts with unit tests.
```

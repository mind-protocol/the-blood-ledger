# Async Architecture — Validation

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Async_Architecture.md
BEHAVIORS:   ./BEHAVIORS_Travel_Experience.md
ALGORITHM:   ./ALGORITHM_Async_Architecture.md
IMPLEMENTATION: ./IMPLEMENTATION_Async_Architecture.md
THIS:        VALIDATION_Async_Architecture.md (you are here)
TEST:        ./TEST_Async_Architecture.md
SYNC:        ./SYNC_Async_Architecture.md
```

---

## INVARIANTS

1. **Single Source of Truth** — Graph mutations flow through GraphOps in the ngram runtime so async hooks never bypass canonical writes.
2. **Bounded Queues** — Injection and stream queues enforce size limits and drop oldest entries with explicit warnings in logs.
3. **Idempotent Actions** — Hook handlers can re-run safely without creating duplicate nodes or duplicate links.
4. **Latency Budget** — Hook invocations respond within a short window so UI-critical events are not delayed.

---

## PROPERTIES

- **Deterministic output**: identical queue payloads yield identical downstream narrator inputs.
- **Ordered delivery**: FIFO ordering holds for JSONL queue consumption in the hook reader.
- **Durable recovery**: queue files survive restart so missed injections are replayed.

---

## ERROR CONDITIONS

- Queue file missing or unreadable while hook executes.
- Malformed JSONL entry breaks parsing or produces empty payload.
- Narrator process unavailable when manual injection is triggered.
- Queue grows without consumers and exceeds size thresholds.

---

## HEALTH COVERAGE

- `docs/infrastructure/async/HEALTH_Async_Architecture.md` tracks hook responsiveness, queue depth, and replay safety signals.

---

## VERIFICATION PROCEDURE

- Run targeted hook tests (planned) to mock queue payloads and verify FIFO consumption.
- Manually append entries to playthrough queues and confirm narrator receives them in order.
- Monitor hook logs for timing and parse failures during a 15-minute soak run.

---

## SYNC STATUS

See `docs/infrastructure/async/SYNC_Async_Architecture.md` for current status, open work, and recent changes.

---

## GAPS / IDEAS / QUESTIONS

- Gap: formal pytest coverage for hook injection remains unimplemented.
- Idea: add a queue length health check for alerting on stalled readers.
- Question: should queue readers migrate to per-playthrough paths instead of default?

- `pytest tests/test_runner_async.py` (planned) to mock hook triggers.
- Manual soak: run narrator + runner concurrently for 30 minutes, monitor SSE logs for dropped events.
- Logging check: Ensure every async worker logs start/end + errors.
```

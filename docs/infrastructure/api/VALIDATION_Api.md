# API — Validation

## Invariants

- `GET /health` returns ISO-8601 UTC timestamps.
- `GET /health` returns `status=ok` only when both read and write graph connections succeed.
- Debug SSE events are valid JSON strings.
- Debug SSE clients are removed on disconnect or cancellation.

## Failure Modes

- Graph read failure returns `503` with `graph_read=error` details.
- Graph write failure returns `503` with `graph_write=error` details.
- Debug stream continues sending `ping` events when idle.

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

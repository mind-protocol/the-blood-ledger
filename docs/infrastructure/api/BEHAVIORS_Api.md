# API — Behaviors

## Health Check

- `GET /health` returns `status=ok` with timestamp and connection details when the graph is reachable.
- If graph connectivity fails, the endpoint responds with `503` and a `status=degraded` payload describing the failure.

## Debug Mutation Stream

- `GET /api/debug/stream` opens a server-sent events stream for mutation events.
- The stream sends:
  - `connected` event on connect
  - `mutation` events with JSON payloads
  - `ping` keepalives when idle

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

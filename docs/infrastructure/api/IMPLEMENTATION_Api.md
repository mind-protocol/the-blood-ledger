# API — Implementation

## Graph Access Helpers

- `create_app()` defines cached helpers for `GraphQueries` and `GraphOps`.
- Instances are lazily constructed and reused for the lifetime of the app process.

## Health Check

- `GET /health` runs a lightweight read query (`RETURN 1 AS ok`) to verify read access.
- A write connection is validated by constructing `GraphOps`.
- Failures return a `503` with details and error messages.

## Debug Mutation Stream

- `GET /api/debug/stream` registers a per-client `asyncio.Queue`.
- Mutation events are broadcast to all queues via `add_mutation_listener`.
- Events are serialized with `json.dumps(..., default=str)` to avoid serialization failures.

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

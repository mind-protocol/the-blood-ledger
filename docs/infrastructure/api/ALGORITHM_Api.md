# API — Algorithm

## Graph Helpers

1. On first access, construct `GraphQueries` or `GraphOps` with `graph_name`, `host`, and `port`.
2. Cache the instance for reuse in subsequent requests.

## Health Check

1. Capture the current UTC timestamp.
2. Run `RETURN 1 AS ok` through `GraphQueries` to validate read access.
3. Instantiate `GraphOps` to validate write access.
4. If any step fails, return `503` with a `degraded` status and error details.
5. If all steps succeed, return `status=ok` with connection details.

## Debug Mutation Stream

1. Create an `asyncio.Queue` per connected client.
2. Register the queue in `_debug_sse_clients`.
3. Yield a `connected` event, then enter a loop:
   - Wait up to 30 seconds for queued events.
   - If an event arrives, emit it as an SSE event with a JSON payload.
   - If idle, emit a `ping` keepalive event.
4. On disconnect or cancellation, remove the queue from `_debug_sse_clients`.

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

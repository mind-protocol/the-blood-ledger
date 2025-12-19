# API — Test

## TEST STRATEGY

Use a thin manual-first strategy: validate HTTP contracts with curl, confirm
SSE streams deliver expected events, and sanity-check playthrough flows against
documented behavior before adding automation.

## UNIT TESTS

No dedicated API unit test suite is documented yet; focus should be on router
helpers (payload shaping, error mapping, queue behavior) once a test harness
exists to isolate FastAPI dependencies.

## INTEGRATION TESTS

Run the API server locally and exercise the health, playthrough, moment, and
debug endpoints against a real graph connection; verify response shapes and SSE
event ordering using manual curl sessions.

## EDGE CASES

- Missing or invalid playthrough IDs should return a stable 404 or 422 payload.
- Graph connectivity failures should downgrade health to `503` without crashing.
- SSE clients that disconnect abruptly should release their queue without leaks.

## TEST COVERAGE

Coverage is currently manual and endpoint-focused, with health and debug streams
verified via curl; automated coverage for action routing and payload schemas is
not yet established.

## HOW TO RUN

Start the API (per `engine/infrastructure/api/app.py`), then use curl against
`/health`, `/api/playthrough/*`, `/api/moment/*`, and `/api/debug/stream` while
FalkorDB is running to confirm the full integration path.

## KNOWN TEST GAPS

There is no automated regression suite for the API endpoints, no fixtures for
graph-backed playthrough creation, and no load coverage for SSE backpressure or
multi-client fan-out.

## FLAKY TESTS

No formal flaky tests are tracked yet, but SSE timing and debug stream pings can
appear inconsistent if the server is under load or clients reconnect rapidly.

## GAPS / IDEAS / QUESTIONS

- [ ] Add pytest coverage for playthrough creation and action routing payloads.
- [ ] Add a stub graph or recorded cassette to exercise endpoints offline.
- Question: Should SSE queues expose metrics to validate fan-out behavior?

## Health Check

- Run `curl http://localhost:8000/health` and confirm `status=ok` with `details`.
- Stop FalkorDB, re-run the request, and confirm a `503` with `status=degraded`.

## Debug Mutation Stream

- Connect: `curl -N http://localhost:8000/api/debug/stream`
- Confirm an initial `connected` event and periodic `ping` events.
- Apply a mutation and verify a mutation event is delivered.

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

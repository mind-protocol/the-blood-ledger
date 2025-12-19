# API — Test

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

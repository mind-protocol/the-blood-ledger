# API — Patterns

## App Factory First

- Use a single `create_app()` factory to wire routes, shared state, and dependency helpers.
- Keep shared resources (graph clients, orchestrators) inside the factory closure.

## Lightweight Health Checks

- Health checks should validate connectivity without expensive graph scans.
- Prefer simple queries and connection instantiation.

## SSE Debug Streams

- Debug streaming is isolated from gameplay SSE to avoid accidental coupling.
- Each client receives a dedicated queue to prevent slow consumers from blocking others.

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

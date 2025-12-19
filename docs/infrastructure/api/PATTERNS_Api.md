# API — Patterns

## THE PROBLEM

The API needs a consistent entrypoint for gameplay actions, streaming, and health
checks without leaking infrastructure concerns across endpoints. Without shared
patterns, initialization becomes fragile, dependencies sprawl, and behavior
drifts between routers.

## THE PATTERN

Centralize the FastAPI setup in a single app factory that wires shared
dependencies, exposes focused endpoints, and keeps debug streaming isolated from
gameplay events. Keep the API thin, delegating heavy work to orchestration and
graph layers.

## PRINCIPLES

### App Factory First

- Use a single `create_app()` factory to wire routes, shared state, and
  dependency helpers.
- Keep shared resources (graph clients, orchestrators) inside the factory
  closure.

### Lightweight Health Checks

- Health checks should validate connectivity without expensive graph scans.
- Prefer simple queries and connection instantiation.

### SSE Debug Streams

- Debug streaming is isolated from gameplay SSE to avoid accidental coupling.
- Each client receives a dedicated queue to prevent slow consumers from blocking
  others.

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| engine/physics/graph | GraphOps/GraphQueries power mutations and health checks. |
| engine/infrastructure/orchestration | Orchestrator processes actions and drives the loop. |
| engine/infrastructure/embeddings | Optional embeddings used during playthrough creation. |
| scenarios/ | Scenario YAML and opening templates drive playthrough creation. |
| FastAPI | HTTP server and routing framework for the API surface. |

## INSPIRATIONS

App-factory FastAPI deployments, SSE queue fan-out patterns, and service
boundaries that separate orchestration from transport concerns.

## SCOPE

### In Scope

- FastAPI app factory wiring for API routers and shared dependencies.
- Playthrough creation, action dispatch, and health/debug endpoints.
- Debug stream isolation policies and queue lifecycle management.

### Out of Scope

- Frontend hooks and UI-specific state handling → see: `docs/frontend/`.
- Graph mutation logic and physics tick behavior → see: `docs/physics/`.
- Narrator prompt composition and agent behavior → see: `docs/agents/narrator/`.

## GAPS / IDEAS / QUESTIONS

- [ ] Document the API versioning strategy once public clients exist.
- [ ] Clarify whether debug SSE should be behind auth or dev-only config.
- IDEA: Split the app factory into per-router factories when the surface grows.
- QUESTION: Should health checks include a read-only scenario asset check?

---

## THE PROBLEM

The API layer must expose playthrough, moment, and debug endpoints without
leaking engine internals or forcing clients to know graph details. Without a
clear API boundary, gameplay flow fragments and frontend integration drifts.

---

## THE PATTERN

A FastAPI app factory wires routers, shared services, and SSE streams in one
place, while each router focuses on a single concern. The API stays thin,
translating requests into orchestrated engine calls and streaming updates.

---

## PRINCIPLES

### Principle 1: Single Entry App Factory

Centralize dependency wiring so route modules stay declarative and shared
state stays scoped to a single application instance.

### Principle 2: Thin Translation Layer

Endpoints translate HTTP payloads into engine calls without embedding business
logic, keeping behavior consistent with core services.

### Principle 3: Stream Isolation

Separate debug SSE from gameplay streams so observability does not interfere
with player-facing event delivery.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| engine/infrastructure/api/app.py | Hosts the FastAPI factory and router wiring. |
| engine/infrastructure/api/playthroughs.py | Implements playthrough CRUD and creation flows. |
| engine/infrastructure/api/moments.py | Provides moment and narration endpoints. |
| engine/infrastructure/api/sse_broadcast.py | Manages per-client SSE queues and broadcasts. |
| engine/infrastructure/orchestration | Bridges API requests to narrator/tick orchestration. |

---

## INSPIRATIONS

FastAPI's router-first design, event-stream APIs in realtime games, and prior
service layering in the history and async architecture modules.

---

## SCOPE

### In Scope

- FastAPI application factory and router wiring.
- Playthrough, moment, tempo, and debug stream endpoints.
- SSE event fan-out for gameplay and debug streams.

### Out of Scope

- Core game logic and physics ticks → see: `docs/physics/`.
- Long-running orchestration workflows → see: `docs/agents/world-runner/`.
- Frontend state management → see: `docs/frontend/`.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm whether API auth will live here or in a dedicated gateway module.
- [ ] Document rate limiting expectations once load patterns are known.
- IDEA: Add structured error envelopes for all endpoints.
- QUESTION: Should debug SSE move to a separate service boundary?

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

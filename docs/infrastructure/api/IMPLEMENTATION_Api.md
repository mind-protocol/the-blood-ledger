# API — Implementation

## CODE STRUCTURE

```
engine/infrastructure/api/
├── __init__.py         # Package export surface
├── app.py              # FastAPI app factory + legacy endpoints
├── moments.py          # Moment graph router + SSE stream
├── playthroughs.py     # Playthrough creation + moment ingestion
├── tempo.py            # Tempo controller endpoints
└── sse_broadcast.py    # Shared SSE client registry and broadcast
```

Each router module owns its own request models and helper functions; the app
factory wires routers plus the legacy endpoints that still live in `app.py`.

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/api/app.py` | App factory, core endpoints, debug SSE. | `create_app`, `player_action`, `debug_stream` | ~735 | SPLIT |
| `engine/infrastructure/api/moments.py` | Moment graph endpoints + SSE stream. | `create_moments_router`, `click_word` | ~489 | WATCH |
| `engine/infrastructure/api/playthroughs.py` | Playthrough creation + discussion trees. | `create_playthroughs_router`, `create_playthrough` | ~579 | WATCH |
| `engine/infrastructure/api/tempo.py` | Tempo endpoints and controller lifecycle. | `create_tempo_router`, `_get_or_create_controller` | ~234 | OK |
| `engine/infrastructure/api/sse_broadcast.py` | Shared SSE fan-out registry. | `register_sse_client`, `broadcast_moment_event` | ~81 | OK |

**Size thresholds:** `app.py` is already above SPLIT; new endpoints should be extracted into router modules before more growth.

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** App-factory + router-factory FastAPI layout with event fan-out for SSE.

**Why this pattern:** Centralized setup keeps shared dependencies consistent, while router factories isolate endpoint groups and keep hot-path code obvious.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Factory | `app.py:create_app` | Single entry for wiring routers + shared helpers. |
| Factory | `moments.py:create_moments_router` | Consistent router setup with config. |
| Observer/Fan-out | `sse_broadcast.py` | Broadcast click/moment events to SSE clients. |
| Cache | per-playthrough maps | Reuse GraphQueries + orchestrators per playthrough. |

### Anti-Patterns to Avoid

- **God Router**: avoid adding new API endpoints directly into `app.py`.
- **Hidden Globals**: keep caches explicit and scoped to modules, not implicit imports.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| API transport | FastAPI routing + request models | graph logic + orchestration | `/api/*` endpoints |
| Playthrough creation | filesystem + GraphOps injection | LLM narration + tick logic | `POST /api/playthrough/create` |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `create_app()` | `engine/infrastructure/api/app.py:110` | Import-time wiring or tests. |
| `app = create_app(...)` | `engine/infrastructure/api/app.py:731` | Uvicorn import path. |
| `__main__` uvicorn run | `engine/infrastructure/api/app.py:733` | `python app.py` entry. |
| `create_moments_router()` | `engine/infrastructure/api/moments.py:156` | App factory. |
| `create_playthroughs_router()` | `engine/infrastructure/api/playthroughs.py:189` | App factory. |
| `create_tempo_router()` | `engine/infrastructure/api/tempo.py:63` | App factory. |

---

## DATA FLOW

### Action Loop: Player Action → Orchestrator

```
Player UI
  └─ POST /api/action (ActionRequest)
        └─ app.py:player_action()
              └─ Orchestrator.process_action()
                    └─ narrator → tick → flips → world runner
                          └─ response payload
```

### Moment Click: Hot Path → SSE Fan-out

```
Player UI
  └─ POST /api/moments/click (ClickRequest)
        └─ MomentTraversal.handle_click()
              └─ broadcast_moment_event()
                    └─ SSE clients receive click_traversed + moment_activated
```

### Playthrough Creation: Scenario → Graph + Scene

```
Client
  └─ POST /api/playthrough/create
        └─ playthroughs.py:create_playthrough()
              ├─ create playthrough dirs + player.yaml
              ├─ load scenario YAML from /scenarios
              ├─ GraphOps.apply() injects nodes/links
              └─ opening.json → scene.json response
```

---

## SCHEMA

### ActionRequest

```yaml
ActionRequest:
  required:
    - playthrough_id: str
    - action: str
  optional:
    - player_id: str            # default "char_player"
    - location: str | null
    - stream: bool              # return SSE when true
```

### PlaythroughCreateRequest

```yaml
PlaythroughCreateRequest:
  required:
    - scenario_id: str
    - player_name: str
  optional:
    - player_gender: str
```

### MomentRequest

```yaml
MomentRequest:
  required:
    - playthrough_id: str
    - text: str
  optional:
    - moment_type: str          # player_freeform | player_click | player_choice
```

### SSE Payloads

```yaml
DebugSSEEvent:
  required:
    - type: str                 # apply_start, node_created, link_created, ...
    - data: object              # event-specific payload

MomentSSEEvent:
  required:
    - type: str                 # click_traversed, moment_activated, ...
    - data: object              # moment_id, weight, clicked_word
  constraints:
    - max_queue_size: 100
```

---

## LOGIC CHAINS

### LC1: Health Check

**Purpose:** Validate graph connectivity without heavy scans.

```
GET /health
  → get_graph_queries().query("RETURN 1 AS ok")
    → get_graph_ops() to validate write path
      → return status or 503 with details
```

**Data transformation:**
- Input: HTTP request.
- Output: status JSON with `details` and optional `errors`.

### LC2: Debug Stream

**Purpose:** Broadcast mutation events to debug UI clients.

```
GET /api/debug/stream
  → register asyncio queue in _debug_sse_clients
    → add_mutation_listener broadcasts events
      → StreamingResponse yields keepalive + events
```

### LC3: Player Moment Ingestion

**Purpose:** Create a player moment and return its id to the caller.

```
POST /api/moment
  → GraphOps + GraphQueries for playthrough
    → MomentProcessor.process_player_action()
      → moment id returned to caller
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/api
    ├── imports → engine/infrastructure/orchestration (Orchestrator)
    ├── imports → engine/physics/graph (GraphOps, GraphQueries)
    ├── imports → engine/moment_graph (MomentTraversal/Queries/Surface)
    ├── imports → engine/infrastructure/memory (MomentProcessor)
    ├── imports → engine/infrastructure/tempo (TempoController)
    └── imports → engine/infrastructure/embeddings (optional embedding service)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| fastapi | HTTP server, routing, SSE responses | `app.py`, `moments.py`, `playthroughs.py`, `tempo.py` |
| pydantic | request/response validation | `app.py`, `moments.py`, `playthroughs.py`, `tempo.py` |
| PyYAML | scenario + player YAML parsing | `playthroughs.py`, `moments.py` |

---

## STATE MANAGEMENT

| State | Location | Scope | Notes |
|-------|----------|-------|-------|
| `_orchestrators` | `app.py` | process | per-playthrough orchestrator cache |
| `_graph_queries` / `_graph_ops` | `app.py` | process | lazy singleton for default graph |
| `_debug_sse_clients` | `app.py` | process | per-connection queues for debug SSE |
| `_queries_cache` | `playthroughs.py` | process | per-playthrough GraphQueries cache |
| `_tempo_controllers` | `tempo.py` | process | per-playthrough tempo state |
| `_tempo_tasks` | `tempo.py` | process | per-playthrough async loop tasks |
| `_sse_clients` | `sse_broadcast.py` | process | per-playthrough moment SSE clients |
| playthrough files | `playthroughs/` | filesystem | `player.yaml`, `scene.json`, queues |

### State Transitions

```
no_orchestrator ──request──▶ orchestrator_cached ──process_exit──▶ cleared
no_tempo_task ──/tempo/start──▶ running_task ──/tempo/stop──▶ cleared
no_sse_client ──SSE connect──▶ queued_client ──disconnect──▶ removed
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Logging + CORS middleware configured in app.py.
2. create_app() wires routers and shared graph helpers.
3. Mutation listener registered for debug streaming.
```

### Request Cycle

```
1. FastAPI routes request to router handler.
2. Handler resolves cached helpers or per-playthrough instances.
3. Response returns JSON or SSE stream; errors bubble as HTTPException.
```

### Shutdown

```
1. No explicit shutdown hook; process exit clears caches.
2. SSE queues are pruned when clients disconnect.
```

---

## CONCURRENCY MODEL

FastAPI handlers run concurrently on the event loop. In-memory caches and SSE
client lists are not locked; they assume single-process ownership and rely on
append/remove operations for best-effort safety. Queue usage is bounded by
maxsize; full queues drop events. Concurrent requests for the same playthrough
can race when creating orchestrators or tempo controllers but converge on a
single cached instance per process.

| Component | Model | Notes |
|-----------|-------|-------|
| FastAPI endpoints | async | Await IO, avoid blocking work. |
| Debug SSE stream | async queues | Per-client queue with keepalive pings. |
| Moment SSE stream | async queues | Shared registry in `sse_broadcast.py`. |
| Tempo loop | background task | `asyncio.create_task` per playthrough. |

---

## CONFIGURATION

| Config | Default | Location | Purpose |
|--------|---------|----------|---------|
| `graph_name` | `blood_ledger` | `create_app`, `create_playthroughs_router` | Base graph name for non-playthrough access. |
| `host` | `localhost` | router factories | FalkorDB host used for graph connections. |
| `port` | `6379` | router factories | FalkorDB port for graph IO. |
| `playthroughs_dir` | `playthroughs` | `create_app` | File storage root for playthrough data. |
| `allow_origins` | `*` | CORS middleware | Development-friendly CORS policy. |
| `uvicorn host/port` | `0.0.0.0:8000` | `app.py` main | Default CLI server binding. |

Logging writes to `data/logs/backend.log` and also mirrors to console loggers.

---

## BIDIRECTIONAL LINKS

### Code -> Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/api/app.py` | 13 | `DOCS: docs/infrastructure/api/` |
| `engine/infrastructure/api/app.py` | 16 | `# DOCS: docs/infrastructure/api/` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| App factory + shared caches | `engine/infrastructure/api/app.py:create_app` |
| Action endpoint | `engine/infrastructure/api/app.py:player_action` |
| Health check | `engine/infrastructure/api/app.py:health_check` |
| Debug SSE | `engine/infrastructure/api/app.py:debug_stream` |
| Playthrough creation | `engine/infrastructure/api/playthroughs.py:create_playthrough` |
| Moments router + SSE | `engine/infrastructure/api/moments.py:create_moments_router` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `engine/infrastructure/api/app.py` | ~735L | <400L | `engine/infrastructure/api/views.py` | view/ledger/chronicle endpoints |
| `engine/infrastructure/api/playthroughs.py` | ~579L | <400L | `engine/infrastructure/api/playthroughs_opening.py` | opening template + scene builder |
| `engine/infrastructure/api/moments.py` | ~489L | <400L | `engine/infrastructure/api/moments_sse.py` | SSE stream helpers |

### Missing Implementation

- [ ] Authentication/rate limiting is not implemented; boundaries are documented but not enforced.
- [ ] Injection queue contract is implicit; needs a dedicated API section for tooling.

### Ideas

- IDEA: Extract remaining legacy endpoints from `app.py` into router modules.
- IDEA: Add a shared error envelope for consistent frontend handling.

### Questions

- QUESTION: Should debug SSE be gated behind a config flag in non-dev deployments?
- QUESTION: Is playthrough creation the canonical place to seed graph data?

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

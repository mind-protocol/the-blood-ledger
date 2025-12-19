# API — Implementation

## CODE STRUCTURE

```
engine/infrastructure/api/app.py            # FastAPI app factory, monolithic endpoints
engine/infrastructure/api/moments.py        # Moment graph router and SSE stream
engine/infrastructure/api/playthroughs.py   # Playthrough creation + moment ingestion
engine/infrastructure/api/tempo.py          # Tempo controller endpoints
engine/infrastructure/api/sse_broadcast.py  # Shared SSE client registry and broadcast
engine/infrastructure/api/__init__.py       # Package export surface
```

Each router module owns its own request models and helper functions; the app
factory wires routers plus the legacy endpoints that still live in `app.py`.

---

## DESIGN PATTERNS

- **App factory**: `create_app()` centralizes wiring for routers, logging, and
  shared graph helpers, keeping initialization consistent across environments.
- **Router factories**: `create_moments_router`, `create_playthroughs_router`,
  and `create_tempo_router` isolate endpoint grouping and keep `app.py` thin.
- **Per-playthrough caches**: routers hold in-memory caches for graph queries,
  orchestrators, and tempo controllers keyed by playthrough id.
- **Shared SSE broadcast**: `sse_broadcast.py` maintains per-playthrough queues
  and makes click/moment events available across modules.

---

## ENTRY POINTS

| Entry Point | File | Triggered By |
|-------------|------|--------------|
| `create_app()` | `engine/infrastructure/api/app.py` | Server startup |
| `app = create_app(...)` | `engine/infrastructure/api/app.py` | Uvicorn import path |
| `create_moments_router()` | `engine/infrastructure/api/moments.py` | App factory |
| `create_playthroughs_router()` | `engine/infrastructure/api/playthroughs.py` | App factory |
| `create_tempo_router()` | `engine/infrastructure/api/tempo.py` | App factory |

---

## DATA FLOW

### Action Loop

```
POST /api/action
  -> get_orchestrator(playthrough_id)
  -> Orchestrator.process_action(...)
  -> physics tick + narrator + world runner side effects
```

### Moment Click (Fast Path)

```
POST /api/moments/click
  -> MomentTraversal.handle_click(...)
  -> broadcast_moment_event(...)
  -> SSE clients receive click_traversed + moment_activated
```

### Playthrough Creation

```
POST /api/playthrough/create
  -> create playthrough directories + player.yaml
  -> load scenario YAML from /scenarios
  -> GraphOps.apply(...) scenario nodes/links
  -> write scene.json + queue files
  -> return scene payload
```

---

## SCHEMA

### Request/Response Models (Pydantic)

| Model | File | Fields |
|-------|------|--------|
| `ActionRequest` | `engine/infrastructure/api/app.py` | `playthrough_id`, `action`, `player_id`, `location`, `stream` |
| `NewPlaythroughRequest` | `engine/infrastructure/api/app.py` | `drive`, `companion`, `initial_goal` |
| `MomentClickRequest` | `engine/infrastructure/api/app.py` | `playthrough_id`, `moment_id`, `word`, `player_id` |
| `PlaythroughCreateRequest` | `engine/infrastructure/api/playthroughs.py` | `scenario_id`, `player_name`, `player_gender` |
| `MomentRequest` | `engine/infrastructure/api/playthroughs.py` | `playthrough_id`, `text`, `moment_type` |
| `SetSpeedRequest` | `engine/infrastructure/api/tempo.py` | `playthrough_id`, `speed` |

### SSE Payloads

Debug SSE events are serialized JSON dicts with `type` and event fields such as
`node_created` or `link_created`. Moment SSE events use `type` plus a `data`
payload with `moment_id`, `weight`, and click metadata.

---

## LOGIC CHAINS

### Health Check

```
GET /health
  -> get_graph_queries().query("RETURN 1 AS ok")
  -> get_graph_ops() to validate write path
  -> return status or 503 with error details
```

### Debug Stream

```
GET /api/debug/stream
  -> register asyncio queue in _debug_sse_clients
  -> add_mutation_listener broadcasts events
  -> StreamingResponse yields keepalive pings + events
```

### Player Moment Ingestion

```
POST /api/moment
  -> GraphOps + GraphQueries for playthrough
  -> MomentProcessor.process_player_action(...)
  -> moment id returned to caller
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

- `engine/infrastructure/orchestration.Orchestrator` for action processing.
- `engine/physics/graph.GraphOps` + `GraphQueries` for graph IO.
- `engine/moment_graph` for traversal, surface stats, and click handling.
- `engine/infrastructure/memory.MomentProcessor` for player moment ingestion.
- `engine/infrastructure/tempo.TempoController` for speed control.
- `engine/infrastructure/embeddings` for optional embeddings on moments.

### External Dependencies

`fastapi`, `pydantic`, `asyncio`, `json`, `yaml`, `logging`, `pathlib`, `datetime`.

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

---

## RUNTIME BEHAVIOR

On startup, `create_app()` configures CORS, logging, and router mounts, then
registers mutation listeners for debug streaming. Requests are handled
asynchronously; errors are logged and surfaced as `HTTPException` responses.
Playthrough creation performs filesystem writes, graph seeding, and JSON
serialization in a single request path without transactional rollback.

---

## CONCURRENCY MODEL

FastAPI handlers run concurrently on the event loop. In-memory caches and SSE
client lists are not locked; they assume single-process ownership and rely on
append/remove operations for best-effort safety. Queue usage is bounded by
maxsize; full queues drop events. Concurrent requests for the same playthrough
can race when creating orchestrators or tempo controllers but converge on a
single cached instance per process.

---

## CONFIGURATION

| Config | Default | Location | Purpose |
|--------|---------|----------|---------|
| `graph_name` | `blood_ledger` | `create_app`, `create_playthroughs_router` | Base graph name |
| `host` | `localhost` | router factories | FalkorDB host |
| `port` | `6379` | router factories | FalkorDB port |
| `playthroughs_dir` | `playthroughs` | `create_app` | File storage root |
| `allow_origins` | `*` | CORS middleware | Allow all origins (dev default) |

Logging writes to `data/logs/backend.log` and also mirrors to console loggers.

---

## BIDIRECTIONAL LINKS

### Code -> Docs

| File | Reference |
|------|-----------|
| `engine/infrastructure/api/app.py` | `DOCS: docs/infrastructure/api/` |
| `engine/infrastructure/api/tempo.py` | `DOCS: docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| App factory + shared caches | `engine/infrastructure/api/app.py:create_app` |
| Playthrough router | `engine/infrastructure/api/playthroughs.py:create_playthroughs_router` |
| Moments router + SSE | `engine/infrastructure/api/moments.py:create_moments_router` |
| Debug SSE | `engine/infrastructure/api/app.py:debug_stream` |
| Tempo API | `engine/infrastructure/api/tempo.py:create_tempo_router` |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide whether auth and rate limiting live inside the API or at a gateway.
- [ ] Document the injection queue contract in a dedicated API section.
- IDEA: Extract remaining legacy endpoints from `app.py` into router modules.
- QUESTION: Should debug SSE be gated behind a config flag in non-dev deployments?

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

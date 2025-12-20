# 07_Backend_API_And_Orchestration_EntryPoints_And_Contracts

@pack:generated_at: 2025-12-20T10:41:21
@pack:repo_kind: blood-ledger

Backend API + orchestration entry points and contracts


---

## SOURCE: docs/infrastructure/api/ALGORITHM_Api.md
# API — Algorithm

## OVERVIEW

This algorithm doc describes how the API module wires the FastAPI app, handles
core runtime helpers (graph access, health checks, SSE debug streaming), and
executes the playthrough-creation flow that seeds the game graph and scene
payloads for the frontend.

## DATA STRUCTURES

- Playthrough folder layout: per-player directory containing queues, scene
  snapshots, and metadata files for API and agent coordination.
- Scenario YAML payloads: structured nodes, links, and opening narration blocks
  injected into the per-playthrough graph.
- Moment records: narration lines stored as moment nodes with status/weight,
  linked to locations for initial scene rendering.
- Debug SSE queues: per-client in-memory queues carrying event payloads.

## ALGORITHM: create_scenario_playthrough

The primary flow accepts a scenario request, generates a unique playthrough id,
creates the on-disk playthrough structure, initializes the FalkorDB graph,
injects scenario nodes/links, seeds opening narration moments, and returns the
scene payload plus identifiers required for the frontend to continue.

## KEY DECISIONS

- Use a single app factory to centralize shared resources, keeping endpoints
  thin and delegating heavy logic to orchestration and graph layers.
- Isolate debug SSE streams from gameplay SSE to avoid cross-talk and stalled
  consumers.
- Keep playthrough graphs isolated per player by using a unique graph name.

## DATA FLOW

Client requests enter FastAPI routes, the API loads scenario data from disk,
executes graph mutations through GraphOps, writes playthrough artifacts to
disk, and returns a scene payload that the frontend rehydrates into the game
view while SSE streams deliver ongoing updates.

## COMPLEXITY

Runtime cost is dominated by I/O and graph writes; scenario injection scales
roughly with the number of nodes/links in the scenario, while playthrough
folder creation and scene serialization are linear in payload size.

## HELPER FUNCTIONS

Graph helpers cache GraphQueries/GraphOps instances per request context, health
checks validate read/write access with lightweight queries, and debug SSE
streams maintain per-client queues that emit events or keepalive pings.
Discussion tree helpers count remaining leaf branches to determine when the
background generator should refresh a companion's topics.

## INTERACTIONS

This module coordinates with graph physics for mutations, with orchestration
services for playthrough actions, with scenario files for seed content, and
with frontend hooks that call playthrough and view endpoints.

## GAPS / IDEAS / QUESTIONS

- [ ] Document API versioning once public clients exist and endpoints stabilize.
- [ ] Clarify how auth and rate limiting should be layered (API vs gateway).
- QUESTION: Should health checks validate scenario assets on disk?

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

## Playthrough Creation

### Overview

End-to-end flow when a player creates a new playthrough, from frontend form submission through graph initialization to first scene render.
This section supersedes the deprecated `ALGORITHM_Playthrough_Creation.md` alias.

### Data Structures

- `PlaythroughCreateRequest` carries `scenario_id`, `player_name`, and `player_gender` for creating a new run with consistent inputs.
- `player.yaml`, `scene.json`, and the queue files (`message_queue.json`, `injection_queue.json`, `stream.jsonl`) persist state on disk for later endpoints.
- Scenario YAML provides `nodes`, `links`, and `opening` blocks that seed the graph and opening scene.

### Algorithm: create_playthrough

1. Slugify the player name and pick a unique playthrough ID by checking the playthroughs directory.
2. Create the playthrough directory structure and write `player.yaml` with scenario metadata.
3. Load the scenario YAML and initialize a dedicated graph using `load_initial_state()`.
4. Apply scenario nodes/links with `GraphOps.apply`, updating the player node name/gender.
5. Create opening moments from `opening.narration` and attach them to the opening place.
6. Build `scene.json` from the opening template (fallback to a minimal scene if absent).
7. Return the playthrough ID, scenario ID, and scene payload for the frontend to render.

### Key Decisions

- Use the playthrough ID as the graph name to isolate player sessions without cross-talk.
- Continue after seed-data or scenario injection failures so the frontend can still render a starter scene.
- Store queues and transcripts on disk so async systems can resume from simple file state.

### Data Flow

Request data flows from the frontend form into `create_playthrough`, then into disk state (`player.yaml`, queues) and graph mutations (seed + scenario), culminating in `scene.json` plus a response payload.

### Complexity

Time scales linearly with the number of scenario nodes, links, and opening lines; disk I/O and graph calls dominate runtime for larger scenarios.

### Helper Functions

- `_opening_to_scene_tree` transforms the opening template into the `scene.json` structure.
- `load_initial_state` seeds the base world graph before scenario injection.
- `GraphOps.apply` and `GraphOps.add_moment` write scenario content and opening moments.

### Interactions

Creates playthrough artifacts consumed by `GET /api/view/{playthrough_id}`, relies on `engine/physics/graph` for mutations, and loads scenario assets from `scenarios/*.yaml`.

### Gaps / Ideas / Questions

- [ ] Should scenario YAML be schema-validated before graph injection to surface errors earlier?
- [ ] Should playthrough creation fail hard if seed data fails, or continue as it does now?

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND FLOW                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. /start                    2. /scenarios                              │
│  ┌──────────────────┐        ┌──────────────────┐                       │
│  │ Enter name       │───────▶│ Select scenario  │                       │
│  │ Select gender    │        │ (5 options)      │                       │
│  │                  │        │                  │                       │
│  │ sessionStorage:  │        │ Click "Begin"    │                       │
│  │  playerName      │        │        │         │                       │
│  │  playerGender    │        └────────┼─────────┘                       │
│  └──────────────────┘                 │                                 │
│                                       ▼                                 │
│                      POST /api/playthrough/create                       │
│                      {scenario_id, player_name, player_gender}          │
│                                       │                                 │
└───────────────────────────────────────┼─────────────────────────────────┘
                                        │
┌───────────────────────────────────────┼─────────────────────────────────┐
│                           BACKEND FLOW                                   │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 1. GENERATE PLAYTHROUGH ID                                       │   │
│  │    - Slugify player name: "Edmund" → "edmund"                    │   │
│  │    - Add suffix if exists: "edmund_2", "edmund_3"...             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 2. CREATE FOLDER STRUCTURE                                       │   │
│  │    playthroughs/{playthrough_id}/                                │   │
│  │    ├── mutations/                                                │   │
│  │    ├── conversations/                                            │   │
│  │    ├── player.yaml          # name, gender, scenario, graph_name │   │
│  │    ├── scene.json           # opening scene for frontend         │   │
│  │    ├── message_queue.json   # player inputs queue                │   │
│  │    ├── injection_queue.json # world events queue                 │   │
│  │    ├── stream.jsonl         # narrator output stream             │   │
│  │    └── PROFILE_NOTES.md     # narrator's player observations     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 3. INITIALIZE GRAPH (FalkorDB)                                   │   │
│  │    - Graph name = playthrough_id (isolated per player)           │   │
│  │    - load_initial_state() loads seed data:                       │   │
│  │      • Base world nodes (places, characters)                     │   │
│  │      • Core narratives and tensions                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 4. LOAD SCENARIO YAML                                            │   │
│  │    scenarios/{scenario_id}.yaml                                  │   │
│  │    Contains:                                                     │   │
│  │      • nodes: characters, places, things specific to scenario    │   │
│  │      • links: relationships, AT positions, BELIEVES edges        │   │
│  │      • opening: {narration, location, characters_present}        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 5. INJECT SCENARIO INTO GRAPH                                    │   │
│  │    - Update char_player with player_name, player_gender          │   │
│  │    - graph.apply(nodes, links) merges into FalkorDB              │   │
│  │    - Creates/updates nodes and relationships                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 6. CREATE OPENING MOMENTS                                        │   │
│  │    - Parse opening.narration from scenario                       │   │
│  │    - Split into lines, create Moment nodes:                      │   │
│  │      {id, text, type:"narration", status:"active", weight:1.0}   │   │
│  │    - Attach to opening location via AT_PLACE edge                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 7. GENERATE scene.json                                           │   │
│  │    - Load opening.json template (discussion tree structure)      │   │
│  │    - Convert to SceneTree format for frontend                    │   │
│  │    - Save to playthrough folder                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                       │                                 │
│                                       ▼                                 │
│                      RETURN {playthrough_id, scenario, scene}           │
│                                                                          │
└───────────────────────────────────────┬─────────────────────────────────┘
                                        │
┌───────────────────────────────────────┼─────────────────────────────────┐
│                           FRONTEND CONTINUES                             │
│                                       ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 8. REDIRECT TO GAME                                              │   │
│  │    - Store playthrough_id in sessionStorage                      │   │
│  │    - Navigate to /playthroughs/{playthrough_id}                  │   │
│  │    - useGameState() fetches /api/view/{playthrough_id}           │   │
│  │    - Renders moments from active_moments                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Key Files

| Step | File | Purpose |
|------|------|---------|
| 1-2 | `frontend/app/start/page.tsx` | Name/gender input |
| 2 | `frontend/app/scenarios/page.tsx` | Scenario selection |
| 3-7 | `engine/infrastructure/api/playthroughs.py` | POST /playthrough/create |
| 3 | `engine/init_db.py` | load_initial_state() |
| 4 | `scenarios/*.yaml` | Scenario definitions |
| 5 | `engine/physics/graph/graph_ops.py` | apply() for graph injection |
| 6 | `engine/physics/graph/graph_ops.py` | add_moment() |
| 8 | `frontend/hooks/useGameState.ts` | Fetches view, renders scene |

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/playthrough/create` | POST | Create new playthrough from scenario |
| `/api/playthrough/scenario` | POST | Alternative endpoint (same function) |
| `/api/view/{playthrough_id}` | GET | Get current view for rendering |

### Error States

| Error | Cause | Fix |
|-------|-------|-----|
| 404 on /scenario | Wrong endpoint path | Use `/api/playthrough/scenario` |
| "No moments found, needs opening" | Opening moments not created | Check step 6, verify graph has Moments |
| Empty view | Player not AT any location | Check scenario has player AT link |

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md


---

## SOURCE: docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md
# API — Algorithm: Playthrough Creation (Legacy Alias)

```
STATUS: DEPRECATED (alias to ALGORITHM_Api.md)
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against engine/infrastructure/api/playthroughs.py (working tree)
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
THIS:            ALGORITHM_Playthrough_Creation.md (legacy alias)
VALIDATION:      ./VALIDATION_Api.md
IMPLEMENTATION:  ./IMPLEMENTATION_Api.md
TEST:            ./TEST_Api.md
SYNC:            ./SYNC_Api.md

IMPL:            engine/infrastructure/api/playthroughs.py
```

> **Contract:** This file is a legacy alias. The canonical algorithm reference
> for the API module is `docs/infrastructure/api/ALGORITHM_Api.md`.

---

## OVERVIEW

Playthrough creation turns a scenario selection into a live, isolated graph
instance plus a starter `scene.json` payload for the frontend. This alias
summarizes the flow so older references keep working while the canonical API
algorithm doc remains the source of truth.

---

## DATA STRUCTURES

### PlaythroughCreateRequest

```
player_name: string
player_gender: string
scenario_id: string
```

The request payload passed to `/api/playthrough/create` and its alias.

### PlaythroughFilesystemLayout

```
playthroughs/{id}/
  player.yaml
  scene.json
  message_queue.json
  injection_queue.json
  stream.jsonl
  PROFILE_NOTES.md
```

Directory layout that makes the playthrough discoverable by other endpoints.

### ScenarioPayload

```
nodes: list
links: list
opening: { narration, ... }
location: string
```

Scenario YAML entries used to seed graph nodes, relationships, and opening
narration moments for the new playthrough.

---

## ALGORITHM: create_playthrough

### Step 1: Generate an isolated playthrough id

Normalize the player name into a slug and append a numeric suffix if the
directory already exists. This prevents collisions while keeping IDs stable
for users who repeat their name.

### Step 2: Materialize the playthrough workspace

Create the playthrough folder structure, write `player.yaml`, and seed the
queue and log files. This step ensures downstream endpoints can immediately
read/write files even if graph initialization fails.

### Step 3: Initialize graph + scenario state

Load base seed data into a new FalkorDB graph and apply the scenario’s nodes
and links. Update the player node with the request’s name and gender before
calling `GraphOps.apply` so the graph reflects the current player identity.

### Step 4: Create opening narration moments

Parse the scenario opening narration, create Moment nodes with `status=possible`,
and attach them to the opening location. These moments are surfaced later by
the canon holder rather than pre-marking them as spoken.

### Step 5: Build the opening scene payload

Transform the opening template into a `scene.json` payload if the template
exists; otherwise write a minimal fallback scene. Persist the JSON so the
frontend can fetch the same scene on subsequent loads.

---

## KEY DECISIONS

### D1: Graph isolation vs. reuse

```
IF playthrough_id is new:
    create a new graph name and seed it
    keep the playthrough isolated per player
ELSE:
    reject or suffix the id to avoid cross-player state bleed
```

Isolation preserves per-player state at the cost of more graph instances.

### D2: Opening moments as possible vs. spoken

```
IF narration lines exist:
    create moments with status="possible" and weight=1.0
    let canon holder surface and record them
ELSE:
    skip moment creation and rely on the fallback scene
```

This keeps canon recording centralized while still bootstrapping the scene.

---

## DATA FLOW

```
PlaythroughCreateRequest
    ↓
playthrough_id + filesystem layout
    ↓
scenario YAML + seed graph data
    ↓
graph mutations + opening moments
    ↓
scene.json payload
    ↓
API response {playthrough_id, scenario, scene}
```

---

## COMPLEXITY

**Time:** O(S + M) — S for scenario nodes/links, M for opening narration lines.

**Space:** O(S + M) — persistent files and graph writes scale with scenario size.

**Bottlenecks:**
- Scenario injection cost grows with node/link count in the YAML.
- Graph initialization latency dominates if seed data is large.

---

## HELPER FUNCTIONS

### `_opening_to_scene_tree()`

**Purpose:** Convert opening template JSON plus scenario data into a scene tree.

**Logic:** Maps beats into narration/voice entries and injects scenario-specific
character and location names into the response payload.

### `_count_branches()`

**Purpose:** Count discussion branches when generating metadata for openings.

**Logic:** Walks nested discussion structures to compute clickables and branch
depths used by the scene tree.

### `_get_playthrough_queries()`

**Purpose:** Provide cached `GraphQueries` objects for a playthrough graph.

**Logic:** Lazily constructs the query helper on first access and reuses it for
subsequent API calls to avoid repeated connection setup.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| engine/init_db.py | `load_initial_state()` | Base world graph seed data |
| engine/physics/graph/graph_ops.py | `GraphOps.apply()` | Scenario nodes/links persisted |
| engine/physics/graph/graph_ops.py | `GraphOps.add_moment()` | Opening narration moments |
| scenarios/*.yaml | Scenario file load | Nodes, links, opening, location |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm whether playthrough creation should fail on seed-data errors.
- [ ] Decide if scene template lookup should be scenario-specific.
- IDEA: Cache parsed scenario YAML to avoid re-reading on duplicate starts.
- IDEA: Emit a single audit event once playthrough creation completes.
- QUESTION: Should the API return validation warnings from graph injection?


---

## SOURCE: docs/infrastructure/api/BEHAVIORS_Api.md
# API — Behaviors

## BEHAVIORS

The API exposes a thin FastAPI surface that brokers playthrough creation,
moment streaming, and debug mutation visibility while delegating heavy work to
orchestration and graph layers. It guarantees consistent response shapes for
health and debug endpoints and preserves a stable SSE connection contract.

## INPUTS / OUTPUTS

- Inputs include HTTP requests to playthrough, moment, action, and health
  routes plus SSE client connections for gameplay and debug streams.
- Outputs include JSON payloads for health/action responses and SSE event
  frames with named events, timestamps, and JSON data payloads.

## EDGE CASES

- If the graph client is unreachable, health checks downgrade to a 503 response
  with a degraded status and explicit error detail.
- Debug stream queues can become idle; the server emits keepalive pings to
  avoid idle timeouts and to confirm stream liveness.

## Health Check

- `GET /health` returns `status=ok` with timestamp and connection details when the graph is reachable.
- If graph connectivity fails, the endpoint responds with `503` and a `status=degraded` payload describing the failure.

## Debug Mutation Stream

- `GET /api/debug/stream` opens a server-sent events stream for mutation events.
- The stream sends:
  - `connected` event on connect
  - `mutation` events with JSON payloads
  - `ping` keepalives when idle

## ANTI-BEHAVIORS

- The API should not mutate graph state inside health checks or debug streams.
- The debug SSE channel should not leak gameplay events or block on slow
  consumers; each client must keep an isolated queue.

## GAPS / IDEAS / QUESTIONS

- [ ] Document the expected payload shapes for `/api/action` once the frontend
  contract stabilizes.
- IDEA: Add explicit backpressure guidance for debug streams in the API docs.
- QUESTION: Should health checks validate scenario assets or remain pure
  connectivity probes?

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md


---

## SOURCE: docs/infrastructure/api/HEALTH_Api.md
# API — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2024-12-18
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the API surface. It ensures that the entry points for player interaction, playthrough management, and debug streaming are responsive and structurally sound.

What it protects:
- **Connectivity**: Availability of core API endpoints and graph database backends.
- **Contract Integrity**: Consistency of request/response schemas for gameplay actions.
- **Streaming Reliability**: Stability of SSE fan-out for real-time updates.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
ALGORITHM:       ./ALGORITHM_Api.md
VALIDATION:      ./VALIDATION_Api.md
IMPLEMENTATION:  ./IMPLEMENTATION_Api.md
THIS:            HEALTH_Api.md
SYNC:            ./SYNC_Api.md

IMPL:            engine/infrastructure/api/app.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. Run HEALTH checks at throttled rates.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: action_loop
    purpose: Ensure player actions can be processed and returned.
    triggers:
      - type: manual
        source: curl /api/action
    frequency:
      expected_rate: 2/min (per active player)
      peak_rate: 20/min
      burst_behavior: Rate limited at transport layer (planned).
    risks:
      - Timeout on narrator generation
      - Broken SSE stream delivery
    notes: Primary interaction loop.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: api_availability
    flow_id: action_loop
    priority: high
    rationale: If the API is down, the game is unplayable.
  - name: graph_reachability
    flow_id: action_loop
    priority: high
    rationale: API depends on FalkorDB for all state.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: stdout
  result:
    representation: enum
    value: OK
    updated_at: 2025-12-20T10:05:00Z
    source: health_check
```

---

## DOCK TYPES (COMPLETE LIST)

- `api` (HTTP/RPC boundary)
- `db` (database reachability)

---

## CHECKER INDEX

```yaml
checkers:
  - name: connectivity_checker
    purpose: Verify API and DB availability.
    status: active
    priority: high
  - name: contract_checker
    purpose: Verify response schema compliance.
    status: pending
    priority: med
```

---

## INDICATOR: api_availability

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: api_availability
  client_value: Ensures the UI can always reach the backend services.
  validation:
    - validation_id: V1 (Conceptual)
      criteria: API returns 200 OK for /health.
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - enum
  semantics:
    enum: OK, DEGRADED, DOWN
  aggregation:
    method: worst_case
    display: Dashboard
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: action_input
    method: engine.infrastructure.api.app.player_action
    location: engine/infrastructure/api/app.py:120
  output:
    id: action_output
    method: engine.infrastructure.api.app.player_action
    location: engine/infrastructure/api/app.py:150
```

---

## MANUAL RUN

```bash
# Verify API Health
curl http://localhost:8000/health

# Verify Action Loop
curl -X POST http://localhost:8000/api/action -d '{"playthrough_id": "test", "action": "look"}'
```

---

## KNOWN GAPS

- [ ] Automated regression for SSE stream delivery under load.
- [ ] Schema validation tests for all router endpoints.

---

## SOURCE: docs/infrastructure/api/IMPLEMENTATION_Api.md
# API — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2024-12-18
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
ALGORITHM:       ./ALGORITHM_Api.md
VALIDATION:      ./VALIDATION_Api.md
THIS:            IMPLEMENTATION_Api.md
HEALTH:          ./HEALTH_Api.md
SYNC:            ./SYNC_Api.md

IMPL:            engine/infrastructure/api/app.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

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

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/api/app.py` | App factory, core endpoints, debug SSE | `create_app`, `player_action` | ~735 | SPLIT |
| `engine/infrastructure/api/moments.py` | Moment graph endpoints + SSE stream | `create_moments_router` | ~489 | WATCH |
| `engine/infrastructure/api/playthroughs.py` | Playthrough creation | `create_playthrough` | ~579 | WATCH |
| `engine/infrastructure/api/tempo.py` | Tempo endpoints | `create_tempo_router` | ~234 | OK |
| `engine/infrastructure/api/sse_broadcast.py` | Shared SSE fan-out registry | `register_sse_client` | ~81 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** App-factory + router-factory FastAPI layout with event fan-out for SSE.

**Why this pattern:** Centralized setup keeps shared dependencies consistent, while router factories isolate endpoint groups and keep hot-path code obvious.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Factory | `app.py:create_app` | Single entry for wiring routers + shared helpers. |
| Observer/Fan-out | `sse_broadcast.py` | Broadcast click/moment events to SSE clients. |
| Cache | per-playthrough maps | Reuse GraphQueries + orchestrators per playthrough. |

### Anti-Patterns to Avoid

- **God Router**: avoid adding new API endpoints directly into `app.py`.
- **Hidden Globals**: keep caches explicit and scoped to modules.

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
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `create_app()` | `engine/infrastructure/api/app.py:110` | Import-time wiring or tests |
| `app = create_app()` | `engine/infrastructure/api/app.py:731` | Uvicorn import path |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Action Loop: Player Action → Orchestrator

This flow handles the primary gameplay interaction loop where a player's intent is processed by the narrator and physics engine.

```yaml
flow:
  name: action_loop
  purpose: Process player actions through the simulation.
  scope: HTTP Request -> Orchestrator -> Result Response
  steps:
    - id: step_1_receive
      description: POST /api/action receives ActionRequest.
      file: engine/infrastructure/api/app.py
      function: player_action
      input: ActionRequest
      output: Response payload
      trigger: HTTP Post
      side_effects: none
    - id: step_2_process
      description: Orchestrator coordinates narrator and physics tick.
      file: engine/infrastructure/orchestration/orchestrator.py
      function: process_action
      input: action_text, playthrough_id
      output: ActionResult
      trigger: player_action call
      side_effects: graph mutations, history updates
  docking_points:
    guidance:
      include_when: action results are transformed or events are emitted
    available:
      - id: action_input
        type: api
        direction: input
        file: engine/infrastructure/api/app.py
        function: player_action
        trigger: POST /api/action
        payload: ActionRequest
        async_hook: not_applicable
        needs: none
        notes: Primary entry point for player intent
      - id: action_output
        type: api
        direction: output
        file: engine/infrastructure/api/app.py
        function: player_action
        trigger: return payload
        payload: object
        async_hook: optional
        needs: none
        notes: Response sent back to UI
    health_recommended:
      - dock_id: action_input
        reason: Verification of player intent ingestion.
      - dock_id: action_output
        reason: Verification of simulation response quality.
```

---

## LOGIC CHAINS

### LC1: Health Check

**Purpose:** Validate graph connectivity without heavy scans.

```
GET /health
  → get_graph_queries().query("RETURN 1 AS ok")
    → get_graph_ops() to validate write path
      → return status JSON
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/api
    ├── imports → engine/infrastructure/orchestration
    ├── imports → engine/physics/graph
    ├── imports → engine/moment_graph
    └── imports → engine/infrastructure/tempo
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| fastapi | HTTP server | `app.py`, `moments.py`, etc. |
| PyYAML | Config parsing | `playthroughs.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Orchestrator Cache | `app.py:_orchestrators` | process | per-playthrough cache |
| SSE Clients | `sse_broadcast.py:_sse_clients` | process | per-connection |

---

## RUNTIME BEHAVIOR

### Initialization

1. create_app() wires routers.
2. Shared graph helpers initialized lazily.

### Request Cycle

1. FastAPI routes to handler.
2. Handler resolves playthrough-specific state.
3. Response returned (JSON or SSE).

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| FastAPI | async | Concurrent request handling on event loop |
| SSE Streams | async queues | Dedicated per-client buffers |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `graph_name` | `create_app` | `blood_ledger` | Default FalkorDB graph |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/api/app.py` | 13 | `DOCS: docs/infrastructure/api/` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| App factory | `engine/infrastructure/api/app.py:create_app` |
| Health check | `engine/infrastructure/api/app.py:health_check` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `app.py` | ~735L | <400L | `views.py` | view/ledger endpoints |

### Missing Implementation

- [ ] Authentication and rate limiting.

---

## SOURCE: docs/infrastructure/api/PATTERNS_Api.md
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

- Frontend hooks and UI-specific state handling -> see: `docs/frontend/`.
- Graph mutation logic and physics tick behavior -> see: `docs/physics/`.
- Narrator prompt composition and agent behavior -> see: `docs/agents/narrator/`.

## GAPS / IDEAS / QUESTIONS

- [ ] Document the API versioning strategy once public clients exist.
- [ ] Clarify whether debug SSE should be behind auth or dev-only config.
- IDEA: Split the app factory into per-router factories when the surface grows.
- QUESTION: Should health checks include a read-only scenario asset check?

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
HEALTH: ./HEALTH_Api.md
SYNC: ./SYNC_Api.md
```


---

## SOURCE: docs/infrastructure/api/SYNC_Api.md
# API — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- API app factory, router wiring, and current playthrough/moment endpoints are live and documented.
- Debug and gameplay SSE streams are established with separate queues.

What's still being designed:
- Auth, rate limiting, and API gateway decisions.

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/api/app.py`

The API module hosts the FastAPI application, including playthrough endpoints, moment APIs, and debug streaming.

## RECENT CHANGES

### 2025-12-20: Broadcast player moments on SSE

- **What:** Emit `moment_spoken` SSE events when `/api/moment` creates a player moment.
- **Why:** UI relies on SSE to refresh; player messages were not appearing.
- **Impact:** Frontend receives a refresh trigger after player input.

### 2025-12-20: Fix moment stream route collision

- **What:** Moved `/api/moments/stream/{playthrough_id}` above the generic
  `/{playthrough_id}/{moment_id}` route in `engine/infrastructure/api/moments.py`.
- **Why:** The generic route was capturing `/stream/{id}` and returning 404.
- **Impact:** SSE stream endpoint responds with 200 as expected.

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Api.md` and updated `TEST_Api.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** API module documentation is now compliant; Health checks are anchored to concrete docking points.

### 2025-12-20: Discussion Tree Branch Counting

- **What:** Count discussion tree branches by remaining leaf paths and document the helper behavior.
- **Why:** Ensure regeneration triggers reflect actual remaining branch paths.
- **Impact:** Branch count now aligns with discussion tree lifecycle expectations.

## GAPS

- [ ] Automated regression for SSE stream delivery under load.
- [ ] Schema validation tests for all router endpoints.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code when touching API routers. Ensure new endpoints are extracted from `app.py` to keep it from growing further.

## TODO

- [ ] Split remaining legacy endpoints from `app.py` into router modules.
- [ ] Implement API versioning strategy.

## POINTERS

- `docs/infrastructure/api/PATTERNS_Api.md` for scope and design rationale.
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` for endpoint-level data flow notes.

## CHAIN

```
THIS:            SYNC_Api.md (you are here)
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
ALGORITHM:       ./ALGORITHM_Api.md
VALIDATION:      ./VALIDATION_Api.md
IMPLEMENTATION:  ./IMPLEMENTATION_Api.md
HEALTH:          ./HEALTH_Api.md
```


---

## SOURCE: docs/infrastructure/api/SYNC_Api_archive_2025-12.md
# Archived: SYNC_Api.md

Archived on: 2025-12-20
Original file: SYNC_Api.md

---

## RECENT CHANGES

### 2025-12-19: Re-verify API PATTERNS template completeness (repair 16)

- **What:** Confirmed `PATTERNS_Api.md` retains a single, complete template
  block with required sections populated.
- **Why:** The repair task targets PATTERNS drift; re-verification closes the
  audit trail without further content changes.
- **Files:**
  - `docs/infrastructure/api/PATTERNS_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Expand API implementation template details (repair 16)

- **What:** Added structured code-architecture sections (file responsibilities, schemas, flows, dependencies, runtime, config, and bidirectional links).
- **Why:** Ensure `IMPLEMENTATION_Api.md` fully matches the implementation template expectations for DOC_TEMPLATE_DRIFT.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Refresh API implementation coverage (repair 16)

- **What:** Expanded `IMPLEMENTATION_Api.md` with the missing template sections
  and rewrote the implementation narrative to match current router layout.
- **Why:** The implementation doc still lacked template coverage for code
  structure, data flow, configuration, and concurrency details.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Expand API test template coverage (repair 16)

- **What:** Added missing test template sections (strategy, unit/integration
  coverage, edge cases, run guidance, coverage, gaps, flaky tracking) in
  `TEST_Api.md`.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the API test document by restoring
  required sections with manual-first guidance.
- **Files:**
  - `docs/infrastructure/api/TEST_Api.md`

### 2025-12-19: Clarify canonical playthrough algorithm location (repair 16)

- **What:** Noted in `ALGORITHM_Api.md` that it supersedes the deprecated playthrough algorithm alias.
- **Why:** Keep the canonical location explicit now that the legacy alias exists for backward references.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`

### 2025-12-19: Clean API PATTERNS duplication (repair 16)

- **What:** Removed the duplicate template block in `PATTERNS_Api.md` and
  replaced non-ASCII scope arrows with ASCII `->`.
- **Why:** Keep one authoritative pattern template while matching ASCII-first
  documentation constraints.
- **Files:**
  - `docs/infrastructure/api/PATTERNS_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Restore legacy playthrough algorithm alias (repair 16)

- **What:** Added `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
  with full template sections and a deprecation notice pointing to the
  canonical API algorithm doc.
- **Why:** The repair task targeted the legacy file; restoring it keeps older
  references functional while preserving `ALGORITHM_Api.md` as canonical.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`

### 2025-12-19: Expand API implementation template sections (repair 16)

- **What:** Added missing implementation template sections (code structure,
  design patterns, schema, entry points, data flow, logic chains, dependencies,
  state management, runtime behavior, concurrency model, configuration,
  bidirectional links, gaps) to `IMPLEMENTATION_Api.md`.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the API implementation doc and align
  the module with required template coverage.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Expand API behaviors template coverage (repair 16)

- **What:** Filled BEHAVIORS, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and GAPS sections in `BEHAVIORS_Api.md`.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for API behaviors documentation by restoring required sections with meaningful content.
- **Files:**
  - `docs/infrastructure/api/BEHAVIORS_Api.md`

### 2025-12-19: Expand playthrough creation sections in canonical algorithm doc (repair 16)

- **What:** Added playthrough creation sections (data structures, algorithm steps, decisions, data flow, complexity, helpers, interactions, gaps) to `ALGORITHM_Api.md`.
- **Why:** The previous playthrough-specific algorithm file was removed to avoid duplication; the canonical doc now holds the full template coverage.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`

### 2025-12-19: Re-verify API validation template completeness (repair 16)

- **What:** Reconfirmed `VALIDATION_Api.md` includes all required template sections and meets length guidance.
- **Why:** Close the repair loop with an explicit verification entry for the API validation doc.
- **Files:**
  - `docs/infrastructure/api/VALIDATION_Api.md`

### 2025-12-19: Normalize API PATTERNS content (repair 16)

- **What:** Removed the duplicate template block in `PATTERNS_Api.md` and kept
  a single, complete set of pattern sections.
- **Why:** Ensure the API patterns doc has one authoritative template instance.
- **Files:**
  - `docs/infrastructure/api/PATTERNS_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Fill API algorithm template sections (repair 16)

- **What:** Added overview, data structures, primary algorithm summary,
  key decisions, data flow, complexity, helper functions, interactions, and
  gaps sections to `ALGORITHM_Api.md`.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the API algorithm doc and align with
  required template headings.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`

### 2025-12-19: Expand API validation template sections (repair 16)

- **What:** Added invariants, properties, error conditions, test coverage, verification procedure, sync status, and gaps sections to the API validation doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for `VALIDATION_Api.md` and align with the validation template requirements.
- **Files:**
  - `docs/infrastructure/api/VALIDATION_Api.md`

### 2025-12-19: Fill missing SYNC template sections (repair 16)

- **What:** Added MATURITY, IN PROGRESS, KNOWN ISSUES, handoffs, TODO, consciousness trace, and pointers sections.
- **Why:** Resolve DOC_TEMPLATE_DRIFT warning for the API SYNC doc.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Fill API PATTERNS template sections (repair 16)

- **What:** Added missing problem, pattern, principles, dependencies,
  inspirations, scope, and gaps sections in `PATTERNS_Api.md`.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the API patterns document.
- **Files:**
  - `docs/infrastructure/api/PATTERNS_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Remove duplicate playthrough algorithm doc

- **What:** Deleted `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` so the API folder has a single canonical ALGORITHM doc.
- **Why:** The redirect file still counted as a duplicate ALGORITHM doc in the same folder, which triggers duplication warnings.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Reconfirm playthrough helper implementations (repair 01-INCOMPLETE_IMPL-api-playthroughs)

- **What:** Verified `_count_branches` and `create_scenario_playthrough` implementations; no code changes required.
- **Why:** Repair task flagged empty implementations; current code already provides real logic.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Align playthrough scenario creation to router implementation

- **What:** Added `/api/playthrough/scenario` alias in `engine/infrastructure/api/playthroughs.py` and removed the duplicate scenario endpoint in `engine/infrastructure/api/app.py`.
- **Why:** The frontend expects a `scene` payload from scenario creation, which the router provides; the app-level endpoint returned a different shape and caused a mismatch.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `engine/infrastructure/api/app.py`

### 2025-12-19: Remove unsupported energy argument when creating opening moments

- **What:** Dropped the `energy` argument passed to `GraphOps.add_moment()` when generating opening moments.
- **Why:** `GraphOps.add_moment()` does not accept `energy`, which raised an exception during playthrough creation and could stall the flow.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`

### 2025-12-19: Finish playthrough helper implementations

- **What:** Expanded discussion branch counting, added per-playthrough GraphQueries caching, and wired player moment embeddings to the embedding service with a safe fallback.
- **Why:** Repair task flagged incomplete helper implementations; these changes provide full logic without breaking moment creation when embeddings are unavailable.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Fix asyncio queue reference in API implementation doc

- **What:** Reworded the debug stream description to avoid `asyncio.Queue` being parsed as a file link.
- **Why:** Link validation flags `asyncio.Queue` as a missing file path.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Remove broken asyncio.Queue file reference

- **What:** Reworded the debug stream description to avoid a broken file reference for `asyncio.Queue`.
- **Why:** `ngram validate` treats `asyncio.Queue` as a file link; the target does not exist.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Map infrastructure API module and link DOCS reference

- **What:** Mapped `engine/infrastructure/api/**` to `docs/infrastructure/api/` in `modules.yaml` and added a `# DOCS:` header in `engine/infrastructure/api/app.py` for `ngram context`.
- **Why:** The API docs existed but the code path was not mapped, so documentation discovery failed for the API module.
- **Files:**
  - `modules.yaml`
  - `engine/infrastructure/api/app.py`

### 2025-12-19: Consolidate API algorithm documentation

- **What:** Merged playthrough creation flow into `docs/infrastructure/api/ALGORITHM_Api.md` and removed the duplicate algorithm file.
- **Why:** Remove duplicate ALGORITHM docs in the API folder and keep a single canonical algorithm reference.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Re-verify playthrough helpers for repair 01-INCOMPLETE_IMPL-api-playthroughs

- **What:** Confirmed `_count_branches` and `_get_playthrough_queries` in `engine/infrastructure/api/playthroughs.py` already contain real logic; no code changes required.
- **Why:** Repair task flagged empty implementations, but the functions are implemented.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Add /api/action endpoint and fix scenario path

- **What:** Added `POST /api/action` endpoint for full game loop. Fixed scenario path in playthroughs.py (was looking in `engine/scenarios` instead of project root `scenarios/`).
- **Why:** The action endpoint was missing - frontend click path had no way to trigger the full narrator/tick/flips loop. Scenario path was wrong due to incorrect parent traversal.
- **Files:**
  - `engine/infrastructure/api/app.py` — added `/api/action` endpoint
  - `engine/infrastructure/api/playthroughs.py` — fixed scenarios_dir path
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md` — documented new endpoints

### 2025-12-19: Verify playthroughs helper implementations (repair 01-INCOMPLETE_IMPL-api-playthroughs)

- **What:** Rechecked `_count_branches` and `_get_playthrough_queries` in `engine/infrastructure/api/playthroughs.py`; no code changes required.
- **Why:** Repair task flagged empty implementations, but the functions already contain logic.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Fill API helper implementations

- **What:** Implemented cached graph helpers, expanded health check, and hardened debug SSE payloads.
- **Why:** Replace incomplete helper stubs and provide meaningful health validation.
- **Files:**
  - `engine/infrastructure/api/app.py`
  - `docs/infrastructure/api/BEHAVIORS_Api.md`
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Verify playthroughs helper implementations

- **What:** Confirmed `_count_branches` and `_get_playthrough_queries` already contain real logic in the playthroughs router.
- **Why:** Repair task flagged them as incomplete, but the implementations are in place.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Re-validate playthroughs repair task

- **What:** Reconfirmed the playthroughs helpers are implemented; no code changes required for this repair run.
- **Why:** Task still flagged incomplete implementations, but the functions already perform real logic.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Reconfirm playthroughs helper implementations (repair 01)

- **What:** Verified `_count_branches` and `_get_playthrough_queries` are fully implemented; no code changes needed.
- **Why:** Repair task again flagged them as incomplete; verification confirms existing logic is intact.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Verify playthroughs helpers (repair 01-INCOMPLETE_IMPL-api-playthroughs)

- **What:** Confirmed `_count_branches` and `_get_playthrough_queries` in `engine/infrastructure/api/playthroughs.py` already contain real logic; no code changes required.
- **Why:** Repair task flagged empty implementations; verification shows they are implemented.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

---



---

## SOURCE: docs/infrastructure/api/VALIDATION_Api.md
# API — Validation

## INVARIANTS

- `GET /health` returns an ISO-8601 UTC timestamp so clients can compare clocks.
- `GET /health` returns `status=ok` only when both read and write graph connections succeed.
- Debug SSE events are serialized JSON strings so downstream consumers can parse them safely.
- Debug SSE clients are removed on disconnect or cancellation to avoid leaked queues.

## PROPERTIES

- The app factory returns a fully wired FastAPI instance with routers and shared dependencies attached once.
- Debug and gameplay streams are isolated; debug queue backpressure must not block gameplay delivery.
- Health checks are lightweight and should not mutate graph state or enqueue gameplay events.

## ERROR CONDITIONS

- Graph read failure returns `503` with `graph_read=error` details.
- Graph write failure returns `503` with `graph_write=error` details.
- Invalid request payloads trigger FastAPI validation errors (HTTP 422) with field-level messages.
- Debug stream keeps sending `ping` events when idle, but closes on cancellation or disconnect.

## TEST COVERAGE

- No dedicated API-only tests are documented; behavior is covered via manual smoke checks and shared engine integration tests.
- The engine test suite exercises downstream services, but does not assert API HTTP responses directly.

## VERIFICATION PROCEDURE

1. Start the API app and confirm `GET /health` returns `status=ok` with a UTC timestamp.
2. Open a debug SSE client and verify JSON payloads plus periodic `ping` events when idle.
3. Force a graph connection failure and confirm `503` responses include `graph_read`/`graph_write` error markers.

## SYNC STATUS

Validation notes align with `docs/infrastructure/api/SYNC_Api.md` and the current implementation doc chain as of 2025-12-19.

## GAPS / IDEAS / QUESTIONS

- [ ] Add explicit API integration tests that assert health and SSE behavior.
- IDEA: Document a reproducible smoke-test script for playthrough creation and action dispatch.
- QUESTION: Should validation include an auth-required health mode once gateway decisions are final?

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md


---

## SOURCE: engine/infrastructure/api/app.py
"""
Blood Ledger — FastAPI Application

Main API application with endpoints for:
- Scene generation and clicks
- View data (map, ledger, faces, chronicle)
- SSE for rolling window updates

Docs:
- docs/engine/moments/PATTERNS_Moments.md — architecture + rationale
- docs/engine/moments/API_Moments.md — HTTP contract for the moment graph

DOCS: docs/infrastructure/api/
"""

# DOCS: docs/infrastructure/api/

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, AsyncGenerator
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from engine.infrastructure.orchestration import Orchestrator
from engine.moment_graph import MomentTraversal, MomentQueries, MomentSurface
from engine.physics.graph import GraphQueries, GraphOps, add_mutation_listener
from engine.infrastructure.api.moments import create_moments_router
from engine.infrastructure.api.playthroughs import create_playthroughs_router
from engine.infrastructure.api.tempo import create_tempo_router

# =============================================================================
# LOGGING SETUP
# =============================================================================

_project_root = Path(__file__).parent.parent.parent
_log_dir = _project_root / "data" / "logs"
_log_dir.mkdir(parents=True, exist_ok=True)

# Configure file logging
_file_handler = logging.FileHandler(_log_dir / "backend.log")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
logging.getLogger().addHandler(_file_handler)

# Also log uvicorn access/errors
logging.getLogger("uvicorn").addHandler(_file_handler)
logging.getLogger("uvicorn.access").addHandler(_file_handler)
logging.getLogger("uvicorn.error").addHandler(_file_handler)

logger = logging.getLogger(__name__)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ActionRequest(BaseModel):
    """Request for a player action."""
    playthrough_id: str
    action: str
    player_id: str = "char_player"
    location: Optional[str] = None
    stream: bool = False  # If true, returns SSE stream instead of JSON


class SceneResponse(BaseModel):
    """Response containing a scene."""
    scene: Dict[str, Any]
    time_elapsed: str


class DialogueChunk(BaseModel):
    """A single chunk of streamed dialogue."""
    speaker: Optional[str] = None  # Character ID if dialogue, None for narration
    text: str


class NewPlaythroughRequest(BaseModel):
    """Request to create a new playthrough."""
    drive: str  # BLOOD, OATH, or SHADOW
    companion: str = "char_aldric"
    initial_goal: Optional[str] = None


class QueryRequest(BaseModel):
    """Request for semantic query."""
    query: str


# =============================================================================
# APPLICATION FACTORY
# =============================================================================

def create_app(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379,
    playthroughs_dir: str = "playthroughs"
) -> FastAPI:
    """
    Create the FastAPI application.

    Args:
        graph_name: FalkorDB graph name
        host: FalkorDB host
        port: FalkorDB port
        playthroughs_dir: Directory for playthrough data

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Blood Ledger API",
        description="API for The Blood Ledger narrative RPG",
        version="0.1.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Per-playthrough orchestrators
    _orchestrators: Dict[str, Orchestrator] = {}
    _debug_sse_clients: list = []  # list of queues for debug/mutation events
    _playthroughs_dir = Path(playthroughs_dir)
    _graph_queries: Optional[GraphQueries] = None
    _graph_ops: Optional[GraphOps] = None

    # Register mutation listener to broadcast to debug SSE clients
    def _mutation_event_handler(event: Dict[str, Any]):
        """Handle mutation events and broadcast to debug SSE clients."""
        for queue in _debug_sse_clients:
            try:
                queue.put_nowait(event)
            except:
                pass  # Queue full or closed

    add_mutation_listener(_mutation_event_handler)

    def get_orchestrator(playthrough_id: str) -> Orchestrator:
        """Get or create orchestrator for a playthrough."""
        if playthrough_id not in _orchestrators:
            _orchestrators[playthrough_id] = Orchestrator(
                playthrough_id=playthrough_id,
                graph_name=graph_name,
                host=host,
                port=port,
                playthroughs_dir=playthroughs_dir
            )
        return _orchestrators[playthrough_id]

    def get_graph_queries() -> GraphQueries:
        """Get graph queries instance for default graph."""
        nonlocal _graph_queries
        if _graph_queries is None:
            _graph_queries = GraphQueries(
                graph_name=graph_name,
                host=host,
                port=port
            )
        return _graph_queries

    def get_playthrough_queries(playthrough_id: str) -> GraphQueries:
        """Get graph queries instance for a specific playthrough."""
        from engine.physics.graph import get_playthrough_graph_name
        pt_graph_name = get_playthrough_graph_name(playthrough_id)
        return GraphQueries(graph_name=pt_graph_name, host=host, port=port)

    def get_moment_queries(playthrough_id: str) -> MomentQueries:
        """Get moment queries instance for a specific playthrough."""
        from engine.physics.graph import get_playthrough_graph_name
        pt_graph_name = get_playthrough_graph_name(playthrough_id)
        return MomentQueries(graph_name=pt_graph_name, host=host, port=port)

    def get_graph_ops() -> GraphOps:
        """Get graph ops instance."""
        nonlocal _graph_ops
        if _graph_ops is None:
            _graph_ops = GraphOps(graph_name=graph_name, host=host, port=port)
        return _graph_ops

    # =========================================================================
    # MOMENTS ROUTER (Moment Graph API)
    # =========================================================================

    # Mount the moments API router for moment graph operations
    # Endpoints: GET /api/moments/current, POST /api/moments/click, etc.
    moments_router = create_moments_router(
        host=host,
        port=port,
        playthroughs_dir=playthroughs_dir
    )
    app.include_router(moments_router, prefix="/api")

    # Mount the playthroughs API router for playthrough management
    # Endpoints: POST /api/playthrough/create, POST /api/moment, discussion trees
    playthroughs_router = create_playthroughs_router(
        graph_name=graph_name,
        host=host,
        port=port,
        playthroughs_dir=playthroughs_dir
    )
    app.include_router(playthroughs_router, prefix="/api")

    # Mount the tempo API router for game speed control
    # Endpoints: POST /api/tempo/speed, GET /api/tempo/{id}, POST /api/tempo/input
    tempo_router = create_tempo_router(
        host=host,
        port=port,
        playthroughs_dir=playthroughs_dir
    )
    app.include_router(tempo_router, prefix="/api")

    # =========================================================================
    # HEALTH CHECK
    # =========================================================================

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        timestamp = datetime.utcnow().isoformat()
        details = {
            "graph_read": "ok",
            "graph_write": "ok",
            "orchestrators": len(_orchestrators)
        }
        errors: Dict[str, str] = {}

        try:
            read = get_graph_queries()
            read.query("RETURN 1 AS ok")
        except Exception as exc:
            details["graph_read"] = "error"
            errors["graph_read"] = str(exc)

        try:
            get_graph_ops()
        except Exception as exc:
            details["graph_write"] = "error"
            errors["graph_write"] = str(exc)

        if errors:
            raise HTTPException(
                status_code=503,
                detail={
                    "status": "degraded",
                    "timestamp": timestamp,
                    "details": details,
                    "errors": errors
                }
            )

        return {"status": "ok", "timestamp": timestamp, "details": details}

    # =========================================================================
    # PLAYTHROUGH ENDPOINTS
    # =========================================================================

    @app.post("/api/playthrough")
    async def create_playthrough(request: NewPlaythroughRequest):
        """
        Create a new playthrough.

        Sets up playthrough directory for mutations and world injections.
        Player psychology tracked in narrator's conversation context.
        Story notes live in the graph (narrative.narrator_notes, tension.narrator_notes).
        """
        import uuid
        playthrough_id = f"pt_{uuid.uuid4().hex[:8]}"
        playthrough_dir = _playthroughs_dir / playthrough_id
        playthrough_dir.mkdir(parents=True, exist_ok=True)

        # Create mutations directory
        (playthrough_dir / "mutations").mkdir(exist_ok=True)

        # Initialize orchestrator
        get_orchestrator(playthrough_id)

        return {
            "playthrough_id": playthrough_id,
            "drive": request.drive,
            "companion": request.companion,
            "status": "created"
        }

    @app.post("/api/action")
    async def player_action(request: ActionRequest):
        """
        Full game loop: narrator -> tick -> flips -> world runner.

        This is the main endpoint for player actions after the initial
        instant-response click path (/api/moment/click).
        """
        try:
            orchestrator = get_orchestrator(request.playthrough_id)
            result = orchestrator.process_action(
                player_action=request.action,
                player_id=request.player_id,
                player_location=request.location
            )
            return result
        except Exception as e:
            logger.error(f"Action processing failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/playthrough/{playthrough_id}")
    async def get_playthrough(playthrough_id: str):
        """Get playthrough status and info."""
        playthrough_dir = _playthroughs_dir / playthrough_id
        if not playthrough_dir.exists():
            raise HTTPException(status_code=404, detail="Playthrough not found")

        return {
            "playthrough_id": playthrough_id,
            "has_world_injection": (playthrough_dir / "world_injection.md").exists()
        }

    # =========================================================================
    # MOMENT GRAPH ENDPOINTS
    # =========================================================================

    class MomentClickRequest(BaseModel):
        """Request for clicking a word using Moment Graph architecture."""
        playthrough_id: str
        moment_id: str
        word: str
        player_id: str = "char_player"

    class MomentClickResponse(BaseModel):
        """Response for Moment Graph click."""
        flipped: bool
        flipped_moments: list
        weight_updates: list
        queue_narrator: bool

    @app.post("/api/moment/click", response_model=MomentClickResponse)
    async def moment_click(request: MomentClickRequest):
        """
        Handle a word click using the Moment Graph architecture.

        This is the instant-response path (<50ms target).
        No LLM calls in this path.

        1. Find CAN_LEAD_TO links from moment where word is in require_words
        2. Apply weight_transfer to target moments
        3. Check for flips (weight > 0.8)
        4. Return flipped moments, or queue_narrator=True if nothing flips
        """
        try:
            ops = get_graph_ops()
            result = ops.handle_click(
                moment_id=request.moment_id,
                clicked_word=request.word,
                player_id=request.player_id
            )
            return MomentClickResponse(**result)
        except Exception as e:
            logger.error(f"Moment click failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/moment/view/{playthrough_id}")
    async def get_moment_view(
        playthrough_id: str,
        location_id: str = Query(..., description="Current location ID"),
        player_id: str = Query("char_player", description="Player character ID")
    ):
        """
        Get the current view using Moment Graph architecture.

        Returns moments visible to player at location, ordered by weight.
        This replaces scene.json reads with live graph queries.
        """
        try:
            queries = get_playthrough_queries(playthrough_id)
            read = get_moment_queries(playthrough_id)
            
            # Resolve present characters at the location
            present = queries.get_characters_at(location_id)
            present_ids = [c['id'] for c in present]
            
            view = read.get_current_view(
                player_id=player_id,
                location_id=location_id,
                present_chars=present_ids
            )
            return view
        except Exception as e:
            logger.error(f"Get moment view failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/view/{playthrough_id}")
    async def get_current_view(
        playthrough_id: str,
        player_id: str = Query("char_player", description="Player character ID"),
        location_id: Optional[str] = Query(
            None,
            description="Override location ID; defaults to player's current AT edge"
        )
    ):
        """
        Resolve the player's current location (unless overridden) and return the
        CurrentView payload described in docs/engine/moments/API_Moments.md.
        """
        try:
            queries = get_playthrough_queries(playthrough_id)
            moments = get_moment_queries(playthrough_id)
            
            resolved_location_id = location_id
            if not resolved_location_id:
                location = queries.get_player_location(player_id=player_id)
                if not location:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Player '{player_id}' has no AT link. Move the player before requesting view."
                    )
                resolved_location_id = location.get("id")

            # Get present characters
            present = queries.get_characters_at(resolved_location_id)
            present_ids = [c['id'] for c in present]

            view = moments.get_current_view(
                player_id=player_id,
                location_id=resolved_location_id,
                present_chars=present_ids
            )

            return view
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get current view failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/moment/view/{playthrough_id}/scene-tree")
    async def get_moment_view_as_scene_tree(
        playthrough_id: str,
        location_id: str = Query(..., description="Current location ID"),
        player_id: str = Query("char_player", description="Player character ID")
    ):
        """
        Get the current view as a SceneTree for backward compatibility.

        Fetches from Moment Graph but converts to SceneTree format
        so existing frontend components work unchanged.
        """
        try:
            from engine.physics.graph.graph_queries import view_to_scene_tree

            read = get_playthrough_queries(playthrough_id)
            view = read.get_current_view(
                player_id=player_id,
                location_id=location_id
            )
            scene_tree = view_to_scene_tree(view)
            return {"scene": scene_tree}
        except Exception as e:
            logger.error(f"Get scene tree failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/moment/weight")
    async def update_moment_weight(request: Request):
        """
        Manually update a moment's weight.

        Request body: {"moment_id": "...", "weight_delta": 0.2, "reason": "..."}
        """
        try:
            body = await request.json()
            ops = get_graph_ops()
            result = ops.update_moment_weight(
                moment_id=body.get("moment_id"),
                weight_delta=body.get("weight_delta", 0.0),
                reason=body.get("reason", "api_call")
            )
            return result
        except Exception as e:
            logger.error(f"Weight update failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # DEBUG SSE ENDPOINT (Graph Mutations)
    # =========================================================================

    @app.get("/api/debug/stream")
    async def debug_stream(request: Request):
        """
        SSE endpoint for graph mutation events.

        Clients connect here to receive real-time updates when mutations are applied.
        Events include: apply_start, node_created, link_created, movement, apply_complete

        Use this for the debug panel in the frontend.
        """
        async def event_generator() -> AsyncGenerator[str, None]:
            queue = asyncio.Queue(maxsize=100)

            # Register this client
            _debug_sse_clients.append(queue)

            try:
                # Send initial connection event
                yield f"event: connected\ndata: {{\"message\": \"Debug stream connected\"}}\n\n"

                while True:
                    # Check if client disconnected
                    if await request.is_disconnected():
                        break

                    try:
                        # Wait for events with timeout
                        event = await asyncio.wait_for(queue.get(), timeout=30)
                        event_type = event.get('type', 'mutation')
                        payload = json.dumps(event, default=str)
                        yield f"event: {event_type}\ndata: {payload}\n\n"
                    except asyncio.TimeoutError:
                        # Send keepalive
                        yield f"event: ping\ndata: {{}}\n\n"
                    except asyncio.CancelledError:
                        break
            finally:
                # Unregister client
                if queue in _debug_sse_clients:
                    _debug_sse_clients.remove(queue)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    # =========================================================================
    # VIEW ENDPOINTS
    # =========================================================================

    @app.get("/api/{playthrough_id}/map")
    async def get_map(playthrough_id: str, player_id: str = "char_player"):
        """
        Get map data showing places and connections.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get all places
            places = read.query("""
                MATCH (p:Place)
                RETURN p.id, p.name, p.type, p.mood
            """)

            # Get connections
            connections = read.query("""
                MATCH (p1:Place)-[r:CONNECTS]->(p2:Place)
                WHERE r.path > 0.5
                RETURN p1.id, p2.id, r.path_distance, r.path_difficulty
            """)

            # Get player location
            player_loc = read.query(f"""
                MATCH (c:Character {{id: '{player_id}'}})-[:AT]->(p:Place)
                RETURN p.id
            """)

            # Handle dict results from FalkorDB
            player_location = None
            if player_loc and player_loc[0]:
                if isinstance(player_loc[0], dict):
                    player_location = player_loc[0].get('p.id')
                else:
                    player_location = player_loc[0][0]

            return {
                "places": places,
                "connections": connections,
                "player_location": player_location
            }
        except Exception as e:
            logger.error(f"Failed to get map: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/ledger")
    async def get_ledger(playthrough_id: str, player_id: str = "char_player"):
        """
        Get ledger data showing debts, oaths, and blood ties.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get core narratives (oath, debt, blood) that player believes
            ledger_items = read.query(f"""
                MATCH (c:Character {{id: '{player_id}'}})-[b:BELIEVES]->(n:Narrative)
                WHERE n.type IN ['oath', 'debt', 'blood', 'enmity']
                  AND b.heard > 0.5
                RETURN n.id, n.name, n.content, n.type, n.tone, b.believes
                ORDER BY b.believes DESC
            """)

            return {"items": ledger_items}
        except Exception as e:
            logger.error(f"Failed to get ledger: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/faces")
    async def get_faces(playthrough_id: str, player_id: str = "char_player"):
        """
        Get faces data showing known characters.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get characters the player knows about (major characters and those in narratives)
            # Note: about_characters is stored as JSON string, so we use a simpler query
            characters = read.query("""
                MATCH (c:Character)
                WHERE c.type IN ['major', 'minor'] AND c.type <> 'player'
                RETURN DISTINCT c.id, c.name, c.type, c.face
            """)

            # Get companion info
            companions = read.query("""
                MATCH (c:Character {type: 'companion'})
                RETURN c.id, c.name, c.face, c.voice_tone
            """)

            return {
                "known_characters": characters,
                "companions": companions
            }
        except Exception as e:
            logger.error(f"Failed to get faces: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/chronicle")
    async def get_chronicle(playthrough_id: str, player_id: str = "char_player"):
        """
        Get chronicle data showing event history.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get memory and account narratives the player believes
            events = read.query(f"""
                MATCH (c:Character {{id: '{player_id}'}})-[b:BELIEVES]->(n:Narrative)
                WHERE n.type IN ['memory', 'account']
                  AND b.heard > 0.5
                RETURN n.id, n.name, n.content, n.type, n.tone, b.believes
                ORDER BY n.weight DESC
                LIMIT 50
            """)

            return {"events": events}
        except Exception as e:
            logger.error(f"Failed to get chronicle: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # QUERY ENDPOINT
    # =========================================================================

    @app.post("/api/{playthrough_id}/query")
    async def semantic_query_post(playthrough_id: str, request: QueryRequest):
        """
        Natural language query via embeddings (POST).
        """
        try:
            from engine.world.map import get_semantic_search
            search = get_semantic_search(graph_name=graph_name, host=host, port=port)
            results = search.find(request.query, limit=10)
            return {"results": results, "query": request.query}
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/query")
    async def semantic_query_get(playthrough_id: str, query: str = Query(..., description="Search query")):
        """
        Natural language query via embeddings (GET).
        """
        try:
            from engine.world.map import get_semantic_search
            search = get_semantic_search(graph_name=graph_name, host=host, port=port)
            results = search.find(query, limit=10)
            return {"results": results, "query": query}
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # INJECTION ENDPOINT
    # =========================================================================

    @app.post("/api/inject")
    async def inject_event(request: Request):
        """
        Write an injection to the queue for hook processing.
        Used by frontend for player UI actions (stop, location change, etc.)
        """
        try:
            body = await request.json()
            injection_file = _playthroughs_dir / "default" / "injection_queue.jsonl"
            injection_file.parent.mkdir(parents=True, exist_ok=True)

            with open(injection_file, "a") as f:
                f.write(json.dumps(body) + "\n")

            return {"status": "ok", "injection": body}
        except Exception as e:
            logger.error(f"Failed to inject: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

# Use absolute path to project root's playthroughs directory
_project_root = Path(__file__).parent.parent.parent
_default_playthroughs = str(_project_root / "playthroughs")

app = create_app(playthroughs_dir=_default_playthroughs)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


---

## SOURCE: engine/infrastructure/api/moments.py
"""
Blood Ledger — Moment Graph API Endpoints

Fast endpoints for moment graph traversal and queries.
The click path is HOT - must be <50ms, no LLM calls.

Docs:
- docs/engine/UI_API_CHANGES_Moment_Graph.md — full API specification
- docs/engine/IMPL_PHASE_1_Moment_Graph.md — implementation guide
"""

import asyncio
import json
import logging
from typing import List, Optional, Dict, Any, AsyncGenerator
from pathlib import Path

import yaml

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from engine.moment_graph import MomentTraversal, MomentQueries, MomentSurface
from engine.physics.graph import GraphQueries, get_playthrough_graph_name
from .sse_broadcast import (
    broadcast_moment_event,
    register_sse_client,
    unregister_sse_client,
    get_sse_clients
)

logger = logging.getLogger(__name__)


def _resolve_graph_name(playthrough_id: str, playthroughs_dir: Optional[Path]) -> str:
    """Resolve the graph name for a playthrough, honoring configured directories."""
    if playthroughs_dir:
        player_file = playthroughs_dir / playthrough_id / "player.yaml"
        if player_file.exists():
            try:
                data = yaml.safe_load(player_file.read_text()) or {}
                graph_name = data.get("graph_name")
                if graph_name:
                    return graph_name
            except Exception as exc:
                logger.warning(f"Failed to read graph name for {playthrough_id}: {exc}")
    return get_playthrough_graph_name(playthrough_id)


def _get_queries(
    playthrough_id: str,
    host: str,
    port: int,
    playthroughs_dir: Optional[Path] = None
) -> MomentQueries:
    """Get MomentQueries for a specific playthrough."""
    graph_name = _resolve_graph_name(playthrough_id, playthroughs_dir)
    return MomentQueries(graph_name=graph_name, host=host, port=port)


def _get_traversal(
    playthrough_id: str,
    host: str,
    port: int,
    playthroughs_dir: Optional[Path] = None
) -> MomentTraversal:
    """Get MomentTraversal for a specific playthrough."""
    graph_name = _resolve_graph_name(playthrough_id, playthroughs_dir)
    return MomentTraversal(graph_name=graph_name, host=host, port=port)


def _get_surface(
    playthrough_id: str,
    host: str,
    port: int,
    playthroughs_dir: Optional[Path] = None
) -> MomentSurface:
    """Get MomentSurface for a specific playthrough."""
    graph_name = _resolve_graph_name(playthrough_id, playthroughs_dir)
    return MomentSurface(graph_name=graph_name, host=host, port=port)


def _get_graph_queries(
    playthrough_id: str,
    host: str,
    port: int,
    playthroughs_dir: Optional[Path] = None
) -> GraphQueries:
    """Get GraphQueries for a specific playthrough."""
    graph_name = _resolve_graph_name(playthrough_id, playthroughs_dir)
    return GraphQueries(graph_name=graph_name, host=host, port=port)

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class MomentResponse(BaseModel):
    """A moment from the graph."""
    id: str
    text: str
    type: str
    status: str
    weight: float
    tone: Optional[str] = None
    tick_created: int = 0
    tick_spoken: Optional[int] = None
    speaker: Optional[str] = None  # From SAID link
    clickable_words: List[str] = Field(default_factory=list)


class TransitionResponse(BaseModel):
    """A CAN_LEAD_TO link."""
    from_id: str
    to_id: str
    trigger: str
    require_words: List[str] = Field(default_factory=list)
    weight_transfer: float = 0.3
    consumes_origin: bool = True


class CurrentMomentsResponse(BaseModel):
    """Response for GET /moments/current."""
    location: Optional[Dict[str, Any]] = None
    characters: List[Dict[str, Any]] = Field(default_factory=list)
    things: List[Dict[str, Any]] = Field(default_factory=list)
    moments: List[MomentResponse]
    transitions: List[TransitionResponse]
    active_count: int


class ClickRequest(BaseModel):
    """Request for clicking a word in a moment."""
    playthrough_id: str
    moment_id: str
    word: str
    tick: int


class ClickResponse(BaseModel):
    """Response for clicking a word."""
    status: str  # ok, no_match, error
    traversed: bool
    target_moment: Optional[MomentResponse] = None
    consumed_origin: bool = False
    new_active_moments: List[MomentResponse] = Field(default_factory=list)


class SurfaceRequest(BaseModel):
    """Request to manually surface a moment."""
    moment_id: str
    playthrough_id: str


# =============================================================================
# ROUTER
# =============================================================================

def create_moments_router(
    host: str = "localhost",
    port: int = 6379,
    playthroughs_dir: str = "playthroughs"
) -> APIRouter:
    """
    Create the moments API router.

    This is mounted in app.py as /api/moments.
    Each playthrough uses its own graph (graph_name = playthrough_id).
    """
    router = APIRouter(prefix="/moments", tags=["moments"])

    # Store config for creating per-playthrough instances
    _host = host
    _port = port
    _playthroughs_dir = Path(playthroughs_dir)

    # SSE client management now uses shared sse_broadcast module
    # broadcast_moment_event, register_sse_client, unregister_sse_client imported from sse_broadcast

    # =========================================================================
    # GET CURRENT MOMENTS
    # =========================================================================

    @router.get("/current/{playthrough_id}", response_model=CurrentMomentsResponse)
    async def get_current_moments(
        playthrough_id: str,
        player_id: str = Query("char_player"),
        location: str = Query(None),
        present_chars: str = Query(None),  # Comma-separated
        present_things: str = Query(None)  # Comma-separated
    ):
        """
        Get visible moments for the current scene.

        Based on player location and present entities.
        Returns active/possible moments and their transitions.
        """
        # Parse comma-separated lists
        chars = present_chars.split(",") if present_chars else []
        things = present_things.split(",") if present_things else []

        # Get playthrough-specific instances
        queries = _get_queries(playthrough_id, _host, _port, _playthroughs_dir)

        # If no location, try to get player's current location
        if not location:
            try:
                read = _get_graph_queries(playthrough_id, _host, _port, _playthroughs_dir)
                result = read.query(f"""
                    MATCH (c:Character {{id: '{player_id}'}})-[:AT]->(p:Place)
                    WHERE EXISTS((c)-[:AT {{present: 1.0}}]->(p))
                    RETURN p.id
                """)
                location = result[0][0] if result else "place_unknown"
            except Exception as e:
                logger.warning(f"Could not get player location: {e}")
                location = "place_unknown"

        try:
            # Get current view from queries
            view = queries.get_current_view(
                player_id=player_id,
                location_id=location,
                present_chars=chars,
                present_things=things
            )

            # Convert to response models
            moments = []
            for m in view.get("moments", []):
                # Get clickable words from transitions
                clickable = []
                for t in view.get("transitions", []):
                    if t["from_id"] == m["id"]:
                        clickable.extend(t.get("require_words", []))

                moments.append(MomentResponse(
                    id=m["id"],
                    text=m.get("text", ""),
                    type=m.get("type", "narration"),
                    status=m.get("status", "possible"),
                    weight=m.get("weight", 0.5),
                    tone=m.get("tone"),
                    tick_created=m.get("tick_created", 0),
                    tick_spoken=m.get("tick_spoken"),
                    speaker=m.get("speaker"),
                    clickable_words=list(set(clickable))
                ))

            transitions = [
                TransitionResponse(
                    from_id=t["from_id"],
                    to_id=t["to_id"],
                    trigger=t.get("trigger", "click"),
                    require_words=t.get("require_words", []),
                    weight_transfer=t.get("weight_transfer", 0.3),
                    consumes_origin=t.get("consumes_origin", True)
                )
                for t in view.get("transitions", [])
            ]

            return CurrentMomentsResponse(
                location=view.get("location"),
                characters=view.get("characters", []),
                things=view.get("things", []),
                moments=moments,
                transitions=transitions,
                active_count=view.get("active_count", 0)
            )

        except Exception as e:
            logger.error(f"get_current_moments failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # CLICK (HOT PATH)
    # =========================================================================

    @router.post("/click", response_model=ClickResponse)
    async def click_word(request: ClickRequest):
        """
        Handle player clicking a word in a moment.

        THIS IS THE HOT PATH - must complete in <50ms.
        No LLM calls. Pure graph traversal.
        """
        try:
            # Get playthrough-specific traversal instance
            traversal = _get_traversal(request.playthrough_id, _host, _port, _playthroughs_dir)

            # Traverse the graph
            result = traversal.handle_click(
                moment_id=request.moment_id,
                word=request.word,
                tick=request.tick,
                player_id="char_player"
            )

            if not result:
                return ClickResponse(
                    status="no_match",
                    traversed=False,
                    consumed_origin=False
                )

            # Get any newly activated moments
            # (For now, just return the target)
            target = MomentResponse(
                id=result["id"],
                text=result.get("text", ""),
                type=result.get("type", "narration"),
                status="active",
                weight=result.get("weight", 0.5),
                tone=result.get("tone"),
                clickable_words=result.get("require_words", [])
            )

            # Broadcast click event to SSE clients
            broadcast_moment_event(request.playthrough_id, "click_traversed", {
                "from_moment_id": request.moment_id,
                "to_moment_id": result["id"],
                "word": request.word,
                "consumed_origin": result.get("consumes_origin", True)
            })

            # Broadcast activation event
            broadcast_moment_event(request.playthrough_id, "moment_activated", {
                "moment_id": result["id"],
                "weight": result.get("weight", 0.5),
                "text": result.get("text", "")
            })

            return ClickResponse(
                status="ok",
                traversed=True,
                target_moment=target,
                consumed_origin=result.get("consumes_origin", True),
                new_active_moments=[target]
            )

        except Exception as e:
            logger.error(f"click_word failed: {e}")
            return ClickResponse(
                status="error",
                traversed=False,
                consumed_origin=False
            )

    # =========================================================================
    # STATS (DEBUG) - Must be before /{moment_id} to avoid route collision
    # =========================================================================

    @router.get("/stats/{playthrough_id}")
    async def get_moment_stats(playthrough_id: str):
        """
        Get moment statistics (debug endpoint).

        Returns counts by status.
        """
        try:
            surface = _get_surface(playthrough_id, _host, _port, _playthroughs_dir)
            stats = surface.get_surface_stats()
            return {"stats": stats}
        except Exception as e:
            logger.error(f"get_moment_stats failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # SURFACE (ADMIN/DEBUG)
    # =========================================================================

    @router.post("/surface")
    async def surface_moment(request: SurfaceRequest):
        """
        Manually surface a moment (for testing/admin).

        Sets the moment's status to 'active' and weight to 1.0.
        """
        try:
            surface = _get_surface(request.playthrough_id, _host, _port, _playthroughs_dir)
            traversal = _get_traversal(request.playthrough_id, _host, _port, _playthroughs_dir)

            surface.set_moment_weight(request.moment_id, 1.0)
            traversal.activate_moment(request.moment_id, tick=0)

            return {"status": "ok", "moment_id": request.moment_id}

        except Exception as e:
            logger.error(f"surface_moment failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # SSE STREAM
    # =========================================================================

    @router.get("/stream/{playthrough_id}")
    async def moment_stream(request: Request, playthrough_id: str):
        """
        SSE endpoint for real-time moment updates.

        Events:
        - moment_activated: A moment became active (weight >= 0.8)
        - moment_spoken: A moment was spoken
        - moment_decayed: A moment decayed (weight < 0.1)
        - weight_updated: A moment's weight changed
        - click_traversed: A click traversal occurred

        Connect: GET /api/moments/stream/{playthrough_id}
        """
        async def event_generator() -> AsyncGenerator[str, None]:
            queue: asyncio.Queue = asyncio.Queue(maxsize=100)

            # Register this client using shared module
            register_sse_client(playthrough_id, queue)

            try:
                # Send initial connection event
                yield f"event: connected\ndata: {{\"playthrough_id\": \"{playthrough_id}\"}}\n\n"

                while True:
                    # Check if client disconnected
                    if await request.is_disconnected():
                        break

                    try:
                        # Wait for events with timeout (for keepalive)
                        event = await asyncio.wait_for(queue.get(), timeout=30)
                        event_type = event.get("type", "update")
                        event_data = json.dumps(event.get("data", {}))
                        yield f"event: {event_type}\ndata: {event_data}\n\n"
                    except asyncio.TimeoutError:
                        # Send keepalive ping
                        yield f"event: ping\ndata: {{}}\n\n"

            finally:
                # Unregister client using shared module
                unregister_sse_client(playthrough_id, queue)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )

    # =========================================================================
    # GET SINGLE MOMENT
    # =========================================================================

    @router.get("/{playthrough_id}/{moment_id}")
    async def get_moment(playthrough_id: str, moment_id: str):
        """
        Get a single moment by ID with full details.

        Includes attachments, speakers, and transitions.
        """
        try:
            queries = _get_queries(playthrough_id, _host, _port, _playthroughs_dir)
            moment = queries.get_moment_by_id(moment_id)

            if not moment:
                raise HTTPException(status_code=404, detail="Moment not found")

            # TODO: Add attachments, speakers, transitions
            return moment

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"get_moment failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # Expose broadcast function for use by other modules
    router.broadcast_moment_event = broadcast_moment_event

    return router


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def get_moments_router(
    host: str = "localhost",
    port: int = 6379,
    playthroughs_dir: str = "playthroughs"
) -> APIRouter:
    """Get the moments router with default config."""
    return create_moments_router(
        host=host,
        port=port,
        playthroughs_dir=playthroughs_dir
    )


---

## SOURCE: engine/infrastructure/api/playthroughs.py
"""
Blood Ledger — Playthrough Management API Endpoints

Endpoints for creating and managing playthroughs, sending player moments,
and discussion tree navigation.

Extracted from app.py to reduce file size.

Docs:
- DOCS: docs/infrastructure/api/
- docs/physics/IMPLEMENTATION_Physics.md — code architecture
- docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md — async queues + injection flow
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from engine.physics.graph import GraphQueries, get_playthrough_graph_name

logger = logging.getLogger(__name__)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class PlaythroughCreateRequest(BaseModel):
    """Request to create a new playthrough."""
    scenario_id: str
    player_name: str
    player_gender: str = "male"


class MomentRequest(BaseModel):
    """Request to send a player moment."""
    playthrough_id: str
    text: str
    moment_type: str = "player_freeform"  # player_freeform, player_click, player_choice


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _opening_to_scene_tree(opening_template: dict, scenario: dict) -> dict:
    """
    Convert opening.json template to SceneTree format with nested freeform_acknowledgment.
    """
    setting = opening_template.get("setting", {})
    beats = opening_template.get("beats", [])
    companion_id = scenario.get("companion", {}).get("id", "char_aldric")

    # Build nested narration from beats
    def build_beat_narration(beat_index: int) -> list:
        """Recursively build narration for a beat with freeform_acknowledgment linking to next."""
        if beat_index >= len(beats):
            return []

        beat = beats[beat_index]
        narration_lines = beat.get("narration", [])
        questions = beat.get("questions", [])

        result = []

        # Add narration lines
        for line in narration_lines:
            # Check if it's dialogue (starts with quote)
            if line.startswith('"'):
                result.append({
                    "text": line,
                    "speaker": companion_id
                })
            else:
                result.append({"text": line})

        # Add questions with freeform_acknowledgment
        for i, question in enumerate(questions):
            is_last_question_of_beat = (i == len(questions) - 1)
            is_last_beat = (beat_index == len(beats) - 1)

            q_narration = {
                "text": question.get("text", ""),
                "speaker": question.get("speaker", companion_id)
            }

            # Add transition if present
            if question.get("transition"):
                result.append({"text": question["transition"]})

            # Build freeform_acknowledgment
            if question.get("type") == "statement":
                # Statements don't need acknowledgment text, just continue
                ack = {"text": ""}
            else:
                # Regular questions get acknowledgment
                ack = {"text": "He nods slowly."}

            # Link to next content
            if is_last_question_of_beat and not is_last_beat:
                # Link to next beat
                ack["then"] = build_beat_narration(beat_index + 1)
            elif not is_last_question_of_beat:
                # Link to next question in same beat (continue with remaining questions)
                remaining_questions = questions[i+1:]
                if remaining_questions:
                    next_q = remaining_questions[0]
                    ack["then"] = [{
                        "text": next_q.get("text", ""),
                        "speaker": next_q.get("speaker", companion_id),
                        "freeform_acknowledgment": {
                            "text": "He nods slowly.",
                            "then": build_beat_narration(beat_index + 1) if is_last_question_of_beat else []
                        }
                    }]

            q_narration["freeform_acknowledgment"] = ack
            result.append(q_narration)
            break  # Only add first question, rest are in nested then

        return result

    # Build the scene tree
    scene = {
        "id": "opening_fireside",
        "location": {
            "place": setting.get("location", "camp_roadside"),
            "name": "Roadside Camp",
            "region": "The North Road",
            "time": setting.get("time", "night")
        },
        "characters": setting.get("characters", ["char_aldric"]),
        "atmosphere": setting.get("atmosphere", []),
        "narration": build_beat_narration(0),
        "voices": []
    }

    return scene


def _count_branches(topics: list) -> int:
    """Count total unexplored branches across all topics."""
    def count_clickables(node: Any) -> int:
        if not isinstance(node, dict):
            return 0

        clickable = node.get("clickable")
        if not isinstance(clickable, dict) or not clickable:
            return 0

        total = 0
        for branch in clickable.values():
            response = branch.get("response") if isinstance(branch, dict) else None
            if isinstance(response, dict):
                branch_total = count_clickables(response)
                total += branch_total if branch_total > 0 else 1
            else:
                total += 1
        return total

    return sum(count_clickables(topic.get("opener", {})) for topic in topics)


def _delete_branch(topic: dict, branch_path: list):
    """Delete a branch from a topic tree."""
    if not branch_path:
        return

    # Navigate to parent of branch to delete
    current = topic.get("opener", {})
    for word in branch_path[:-1]:
        clickable = current.get("clickable", {})
        if word in clickable:
            current = clickable[word].get("response", {})
        else:
            return  # Path not found

    # Delete the final branch
    clickable = current.get("clickable", {})
    if branch_path[-1] in clickable:
        del clickable[branch_path[-1]]


# =============================================================================
# ROUTER
# =============================================================================

def create_playthroughs_router(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379,
    playthroughs_dir: str = "playthroughs"
) -> APIRouter:
    """
    Create the playthroughs API router.

    This is mounted in app.py as /api.
    Handles playthrough creation, moment sending, and discussion trees.
    """
    router = APIRouter(tags=["playthroughs"])

    # Store config
    _host = host
    _port = port
    _graph_name = graph_name
    _playthroughs_dir = Path(playthroughs_dir)
    _queries_cache: Dict[str, GraphQueries] = {}

    def _get_playthrough_queries(playthrough_id: str) -> GraphQueries:
        """Get graph queries instance for a specific playthrough."""
        if playthrough_id not in _queries_cache:
            pt_graph_name = get_playthrough_graph_name(playthrough_id) or _graph_name
            _queries_cache[playthrough_id] = GraphQueries(
                graph_name=pt_graph_name,
                host=_host,
                port=_port
            )
        return _queries_cache[playthrough_id]

    # =========================================================================
    # PLAYTHROUGH CREATION
    # =========================================================================

    @router.post("/playthrough/create")
    async def create_playthrough(request: PlaythroughCreateRequest):
        """
        Create a new playthrough:
        1. Create playthrough directory
        2. Save player.yaml
        3. Inject scenario nodes/links into graph
        4. Generate scene.json from opening.json template
        5. Return scene for frontend to display
        """
        import re
        import yaml
        from engine.physics.graph.graph_ops import GraphOps

        # Generate playthrough ID from player name
        # Slugify: lowercase, replace spaces/special chars with underscore
        base_id = re.sub(r'[^a-z0-9]+', '_', request.player_name.lower()).strip('_')
        if not base_id:
            base_id = "player"

        # Find unique ID (add number suffix if duplicate exists)
        playthrough_id = base_id
        counter = 2
        while (_playthroughs_dir / playthrough_id).exists():
            playthrough_id = f"{base_id}_{counter}"
            counter += 1

        playthrough_dir = _playthroughs_dir / playthrough_id
        playthrough_dir.mkdir(parents=True, exist_ok=True)
        (playthrough_dir / "mutations").mkdir(exist_ok=True)
        (playthrough_dir / "conversations").mkdir(exist_ok=True)

        # 1. Save player.yaml (includes graph_name for other endpoints)
        player_data = {
            "name": request.player_name,
            "gender": request.player_gender,
            "scenario": request.scenario_id,
            "graph_name": playthrough_id,  # Graph name = playthrough_id for isolation
            "created_at": datetime.utcnow().isoformat()
        }
        (playthrough_dir / "player.yaml").write_text(yaml.dump(player_data))

        # 2. Load and inject scenario
        scenarios_dir = Path(__file__).parent.parent.parent.parent / "scenarios"
        scenario_file = scenarios_dir / f"{request.scenario_id}.yaml"

        if not scenario_file.exists():
            raise HTTPException(status_code=404, detail=f"Scenario not found: {request.scenario_id}")

        scenario = yaml.safe_load(scenario_file.read_text())

        # Use playthrough_id as graph name for isolation
        playthrough_graph_name = playthrough_id

        # Initialize new graph with seed data
        try:
            from engine.init_db import load_initial_state
            logger.info(f"Initializing graph {playthrough_graph_name} with seed data...")
            load_initial_state(playthrough_graph_name, _host, _port)
            logger.info(f"Seed data loaded for {playthrough_graph_name}")
        except Exception as e:
            logger.error(f"Failed to load seed data: {e}")
            # Continue anyway - scenario may still work

        # Inject scenario nodes and links into graph
        try:
            graph = GraphOps(graph_name=playthrough_graph_name, host=_host, port=_port)

            # Build injection data from scenario
            inject_data = {
                "nodes": scenario.get("nodes", []),
                "links": scenario.get("links", [])
            }

            # Update player name/gender in player node if present
            for node in inject_data["nodes"]:
                if node.get("id") == "char_player":
                    node["name"] = request.player_name
                    node["gender"] = request.player_gender

            if inject_data["nodes"] or inject_data["links"]:
                result = graph.apply(data=inject_data, playthrough=playthrough_id)
                logger.info(f"Scenario injected: {len(result.persisted)} items, {len(result.errors)} errors")
                if result.errors:
                    for err in result.errors[:5]:
                        logger.warning(f"  Injection error: {err}")
        except Exception as e:
            logger.error(f"Failed to inject scenario: {e}")

        # 3. Create opening moments from scenario
        try:
            opening = scenario.get("opening", {})
            opening_narration = opening.get("narration", "")
            location_id = scenario.get("location", "place_camp")

            if opening_narration:
                # Split narration into lines and create moments
                lines = [line.strip() for line in opening_narration.strip().split("\n") if line.strip()]
                previous_moment_id = None
                for i, line in enumerate(lines):
                    moment_id = f"opening_{playthrough_id[:8]}_{i}"
                    
                    # Resolve speaker if line starts with quote
                    speaker = None
                    if line.startswith('"') and companion_id:
                        speaker = companion_id
                        line = line.strip('"')

                    graph.add_moment(
                        id=moment_id,
                        text=line,
                        type="dialogue" if speaker else "narration",
                        speaker=speaker,
                        tick=0,
                        place_id=location_id,
                        status="active", # Mark as active so they surface immediately
                        weight=1.0 - (i * 0.01) # Slight weight gradient for ordering
                    )
                    
                    # Create ATTACHED_TO link to location (presence_required=false for opening)
                    graph.query(
                        """
                        MATCH (m:Moment {id: $moment_id}), (p:Place {id: $place_id})
                        MERGE (m)-[:ATTACHED_TO {presence_required: false, persistent: false}]->(p)
                        """,
                        params={"moment_id": moment_id, "place_id": location_id}
                    )
                    
                    # Link to previous moment via THEN (history)
                    if previous_moment_id:
                        graph.query(
                            """
                            MATCH (m1:Moment {id: $prev}), (m2:Moment {id: $curr})
                            MERGE (m1)-[:THEN {tick: 0}]->(m2)
                            """,
                            params={"prev": previous_moment_id, "curr": moment_id}
                        )
                    
                    previous_moment_id = moment_id
                logger.info(f"Created {len(lines)} opening moments for {playthrough_id}")
        except Exception as e:
            logger.error(f"Failed to create opening moments: {e}")

        # 4. Load opening.json template and convert to scene
        opening_template_path = Path(__file__).parent.parent.parent / "docs" / "opening" / "opening.json"
        if opening_template_path.exists():
            opening_template = json.loads(opening_template_path.read_text())
            scene = _opening_to_scene_tree(opening_template, scenario)
        else:
            # Fallback minimal scene
            scene = {
                "id": f"scene_{request.scenario_id}_start",
                "location": {"place": "place_camp", "name": "Camp", "region": "The North", "time": "night"},
                "characters": ["char_aldric"],
                "atmosphere": ["The fire crackles."],
                "narration": [{"text": "Aldric looks at you.", "speaker": "char_aldric"}],
                "voices": []
            }

        # 4. Save scene.json
        (playthrough_dir / "scene.json").write_text(json.dumps(scene, indent=2))

        # 5. Initialize empty files
        (playthrough_dir / "message_queue.json").write_text("[]")
        (playthrough_dir / "injection_queue.json").write_text('{"injections": []}')
        (playthrough_dir / "stream.jsonl").write_text("")
        (playthrough_dir / "PROFILE_NOTES.md").write_text("# Player Profile (Opening)\n\n## Answers So Far\n\n## Emerging Pattern\n")

        logger.info(f"Created playthrough {playthrough_id} with scenario {request.scenario_id}")

        return {
            "status": "ok",
            "playthrough_id": playthrough_id,
            "scenario": request.scenario_id,
            "scene": scene
        }

    @router.post("/playthrough/scenario")
    async def create_scenario_playthrough(request: PlaythroughCreateRequest):
        """Alias for /playthrough/create to keep the API contract consistent."""
        logger.info("Creating playthrough via /playthrough/scenario alias.")
        return await create_playthrough(request)

    # =========================================================================
    # MOMENT ENDPOINT (Graph-based)
    # =========================================================================

    @router.post("/moment")
    async def send_moment(request: MomentRequest):
        """
        Send a player moment.

        Creates the moment directly in the graph using MomentProcessor.
        The physics system handles any reactions via tick/weight propagation.
        """
        from engine.infrastructure.memory.moment_processor import MomentProcessor
        from engine.physics.graph import GraphOps

        playthrough_dir = _playthroughs_dir / request.playthrough_id
        if not playthrough_dir.exists():
            raise HTTPException(status_code=404, detail="Playthrough not found")

        try:
            # Get graph for this playthrough
            graph_name = get_playthrough_graph_name(request.playthrough_id)
            ops = GraphOps(graph_name=graph_name, host=_host, port=_port)
            queries = _get_playthrough_queries(request.playthrough_id)

            # Get player location
            player_loc = queries.get_player_location("char_player")
            location_id = player_loc.get("id", "place_unknown") if player_loc else "place_unknown"

            # Get current tick from tempo state
            tempo_file = playthrough_dir / "tempo_state.json"
            current_tick = 0
            if tempo_file.exists():
                try:
                    tempo_data = json.loads(tempo_file.read_text())
                    current_tick = tempo_data.get("tick", 0)
                except:
                    pass

            # Create embedding function (use None for now - embeddings are optional)
            def dummy_embed(text: str):
                if not text or not text.strip():
                    return None
                try:
                    from engine.infrastructure.embeddings.service import get_embedding_service
                    return get_embedding_service().embed(text)
                except Exception as exc:
                    logger.warning(f"[moment] Embedding unavailable: {exc}")
                    return None

            # Create moment processor
            processor = MomentProcessor(
                graph_ops=ops,
                embed_fn=dummy_embed,
                playthrough_id=request.playthrough_id,
                playthroughs_dir=_playthroughs_dir
            )
            processor._current_tick = current_tick
            processor._current_place_id = location_id

            # Process the player action into a graph moment
            moment_id = processor.process_player_action(
                text=request.text,
                player_id="char_player",
                action_type=request.moment_type,
                initial_weight=1.0,
                initial_status="spoken"
            )

            # Broadcast to SSE listeners so UI refreshes immediately.
            try:
                from engine.infrastructure.api.sse_broadcast import broadcast_moment_event
                broadcast_moment_event(request.playthrough_id, "moment_spoken", {
                    "moment_id": moment_id,
                    "tick": current_tick
                })
            except Exception as exc:
                logger.warning(f"[moment] SSE broadcast failed: {exc}")

            logger.info(f"[moment] Created player moment {moment_id} for {request.playthrough_id}")

            return {
                "status": "created",
                "moment_id": moment_id,
                "narrator_started": False,
                "narrator_running": False
            }

        except Exception as e:
            logger.error(f"[moment] Failed to create moment: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # DISCUSSION TREE ENDPOINTS
    # =========================================================================

    @router.get("/{playthrough_id}/discussion/{char_id}/topics")
    async def get_discussion_topics(playthrough_id: str, char_id: str):
        """
        Get list of available discussion topics for a character.
        """
        tree_file = _playthroughs_dir / playthrough_id / "discussion_trees" / f"{char_id}.json"

        if not tree_file.exists():
            return {"topics": [], "branch_count": 0}

        try:
            data = json.loads(tree_file.read_text())
            topics = data.get("topics", [])
            branch_count = _count_branches(topics)

            return {
                "topics": [{"id": t["id"], "name": t["name"]} for t in topics],
                "branch_count": branch_count
            }
        except Exception as e:
            logger.error(f"Failed to get discussion topics: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{playthrough_id}/discussion/{char_id}/topic/{topic_id}")
    async def get_discussion_topic(playthrough_id: str, char_id: str, topic_id: str):
        """
        Get a specific discussion topic tree.
        """
        tree_file = _playthroughs_dir / playthrough_id / "discussion_trees" / f"{char_id}.json"

        if not tree_file.exists():
            raise HTTPException(status_code=404, detail="Discussion trees not found")

        try:
            data = json.loads(tree_file.read_text())
            topics = data.get("topics", [])

            for topic in topics:
                if topic["id"] == topic_id:
                    return {"topic": topic}

            raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get topic: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/{playthrough_id}/discussion/{char_id}/use-branch")
    async def use_discussion_branch(
        playthrough_id: str,
        char_id: str,
        request: Request
    ):
        """
        Mark a branch as used (delete it from the tree).
        Request body: {"topic_id": "...", "branch_path": ["word1", "word2"]}

        Returns remaining branch count. Triggers regeneration if < 5.
        """
        try:
            body = await request.json()
            topic_id = body.get("topic_id")
            branch_path = body.get("branch_path", [])

            tree_file = _playthroughs_dir / playthrough_id / "discussion_trees" / f"{char_id}.json"

            if not tree_file.exists():
                raise HTTPException(status_code=404, detail="Discussion trees not found")

            data = json.loads(tree_file.read_text())
            topics = data.get("topics", [])

            # Find and modify the topic
            modified = False
            for topic in topics:
                if topic["id"] == topic_id:
                    _delete_branch(topic, branch_path)
                    modified = True
                    break

            if not modified:
                raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found")

            # Save updated JSON
            tree_file.write_text(json.dumps({"topics": topics}, indent=2))

            # Count remaining branches
            branch_count = _count_branches(topics)

            # Trigger regeneration if needed
            regenerate_needed = branch_count < 5

            return {
                "status": "ok",
                "branch_count": branch_count,
                "regenerate_needed": regenerate_needed
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to use branch: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return router


---

## SOURCE: engine/infrastructure/api/sse_broadcast.py
"""
SSE Broadcast — Shared module for broadcasting events to SSE clients.

Used by:
- moments.py (click handler)
- orchestrator.py (after narrator/world runner)
"""

import asyncio
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# Per-playthrough SSE client queues
# Key: playthrough_id, Value: list of asyncio.Queue for connected clients
_sse_clients: Dict[str, List[asyncio.Queue]] = {}


def get_sse_clients() -> Dict[str, List[asyncio.Queue]]:
    """Get the SSE clients dict (for moments.py to register clients)."""
    return _sse_clients


def register_sse_client(playthrough_id: str, queue: asyncio.Queue):
    """Register a new SSE client queue for a playthrough."""
    if playthrough_id not in _sse_clients:
        _sse_clients[playthrough_id] = []
    _sse_clients[playthrough_id].append(queue)
    logger.debug(f"[SSE] Registered client for {playthrough_id}, total: {len(_sse_clients[playthrough_id])}")


def unregister_sse_client(playthrough_id: str, queue: asyncio.Queue):
    """Unregister an SSE client queue."""
    if playthrough_id in _sse_clients:
        try:
            _sse_clients[playthrough_id].remove(queue)
            logger.debug(f"[SSE] Unregistered client for {playthrough_id}")
        except ValueError:
            pass
        if not _sse_clients[playthrough_id]:
            del _sse_clients[playthrough_id]


def broadcast_moment_event(playthrough_id: str, event_type: str, data: Dict[str, Any]):
    """
    Broadcast a moment event to all SSE clients for a playthrough.

    Event types:
    - moment_activated: New moment became active
    - moment_spoken: Moment was spoken (recorded to canon)
    - moment_decayed: Moment weight fell below threshold
    - weight_updated: Moment weight changed
    - click_traversed: Click led to new moment

    Args:
        playthrough_id: The playthrough to broadcast to
        event_type: The SSE event type
        data: The event payload
    """
    if playthrough_id not in _sse_clients:
        logger.debug(f"[SSE] No clients for {playthrough_id}, skipping broadcast")
        return

    client_count = len(_sse_clients[playthrough_id])
    sent = 0

    for queue in _sse_clients[playthrough_id]:
        try:
            queue.put_nowait({"type": event_type, "data": data})
            sent += 1
        except asyncio.QueueFull:
            logger.warning(f"[SSE] Queue full for {playthrough_id}, dropping event")

    if sent > 0:
        logger.debug(f"[SSE] Broadcast {event_type} to {sent}/{client_count} clients for {playthrough_id}")


# Note: Canon Holder (not yet implemented) should call broadcast_moment_event
# when moments transition to 'spoken' status.
# See: docs/infrastructure/canon/ALGORITHM_Canon_Holder.md


---

## SOURCE: engine/infrastructure/orchestration/orchestrator.py
"""
Blood Ledger — Orchestrator

The main loop that coordinates:
1. Narrator (scene generation)
2. Graph ticks (physics simulation)
3. World Runner (flip resolution)
4. State management

This is the entry point for the game engine.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from engine.physics.graph import GraphOps, GraphQueries
from engine.physics import GraphTick
from .narrator import NarratorService
from .world_runner import WorldRunnerService

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Main orchestrator for the Blood Ledger game engine.
    """

    def __init__(
        self,
        playthrough_id: str,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379,
        playthroughs_dir: str = "playthroughs"
    ):
        # Playthrough
        self.playthrough_id = playthrough_id
        self.playthrough_dir = Path(playthroughs_dir) / playthrough_id
        self.playthrough_dir.mkdir(parents=True, exist_ok=True)

        # Database
        self.read = GraphQueries(graph_name=graph_name, host=host, port=port)
        self.write = GraphOps(graph_name=graph_name, host=host, port=port)

        # Services
        self.narrator = NarratorService()
        self.world_runner = WorldRunnerService(graph_ops=self.write, graph_queries=self.read)
        self.tick_engine = GraphTick(graph_name=graph_name, host=host, port=port)

        # State
        self.last_tick_time: Optional[datetime] = None

        logger.info(f"[Orchestrator] Initialized playthrough '{playthrough_id}'")

    def process_action(
        self,
        player_action: str,
        player_id: str = "char_player",
        player_location: str = None
    ) -> Dict[str, Any]:
        """
        Process a player action through the full loop.

        Args:
            player_action: What the player did (clicked word, free input, etc.)
            player_id: Player character ID
            player_location: Current location (or lookup from graph)

        Returns:
            Full narrator output: {dialogue, mutations, scene, time_elapsed}

        The Loop:
        1. Build scene context
        2. Call Narrator with context + any world_injection
        3. Parse response, apply mutations
        4. Run graph tick based on time_elapsed (only for significant actions)
        5. If flips detected, call World Runner
        6. Store world_injection for next call
        7. Return full output
        """
        logger.info(f"[Orchestrator] Processing action: {player_action}")
        logger.info(f"[Orchestrator] player_id={player_id}, player_location={player_location}")

        # Get player location if not provided
        if not player_location:
            player_location = self._get_player_location(player_id)
            logger.info(f"[Orchestrator] Resolved location to: {player_location}")

        # 1. Build scene context
        scene_context = self._build_scene_context(player_id, player_location)
        logger.info(f"[Orchestrator] Scene context has {len(scene_context.get('present', []))} characters present")

        # 2. Load world_injection if exists
        world_injection = self._load_world_injection()

        # 3. Call Narrator
        narrator_output = self.narrator.generate(
            scene_context=scene_context,
            world_injection=world_injection,
            instruction=f"Player action: {player_action}"
        )

        # Clear consumed world_injection
        if world_injection:
            self._clear_world_injection()

        # 4. Apply mutations
        mutations = narrator_output.get('mutations', [])
        if mutations:
            self._apply_mutations(mutations)

        # 5. Run graph tick (only for significant actions with time_elapsed)
        time_elapsed = narrator_output.get('time_elapsed')
        if time_elapsed:
            elapsed_minutes = self._parse_time(time_elapsed)

            # Only tick if significant time passed (5+ minutes)
            if elapsed_minutes >= 5:
                tick_result = self.tick_engine.run(
                    elapsed_minutes=elapsed_minutes,
                    player_id=player_id,
                    player_location=player_location
                )

                # 6. If flips, call World Runner
                if tick_result.flips:
                    self._process_flips(
                        flips=tick_result.flips,
                        player_id=player_id,
                        player_location=player_location,
                        time_elapsed=time_elapsed
                    )

        # 7. Return full output
        return narrator_output

    def process_action_streaming(
        self,
        player_action: str,
        player_id: str = "char_player",
        player_location: str = None
    ) -> Dict[str, Any]:
        """
        Process a player action for streaming response.

        Same as process_action but returns the full narrator output
        with dialogue chunks for streaming.

        Returns:
            {
                dialogue: [{speaker?, text}, ...],
                mutations: [...],
                scene: {} or full SceneTree,
                time_elapsed?: string
            }
        """
        return self.process_action(
            player_action=player_action,
            player_id=player_id,
            player_location=player_location
        )

    def _build_scene_context(
        self,
        player_id: str,
        player_location: str
    ) -> Dict[str, Any]:
        """Build scene context for the Narrator."""
        # Use GraphQueries' build_scene_context
        try:
            context = self.read.build_scene_context(player_location, player_id)
            logger.info(f"[Orchestrator] Built context for {player_location}: {len(context.get('present', []))} present, {len(context.get('active_narratives', []))} narratives")
        except Exception as e:
            logger.error(f"[Orchestrator] Failed to build context: {e}")
            context = {
                'location': {'id': player_location, 'name': 'Unknown'},
                'present': [],
                'active_narratives': [],
                'tensions': []
            }

        # Add time info
        context['time'] = {
            'time_of_day': self._get_time_of_day(),
            'day': self._get_game_day()
        }

        # Add player state
        context['player_state'] = {
            'pursuing': self._get_player_goal(player_id),
            'recent': self._get_recent_action()
        }

        return context

    def _get_player_location(self, player_id: str) -> str:
        """Get player's current location."""
        try:
            location = self.read.get_player_location(player_id=player_id)
            if location and location.get("id"):
                return location["id"]
        except Exception as exc:
            logger.warning(f"[Orchestrator] Failed to resolve player location: {exc}")
        return "place_unknown"

    def _get_time_of_day(self) -> str:
        """Get current time of day (would be tracked in game state)."""
        tick = self._get_world_tick()
        if tick is None:
            hour = datetime.utcnow().hour
        else:
            hour = (tick % 1440) // 60

        if hour < 6:
            return "night"
        if hour < 9:
            return "dawn"
        if hour < 12:
            return "morning"
        if hour < 14:
            return "midday"
        if hour < 17:
            return "afternoon"
        if hour < 20:
            return "dusk"
        if hour < 22:
            return "evening"
        return "night"

    def _get_game_day(self) -> int:
        """Get current game day (would be tracked in game state)."""
        tick = self._get_world_tick()
        if tick is None:
            return 1
        if tick < 0:
            return 1
        return (tick // 1440) + 1

    def _get_player_goal(self, player_id: str) -> str:
        """Get player's current goal from active narratives."""
        beliefs = self.read.get_character_beliefs(player_id)
        for belief in beliefs:
            if belief.get('type') == 'oath' and belief.get('believes', 0) > 0.5:
                return belief.get('content', '')[:50]
        return "Survive"

    def _get_recent_action(self) -> str:
        """Get description of recent action (would be tracked in state)."""
        path = self.playthrough_dir / "current_action.json"
        if path.exists():
            try:
                data = json.loads(path.read_text())
                action = data.get("action")
                if action:
                    return str(action)
            except Exception as exc:
                logger.warning(f"[Orchestrator] Failed to load recent action: {exc}")
        return "Continuing the journey"

    def _apply_mutations(self, mutations: List[Dict[str, Any]]):
        """Apply mutations from Narrator output."""
        # Convert Narrator mutation format to apply format
        data = {
            'nodes': [],
            'links': [],
            'updates': [],
            'movements': []
        }

        for mutation in mutations:
            mut_type = mutation.get('type')
            payload = mutation.get('payload', mutation)

            if mut_type == 'new_narrative':
                data['nodes'].append({
                    'type': 'narrative',
                    **payload
                })

            elif mut_type == 'new_character':
                # New character invented during conversation
                data['nodes'].append({
                    'type': 'character',
                    'id': payload.get('id'),
                    'name': payload.get('name'),
                    'traits': payload.get('traits', []),
                    'character_type': 'minor',  # Invented characters are minor by default
                })
                # If location specified, add AT relationship
                if payload.get('location'):
                    data['links'].append({
                        'type': 'at',
                        'character': payload.get('id'),
                        'place': payload.get('location'),
                        'present': 1.0
                    })

            elif mut_type == 'new_edge':
                # New relationship edge
                data['links'].append({
                    'type': payload.get('type', 'KNOWS').lower(),
                    'from': payload.get('from'),
                    'to': payload.get('to'),
                    **payload.get('properties', {})
                })

            elif mut_type == 'update_belief':
                data['links'].append({
                    'type': 'belief',
                    'character': payload.get('character'),
                    'narrative': payload.get('narrative'),
                    'heard': payload.get('heard'),
                    'believes': payload.get('believes'),
                    'doubts': payload.get('doubts')
                })

            elif mut_type == 'adjust_focus':
                data['updates'].append({
                    'node': payload.get('narrative'),
                    'focus': payload.get('focus')
                })

        if any(data.values()):
            self.write.apply(data=data)

    def _parse_time(self, time_str: str) -> float:
        """Parse time string to minutes."""
        if not time_str:
            return 5.0

        time_lower = time_str.lower()

        # Handle "X-Y minutes" format
        import re
        range_match = re.search(r'(\d+)-(\d+)\s*min', time_lower)
        if range_match:
            return (float(range_match.group(1)) + float(range_match.group(2))) / 2

        # Handle "X minutes"
        min_match = re.search(r'(\d+)\s*min', time_lower)
        if min_match:
            return float(min_match.group(1))

        # Handle "X hours"
        hour_match = re.search(r'(\d+)\s*hour', time_lower)
        if hour_match:
            return float(hour_match.group(1)) * 60

        # Handle "X days"
        day_match = re.search(r'(\d+)\s*day', time_lower)
        if day_match:
            return float(day_match.group(1)) * 24 * 60

        return 5.0

    def _process_flips(
        self,
        flips: List[Dict[str, Any]],
        player_id: str,
        player_location: str,
        time_elapsed: str
    ):
        """Process flipped tensions through World Runner."""
        # Build graph context
        graph_context = self._build_graph_context(flips)

        # Build player context
        player_context = {
            'location': player_location,
            'engaged_with': None,  # TODO: Track engagement
            'recent_action': self._get_recent_action()
        }

        # Call World Runner
        wr_output = self.world_runner.process_flips(
            flips=flips,
            graph_context=graph_context,
            player_context=player_context,
            time_span=time_elapsed
        )

        # Apply graph mutations
        graph_mutations = wr_output.get('graph_mutations', {})
        if graph_mutations:
            self._apply_wr_mutations(graph_mutations)

        # Store world_injection for next Narrator call
        world_injection = wr_output.get('world_injection')
        if world_injection:
            self._save_world_injection(json.dumps(world_injection))

        logger.info(f"[Orchestrator] Processed {len(flips)} flips")

    def _build_graph_context(self, flips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build graph context for World Runner."""
        # Get relevant narratives from flips
        narrative_ids = set()
        for flip in flips:
            narr_ids = flip.get('narratives', [])
            if isinstance(narr_ids, str):
                narr_ids = json.loads(narr_ids)
            narrative_ids.update(narr_ids)

        relevant_narratives = []
        for narr_id in narrative_ids:
            narr = self.read.get_narrative(narr_id)
            if narr:
                # Get believers
                believers = self.read.get_narrative_believers(narr_id)
                narr['believers'] = [b.get('id') for b in believers]
                relevant_narratives.append(narr)

        # Get character locations
        characters = self.read.get_all_characters()
        char_locations = {}
        for char in characters:
            char_id = char.get('id')
            loc = self._get_character_location_by_id(char_id)
            if loc:
                char_locations[char_id] = loc

        return {
            'relevant_narratives': relevant_narratives,
            'character_locations': char_locations
        }

    def _get_character_location_by_id(self, char_id: str) -> Optional[str]:
        """Get a character's location."""
        cypher = f"""
        MATCH (c:Character {{id: '{char_id}'}})-[r:AT]->(p:Place)
        WHERE r.present > 0.5
        RETURN p.id
        """
        try:
            results = self.read.query(cypher)
            return results[0].get('p.id') if results else None
        except:
            return None

    def _apply_wr_mutations(self, mutations: Dict[str, Any]):
        """Apply World Runner mutations."""
        data = {
            'nodes': [],
            'links': [],
            'updates': [],
            'movements': []
        }

        # New narratives
        for narr in mutations.get('new_narratives', []):
            data['nodes'].append({
                'type': 'narrative',
                **narr
            })

        # New beliefs
        for belief in mutations.get('new_beliefs', []):
            data['links'].append({
                'type': 'belief',
                **belief
            })

        # Tension updates
        for update in mutations.get('tension_updates', []):
            data['updates'].append({
                'tension': update.get('id'),
                'pressure': update.get('pressure'),
                'resolved': update.get('resolved')
            })

        # New tensions
        for tension in mutations.get('new_tensions', []):
            data['nodes'].append({
                'type': 'tension',
                **tension
            })

        # Character movements
        for move in mutations.get('character_movements', []):
            data['movements'].append(move)

        if any(data.values()):
            self.write.apply(data=data)

    def new_game(self, initial_state_path: str = None):
        """Start a new game."""
        # Reset narrator session
        self.narrator.reset_session()

        # Clear world injection
        self._clear_world_injection()

        # Load initial state if provided
        if initial_state_path:
            self.write.apply(path=initial_state_path)

        logger.info("[Orchestrator] New game started")

        # -------------------------------------------------------------------------

        # World Injection File Management

        # -------------------------------------------------------------------------

    

        def _world_injection_path(self) -> Path:

            """Get path to world_injection.json for this playthrough."""

            if not self.playthrough_dir.exists():

                self.playthrough_dir.mkdir(parents=True, exist_ok=True)

            return self.playthrough_dir / "world_injection.json"

    

        def _get_world_tick(self) -> Optional[int]:

            """Get current world tick from graph state."""

            try:

                result = self.read._query("""

                    MATCH (w:World)

                    RETURN w.tick

                    LIMIT 1

                """)

                if result and result[0]:

                    tick_value = result[0][0]

                    if tick_value is not None:

                        return int(tick_value)

            except Exception as exc:

                logger.debug(f"[Orchestrator] Failed to load world tick: {exc}")

            return None

    

        def _load_world_injection(self) -> Optional[Dict[str, Any]]:

            """Load world_injection dictionary from file if it exists."""

            path = self._world_injection_path()

            if path.exists():

                try:

                    with open(path, 'r') as f:

                        return json.load(f)

                except Exception as e:

                    logger.error(f"[Orchestrator] Failed to load world_injection: {e}")

            return None

    def _save_world_injection(self, injection: Dict[str, Any]):
        """Save world_injection dictionary to file."""
        path = self._world_injection_path()
        try:
            with open(path, 'w') as f:
                json.dump(injection, f, indent=2)
            logger.info(f"[Orchestrator] Saved world_injection to {path}")
        except Exception as e:
            logger.error(f"[Orchestrator] Failed to save world_injection: {e}")

    def _clear_world_injection(self):
        """Delete world_injection file after it's consumed."""
        path = self._world_injection_path()
        if path.exists():
            try:
                path.unlink()
                logger.info(f"[Orchestrator] Cleared world_injection")
            except Exception as e:
                logger.error(f"[Orchestrator] Failed to clear world_injection: {e}")


---

## SOURCE: engine/infrastructure/orchestration/agent_cli.py
"""
Agent CLI wrapper for non-interactive agent calls.

Centralizes command construction, execution, and response parsing so
callers share consistent behavior and error handling across providers.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import logging
import os
from pathlib import Path
import subprocess
from typing import Any, Optional

logger = logging.getLogger(__name__)

AGENTS_MODEL_ENV = "AGENTS_MODEL"
DEFAULT_AGENT_MODEL = "claude"
SUPPORTED_AGENT_MODELS = ("claude", "codex")
_DOTENV_LOADED = False


@dataclass(frozen=True)
class AgentCliResult:
    stdout: str
    stderr: str
    returncode: int
    raw_stdout: str = ""


def get_agent_model(model: Optional[str] = None) -> str:
    _load_dotenv_if_needed()
    if model:
        model = model.lower()
    else:
        model = (os.environ.get(AGENTS_MODEL_ENV) or DEFAULT_AGENT_MODEL).lower()
    if model not in SUPPORTED_AGENT_MODELS:
        raise ValueError(f"Unknown agent model: {model}")
    return model


def _load_dotenv_if_needed() -> None:
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    if os.environ.get(AGENTS_MODEL_ENV):
        _DOTENV_LOADED = True
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        _DOTENV_LOADED = True
        return
    project_root = Path(__file__).resolve().parents[3]
    load_dotenv(project_root / ".env")
    _DOTENV_LOADED = True


def build_agent_command(
    prompt: str,
    *,
    agent_model: Optional[str] = None,
    continue_session: bool = False,
    output_format: str = "json",
    add_dir: Optional[str] = None,
    system_prompt: Optional[str] = None,
    verbose: bool = True,
    allow_dangerous: bool = True,
) -> tuple[list[str], Optional[str]]:
    agent_model = get_agent_model(agent_model)
    if agent_model == "codex":
        combined_prompt = prompt if not system_prompt else f"{system_prompt}\n\n{prompt}"
        cmd = ["codex", "exec"]
        cmd.append("--json")
        if allow_dangerous:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
        cmd.append("-")
        return cmd, combined_prompt

    cmd = ["claude"]
    if continue_session:
        cmd.append("--continue")
    cmd.extend(["-p", prompt])
    cmd.extend(["--output-format", output_format])
    if allow_dangerous:
        cmd.append("--dangerously-skip-permissions")
    if add_dir:
        cmd.extend(["--add-dir", add_dir])
    if system_prompt:
        cmd.extend(["--append-system-prompt", system_prompt])
    if verbose:
        cmd.append("--verbose")
    return cmd, None


def run_agent(
    prompt: str,
    *,
    working_dir: Optional[str] = None,
    timeout: int = 600,
    continue_session: bool = False,
    output_format: str = "json",
    add_dir: Optional[str] = None,
    system_prompt: Optional[str] = None,
    verbose: bool = True,
    allow_dangerous: bool = True,
) -> AgentCliResult:
    agent_model = get_agent_model()
    cmd, stdin_payload = build_agent_command(
        prompt,
        agent_model=agent_model,
        continue_session=continue_session if agent_model == "claude" else False,
        output_format=output_format,
        add_dir=add_dir,
        system_prompt=system_prompt,
        verbose=verbose,
        allow_dangerous=allow_dangerous,
    )

    if stdin_payload and not stdin_payload.endswith("\n"):
        stdin_payload += "\n"

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=stdin_payload,
        timeout=timeout,
        cwd=working_dir,
    )

    raw_stdout = result.stdout or ""
    if agent_model == "codex":
        stdout = parse_codex_stream_output(raw_stdout)
    else:
        stdout = raw_stdout

    return AgentCliResult(
        stdout=stdout,
        stderr=result.stderr or "",
        returncode=result.returncode,
        raw_stdout=raw_stdout,
    )


def parse_claude_json_output(output: str) -> Any:
    """Parse Claude JSON output, unwrapping result envelopes and code fences."""
    output = output.strip()
    try:
        envelope = json.loads(output)
    except json.JSONDecodeError:
        fenced = _strip_code_fence(output)
        return json.loads(fenced)

    if isinstance(envelope, dict) and "result" in envelope:
        result = envelope["result"]
        if isinstance(result, str):
            cleaned = _strip_code_fence(result)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return cleaned
        return result
    return envelope


def extract_claude_text(output: str) -> str:
    """Extract plain text from JSON or text output."""
    output = output.strip()
    try:
        parsed = parse_claude_json_output(output)
    except json.JSONDecodeError:
        return _strip_code_fence(output)

    if isinstance(parsed, str):
        return parsed
    return json.dumps(parsed)


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if len(lines) <= 2:
        return ""
    return "\n".join(lines[1:-1]).strip()


def parse_codex_stream_output(output: str) -> str:
    """Extract text deltas from Codex stream JSON output."""
    parts: list[str] = []
    for line in output.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg_type = data.get("type")
        if msg_type == "content_block_delta":
            delta = data.get("delta", {})
            if delta.get("type") == "text_delta":
                parts.append(delta.get("text", ""))
        elif msg_type == "assistant":
            message = data.get("message", {})
            for content in message.get("content", []):
                if content.get("type") == "text":
                    parts.append(content.get("text", ""))
        elif msg_type == "result":
            result = data.get("result")
            if isinstance(result, str):
                parts.append(result)
    return "".join(parts)


---

## SOURCE: engine/run.py
#!/usr/bin/env python3
"""
Blood Ledger — Run Script

Start the backend server locally.

Usage:
    python run.py
    python run.py --host 0.0.0.0 --port 8000
"""

import os
import sys
import argparse
import logging

# Add parent directory to path so 'from engine.' imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run Blood Ledger backend')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    parser.add_argument('--graph', default='blood_ledger', help='Graph name')
    parser.add_argument('--db-host', default='localhost', help='FalkorDB host')
    parser.add_argument('--db-port', type=int, default=6379, help='FalkorDB port')
    args = parser.parse_args()

    # Set environment variables
    os.environ['GRAPH_NAME'] = args.graph
    os.environ['FALKORDB_HOST'] = args.db_host
    os.environ['FALKORDB_PORT'] = str(args.db_port)

    logger.info(f"Starting Blood Ledger backend on {args.host}:{args.port}")
    logger.info(f"FalkorDB: {args.db_host}:{args.db_port}, Graph: {args.graph}")

    import uvicorn

    # Use fully-qualified module path so uvicorn never imports an unrelated
    # third-party `api` package when run outside the engine/ directory.
    uvicorn.run(
        "engine.infrastructure.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()


---

## SOURCE: engine/init_db.py
#!/usr/bin/env python3
"""
Blood Ledger — Database Initialization

Creates schema indexes and loads initial game state.

Usage:
    python init_db.py
    python init_db.py --host localhost --port 6379
"""

import argparse
import logging
import redis
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_indexes(r: redis.Redis, graph_name: str):
    """Create indexes for efficient querying."""
    indexes = [
        # Node ID indexes (primary lookups)
        "CREATE INDEX FOR (n:Character) ON (n.id)",
        "CREATE INDEX FOR (n:Place) ON (n.id)",
        "CREATE INDEX FOR (n:Thing) ON (n.id)",
        "CREATE INDEX FOR (n:Narrative) ON (n.id)",
        "CREATE INDEX FOR (n:Tension) ON (n.id)",

        # Type indexes (filtering)
        "CREATE INDEX FOR (n:Character) ON (n.type)",
        "CREATE INDEX FOR (n:Place) ON (n.type)",
        "CREATE INDEX FOR (n:Narrative) ON (n.type)",

        # Name indexes (search)
        "CREATE INDEX FOR (n:Character) ON (n.name)",
        "CREATE INDEX FOR (n:Place) ON (n.name)",
        "CREATE INDEX FOR (n:Thing) ON (n.name)",
        "CREATE INDEX FOR (n:Narrative) ON (n.name)",
    ]

    for cypher in indexes:
        try:
            r.execute_command('GRAPH.QUERY', graph_name, cypher)
            logger.info(f"Created index: {cypher.split('ON')[1].strip()}")
        except Exception as e:
            if "already exists" in str(e).lower():
                logger.debug(f"Index already exists: {cypher}")
            else:
                logger.warning(f"Index creation failed: {e}")


def load_initial_state(graph_name: str, host: str, port: int):
    """Load initial game state from YAML."""
    from engine.physics.graph.graph_ops import GraphOps

    graph = GraphOps(graph_name=graph_name, host=host, port=port)

    # First load world data from data/world/*.yaml
    # These are flat lists, need to wrap them in {nodes: [...]} or {links: [...]} format
    import yaml as yaml_module
    world_dir = Path(__file__).parent.parent / "data" / "world"
    if world_dir.exists():
        # Phase 1: Load nodes first (order matters for references)
        node_files = {
            "places.yaml": "place",
            "places_minor.yaml": "place",
            "characters.yaml": "character",
            "things.yaml": "thing",
            "narratives.yaml": "narrative",
            "tensions.yaml": "tension",
            "events.yaml": "event",
        }
        for filename, node_type in node_files.items():
            world_file = world_dir / filename
            if world_file.exists():
                logger.info(f"Loading world nodes: {filename}")
                try:
                    raw_items = yaml_module.safe_load(world_file.read_text())
                    if raw_items and isinstance(raw_items, list):
                        nodes = []
                        for item in raw_items:
                            item["type"] = node_type
                            nodes.append(item)
                        result = graph.apply(data={"nodes": nodes, "links": []})
                        if result.success:
                            logger.info(f"  Loaded {len(result.persisted)} {node_type}s")
                        else:
                            for error in result.errors[:3]:
                                logger.warning(f"  Error: {error['item']}: {error['message']}")
                except Exception as e:
                    logger.error(f"  Failed to load {filename}: {e}")

        # Phase 2: Load links (after nodes exist)
        link_files = {
            "routes.yaml": "geography",
            "beliefs.yaml": "belief",
            "holdings.yaml": "holding",
            "thing_locations.yaml": "thing_location",
            "thing_ownership.yaml": "thing_ownership",
        }
        for filename, link_type in link_files.items():
            world_file = world_dir / filename
            if world_file.exists():
                logger.info(f"Loading world links: {filename}")
                try:
                    raw_items = yaml_module.safe_load(world_file.read_text())
                    if raw_items and isinstance(raw_items, list):
                        links = []
                        for item in raw_items:
                            item["type"] = link_type
                            links.append(item)
                        result = graph.apply(data={"nodes": [], "links": links})
                        if result.success:
                            logger.info(f"  Loaded {len(result.persisted)} {link_type} links")
                        else:
                            for error in result.errors[:3]:
                                logger.warning(f"  Error: {error['item']}: {error['message']}")
                except Exception as e:
                    logger.error(f"  Failed to load {filename}: {e}")

    # Then load initial state (core narratives, beliefs, presences)
    init_file = Path(__file__).parent / "data" / "init" / "initial_state.yaml"

    if not init_file.exists():
        logger.error(f"Initial state file not found: {init_file}")
        return False

    logger.info(f"Loading initial state from: {init_file}")
    result = graph.apply(path=str(init_file))

    if result.success:
        logger.info(f"Loaded {len(result.persisted)} items successfully")
        if result.has_duplicates:
            logger.warning(f"Found {len(result.duplicates)} potential duplicates")
    else:
        logger.error(f"Errors during load:")
        for error in result.errors:
            logger.error(f"  {error['item']}: {error['message']}")
            logger.info(f"    Fix: {error['fix']}")

    return result.success


def verify_data(r: redis.Redis, graph_name: str):
    """Verify initial data was loaded."""
    queries = [
        ("Characters", "MATCH (n:Character) RETURN count(n)"),
        ("Places", "MATCH (n:Place) RETURN count(n)"),
        ("Narratives", "MATCH (n:Narrative) RETURN count(n)"),
        ("Tensions", "MATCH (n:Tension) RETURN count(n)"),
        ("Beliefs", "MATCH ()-[r:BELIEVES]->() RETURN count(r)"),
        ("Presences", "MATCH ()-[r:AT]->() RETURN count(r)"),
        ("Geography", "MATCH ()-[r:CONNECTS]->() RETURN count(r)"),
    ]

    logger.info("\n=== Database Contents ===")
    for name, cypher in queries:
        try:
            result = r.execute_command('GRAPH.QUERY', graph_name, cypher)
            # FalkorDB returns [[[count]], stats]
            count = result[0][0][0] if result and result[0] else 0
            logger.info(f"  {name}: {count}")
        except Exception as e:
            logger.warning(f"  {name}: error - {e}")


def main():
    parser = argparse.ArgumentParser(description='Initialize Blood Ledger database')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--graph', default='blood_ledger', help='Graph name')
    parser.add_argument('--skip-data', action='store_true', help='Skip loading initial data')
    args = parser.parse_args()

    logger.info(f"Connecting to FalkorDB at {args.host}:{args.port}")

    try:
        r = redis.Redis(host=args.host, port=args.port, decode_responses=True)
        r.ping()
        logger.info("Connected successfully")
    except redis.exceptions.ConnectionError:
        logger.error(f"Cannot connect to FalkorDB at {args.host}:{args.port}")
        logger.info("Start FalkorDB with: redis-server --loadmodule /path/to/falkordb.so")
        return 1

    # Check if FalkorDB module is loaded
    modules = r.execute_command('MODULE', 'LIST')
    has_graph = any(m[1] == b'graph' or m[1] == 'graph' for m in modules)
    if not has_graph:
        logger.error("FalkorDB module not loaded. Start Redis with --loadmodule falkordb.so")
        return 1

    logger.info(f"Initializing graph: {args.graph}")

    # Create indexes
    logger.info("\n=== Creating Indexes ===")
    create_indexes(r, args.graph)

    # Load initial data
    if not args.skip_data:
        logger.info("\n=== Loading Initial State ===")
        if not load_initial_state(args.graph, args.host, args.port):
            logger.error("Failed to load initial state")
            return 1

    # Verify
    verify_data(r, args.graph)

    logger.info("\n=== Initialization Complete ===")
    logger.info(f"Graph '{args.graph}' is ready")
    logger.info(f"View in browser: http://localhost:3000")

    return 0


if __name__ == "__main__":
    exit(main())

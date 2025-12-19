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

## Playthrough Creation

### Overview

End-to-end flow when a player creates a new playthrough, from frontend form submission through graph initialization to first scene render.

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

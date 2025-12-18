# Archived: SYNC_Async_Architecture.md

Archived on: 2025-12-18
Original file: SYNC_Async_Architecture.md

---

## Implementation Phases

### Phase 1: Graph SSE Foundation

**Goal:** Graph emits SSE for position updates and image ready events only

**Tasks:**
1. Create SSE manager in `api/app.py`
2. Add SSE endpoint `/api/graph/stream`
3. Emit `position_update` when player location changes
4. Emit `image_ready` when place image generates
5. Frontend subscribes on load

**Files to modify:**
- `engine/api/app.py`
- `engine/db/graph_ops.py`
- `frontend/hooks/useGameState.ts`

---

### Phase 2: Hook Injection System

**Goal:** World can interrupt Narrator

**Tasks:**
1. Create `injection_queue.jsonl` handling
2. Create `check_injection.py` hook script
3. Configure PostToolUse hook in Claude Code
4. Frontend stop button writes to queue

**Files to create:**
- `engine/scripts/check_injection.py`
- `playthroughs/default/injection_queue.jsonl`

**Files to modify:**
- `.claude/hooks.json` (if exists)
- `frontend/components/scene/CenterStage.tsx`

---

### Phase 3: Runner Background Execution

**Goal:** Runner executes in background, outputs via TaskOutput

**Tasks:**
1. Modify Runner to output JSON to stdout
2. Narrator spawns with `run_in_background=true`
3. Narrator reads via `TaskOutput` on reminder
4. Runner writes to graph during execution

**Files to modify:**
- `engine/orchestration/world_runner.py`
- `engine/orchestration/narrator.py`

---

### Phase 4: Waypoint Creation & Fog

**Goal:** Places materialize during travel

**Tasks:**
1. Runner creates place nodes during travel
2. Graph triggers image generation
3. Frontend shows places on map
4. Visibility system tracks player knowledge

**Files to modify:**
- `engine/orchestration/world_runner.py`
- `engine/db/graph_ops.py`
- `frontend/components/map/` (new)

---

### Phase 5: Discussion Trees

**Goal:** Companions have evergreen conversations

**Tasks:**
1. Discussion tree generator subagent
2. Per-character storage
3. Branch deletion on use
4. Regeneration trigger
5. Idle initiation

**Files to create:**
- `agents/discussion_generator/`
- `prompts/discussion_generator.md`

---

### Phase 6: Map & Travel UI

**Goal:** Full travel experience

**Tasks:**
1. Map component with fog of war
2. Player position animation
3. Stop button
4. Location click → destination change
5. Image crossfade on location change

**Files to create:**
- `frontend/components/map/MapView.tsx`
- `frontend/components/map/FogOfWar.tsx`
- `frontend/components/map/PlayerToken.tsx`

---


## Existing Files Reference

### Engine

```
engine/
├── api/app.py                    # API endpoints (needs SSE)
├── db/
│   ├── graph_queries.py          # Read operations (OK)
│   └── graph_ops.py              # Write operations (needs SSE emit)
├── orchestration/
│   ├── orchestrator.py           # Current sync orchestrator (to replace)
│   ├── narrator.py               # Scene generation (needs async)
│   └── world_runner.py           # World simulation (needs background)
├── physics/
│   └── tick.py                   # Energy ticking (OK)
└── models/                       # Data models (OK)
```

### Frontend

```
frontend/
├── components/
│   ├── scene/
│   │   ├── CenterStage.tsx       # Main scene (needs travel mode)
│   │   └── SettingStrip.tsx      # Left panel (needs crossfade)
│   └── map/                      # NEW - map components
├── hooks/
│   ├── useGameState.ts           # State management (needs SSE)
│   └── useSceneTree.ts           # Scene tree (OK)
└── public/
    └── images/places/            # Place images (OK)
```

---


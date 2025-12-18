# Archived: SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

Archived on: 2025-12-18
Original file: SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

---

## What Exists

### Documentation
- [x] PATTERNS_Narrator.md — Core design philosophy
- [x] PATTERNS_World_Building.md — Pre-generation as world-building
- [x] BEHAVIORS_Narrator.md — What narrator produces (scene package, time_elapsed, mutations)
- [x] ALGORITHM_Scene_Generation.md — How to generate scene trees
- [x] ALGORITHM_Rolling_Window.md — Real-time generation strategy
- [x] ALGORITHM_Thread.md — Persistent conversation with --continue
- [x] ALGORITHM_Prompt_Structure.md — Prompt format with world injection
- [x] HANDOFF_Rolling_Window_Architecture.md — SSE push architecture for layer 2
- [x] TEMPLATE_Player_Notes.md — Template for per-playthrough player profiling
- [x] TEMPLATE_Story_Notes.md — Template for narrator's creative notebook

### Backend (IMPLEMENTED)
- [x] `engine/api/app.py` — FastAPI with SSE streaming endpoint
- [x] `engine/orchestration/orchestrator.py` — Main game loop
- [x] `engine/orchestration/narrator.py` — Claude CLI integration with --continue
- [x] `engine/orchestration/world_runner.py` — Tension flip resolution
- [x] `engine/physics/graph_tick.py` — Graph tick computation
- [x] `engine/db/graph_ops.py` — Graph mutations
- [x] `engine/db/graph_queries.py` — Graph queries

### Frontend (IMPLEMENTED)
- [x] Scene tree types in `frontend/types/game.ts`
- [x] `useSceneTree` hook for state management + streaming
- [x] `useDialogueStream` hook for SSE consumption
- [x] `DialogueStream` component for streaming display
- [x] Click → lookup response logic (instant for pre-baked)
- [x] Click → SSE stream (for clicks without response)
- [x] Clickable word UI with variants (subtle/voice)
- [x] Scene rendering from JSON (narration/speech/voices)
- [x] Free input text area with streaming
- [x] `sendActionStreaming()` API function

### Data
- [x] `/data/graph.json` — Narrative graph with characters, narratives, tensions
- [x] `/data/scenes/camp_night.json` — Example authored scene tree

---












## Key Design: Conversational-First

### The Two Response Paths

**Conversational (<5 min):**
```
Player: "Aldric, do you have kids?"
    ↓
[STREAM] "Ahah, kids..."
    ↓
[QUERY] Graph for family data
    ↓
[INVENT] Niece Edda, archer
    ↓
[STREAM] "But my niece — Edda — she's the finest archer..."
    ↓
[MUTATIONS] Create char_edda, link to Aldric
    ↓
[RETURN] {} — no scene refresh, conversation continues
```

**Significant (≥5 min):**
```
Player: "Let's break camp and head for York."
    ↓
[STREAM] "You stamp out the embers..."
    ↓
[QUERY] What's on the road?
    ↓
[STREAM] Continue narration
    ↓
[GENERATE] Full SceneTree for arrival
    ↓
[RETURN] scene + time_elapsed → triggers world runner
```

### time_elapsed Drives World Tick

Only significant actions (≥5 minutes) trigger world simulation:
- Graph tick runs
- Tensions accumulate
- Flips may occur → World Runner
- World injection created for next call

---












## API: SSE Streaming

### Endpoint

```
POST /api/scene/action
{
  "playthrough_id": "...",
  "action": "Aldric, do you have kids?",
  "player_id": "char_rolf",
  "stream": true  // Enable SSE
}
```

### SSE Events

| Event | Data | When |
|-------|------|------|
| `dialogue` | `{speaker?: string, text: string}` | Each dialogue chunk |
| `mutation` | `{type, payload}` | Graph changes |
| `scene` | Full SceneTree | Significant action complete |
| `time` | `{time_elapsed: string}` | Time passed |
| `complete` | `{status: "ok"}` | Stream finished |
| `error` | `{error: string}` | Error occurred |

### Frontend Consumption

```typescript
import { sendActionStreaming } from '@/lib/api';

await sendActionStreaming(
  playthroughId,
  action,
  {
    onDialogue: (chunk) => { /* append to display */ },
    onMutation: (mutation) => { /* track changes */ },
    onScene: (scene) => { /* update scene state */ },
    onComplete: () => { /* streaming done */ },
  }
);
```

---












## Output Schema

### NarratorOutput

```typescript
interface NarratorOutput {
  dialogue: DialogueChunk[];        // Streamed response chunks
  mutations: GraphMutation[];       // Changes invented during generation
  scene: SceneTree | {};            // Full scene OR empty for conversational
  time_elapsed?: string;            // Only for significant actions
  seeds?: Seed[];                   // Setups for future payoff
}

interface DialogueChunk {
  speaker?: string;  // Character ID if dialogue, omit for narration
  text: string;
}

interface GraphMutation {
  type: 'new_character' | 'new_edge' | 'new_narrative' | 'update_belief' | 'adjust_focus';
  payload: Record<string, unknown>;
}
```

---












## The Full Loop

```
Player action received
         ↓
[STEP 0] Classify: conversational or significant?
         ↓
[STREAM] Begin response immediately (character voice)
         ↓
[QUERY]  Graph for facts as needed (natural language)
         ↓
[INVENT] When sparse — this is content creation
         ↓
[STREAM] Continue response, weaving queries and invention
         ↓
[QUERY]  Look for connections to existing content
         ↓
[STREAM] Add connection callbacks ("actually, she trained near...")
         ↓
[MUTATIONS] Persist everything invented
         ↓
[DECIDE] Scene refresh needed?
         ↓
         ├── Conversational (<5 min): Return {}
         │
         └── Significant (≥5 min): Generate full SceneTree
                                           ↓
                                   Return scene + time_elapsed
                                           ↓
                                   Engine triggers world runner
```

---












## File Structure

```
engine/
  api/
    app.py              # FastAPI + SSE streaming
  orchestration/
    orchestrator.py     # Main game loop
    narrator.py         # Claude CLI wrapper
    world_runner.py     # Tension flip resolution
  physics/
    graph_tick.py       # Time-based simulation
  db/
    graph_ops.py        # Write mutations
    graph_queries.py    # Read queries

frontend/
  types/
    game.ts             # DialogueChunk, GraphMutation, NarratorOutput
  lib/
    api.ts              # sendActionStreaming()
  hooks/
    useSceneTree.ts     # Scene state + streaming integration
    useDialogueStream.ts # SSE consumption hook
  components/scene/
    CenterStage.tsx     # Main scene display
    DialogueStream.tsx  # Streaming dialogue display

agents/narrator/
  CLAUDE.md             # Narrator prompt (updated for conversational flow)
```

---












## Implementation Details

### Mutation Types

The narrator can create:

| Mutation | Purpose |
|----------|---------|
| `new_character` | Invent characters during conversation |
| `new_edge` | Create relationships (KIN, KNOWS, etc.) |
| `new_narrative` | New backstory, memory, rumor |
| `update_belief` | Character learns something |
| `adjust_focus` | Change narrative pacing |

### World Runner Trigger

Only triggered when:
1. `time_elapsed` is present (significant action)
2. Parsed time ≥ 5 minutes
3. Graph tick detects tension flips

---












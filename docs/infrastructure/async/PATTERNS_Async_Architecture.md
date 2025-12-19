# Async Architecture — Design Patterns

**Version:** 2.0
**Status:** DESIGNING
**Replaces:** Current synchronous orchestrator pattern

---

## Core Principle

**Travel is not a loading screen. Travel is play.**

The world materializes as you move through it. No skeleton. No pre-authored waypoints. The Runner writes places to the graph as it computes the journey. The Frontend sees them appear via SSE. Images generate automatically.

---

## The Architecture in One Sentence

> **Graph is truth. Runner writes. TaskOutput returns. Hook interrupts.**

---

## CHAIN

```
BEHAVIORS:      ./BEHAVIORS_Travel_Experience.md
ALGORITHM:      ./ALGORITHM_Async_Architecture.md
VALIDATION:     ./VALIDATION_Async_Architecture.md
IMPLEMENTATION: ./IMPLEMENTATION_Async_Architecture.md
TEST:           ./TEST_Async_Architecture.md
THIS:           PATTERNS_Async_Architecture.md
SYNC:           ./SYNC_Async_Architecture.md
```

---

## Component Responsibilities

### Graph — Source of Truth

The graph is not a passive database. It is the orchestrator.

- Stores all state (places, characters, narratives, tensions, energy)
- Emits SSE events on every write
- Triggers image generation when places are created
- Writes to injection queue when characters are activated

**What it is NOT:**
- Managed by an external orchestrator process
- Polled for changes
- A cache or intermediate state

### Runner — Background World Processor

The Runner simulates the world in the background while the player experiences the journey.

- Spawned by Narrator as background bash task (`run_in_background=true`)
- Creates waypoint places (writes directly to graph)
- Ticks energy and pressure each segment
- Resolves tension breaks, creates narratives
- Outputs completion JSON via TaskOutput (NOT via hook)

**Key clarification:** Runner completion is read via `TaskOutput`, not hook injection. Hooks are for interruptions only.

### Narrator — Streaming Experience Layer

The Narrator owns the player experience. It streams, responds, and reacts.

- Spawns Runner with `bash(run_in_background=true)`
- Streams journey narration immediately (doesn't wait for Runner)
- Handles player conversation (input queue)
- Reads Runner output via `TaskOutput` when system reminder arrives
- Receives interruptions via PostToolUse hook

**Narrator reads:**
- Graph for current state
- TaskOutput for Runner completion
- Hook for mid-stream interruptions (character speaks, player UI)

### Frontend — Real-Time Visualization

The Frontend subscribes once and receives everything.

- Subscribes to graph SSE stream
- Updates map position in real-time
- Reveals fog on visibility changes
- Displays images when ready
- Writes to injection queue (player UI actions like stop button)

### Hook — Interruption Mechanism

Hooks are for interruptions ONLY. Not for Runner completion.

**Hook fires when:**
- A character in the player's group is activated via narrative
- Player uses UI (stop button, location click, portrait click)

**Hook does NOT fire for:**
- Runner completing a task (use TaskOutput)
- Normal state updates (use SSE)

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         GRAPH                               │
│                   (source of truth)                         │
│                                                             │
│   places ─── characters ─── narratives ─── tensions         │
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │ SSE stream  │    │ write API   │    │ read API    │    │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
└──────────┼──────────────────┼──────────────────┼────────────┘
           │                  │                  │
           ▼                  │                  │
┌─────────────────┐           │                  │
│    FRONTEND     │           │                  │
│                 │           │                  │
│  map ← position │           │                  │
│  fog ← visibility           │                  │
│  img ← place.image          │                  │
│        │                    │                  │
│        └──────── writes ────┼──→ injection_queue.jsonl
└─────────────────┘           │                  │
                              │                  │
                ┌─────────────┘                  │
                │                                │
                ▼                                │
         ┌─────────────┐                         │
         │   RUNNER    │                         │
         │ (background)│                         │
         │             │                         │
         │  creates    │                         │
         │  places     │─────writes─────────────→│
         │  ticks      │                         │
         └──────┬──────┘                         │
                │                                │
                │ (main output)                  │
                ▼                                │
         ┌─────────────┐                         │
         │ TaskOutput  │                         │
         │ (on system  │                         │
         │  reminder)  │                         │
         └──────┬──────┘                         │
                │                                │
                ▼                                │
         ┌─────────────────┐                     │
         │    NARRATOR     │←───reads────────────┘
         │                 │
         │  streams        │←─── PostToolUse Hook
         │  responds       │     (interruptions only)
         │  spawns Runner  │
         └─────────────────┘
```

---

## Key Design Decisions

### Why No Orchestrator in This Flow?

**In the async/travel flow:** No orchestrator. Narrator spawns Runner directly as a background Task(). The graph is the coordination point — components write to it, it emits events, others react.

**In other contexts:** The orchestrator still exists for non-travel scenarios (scene management, turn-based interactions, etc.). This async architecture is specifically for travel and background world simulation.

The current synchronous orchestrator creates:
- Single point of failure
- Complex state management
- Synchronous bottlenecks

The async architecture makes the **graph the coordinator** for real-time flows.

### Why TaskOutput for Runner Completion?

Runner is a long-running background task. When it completes, Narrator needs to know.

**Option rejected:** Hook injection
- Hooks are for interruptions (character speaks, player UI)
- Runner completion is not an interruption — it's expected

**Option chosen:** TaskOutput
- System sends reminder when background task has output
- Narrator calls `TaskOutput(task_id)` to read result
- Clean separation: TaskOutput for completion, Hook for interruptions

### Why SSE Instead of Polling?

The Frontend needs real-time updates during travel:
- Player position moves
- New places appear on map
- Images become ready
- Fog reveals

Polling would mean:
- Constant requests
- Delayed updates
- Wasted resources

SSE provides:
- Single connection
- Instant updates
- Efficient resource use

### Why Ephemeral Discussion Trees?

Companions need to feel alive. Pre-authored dialogue runs out.

**Solution:**
- Generate discussion trees in background (5-10 topics, 3-4 depth each)
- Delete branches when used
- Regenerate when branches < threshold
- Trees feel fresh, never repeat

---

## File Paths

| Purpose | Path |
|---------|------|
| Place images | `frontend/public/images/places/{place_id}.png` |
| Discussion trees | `playthroughs/default/discussion_trees/{char_id}.json` |
| Injection queue | `playthroughs/default/injection_queue.jsonl` |

---

## What Goes Where

| Component | Responsibilities |
|-----------|-----------------|
| **Graph** | All persistent state, SSE emission, image generation trigger, character activation → injection queue |
| **Runner** | World simulation, place creation, energy ticking, break resolution, main output via TaskOutput |
| **Narrator** | Player experience, conversation, scene generation, journey narration, reads TaskOutput, receives hook interruptions |
| **Frontend** | Map rendering, fog of war, image display, real-time updates, player UI → injection queue |
| **Hook** | Character speaks (from graph activation), player UI actions (stop, click location) |

---

## Clarifications

### Multiple Runners

Multiple Runner instances can run simultaneously. Example: player traveling while characters move elsewhere in the world.

### Runner Robustness

Runner is assumed not to crash. No explicit failure handling in this architecture.

### Travel Interruption Position

If player aborts mid-travel, their position is the **last completed waypoint**. No interpolation.

### Narrator/Runner Timing

If Runner finishes before Narrator's journey narration completes, Narrator keeps streaming and incorporates the completion at the end. Runner completion doesn't interrupt the narrative flow.

### Player's Group Determination

Determined by `scene.json.characters` — array of character IDs present in the current scene. When a narrative activates a character in this list, injection fires.

### Idle Detection for Discussion Trees

Frontend responsibility. Frontend tracks time since last player input and triggers companion initiation after 10+ seconds of idle during travel.

---

## Related Documents

- `ALGORITHM_Async_Architecture.md` — Runner protocol, hooks, SSE, waypoints, fog, images, discussions
- `BEHAVIORS_Travel_Experience.md` — What travel should feel like
- `SYNC_Async_Architecture.md` — Current vs target state

# 08_Frontend_UI_Dataflow_And_Runtime_Config

@pack:generated_at: 2025-12-20T10:41:21
@pack:repo_kind: blood-ledger

Frontend runtime, UI dataflow, and contracts


---

## SOURCE: docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md
# Frontend — Implementation: Runtime and Configuration

```
STATUS: STABLE
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Presentation_Layer.md
BEHAVIORS:       ../BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ../ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ../VALIDATION_Frontend_Invariants.md
OVERVIEW:        ../IMPLEMENTATION_Frontend_Code_Architecture.md
THIS:            IMPLEMENTATION_Runtime_And_Config.md (you are here)
TEST:            ../TEST_Frontend_Coverage.md
SYNC:            ../SYNC_Frontend.md

IMPL:            frontend/app/page.tsx
```

---

## ENTRY POINTS

| Entry Point | Trigger | Notes |
|-------------|---------|-------|
| `frontend/app/page.tsx` | User navigates to `/` | Renders `GameClient` |
| `frontend/hooks/useGameState.ts` | GameClient mounts | Initial load + refresh |
| `frontend/hooks/useMoments.ts` | Scene uses moments | Click traversal + SSE |

---

## CODE STRUCTURE

```
frontend/
├── app/               # App Router entry points
│   ├── page.tsx
│   ├── layout.tsx
│   ├── start/page.tsx
│   ├── map/page.tsx
│   └── scenarios/page.tsx
├── components/        # UI composition
│   ├── GameClient.tsx
│   ├── GameLayout.tsx
│   ├── Providers.tsx
│   ├── scene/
│   ├── moment/
│   ├── map/
│   ├── panel/
│   ├── voices/
│   ├── chronicle/
│   ├── minimap/
│   ├── debug/
│   └── ui/
├── hooks/             # State management hooks
│   ├── useGameState.ts
│   └── useMoments.ts
├── lib/               # API + utilities
│   ├── api.ts
│   └── map/
├── types/             # Shared TypeScript types
│   ├── game.ts
│   ├── moment.ts
│   └── map.ts
├── data/              # Fallback static data
│   └── game-state.json
└── public/            # Static assets
    └── playthroughs/
```

### File Responsibilities

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `frontend/hooks/useGameState.ts` | Main game state + API integration | ~423 | WATCH |
| `frontend/lib/api.ts` | Backend API client | ~419 | WATCH |
| `frontend/hooks/useMoments.ts` | Moment system state + SSE | ~197 | OK |
| `frontend/types/game.ts` | Core game types | ~312 | OK |
| `frontend/components/GameClient.tsx` | Game wrapper + loading states | ~106 | OK |
| `frontend/components/GameLayout.tsx` | Scene + right panel layout | ~63 | OK |
| `frontend/app/page.tsx` | Main entry point | ~12 | OK |

**Size thresholds:** OK (<400 lines), WATCH (400-700), SPLIT (>700)

### Component Inventory (Highlights)

- **Scene UI:** `frontend/components/scene/CenterStage.tsx` (~435L, WATCH) and related scene components.
- **Moment UI:** `frontend/components/moment/MomentDebugPanel.tsx` (~221L), `MomentDisplay.tsx` (~201L).
- Detailed component docs live under `docs/frontend/scene/`.

---

## MODULE DEPENDENCIES (INTERNAL)

```
frontend/app/page.tsx
  └─ frontend/components/GameClient.tsx
      ├─ frontend/hooks/useGameState.ts
      │   ├─ frontend/lib/api.ts
      │   └─ frontend/types/game.ts
      └─ frontend/components/GameLayout.tsx
          ├─ frontend/components/scene/SceneView.tsx
          └─ frontend/components/panel/RightPanel.tsx
```

---

## EXTERNAL DEPENDENCIES

- `react` for UI composition
- `next` for App Router and server/client integration
- `tailwindcss` for styling

---

## DATA FLOW (SUMMARY)

- **Initial load:** `GameClient` → `useGameState` → `frontend/lib/api.ts` → transformed `GameState` → `GameLayout`.
- **Moment click:** `ClickableText` → `useMoments.clickWord` → API → update active/spoken state.
- **Streaming:** `useMoments` subscribes to SSE; events trigger state updates.

See `docs/frontend/ALGORITHM_Frontend_Data_Flow.md` for the full data-flow algorithm and event types.

---

## STATE MANAGEMENT

| State | Location | Scope |
|-------|----------|-------|
| `gameState` | `useGameState` | Per-page |
| `activeMoments` | `useMoments` | Per-location |
| `spokenMoments` | `useMoments` | Per-location |
| `isLoading` / `error` | Hooks | Per-hook |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `frontend/.env.local` | `http://localhost:8000` | Backend API base URL |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Reference |
|------|-----------|
| `frontend/app/page.tsx` | `docs/frontend/PATTERNS_Presentation_Layer.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM initial load | `frontend/hooks/useGameState.ts` |
| ALGORITHM click traversal | `frontend/hooks/useMoments.ts` |
| BEHAVIOR B1 (initial load) | `frontend/hooks/useGameState.ts` |
| BEHAVIOR B3 (moment click) | `frontend/hooks/useMoments.ts` |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add DOCS reference to `frontend/app/page.tsx` if missing
- [ ] Consider splitting `frontend/components/scene/CenterStage.tsx` if it grows


---

## SOURCE: docs/frontend/PATTERNS_Presentation_Layer.md
# Frontend — Patterns: Presentation Layer for The Blood Ledger

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against current implementation
```

---

## CHAIN

```
THIS:            PATTERNS_Presentation_Layer.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/app/page.tsx
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update SYNC_Frontend.md with changes
2. Run: `cd frontend && npm run build` to verify

**After modifying the code:**
1. Update this doc chain to match
2. Run: `cd frontend && npm run build` to verify

---

## THE PROBLEM

The Blood Ledger is a narrative game with:
- A Python backend (FastAPI) handling game logic, graph database, LLM orchestration
- Complex game state: scenes, characters, moments, ledger entries, chronicle
- Real-time updates via SSE streaming

The frontend needs to:
1. Present this rich narrative world to players
2. Handle streaming dialogue and scene updates
3. Support interactive elements (clickable words, hotspots)
4. Work gracefully when the backend is unavailable (fallback to static data)

---

## THE PATTERN

**Next.js with React hooks for state management and SSE streaming**

Core architecture:
1. **Next.js 16 App Router** — Modern React patterns, server components where possible
2. **Custom hooks** — `useGameState` and `useMoments` manage API interaction and state
3. **Component hierarchy** — GameClient → GameLayout → Panel components
4. **Tailwind CSS** — Utility-first styling for consistent dark theme
5. **SSE streaming** — Real-time updates from backend Narrator

The frontend is a **window into the engine**, not part of it. The backend is complete without the frontend — you could run world updates in headless mode.

---

## PRINCIPLES

### Principle 1: Backend-Driven State

The frontend doesn't own game state. All truth lives in the Python backend's graph database.

**Why:** Game logic belongs in one place. The frontend renders what the backend says is true.

**Implementation:**
- `useGameState` fetches from `/api/view/*` endpoints
- SSE streaming pushes real-time updates
- Local state is derived, not authoritative

### Principle 2: Graceful Degradation

When backend is unavailable, show static fallback data rather than errors.

**Why:** Development experience. Demo capability. Resilience.

**Implementation:**
- `fallbackState` prop in GameClient
- `isConnected` flag drives "Live" vs "Static" indicator
- Static JSON in `frontend/data/game-state.json`

### Principle 3: Component Isolation

Each component handles one responsibility. Scene components don't know about map components.

**Why:** Maintainability. The game has many features; they should be independently modifiable.

**Structure:**
- `components/scene/` — Scene rendering, hotspots, atmosphere
- `components/moment/` — Moment system display, clickable text
- `components/map/` — Map canvas, fog of war
- `components/panel/` — Right panel tabs (chronicle, ledger, conversations)
- `components/voices/` — Internal thoughts display

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `engine/api/` | REST and SSE endpoints provide authoritative state snapshots so the UI can render without duplicating logic. |
| `engine/api/moments.py` | Moments endpoint defines the payload shape for the narrative stream and keeps hooks aligned. |
| `docs/physics/` | Moment system and energy model live here, guiding UI expectations and debug displays. |
| `docs/infrastructure/async/` | Streaming patterns and injection queues define the cadence the UI must mirror. |

---

## INSPIRATIONS

- **Disco Elysium** — Voices as internal thoughts, layered UI, and click-to-explore narrative fragments.
- **80 Days** — Narrative presentation with travel pacing, atmosphere, and constrained choice surfaces.
- **Twine/Ink** — Clickable narrative words, branching micro-interactions, and text-first emphasis.

---

## SCOPE

### In Scope

- Render scenes, moments, maps, and panels from backend-provided state, including static fallback snapshots.
- Manage UI-only state such as layout toggles, scroll positions, and input buffering without owning canon.
- Surface real-time updates through SSE-driven hooks and present interactive affordances like clickable words.

### Out of Scope

- Game logic, simulations, and graph mutations remain in Python services; the UI never computes outcomes.
- Persistent storage, authentication, and account management are handled elsewhere or deferred from v1.
- Image generation and media pipelines live in backend tools; the frontend only renders provided assets.

---

## WHAT THIS DOES NOT SOLVE

- **Game logic** — Lives in the Python backend; frontend never decides outcomes or world state.
- **Persistence** — Graph database ownership stays server-side; UI does not store canonical history.
- **LLM orchestration** — Narrator and agent prompting run in backend services, not the browser.
- **Image generation** — Ideogram and asset pipelines are server tools; UI only renders returned assets.
- **Authentication** — Not implemented for v1; assumptions remain single-player and session-local.

---

## GAPS / IDEAS / QUESTIONS

- [x] TEST doc: Document component testing approach, including expectations for hooks and UI utilities.
- [x] IMPLEMENTATION doc: Detail file structure and data flows across routes, hooks, and panels.
- QUESTION: Should useMoments replace useGameState entirely, or coexist as parallel reads of backend state?
- IDEA: Use Storybook or Ladle for component development and QA of scene/panel variants.


---

## SOURCE: docs/frontend/ALGORITHM_Frontend_Data_Flow.md
# Frontend Data Flow — Algorithm

```
UPDATED: 2025-12-19
STATUS: CANONICAL (describes desired state)
```

---

## CHAIN

```
THIS:            ALGORITHM_Frontend_Data_Flow.md (you are here)
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/hooks/useGameState.ts
```

---

## OVERVIEW

This document describes the frontend data flow between UI events, REST/SSE
calls, and in-memory state updates for the moment system and scene rendering.

---

## DATA STRUCTURES

- **GameState**: aggregate of scene, moments, characters, and UI flags that
  powers the main render tree and the right-panel tabs.
- **Moment**: text payload with status flags (active/spoken/decayed), weight,
  and clickable word metadata used by the moment stream.
- **SSE Event**: `{type, payload}` structures emitted by `/api/moments/stream`
  to notify the frontend about moment activation, decay, or clicks.
- **Action Payload**: `{playthrough_id, action, player_id}` for full-loop
  narrator requests that mutate the graph and update the scene.

---

## ALGORITHM: ProcessFrontendDataFlow

1. Capture a UI event (click on a word or a free-text action).
2. Select the appropriate backend path (instant click vs full action loop).
3. Issue a REST request with playthrough identifiers and payload data.
4. On response, update local state (scene, moments, indicators) immediately.
5. Subscribe to SSE stream updates and reconcile via `fetchGameState`.
6. Render components based on updated GameState and Moment arrays.

---

## KEY DECISIONS

- Favor backend-driven truth: the frontend does not own authoritative state,
  so most updates reconcile via server responses or SSE pushes.
- Keep two paths for latency: instant clicks stay under 50ms, full actions
  allow slower LLM responses while keeping the UI responsive.
- Use SSE to avoid polling: the client listens for event triggers and refreshes
  state when moments activate, speak, decay, or traverse.

---

## DATA FLOW

### Two Paths

### Path 1: Instant Click (No LLM)

```
Player clicks word
    ↓
POST /api/moment/click
{playthrough_id, moment_id, word, tick}
    ↓
Backend: weight updates, flip detection
    ↓
Response: {traversed, target_moment, new_active_moments}
    ↓
Frontend: update local state immediately
```

**Latency target:** <50ms

**When to use:** Clicking highlighted words in moments

---

### Path 2: Full Loop (With LLM)

```
Player types free text OR narrator response needed
    ↓
POST /api/action
{playthrough_id, action, player_id}
    ↓
Backend: orchestrator.process_action()
  → Narrator generates response
  → Mutations applied
  → GraphTick runs (if time elapsed ≥5min)
  → Flips → World Runner
    ↓
Response: {dialogue, mutations, scene, time_elapsed}
    ↓
Frontend: update scene
```

**Latency:** 2-10 seconds (LLM call)

**When to use:** Free text input, complex actions

---

## Moment Updates: Current vs Desired

### Current Implementation (SSE)

```typescript
// useGameState.ts - IMPLEMENTED
useEffect(() => {
  const unsubscribe = api.subscribeToMomentStream(playthroughId, {
    onMomentActivated: (data) => fetchGameState(),
    onMomentSpoken: (data) => fetchGameState(),
    onClickTraversed: (data) => fetchGameState(),
    // ... other handlers
  });
  return () => unsubscribe();
}, [playthroughId]);
```

**Benefits:**
- Real-time updates via SSE
- No arbitrary delays
- Backend pushes when ready

### Future Optimization (Incremental Updates)

```typescript
// useGameState.ts - FUTURE: Update state incrementally instead of full refresh
useEffect(() => {
  const unsubscribe = subscribeToMomentStream(playthroughId, {
    onMomentActivated: (data) => {
      // Add moment to local state directly
      setMoments(prev => [...prev, data]);
    },
    onMomentSpoken: (data) => {
      // Mark moment as spoken in place
      updateMomentStatus(data.moment_id, 'spoken');
    },
    onWeightUpdated: (data) => {
      // Update moment weight in place
      updateMomentWeight(data.moment_id, data.weight);
    },
  });
  return () => unsubscribe();
}, [playthroughId]);
```

**When to implement:** When fetchGameState becomes a bottleneck

---

## SSE Event Types

| Event | Payload | When |
|-------|---------|------|
| `moment_activated` | `{moment_id, weight, text}` | New moment becomes active |
| `moment_spoken` | `{moment_id, tick}` | Moment shown to player |
| `moment_decayed` | `{moment_id}` | Moment weight fell below threshold |
| `weight_updated` | `{moment_id, weight}` | Click changed moment weight |
| `click_traversed` | `{from_id, to_id, word, consumed}` | Click led to new moment |

---

## Implementation Checklist

### Backend (exists)
- [x] `GET /api/moments/stream/{playthrough_id}` — SSE endpoint
- [x] Event emission on moment changes

### Frontend (complete)
- [x] `subscribeToMomentStream()` — Client function exists in api.ts
- [x] **Hook into useGameState** — SSE subscription in useEffect
- [x] **Remove polling hack** — Removed setTimeout from CenterStage.tsx
- [x] **Handle SSE events** — All event types handled, trigger fetchGameState

---

## Migration Path

1. Add SSE subscription to useGameState.ts
2. Handle all event types
3. Remove `setTimeout(() => refresh(), 1000)` from CenterStage.tsx
4. Test: send action, verify moments appear without polling

---

## Files

| File | Role |
|------|------|
| `frontend/lib/api.ts` | `subscribeToMomentStream()` — client SSE function |
| `frontend/hooks/useGameState.ts` | Manages state refresh and SSE hooks |
| `frontend/components/scene/CenterStage.tsx` | Sends action inputs to backend |
| `engine/infrastructure/api/moments.py` | SSE endpoint |

---

## COMPLEXITY

- Instant click path: O(1) request/response with small payloads and immediate
  in-memory updates for the active moments array.
- Full action loop: dominated by LLM latency; frontend work is O(1) for
  request/response but may trigger O(n) state refresh when reloading lists.
- SSE handling: O(1) per event, with optional O(n) refresh when full state is
  refetched after a stream notification.

---

## HELPER FUNCTIONS

- `subscribeToMomentStream(playthroughId, handlers)` in `frontend/lib/api.ts`
  wires SSE events to hook-level callbacks.
- `fetchGameState()` in `frontend/hooks/useGameState.ts` reconciles backend
  truth with local state after SSE or action responses.
- `sendMoment()` and `sendAction()` in the API layer emit click and free-text
  requests to the backend endpoints.

---

## INTERACTIONS

- UI components emit events from `CenterStage` and clickable moment text,
  calling API helpers that route to `/api/moment/click` or `/api/action`.
- The backend responds with scene and mutation data; the frontend updates
  GameState and re-renders the scene, map, and panels accordingly.
- SSE stream notifications act as a trigger for refresh to keep moments in
  sync with backend graph updates without polling.

---

## GAPS / IDEAS / QUESTIONS

- Should the incremental SSE update strategy replace the full refresh path,
  or do we need a hybrid to guard against missed events?
- What is the target latency budget for full-action LLM calls on low-power
  devices, and do we need progress or retry UI states?
- The moment system still coexists with legacy scene state; confirm the
  deprecation plan and whether `useMoments` becomes the sole source.


---

## SOURCE: docs/frontend/SYNC_Frontend.md
# Frontend — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: CANONICAL
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
THIS:            SYNC_Frontend.md (you are here)

IMPL:            frontend/app/page.tsx
```

---

## CURRENT STATE

The frontend is a functional Next.js 16 application with React 19. It serves as the presentation layer for The Blood Ledger game.

**Tech Stack:**
- Next.js 16.0.10
- React 19.2.1
- Tailwind CSS 4
- TypeScript 5

**Key Files:**
| Path | Purpose |
|------|---------|
| `frontend/app/page.tsx` | Main entry, loads GameClient |
| `frontend/app/start/page.tsx` | Opening/start screen |
| `frontend/app/map/page.tsx` | Map view |
| `frontend/app/playthroughs/[id]/page.tsx` | Playthrough-specific view |
| `frontend/app/scenarios/page.tsx` | Scenario selection |
| `frontend/components/GameClient.tsx` | Main game client, handles loading states |
| `frontend/components/GameLayout.tsx` | Layout with scene + right panel |
| `frontend/hooks/useGameState.ts` | State management, API integration |
| `frontend/hooks/useMoments.ts` | Moment system state |
| `frontend/types/game.ts` | TypeScript types for game state |
| `frontend/lib/api.ts` | API client functions |

**Component Organization:**
- `components/scene/` — Scene rendering (SceneView, CenterStage, SceneImage, etc.)
- `components/moment/` — Moment system (MomentDisplay, MomentStream, ClickableText)
- `components/map/` — Map display (MapCanvas, MapClient)
- `components/panel/` — Right panel tabs
- `components/voices/` — Internal thoughts
- `components/chronicle/` — Chronicle display
- `components/debug/` — Debug panel

---

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- Next.js App Router entry points and layout flow.
- Backend-driven state hooks with REST + SSE updates.
- Scene, moment, map, panel, and voice component hierarchy.

What's still being designed:
- Testing strategy and coverage expectations for frontend modules.
- Long-term consolidation plan for `useGameState` and `useMoments`.

What's proposed (v2):
- Replace remaining static fallbacks with scenario-specific mocks.
- Expand automated UI coverage for core playthrough flows.

---

## IN PROGRESS

- Align frontend testing approach with backend CI constraints.
- Track when the moment system can fully replace legacy scene state.

---

## RECENT CHANGES

### 2025-12-20: Use placeId for moment fetches

- **What:** CenterStage now passes `currentScene.placeId` as the location for moment fetches.
- **Why:** Scene IDs are not place IDs; spoken moments were filtered out.
- **Impact:** Player-sent moments surface in the chat after refresh/SSE.

### 2025-12-20: Stop using deprecated scene ids

- **What:** Scene `id` now defaults to `placeId` in view/narrator transforms and fallback scenes.
- **Why:** Scene IDs are deprecated; downstream logic expects place ids.
- **Impact:** Moment fetches and scene references stay aligned.

### 2025-12-20: Consolidated frontend implementation docs

- **What:** Merged code structure details into `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` and removed the duplicate `IMPLEMENTATION_Code_Structure.md`.
- **Why:** Resolve documentation duplication in the frontend implementation folder.
- **Files:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md`, `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`, `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md`

---

## KNOWN ISSUES

No critical issues currently tracked, but automated frontend tests are sparse
and the dual state hooks (`useGameState` + `useMoments`) add maintenance risk.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Stable; frontend surface area is mapped and documented, with tests as the main gap.

**Attention points:**
Keep hook ownership clear as the moment system evolves to prevent drift.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement or VIEW_Extend

**Where things are:**
- Entry point: `frontend/app/page.tsx`
- State management: `frontend/hooks/useGameState.ts`
- Types: `frontend/types/game.ts`
- API client: `frontend/lib/api.ts`

**Key context:**
The frontend talks to a Python FastAPI backend via REST + SSE. The moment system (`useMoments`) is newer and may eventually replace `useGameState`. Both currently coexist.

**Watch out for:**
- Two state systems (useGameState and useMoments) — understand which one handles what
- Backend must be running for live mode; otherwise falls back to static data

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Frontend is a working Next.js app that renders the game. It connects to the Python backend for state. The moment system is the newer approach for displaying narrative content.

**Decisions made:**
- Using Next.js 16 with App Router (modern React patterns)
- Tailwind for styling (consistent with dark atmospheric theme)
- Separate hooks for different concerns (game state vs moments)

**Needs your input:**
- Should the moment system fully replace the old scene system?
- Testing strategy — currently minimal

---

## TODO

### Immediate

- [x] Add DOCS reference to main entry file (frontend/app/page.tsx)

### Later

- [x] Create IMPLEMENTATION doc with detailed file structure
- [x] Create TEST doc when testing strategy is decided
- [ ] Set up test framework (Vitest/Jest)
- [ ] Add unit tests for transform functions
- IDEA: Add Playwright tests for key flows

---

## POINTERS

| What | Where |
|------|-------|
| Game state hook | `frontend/hooks/useGameState.ts` |
| Moment hook | `frontend/hooks/useMoments.ts` |
| API client | `frontend/lib/api.ts` |
| Types | `frontend/types/game.ts` |
| Scene components | `frontend/components/scene/` |
| Moment components | `frontend/components/moment/` |
| Backend API docs | `docs/physics/API_Physics.md` |

---

## Agent Observations

### Remarks
- The frontend doc chain is now centered on the implementation overview entry point.
- The algorithm doc now captures data flow, complexity, and helper calls in one place.

### Suggestions
- [ ] If `useGameState.ts` and `api.ts` continue to grow, consider extracting transformers and moment-specific API helpers.

### Propositions
- Keep component inventories in the `docs/frontend/scene/` module to avoid repeating long file lists here.

---

## GAPS

- Completed: Filled SCOPE and expanded short sections in `docs/frontend/PATTERNS_Presentation_Layer.md`.
- Completed: Logged the update in `docs/frontend/SYNC_Frontend.md`.
- Remaining: Commit the doc updates once the unexpected staged change in `docs/frontend/scenarios/SYNC_Scenario_Selection.md` is resolved.

--- 

## ARCHIVE

Older content archived to: `docs/frontend/archive/SYNC_archive_2024-12.md`


---

## ARCHIVE

Older content archived to: `SYNC_Frontend_archive_2025-12.md`


---

## SOURCE: frontend/lib/api.ts
// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md
/**
 * Blood Ledger API Client
 *
 * Connects frontend to the Python backend.
 */

import type { DialogueChunk, GraphMutation, SceneTree } from '@/types/game';
import { showToast } from '@/components/ui/Toast';

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Track if we've shown the backend down toast recently (debounce)
let lastBackendErrorTime = 0;
const TOAST_DEBOUNCE_MS = 5000;

function handleApiError(error: unknown, context: string) {
  const now = Date.now();
  // Only show toast if we haven't shown one recently
  if (now - lastBackendErrorTime > TOAST_DEBOUNCE_MS) {
    lastBackendErrorTime = now;
    showToast('Backend is unavailable. Check if the server is running.', 'error', 6000);
  }
  console.error(`[API] ${context}:`, error);
}

// -----------------------------------------------------------------------------
// Types for API responses
// -----------------------------------------------------------------------------

interface ApiPlace {
  'p.id': string;
  'p.name': string;
  'p.type': string;
  'p.mood'?: string;
}

interface ApiConnection {
  'p1.id': string;
  'p2.id': string;
  'r.path_distance'?: string;
  'r.path_difficulty'?: string;
}

interface ApiCharacter {
  'c.id': string;
  'c.name': string;
  'c.face'?: string;
  'c.voice_tone'?: string;
}

interface ApiNarrative {
  'n.id': string;
  'n.name': string;
  'n.content'?: string;
  'n.type': string;
  'n.weight'?: number;
}

// -----------------------------------------------------------------------------
// API Functions
// -----------------------------------------------------------------------------

export async function createPlaythrough(
  scenarioId: string,
  playerName: string,
  playerGender: string = 'male'
): Promise<{ playthrough_id: string; scenario: string; scene: SceneTree }> {
  try {
    const res = await fetch(`${API_BASE}/api/playthrough/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scenario_id: scenarioId,
        player_name: playerName,
        player_gender: playerGender
      }),
    });
    if (!res.ok) throw new Error(`Failed to create playthrough: ${res.statusText}`);
    return res.json();
  } catch (error) {
    handleApiError(error, 'createPlaythrough');
    throw error;
  }
}

export async function sendMoment(
  playthroughId: string,
  text: string,
  momentType: 'player_freeform' | 'player_click' | 'player_choice' = 'player_freeform'
): Promise<{ status: string; narrator_started: boolean; narrator_running: boolean }> {
  try {
    const res = await fetch(`${API_BASE}/api/moment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playthrough_id: playthroughId,
        text,
        moment_type: momentType,
      }),
    });
    if (!res.ok) throw new Error(`Failed to send moment: ${res.statusText}`);
    return res.json();
  } catch (error) {
    handleApiError(error, 'sendMoment');
    throw error;
  }
}

export async function getPlaythrough(playthroughId: string): Promise<{
  playthrough_id: string;
  has_player_notes: boolean;
  has_story_notes: boolean;
  has_world_injection: boolean;
}> {
  try {
    const res = await fetch(`${API_BASE}/api/playthrough/${playthroughId}`);
    if (!res.ok) throw new Error(`Playthrough not found: ${playthroughId}`);
    return res.json();
  } catch (error) {
    handleApiError(error, 'getPlaythrough');
    throw error;
  }
}

export async function getMap(playthroughId: string): Promise<{
  places: ApiPlace[];
  connections: ApiConnection[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/map`);
  if (!res.ok) throw new Error(`Failed to fetch map: ${res.statusText}`);
  return res.json();
}

export async function getFaces(playthroughId: string): Promise<{
  known_characters: ApiCharacter[];
  companions: ApiCharacter[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/faces`);
  if (!res.ok) throw new Error(`Failed to fetch faces: ${res.statusText}`);
  return res.json();
}

export async function getLedger(playthroughId: string): Promise<{
  items: ApiNarrative[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/ledger`);
  if (!res.ok) throw new Error(`Failed to fetch ledger: ${res.statusText}`);
  return res.json();
}

export async function getChronicle(playthroughId: string): Promise<{
  events: ApiNarrative[];
}> {
  const res = await fetch(`${API_BASE}/api/${playthroughId}/chronicle`);
  if (!res.ok) throw new Error(`Failed to fetch chronicle: ${res.statusText}`);
  return res.json();
}

export async function semanticQuery(
  playthroughId: string,
  query: string
): Promise<{
  results: Array<{
    id: string;
    name: string;
    type: string;
    content?: string;
    similarity: number;
  }>;
  query: string;
}> {
  const res = await fetch(
    `${API_BASE}/api/${playthroughId}/query?query=${encodeURIComponent(query)}`,
    { method: 'POST' }
  );
  if (!res.ok) throw new Error(`Query failed: ${res.statusText}`);
  return res.json();
}

// -----------------------------------------------------------------------------
// Moment Types
// -----------------------------------------------------------------------------

export interface Moment {
  id: string;
  text: string;
  type: string;
  status: string;
  weight: number;
  tone?: string;
  tick_created?: number;
  tick_spoken?: number;
  speaker?: string;
  clickable_words: string[];
}

export interface MomentTransition {
  from_id: string;
  to_id: string;
  trigger: string;
  require_words: string[];
  weight_transfer: number;
  consumes_origin: boolean;
}

export interface CurrentMomentsResponse {
  moments: Moment[];
  transitions: MomentTransition[];
  active_count: number;
}

export interface ClickMomentResponse {
  status: string;
  traversed: boolean;
  target_moment?: Moment;
  consumed_origin: boolean;
  new_active_moments: Moment[];
}

// SSE event handlers for moment stream
export interface MomentStreamCallbacks {
  onMomentActivated?: (data: { moment_id: string; weight: number; text: string }) => void;
  onMomentSpoken?: (data: { moment_id: string; tick: number }) => void;
  onMomentDecayed?: (data: { moment_id: string }) => void;
  onWeightUpdated?: (data: { moment_id: string; weight: number }) => void;
  onClickTraversed?: (data: { from_moment_id: string; to_moment_id: string; word: string; consumed_origin: boolean }) => void;
  onComplete?: () => void;
  onError?: (error: string) => void;
}

/**
 * Fetch current moments for a location.
 */
export async function fetchCurrentMoments(
  playthroughId: string,
  location: string,
  presentChars?: string[]
): Promise<CurrentMomentsResponse> {
  const params = new URLSearchParams({ location });
  if (presentChars?.length) {
    params.set('present_chars', presentChars.join(','));
  }

  const res = await fetch(`${API_BASE}/api/moments/current/${playthroughId}?${params}`);
  if (!res.ok) throw new Error(`Failed to fetch moments: ${res.statusText}`);
  return res.json();
}

/**
 * Click a word in a moment to traverse.
 */
export async function clickMoment(
  playthroughId: string,
  momentId: string,
  word: string,
  tick: number
): Promise<ClickMomentResponse> {
  const res = await fetch(`${API_BASE}/api/moments/click`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      playthrough_id: playthroughId,
      moment_id: momentId,
      word,
      tick
    }),
  });
  if (!res.ok) throw new Error(`Click failed: ${res.statusText}`);
  return res.json();
}

/**
 * Get moment statistics.
 */
export async function getMomentStats(): Promise<{
  stats: Record<string, number>;
}> {
  const res = await fetch(`${API_BASE}/api/moments/stats`);
  if (!res.ok) throw new Error(`Failed to fetch moment stats: ${res.statusText}`);
  return res.json();
}

/**
 * Subscribe to the moment stream SSE endpoint.
 * Returns a function to close the connection.
 */
export function subscribeToMomentStream(
  playthroughId: string,
  callbacks: MomentStreamCallbacks
): () => void {
  const url = `${API_BASE}/api/moments/stream/${playthroughId}`;
  const eventSource = new EventSource(url);

  eventSource.addEventListener('connected', () => {
    console.log('[SSE] Connected to moment stream');
  });

  eventSource.addEventListener('moment_activated', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onMomentActivated?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse moment_activated event:', e);
    }
  });

  eventSource.addEventListener('moment_spoken', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onMomentSpoken?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse moment_spoken event:', e);
    }
  });

  eventSource.addEventListener('moment_decayed', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onMomentDecayed?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse moment_decayed event:', e);
    }
  });

  eventSource.addEventListener('weight_updated', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onWeightUpdated?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse weight_updated event:', e);
    }
  });

  eventSource.addEventListener('click_traversed', (event) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onClickTraversed?.(data);
    } catch (e) {
      console.error('[SSE] Failed to parse click_traversed event:', e);
    }
  });

  eventSource.addEventListener('complete', () => {
    callbacks.onComplete?.();
  });

  eventSource.addEventListener('error', (event) => {
    console.error('[SSE] Stream error:', event);
    callbacks.onError?.('Stream connection error');
  });

  eventSource.addEventListener('ping', () => {
    // Keepalive, do nothing
  });

  // Return close function
  return () => {
    eventSource.close();
  };
}

// -----------------------------------------------------------------------------
// View API (Moment System)
// -----------------------------------------------------------------------------

export interface Place {
  id: string;
  name: string;
  type: string;
}

export interface CurrentView {
  location: Place;
  characters: Array<{
    id: string;
    name: string;
    face?: string;
  }>;
  things: Array<{
    id: string;
    name: string;
  }>;
  moments: Moment[];
  transitions: Array<{
    from: string;
    words: string[];
    to: string;
  }>;
}

/**
 * Get current view for a playthrough (replaces getCurrentScene).
 */
export async function getCurrentView(playthroughId: string): Promise<CurrentView | null> {
  try {
    const res = await fetch(`${API_BASE}/api/view/${playthroughId}`);
    if (!res.ok) {
      if (res.status === 404) return null;
      throw new Error(`Failed to get view: ${res.statusText}`);
    }
    return res.json();
  } catch (error) {
    handleApiError(error, 'getCurrentView');
    return null;
  }
}

// -----------------------------------------------------------------------------
// Health Check
// -----------------------------------------------------------------------------

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}


---

## SOURCE: frontend/hooks/useGameState.ts
// DOCS: docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md
'use client';

import { useState, useEffect, useCallback } from 'react';
import { GameState, MapRegion, Character, LedgerEntry, ChronicleEntry, Scene, Voice, SceneTree } from '@/types/game';
import * as api from '@/lib/api';

// Default playthrough for development
const DEFAULT_PLAYTHROUGH = 'beorn';

// Loading messages that update as we progress
const LOADING_STAGES = [
  "Awakening the Narrator...",
  "The world stirs...",
  "Gathering the threads of your story...",
  "The scene takes shape...",
];

interface UseGameStateResult {
  gameState: GameState | null;
  playthroughId: string;
  isLoading: boolean;
  loadingMessage: string;
  error: string | null;
  isConnected: boolean;
  needsOpening: boolean;  // True if no scene.json or default content
  refresh: () => Promise<void>;
  sendAction: (action: string) => Promise<void>;
  clickWord: (word: string, path?: string[]) => Promise<void>;
}

export function useGameState(playthroughId: string = DEFAULT_PLAYTHROUGH): UseGameStateResult {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loadingMessage, setLoadingMessage] = useState(LOADING_STAGES[0]);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [needsOpening, setNeedsOpening] = useState(false);

  const fetchGameState = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    setLoadingMessage(LOADING_STAGES[0]);

    try {
      // Check backend health
      const healthy = await api.checkHealth();
      setIsConnected(healthy);

      if (!healthy) {
        setError('Backend not available');
        setIsLoading(false);
        return;
      }

      setLoadingMessage(LOADING_STAGES[1]);

      // Fetch view data in parallel
      const [mapData, facesData, ledgerData, chronicleData] = await Promise.all([
        api.getMap(playthroughId),
        api.getFaces(playthroughId),
        api.getLedger(playthroughId),
        api.getChronicle(playthroughId),
      ]);

      setLoadingMessage(LOADING_STAGES[2]);

      // Try to load current view (moment system)
      let scene: Scene;
      let voices: Voice[] = [];
      let sceneTree: SceneTree | undefined;

      const view = await api.getCurrentView(playthroughId);
      // Backend returns active_moments, frontend type says moments - handle both
      const moments = (view as any)?.active_moments || view?.moments || [];
      if (view && moments.length > 0) {
        // Normalize view to always have moments field
        const normalizedView = { ...view, moments } as api.CurrentView;
        // Transform view to scene format
        scene = transformViewToScene(normalizedView);
        voices = transformMomentsToVoices(moments);
        // Scene tree is the raw view with clickable moments
        sceneTree = normalizedView as unknown as SceneTree;
        setNeedsOpening(false);
        console.log('Loaded view from moment system');
      } else {
        // No moments yet - redirect to opening
        console.log('No moments found, needs opening');
        setNeedsOpening(true);
        setIsLoading(false);
        return;
      }

      // Transform to GameState format
      const map: MapRegion[] = [{
        id: 'region_north',
        name: 'The North',
        locations: mapData.places.map((p) => ({
          id: p['p.id'],
          name: p['p.name'],
          type: mapPlaceType(p['p.type']),
          position: { x: 50, y: 50 },
          discovered: true,
          current: p['p.id'] === 'place_camp',
          connected: mapData.connections
            .filter((c) => c['p1.id'] === p['p.id'])
            .map((c) => c['p2.id']),
        })),
      }];

      const characters: Character[] = [
        ...facesData.companions.map((c) => ({
          id: c['c.id'],
          name: c['c.name'],
          description: '',
          face: c['c.face'] || null,
          location: 'The Camp',
          isCompanion: true,
          isPresent: true,
        })),
        ...facesData.known_characters.map((c) => ({
          id: c['c.id'],
          name: c['c.name'],
          description: '',
          face: c['c.face'] || null,
          location: 'Unknown',
          isCompanion: false,
          isPresent: false,
        })),
      ];

      const ledger: LedgerEntry[] = ledgerData.items.map((n) => ({
        id: n['n.id'],
        type: (n['n.type'] as 'debt' | 'oath' | 'blood') || 'oath',
        subject: n['n.name'],
        content: n['n.content'] || '',
        resolved: false,
      }));

      const chronicle: ChronicleEntry[] = chronicleData.events.map((e, i) => ({
        id: e['n.id'] || `event_${i}`,
        day: i + 1,
        location: 'The North',
        content: e['n.content'] || e['n.name'],
        isPlayerWritten: false,
      }));

      // Build game state
      const state: GameState = {
        player: {
          name: 'Rolf',
          title: null,
          day: 1,
          location: scene.location,
        },
        currentScene: scene,
        sceneTree,  // Raw Narrator response with clickables
        characters,
        voices,
        chronicle,
        ledger,
        conversations: [],
        map,
      };

      setGameState(state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load game state');
    } finally {
      setIsLoading(false);
    }
  }, [playthroughId]);

  const sendAction = useCallback(async (action: string) => {
    setLoadingMessage("The world responds...");
    try {
      // Queue the moment - scene updates come via SSE stream
      await api.sendMoment(playthroughId, action, 'player_freeform');
      // Note: Scene updates arrive via SSE, not from this call
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Action failed');
    }
  }, [playthroughId]);

  // Note: clickWord is deprecated - use moment system's clickMoment instead
  const clickWord = useCallback(async (_word: string, _path: string[] = []) => {
    console.warn('[useGameState] clickWord is deprecated. Use moment system instead.');
  }, []);

  useEffect(() => {
    fetchGameState();
  }, [fetchGameState]);

  // SSE subscription for real-time moment updates
  useEffect(() => {
    if (!playthroughId || playthroughId === DEFAULT_PLAYTHROUGH) return;

    console.log('[SSE] Subscribing to moment stream for', playthroughId);

    const unsubscribe = api.subscribeToMomentStream(playthroughId, {
      onMomentActivated: (data) => {
        console.log('[SSE] Moment activated:', data.moment_id);
        // Refresh to get full moment data
        fetchGameState();
      },
      onMomentSpoken: (data) => {
        console.log('[SSE] Moment spoken:', data.moment_id);
        // Update moment status in local state if needed
        fetchGameState();
      },
      onMomentDecayed: (data) => {
        console.log('[SSE] Moment decayed:', data.moment_id);
        fetchGameState();
      },
      onWeightUpdated: (data) => {
        console.log('[SSE] Weight updated:', data.moment_id, data.weight);
        // Could update weight in place, but full refresh is simpler
      },
      onClickTraversed: (data) => {
        console.log('[SSE] Click traversed:', data.word, data.from_moment_id, '->', data.to_moment_id);
        fetchGameState();
      },
      onError: (error) => {
        console.warn('[SSE] Stream error (will reconnect):', error);
      }
    });

    return () => {
      console.log('[SSE] Unsubscribing from moment stream');
      unsubscribe();
    };
  }, [playthroughId, fetchGameState]);

  return {
    gameState,
    playthroughId,
    isLoading,
    loadingMessage,
    error,
    isConnected,
    needsOpening,
    refresh: fetchGameState,
    sendAction,
    clickWord,
  };
}

// Helper: Map place type to SceneType
function mapPlaceType(type: string): Scene['type'] {
  const mapping: Record<string, Scene['type']> = {
    camp: 'CAMP',
    city: 'GATE',
    ruin: 'VILLAGE',
    village: 'VILLAGE',
    road: 'ROAD',
    hold: 'HOLD',
    forest: 'FOREST',
    church: 'CHURCH',
  };
  return mapping[type?.toLowerCase()] || 'CAMP';
}

// Helper: Transform Narrator scene response
function transformScene(s: Record<string, unknown>): Scene {
  const location = s.location as Record<string, string> | undefined;
  const characters = s.characters as string[] | undefined;

  // Handle narration - can be {raw, clickables} object or array of {text}
  const narration = s.narration as { raw?: string; clickables?: string[] } | Array<{ text: string }> | undefined;
  let atmosphereText: string[] = [];

  if (s.atmosphere) {
    atmosphereText = s.atmosphere as string[];
  } else if (narration) {
    if ('raw' in narration && typeof narration.raw === 'string') {
      // Narrator format: {raw: "...", clickables: [...]}
      atmosphereText = [narration.raw];
    } else if (Array.isArray(narration)) {
      // Array format: [{text: "..."}, ...]
      atmosphereText = narration.map(n => n.text);
    }
  }

  if (atmosphereText.length === 0) {
    atmosphereText = ['The scene unfolds before you...'];
  }

  // Extract clickables from narration
  const clickables = (narration && 'clickables' in narration)
    ? (narration.clickables as string[]) || []
    : [];

  const placeId = (location?.place as string) || undefined;

  return {
    id: placeId || (s.id as string) || 'scene_generated',
    placeId,
    type: mapPlaceType((location?.place as string) || 'camp'),
    name: (location?.name as string) || 'THE CAMP',
    location: (location?.region as string) || 'The North',
    timeOfDay: ((location?.time as string)?.toUpperCase() || 'NIGHT') as Scene['timeOfDay'],
    weather: 'CLEAR',
    atmosphere: atmosphereText,
    hotspots: [
      // Clickable words from narration
      ...clickables.map((word: string, i: number) => ({
        id: `click_${word}`,
        type: 'object' as const,
        name: word,
        description: `Click to explore: ${word}`,
        position: { x: 20 + (i * 15) % 60, y: 70 + (i % 3) * 10 },
        icon: '👁',
        actions: [
          { id: `click_${word}`, label: word },
        ],
      })),
      // Characters in scene
      ...(characters || []).map((charId: string, i: number) => {
        const charName = charId.replace('char_', '');
        return {
          id: charId,
          type: 'person' as const,
          name: charName.replace(/^\w/, c => c.toUpperCase()),
          description: 'Present in the scene.',
          position: { x: 60 + i * 10, y: 40 + i * 5 },
          icon: '🧍',
          imageUrl: `/playthroughs/default/images/characters/${charId}.png`,
          actions: [
            { id: `talk_${charId}`, label: 'Talk' },
          ],
        };
      }),
    ],
    actions: [
      { id: 'look_around', label: 'Look around' },
      { id: 'wait', label: 'Wait' },
    ],
  };
}

// Helper: Transform Narrator voices
function transformVoices(s: Record<string, unknown>): Voice[] {
  const voices = s.voices as Array<{
    source: string;
    text: string;
    weight: number;
  }> | undefined;

  if (!voices) return [];

  return voices.map((v, i) => ({
    id: `voice_${i}`,
    type: 'memory' as const,
    source: v.source,
    content: v.text,
    weight: v.weight,
  }));
}

// Helper: Transform moment system view to Scene format
function transformViewToScene(view: api.CurrentView): Scene {
  const location = view.location;

  // Get atmosphere from narration moments
  const narrationMoments = view.moments.filter(m => m.type === 'narration' || m.type === 'action');
  const atmosphereText = narrationMoments.map(m => m.text);

  if (atmosphereText.length === 0) {
    atmosphereText.push('The scene unfolds before you...');
  }

  // Build clickable words from transitions
  const clickables: string[] = [];
  for (const t of view.transitions) {
    for (const word of t.words) {
      if (!clickables.includes(word)) {
        clickables.push(word);
      }
    }
  }

  return {
    id: location.id,
    placeId: location.id,
    type: mapPlaceType(location.type),
    name: location.name.toUpperCase(),
    location: 'The North',
    timeOfDay: 'NIGHT',
    weather: 'CLEAR',
    atmosphere: atmosphereText,
    hotspots: [
      // Clickable words from moments
      ...clickables.map((word, i) => ({
        id: `click_${word}`,
        type: 'object' as const,
        name: word,
        description: `Click to explore: ${word}`,
        position: { x: 20 + (i * 15) % 60, y: 70 + (i % 3) * 10 },
        icon: '👁',
        actions: [{ id: `click_${word}`, label: word }],
      })),
      // Characters in scene
      ...view.characters.map((char, i) => ({
        id: char.id,
        type: 'person' as const,
        name: char.name,
        description: 'Present in the scene.',
        position: { x: 60 + i * 10, y: 40 + i * 5 },
        icon: '🧍',
        imageUrl: `/playthroughs/default/images/characters/${char.id}.png`,
        actions: [{ id: `talk_${char.id}`, label: 'Talk' }],
      })),
    ],
    actions: [
      { id: 'look_around', label: 'Look around' },
      { id: 'wait', label: 'Wait' },
    ],
  };
}

// Helper: Transform moments to voices
function transformMomentsToVoices(moments: api.Moment[]): Voice[] {
  // Filter for dialogue moments with speakers
  const dialogueMoments = moments.filter(m => m.type === 'dialogue' && m.speaker);

  return dialogueMoments.map((m, i) => ({
    id: `voice_${m.id || i}`,
    type: 'memory' as const,
    source: m.speaker || 'Unknown',
    content: m.text,
    weight: m.weight,
  }));
}

// Helper: Create fallback scene when Narrator unavailable
function createFallbackScene(
  mapData: { places: Array<{ 'p.id': string; 'p.name': string; 'p.type': string; 'p.mood'?: string }> },
  facesData: { companions: Array<{ 'c.id': string; 'c.name': string }> }
): Scene {
  const camp = mapData.places.find(p => p['p.id'] === 'place_camp');

  return {
    id: 'place_camp',
    placeId: 'place_camp',
    type: 'CAMP',
    name: camp?.['p.name'] || 'THE CAMP',
    location: 'The North',
    timeOfDay: 'NIGHT',
    weather: 'CLEAR',
    atmosphere: [
      'Cold night. Stars visible through bare branches.',
      'The fire crackles, throwing shadows.',
      camp?.['p.mood'] ? `The air feels ${camp['p.mood']}.` : '',
    ].filter(Boolean),
    hotspots: facesData.companions.map((c) => ({
      id: c['c.id'],
      type: 'person' as const,
      name: c['c.name'],
      description: `${c['c.name']} is here.`,
      position: { x: 60, y: 50 },
      icon: '🧍',
      actions: [
        { id: `talk_${c['c.id']}`, label: 'Talk', description: `Speak with ${c['c.name']}` },
      ],
    })),
    actions: [
      { id: 'look_around', label: 'Look around', description: 'Survey the camp' },
      { id: 'rest', label: 'Rest', description: 'Get some sleep' },
    ],
  };
}


---

## SOURCE: frontend/hooks/useMoments.ts
// DOCS: docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md
'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  fetchCurrentMoments,
  clickMoment,
  subscribeToMomentStream,
  type Moment,
  type MomentTransition,
  type CurrentMomentsResponse,
  type ClickMomentResponse,
} from '@/lib/api';

/**
 * State returned by useMoments hook.
 */
interface MomentsState {
  /** Spoken moments (history) */
  spokenMoments: Moment[];
  /** Currently active moments */
  activeMoments: Moment[];
  /** All available transitions */
  transitions: MomentTransition[];
  /** Is a traversal in progress */
  isLoading: boolean;
  /** Last error, if any */
  error: string | null;
}

/**
 * Actions returned by useMoments hook.
 */
interface MomentsActions {
  /** Handle a word click in a moment */
  clickWord: (momentId: string, word: string) => Promise<void>;
  /** Refresh current moments from API */
  refresh: () => Promise<void>;
  /** Clear error state */
  clearError: () => void;
}

/**
 * Hook for managing moment state.
 *
 * Connects to the moment API and SSE stream for real-time updates.
 * Handles click traversal and state management.
 *
 * @example
 * const { spokenMoments, activeMoments, clickWord, isLoading } = useMoments({
 *   playthroughId: 'pt_abc123',
 *   location: 'place_camp',
 *   tick: 1234
 * });
 */
export function useMoments({
  playthroughId,
  location,
  tick,
  autoConnect = true,
}: {
  playthroughId: string;
  location?: string;
  tick: number;
  autoConnect?: boolean;
}): MomentsState & MomentsActions {
  const [spokenMoments, setSpokenMoments] = useState<Moment[]>([]);
  const [activeMoments, setActiveMoments] = useState<Moment[]>([]);
  const [transitions, setTransitions] = useState<MomentTransition[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch current moments from API
  const fetchMoments = useCallback(async () => {
    if (!playthroughId || !location) return;

    try {
      const data = await fetchCurrentMoments(playthroughId, location);

      // Separate spoken and active
      const spoken = data.moments.filter(m => m.status === 'spoken');
      const active = data.moments.filter(m =>
        m.status === 'active' || m.status === 'possible'
      );

      setSpokenMoments(spoken);
      setActiveMoments(active);
      setTransitions(data.transitions);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch moments:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
  }, [playthroughId, location]);

  // Handle word click
  const handleClickWord = useCallback(
    async (momentId: string, word: string) => {
      if (isLoading) return;

      setIsLoading(true);
      setError(null);

      try {
        const data = await clickMoment(playthroughId, momentId, word, tick);

        if (data.traversed && data.target_moment) {
          // Move origin to spoken (if consumed)
          if (data.consumed_origin) {
            setActiveMoments(prev => {
              const origin = prev.find(m => m.id === momentId);
              if (origin) {
                setSpokenMoments(s => [...s, { ...origin, status: 'spoken' }]);
              }
              return prev.filter(m => m.id !== momentId);
            });
          }

          // Add new active moments
          setActiveMoments(prev => [...prev, ...data.new_active_moments]);
        }
      } catch (err) {
        console.error('Click failed:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    },
    [playthroughId, tick, isLoading]
  );

  // Connect to SSE stream for real-time updates
  useEffect(() => {
    if (!autoConnect || !playthroughId) return;

    // Connect to moment stream using API function
    const close = subscribeToMomentStream(playthroughId, {
      onMomentActivated: (data) => {
        setActiveMoments(prev => {
          // Avoid duplicates
          if (prev.some(m => m.id === data.moment_id)) return prev;
          // Create minimal moment from event data
          return [...prev, {
            id: data.moment_id,
            text: data.text,
            type: 'narration',
            status: 'active',
            weight: data.weight,
            clickable_words: [],
          }];
        });
      },
      onMomentSpoken: (data) => {
        // Move from active to spoken
        setActiveMoments(prev => {
          const moment = prev.find(m => m.id === data.moment_id);
          if (moment) {
            setSpokenMoments(s => [...s, { ...moment, status: 'spoken' }]);
            return prev.filter(m => m.id !== data.moment_id);
          }
          // Player-originated moments may skip "active" state; refresh view.
          fetchMoments();
          return prev;
        });
      },
      onWeightUpdated: (data) => {
        setActiveMoments(prev =>
          prev.map(m =>
            m.id === data.moment_id ? { ...m, weight: data.weight } : m
          )
        );
      },
      onError: (error) => {
        console.error('[useMoments] SSE error:', error);
        setError('Connection lost. Reconnecting...');
      }
    });

    return () => {
      close();
    };
  }, [autoConnect, playthroughId, fetchMoments]);

  // Initial fetch
  useEffect(() => {
    fetchMoments();
  }, [fetchMoments]);

  return {
    spokenMoments,
    activeMoments,
    transitions,
    isLoading,
    error,
    clickWord: handleClickWord,
    refresh: fetchMoments,
    clearError: () => setError(null),
  };
}

export default useMoments;


---

## SOURCE: frontend/app/page.tsx
// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md
'use client';

import { useState, useEffect } from 'react';
import { GameClient } from '@/components/GameClient';
import gameStateData from '@/data/game-state.json';
import { GameState } from '@/types/game';

export default function Home() {
  const [playthroughId, setPlaythroughId] = useState<string | undefined>(undefined);

  // Read playthrough ID from session storage on mount
  useEffect(() => {
    const stored = sessionStorage.getItem('playthroughId');
    if (stored) {
      setPlaythroughId(stored);
    }
  }, []);

  // Static data as fallback when backend unavailable
  const fallbackState = gameStateData as GameState;

  return <GameClient fallbackState={fallbackState} playthroughId={playthroughId} />;
}


---

## SOURCE: frontend/components/GameClient.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useGameState } from '@/hooks/useGameState';
import { useTempo } from '@/hooks/useTempo';
import { GameLayout } from '@/components/GameLayout';
import { GameState } from '@/types/game';

interface GameClientProps {
  fallbackState: GameState;
  playthroughId?: string;
}

// Immersive loading messages (generic, not plot-specific)
const LOADING_MESSAGES = [
  "The fire crackles in the darkness...",
  "Shadows dance at the edge of vision...",
  "The wind carries distant voices...",
  "Memory stirs in the silence...",
  "The world holds its breath...",
];

export function GameClient({ fallbackState, playthroughId: propPlaythroughId }: GameClientProps) {
  const router = useRouter();
  const { gameState, playthroughId, isLoading, error, isConnected, needsOpening, loadingMessage, sendAction } = useGameState(propPlaythroughId);
  const { speed, tick } = useTempo(playthroughId);

  // Redirect to start screen if no scene exists
  useEffect(() => {
    if (needsOpening && !isLoading) {
      router.replace('/start');
    }
  }, [needsOpening, isLoading, router]);

  // Handle player actions (free input)
  const handleAction = async (action: string) => {
    console.log('Action:', action);
    await sendAction(action);
  };

  // Show immersive loading state (also while redirecting to opening)
  if (isLoading || needsOpening) {
    const message = loadingMessage || LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)];

    return (
      <div className="flex items-center justify-center min-h-screen bg-stone-950">
        <div className="max-w-lg text-center px-8">
          {/* Atmospheric glow */}
          <div className="relative mb-8">
            <div className="absolute inset-0 blur-3xl bg-amber-900/20 rounded-full" />
            <div className="relative text-6xl animate-pulse">🔥</div>
          </div>

          {/* Loading message */}
          <p className="text-stone-400 text-lg italic leading-relaxed mb-6">
            {message}
          </p>

          {/* Subtle progress indicator */}
          <div className="flex justify-center gap-1">
            <div className="w-2 h-2 rounded-full bg-stone-600 animate-pulse" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 rounded-full bg-stone-600 animate-pulse" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 rounded-full bg-stone-600 animate-pulse" style={{ animationDelay: '300ms' }} />
          </div>

          {/* Connection status */}
          <p className="text-stone-600 text-xs mt-8">
            {isConnected ? 'Connected to the world...' : 'Awakening the Narrator...'}
          </p>
        </div>
      </div>
    );
  }

  // Use live data if connected, fallback otherwise
  const state = isConnected && gameState ? gameState : fallbackState;

  return (
    <>
      {/* Top right: Connection status */}
      <div className="fixed top-2 right-2 z-50">
        <div
          className={`px-2 py-1 rounded text-xs ${
            isConnected
              ? 'bg-green-900/50 text-green-300'
              : 'bg-amber-900/50 text-amber-300'
          }`}
        >
          {isConnected ? '● Live' : '○ Static'}
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div className="fixed top-2 left-2 right-16 z-50 bg-red-900/80 text-red-200 px-3 py-1 rounded text-sm">
          {error}
        </div>
      )}

      <GameLayout
        initialState={state}
        playthroughId={playthroughId}
        onAction={handleAction}
        tick={tick}
        speed={speed}
      />
    </>
  );
}

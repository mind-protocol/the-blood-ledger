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

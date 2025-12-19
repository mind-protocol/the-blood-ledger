# Frontend Data Flow — Algorithm

```
UPDATED: 2025-12-19
STATUS: CANONICAL (describes desired state)
```

---

## Overview

How data flows between frontend and backend for the moment system.

---

## Two Paths

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
| `frontend/hooks/useGameState.ts` | Needs SSE integration |
| `frontend/components/scene/CenterStage.tsx` | Has polling hack to remove |
| `engine/infrastructure/api/moments.py` | SSE endpoint |

---

## Chain

- PATTERNS: `docs/frontend/PATTERNS_Presentation_Layer.md`
- BEHAVIORS: `docs/frontend/BEHAVIORS_Frontend_State_And_Interaction.md`
- **ALGORITHM: This file**
- IMPLEMENTATION: `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- SYNC: `docs/frontend/SYNC_Frontend.md`

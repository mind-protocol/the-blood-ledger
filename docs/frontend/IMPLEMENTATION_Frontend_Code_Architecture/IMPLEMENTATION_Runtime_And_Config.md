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
frontend/app/page.tsx
frontend/app/layout.tsx
frontend/app/start/page.tsx
frontend/app/map/page.tsx
frontend/app/scenarios/page.tsx
frontend/components/GameClient.tsx
frontend/components/GameLayout.tsx
frontend/components/Providers.tsx
frontend/components/scene/
frontend/components/moment/
frontend/components/map/
frontend/components/panel/
frontend/components/voices/
frontend/components/chronicle/
frontend/components/minimap/
frontend/components/debug/
frontend/components/ui/
frontend/hooks/useGameState.ts
frontend/hooks/useMoments.ts
frontend/lib/api.ts
frontend/lib/map/
frontend/types/game.ts
frontend/types/moment.ts
frontend/types/map.ts
frontend/data/game-state.json
frontend/public/playthroughs/
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
- **Moment UI:** `frontend/components/moment/MomentDebugPanel.tsx` (~221L), `frontend/components/moment/MomentDisplay.tsx` (~201L).
- **Chronicle UI:** `frontend/components/chronicle/ChroniclePanel.tsx` (~200L).
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
- **Moment click:** `ClickableText` → `useMoments#clickWord` → API → update active/spoken state.
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

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

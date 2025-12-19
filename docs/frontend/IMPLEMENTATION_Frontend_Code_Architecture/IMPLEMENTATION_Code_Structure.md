# Frontend — Implementation: Code Structure

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
THIS:            IMPLEMENTATION_Code_Structure.md (you are here)
TEST:            ../TEST_Frontend_Coverage.md
SYNC:            ../SYNC_Frontend.md

IMPL:            frontend/app/page.tsx
```

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

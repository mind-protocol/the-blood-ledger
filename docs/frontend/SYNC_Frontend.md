# Frontend — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
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

## RECENT CHANGES

### 2025-12-19: Link toast UI component to frontend docs

- **What:** Added a DOCS reference in `frontend/components/ui/Toast.tsx` and listed it as an entry point in `modules.yaml`.
- **Why:** Ensure the shared UI toast component is discoverable through the frontend documentation chain.
- **Files:** `frontend/components/ui/Toast.tsx`, `modules.yaml`
- **Struggles/Insights:** None.

### 2025-12-19: Link moment component docs to Scene module

- **What:** Noted Scene-owned documentation for moment components in `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`.
- **Why:** Keep moment UI documentation aligned with the Scene module mapping.
- **Files:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- **Struggles/Insights:** None.

---

## KNOWN ISSUES

No critical issues currently tracked.

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

## ARCHIVE

Older content archived to: `SYNC_Frontend_archive_2025-12.md`

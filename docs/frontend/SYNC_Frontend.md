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

## MATURITY

**What's canonical (v1):**
- Next.js 16 app structure
- Scene display with atmospheric UI
- useGameState hook for backend connection
- useMoments hook for moment system
- Right panel with Chronicle/Ledger/Conversations tabs
- Map view with fog of war
- Moment display with clickable text
- SSE streaming integration

**What's still being designed:**
- Testing strategy (Playwright mentioned in docs but not yet implemented)
- Component-level tests

**What's proposed (v2+):**
- Storybook for component development
- Better offline/fallback experience

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

### 2025-12-19: Link chronicle component to frontend docs

- **What:** Added DOCS reference in `frontend/components/chronicle/ChroniclePanel.tsx`
- **Why:** Ensure the chronicle component is discoverable via `ngram context`
- **Files:** `frontend/components/chronicle/ChroniclePanel.tsx`

### 2025-12-19: Link voices component to frontend docs

- **What:** Added DOCS reference in `frontend/components/voices/Voices.tsx` and listed it as a frontend entry point
- **Why:** Ensure the voices component is discoverable via `ngram context` and mapped in the module manifest
- **Files:** `frontend/components/voices/Voices.tsx`, `modules.yaml`

### 2025-12-19: Map frontend module in manifest

- **What:** Added frontend module mapping in modules.yaml for `frontend/**` (covers `frontend/components`)
- **Why:** Ensure code/docs are linked and validated by ngram
- **Files:** `modules.yaml`
- **Status:** Mapping now present in manifest for repair 26-UNDOCUMENTED-frontend

### 2025-12-19: Implement SSE integration per Migration Path

- **What:** Added SSE subscription to useGameState.ts, removed polling hack from CenterStage.tsx
- **Why:** Replace setTimeout polling with real-time SSE event handling
- **Files:**
  - `frontend/hooks/useGameState.ts` — Added useEffect with subscribeToMomentStream
  - `frontend/components/scene/CenterStage.tsx` — Removed setTimeout polling
  - `docs/frontend/ALGORITHM_Frontend_Data_Flow.md` — Updated checklist and code examples

### 2025-12-19: Complete documentation chain created

- **What:** Created full documentation chain for frontend module
- **Why:** INCOMPLETE_CHAIN issue detected by ngram doctor
- **Files created:**
  - `BEHAVIORS_Frontend_State_And_Interaction.md` — Observable behaviors (loading, clicks, SSE)
  - `ALGORITHM_Frontend_Data_Flow.md` — Data flow and state transformation logic
  - `VALIDATION_Frontend_Invariants.md` — Invariants and verification procedures
  - `IMPLEMENTATION_Frontend_Code_Architecture.md` — Code structure and file responsibilities
  - `TEST_Frontend_Coverage.md` — Test strategy and coverage gaps
- **Files updated:**
  - `PATTERNS_Presentation_Layer.md` — Updated CHAIN section links
  - `SYNC_Frontend.md` — Added CHAIN section, updated todos

### 2025-12-18: Initial documentation created

- **What:** Created module documentation for frontend
- **Why:** Frontend had 52 files but no module mapping in docs
- **Files:** `docs/frontend/PATTERNS_Presentation_Layer.md`, `docs/frontend/SYNC_Frontend.md`

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

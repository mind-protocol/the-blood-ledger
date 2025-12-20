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

### 2025-12-21: Resume SSE subscription for default playthrough

- **What:** `frontend/hooks/useGameState.ts` now subscribes to `/api/moments/stream/{playthrough_id}` whenever a playthrough ID is available, including the default `'beorn'` dev playthrough.
- **Why:** The demo/default path previously hit the guard that skipped SSE, so player input never triggered `moment_spoken`/`moment_activated` refreshes. Energy/canon documentation underlines that action → energy → canon should always flow through the stream.
- **Impact:** Sending messages on the default playthrough now triggers the documented SSE-driven refresh, closing the "no response" experience loop.

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

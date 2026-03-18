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
HEALTH:          ./HEALTH_Frontend_Runtime.md
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/app/page.tsx, frontend/app/layout.tsx, frontend/app/globals.css, frontend/lib/api.ts, frontend/types/game.ts, frontend/types/map.ts, frontend/components/ui/Toast.tsx, frontend/components/voices/Voices.tsx
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
- `frontend/types/moment.ts` — TypeScript contracts for moment payloads

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

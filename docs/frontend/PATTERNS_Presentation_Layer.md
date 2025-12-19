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
BEHAVIORS:       (not yet documented)
ALGORITHM:       (not yet documented)
VALIDATION:      (not yet documented)
IMPLEMENTATION:  (not yet documented)
TEST:            (not yet documented)
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
| `engine/api/` | REST endpoints for game state |
| `engine/api/moments.py` | Moments API for new display system |
| `docs/physics/` | Moment system architecture |
| `docs/infrastructure/async/` | SSE streaming patterns |

---

## INSPIRATIONS

- **Disco Elysium** — Voices as internal thoughts, click-to-explore
- **80 Days** — Narrative presentation, atmospheric UI
- **Twine/Ink** — Clickable narrative words

---

## WHAT THIS DOES NOT SOLVE

- **Game logic** — Lives in Python backend
- **Persistence** — Graph database on backend
- **LLM orchestration** — Narrator module on backend
- **Image generation** — Ideogram API via Python tools
- **Authentication** — Not implemented (single-player game)

---

## GAPS / IDEAS / QUESTIONS

- [ ] TEST doc: Document component testing approach
- [ ] IMPLEMENTATION doc: Detail file structure and data flows
- QUESTION: Should useMoments replace useGameState entirely, or coexist?
- IDEA: Storybook for component development

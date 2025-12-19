# Archived: SYNC_Frontend.md

Archived on: 2025-12-19
Original file: SYNC_Frontend.md

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


## RECENT CHANGES

### 2025-12-19: Link debug component to frontend docs

- **What:** Added DOCS reference in `frontend/components/debug/DebugPanel.tsx`
- **Why:** Ensure the debug panel is discoverable via `ngram context`
- **Files:** `frontend/components/debug/DebugPanel.tsx`

### 2025-12-19: Link chronicle component to frontend docs

- **What:** Added DOCS reference in `frontend/components/chronicle/ChroniclePanel.tsx`
- **Why:** Ensure the chronicle component is discoverable via `ngram context`
- **Files:** `frontend/components/chronicle/ChroniclePanel.tsx`

### 2025-12-19: Link voices component to frontend docs

- **What:** Added DOCS reference in `frontend/components/voices/Voices.tsx`
- **Why:** Ensure the voices component is discoverable via `ngram context` (manifest already covered `frontend/**`)
- **Files:** `frontend/components/voices/Voices.tsx`

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


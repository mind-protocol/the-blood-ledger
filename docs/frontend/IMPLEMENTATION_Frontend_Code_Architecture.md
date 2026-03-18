# Frontend — Implementation: Code Architecture (Overview)

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
THIS:            IMPLEMENTATION_Frontend_Code_Architecture.md (you are here)
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/app/page.tsx, frontend/hooks/useMoments.ts, frontend/components/debug/DebugPanel.tsx
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## SUMMARY

The frontend is a Next.js App Router UI that renders the game state provided by the backend. State logic lives in hooks, while components focus on presentation and interaction.

**Key components:**
- `frontend/components/chronicle/ChroniclePanel.tsx` — Chronicle entry list and write flow.

---

## CONTENTS

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` — Entry points, code structure, runtime flow, configuration, and doc links

---

## LOGIC CHAINS

### LC1: Initial app render and fallback selection

`frontend/app/page.tsx` → `frontend/components/GameClient.tsx` loads bootstrap state, then selects live vs fallback view based on connection status and hook readiness.

### LC2: Live updates via hooks and SSE

`frontend/hooks/useGameState.ts` → fetches REST state, subscribes to SSE stream, then pushes updates into React state so scene and panel components re-render.

---

## CONCURRENCY MODEL

The frontend runs on the browser event loop with React scheduling async fetch and SSE callbacks; no explicit worker threads are used, and state updates serialize through React setState batching.

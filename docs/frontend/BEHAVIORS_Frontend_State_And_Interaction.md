# Frontend — Behaviors: State Management and User Interaction

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against current implementation
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
THIS:            BEHAVIORS_Frontend_State_And_Interaction.md (you are here)
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/app/page.tsx
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Initial Game State Loading

```
GIVEN:  User navigates to the game page
WHEN:   Page mounts
THEN:   useGameState fetches state from backend API endpoints in parallel:
        - /api/{playthrough}/map
        - /api/{playthrough}/faces
        - /api/{playthrough}/ledger
        - /api/{playthrough}/chronicle
        - /api/view/{playthrough}
AND:    Loading messages cycle through atmospheric stages
AND:    isConnected is set based on backend health check
```

### B2: Backend Unavailable Fallback

```
GIVEN:  Backend health check fails
WHEN:   useGameState attempts to fetch game state
THEN:   isConnected is set to false
AND:    Error message is displayed
AND:    Toast notification shows "Backend is unavailable"
```

### B3: Moment System Interaction

```
GIVEN:  Scene is loaded with active moments
WHEN:   User clicks a word in a moment's text
THEN:   clickMoment API is called with momentId, word, and current tick
AND:    Origin moment may be consumed (moved to spoken)
AND:    New active moments are added to state
AND:    UI updates to reflect new moment state
```

### B4: SSE Real-Time Updates

```
GIVEN:  User is connected to a playthrough
WHEN:   Backend emits SSE event (moment_activated, moment_spoken, weight_updated)
THEN:   useMoments hook processes the event
AND:    State is updated without full page refresh
AND:    UI reflects changes in real-time
```

### B5: Player Action Submission

```
GIVEN:  User has entered text in the action input
WHEN:   User submits the action
THEN:   sendMoment API is called with action text
AND:    Backend queues the moment for Narrator processing
AND:    Scene updates arrive via SSE stream (not from API response)
```

### B6: Opening Redirect

```
GIVEN:  Backend returns no moments for a playthrough
WHEN:   useGameState finishes loading
THEN:   needsOpening is set to true
AND:    User should be redirected to opening/start flow
```

---

## INPUTS / OUTPUTS

### Primary Hook: `useGameState(playthroughId)`

**Inputs:** `playthroughId` (string, default `default`).

**Outputs:** `gameState`, `isLoading`, `loadingMessage`, `error`, `isConnected`, `needsOpening`, `refresh`, `sendAction`, `clickWord` (deprecated).

**Side Effects:** backend API requests, SSE subscription, toast on error.

### Secondary Hook: `useMoments({ playthroughId, location, tick })`

**Inputs:** `playthroughId`, `location`, `tick`, optional `autoConnect` (default true).

**Outputs:** `spokenMoments`, `activeMoments`, `transitions`, `isLoading`, `error`, `clickWord`, `refresh`, `clearError`.

---

## EDGE CASES (SUMMARY)

- Backend starts unavailable → error state; refresh recovers when backend returns.
- SSE connection loss → error callback + reconnection message.
- Duplicate moment activation → deduplicate by ID.
- Empty moments response → `needsOpening` set true and redirect.

---

## ANTI-BEHAVIORS (SUMMARY)

- No direct mutation of `gameState` or moment arrays.
- No stale UI after SSE updates.
- No concurrent traversal clicks while `isLoading`.
- No stale error state after successful refresh.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Document image loading behavior for scene banners
- [ ] Document map canvas interaction behaviors
- IDEA: Add optimistic UI updates for faster perceived response
- QUESTION: Should useMoments fully replace useGameState, or coexist permanently?

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

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| playthroughId | string | ID of the playthrough (defaults to 'default') |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| gameState | GameState | null | Full game state or null if loading |
| isLoading | boolean | Whether state is being fetched |
| loadingMessage | string | Atmospheric loading message |
| error | string | null | Error message if fetch failed |
| isConnected | boolean | Whether backend is available |
| needsOpening | boolean | Whether playthrough needs opening |
| refresh | () => Promise | Refetch game state |
| sendAction | (action) => Promise | Submit player action |
| clickWord | (word, path) => Promise | DEPRECATED - use moment system |

**Side Effects:**

- Network requests to backend API
- SSE connection established
- Toast notifications on error

### Secondary Hook: `useMoments({ playthroughId, location, tick })`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| playthroughId | string | ID of the playthrough |
| location | string | Current location ID |
| tick | number | Current game tick |
| autoConnect | boolean | Whether to auto-connect SSE (default: true) |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| spokenMoments | Moment[] | Moments that have been spoken |
| activeMoments | Moment[] | Currently active/possible moments |
| transitions | MomentTransition[] | Available click transitions |
| isLoading | boolean | Whether traversal is in progress |
| error | string | null | Error message if any |
| clickWord | (momentId, word) => Promise | Trigger word click traversal |
| refresh | () => Promise | Refetch moments |
| clearError | () => void | Clear error state |

---

## EDGE CASES

### E1: Backend Starts Unavailable Then Becomes Available

```
GIVEN:  User loads page while backend is down
THEN:   Error state is shown
WHEN:   Backend becomes available and user refreshes
THEN:   Normal game state loads
```

### E2: SSE Connection Lost

```
GIVEN:  User is playing with active SSE connection
WHEN:   Network drops or backend restarts
THEN:   Error callback fires with "Connection lost"
AND:    UI shows reconnection message
```

### E3: Duplicate Moment Activation

```
GIVEN:  Active moments exist
WHEN:   SSE emits moment_activated for existing moment ID
THEN:   Duplicate is not added (deduplication in hook)
```

### E4: Empty Moments Response

```
GIVEN:  Playthrough exists but has no moments
WHEN:   useGameState loads
THEN:   needsOpening is set to true
AND:    User redirected to start flow
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Direct State Mutation

```
GIVEN:   Game state is loaded
WHEN:    Component tries to modify state directly
MUST NOT: Mutate gameState object directly
INSTEAD:  Use sendAction or clickWord to trigger backend changes
```

### A2: Stale UI After Action

```
GIVEN:   User performs an action
WHEN:    Backend processes and SSE emits update
MUST NOT: Show stale data after SSE event received
INSTEAD:  UI must reflect new state immediately
```

### A3: Multiple Concurrent Traversals

```
GIVEN:   User clicks a word
WHEN:    Traversal is in progress (isLoading = true)
MUST NOT: Allow another click to trigger traversal
INSTEAD:  Ignore clicks while isLoading
```

### A4: Error State Persistence

```
GIVEN:   An error occurred during fetch
WHEN:    User triggers refresh
MUST NOT: Keep showing stale error after successful refresh
INSTEAD:  Clear error state and show fresh data
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Document image loading behavior for scene banners
- [ ] Document map canvas interaction behaviors
- IDEA: Add optimistic UI updates for faster perceived response
- QUESTION: Should useMoments fully replace useGameState, or coexist permanently?

# Frontend — Validation: Invariants and Verification

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against current implementation
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
THIS:            VALIDATION_Frontend_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/hooks/useGameState.ts
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

These must ALWAYS be true:

### V1: Backend Is Source of Truth

```
Frontend state is ALWAYS derived from backend API responses.
Local state modifications are temporary UI state only.
Game logic decisions live in Python backend, never in frontend.
```

**Checked by:** Manual review - ensure no game logic in frontend

### V2: Loading State Consistency

```
IF isLoading == true THEN gameState may be null or stale
IF isLoading == false AND error == null THEN gameState reflects latest fetch
IF isLoading == false AND error != null THEN gameState may be null
```

**Checked by:** Code review of useGameState hook state transitions

### V3: Moment State Separation

```
A moment can only be in ONE state at a time:
- 'active' OR 'possible' in activeMoments array
- 'spoken' in spokenMoments array
Never in both arrays simultaneously.
```

**Checked by:** useMoments hook logic - removal before addition

### V4: No Duplicate Moments

```
Each moment ID appears at most once across activeMoments and spokenMoments.
SSE handlers check for existing IDs before adding.
```

**Checked by:** Deduplication check in onMomentActivated callback

### V5: TypeScript Type Safety

```
All API responses are typed.
GameState, Moment, MomentTransition have defined interfaces.
No 'any' types in production code paths.
```

**Checked by:** TypeScript compiler, `npm run build`

---

## PROPERTIES

For property-based testing:

### P1: State Transformation Idempotency

```
FORALL view: CurrentView:
    transformViewToScene(view) produces consistent Scene
    Same input always produces same output
```

**Tested by:** NOT YET TESTED - pure function, could add unit tests

### P2: Click Traversal Atomicity

```
FORALL click event:
    Either traversal completes AND state updates
    OR traversal fails AND state unchanged
    Never partial state updates
```

**Tested by:** NOT YET TESTED - would require integration tests

### P3: SSE Event Ordering

```
FORALL events e1, e2 for same moment:
    If e1 arrives before e2, e1 processed before e2
    No race conditions in state updates
```

**Tested by:** NOT YET TESTED - SSE handlers are synchronous

---

## ERROR CONDITIONS

### E1: Backend Unavailable

```
WHEN:    Health check returns non-ok status
THEN:    isConnected = false, error set, toast shown
SYMPTOM: User sees "Backend is unavailable" message
```

**Tested by:** NOT YET TESTED - manual verification

### E2: API Request Failure

```
WHEN:    Any fetch throws or returns non-ok status
THEN:    Error caught, error state set, loading cleared
SYMPTOM: Error message displayed to user
```

**Tested by:** NOT YET TESTED - error handling in each API call

### E3: SSE Connection Lost

```
WHEN:    EventSource emits 'error' event
THEN:    onError callback fires, error state set
SYMPTOM: User sees "Connection lost. Reconnecting..."
```

**Tested by:** NOT YET TESTED - SSE error handler exists

### E4: Invalid API Response Shape

```
WHEN:    API returns unexpected data shape
THEN:    TypeScript catches at compile time (for typed fields)
SYMPTOM: Runtime error if untyped data accessed
```

**Tested by:** TypeScript compilation, manual testing

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Backend source of truth | Manual review | - |
| V2: Loading state consistency | - | NOT YET TESTED |
| V3: Moment state separation | - | NOT YET TESTED |
| V4: No duplicate moments | - | NOT YET TESTED |
| V5: TypeScript safety | `npm run build` | Automated |
| E1: Backend unavailable | - | NOT YET TESTED |
| E2: API failure | - | NOT YET TESTED |
| E3: SSE connection lost | - | NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Build succeeds: `cd frontend && npm run build`
[ ] No TypeScript errors
[ ] Backend available: start backend, verify /health returns 200
[ ] Game loads: navigate to /, verify scene displays
[ ] Moment clicks work: click a word, verify new content appears
[ ] SSE works: perform action, verify real-time update
[ ] Error handling: stop backend, verify error toast appears
```

### Automated

```bash
# Build (type checking)
cd frontend && npm run build

# Lint
cd frontend && npm run lint

# No dedicated test suite yet (see TEST doc)
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: frontend/hooks/useGameState.ts @ current
    impl: frontend/hooks/useMoments.ts @ current
    impl: frontend/lib/api.ts @ current
VERIFIED_BY: ngram repair agent
RESULT:
    V1: PASS (by design)
    V2: PASS (code review)
    V3: PASS (code review)
    V4: PASS (code review)
    V5: PASS (npm run build succeeds)
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add unit tests for transformation functions
- [ ] Add integration tests for click traversal
- [ ] Add E2E tests with Playwright for full flows
- IDEA: Property-based tests with fast-check for transformations
- QUESTION: Should we add runtime validation (e.g., zod) for API responses?

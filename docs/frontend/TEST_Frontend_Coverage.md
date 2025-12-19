# Frontend — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
THIS:            TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            (no test files yet)
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

The frontend currently has minimal automated testing. The strategy going forward should be:

1. **Unit Tests** (Jest/Vitest) — For pure functions like transformers
2. **Component Tests** (React Testing Library) — For UI component behavior
3. **E2E Tests** (Playwright) — For critical user flows

Priority order:
1. Transform functions (pure, easy to test)
2. Hook behavior (mock API, verify state changes)
3. E2E flows (game load, moment interaction)

---

## UNIT TESTS

### Transform Functions (TO BE IMPLEMENTED)

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `transformViewToScene` | CurrentView with moments | Scene with atmosphere, hotspots | pending |
| `transformMomentsToVoices` | Moment[] with dialogue | Voice[] with speaker/content | pending |
| `mapPlaceType` | 'camp' | 'CAMP' | pending |
| `mapPlaceType` | 'unknown' | 'CAMP' (fallback) | pending |

### API Client Functions (TO BE IMPLEMENTED)

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `checkHealth` success | mock 200 | true | pending |
| `checkHealth` failure | mock network error | false | pending |
| `getMap` success | playthroughId | { places, connections } | pending |
| `getMap` error | invalid id | throws | pending |

---

## INTEGRATION TESTS

### Game State Loading (TO BE IMPLEMENTED)

```
GIVEN:  Backend is available
WHEN:   useGameState hook mounts
THEN:   gameState is populated with transformed data
STATUS: pending
```

### Moment Click Traversal (TO BE IMPLEMENTED)

```
GIVEN:  Moments are loaded, user clicks a word
WHEN:   clickWord is called
THEN:   API is called, state updates with new moments
STATUS: pending
```

### SSE Connection (TO BE IMPLEMENTED)

```
GIVEN:  useMoments hook mounts with autoConnect=true
WHEN:   SSE events arrive
THEN:   State updates accordingly
STATUS: pending
```

---

## E2E TESTS

### Critical User Flows (TO BE IMPLEMENTED)

| Flow | Steps | Expected Result | Status |
|------|-------|-----------------|--------|
| Game Load | Navigate to /, wait for load | Scene displays with atmosphere | pending |
| Moment Interaction | Click word in moment | New content appears | pending |
| Error Handling | Load with backend down | Error toast shown | pending |
| Opening Flow | New playthrough | Redirected to start | pending |

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Backend unavailable on load | Verify error state | pending |
| Empty moments response | Verify needsOpening set | pending |
| SSE connection lost | Verify error callback | pending |
| Duplicate moment activation | Verify deduplication | pending |
| Concurrent click prevention | Verify isLoading guard | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `hooks/useGameState.ts` | 0% | No tests yet |
| `hooks/useMoments.ts` | 0% | No tests yet |
| `lib/api.ts` | 0% | No tests yet |
| `components/*` | 0% | No tests yet |

---

## HOW TO RUN

```bash
# Currently no test suite configured
# Future commands:

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npx playwright test
```

---

## KNOWN TEST GAPS

- [ ] No test framework configured (need to add Jest/Vitest)
- [ ] No component tests
- [ ] No E2E tests
- [ ] No mocking infrastructure for API calls
- [ ] No SSE mocking for real-time updates

---

## FLAKY TESTS

No tests exist yet, so no flaky tests to report.

---

## RECOMMENDED IMPLEMENTATION ORDER

1. **Set up test framework**
   - Add Vitest or Jest
   - Configure for TypeScript + React

2. **Unit tests for transformers** (highest value, lowest effort)
   - `transformViewToScene`
   - `transformMomentsToVoices`
   - `mapPlaceType`

3. **Hook tests with mocked API**
   - `useGameState` loading flow
   - `useMoments` click traversal

4. **E2E with Playwright**
   - Game load flow
   - Moment interaction flow

---

## GAPS / IDEAS / QUESTIONS

- [ ] Choose test framework (Vitest recommended for Vite compat)
- [ ] Set up MSW for API mocking
- [ ] Add Playwright for E2E
- IDEA: Use Storybook for visual component testing
- IDEA: Add snapshot tests for component structure
- QUESTION: Should we aim for specific coverage percentage?

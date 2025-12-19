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

No automated tests are configured yet.

Priority order:
1. Unit tests for pure transformers and API helpers.
2. Hook behavior with mocked API/SSE.
3. E2E flows for player-facing journeys.

---

## PLANNED COVERAGE

### Unit targets
- `transformViewToScene`, `transformMomentsToVoices`, `mapPlaceType`.
- API helpers: `checkHealth` success/failure, `getMap` success/error.

### Integration targets
- `useGameState` initial load and refresh.
- `useMoments` click traversal.
- SSE event handling updates.

### E2E targets
- Game load and scene render.
- Moment click interaction.
- Backend down error handling.
- Opening flow redirect.

---

## RUNNING TESTS

No test suite is configured yet. Expected commands once added:
`npm test` and `npx playwright test`.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Choose test framework (Vitest recommended for Vite compat)
- [ ] Set up MSW for API mocking
- [ ] Add Playwright for E2E
- IDEA: Use Storybook for visual component testing
- IDEA: Add snapshot tests for component structure
- QUESTION: Should we aim for specific coverage percentage?

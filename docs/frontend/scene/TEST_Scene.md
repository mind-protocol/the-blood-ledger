# Scene View — Tests

```
CREATED: 2024-12-17
STATUS: TODO
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
BEHAVIORS:   ./BEHAVIORS_Scene.md
ALGORITHM:   ./ALGORITHM_Scene.md
VALIDATION:  ./VALIDATION_Scene.md
THIS:        TEST_Scene.md (you are here)
SYNC:        ./SYNC_Scene.md

IMPL:        (no test files yet)
```

---

## PLANNED SUITES

| Suite | Location | Purpose |
|-------|----------|---------|
| Component test | `frontend/components/SceneView/SceneView.test.tsx` | Validate render of scene payloads, voices ordering, and fallback text without relying on live SSE. |
| Integration | `frontend/tests/scene.spec.ts` | Playwright script verifying initial scene load, text reveal timing, and action buttons. |
| API snapshot | `frontend/tests/api/scene.spec.ts` | Contract tests for `/api/view` payload shape and compatibility with frontend transforms. |

---

## TEST STRATEGY

Prioritize deterministic component tests for SceneView/CenterStage, then layer
integration coverage for scene load and action buttons once the E2E harness is
ready. Manual QA remains the short-term safety net until test scaffolding exists.

---

## UNIT TESTS

### Scene rendering helpers (planned)

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| SceneView renders header | Minimal `CurrentView` payload | Header shows location/type with safe fallbacks | pending |
| CenterStage timing | Short scene text | Reading time clamps to configured min/max bounds | pending |
| Voice ordering | Voices with descending weights | Top four render in order with opacity based on weight | pending |

---

## INTEGRATION TESTS

### Scene load and actions (planned)

```
GIVEN:  A playthrough with a valid /api/view response.
WHEN:   The scene page loads and the player waits for the main view.
THEN:   Header, banner, voices, and action buttons render without errors.
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Missing banner image | Render SceneBanner with empty URL | pending |
| No voices available | Render SceneView with empty voices list | pending |
| Extremely long text | CenterStage handles long narration without crash | pending |
| Missing portraits | People rows fall back to default avatars | pending |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `SceneView.tsx` | 0% | No automated tests; manual checks only. |
| `CenterStage.tsx` | 0% | Timing and word-click logic untested. |
| `SceneBanner.tsx` | 0% | Fallback rendering needs component coverage. |
| `SceneActions.tsx` | 0% | Action button visibility and handlers untested. |

---

## HOW TO RUN

```bash
# No automated tests are wired yet for the scene module.
# Expected commands once suites exist:
npm test
npx playwright test frontend/tests/scene.spec.ts
```

---

## KNOWN TEST GAPS

- [ ] No component tests validating SceneView fallbacks and header rendering.
- [ ] No integration coverage for action buttons or CenterStage timing.
- [ ] No mocked SSE stream for incremental moment updates.

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| None yet | n/a | No automated tests exist, so flakiness is unmeasured | Add baseline test suite first |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add unit tests for SceneView and CenterStage rendering fallbacks.
- [ ] Add Playwright smoke test for action button presence and voice ordering.
- IDEA: Use MSW to mock `/api/view` payloads for predictable component tests.
- QUESTION: Should scene tests live under `frontend/tests/` or co-locate?

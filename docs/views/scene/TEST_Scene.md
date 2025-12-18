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
```

---

## Planned Suites

| Suite | Location | Purpose |
|-------|----------|---------|
| Component test | `frontend/components/SceneView/SceneView.test.tsx` | Validate render of CurrentView payloads |
| Integration | `frontend/tests/scene.spec.ts` | Playwright script verifying transitions + wait flow |
| API snapshot | `frontend/tests/api/scene.spec.ts` | Contract tests for `/api/view` payload |

---

## Coverage Gaps

- No automated tests exist yet (manual QA only).
- Need mocking layer for SSE stream to assert incremental updates.
```

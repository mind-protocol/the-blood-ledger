# Scene View — Validation

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
BEHAVIORS:   ./BEHAVIORS_Scene.md
ALGORITHM:   ./ALGORITHM_Scene.md
THIS:        VALIDATION_Scene.md (you are here)
TEST:        ./TEST_Scene.md
SYNC:        ./SYNC_Scene.md
```

---

## Invariants

1. **Moment Count Limit** — UI renders at most 20 active moments; overflow is paged/stacked to avoid scroll fatigue.
2. **Action Latency** — Click → response under 100ms (local), enforced via perf tests.
3. **Wait Trigger** — Timer cannot fire while a narrator response is in-flight (prevents double-advance).
4. **Ledger Links** — Each highlighted ledger reference resolves to an existing entry.

---

## Checks

- Manual smoke: run `npm run dev` in `frontend/` and interact with `/scene` route.
- Automated (planned): Playwright script verifying clickable word highlights and SSE updates.
- API contract: Snapshot tests ensuring `/api/view` output matches docs/engine/moments/API_Moments.md.
```

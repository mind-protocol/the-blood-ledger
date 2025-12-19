# Scenario Selection - Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:  ./PATTERNS_Scenario_Selection.md
THIS:      SYNC_Scenario_Selection.md (you are here)
IMPL:      frontend/app/scenarios/page.tsx
```

---

## MATURITY

**What's canonical (v1):**
- Scenario selection page renders a curated list with preview details.
- Selected scenario starts a playthrough via the createPlaythrough API call.

**What's still being designed:**
- Whether the scenario list should be fetched from the backend.
- Visual styling for tone tags beyond neutral stone palette.

**What's proposed (v2+):**
- Scenario filters or grouping by tone.

---

## CURRENT STATE

The scenario selection page reads player name/gender from session storage,
redirects to `/start` if missing, and presents a two-column UI that previews the
selected scenario before triggering playthrough creation.

---

## RECENT CHANGES

### 2025-12-19: Documented scenario selection module

- **What:** Added scenario selection docs, mapping, and DOCS reference.
- **Why:** Repair task flagged `frontend/app/scenarios` as undocumented.
- **Files:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`, `docs/frontend/scenarios/SYNC_Scenario_Selection.md`, `modules.yaml`, `frontend/app/scenarios/page.tsx`

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documented the scenario selection module and linked the entrypoint.

**What you need to understand:**
Scenario IDs are hardcoded in the UI and must stay aligned with `scenarios/*.yaml`.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL->DOCS: Update docs if the selection flow or API contract changes.

### Tests to Run

```bash
cd frontend && npm run build
```

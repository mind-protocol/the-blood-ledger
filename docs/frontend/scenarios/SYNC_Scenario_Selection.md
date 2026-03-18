# Scenario Selection - Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
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

### 2025-12-21: Externalized scenario list data

- **What:** Moved SCENARIOS into `frontend/data/scenarios.ts` and updated the patterns doc to match.
- **Why:** Address hardcoded configuration warning and keep docs aligned.
- **Files:** `frontend/data/scenarios.ts`, `frontend/app/scenarios/page.tsx`, `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`

### 2025-12-20: Align scenario selection docs with current UI

- **What:** Noted session-storage gating and visual tone details in the patterns doc.
- **Why:** Resolve code/doc drift warning for the scenario selection entrypoint.
- **Files:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`

### 2025-12-19: Documented scenario selection module

- **What:** Added scenario selection docs, mapping, and DOCS reference.
- **Why:** Repair task flagged `frontend/app/scenarios` as undocumented.
- **Files:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`, `docs/frontend/scenarios/SYNC_Scenario_Selection.md`, `modules.yaml`, `frontend/app/scenarios/page.tsx`

### 2025-12-19: Filled missing pattern template sections

- **What:** Added SCOPE and INSPIRATIONS sections to the scenario selection patterns doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for missing template fields.
- **Files:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`

### 2025-12-19: Expanded scenario selection pattern details

- **What:** Expanded INSPIRATIONS/SCOPE and clarified out-of-scope bullets to meet template length thresholds.
- **Why:** Repair task required missing sections plus 50+ character guidance.
- **Files:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`

---

## IN PROGRESS

Template drift repair: adding required SYNC sections and expanding terse notes
to meet the minimum detail threshold for this module snapshot.

---

## KNOWN ISSUES

No runtime defects are tracked here today, but scenario list drift is still a
standing risk because the UI list is static and must mirror `scenarios/*.yaml`.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documented the scenario selection module and linked the entrypoint.

**What you need to understand:**
Scenario IDs are hardcoded in the UI and must stay aligned with `scenarios/*.yaml`.

---

## HANDOFF: FOR HUMAN

**Summary:** This repair only fills missing SYNC sections and clarifies drift
risks; no code behavior or scenario content was changed in this pass.

**Requests:** None. If you want scenario metadata sourced dynamically, decide
when that backend contract is ready so the UI can follow.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL->DOCS: Update docs if the selection flow or API contract changes.

### Tests to Run

```bash
cd frontend && npm run build
```

---

## CONSCIOUSNESS TRACE

I focused on template compliance and kept the wording grounded in current
behavior, keeping uncertainty explicit around future metadata sourcing.

---

## POINTERS

- `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md` for design intent.
- `frontend/app/scenarios/page.tsx` for the live UI flow and scenario list.

---

## Agent Observations

### Remarks
- The scenario selection pattern now includes expanded scope and inspiration notes that meet template requirements.

### Suggestions
- [ ] Add a brief note on how the UI should react if a selected scenario YAML is missing.

### Propositions
- Consider adding a lightweight visual tone tag guide once categories are standardized.

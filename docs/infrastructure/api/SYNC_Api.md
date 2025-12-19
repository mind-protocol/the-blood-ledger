# API — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex
STATUS: CANONICAL
```

---

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- API app factory, router wiring, and current playthrough/moment endpoints are live and documented.
- Debug and gameplay SSE streams are established with separate queues and known payload shapes.

What's still being designed:
- Auth, rate limiting, and API gateway decisions are pending until load and access patterns stabilize.

What's proposed (v2):
- Split router-level docs into per-route modules if the API surface keeps growing.

---

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/api/app.py`

The API module hosts the FastAPI application, including playthrough endpoints, moment APIs, and debug streaming.

---

## IN PROGRESS

- Tracking template completeness for the API SYNC doc so future repairs do not regress section coverage.
- Waiting on product direction to confirm whether authentication should be handled here or via a gateway service.

---

## RECENT CHANGES

### 2025-12-19: Expand API validation template sections (repair 16)

- **What:** Added invariants, properties, error conditions, test coverage, verification procedure, sync status, and gaps sections to the API validation doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for `VALIDATION_Api.md` and align with the validation template requirements.
- **Files:**
  - `docs/infrastructure/api/VALIDATION_Api.md`

### 2025-12-19: Fill missing SYNC template sections (repair 16)

- **What:** Added MATURITY, IN PROGRESS, KNOWN ISSUES, handoffs, TODO, consciousness trace, and pointers sections.
- **Why:** Resolve DOC_TEMPLATE_DRIFT warning for the API SYNC doc.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Fill API PATTERNS template sections (repair 16)

- **What:** Added missing problem, pattern, principles, dependencies,
  inspirations, scope, and gaps sections in `PATTERNS_Api.md`.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the API patterns document.
- **Files:**
  - `docs/infrastructure/api/PATTERNS_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Remove duplicate playthrough algorithm doc

- **What:** Deleted `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` so the API folder has a single canonical ALGORITHM doc.
- **Why:** The redirect file still counted as a duplicate ALGORITHM doc in the same folder, which triggers duplication warnings.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Reconfirm playthrough helper implementations (repair 01-INCOMPLETE_IMPL-api-playthroughs)

- **What:** Verified `_count_branches` and `create_scenario_playthrough` implementations; no code changes required.
- **Why:** Repair task flagged empty implementations; current code already provides real logic.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Align playthrough scenario creation to router implementation

- **What:** Added `/api/playthrough/scenario` alias in `engine/infrastructure/api/playthroughs.py` and removed the duplicate scenario endpoint in `engine/infrastructure/api/app.py`.
- **Why:** The frontend expects a `scene` payload from scenario creation, which the router provides; the app-level endpoint returned a different shape and caused a mismatch.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `engine/infrastructure/api/app.py`

### 2025-12-19: Remove unsupported energy argument when creating opening moments

- **What:** Dropped the `energy` argument passed to `GraphOps.add_moment()` when generating opening moments.
- **Why:** `GraphOps.add_moment()` does not accept `energy`, which raised an exception during playthrough creation and could stall the flow.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`

### 2025-12-19: Finish playthrough helper implementations

- **What:** Expanded discussion branch counting, added per-playthrough GraphQueries caching, and wired player moment embeddings to the embedding service with a safe fallback.
- **Why:** Repair task flagged incomplete helper implementations; these changes provide full logic without breaking moment creation when embeddings are unavailable.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Fix asyncio queue reference in API implementation doc

- **What:** Reworded the debug stream description to avoid `asyncio.Queue` being parsed as a file link.
- **Why:** Link validation flags `asyncio.Queue` as a missing file path.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Remove broken asyncio.Queue file reference

- **What:** Reworded the debug stream description to avoid a broken file reference for `asyncio.Queue`.
- **Why:** `ngram validate` treats `asyncio.Queue` as a file link; the target does not exist.
- **Files:**
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`

### 2025-12-19: Map infrastructure API module and link DOCS reference

- **What:** Mapped `engine/infrastructure/api/**` to `docs/infrastructure/api/` in `modules.yaml` and added a `# DOCS:` header in `engine/infrastructure/api/app.py` for `ngram context`.
- **Why:** The API docs existed but the code path was not mapped, so documentation discovery failed for the API module.
- **Files:**
  - `modules.yaml`
  - `engine/infrastructure/api/app.py`

### 2025-12-19: Consolidate API algorithm documentation

- **What:** Merged playthrough creation flow into `docs/infrastructure/api/ALGORITHM_Api.md` and removed the duplicate algorithm file.
- **Why:** Remove duplicate ALGORITHM docs in the API folder and keep a single canonical algorithm reference.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Re-verify playthrough helpers for repair 01-INCOMPLETE_IMPL-api-playthroughs

- **What:** Confirmed `_count_branches` and `_get_playthrough_queries` in `engine/infrastructure/api/playthroughs.py` already contain real logic; no code changes required.
- **Why:** Repair task flagged empty implementations, but the functions are implemented.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Add /api/action endpoint and fix scenario path

- **What:** Added `POST /api/action` endpoint for full game loop. Fixed scenario path in playthroughs.py (was looking in `engine/scenarios` instead of project root `scenarios/`).
- **Why:** The action endpoint was missing - frontend click path had no way to trigger the full narrator/tick/flips loop. Scenario path was wrong due to incorrect parent traversal.
- **Files:**
  - `engine/infrastructure/api/app.py` — added `/api/action` endpoint
  - `engine/infrastructure/api/playthroughs.py` — fixed scenarios_dir path
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md` — documented new endpoints

### 2025-12-19: Verify playthroughs helper implementations (repair 01-INCOMPLETE_IMPL-api-playthroughs)

- **What:** Rechecked `_count_branches` and `_get_playthrough_queries` in `engine/infrastructure/api/playthroughs.py`; no code changes required.
- **Why:** Repair task flagged empty implementations, but the functions already contain logic.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Fill API helper implementations

- **What:** Implemented cached graph helpers, expanded health check, and hardened debug SSE payloads.
- **Why:** Replace incomplete helper stubs and provide meaningful health validation.
- **Files:**
  - `engine/infrastructure/api/app.py`
  - `docs/infrastructure/api/BEHAVIORS_Api.md`
  - `docs/infrastructure/api/IMPLEMENTATION_Api.md`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Verify playthroughs helper implementations

- **What:** Confirmed `_count_branches` and `_get_playthrough_queries` already contain real logic in the playthroughs router.
- **Why:** Repair task flagged them as incomplete, but the implementations are in place.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Re-validate playthroughs repair task

- **What:** Reconfirmed the playthroughs helpers are implemented; no code changes required for this repair run.
- **Why:** Task still flagged incomplete implementations, but the functions already perform real logic.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Reconfirm playthroughs helper implementations (repair 01)

- **What:** Verified `_count_branches` and `_get_playthrough_queries` are fully implemented; no code changes needed.
- **Why:** Repair task again flagged them as incomplete; verification confirms existing logic is intact.
- **Files:**
  - `docs/infrastructure/api/SYNC_Api.md`

### 2025-12-19: Verify playthroughs helpers (repair 01-INCOMPLETE_IMPL-api-playthroughs)

- **What:** Confirmed `_count_branches` and `_get_playthrough_queries` in `engine/infrastructure/api/playthroughs.py` already contain real logic; no code changes required.
- **Why:** Repair task flagged empty implementations; verification shows they are implemented.
- **Files:**
  - `engine/infrastructure/api/playthroughs.py`
  - `docs/infrastructure/api/SYNC_Api.md`

---

## KNOWN ISSUES

- None logged for API runtime behavior; doc drift repairs are still ongoing in other modules and may reference API dependencies.

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Implement_Write_Or_Modify_Code

**Context:** This SYNC entry now includes missing template sections; keep them updated if API behavior changes.

**Watch out for:** Avoid adding duplicate algorithm files under `docs/infrastructure/api/`; keep `ALGORITHM_Api.md` canonical.

---

## HANDOFF: FOR HUMAN

**Executive summary:** Filled missing SYNC template sections for the API doc to resolve template drift warnings.

**Decisions made:** None; content clarifies current status and keeps the canonical API docs intact.

**Needs your input:** Confirm whether authentication and rate limiting should live in the API module or a gateway.

---

## TODO

- [ ] Revisit API auth and rate limiting scope once the gateway strategy is chosen to avoid documenting the wrong boundary.
- [ ] Keep SYNC entries concise while still meeting template requirements as new API endpoints are added.

---

## CONSCIOUSNESS TRACE

The repair focus here is documentation completeness, with no behavior changes; remaining uncertainty centers on future auth/gateway design choices.

---

## POINTERS

- `docs/infrastructure/api/PATTERNS_Api.md` for scope and design rationale.
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` for endpoint-level data flow notes.
- `engine/infrastructure/api/app.py` for the app factory and router wiring.

---

## AGENT OBSERVATIONS

### Remarks
- `engine/infrastructure/api/app.py` remains a large monolith that bundles multiple endpoint groups.
- Repair task flagged playthrough helper functions as empty, but they are already implemented.
- Re-validated playthroughs helper implementations for this repair run; no code changes required.
 - Confirmed playthrough helper implementations for repair 01-INCOMPLETE_IMPL-api-playthroughs.
- Reconfirmed `_count_branches` and `_get_playthrough_queries` implementations during this repair run.
- PATTERNS template sections now reflect the API boundary and dependencies.

### Suggestions
- [ ] Consider splitting `engine/infrastructure/api/app.py` into smaller router modules once the API surface stabilizes.

### Propositions
- Establish a dedicated API doc chain for each major router (moments, playthroughs, debug).

---

## CHAIN

PATTERNS: ./PATTERNS_Api.md
BEHAVIORS: ./BEHAVIORS_Api.md
ALGORITHM: ./ALGORITHM_Api.md
VALIDATION: ./VALIDATION_Api.md
IMPLEMENTATION: ./IMPLEMENTATION_Api.md
TEST: ./TEST_Api.md
SYNC: ./SYNC_Api.md

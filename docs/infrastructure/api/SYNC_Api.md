# API — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex
STATUS: CANONICAL
```

---

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/api/app.py`

The API module hosts the FastAPI application, including playthrough endpoints, moment APIs, and debug streaming.

---

## RECENT CHANGES

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

- **What:** Merged playthrough creation flow into `docs/infrastructure/api/ALGORITHM_Api.md` and replaced the duplicate algorithm file with a redirect.
- **Why:** Remove duplicate ALGORITHM docs in the API folder and keep a single canonical algorithm reference.
- **Files:**
  - `docs/infrastructure/api/ALGORITHM_Api.md`
  - `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`

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

## AGENT OBSERVATIONS

### Remarks
- `engine/infrastructure/api/app.py` remains a large monolith that bundles multiple endpoint groups.
- Repair task flagged playthrough helper functions as empty, but they are already implemented.
- Re-validated playthroughs helper implementations for this repair run; no code changes required.
 - Confirmed playthrough helper implementations for repair 01-INCOMPLETE_IMPL-api-playthroughs.
- Reconfirmed `_count_branches` and `_get_playthrough_queries` implementations during this repair run.

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

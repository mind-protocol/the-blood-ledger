# API — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Claude Opus 4.5
STATUS: CANONICAL
```

---

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/api/app.py`

The API module hosts the FastAPI application, including playthrough endpoints, moment APIs, and debug streaming.

---

## RECENT CHANGES

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

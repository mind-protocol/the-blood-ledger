# API — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- API app factory, router wiring, and current playthrough/moment endpoints are live and documented.
- Debug and gameplay SSE streams are established with separate queues.

What's still being designed:
- Auth, rate limiting, and API gateway decisions.

## CURRENT STATE

**Implementation Location:** `engine/infrastructure/api/app.py`

The API module hosts the FastAPI application, including playthrough endpoints, moment APIs, and debug streaming.

## RECENT CHANGES

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Api.md` and updated `TEST_Api.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** API module documentation is now compliant; Health checks are anchored to concrete docking points.

### 2025-12-20: Discussion Tree Branch Counting

- **What:** Count discussion tree branches by remaining leaf paths and document the helper behavior.
- **Why:** Ensure regeneration triggers reflect actual remaining branch paths.
- **Impact:** Branch count now aligns with discussion tree lifecycle expectations.

## GAPS

- [ ] Automated regression for SSE stream delivery under load.
- [ ] Schema validation tests for all router endpoints.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code when touching API routers. Ensure new endpoints are extracted from `app.py` to keep it from growing further.

## TODO

- [ ] Split remaining legacy endpoints from `app.py` into router modules.
- [ ] Implement API versioning strategy.

## POINTERS

- `docs/infrastructure/api/PATTERNS_Api.md` for scope and design rationale.
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` for endpoint-level data flow notes.

## CHAIN

```
THIS:            SYNC_Api.md (you are here)
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
ALGORITHM:       ./ALGORITHM_Api.md
VALIDATION:      ./VALIDATION_Api.md
IMPLEMENTATION:  ./IMPLEMENTATION_Api.md
HEALTH:          ./HEALTH_Api.md
```

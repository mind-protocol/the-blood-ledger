# Tempo Controller — Sync

```
UPDATED: 2025-12-19
STATUS: IMPLEMENTED
```

---

## Current State

Tempo Controller is **implemented** with backend, API, and frontend components.

Latest repair update:
- Hardened `TempoController.stop` and `update_display_queue_size` with cleanup,
  validation, and logging.
- Added the missing PATTERNS, BEHAVIORS, VALIDATION, and TEST docs to complete
  the documentation chain.

### Doc Chain

| Doc | Status |
|-----|--------|
| PATTERNS | ✓ Complete |
| BEHAVIORS | ✓ Complete |
| ALGORITHM | ✓ Complete |
| VALIDATION | ✓ Complete |
| IMPLEMENTATION | ✓ Complete |
| TEST | ✓ Complete |
| SYNC | ✓ This file |

### Code Status

| Component | Status | Notes |
|-----------|--------|-------|
| `tempo_controller.py` | ✓ Implemented | ~320 lines, main loop |
| `tempo.py` (API) | ✓ Implemented | FastAPI endpoints |
| `SpeedControl.tsx` | ✓ Implemented | Frontend buttons |
| `GameClient.tsx` | ✓ Integrated | Shows SpeedControl |
| Tests | ❌ Missing | No test coverage yet |

---

## Implementation Summary

### Backend

**TempoController class** (`engine/infrastructure/tempo/tempo_controller.py`):
- Async main loop with speed state machine
- Modes: pause, 1x, 2x, 3x
- Physics ticking via `GraphTick`
- Moment surfacing via `CanonHolder`
- SSE broadcast for speed changes

**API endpoints** (`engine/infrastructure/api/tempo.py`):
- `POST /api/tempo/speed` — Set speed
- `GET /api/tempo/{id}` — Get state
- `POST /api/tempo/input` — Player input
- `POST /api/tempo/start/{id}` — Start controller
- `POST /api/tempo/stop/{id}` — Stop controller

### Frontend

**SpeedControl component** (`frontend/components/SpeedControl.tsx`):
- Four buttons: ⏸ Pause | 🗣️ 1x | 🚶 2x | ⏩ 3x
- Fetches current speed on mount
- Listens for SSE speed_changed events
- POST to /api/tempo/speed on click

**GameClient integration**:
- SpeedControl shown in top-right corner next to connection status

---

## Architecture Clarification

The key insight from implementing Tempo Controller:

```
Narrator (separate) → creates moments (status=possible) → sits in graph
                                    ↓
TempoController.run() → tick interval → physics.tick() → detect_ready_moments()
                                    ↓
                         CanonHolder.record_to_canon() → SSE broadcast
                                    ↓
                              Frontend displays
```

**Narrator and Tempo are decoupled:**
- Narrator creates content (moments with `status=possible`)
- Tempo surfaces and speaks content (possible → active → spoken)

This is why `_record_narrator_output` was deleted from Orchestrator — it incorrectly bypassed physics surfacing.

---

## Remaining Work

### Missing Docs

### Missing Implementation

- [ ] Display filtering in frontend (2x shows only dialogue, 3x only interrupts)
- [ ] "The Snap" visual transition (3x → 1x)
- [ ] Backpressure reporting from frontend to backend
- [ ] Tests for TempoController

### Open Questions

- QUESTION: How/when does narrator get called to generate new moments?
- QUESTION: Should `detect_ready_moments()` use a lighter query than full physics?

---

## Files Changed This Session

| File | Change |
|------|--------|
| `engine/infrastructure/tempo/tempo_controller.py` | Validate queue size updates, clear pending input on stop |
| `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md` | Documented stop cleanup and queue size normalization |
| `engine/infrastructure/orchestration/orchestrator.py` | Removed `_record_narrator_output`, `_create_moment_node`, CanonHolder import |
| `engine/infrastructure/tempo/__init__.py` | Created |
| `engine/infrastructure/tempo/tempo_controller.py` | Created |
| `engine/infrastructure/api/tempo.py` | Created |
| `engine/infrastructure/api/app.py` | Added tempo router |
| `frontend/components/SpeedControl.tsx` | Created |
| `frontend/components/GameClient.tsx` | Added SpeedControl |
| `docs/infrastructure/tempo/PATTERNS_Tempo.md` | Created |
| `docs/infrastructure/tempo/BEHAVIORS_Tempo.md` | Created |
| `docs/infrastructure/tempo/VALIDATION_Tempo.md` | Created |
| `docs/infrastructure/tempo/TEST_Tempo.md` | Created |

---

## Chain

- PATTERNS: `docs/infrastructure/tempo/PATTERNS_Tempo.md` ✓
- BEHAVIORS: `docs/infrastructure/tempo/BEHAVIORS_Tempo.md` ✓
- ALGORITHM: `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md` ✓
- VALIDATION: `docs/infrastructure/tempo/VALIDATION_Tempo.md` ✓
- IMPLEMENTATION: `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md` ✓
- TEST: `docs/infrastructure/tempo/TEST_Tempo.md` ✓
- **SYNC: This file** ✓

## Agent Observations

### Remarks
- Backpressure relies on the frontend reporting queue size; invalid values now get clamped.

### Suggestions
- [ ] Add TempoController tests for stop behavior and backpressure handling.

### Propositions
- Consider emitting a tempo shutdown event so the frontend can clear UI state.

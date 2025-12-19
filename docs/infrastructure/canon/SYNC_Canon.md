# Canon Holder — Sync

```
UPDATED: 2025-12-19
STATUS: IMPLEMENTED
```

---

## Current State

Canon Holder is **implemented and tested**.

### Doc Chain

| Doc | Status |
|-----|--------|
| PATTERNS | ✓ Complete |
| BEHAVIORS | ✓ Complete |
| ALGORITHM | ✓ Complete (10 queries) |
| VALIDATION | ✓ Complete (7 invariants) |
| IMPLEMENTATION | ✓ Complete |
| TEST | ✓ Complete (16 tests passing) |
| SYNC | ✓ This file |

### Code Status

| Component | Status | Notes |
|-----------|--------|-------|
| `canon_holder.py` | ✓ Implemented | ~310 lines, Q6/Q7 queries |
| `speaker.py` | ✓ Implemented | ~90 lines, Q5 query |
| `__init__.py` | ✓ Implemented | Module exports |
| `playthroughs.py` opening | ✓ Fixed | Creates as `possible` with ATTACHED_TO |
| `orchestrator.py` | ✓ Wired | Calls Canon Holder after narrator |
| SSE broadcast | ✓ Integrated | Called from `record_to_canon()` |

---

## Resolved Issues

### I1: Opening Moments Skip Canon Holder — FIXED

**File:** `engine/infrastructure/api/playthroughs.py`

**Before:**
```python
graph.add_moment(
    status="active",
    tick_spoken=0,
    weight=1.0
)
```

**After:**
```python
graph.add_moment(
    status="possible",
    weight=1.0,
    energy=1.0
)
# Creates ATTACHED_TO link to location with presence_required=false
```

### I2: SSE Not Broadcast by Narrator — FIXED

Canon Holder now broadcasts SSE events via lazy import of `broadcast_moment_event()` in `record_to_canon()`.

### I3: Orchestrator Not Wired to Canon Holder — FIXED

Orchestrator now creates `CanonHolder` instance and calls `_record_narrator_output()` after narrator returns.

---

## Implementation Summary

### Files Created

| File | Purpose |
|------|---------|
| `engine/infrastructure/canon/__init__.py` | Module exports |
| `engine/infrastructure/canon/canon_holder.py` | Main recording logic (Q6, Q7) |
| `engine/infrastructure/canon/speaker.py` | Speaker resolution (Q5) |
| `tests/infrastructure/canon/__init__.py` | Test module |
| `tests/infrastructure/canon/test_canon_holder.py` | 16 unit tests |

### Key Implementation Details

- **SAID link created** (not speaker stored on moment) — per ALGORITHM Q6 Step 2
- **Lazy import** for SSE broadcast to avoid circular dependency
- **Energy cost**: 60% consumed on actualization (energy *= 0.4)
- **Speaker resolution**: Q5 finds highest CAN_SPEAK.strength character present and awake

---

## Remaining Work

### Missing Implementation

- [ ] `detect_and_surface()` — Tick-based surfacing of possible → active
- [ ] `time.py` — Time advancement mechanics
- [ ] `strength.py` — Strength mechanics

### Missing Tests

- [ ] Integration tests with real FalkorDB
- [ ] Property-based tests for THEN chain acyclicity
- [ ] Stress tests with 100+ moments

---

## Test Results

```
16 passed in 0.58s

Tests cover:
- Q5: determine_speaker (2 tests)
- Q6: record_to_canon (4 tests)
- Q7: get_last_spoken_moment (2 tests)
- B3: Energy conservation (1 test)
- B4: Highest speaker wins (1 test)
- B9: Dialogue without speaker (1 test)
- E1: First moment (1 test)
- E2: Narration moment (1 test)
- E4: Player caused flag (1 test)
- SSE broadcast (1 test)
- V4: Energy formula (1 test)
```

---

## Recent Changes

### 2025-12-19: Fixed canon implementation doc file references

- **What:** Replaced bare file names in `IMPLEMENTATION_Canon.md` with full repo paths, removed stray `# DOCS:` labels, and clarified missing module items.
- **Why:** The broken-link checker flags bare filenames and doc header strings as missing files.
- **Files:** `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`

### 2025-12-19: Verified canon docs mapping

- **What:** Confirmed `modules.yaml` mapping and DOCS references already cover `engine/infrastructure/canon/**`.
- **Why:** Repair 60 flagged undocumented canon files; verification shows existing docs are authoritative.
- **Files:** `modules.yaml`, `engine/infrastructure/canon/canon_holder.py`, `engine/infrastructure/canon/speaker.py`, `engine/infrastructure/canon/__init__.py`

### 2025-12-19: Mapped canon tests for documentation coverage

- **What:** Added `tests/infrastructure/canon/**` under the canon module's `additional_code`.
- **Why:** Ensure `ngram validate` treats canon tests as mapped code and stops flagging them as undocumented.
- **Files:** `modules.yaml`

### 2025-12-19: Mapped canon module in manifest

- **What:** Added `modules.yaml` entry linking canon code/tests to docs.
- **Why:** Fix undocumented mapping for `tests/infrastructure/canon`.
- **Files:** `modules.yaml`

### 2025-12-19: Linked canon holder to docs

- **What:** Added an in-docstring `DOCS:` reference for `canon_holder.py`.
- **Why:** Ensure `ngram context` discovers the canon documentation chain.
- **Files:** `engine/infrastructure/canon/canon_holder.py`

---

## Chain

- PATTERNS: `docs/infrastructure/canon/PATTERNS_Canon.md` ✓
- BEHAVIORS: `docs/infrastructure/canon/BEHAVIORS_Canon.md` ✓
- ALGORITHM: `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md` ✓
- VALIDATION: `docs/infrastructure/canon/VALIDATION_Canon.md` ✓
- IMPLEMENTATION: `docs/infrastructure/canon/IMPLEMENTATION_Canon.md` ✓
- TEST: `docs/infrastructure/canon/TEST_Canon.md` ✓
- **SYNC: This file** ✓

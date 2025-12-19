# Schema Models — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Pydantic models for nodes, links, and tensions in `engine/models/`.
- Enum taxonomy for schema fields in `engine/models/base.py`.

**What's still being designed:**
- Cross-model validation rules beyond field-level checks.

**What's proposed (v2+):**
- Dedicated schema validation suite that enforces graph-level invariants.

---

## CURRENT STATE

The engine exposes a unified set of Pydantic models for graph nodes, links, and
tensions, along with shared enums and helper methods. The module is structured
by responsibility (base enums, nodes, links, tensions) and re-exported from
`engine/models/__init__.py` for stable imports. Tests live in
`engine/tests/test_models.py` with some integration coverage in scenario tests.

---

## RECENT CHANGES

### 2025-12-19: Revalidated link helper implementations with line refs (repair 06, current run)

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py` (`engine/models/links.py:66`, `engine/models/links.py:120`, `engine/models/links.py:140`, `engine/models/links.py:160`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation for link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated node helper implementations with line refs (repair 07)

- **What:** Confirmed `Narrative.is_core_type` and Moment helpers (`tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) are implemented in `engine/models/nodes.py` (`Narrative.is_core_type` at `engine/models/nodes.py:185`, Moment helpers starting at `engine/models/nodes.py:249`); no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair required validation of node helper properties.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Repair task appears stale relative to current code.

### 2025-12-19: Verified GameTimestamp comparison helpers (repair 05)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair task required validation for the base model helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale relative to current implementation.

### 2025-12-19: Rechecked link helper implementations (repair 05, latest run)

- **What:** Reconfirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required verification for link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated link helper implementations (repair 05, current run)

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` in `engine/models/links.py` remain implemented; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of the link helper properties.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Verified GameTimestamp helpers with test attempt (current run)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; attempted `pytest engine/tests/test_models.py`.
- **Why:** Current INCOMPLETE_IMPL repair requires evidence for comparison helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Test:** `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess` dependency).
- **Struggles/Insights:** Test dependency missing in environment; helper implementations still present.

### 2025-12-19: Verified GameTimestamp helper implementations (repair 04)

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are implemented in `engine/models/base.py`; no code changes required.
- **Why:** Current INCOMPLETE_IMPL repair run flagged empty helpers; verification shows the implementations are already present.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale relative to current code.

### 2025-12-19: Rechecked GameTimestamp comparison helpers (current run)

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are already implemented in `engine/models/base.py`; no code changes made.
- **Why:** Current INCOMPLETE_IMPL repair run required validation of these helpers.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task is stale relative to the current implementation.

### 2025-12-19: Logged repair 04 verification (current run)

- **What:** Recorded the current repair run verification for `GameTimestamp` helpers in `engine/models/base.py`; no code changes needed.
- **Why:** Repair task required confirmation for this run.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Logged repair 06 verification (current run)

- **What:** Recorded the current repair run verification for node helper properties in `engine/models/nodes.py`; no code changes needed.
- **Why:** Repair task required confirmation for this run.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; verification only.

### 2025-12-19: Revalidated node helper implementations (repair 06)

- **What:** Rechecked `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` in `engine/models/nodes.py`; implementations already present.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reconfirmed link helper implementations (repair 05)

- **What:** Verified `belief_intensity`, `is_present`, `has_item`, and `is_here` remain implemented in `engine/models/links.py`.
- **Why:** Current INCOMPLETE_IMPL repair run required confirmation.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale; no code changes required.

### 2025-12-19: Revalidated link helper implementations (repair 05)

- **What:** Rechecked `belief_intensity`, `is_present`, `has_item`, and `is_here` in `engine/models/links.py`; implementations already present.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reverified GameTimestamp comparison helpers (repair 04)

- **What:** Rechecked `GameTimestamp.__str__`, `__le__`, and `__gt__` and confirmed implementations already exist.
- **Why:** Current INCOMPLETE_IMPL repair run required verification.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale relative to current code.

### 2025-12-19: Verified node helper implementations

- **What:** Confirmed `is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, and `can_surface` are implemented in `engine/models/nodes.py`.
- **Why:** Repair task flagged incomplete helpers; verification shows no changes needed.
- **Files:** `engine/models/nodes.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Verified link helper implementations

- **What:** Confirmed `belief_intensity`, `is_present`, `has_item`, and `is_here` helpers are implemented in `engine/models/links.py`.
- **Why:** Repair task flagged incomplete helpers; verification shows no changes needed.
- **Files:** `engine/models/links.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Verified GameTimestamp comparison helpers

- **What:** Confirmed `GameTimestamp.__str__`, `__le__`, and `__gt__` are fully implemented in `engine/models/base.py`.
- **Why:** Repair task flagged incomplete implementations; verification shows the functions are already complete.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task appears stale; no code changes required.

### 2025-12-19: Reconfirmed GameTimestamp comparison helpers

- **What:** Rechecked `GameTimestamp.__str__`, `__le__`, and `__gt__` for the 06-INCOMPLETE_IMPL-models-base repair run; no code changes needed.
- **Why:** Current repair task required verification in the latest run.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`, `.ngram/state/SYNC_Project_State.md`.
- **Struggles/Insights:** Repair task remains stale relative to current code.

### 2025-12-19: Revalidated GameTimestamp comparison helpers (repair 04)

- **What:** Verified `GameTimestamp.__str__`, `__le__`, and `__gt__` are fully implemented in `engine/models/base.py`; no code changes required.
- **Why:** Repair task flagged incomplete implementations; current code already satisfies the expected behavior.
- **Files:** `engine/models/base.py`, `docs/schema/models/SYNC_Schema_Models.md`.
- **Struggles/Insights:** Repair task remains stale relative to current implementation.

### 2025-12-19: Documented schema models module

- **What:** Added module docs and mapping for `engine/models/**`.
- **Why:** Close undocumented module gap and enable `ngram` context navigation.
- **Files:** `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`, `docs/schema/models/SYNC_Schema_Models.md`, `engine/models/__init__.py`, `modules.yaml`.
- **Struggles/Insights:** Minimal chain created to avoid duplicating existing schema docs.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Added docs + mapping; no code changes beyond DOCS reference.

**What you need to understand:**
Schema models are the canonical Pydantic types for nodes/links/tensions. Keep
`engine/models/__init__.py` as the public entry point and update docs if fields
change.

**Watch out for:**
Some schema behavior is documented in `docs/schema/SCHEMA.md` but not yet linked
into a full doc chain for this module.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL->DOCS: If model fields change, update `docs/schema/models/`.

### Tests to Run

```bash
pytest engine/tests/test_models.py
```

## Agent Observations

### Remarks
- Repair task flagged incomplete functions, but `engine/models/base.py` already contains full implementations for the comparison helpers.
- Reverified the base model comparison helpers for repair 05; no code changes required.
- Repair task for `engine/models/links.py` flagged missing helpers, but implementations are already present.
- Repair task for `engine/models/nodes.py` flagged missing helpers, but implementations are already present.
- Reverified GameTimestamp comparison helpers for the current repair run; no changes required.
- Logged the current repair run verification for `GameTimestamp` helpers; no code changes required.
- Revalidated link helper implementations in `engine/models/links.py`; no changes required.
- Revalidated node helper implementations in `engine/models/nodes.py`; no changes required.
- Confirmed the current repair run for `engine/models/base.py` remains a verification-only update; no code changes needed.
- Attempted `pytest engine/tests/test_models.py`; missing `pytest_xprocess` prevented the test run.
- Reconfirmed link helper properties for the current repair run; no code changes required.
- Rechecked link helper implementations for the latest repair run; no code changes required.
- Revalidated link helper implementations for the current repair run; no code changes required.

### Suggestions
- [ ] Consider adding explicit tests for `GameTimestamp` ordering in `engine/tests/test_models.py`.

### Propositions

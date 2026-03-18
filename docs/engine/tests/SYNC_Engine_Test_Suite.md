# Engine Test Suite — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Unit and behavior tests for physics constants, tensions, and moment logic.
- Spec consistency checks for schema enums and constants.

**What's still being designed:**
- Integration and end-to-end coverage that depends on FalkorDB.
- Scenario-level tests that exercise full playthrough loops.

**What's proposed (v2+):**
- CI profiles that separate unit, integration, and slow tests.
- Fixtures for deterministic graph data across test runs.

---

## CURRENT STATE

`engine/tests/` houses the engine-level test suite. The tests are layered by
dependency: pure behavior/spec tests run without a database, while integration
and E2E tests rely on a running FalkorDB instance and skip when unavailable.

---

## IN PROGRESS

No active work.

---

## RECENT CHANGES

- 2025-12-21: Added DATA/INSPIRATIONS/SCOPE sections to PATTERNS_Spec_Linked_Test_Suite.md.
- 2025-12-21: Normalized implementation doc references and notes to match current repo state.

### 2025-12-19: Expand test file responsibilities

- **What:** Added a file responsibilities table and expanded key file descriptions in the implementation doc.
- **Why:** Align test layout documentation with the current `engine/tests` suite.
- **Files:** `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md`, `docs/engine/tests/SYNC_Engine_Test_Suite.md`
- **Struggles/Insights:** None.

### 2025-12-19: Verified implementation doc file references

- **What:** Confirmed `IMPLEMENTATION_Test_File_Layout.md` references concrete `engine/tests/**` paths instead of missing or wildcard tokens.
- **Why:** Close the BROKEN_IMPL_LINK repair for test file layout references.
- **Files:** `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md`, `docs/engine/tests/SYNC_Engine_Test_Suite.md`
- **Struggles/Insights:** The implementation doc already used full paths, so no doc edits were required beyond recording verification. `ngram validate` still reports pre-existing schema/product/network/storms doc gaps.

### 2025-12-19: Documented engine tests module

- **What:** Added module docs and mapping for `engine/tests`.
- **Why:** Close the undocumented test suite gap for the engine.
- **Files:** `docs/engine/tests/PATTERNS_Spec_Linked_Test_Suite.md`, `docs/engine/tests/BEHAVIORS_Test_Coverage_Layers.md`, `docs/engine/tests/ALGORITHM_Test_Run_Flow.md`, `docs/engine/tests/VALIDATION_Test_Suite_Invariants.md`, `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md`, `docs/engine/tests/TEST_Test_Suite_Coverage.md`, `docs/engine/tests/SYNC_Engine_Test_Suite.md`, `modules.yaml`, `engine/tests/__init__.py`
- **Struggles/Insights:** The suite is intentionally split between spec-only and integration tests.

### 2025-12-19: Normalize test file references

- **What:** Replaced bare test filenames with full `engine/tests/...` paths and expanded the moment test list.
- **Why:** Avoid broken implementation link checks on relative or glob-style references.
- **Files:** `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md`, `docs/engine/tests/SYNC_Engine_Test_Suite.md`

### 2025-12-20: Add health doc

- **What:** Added `HEALTH_Engine_Test_Suite.md` for test suite health checks.
- **Why:** Close the doc chain gap flagged by `ngram validate`.
- **Files:** `docs/engine/tests/HEALTH_Engine_Test_Suite.md`

---

## KNOWN ISSUES

### Integration Tests Require External Services

- **Severity:** Medium
- **Symptom:** `test_implementation.py` and other integration tests skip without FalkorDB.
- **Suspected cause:** Local DB not running or fixtures missing.
- **Attempted:** None in this repair.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Test_Write_Tests_And_Verify.md`

**Where I stopped:** Documented the module and linked `engine/tests/__init__.py`.

**What you need to understand:**
The suite intentionally separates spec-only tests from integration tests that
require the graph database.

**Watch out for:**
Integration tests will skip silently if FalkorDB is not available.

**Open questions I had:**
How best to split unit vs integration in CI without duplicating fixtures.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Engine tests are now documented and mapped. The suite combines spec/behavior
tests with integration tests that require FalkorDB.

**Decisions made:**
Documented the suite as DESIGNING since integration coverage is still in flux.

**Needs your input:**
If you want CI coverage for integration tests, specify the preferred DB setup.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Refresh coverage table when new engine tests land.

### Tests to Run

```bash
pytest engine/tests -v
```

### Immediate

- [ ] Decide CI split between unit-only and integration tests.

### Later

- IDEA: Add shared graph fixtures for repeatable integration runs.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Calm; scope is well-bounded to documentation only.

**Threads I was holding:**
Spec consistency tests reference legacy schema paths that may need alignment.

**Intuitions:**
The test suite will benefit from explicit markers beyond pytest defaults.

**What I wish I'd known at the start:**
Whether `docs/engine/SCHEMA.md` still exists or has moved to `docs/schema/SCHEMA.md`.

---

## POINTERS

| What | Where |
|------|-------|
| Engine test suite root | `engine/tests/` |
| Test suite docs | `docs/engine/tests/` |

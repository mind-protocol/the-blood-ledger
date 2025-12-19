# Engine Test Suite — Behaviors: Coverage Layers

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

===============================================================================
## CHAIN
===============================================================================

```
PATTERNS:       ./PATTERNS_Spec_Linked_Test_Suite.md
ALGORITHM:      ./ALGORITHM_Test_Run_Flow.md
VALIDATION:     ./VALIDATION_Test_Suite_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Test_File_Layout.md
TEST:           ./TEST_Test_Suite_Coverage.md
SYNC:           ./SYNC_Engine_Test_Suite.md
THIS:           BEHAVIORS_Test_Coverage_Layers.md (you are here)
IMPL:           ../../../engine/tests/__init__.py
```

===============================================================================
## OBSERVABLE BEHAVIOR
===============================================================================

When running `pytest engine/tests`, the suite behaves in layers:

1. **Behavior/spec tests run without external services.**
   - Physics constants, tension formulas, and moment model behaviors are
     validated directly.

2. **Schema/spec consistency tests validate static references.**
   - Spec docs and schema enums are compared for consistency.

3. **Integration/E2E tests require FalkorDB.**
   - Tests that need a graph database skip if FalkorDB is unavailable.

4. **Scenario/integration tests run through end-to-end flows.**
   - Tests verify multi-module interactions and playthrough plumbing.

The suite makes dependency requirements explicit in each test file docstring,
so engineers can choose the right subset for local runs.

===============================================================================
## INPUTS AND OUTPUTS
===============================================================================

**Inputs:**
- Python modules in `engine/` referenced by tests.
- Optional FalkorDB instance (integration tests).
- Spec/schema docs referenced by consistency checks.

**Outputs:**
- Pytest pass/fail results for unit/spec tests.
- Skipped tests when required services or data are missing.

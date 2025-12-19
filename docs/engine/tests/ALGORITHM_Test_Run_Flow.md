# Engine Test Suite — Algorithm: Test Run Flow

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

===============================================================================
## CHAIN
===============================================================================

```
PATTERNS:       ./PATTERNS_Spec_Linked_Test_Suite.md
BEHAVIORS:      ./BEHAVIORS_Test_Coverage_Layers.md
VALIDATION:     ./VALIDATION_Test_Suite_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Test_File_Layout.md
TEST:           ./TEST_Test_Suite_Coverage.md
SYNC:           ./SYNC_Engine_Test_Suite.md
THIS:           ALGORITHM_Test_Run_Flow.md (you are here)
IMPL:           ../../../engine/tests/__init__.py
```

===============================================================================
## RUN FLOW
===============================================================================

1. **Collect tests under `engine/tests/`.**
2. **Execute unit/spec tests immediately.**
   - Pure logic tests run without a database.
3. **Initialize integration fixtures.**
   - Tests that require a graph database attempt to connect to FalkorDB.
4. **Skip integration tests if dependencies are missing.**
   - Database or fixture failures trigger `pytest.skip`.
5. **Report results.**
   - Unit/spec tests must pass; integration tests are either pass or skip.

===============================================================================
## COMMON RUN MODES
===============================================================================

```bash
# Full suite (unit + integration; integration may skip)
pytest engine/tests -v

# Unit/spec only (exclude integration)
pytest engine/tests -v -m "not integration"

# Integration only
pytest engine/tests -v -m integration
```

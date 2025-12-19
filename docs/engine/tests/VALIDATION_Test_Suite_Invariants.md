# Engine Test Suite — Validation: Test Invariants

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
ALGORITHM:      ./ALGORITHM_Test_Run_Flow.md
IMPLEMENTATION: ./IMPLEMENTATION_Test_File_Layout.md
TEST:           ./TEST_Test_Suite_Coverage.md
SYNC:           ./SYNC_Engine_Test_Suite.md
THIS:           VALIDATION_Test_Suite_Invariants.md (you are here)
IMPL:           ../../../engine/tests/__init__.py
```

===============================================================================
## INVARIANTS
===============================================================================

1. **Unit/spec tests must not require external services.**
2. **Integration tests must guard database access with skip logic.**
3. **Every test module documents its spec coverage in the docstring.**
4. **The suite can be executed from repo root via `pytest engine/tests`.**

===============================================================================
## VALIDATION STEPS
===============================================================================

```bash
# Ensure unit/spec tests pass without DB
pytest engine/tests -v -m "not integration"

# Verify integration tests fail fast or skip when DB is missing
pytest engine/tests -v -m integration
```

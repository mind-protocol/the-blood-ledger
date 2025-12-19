# Engine Test Suite — Test Coverage

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
VALIDATION:     ./VALIDATION_Test_Suite_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Test_File_Layout.md
SYNC:           ./SYNC_Engine_Test_Suite.md
THIS:           TEST_Test_Suite_Coverage.md (you are here)
IMPL:           ../../../engine/tests/__init__.py
```

===============================================================================
## COVERAGE SUMMARY
===============================================================================

| Area | Coverage | Notes |
|------|----------|-------|
| Physics behaviors | Partial | `test_behaviors.py` validates constants + formulas |
| Schema consistency | Partial | `test_spec_consistency.py` checks enums/constants |
| Moment lifecycle | Partial | `test_moment*.py` validates moment processing paths |
| History system | Partial | `test_history.py` exercises history service |
| Narrator integration | Partial | `test_narrator_integration.py` covers clickables |
| Integration stubs | Draft | `test_implementation.py` documents DB requirements |

===============================================================================
## HOW TO RUN
===============================================================================

```bash
# Full suite (integration tests may skip)
pytest engine/tests -v

# Unit/spec only
pytest engine/tests -v -m "not integration"

# Integration only (requires FalkorDB)
pytest engine/tests -v -m integration
```

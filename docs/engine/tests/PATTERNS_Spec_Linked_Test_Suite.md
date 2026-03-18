# Engine Test Suite — Patterns: Spec-Linked Layered Tests

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

===============================================================================
## CHAIN
===============================================================================

```
BEHAVIORS:      ./BEHAVIORS_Test_Coverage_Layers.md
ALGORITHM:      ./ALGORITHM_Test_Run_Flow.md
VALIDATION:     ./VALIDATION_Test_Suite_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Test_File_Layout.md
HEALTH:         ./HEALTH_Engine_Test_Suite.md
TEST:           ./TEST_Test_Suite_Coverage.md
SYNC:           ./SYNC_Engine_Test_Suite.md
THIS:           PATTERNS_Spec_Linked_Test_Suite.md (you are here)
IMPL:           ../../../engine/tests/__init__.py
```

===============================================================================
## THE PROBLEM
===============================================================================

The engine relies on a web of rules (physics, moments, schema invariants, and
story mechanics). Without a coherent test suite, changes to these rules can
silently drift from the spec and break core gameplay behaviors.

===============================================================================
## THE PATTERN
===============================================================================

**Use a layered test suite that ties every behavioral claim back to the spec.**

Engine tests are organized by dependency level:
- **Behavior/spec tests**: pure logic checks with no database dependency.
- **Model/schema tests**: validate enums, constants, and data shapes.
- **Integration/E2E tests**: exercise graph-backed behavior and require
  external services (FalkorDB), skipping when unavailable.

Each test file documents the spec or invariant it validates, making the tests
the executable spine of the design documents.

===============================================================================
## PRINCIPLES
===============================================================================

### Principle 1: Spec-First Assertions

Behavioral tests encode the spec so that any drift surfaces immediately in
pytest, not in gameplay.

### Principle 2: Layered Dependencies

Tests declare their environment needs and skip gracefully when dependencies
like the graph database are missing.

### Principle 3: Documentation In the Test Header

Each test file starts with a docstring that states what it validates, which
spec clauses it covers, and how to run it.

===============================================================================
## DEPENDENCIES
===============================================================================

| Module | Why We Depend On It |
|--------|----------------------|
| engine/models | Schema models and enums referenced by unit tests |
| engine/physics | Physics constants and tick behavior tested in isolation |
| engine/infrastructure | Integration points exercised by scenario tests |
| docs/schema/SCHEMA.md | Schema reference used by spec consistency tests |
| data/init/BLOOD_LEDGER_DESIGN_DOCUMENT.md | Design spec referenced in tests |

===============================================================================
## DATA
===============================================================================

Test metadata lives in docstrings and module headers. Assertions reference
spec IDs, invariant names, or doc sections so failures can be traced back to
the design contract without reverse engineering the test intent.

===============================================================================
## INSPIRATIONS
===============================================================================

- Spec-driven testing practices where every assertion cites a requirement.
- Layered test pyramids that keep fast unit tests separate from slow I/O runs.

===============================================================================
## SCOPE
===============================================================================

In scope: engine test organization, spec-linked assertions, and skip behavior
for external dependencies. Out of scope: frontend tests, load tests, and full
CI orchestration.

===============================================================================
## WHAT THIS DOES NOT SOLVE
===============================================================================

- It does not stand up external services for integration tests.
- It does not cover frontend rendering or UI interactions.
- It does not guarantee narrative quality, only mechanical correctness.

===============================================================================
## GAPS / IDEAS / QUESTIONS
===============================================================================

- [ ] Add BEHAVIORS/TEST docs when test categories stabilize.
- [ ] Align spec path references in tests with canonical schema docs.
- IDEA: Add CI profiles for unit vs integration runs.

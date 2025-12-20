# Engine Test Suite — Implementation: File Layout

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
TEST:           ./TEST_Test_Suite_Coverage.md
SYNC:           ./SYNC_Engine_Test_Suite.md
THIS:           IMPLEMENTATION_Test_File_Layout.md (you are here)
IMPL:           ../../../engine/tests/__init__.py
```

===============================================================================
## DIRECTORY STRUCTURE
===============================================================================

```
engine/tests/__init__.py
engine/tests/test_behaviors.py
engine/tests/test_e2e_moment_graph.py
engine/tests/test_history.py
engine/tests/test_implementation.py
engine/tests/test_integration_scenarios.py
engine/tests/test_models.py
engine/tests/test_moment.py
engine/tests/test_moment_graph.py
engine/tests/test_moment_lifecycle.py
engine/tests/test_moment_standalone.py
engine/tests/test_moments_api.py
engine/tests/test_narrator_integration.py
engine/tests/test_spec_consistency.py
```

===============================================================================
## FILE RESPONSIBILITIES
===============================================================================

| File | Responsibility |
| --- | --- |
| `engine/tests/__init__.py` | Test package marker with DOCS pointer for the suite. |
| `engine/tests/test_behaviors.py` | Physics behavior invariants (time progression, constants, decay, pressure). |
| `engine/tests/test_e2e_moment_graph.py` | End-to-end moment graph flow with FalkorDB (create, click, decay, lifecycle). |
| `engine/tests/test_history.py` | History module tests for conversations, timestamps, and history queries. |
| `engine/tests/test_implementation.py` | Integration stubs requiring running systems and FalkorDB. |
| `engine/tests/test_integration_scenarios.py` | Structural integration tests over models and relationships. |
| `engine/tests/test_models.py` | Pydantic schema validation for nodes, links, and tensions. |
| `engine/tests/test_moment.py` | Moment model, GraphOps/GraphQueries helpers (ngram repo), processor, transcript handling. |
| `engine/tests/test_moment_graph.py` | Moment graph schema, view queries, click handling, scene tree mapping. |
| `engine/tests/test_moment_lifecycle.py` | Moment lifecycle operations (decay, dormancy, reactivation, GC). |
| `engine/tests/test_moment_standalone.py` | Standalone moment model/helper checks without pytest. |
| `engine/tests/test_moments_api.py` | FastAPI moment endpoints (current view, click, surface, stats, stream). |
| `engine/tests/test_narrator_integration.py` | Narrator/moment integration around clickables and processor schema. |
| `engine/tests/test_spec_consistency.py` | Spec/schema consistency and enum/constant checks. |

===============================================================================
## ENTRY POINTS
===============================================================================

**Primary module header:** `engine/tests/__init__.py`

**Key files by role:**
- `engine/tests/test_behaviors.py`: Physics and tension formula invariants.
- `engine/tests/test_e2e_moment_graph.py`: End-to-end moment graph flow with FalkorDB.
- `engine/tests/test_history.py`: Conversation threads, timestamps, and history queries.
- `engine/tests/test_models.py`: Pydantic schema validation for nodes/links/tensions.
- `engine/tests/test_spec_consistency.py`: Schema/spec consistency checks.
- `engine/tests/test_implementation.py`: Integration stubs for DB-backed systems.
- `engine/tests/test_integration_scenarios.py`: Multi-module scenario validation.
- `engine/tests/test_moment.py`: Moment processing, queries, and transcript handling.
- `engine/tests/test_moment_graph.py`: Moment graph transitions and attachments.
- `engine/tests/test_moment_lifecycle.py`: Moment lifecycle state coverage.
- `engine/tests/test_moment_standalone.py`: Moment behavior without graph fixtures.
- `engine/tests/test_moments_api.py`: Moment API endpoints and SSE stream tests.
- `engine/tests/test_narrator_integration.py`: Narrator clickables and processor integration.

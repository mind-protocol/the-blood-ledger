# Moment Graph — Test Coverage

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Moments.md
BEHAVIORS:      ./BEHAVIORS_Moment_Lifecycle.md
ALGORITHM:      ./ALGORITHM_Moment_Graph_Operations.md
VALIDATION:     ./VALIDATION_Moment_Graph_Invariants.md
IMPLEMENTATION: ./IMPLEMENTATION_Moment_Graph_Stub.md
SYNC:           ./SYNC_Moments.md
THIS:           TEST_Moment_Graph_Coverage.md (you are here)
IMPL:           engine/moments/__init__.py
```

---

## CURRENT COVERAGE

Tests exist for moment graph behavior in the engine test suite, but the
moment graph module itself is still a stub.

| Area | Coverage | Location |
|------|----------|----------|
| Moment graph behavior | partial | `engine/tests/test_moment_graph.py` |
| Moment lifecycle | partial | `engine/tests/test_moment_lifecycle.py` |
| Moments API | partial | `engine/tests/test_moments_api.py` |
| End-to-end moment graph | partial | `engine/tests/test_e2e_moment_graph.py` |

---

## GAPS

- No direct tests cover a concrete graph-backed Moment implementation yet.
- The stub module does not expose behavior to validate directly.

---

## HOW TO RUN

```bash
pytest engine/tests/test_moment_graph.py \
  engine/tests/test_moment_lifecycle.py \
  engine/tests/test_moments_api.py \
  engine/tests/test_e2e_moment_graph.py
```

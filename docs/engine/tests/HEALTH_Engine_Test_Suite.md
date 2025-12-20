# Engine Tests — Health: Test Suite Coverage

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the engine test suite execution. It exists to catch
regressions that break core engine invariants. It does not verify frontend
behavior.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Spec_Linked_Test_Suite.md
BEHAVIORS:       ./BEHAVIORS_Test_Coverage_Layers.md
ALGORITHM:       ./ALGORITHM_Test_Run_Flow.md
VALIDATION:      ./VALIDATION_Test_Suite_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Test_File_Layout.md
THIS:            HEALTH_Engine_Test_Suite.md
SYNC:            ./SYNC_Engine_Test_Suite.md
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: engine_tests_pass
    flow_id: test_run
    priority: high
    rationale: Core engine invariants rely on passing tests.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: engine_tests_pass
```

---

## HOW TO RUN

```bash
pytest engine/tests
```

---

## KNOWN GAPS

- [ ] Test coverage is incomplete; failing tests may not cover all invariants.

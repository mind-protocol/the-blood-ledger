# Narrator — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2024-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
THIS:            TEST_Narrator.md (you are here)
SYNC:            ./SYNC_Narrator.md

IMPL:            engine/tests/test_narrator_integration.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY (Condensed)

1. Schema validation (output structure)
2. Behavioral checks (classification, clickables)
3. Integration (tool calls + graph updates)
4. Human review (voice quality)

---

## KEY TESTS

### Schema
- `test_dialogue_chunk_valid`
- `test_mutation_valid`
- `test_scene_tree_valid`

### Clickables
- `test_parse_inline_clickable`
- `test_multiple_clickables`
- `test_clickable_in_quotes`

### Integration (manual/partial)
- Conversational: no `time_elapsed`, `scene: {}`
- Significant: `time_elapsed` present, SceneTree returned
- Invention: invented content -> mutation -> graph

---

## HOW TO RUN

```bash
pytest engine/tests/test_narrator_integration.py -v
pytest engine/tests/test_models.py -v -k narrator
```

---

## KNOWN GAPS

- [ ] No automated behavioral tests
- [ ] No voice consistency automation
- [ ] No regression tests for prompt changes
- [ ] No performance/latency tests

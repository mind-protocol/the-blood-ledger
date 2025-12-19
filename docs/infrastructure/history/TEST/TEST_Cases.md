# History — Test Cases

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:    ../PATTERNS_History.md
BEHAVIORS:   ../BEHAVIORS_History.md
ALGORITHM:   ../ALGORITHM/ALGORITHM_Overview.md
VALIDATION:  ../VALIDATION_History.md
THIS:        TEST_Cases.md
OVERVIEW:    ./TEST_Overview.md
IMPLEMENTATION: ../IMPLEMENTATION_History_Service_Architecture.md
SYNC:        ../SYNC_History.md
```

---

## UNIT TESTS

### Invariant Tests

| Test | Expected | Status |
|------|----------|--------|
| `test_no_orphan_narratives` | All narratives have >=1 BELIEVES edge | pending |
| `test_source_xor_detail` | Each narrative has source OR detail, not both/neither | pending |
| `test_belief_bounds` | Beliefs in [0.0, 1.0] | pending |
| `test_timestamp_consistency` | BELIEVES.when >= narrative.occurred_at | pending |

### Query Tests

| Test | Expected | Status |
|------|----------|--------|
| `test_query_own_beliefs_only` | Only narratives character BELIEVES | pending |
| `test_query_by_person` | Narratives mentioning target character | pending |
| `test_query_by_place` | Narratives at/about place | pending |
| `test_query_by_time_range` | Narratives in range | pending |
| `test_query_empty_beliefs` | Empty result, no error | pending |

### Recording Tests

| Test | Expected | Status |
|------|----------|--------|
| `test_record_player_history` | Narrative + beliefs created | pending |
| `test_conversation_appended` | Markdown file updated | pending |
| `test_source_reference_valid` | source.file and source.section match | pending |
| `test_record_world_history` | Narrative with detail field | pending |
| `test_witness_beliefs_created` | BELIEVES for each witness | pending |

### Propagation Tests

| Test | Expected | Status |
|------|----------|--------|
| `test_propagation_nearby` | Nearby characters learn | pending |
| `test_propagation_distant` | Distant confidence lower | pending |
| `test_propagation_no_cycles` | No infinite loops | pending |
| `test_propagation_respects_distance` | Confidence decreases with hops | pending |

---

## INTEGRATION TESTS (SUMMARY)

- Scene recording to query flow
- World event to player discovery
- "They remembered" callback flow

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| query_history() | 0% | Not implemented |
| record_player_history() | 0% | Not implemented |
| record_world_history() | 0% | Not implemented |
| propagate_belief() | 0% | Not implemented |
| read_markdown_section() | 0% | Not implemented |

---

## KNOWN TEST GAPS

- [ ] Property-based tests for query filtering
- [ ] Stress test with thousands of narratives
- [ ] Test timestamp parsing edge cases
- [ ] Test concurrent writes to conversation files
- [ ] Test graph consistency under partial failures

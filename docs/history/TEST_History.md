# History — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_History.md
BEHAVIORS:   ./BEHAVIORS_History.md
ALGORITHM:   ./ALGORITHM_History.md
VALIDATION:  ./VALIDATION_History.md
THIS:        TEST_History.md (you are here)
SYNC:        ./SYNC_History.md
```

---

## TEST STRATEGY

The history system is foundational — if it breaks, "they remembered" moments fail. Testing strategy:

1. **Invariant tests** — Ensure data integrity (no orphans, valid references)
2. **Query tests** — Verify belief filtering works correctly
3. **Recording tests** — Verify both player-experienced and world-generated paths
4. **Integration tests** — Full flows from event to retrieval
5. **Experience tests** — Manual validation that memory feels right

Priority: Invariants first (data integrity), then queries (functionality), then experience (feel).

---

## UNIT TESTS

### Invariant Tests

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_no_orphan_narratives` | Graph with narratives | All narratives have >=1 BELIEVES edge | pending |
| `test_source_xor_detail` | Graph with narratives | Each has source OR detail, not both/neither | pending |
| `test_belief_bounds` | Graph with beliefs | All beliefs in [0.0, 1.0] | pending |
| `test_timestamp_consistency` | Graph with beliefs | All BELIEVES.when >= narrative.occurred_at | pending |

### Query Tests

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_query_own_beliefs_only` | player queries | Only narratives player BELIEVES | pending |
| `test_query_by_person` | query about "aldric" | Only narratives mentioning Aldric | pending |
| `test_query_by_place` | query about "york" | Narratives at/about York | pending |
| `test_query_by_time_range` | query Day 3-5 | Only narratives in range | pending |
| `test_query_empty_beliefs` | character with no beliefs | Empty result, no error | pending |

### Recording Tests

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_record_player_history` | scene data + witnesses | Narrative + beliefs created | pending |
| `test_conversation_appended` | scene data | Markdown file updated | pending |
| `test_source_reference_valid` | recorded narrative | source.file and source.section match | pending |
| `test_record_world_history` | off-screen event | Narrative with detail field | pending |
| `test_witness_beliefs_created` | 3 witnesses | 3 BELIEVES edges | pending |

### Propagation Tests

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_propagation_nearby` | event at place | Nearby characters learn | pending |
| `test_propagation_distant` | event at place | Distant chars have lower confidence | pending |
| `test_propagation_no_cycles` | connected graph | No infinite loops | pending |
| `test_propagation_respects_distance` | multi-hop | Confidence decreases with hops | pending |

---

## INTEGRATION TESTS

### Scene Recording to Query

```
GIVEN:  Empty graph with player, Aldric
        No conversation files exist
WHEN:   record_player_history({
            content: "Aldric told me about his brother",
            conversation: "Aldric: My brother held the bridge...",
            witnesses: ["player", "char_aldric"],
            occurred_at: "Day 4, night",
            occurred_where: "place_camp"
        })
THEN:   Conversation file created with section
AND:    Narrative node exists with source reference
AND:    Player BELIEVES with source="participated"
AND:    Aldric BELIEVES with source="participated"
AND:    query_history("player", about="aldric") returns narrative
AND:    Result includes full conversation text
STATUS: pending
```

### World Event to Player Discovery

```
GIVEN:  Graph with player at Durham, characters at York
        York uprising happens (world-generated)
WHEN:   record_world_history({
            content: "Saxon thegns seized York",
            detail: "The rebellion began at dawn...",
            occurred_at: "Day 12, dawn",
            occurred_where: "place_york",
            witnesses: ["char_malet", "char_cumin"]
        })
THEN:   Narrative has detail field (no conversation)
AND:    Malet BELIEVES with high confidence
AND:    Player does NOT believe (too far)
AND:    query_history("player", place="york") returns empty
AND:    After player reaches York and is told:
        query_history("player", place="york") returns narrative
STATUS: pending
```

### "They Remembered" Flow

```
GIVEN:  Player killed guard at Day 5
        Guard's friend exists, witnessed (low confidence rumor)
        Time passes to Day 10
WHEN:   Player encounters guard's friend
AND:    Narrator queries friend's beliefs about player
THEN:   narr_guard_killed appears in results
AND:    Narrator can generate dialogue referencing the killing
STATUS: pending
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Query with no matching beliefs | Return empty list, not error | pending |
| Narrative about multiple characters | Appears in queries for all | pending |
| Same event, different beliefs | Both players and characters can have different confidence | pending |
| Very old narrative | Still retrievable, timestamp correct | pending |
| Conversation file deleted | Query returns narrative without conversation, logs warning | pending |
| Malformed timestamp | Graceful handling, logged | pending |

---

## TEST FIXTURES

### Minimal Graph Fixture

```python
@pytest.fixture
def minimal_graph():
    """Graph with player, one character, one narrative, one belief"""
    return {
        "nodes": [
            {"id": "player", "type": "Character"},
            {"id": "char_aldric", "type": "Character"},
            {"id": "narr_test", "type": "Narrative",
             "content": "Test narrative",
             "detail": "Full test detail",
             "occurred_at": "Day 1, morning"}
        ],
        "edges": [
            {"from": "player", "to": "narr_test", "type": "BELIEVES",
             "believes": 1.0, "source": "witnessed", "when": "Day 1, morning"}
        ]
    }
```

### Rolf Story Fixture

```python
@pytest.fixture
def rolf_story_graph():
    """Full Rolf starter story with Edmund conflict"""
    # Player, Edmund, Aldric, Mildred
    # The Betrayal vs The Salvation narratives
    # Conflicting beliefs
    ...
```

### Conversation File Fixture

```python
@pytest.fixture
def sample_conversation_file(tmp_path):
    """Create a sample conversation markdown file"""
    content = """# Conversations with Aldric

## Day 4, Night — The Camp

Aldric stares into the fire. He hasn't spoken in an hour.

You: "You fought at Stamford Bridge."
Aldric: "Aye."
You: "What happened?"
Aldric: *long pause* "My brother held the bridge."
"""
    file = tmp_path / "conversations" / "char_aldric.md"
    file.parent.mkdir(parents=True)
    file.write_text(content)
    return file
```

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

## HOW TO RUN

```bash
# Run all history tests
pytest tests/engine/test_history.py -v

# Run specific test category
pytest tests/engine/test_history.py -k "invariant" -v
pytest tests/engine/test_history.py -k "query" -v
pytest tests/engine/test_history.py -k "record" -v

# Run with coverage
pytest tests/engine/test_history.py --cov=engine/history --cov-report=html

# Run integration tests only
pytest tests/engine/test_history.py -m integration -v
```

---

## KNOWN TEST GAPS

- [ ] Property-based tests for query filtering
- [ ] Stress test with thousands of narratives
- [ ] Test timestamp parsing edge cases
- [ ] Test concurrent writes to conversation files
- [ ] Test graph consistency under partial failures

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| None yet | - | - | - |

---

## EXPERIENCE TESTS (MANUAL)

These can't be fully automated — they test feel, not correctness.

### Test: Memory Surfaces Organically

**Procedure:**
1. Play for 1 hour, making notable choices
2. Continue playing for another hour
3. Note every time an character references past events

**Pass if:** At least 3 organic references per 2-hour session
**Fail if:** References feel forced or never happen

### Test: Chronicle Is Accurate

**Procedure:**
1. Play for 2 hours, noting key events mentally
2. Open Chronicle view
3. Compare Chronicle to memory

**Pass if:** All remembered events appear; order is correct
**Fail if:** Events missing or out of order

### Test: Belief Uncertainty Feels Real

**Procedure:**
1. Create scenario where character has low-confidence belief
2. Query character's history
3. Observe how confidence affects dialogue

**Pass if:** Low-confidence beliefs feel uncertain in character speech
**Fail if:** All beliefs treated equally regardless of confidence

---

## GAPS / IDEAS / QUESTIONS

- [ ] How to mock FalkorDB for unit tests?
- [ ] Should we test with real graph DB for integration?
- [ ] Need test data generator for large graphs
- IDEA: Record actual play sessions for regression tests
- IDEA: Use LLM to evaluate "organic" vs "forced" references
- QUESTION: What's acceptable query latency for tests?

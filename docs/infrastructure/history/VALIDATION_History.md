# History — Validation: Invariants and Verification

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
THIS:        VALIDATION_History.md (you are here)
IMPLEMENTATION: ./IMPLEMENTATION_History_Service_Architecture.md
TEST:        ./TEST_History.md
SYNC:        ./SYNC_History.md
```

---

## INVARIANTS

These must ALWAYS be true:

### V1: No Orphan Narratives

```
Every narrative in the graph must have at least one BELIEVES edge
(Someone must know about it, or it shouldn't exist)
```

**Checked by:** `test_no_orphan_narratives` — query for narratives with zero incoming BELIEVES

### V2: Source XOR Detail

```
A narrative has EITHER source.file (player-experienced)
OR detail field (world-generated)
NEVER both, NEVER neither (for historical narratives)
```

**Checked by:** `test_source_xor_detail` — validate all narrative nodes

### V3: Conversation Sections Exist

```
If narrative.source.file and narrative.source.section exist,
the referenced file must exist and contain that section header
```

**Checked by:** `test_conversation_references` — for each source, verify file/section

### V4: Timestamp Consistency

```
For any BELIEVES edge:
  believes.when >= narrative.occurred_at
(You can't learn about something before it happened)
```

**Checked by:** `test_timestamp_consistency` — compare all BELIEVES.when to narrative.occurred_at

### V5: Belief Bounds

```
0.0 <= believes.believes <= 1.0
(Confidence is always a valid probability)
```

**Checked by:** `test_belief_bounds` — validate all BELIEVES edges

---

## PROPERTIES

For property-based testing:

### P1: Query Respects Belief Filter

```
FORALL character_id, query_params:
    results = query_history(character_id, query_params)
    FORALL narrative IN results:
        EXISTS (character_id)-[BELIEVES]->(narrative)
```

**Tested by:** `test_query_respects_beliefs` | NOT YET TESTED — needs graph implementation

### P2: Recording Creates Complete Links

```
FORALL event_data, witnesses:
    narrative_id = record_player_history(event_data, witnesses)
    FORALL witness IN witnesses:
        EXISTS (witness)-[BELIEVES]->(narrative_id)
```

**Tested by:** `test_recording_creates_links` | NOT YET TESTED — needs graph implementation

### P3: Propagation Degrades Confidence

```
FORALL narrative, origin_place, distant_place:
    propagate_belief(narrative, origin_place)
    near_belief = get_belief(nearby_char, narrative)
    far_belief = get_belief(distant_char, narrative)
    near_belief.believes >= far_belief.believes
```

**Tested by:** `test_propagation_degrades` | NOT YET TESTED — needs propagation implementation

---

## ERROR CONDITIONS

### E1: Missing Conversation File

```
WHEN:    Narrative has source.file that doesn't exist
THEN:    query_history returns narrative with conversation=None
         and logs warning
SYMPTOM: History query returns incomplete results
```

**Tested by:** `test_missing_conversation_file` | NOT YET TESTED

### E2: Invalid Section Reference

```
WHEN:    Narrative has source.section not found in file
THEN:    query_history returns narrative with conversation=None
         and logs warning
SYMPTOM: Narrator can't retrieve full dialogue
```

**Tested by:** `test_invalid_section_reference` | NOT YET TESTED

### E3: Circular Belief Propagation

```
WHEN:    Propagation logic could create infinite loops
THEN:    Must detect visited characters and stop
SYMPTOM: Infinite loop, memory exhaustion
```

**Tested by:** `test_propagation_no_cycles` | NOT YET TESTED

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: No orphan narratives | `test_no_orphan_narratives` | NOT YET TESTED |
| V2: Source XOR detail | `test_source_xor_detail` | NOT YET TESTED |
| V3: Conversation sections exist | `test_conversation_references` | NOT YET TESTED |
| V4: Timestamp consistency | `test_timestamp_consistency` | NOT YET TESTED |
| V5: Belief bounds | `test_belief_bounds` | NOT YET TESTED |
| P1: Query respects beliefs | `test_query_respects_beliefs` | NOT YET TESTED |
| P2: Recording creates links | `test_recording_creates_links` | NOT YET TESTED |
| P3: Propagation degrades | `test_propagation_degrades` | NOT YET TESTED |
| E1: Missing file | `test_missing_conversation_file` | NOT YET TESTED |
| E2: Invalid section | `test_invalid_section_reference` | NOT YET TESTED |
| E3: No cycles | `test_propagation_no_cycles` | NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Create a player-experienced narrative — verify conversation appended
[ ] Create a world-generated narrative — verify detail field present
[ ] Query as player — verify only player's beliefs returned
[ ] Query as character — verify only character's beliefs returned
[ ] Check cross-character: player doesn't see character-only beliefs
[ ] Verify timestamps: learning is after occurrence
[ ] Test propagation: distant characters have lower confidence
```

### Automated

```bash
# Run history module tests
pytest tests/engine/test_history.py

# Run with coverage
pytest tests/engine/test_history.py --cov=engine/history

# Run invariant checks
python scripts/check_history_invariants.py
```

---

## INTEGRATION TESTS

### I1: Full Scene Recording Flow

```
GIVEN:  Empty graph with player and character
WHEN:   Narrator records a scene with dialogue
THEN:   Conversation file updated
AND:    Narrative created with source reference
AND:    Both characters have BELIEVES
AND:    Query returns narrative with full conversation
```

### I2: World Update Recording Flow

```
GIVEN:  Graph with player distant from York
WHEN:   Runner records York uprising
THEN:   Narrative created with detail
AND:    Characters at York have high-confidence beliefs
AND:    Player has NO belief (too far)
AND:    Query by player returns nothing about York
```

### I3: "They Remembered" Moment

```
GIVEN:  Player killed guard in Day 5
AND:    Guard's friend exists in graph
WHEN:   Player encounters guard's friend in Day 10
THEN:   Friend's query returns the killing narrative
AND:    Narrator can reference it in scene
```

---

## SYNC STATUS

```
LAST_VERIFIED: Not yet verified
VERIFIED_AGAINST: N/A (not implemented)
VERIFIED_BY: N/A
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
    V4: NOT RUN
    V5: NOT RUN
```

---

## EXPERIENCE VALIDATION

Beyond technical correctness, the history system must deliver these experiences:

### "They Remembered"

**Test:** Play for 2+ hours. Did an character reference something from hour 1?
**Pass criteria:** At least one organic callback per hour of play
**How to measure:** Log when narratives surface; count callbacks

### "I Was Wrong"

**Test:** Player discovers their foundational belief was mistaken
**Pass criteria:** Player's belief state can differ from truth; revelation is impactful
**How to measure:** Player interviews after session

### Chronicle Makes Sense

**Test:** Open Chronicle after 5 hours of play
**Pass criteria:** Chronological record matches player's experience; no missing events
**How to measure:** Compare Chronicle to session recording

---

## GAPS / IDEAS / QUESTIONS

- [ ] Performance benchmarks: how many narratives before queries slow?
- [ ] Integration test with actual FalkorDB
- [ ] Test narrative weight's effect on surfacing
- IDEA: Fuzzing conversation references for robustness
- IDEA: Property-based test: belief confidence never increases through propagation
- QUESTION: How to test "organic" callbacks? (LLM judgment?)

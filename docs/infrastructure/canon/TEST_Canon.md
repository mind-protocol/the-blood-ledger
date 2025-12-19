# Canon Holder — Test

```
STATUS: SPEC
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Canon.md
BEHAVIORS:       ./BEHAVIORS_Canon.md
ALGORITHM:       ./ALGORITHM_Canon_Holder.md
VALIDATION:      ./VALIDATION_Canon.md
IMPLEMENTATION:  ./IMPLEMENTATION_Canon.md
THIS:            TEST_Canon.md (you are here)
SYNC:            ./SYNC_Canon.md

IMPL:            tests/infrastructure/canon/test_canon_holder.py
```

---

## TEST STRATEGY

1. **Unit tests** for each query (Q1-Q10) in isolation
2. **Behavior tests** for each B1-B9 from BEHAVIORS
3. **Invariant tests** for V1-V7 from VALIDATION
4. **Integration tests** for full flow (tick → surface → record → SSE)

Use test graph with known structure. No mocking FalkorDB — test against real instance.

---

## UNIT TESTS

### Query Tests

| Test | Query | Input | Expected | Status |
|------|-------|-------|----------|--------|
| `test_q1_detect_ready` | Q1 | moments with salience 0.2, 0.3, 0.5 | returns only 0.3, 0.5 | pending |
| `test_q2_presence_met` | Q2 | moment attached to present char | missing_count = 0 | pending |
| `test_q2_presence_unmet` | Q2 | moment attached to absent char | missing_count = 1 | pending |
| `test_q3_player_location` | Q3 | player AT place_camp | returns place_camp | pending |
| `test_q5_speaker_present` | Q5 | char with CAN_SPEAK at location | returns char_id | pending |
| `test_q5_speaker_asleep` | Q5 | char with CAN_SPEAK but sleeping | returns NULL | pending |
| `test_q5_speaker_absent` | Q5 | char with CAN_SPEAK at different place | returns NULL | pending |
| `test_q5_highest_wins` | Q5 | two chars, strength 0.8 and 0.5 | returns 0.8 char | pending |
| `test_q7_last_spoken` | Q7 | three spoken moments | returns highest tick | pending |

---

## BEHAVIOR TESTS

### B1: Moment Surfaces When Salient

```
GIVEN:  Moment with status='possible', weight=0.5, energy=0.8 (salience=0.4)
        Attached to char_aldric with presence_required=true
        char_aldric AT place_camp
        char_player AT place_camp
WHEN:   detect_and_surface() runs
THEN:   Moment status becomes 'active'
        SSE 'moment_activated' sent
STATUS: pending
```

### B2: Active Moment Becomes Canon

```
GIVEN:  Moment with status='active', type='dialogue'
        char_aldric has CAN_SPEAK to moment with strength=0.9
        char_aldric AT place_camp, state='awake', alive=true
        char_player AT place_camp
WHEN:   process_ready_moments() runs
THEN:   Moment status becomes 'spoken'
        SAID link created from char_aldric
        THEN link created from previous moment
        SSE 'moment_spoken' sent
STATUS: pending
```

### B3: Speaking Costs Energy

```
GIVEN:  Moment with energy=1.0, status='active'
WHEN:   Moment is recorded to canon
THEN:   Moment energy becomes 0.4
STATUS: pending
```

### B4: Highest Weight Speaker Wins

```
GIVEN:  Moment with two CAN_SPEAK links
        char_aldric strength=0.9, present, awake
        char_edmund strength=0.7, present, awake
WHEN:   determine_speaker() runs
THEN:   Returns char_aldric
STATUS: pending
```

### B5: Moment Goes Dormant

```
GIVEN:  Moment with status='active'
        ATTACHED_TO char_aldric with presence_required=true, persistent=true
        char_aldric AT place_camp
        char_player AT place_camp
WHEN:   Player moves to place_york (char_aldric stays at camp)
THEN:   Moment status becomes 'dormant'
STATUS: pending
```

### B6: Dormant Reactivates

```
GIVEN:  Moment with status='dormant'
        ATTACHED_TO char_aldric with presence_required=true
        char_aldric AT place_camp
        char_player AT place_york
WHEN:   Player moves back to place_camp
THEN:   Moment status becomes 'active'
        SSE 'moment_activated' sent
STATUS: pending
```

### B7: Moments Decay

```
GIVEN:  Moment with weight=0.005, status='active'
WHEN:   Decay check runs
THEN:   Moment status becomes 'decayed'
STATUS: pending
```

### B8: Multiple Moments Paced

```
GIVEN:  5 moments with status='active', all valid speakers
        Salience: 0.9, 0.8, 0.7, 0.6, 0.5
WHEN:   process_ready_moments() runs
THEN:   Only top 3 (0.9, 0.8, 0.7) become spoken
        Others remain active
        THEN links chain: m1 → m2 → m3
STATUS: pending
```

### B9: Dialogue Without Speaker Waits

```
GIVEN:  Moment with status='active', type='dialogue'
        CAN_SPEAK link to char_aldric
        char_aldric AT place_york (different from player)
WHEN:   process_ready_moments() runs
THEN:   Moment remains 'active'
        No SAID link created
STATUS: pending
```

---

## EDGE CASE TESTS

### E1: First Moment (No Previous)

```
GIVEN:  No spoken moments in graph
        One active moment ready
WHEN:   process_ready_moments() runs
THEN:   Moment becomes spoken
        No THEN link created (nothing to link from)
STATUS: pending
```

### E2: Narration Moment

```
GIVEN:  Moment with type='narration', status='active'
        No CAN_SPEAK links
WHEN:   process_ready_moments() runs
THEN:   Moment becomes spoken
        No SAID link created
        speaker=NULL in SSE event
STATUS: pending
```

### E3: All Speakers Asleep

```
GIVEN:  Dialogue moment with status='active'
        Only CAN_SPEAK character has state='sleeping'
WHEN:   process_ready_moments() runs
THEN:   Moment remains active
STATUS: pending
```

### E4: Player Input Moment

```
GIVEN:  Moment created from player click
        Previous spoken moment exists
WHEN:   record_to_canon() called with player_caused=true
THEN:   THEN link has player_caused=true
STATUS: pending
```

---

## INTEGRATION TESTS

### Full Tick Cycle

```
GIVEN:  Fresh playthrough graph
        Player at place_camp
        char_aldric at place_camp, awake
        3 possible moments:
          m1: salience=0.5, attached to aldric (presence_required)
          m2: salience=0.2, attached to camp
          m3: salience=0.4, attached to aldric
WHEN:   Full tick runs (detect_and_surface + process_ready_moments)
THEN:   m1 and m3 become active then spoken (above threshold)
        m2 remains possible (below threshold)
        THEN chain: m1 → m3 (by salience order)
        Two SSE events sent
STATUS: pending
```

### Location Change Flow

```
GIVEN:  Active conversation at place_camp
        Player moves to place_york
WHEN:   Location change handler runs
THEN:   Camp-attached moments go dormant
        York-attached moments activate
        SSE events reflect changes
STATUS: pending
```

### Click Traversal + Canon

```
GIVEN:  Active moment m1 with CAN_LEAD_TO → m2
        m2 has status='possible'
WHEN:   Player clicks word in m1
THEN:   m2 becomes active
        m2 immediately processed by Canon Holder
        m2 becomes spoken
        THEN link: m1 → m2 with player_caused=true
STATUS: pending
```

---

## TEST FIXTURES

### Minimal Graph

```python
@pytest.fixture
def minimal_graph():
    """Player + one character + one place + one moment."""
    return {
        'nodes': [
            {'id': 'char_player', 'label': 'Character', 'type': 'player'},
            {'id': 'char_aldric', 'label': 'Character', 'type': 'companion', 'state': 'awake', 'alive': True},
            {'id': 'place_camp', 'label': 'Place'},
            {'id': 'moment_1', 'label': 'Moment', 'status': 'possible', 'type': 'dialogue', 'weight': 0.5, 'energy': 0.8}
        ],
        'links': [
            {'from': 'char_player', 'to': 'place_camp', 'type': 'AT', 'present': 1.0},
            {'from': 'char_aldric', 'to': 'place_camp', 'type': 'AT', 'present': 1.0},
            {'from': 'char_aldric', 'to': 'moment_1', 'type': 'CAN_SPEAK', 'strength': 0.9},
            {'from': 'moment_1', 'to': 'char_aldric', 'type': 'ATTACHED_TO', 'presence_required': True, 'persistent': True}
        ]
    }
```

### Conversation Graph

```python
@pytest.fixture
def conversation_graph():
    """Multi-moment graph with transitions."""
    # ... extended fixture with 5 moments, CAN_LEAD_TO links
```

---

## HOW TO RUN

```bash
# Run all canon tests
pytest tests/infrastructure/canon/ -v

# Run specific behavior
pytest tests/infrastructure/canon/test_canon_holder.py::test_b2_active_becomes_canon -v

# Run with coverage
pytest tests/infrastructure/canon/ --cov=engine/infrastructure/canon --cov-report=html

# Run integration only
pytest tests/infrastructure/canon/ -m integration -v
```

---

## KNOWN TEST GAPS

- [ ] Property-based tests for THEN chain acyclicity
- [ ] Stress test with 100+ moments
- [ ] Concurrent tick handling
- [ ] SSE delivery verification (mock or actual client?)

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| (none yet) | — | — | — |

---

## GAPS / IDEAS / QUESTIONS

- QUESTION: How to test SSE events? Mock broadcast function or spin up test client?
- IDEA: Snapshot testing for graph state after operations
- IDEA: Hypothesis for property-based testing of status transitions

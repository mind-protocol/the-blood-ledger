# Narrator — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2024-12-19
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

## TEST STRATEGY

The Narrator is an LLM agent, not deterministic code. Testing requires:

1. **Schema Validation** — Output structure must be correct
2. **Behavioral Testing** — Key behaviors must manifest
3. **Integration Testing** — Tool calls must work end-to-end
4. **Quality Sampling** — Human review of output quality

### Testing Pyramid

```
        ┌───────────────────┐
        │  Human Quality    │  ← Manual review, gold standards
        │     Review        │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │   Behavioral      │  ← Does it follow the rules?
        │     Tests         │     (classification, voice, etc.)
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │   Integration     │  ← Tools work? Graph updates?
        │     Tests         │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │   Schema/Unit     │  ← Output validates? Mutations correct?
        │     Tests         │
        └─────────────────────┘
```

---

## UNIT TESTS

### Schema Validation

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_dialogue_chunk_valid` | DialogueChunk JSON | Validates against schema | ✓ Covered |
| `test_mutation_valid` | GraphMutation JSON | Validates against Pydantic | ✓ Covered |
| `test_scene_tree_valid` | SceneTree JSON | Validates against schema | ✓ Covered |

### Clickable Parsing

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_parse_inline_clickable` | `"[word](speaks)"` | `{word: "word", speaks: "speaks"}` | ✓ Covered |
| `test_multiple_clickables` | Text with 3 clickables | All 3 parsed | ✓ Covered |
| `test_clickable_in_quotes` | Dialogue with clickable | Parsed correctly | ✓ Covered |

---

## INTEGRATION TESTS

### I1: Conversational Response Flow

```
GIVEN:  Player asks "Do you have kids?" (conversational action)
WHEN:   Narrator processes action
THEN:   Dialogue chunks streamed via SSE
AND:    No time_elapsed in output
AND:    Mutations (if any) persisted to graph
AND:    No scene refresh triggered
STATUS: ⚠ Partial — needs automated verification
```

### I2: Significant Action Flow

```
GIVEN:  Player says "Let's break camp" (significant action)
WHEN:   Narrator processes action
THEN:   Dialogue chunks streamed
AND:    time_elapsed present in output (e.g., "4 hours")
AND:    World Runner invoked (background)
AND:    Scene may refresh
STATUS: ⚠ Partial — needs e2e test
```

### I3: Invention and Persistence

```
GIVEN:  Player asks about something not in graph
WHEN:   Narrator invents content
THEN:   Invented content appears in dialogue
AND:    Corresponding mutation created
AND:    Mutation applied to graph
AND:    Future queries return invented content
STATUS: ⚠ NOT TESTED — manual verification only
```

### I4: Graph Query Mid-Stream

```
GIVEN:  Narrator streaming dialogue
WHEN:   Graph query needed for facts
THEN:   Query executes without blocking stream
AND:    Facts appear in subsequent chunks
STATUS: ⚠ NOT TESTED
```

### I5: Clickable Creates Graph Links

```
GIVEN:  Narrator outputs inline clickable [word](speaks)
WHEN:   stream_dialogue.py processes it
THEN:   Moment created in graph
AND:    CAN_LEAD_TO link created to target moment
AND:    Clickable activatable in frontend
STATUS: ⚠ Partial — graph-native mode tested
```

---

## BEHAVIORAL TESTS

These test narrator policy compliance:

### B1: Action Classification

| Action | Expected Classification | Status |
|--------|------------------------|--------|
| "Do you have kids?" | Conversational | ⚠ Manual |
| "Tell me about York" | Conversational | ⚠ Manual |
| Click on character word | Conversational | ⚠ Manual |
| "Let's break camp" | Significant | ⚠ Manual |
| "I attack him" | Significant | ⚠ Manual |
| "Wait until dawn" | Significant | ⚠ Manual |

### B2: Voice Consistency

| Character | Expected Style | Test Method | Status |
|-----------|---------------|-------------|--------|
| Aldric | Terse, Saxon rhythms, direct | Human review | ⚠ Manual |
| Edmund | Verbose, justifying, defensive | Human review | ⚠ Manual |
| Player companion | Matches player preference | Human review | ⚠ Manual |

### B3: Clickable Quality

| Test | Criteria | Status |
|------|----------|--------|
| Word appears in text | Exact match | ✓ Automated |
| Word is specific | Name, place, emotional noun | ⚠ Manual |
| 3-6 clickables per block | Count check | ✓ Automated |
| No generic words | "the", "and" not clickable | ⚠ Manual |

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Empty graph query result | Narrator should invent | ⚠ NOT TESTED |
| World injection present | Events woven into narrative | ⚠ NOT TESTED |
| High urgency interruption | Current flow breaks | ⚠ NOT TESTED |
| Player profile empty | Falls back to defaults | ⚠ NOT TESTED |
| Multiple characters present | All hear, some respond | ⚠ NOT TESTED |
| Long conversation (>20 turns) | Context maintained | ⚠ Manual |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| Schema validation | ~90% | Pydantic models comprehensive |
| Streaming tool | ~70% | Core paths tested |
| Graph integration | ~50% | Happy path only |
| Behavioral rules | ~20% | Mostly manual review |
| Voice consistency | ~10% | Human evaluation only |
| Edge cases | ~10% | Minimal coverage |

---

## HOW TO RUN

```bash
# Run narrator integration tests
pytest engine/tests/test_narrator_integration.py -v

# Run with coverage
pytest engine/tests/test_narrator_integration.py --cov=engine/infrastructure/orchestration

# Run schema validation tests
pytest engine/tests/test_models.py -v -k narrator

# Manual test: invoke narrator directly
claude -p "$(cat test_prompts/narrator_test.txt)" --output-format json
```

### Manual Testing Protocol

For behavioral verification:

1. **Start test playthrough**
   ```bash
   cd agents/narrator
   claude -p "Test scene: player at camp with Aldric"
   ```

2. **Test conversational action**
   - Send: "Do you have kids?"
   - Verify: No time_elapsed in output

3. **Test significant action**
   - Send: "Let's break camp"
   - Verify: time_elapsed present

4. **Test invention**
   - Ask about something not in graph
   - Verify: mutation created

5. **Test voice consistency**
   - Review 10 Aldric lines
   - Check: terse, direct, Saxon rhythms

---

## KNOWN TEST GAPS

- [ ] No automated behavioral tests
- [ ] No voice consistency automation
- [ ] No regression tests for prompt changes
- [ ] No performance/latency tests
- [ ] No stress tests for long sessions
- [ ] No tests for world injection handling

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| `test_narrator_integration` | ~20% | LLM non-determinism | Run 3x, pass if 2/3 |
| `test_clickable_parsing` | ~5% | Edge cases in text | Improve parser |

---

## GOLD STANDARD SESSIONS

For regression testing, maintain gold standard sessions:

```
tests/gold_standards/
├── camp_conversation.json     # Expected output for camp scene
├── travel_significant.json    # Expected output for travel
├── invention_flow.json        # Invented character flow
└── callback_test.json         # Setup → payoff verification
```

Compare new narrator versions against gold standards:
- Structure must match
- Behavioral rules must hold
- Voice quality subjectively similar

---

## GAPS / IDEAS / QUESTIONS

- [ ] Implement LLM-judge for automated voice consistency
- [ ] Add latency benchmarks (first chunk < 2s)
- [ ] Property-based tests for mutation validity
- [ ] Snapshot tests for regression detection
- IDEA: Use Claude to evaluate narrator output quality
- IDEA: A/B test framework for prompt variations
- QUESTION: How to test "engaging" narratively?
- QUESTION: How to automate callback verification?

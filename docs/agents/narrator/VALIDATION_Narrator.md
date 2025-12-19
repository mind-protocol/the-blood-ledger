# Narrator — Validation: Behavioral Invariants and Output Verification

```
STATUS: DRAFT
CREATED: 2024-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
PATTERNS:        ./PATTERNS_World_Building.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
ALGORITHM:       ./ALGORITHM_Rolling_Window.md
ALGORITHM:       ./ALGORITHM_Prompt_Structure.md
ALGORITHM:       ./ALGORITHM_Thread.md
THIS:            VALIDATION_Narrator.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            agents/narrator/CLAUDE.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run validation checks.

---

## INVARIANTS

These must ALWAYS be true:

### V1: Action Classification

```
Every player action MUST be classified as either:
  - Conversational (<5 min in-world time)
  - Significant (≥5 min in-world time)

Classification determines:
  - Conversational → no time_elapsed, no world tick, no scene refresh
  - Significant → time_elapsed + world tick + optional scene refresh
```

**Checked by:** Output inspection — presence/absence of `time_elapsed` field

### V2: Immediate Response

```
Narrator MUST begin streaming dialogue before querying the graph.
"Talk first, query second."

The pattern is:
  1. Initial response (dialogue/narration)
  2. Graph query (mid-stream)
  3. Continue with facts
  4. Invent if sparse
  5. Persist mutations
```

**Checked by:** Latency measurement — first chunk within 2s of request

### V3: Invention Persistence

```
FORALL invention ∈ narrator_output:
  invention MUST be persisted as mutation
  mutation MUST link to existing graph nodes

No ephemeral inventions. What's spoken becomes canon.
```

**Checked by:** `test_invention_creates_mutation` — compare dialogue content to mutations list

### V4: Character Voice Consistency

```
FORALL character speaking:
  character.dialogue MUST match character.voice.tone + character.voice.style

Aldric sounds like Aldric (terse, Saxon rhythms).
Edmund sounds like Edmund (justifying, verbose).
```

**Checked by:** Manual review + voice consistency scoring

### V5: Clickable Validity

```
FORALL clickable word in output:
  word MUST appear in text (exact match)
  word MUST be specific (names, places, emotional nouns)
  word MUST have either:
    - Pre-baked response, OR
    - waitingMessage for on-demand generation
```

**Checked by:** `test_clickable_appears_in_text` — verify word presence

### V6: Mutation Schema Compliance

```
FORALL mutation in output.mutations:
  mutation.type ∈ {new_character, new_edge, new_narrative, update_belief, adjust_focus}
  mutation.payload MUST validate against schema in TOOL_REFERENCE.md
```

**Checked by:** Pydantic model validation in engine/models/

---

## PROPERTIES

For property-based testing:

### P1: Time Classification Consistency

```
FORALL action_1, action_2:
    IF action_1.type == action_2.type
    THEN classification(action_1) == classification(action_2)

Same action types should classify the same way.
```

**Tested by:** NOT YET TESTED — would need action type taxonomy

### P2: Mutation Graph Integrity

```
FORALL mutation in output.mutations:
    IF mutation.type == "new_edge":
        from_node EXISTS in graph
        to_node EXISTS in graph OR to_node in same mutation batch
```

**Tested by:** NOT YET TESTED — needs graph state access

### P3: Dialogue Flows Forward

```
FORALL moment sequence M1 → M2 → M3:
    narrative coherence: M2 responds to M1, M3 responds to M2
    No contradictions within sequence
```

**Tested by:** Manual review — subjective quality check

---

## ERROR CONDITIONS

### E1: Empty Dialogue

```
WHEN:    Narrator returns empty dialogue array
THEN:    Retry with different seed OR escalate
SYMPTOM: Player sees nothing, scene stalls
```

**Tested by:** `test_dialogue_not_empty` | Output validation

### E2: Invalid Mutation References

```
WHEN:    Mutation references non-existent graph node
THEN:    Mutation rejected, warning logged
SYMPTOM: Graph becomes inconsistent, callbacks fail
```

**Tested by:** `test_mutation_references_valid` | Graph validation

### E3: Clickable Word Missing

```
WHEN:    Clickable key doesn't appear in text
THEN:    Frontend can't highlight, word is dead
SYMPTOM: Player sees text but can't click expected word
```

**Tested by:** `test_clickable_word_in_text` | String matching

### E4: Classification Drift

```
WHEN:    Similar actions classified differently
THEN:    Inconsistent world pacing
SYMPTOM: Time moves unpredictably, player confusion
```

**Tested by:** Manual review of action/classification pairs

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Action classification | Manual inspection | ⚠ Spot-checked |
| V2: Immediate response | Latency monitoring | ⚠ NOT AUTOMATED |
| V3: Invention persistence | `test_narrator_integration` | ⚠ Partial |
| V4: Voice consistency | Manual review | ⚠ NOT AUTOMATED |
| V5: Clickable validity | Output validation | ⚠ Spot-checked |
| V6: Mutation schema | Pydantic validation | ✓ Covered |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — check time_elapsed presence matches action type
[ ] V2 holds — first response chunk arrives < 2s
[ ] V3 holds — every invention appears in mutations
[ ] V4 holds — characters sound distinct and consistent
[ ] V5 holds — all clickable words appear in their text
[ ] V6 holds — mutations validate against schemas
```

### Automated

```bash
# Run narrator integration tests
pytest engine/tests/test_narrator_integration.py

# Validate mutation schemas
python -c "
from engine.models import *
import json
# Load narrator output and validate
"

# Check clickable validity
python tools/validate_narrator_output.py --check clickables
```

---

## EXPERIENCE VALIDATION

Beyond technical correctness, the narrator must deliver these experiences:

### "Instant Response"

**Test:** Click a word, time how long until text appears
**Pass criteria:** First chunk within 500ms (local), 2s (with graph query)
**How to measure:** Browser devtools timing

### "Characters Sound Right"

**Test:** Read 10 Aldric lines, 10 Edmund lines
**Pass criteria:** Can identify speaker without looking at name
**How to measure:** Blind read test with test users

### "The World Grew"

**Test:** After 1 hour of play, count new graph nodes
**Pass criteria:** At least 3-5 new characters/narratives invented
**How to measure:** Graph diff before/after session

### "Callbacks Work"

**Test:** Reference something from early game later
**Pass criteria:** Narrator remembers and can call back
**How to measure:** Intentional setup → payoff sequence

---

## QUALITY GATES

Before deploying narrator changes:

1. **Output Structure** — All required fields present, schemas valid
2. **Voice Consistency** — Spot check 5 dialogue samples per character
3. **Classification Accuracy** — Test 10 actions of each type
4. **Mutation Validity** — Apply mutations to test graph, no errors
5. **Latency** — First chunk < 2s for 95% of requests

---

## GAPS / IDEAS / QUESTIONS

- [ ] Automated voice consistency scoring (LLM judge?)
- [ ] Property-based tests for mutation graph integrity
- [ ] Regression test suite for classification drift
- IDEA: Record gold standard sessions for comparison
- IDEA: A/B test different narrator prompts
- QUESTION: How to test "engaging" vs just "correct"?
- QUESTION: How to validate seeds → payoff tracking?

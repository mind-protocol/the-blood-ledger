# CLI Tools — Validation: Streaming and Image Invariants

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against current code
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_CLI_Agent_Utilities.md
BEHAVIORS:       ./BEHAVIORS_CLI_Streaming_And_Image_Output.md
ALGORITHM:       ./ALGORITHM_CLI_Tool_Flows.md
THIS:            VALIDATION_CLI_Tool_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
TEST:            ./TEST_CLI_Tool_Coverage.md
SYNC:            ./SYNC_CLI_Tools.md

IMPL:            tools/stream_dialogue.py
                 tools/image_generation/generate_image.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## INVARIANTS

### V1: Stream events append to the playthrough stream file

```
Every CLI invocation that emits an event appends one JSON line to
playthroughs/{playthrough}/stream.jsonl with type + timestamp + data.
```

**Checked by:** Manual inspection of stream.jsonl after running the tool.

### V2: Clickables always create possible targets and CAN_LEAD_TO links

```
For every [word](speaks) in the input text, there is:
- a target moment with status=possible and weight=0.5
- a CAN_LEAD_TO link with weight_transfer=0.4
```

**Checked by:** `engine/tests/test_narrator_integration.py::test_create_moment_with_clickables*`.

### V3: Images saved under frontend public playthrough folder

```
When save=True, images are written under
frontend/public/playthroughs/{playthrough}/images/.
```

**Checked by:** Manual run of generate_image with IDEOGRAM_API_KEY.

---

## PROPERTIES

### P1: Clickable parsing removes markup but preserves words

```
FORALL text with [word](speaks):
    cleaned_text contains word and excludes brackets/parentheses
```

**Tested by:** `engine/tests/test_narrator_integration.py::TestClickableParsing`.

---

## ERROR CONDITIONS

### E1: Missing text for dialogue/narration

```
WHEN:    stream_dialogue runs without text for dialogue/narration
THEN:    exits with code 1 and prints an error
SYMPTOM: stderr contains "text required" message
```

**Tested by:** NOT YET TESTED — no CLI arg error tests.

### E2: Missing IDEOGRAM_API_KEY

```
WHEN:    generate_image runs without API key
THEN:    exits with ValueError and prints an error
SYMPTOM: "IDEOGRAM_API_KEY not found" message
```

**Tested by:** NOT YET TESTED — requires env isolation.

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: stream.jsonl appends | — | ⚠ NOT YET TESTED |
| V2: clickables create moments/links | `test_create_moment_with_clickables*` | ✓ covered |
| V3: image saves to frontend public | — | ⚠ NOT YET TESTED |
| P1: clickable parsing | `TestClickableParsing` | ✓ covered |
| E1: missing text error | — | ⚠ NOT YET TESTED |
| E2: missing API key error | — | ⚠ NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Run: python3 tools/stream_dialogue.py -p default -t dialogue "Hello"
[ ] Confirm stream.jsonl appended in playthroughs/default/
[ ] Confirm created moments in graph (GraphOps query)
[ ] Run: python3 tools/image_generation/generate_image.py --type scene_banner --prompt "Camp" --no-save
[ ] Confirm URL printed without local file
```

### Automated

```bash
pytest engine/tests/test_narrator_integration.py -k "clickable"
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    impl: tools/stream_dialogue.py (working tree)
    impl: tools/image_generation/generate_image.py (working tree)
VERIFIED_BY: manual doc inspection
RESULT:
    V1: NOT RUN
    V2: NOT RUN
    V3: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add a lightweight CLI test for stream_event append behavior.
- [ ] Add a network-mocked test for generate_image response handling.
- QUESTION: Should stream_event include a schema version field?

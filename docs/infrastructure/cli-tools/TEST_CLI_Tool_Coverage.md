# CLI Tools — Tests: Coverage and Gaps

```
STATUS: STABLE
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_CLI_Agent_Utilities.md
BEHAVIORS:       ./BEHAVIORS_CLI_Streaming_And_Image_Output.md
ALGORITHM:       ./ALGORITHM_CLI_Tool_Flows.md
VALIDATION:      ./VALIDATION_CLI_Tool_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
THIS:            TEST_CLI_Tool_Coverage.md (you are here)
SYNC:            ./SYNC_CLI_Tools.md

IMPL:            engine/tests/test_narrator_integration.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

Use narrator integration tests for parsing and moment creation coverage. Validate image generation manually because it requires a real API key and network access.

---

## UNIT TESTS

### Clickable Parsing and Moment Creation

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `TestClickableParsing::test_parse_single_clickable` | text with one clickable | cleaned text + map | existing |
| `TestClickableParsing::test_parse_multiple_clickables` | text with two clickables | cleaned text + map | existing |
| `TestClickableParsing::test_parse_no_clickables` | plain text | empty map | existing |
| `test_create_moment_with_clickables` | mock graph ops | moments + links | existing |

---

## INTEGRATION TESTS

### Narrator Integration Uses CLI Helpers

```
GIVEN:  narrator integration tests in engine/tests/test_narrator_integration.py
WHEN:   create_moment_with_clickables is invoked with mocked graph ops
THEN:   GraphOps.add_moment + add_can_lead_to are called with expected values (ngram repo runtime)
STATUS: existing
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Missing dialogue text | none | not covered |
| Invalid JSON for scene/mutation | none | not covered |
| Missing IDEOGRAM_API_KEY | none | not covered |
| Unknown image type | none | not covered |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| Clickable parsing | partial | covered in narrator integration tests |
| Graph moment creation | partial | covered with mocks |
| Stream file append | none | needs CLI-level test |
| Image generation | none | manual only |

---

## HOW TO RUN

```bash
pytest engine/tests/test_narrator_integration.py -k "clickable"
```

---

## KNOWN TEST GAPS

- [ ] No automated test for stream.jsonl append behavior.
- [ ] No mocked test for Ideogram API request/response handling.
- [ ] No CLI arg validation tests for missing text or invalid JSON.

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| None known | n/a | n/a | n/a |

---

## GAPS

- [ ] Add a unit test for stream_event JSONL output.
- [ ] Add a network-mocked test for generate_image response handling.

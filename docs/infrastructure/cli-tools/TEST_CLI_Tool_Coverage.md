# CLI Tools — Tests: Coverage and Gaps

```
STATUS: TODO
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_CLI_Agent_Utilities.md
BEHAVIORS:       ./BEHAVIORS_CLI_Streaming_And_Image_Output.md
ALGORITHM:       ./ALGORITHM_CLI_Tool_Flows.md
VALIDATION:      ./VALIDATION_CLI_Tool_Invariants.md
THIS:            TEST_CLI_Tool_Coverage.md (you are here)
SYNC:            ./SYNC_CLI_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
```

---

## CURRENT COVERAGE

No automated tests are present for the CLI tools in this module.

---

## PLANNED SUITES

| Test | Target | Description |
|------|--------|-------------|
| `tests/tools/test_stream_dialogue.py` | CLI graph + stream | Validate clickables, moment creation, stream file writes |
| `tests/tools/test_generate_image.py` | CLI wrapper | Validate request payload and output file path |

---

## MANUAL CHECKS

- `python3 tools/stream_dialogue.py -p default -t narration "A test line"`
- `python3 tools/image_generation/generate_image.py --list-types`

---

## GAPS

- No hermetic tests for graph side effects or stream file output.
- No CLI error-path tests (invalid JSON, missing API key).

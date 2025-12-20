# CLI Tools — Health: Stream and Mutation Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the CLI tools that stream dialogue and apply graph
mutations. It exists to detect failures where CLI output or graph writes do
not reach the frontend. It does not verify narrative correctness.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_CLI_Agent_Utilities.md
BEHAVIORS:       ./BEHAVIORS_CLI_Streaming_And_Image_Output.md
ALGORITHM:       ./ALGORITHM_CLI_Tool_Flows.md
VALIDATION:      ./VALIDATION_CLI_Tool_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
THIS:            HEALTH_CLI_Tools.md
SYNC:            ./SYNC_CLI_Tools.md

IMPL:            tools/stream_dialogue.py
IMPL:            tools/image_generation/generate_image.py
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: cli_stream_output
    flow_id: stream_dialogue
    priority: high
    rationale: CLI streams must reach the frontend SSE channel.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: cli_stream_output
```

---

## HOW TO RUN

```bash
# Manual: run stream_dialogue with a short line and confirm SSE output
python3 tools/stream_dialogue.py --text "Health check" --playthrough default
```

---

## KNOWN GAPS

- [ ] No automated health checker for CLI streaming output.

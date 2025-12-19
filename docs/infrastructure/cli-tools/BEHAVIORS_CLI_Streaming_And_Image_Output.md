# CLI Tools — Behaviors: Streaming Dialogue and Image Output

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against current code
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_CLI_Agent_Utilities.md
THIS:            BEHAVIORS_CLI_Streaming_And_Image_Output.md (you are here)
ALGORITHM:       ./ALGORITHM_CLI_Tool_Flows.md
VALIDATION:      ./VALIDATION_CLI_Tool_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
TEST:            ./TEST_CLI_Tool_Coverage.md
SYNC:            ./SYNC_CLI_Tools.md

IMPL:            tools/stream_dialogue.py
                 tools/image_generation/generate_image.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Stream dialogue/narration to graph and stream file

```
GIVEN:  a playthrough id and dialogue/narration text
WHEN:   stream_dialogue is invoked with -t dialogue or -t narration
THEN:   a moment is created in the graph with status=active and weight=1.0
AND:    a stream.jsonl event is appended with cleaned text (no clickable markup)
```

### B2: Create clickable targets for inline clickables

```
GIVEN:  text containing [word](player speaks) syntax
WHEN:   stream_dialogue parses and creates clickables
THEN:   each word produces a target moment with status=possible and weight=0.5
AND:    a CAN_LEAD_TO link is created with weight_transfer=0.4
```

### B3: Persist scene/mutation payloads and stream event

```
GIVEN:  scene or mutation JSON from --file or inline text
WHEN:   stream_dialogue is invoked with -t scene or -t mutation
THEN:   the payload is written to playthroughs/{id}/scene.json (scene only)
AND:    a stream.jsonl event is appended with the payload
```

### B4: Generate and optionally save images

```
GIVEN:  an image prompt, type, and optional playthrough/name
WHEN:   generate_image is invoked
THEN:   the Ideogram API returns an image URL and metadata
AND:    the image is saved to frontend/public/playthroughs/{id}/images/ unless --no-save
```

---

## INPUTS / OUTPUTS

### Primary Function: `create_moment_with_clickables()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| playthrough | str | Playthrough ID to choose graph + stream path |
| text | str | Dialogue or narration with optional clickables |
| moment_type | str | "dialogue" or "narration" |
| speaker | str | Character id for dialogue |
| tone | str | Optional tone string |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| moment_id | str | ID for the created main moment |
| clickables | dict | Map of word -> metadata including target_moment_id |

**Side Effects:**

- Writes moments and CAN_LEAD_TO links to the graph
- Prints graph creation feedback to stdout

### Primary Function: `generate_image()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| prompt | str | Ideogram prompt text |
| image_type | str | Key in IMAGE_TYPES config |
| playthrough | str | Playthrough folder name |
| name | str | Optional output filename |
| seed | int | Optional deterministic seed |
| rendering_speed | str | FLASH/TURBO/DEFAULT/QUALITY |
| save | bool | Whether to download the image |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| result | dict | URL, seed, resolution, prompt_used, and local_path if saved |

**Side Effects:**

- Calls the Ideogram API and downloads the resulting image
- Writes PNG files to the frontend public folder when save=True

---

## EDGE CASES

### E1: Missing text for dialogue or narration

```
GIVEN:  no text argument is provided
THEN:   the tool prints an error and exits with code 1
```

### E2: Invalid JSON for scene/mutation

```
GIVEN:  malformed JSON in --file or inline text
THEN:   the tool prints an error and exits with code 1
```

### E3: Missing API key

```
GIVEN:  IDEOGRAM_API_KEY is missing
THEN:   generate_image raises a ValueError and exits with code 1
```

### E4: Unknown image type

```
GIVEN:  an image type not in IMAGE_TYPES
THEN:   generate_image raises a ValueError and exits with code 1
```

---

## ANTI-BEHAVIORS

### A1: Clickable markup leaks into stream payload

```
GIVEN:   text with [word](speaks) markup
WHEN:    stream_event payload is built
MUST NOT: include the raw brackets/parentheses
INSTEAD:  send cleaned text and a clickable map
```

### A2: Image downloads when --no-save is set

```
GIVEN:   generate_image --no-save
WHEN:    the API response returns a URL
MUST NOT: download or write the image to disk
INSTEAD:  return URL and metadata only
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should stream_dialogue validate speaker IDs before graph writes?
- [ ] Should generate_image retry on transient HTTP failures?
- IDEA: Add a dry-run mode for stream_dialogue that skips graph writes.
- QUESTION: Should stream_dialogue enforce a maximum event size?

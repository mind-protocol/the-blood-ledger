# CLI Tools — Algorithm: Stream Events and Image Requests

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
THIS:            ALGORITHM_CLI_Tool_Flows.md (you are here)
VALIDATION:      ./VALIDATION_CLI_Tool_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
TEST:            ./TEST_CLI_Tool_Coverage.md
SYNC:            ./SYNC_CLI_Tools.md

IMPL:            tools/stream_dialogue.py
IMPL:            tools/image_generation/generate_image.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Two CLI tools sit between agents and infrastructure:

- `stream_dialogue.py` turns narration/dialogue into graph moments and appends an SSE stream event.
- `generate_image.py` wraps the Ideogram 3.0 API and writes images to the frontend's public folder.

Both tools follow a request → enrich → persist → emit pattern to keep agent calls simple.

---

## DATA STRUCTURES

### Stream Event

```
{
  "type": "dialogue" | "narration" | "scene" | "mutation" | "time" | "complete" | "error",
  "timestamp": "ISO-8601",
  "data": {
    "text": "cleaned text",
    "moment_id": "...",
    "clickable": {"word": {"speaks": "...", "target_moment_id": "..."}},
    "tone": "optional"
  }
}
```

### Clickable Map

```
{
  "Word": {
    "speaks": "Player prompt",
    "intent": "ask",
    "waitingMessage": "...",
    "target_moment_id": "{moment_id}_click_word"
  }
}
```

### Image Request Payload

```
{
  "prompt": "...",
  "aspect_ratio": "3x1",
  "style_type": "REALISTIC",
  "rendering_speed": "DEFAULT",
  "magic_prompt": "AUTO",
  "negative_prompt": "people, persons, ..."
}
```

---

## ALGORITHM: Stream Dialogue/Narration

### Step 1: Resolve graph context

- Read playthroughs/{id}/player.yaml to map to graph_name.
- Query world tick and player location for tick/place defaults.

### Step 2: Parse inline clickables

- Use regex to transform `[word](speaks)` into clean text.
- Build a clickable map keyed by word.

### Step 3: Create moments and links

- Create the main moment with status=active, weight=1.0.
- For each clickable:
  - Create a target moment with status=possible, weight=0.5.
  - Add a CAN_LEAD_TO link with weight_transfer=0.4.

### Step 4: Emit stream event

- Build a stream event with clean text, moment_id, and clickable metadata.
- Append JSON to playthroughs/{id}/stream.jsonl.

---

## ALGORITHM: Stream Scene/Mutation/Time

### Step 1: Load payload

- Resolve JSON either from --file or inline text.
- For scenes, persist to playthroughs/{id}/scene.json.

### Step 2: Emit stream event

- Append the payload to stream.jsonl with the proper type.

---

## ALGORITHM: Generate Image

### Step 1: Validate inputs

- Ensure IDEOGRAM_API_KEY is set.
- Validate image_type against IMAGE_TYPES.

### Step 2: Build request

- Combine prompt + type config (aspect_ratio/style).
- Include negative_prompt and optional seed.

### Step 3: Call Ideogram API

- POST multipart/form-data to the Ideogram endpoint.
- Parse response data and extract URL + metadata.

### Step 4: Save image (optional)

- If save=True, download URL and write to:
  `frontend/public/playthroughs/{id}/images/{name or type_timestamp}.png`

---

## KEY DECISIONS

### D1: Graph-native moments for dialogue/narration

```
IF event is dialogue/narration:
    create moments + links in graph
    emit stream event with cleaned text
ELSE:
    stream payload only
```

### D2: Save images by default

```
IF --no-save:
    return URL only
ELSE:
    download image and write to frontend public folder
```

---

## DATA FLOW

```
CLI args
    ↓
stream_dialogue.py
    ↓
GraphOps + stream.jsonl
    ↓
Frontend SSE + graph storage
```

```
CLI args
    ↓
generate_image.py
    ↓
Ideogram API → image URL
    ↓
frontend/public/playthroughs/{id}/images
```

---

## HELPER FUNCTIONS

### `parse_inline_clickables()`

**Purpose:** Extract clickable words and return cleaned text.

### `stream_event()`

**Purpose:** Append structured events to the playthrough stream file.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| engine.physics.graph.graph_ops | `GraphOps.add_moment`, `add_can_lead_to` | Moment + link creation |
| engine.physics.graph.graph_queries | `get_player_location`, `_query` | Tick/place context |
| Ideogram API | `POST /v1/ideogram-v3/generate` | Image URL + metadata |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should the stream event format include a schema version?
- IDEA: Add a retry policy for Ideogram 5xx errors.
- QUESTION: Should clickables allow nested punctuation normalization?

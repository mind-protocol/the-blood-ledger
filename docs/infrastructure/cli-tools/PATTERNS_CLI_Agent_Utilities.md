# CLI Agent Utilities — Patterns: Agent-Invocable Command Line Tools

```
STATUS: STABLE
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against current code
```

---

## CHAIN

```
THIS:            PATTERNS_CLI_Agent_Utilities.md (you are here)
SYNC:            ./SYNC_CLI_Tools.md
IMAGE_PROMPTING: ../image-generation/PATTERNS_Image_Generation.md

IMPL:            tools/stream_dialogue.py
                 tools/image_generation/generate_image.py
```

---

## THE PROBLEM

AI agents (narrator, world-runner) need to communicate with the game system in standardized ways:

1. **Stream content to frontend** — Dialogue, narration, and mutations must flow from agents to players in real-time
2. **Generate visual assets** — Scene banners, character portraits, and object icons must be generated on demand
3. **Persist to graph** — Content must be stored in the moments graph for history and replay

Without standardized CLI tools, agents would need to:
- Construct raw API calls or graph operations inline
- Manage file paths and formats inconsistently
- Duplicate boilerplate across agent implementations

---

## THE PATTERN

**CLI tools as the agent interface layer.**

Each tool is a standalone Python script that:
1. Accepts structured arguments (playthrough ID, content type, text)
2. Handles all internal complexity (graph ops, file writes, API calls)
3. Prints status feedback for agent visibility
4. Returns structured output when needed

Agents invoke these tools via shell commands, treating them as black-box utilities.

---

## PRINCIPLES

### Principle 1: Graph-Native by Default

All content flows through the moments graph. When stream_dialogue creates narration, it:
- Creates a moment node in the graph (with tick, place, weight)
- Creates CAN_LEAD_TO edges for clickable words
- Writes to stream.jsonl for SSE delivery

The graph is the source of truth; the stream file is a delivery mechanism.

### Principle 2: Inline Clickable Syntax

Clickables use markdown-like syntax for simplicity:

```
"My niece [Edda](Who's Edda?) is an archer."
```

This parses to:
- Clean text: "My niece Edda is an archer."
- Clickable map: {"Edda": {"speaks": "Who's Edda?"}}

The target moment is created as "possible" with weight 0.5. Player click adds 0.4 weight, flipping it to "active" (0.9 > 0.8 threshold).

### Principle 3: Separation of Stage and Scene

Image generation creates **locations only** — no characters, no objects. The UI composites characters and objects over the location banner. This ensures:
- Visual consistency with game state
- No AI hallucinations (unwanted props)
- Proper layering of narrative elements

---

## THE TOOLS

### stream_dialogue.py

Streams dialogue and narration to the frontend via the moments graph.

**Types:**
- `dialogue` — Character speech with speaker ID
- `narration` — Environmental description (no speaker)
- `mutation` — World state changes
- `scene` — Full scene JSON
- `time` — Time elapsed signal
- `complete` — Stream end signal
- `error` — Error reporting

**Usage:**
```bash
# Dialogue with clickable
python3 tools/stream_dialogue.py -p default -t dialogue -s char_aldric \
    "My niece [Edda](Who's Edda?) is an archer."

# Narration with tone
python3 tools/stream_dialogue.py -p default -t narration --tone tense \
    "He prods the embers with a stick."

# Complete the stream
python3 tools/stream_dialogue.py -p default -t complete
```

### generate_image.py

Generates images via Ideogram 3.0 API.

**Image Types:**
- `scene_banner` — 3:1 atmospheric location (no people)
- `setting_strip` — 1:3 vertical strip
- `character_portrait` — 1:1 character face
- `character_portrait_tall` — 3:4 full portrait
- `object_icon` — 1:1 item icon
- `map_region` — 4:3 regional map
- `full_map` — 1:1 world map

**Usage:**
```bash
python3 tools/image_generation/generate_image.py \
    --type scene_banner \
    --prompt "A forest clearing at night, bare oak trees, frost on grass" \
    --playthrough default \
    --name camp_night
```

See `../image-generation/PATTERNS_Image_Generation.md` for full prompting guide.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `engine/db/graph_ops.py` | Creating moments and edges in graph |
| `engine/db/graph_queries.py` | Querying player location, world tick |
| `playthroughs/{id}/stream.jsonl` | SSE event delivery |
| Ideogram API | External image generation |

---

## WHAT THIS DOES NOT SOLVE

- **Real-time streaming** — These are CLI tools, not persistent services. They write to files that the API tails.
- **Agent orchestration** — The tools don't coordinate between narrator and world-runner. That's handled by `engine/orchestration/`.
- **Content validation** — The tools accept what agents give them. Validation happens upstream.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should stream_dialogue validate speaker IDs against the graph?
- [ ] Could we add a --dry-run flag to preview without graph writes?
- IDEA: Auto-generate image prompts from place metadata
- QUESTION: How should we handle streaming errors gracefully?

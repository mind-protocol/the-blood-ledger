# CLI Tools — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_CLI_Agent_Utilities.md
BEHAVIORS:      ./BEHAVIORS_CLI_Streaming_And_Image_Output.md
ALGORITHM:      ./ALGORITHM_CLI_Tool_Flows.md
VALIDATION:     ./VALIDATION_CLI_Tool_Invariants.md
THIS:           IMPLEMENTATION_CLI_Tools_Architecture.md (you are here)
TEST:           ./TEST_CLI_Tool_Coverage.md
SYNC:           ./SYNC_CLI_Tools.md

IMPL:           tools/stream_dialogue.py
                tools/image_generation/generate_image.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
tools/stream_dialogue.py                # CLI stream events + graph moments
tools/image_generation/generate_image.py # Ideogram API client + file save
tools/image_generation/README.md         # Usage and flags
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `tools/stream_dialogue.py` | Stream dialogue, narration, scene, mutation events + graph moments | `create_moment_with_clickables`, `parse_inline_clickables`, `stream_event`, `main` | ~400 | WATCH |
| `tools/image_generation/generate_image.py` | Generate images via Ideogram API and save assets | `generate_image`, `main` | ~288 | OK |
| `tools/image_generation/README.md` | Usage and CLI options | - | ~79 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Layered CLI utilities (CLI -> adapter -> side effects)

**Why this pattern:** Each script isolates the CLI boundary from core systems (graph operations, file writes, or HTTP calls). This keeps agent tooling thin and allows engine modules and external APIs to evolve without rewriting agent prompts.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Adapter | `tools/stream_dialogue.py` | Adapts CLI input into GraphOps + stream file writes |
| Data-driven config | `tools/image_generation/generate_image.py:IMAGE_TYPES` | Encodes image presets without branching logic |
| Command-style entry point | `main()` in each script | Parses CLI args and triggers workflow |

### Anti-Patterns to Avoid

- **God Script:** Avoid adding unrelated workflows to `tools/stream_dialogue.py` or `tools/image_generation/generate_image.py`. Create a new CLI script instead.
- **Hidden Side Effects:** Keep file paths and graph writes explicit; avoid implicit globals beyond PROJECT_ROOT.
- **Premature Abstraction:** Extract helpers only when there are multiple call sites.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| CLI tools | CLI parsing, graph writes, stream file I/O, HTTP calls | Orchestrators and agents | `python3 tools/...` command interface |
| Graph layer | `engine/physics/graph/` queries/ops | CLI scripts | `GraphOps`, `GraphQueries` |
| Image API | Ideogram API calls | CLI scripts | HTTP requests via `requests` |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `tools/stream_dialogue.py` | Agent or orchestrator CLI call |
| `main()` | `tools/image_generation/generate_image.py` | Agent or tool invocation |

---

## DATA FLOW

### Dialogue/Narration Stream Flow

```
┌────────────────────┐
│ Agent CLI call      │
└────────┬───────────┘
         │ args
         ▼
┌────────────────────┐
│ tools/stream_dialogue.py │ ← parse clickables + resolve tick/place
└────────┬───────────┘
         │ graph writes
         ▼
┌────────────────────┐
│ GraphOps / Queries │
└────────┬───────────┘
         │ stream event
         ▼
┌────────────────────┐
│ stream.jsonl file   │
└────────────────────┘
```

### Image Generation Flow

```
┌────────────────────┐
│ Agent CLI call      │
└────────┬───────────┘
         │ args
         ▼
┌────────────────────┐
│ tools/image_generation/generate_image.py │ ← build payload + call API
└────────┬───────────┘
         │ image bytes
         ▼
┌────────────────────┐
│ playthrough assets  │
└────────────────────┘
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
tools/stream_dialogue.py
    └── imports → GraphOps (`engine/physics/graph/graph_ops.py`)
    └── imports → GraphQueries (`engine/physics/graph/graph_queries.py`)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `requests` | HTTP calls to Ideogram | `tools/image_generation/generate_image.py` |
| `dotenv` | Load `.env` API key | `tools/image_generation/generate_image.py` |
| `yaml` | Playthrough graph lookup | `tools/stream_dialogue.py` |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `IDEOGRAM_API_KEY` | `.env` | - | API key for Ideogram image generation |
| `IMAGE_TYPES` | `tools/image_generation/generate_image.py` | presets | Aspect ratio + style per type |

---

## BIDIRECTIONAL LINKS

### Code -> Docs

| File | Line | Reference |
|------|------|-----------|
| `tools/stream_dialogue.py` | 2 | `docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md` |
| `tools/image_generation/generate_image.py` | 4 | `docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| Algorithm A1 | `tools/stream_dialogue.py:create_moment_with_clickables` |
| Algorithm A2 | `tools/stream_dialogue.py:main` |
| Algorithm A3 | `tools/image_generation/generate_image.py:generate_image` |
| Behavior B1 | `tools/stream_dialogue.py:create_moment_with_clickables` |
| Behavior B3 | `tools/image_generation/generate_image.py:generate_image` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `tools/stream_dialogue.py` | ~400L | <400L | clickables helper module (planned) | `parse_inline_clickables`, clickable parsing helpers |

### Ideas

- IDEA: Add retry policy around image API calls with exponential backoff.
- IDEA: Add structured logging for stream events and graph writes.

### Questions

- QUESTION: Should stream_dialogue expose a JSON-only mode for integration tests?

# CLI Tools — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: CANONICAL
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_CLI_Agent_Utilities.md
BEHAVIORS:       ./BEHAVIORS_CLI_Streaming_And_Image_Output.md
ALGORITHM:       ./ALGORITHM_CLI_Tool_Flows.md
VALIDATION:      ./VALIDATION_CLI_Tool_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Tools_Architecture.md
TEST:            ./TEST_CLI_Tool_Coverage.md
THIS:            SYNC_CLI_Tools.md (you are here)
```

---

## MATURITY

**What's canonical (v1):**
- `stream_dialogue.py` — Graph-native moment creation with SSE delivery
- `generate_image.py` — Ideogram 3.0 integration with type presets
- Inline clickable syntax `[word](speaks text)`
- Image types: scene_banner, character_portrait, etc.

**What's still being designed:**
- Auto-prompt generation from place metadata
- Portrait pipeline with moderation rules

**What's proposed (v2+):**
- Regional vegetation mapping
- Dry-run mode for testing

---

## CURRENT STATE

Both CLI tools are functional and actively used by agents:

**stream_dialogue.py**: Creates moments in the graph with proper tick, place, and weight values. Supports dialogue (with speaker), narration (no speaker), mutations, and time signals. Clickable words create "possible" target moments that flip to "active" when players click.

**generate_image.py**: Generates images via Ideogram 3.0 API. Saves to `frontend/public/playthroughs/{playthrough}/images/`. Supports various aspect ratios and style types.

---

## RECENT CHANGES

### 2025-12-19: Repair implementation doc link paths

- **What:** Replaced bare filename/module tokens with concrete paths and removed the nonexistent extraction target filename
- **Why:** Broken-link repair flagged non-existent file references in the implementation doc
- **Files:**
  - `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md`

### 2025-12-19: Verified tools documentation mapping

- **What:** Confirmed `tools/` files map to existing cli-tools and image-generation docs
- **Why:** Repair task flagged tools as undocumented; mapping already exists
- **Files:**
  - `modules.yaml`
  - `tools/stream_dialogue.py`
  - `tools/image_generation/generate_image.py`
  - `tools/image_generation/README.md`

### 2025-12-19: Sync DOCS reference line numbers

- **What:** Updated the line number reference for the image-generation DOCS comment
- **Why:** DOCS comments were reordered in `tools/image_generation/generate_image.py`
- **Files:**
  - `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md`

### 2025-12-19: Complete documentation chain

- **What:** Added BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, and TEST docs
- **Why:** Repair incomplete chain for cli-tools module
- **Files:**
  - `docs/infrastructure/cli-tools/BEHAVIORS_CLI_Streaming_And_Image_Output.md`
  - `docs/infrastructure/cli-tools/ALGORITHM_CLI_Tool_Flows.md`
  - `docs/infrastructure/cli-tools/VALIDATION_CLI_Tool_Invariants.md`
  - `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md`
  - `docs/infrastructure/cli-tools/TEST_CLI_Tool_Coverage.md`

### 2025-12-19: Documentation created

- **What:** Created PATTERNS and SYNC docs for cli-tools module
- **Why:** Module was flagged as undocumented by ngram doctor
- **Files:**
  - `docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md`
  - `docs/infrastructure/cli-tools/SYNC_CLI_Tools.md`
  - `modules.yaml` (fixed path from `engine/tools/**` to `tools/**`)

---

## KNOWN ISSUES

None currently active.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Extend or VIEW_Implement

**Where things are:**
- Stream dialogue tool: `tools/stream_dialogue.py`
- Image generation tool: `tools/image_generation/generate_image.py`
- Image prompting guide: `docs/infrastructure/image-generation/PATTERNS_Image_Generation.md`

**Watch out for:**
- Image generation requires `IDEOGRAM_API_KEY` in `.env`
- Clickable syntax must use exact format: `[word](speaks text)`
- Graph name derived from `playthroughs/{id}/player.yaml`

---

## HANDOFF: FOR HUMAN

**Executive summary:**
CLI tools for agents are documented and functional. stream_dialogue.py handles all narration/dialogue output with graph persistence. generate_image.py handles visual asset generation.

**Decisions made:**
- Renamed module from `tools` to `cli-tools` for clarity
- Fixed code path from empty `engine/tools/**` to actual `tools/**`
- Image prompting guide lives separately in `docs/infrastructure/image-generation/`

---

## POINTERS

| What | Where |
|------|-------|
| Stream dialogue script | `tools/stream_dialogue.py` |
| Image generation script | `tools/image_generation/generate_image.py` |
| Image generation README | `tools/image_generation/README.md` |
| Image prompting guide | `docs/infrastructure/image-generation/PATTERNS_Image_Generation.md` |
| Image generation SYNC | `docs/infrastructure/image-generation/SYNC_Image_Generation.md` |
| Module manifest | `modules.yaml` (cli-tools entry) |

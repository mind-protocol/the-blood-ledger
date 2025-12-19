# Image Generation — Implementation: Code Architecture and Structure

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Image_Generation.md
BEHAVIORS:      ./BEHAVIORS_Image_Generation.md
ALGORITHM:      ./ALGORITHM_Image_Generation.md
VALIDATION:     ./VALIDATION_Image_Generation.md
THIS:           IMPLEMENTATION_Image_Generation.md
TEST:           ./TEST_Image_Generation.md
SYNC:           ./SYNC_Image_Generation.md

IMPL:           tools/image_generation/generate_image.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
tools/
└── image_generation/
    ├── generate_image.py     # CLI + API wrapper for Ideogram image generation
    └── README.md             # Usage and configuration notes
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `tools/image_generation/generate_image.py` | Build API request, download result, and save image files | `generate_image`, `main`, `IMAGE_TYPES` | ~287 | OK |
| `tools/image_generation/README.md` | Document CLI usage, options, and output paths | - | ~78 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline (sequential CLI flow)

**Why this pattern:** The tool is a linear sequence: validate inputs → assemble request → call API → download → persist file. A pipeline keeps steps explicit and easy to trace.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Table-driven configuration | `tools/image_generation/generate_image.py:IMAGE_TYPES` | Centralizes per-type aspect ratio and style metadata |
| CLI command pattern | `tools/image_generation/generate_image.py:main` | Exposes a predictable command-line interface |

### Anti-Patterns to Avoid

- **Prompt rules in code**: Prompt structure belongs in docs, not hardcoded strings → keep the tool generic.
- **God script**: Don't add prompt generation, graph updates, and UI tasks into this file → keep it focused on API + file IO.
- **Hardcoded paths**: Keep output paths derived from `PROJECT_ROOT` and CLI args, not inline constants.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Image generation CLI | Ideogram request, download, save | Prompt authoring, UI display | CLI args, `generate_image()` |
| Storage layout | Writes under `frontend/public/playthroughs/...` | Frontend cache handling | Filesystem path |

---

## SCHEMA

### ImageRequest

```yaml
ImageRequest:
  required:
    - prompt: string          # full prompt string
    - image_type: string      # key from IMAGE_TYPES
  optional:
    - playthrough: string     # folder name (default "default")
    - name: string            # filename without extension
    - seed: integer           # reproducible seed
    - rendering_speed: string # FLASH | TURBO | DEFAULT | QUALITY
    - magic_prompt: string    # AUTO | ON | OFF
```

### ImageResult

```yaml
ImageResult:
  required:
    - url: string
    - image_type: string
  optional:
    - seed: integer
    - resolution: string
    - prompt_used: string
    - style_type: string
    - local_path: string
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `tools/image_generation/generate_image.py:193` | CLI execution (`python generate_image.py ...`) |
| `generate_image()` | `tools/image_generation/generate_image.py:72` | Programmatic use by other tooling |

---

## DATA FLOW

### CLI Flow: Prompt → API → File

```
┌──────────────────┐
│ CLI arguments    │
└────────┬─────────┘
         │ prompt + type
         ▼
┌──────────────────────────┐
│ generate_image()         │ ← validate + build request
│ generate_image.py        │
└────────┬─────────────────┘
         │ multipart request
         ▼
┌──────────────────┐
│ Ideogram API     │
└────────┬─────────┘
         │ image URL
         ▼
┌──────────────────────────┐
│ download + save PNG      │
│ frontend/public/...      │
└──────────────────────────┘
```

---

## LOGIC CHAINS

### LC1: CLI Image Generation

**Purpose:** Generate and persist a single image via the CLI.

```
CLI args
  → generate_image.main()        # parse args and call generator
    → generate_image()           # validate + request + download
      → requests.post()          # Ideogram API
        → requests.get()         # download image
          → write PNG to disk
```

**Data transformation:**
- Input: `prompt` string + `image_type` string
- After request: JSON response with URL + metadata
- Output: local PNG + `ImageResult` dict

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
tools/image_generation/generate_image.py
    └── none (standalone utility)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `requests` | API and image download | `tools/image_generation/generate_image.py` |
| `python-dotenv` | Loading `.env` | `tools/image_generation/generate_image.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| API configuration | `generate_image.py:API_URL` | module | process lifetime |
| Type config | `generate_image.py:IMAGE_TYPES` | module | process lifetime |
| API key | `generate_image.py:API_KEY` | module | process lifetime |

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Load `.env` from project root
2. Parse CLI args
3. Validate API key and image type
```

### Request Cycle

```
1. Build multipart request
2. Submit to Ideogram API
3. Download image and save locally
```

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `IDEOGRAM_API_KEY` | `.env` | none | API token for Ideogram |
| `--type` | CLI arg | `scene_banner` | Image type from `IMAGE_TYPES` |
| `--playthrough` | CLI arg | `default` | Output playthrough folder |
| `--name` | CLI arg | none | Output filename without extension |
| `--seed` | CLI arg | none | Reproducible seed |
| `--speed` | CLI arg | `DEFAULT` | Rendering speed |
| `--no-save` | CLI arg | false | Skip saving PNG locally |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `tools/image_generation/generate_image.py` | 3 | `# DOCS: docs/infrastructure/image-generation/IMPLEMENTATION_Image_Generation.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM step 1 | `tools/image_generation/generate_image.py:72` |
| ALGORITHM step 2 | `tools/image_generation/generate_image.py:131` |
| ALGORITHM step 3 | `tools/image_generation/generate_image.py:162` |
| BEHAVIOR B2 | `tools/image_generation/generate_image.py:164` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

None (all files <400 lines).

### Missing Implementation

- [ ] GraphOps integration for `image_path` persistence (tracked in SYNC).

### Ideas

- IDEA: Add a dry-run mode that prints the final request payload without hitting the API.

### Questions

- QUESTION: Should retries and backoff live here or in a higher-level orchestration tool?

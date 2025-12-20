# Chronicle System — Mechanisms: Generation Pipeline

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Chronicle System.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
BEHAVIORS:       ./BEHAVIORS_Chronicle_Types.md
THIS:            MECHANISMS_Chronicle_Pipeline.md (you are here)
VERIFICATION:    ./VALIDATION_Chronicle_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Chronicle_System.md
TEST:            ./TEST_Chronicle_System.md
SYNC:            ./SYNC_Chronicle_System.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Chronicle System.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Chronicles are generated from a session buffer via LLM scripting, TTS voice tracks, and FFmpeg composition. The pipeline yields an MP4, thumbnail, and metadata for distribution.

---

## DATA STRUCTURES

### ChronicleBuffer

```
entries: list[event]
ledger_changes: list
snapshots: list
shadow_events: list
```

---

## MECHANISM: Generate Chronicle

### Step 1: Select key moments

LLM selects peaks and produces a structured script.

### Step 2: Generate audio tracks

TTS produces narrator and character lines.

### Step 3: Compose timeline

Images, text, and audio are assembled into a timeline.

### Step 4: Render video

FFmpeg renders MP4 and thumbnails.

### Step 5: Upload and share

Optional upload to YouTube with metadata.

---

## KEY DECISIONS

### D1: Script structure by chronicle type

```
IF type == session:
    short format
ELSE IF type == weekly:
    arc format
ELSE:
    life format
```

### D2: Director mode override

```
IF player selects director mode:
    apply player-selected moments/tone
```

---

## DATA FLOW

```
Chronicle buffer
    ↓
LLM script
    ↓
TTS audio
    ↓
FFmpeg render
    ↓
MP4 + metadata
```

---

## COMPLEXITY

**Time:** O(n) per script + render.

**Space:** O(n) for audio/video assets.

**Bottlenecks:**
- TTS latency
- FFmpeg render time

---

## HELPER FUNCTIONS

### `select_key_moments()`

**Purpose:** Choose 3–5 peak moments.

**Logic:** Sort events by narrative weight and emotional tags.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/product/gtm-strategy | upload_destination | Channel destinations |
| docs/product/ledger-lock | chronicle_preview | Conversion preview snippet |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define asset storage strategy
- [ ] Define fallback when TTS fails
- IDEA: Add per-character voice overrides

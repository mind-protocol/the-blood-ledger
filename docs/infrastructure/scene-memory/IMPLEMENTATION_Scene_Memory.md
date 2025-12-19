# Scene Memory System — Implementation: Moment Processing Architecture

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Scene_Memory.md
BEHAVIORS:      ./BEHAVIORS_Scene_Memory.md
ALGORITHM:      ./ALGORITHM_Scene_Memory.md
VALIDATION:     ./VALIDATION_Scene_Memory.md
THIS:           IMPLEMENTATION_Scene_Memory.md
TEST:           ./TEST_Scene_Memory.md
SYNC:           ./SYNC_Scene_Memory.md

IMPL:           engine/infrastructure/memory/moment_processor.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/
└── infrastructure/
    └── memory/
        ├── __init__.py          # Exports MomentProcessor for external use
        └── moment_processor.py  # Moment creation + transcript management
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/memory/__init__.py` | Module export surface | `MomentProcessor` | ~9 | OK |
| `engine/infrastructure/memory/moment_processor.py` | Create moments, manage transcript, connect to GraphOps | `MomentProcessor`, `get_moment_processor` | ~583 | WATCH |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline service

**Why this pattern:** The module transforms narrator/player inputs into persisted graph moments plus transcript entries in a linear flow: build entry, append transcript, embed text, persist to graph.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Strategy | `engine/infrastructure/memory/moment_processor.py:30` | Inject `embed_fn` to swap embedding providers |
| Facade | `engine/infrastructure/memory/moment_processor.py:19` | Provide a single interface over GraphOps + transcript IO |
| Factory | `engine/infrastructure/memory/moment_processor.py:561` | Create a configured processor with defaults |

### Anti-Patterns to Avoid

- **God Object**: `MomentProcessor` is already large; extract transcript IO and ID helpers if it grows.
- **Hidden Side Effects**: Keep transcript writes explicit and logged; avoid implicit state changes.
- **Tight Coupling**: Depend on GraphOps interface, not its internals.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Moment processing | Moment IDs, transcript writes, graph calls | GraphOps implementation details | `MomentProcessor` methods |
| Embedding | Embedding invocation | Embedding model config | `embed_fn` injection |
| Playthrough storage | Transcript path and writes | Playthrough lifecycle | `playthrough_id`, `playthroughs_dir` |

---

## SCHEMA

### Transcript Entry

```yaml
TranscriptEntry:
  required:
    - type: string            # dialogue | narration | hint | player_* variants
    - text: string            # content displayed to player
    - tick: int               # world tick
    - place: string           # place_id
    - moment_id: string       # graph moment id
    - timestamp: string       # UTC ISO timestamp
  optional:
    - speaker: string         # character id for dialogue/player actions
    - tone: string            # emotional tone
    - status: string          # possible | active | spoken
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `MomentProcessor` | `engine/infrastructure/memory/moment_processor.py:17` | Orchestration setup for a playthrough |
| `set_context` | `engine/infrastructure/memory/moment_processor.py:108` | Scene start / location change |
| `process_dialogue` | `engine/infrastructure/memory/moment_processor.py:126` | Narrator dialogue line |
| `process_narration` | `engine/infrastructure/memory/moment_processor.py:191` | Narrator narration line |
| `process_player_action` | `engine/infrastructure/memory/moment_processor.py:252` | Player click/freeform/choice |
| `process_hint` | `engine/infrastructure/memory/moment_processor.py:319` | Hint or whispered line |
| `create_possible_moment` | `engine/infrastructure/memory/moment_processor.py:380` | Pre-seed possible moments |
| `link_moments` | `engine/infrastructure/memory/moment_processor.py:450` | Connect moments for traversal |
| `link_narrative_to_moments` | `engine/infrastructure/memory/moment_processor.py:483` | Attribute narratives to moments |
| `get_moment_processor` | `engine/infrastructure/memory/moment_processor.py:559` | Convenience factory |

---

## DATA FLOW

### Spoken Moment Creation

```
Narrator/Player text
        │
        ▼
MomentProcessor.process_*()     # build entry + IDs
        │
        ├─ _append_to_transcript()  # persist transcript.json + line number
        ├─ embed_fn()               # only if text > 20 chars
        ▼
GraphOps.add_moment()            # persist Moment node + links
```

### Possible Moment Seeding

```
Seed text + speaker
        │
        ▼
MomentProcessor.create_possible_moment()
        │
        ├─ GraphOps.add_moment(status="possible")
        ├─ GraphOps.add_can_speak()
        └─ GraphOps.add_attached_to()
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/memory/moment_processor.py
    └── imports → engine.physics.graph.graph_ops.GraphOps
    └── imports → engine.infrastructure.embeddings.service.get_embedding_service
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `json` | Transcript persistence | `engine/infrastructure/memory/moment_processor.py` |
| `logging` | Processor diagnostics | `engine/infrastructure/memory/moment_processor.py` |
| `pathlib` | Playthrough paths | `engine/infrastructure/memory/moment_processor.py` |
| `datetime` | Transcript timestamps | `engine/infrastructure/memory/moment_processor.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| current tick | `engine/infrastructure/memory/moment_processor.py:59` | instance | set via `set_context` |
| current place | `engine/infrastructure/memory/moment_processor.py:60` | instance | set via `set_context` |
| last moment id | `engine/infrastructure/memory/moment_processor.py:61` | instance | updated per processed moment |
| transcript line count | `engine/infrastructure/memory/moment_processor.py:64` | instance | loaded/updated per write |
| transcript path | `engine/infrastructure/memory/moment_processor.py:56` | instance | derived at init |

---

## RUNTIME BEHAVIOR

### Initialization

1. Create `MomentProcessor` with GraphOps + embed function.
2. Resolve playthrough directory and transcript path.
3. Load transcript line count or initialize empty transcript.

### Main Loop / Request Cycle

1. `set_context(tick, place_id)` at scene start.
2. Call `process_*` for each narration/dialogue/player action.
3. Optionally seed possible moments and link them.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `playthroughs_dir` | `engine/infrastructure/memory/moment_processor.py:30` | `engine/playthroughs` | Transcript storage root |
| `graph_name` | `engine/infrastructure/memory/moment_processor.py:561` | `blood_ledger` | Target graph database |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/memory/moment_processor.py` | 1 | `DOCS: docs/infrastructure/scene-memory/` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| Spoken moment creation | `engine/infrastructure/memory/moment_processor.py:126` |
| Player action processing | `engine/infrastructure/memory/moment_processor.py:252` |
| Possible moment seeding | `engine/infrastructure/memory/moment_processor.py:380` |
| Transcript persistence | `engine/infrastructure/memory/moment_processor.py:66` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `engine/infrastructure/memory/moment_processor.py` | ~583L | <400L | transcript store module (proposed) | `_load_transcript_line_count`, `_write_transcript`, `_append_to_transcript` |
| `engine/infrastructure/memory/moment_processor.py` | ~583L | <400L | moment id helper module (proposed) | `_generate_id`, `_tick_to_time_of_day` |

### Missing Implementation

- [ ] None observed in this module.

### Questions

- QUESTION: Should transcript IO move behind a storage interface to support streaming or append-only logs?

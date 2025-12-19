# Narrator — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2024-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
PATTERNS:        ./PATTERNS_World_Building.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
THIS:            IMPLEMENTATION_Narrator.md (you are here)
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            agents/narrator/CLAUDE.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

The Narrator is an AI agent, not traditional code. Its "implementation" is a CLAUDE.md instruction file that configures Claude's behavior when invoked via CLI.

```
agents/
└── narrator/
    ├── CLAUDE.md                 # Agent instructions (878 lines)
    └── .claude/                  # Claude CLI state directory

tools/
└── stream_dialogue.py            # Streaming tool for narrator output

engine/
├── infrastructure/
│   └── orchestration/
│       ├── narrator.py           # Python service that invokes Claude CLI
│       └── narrator_prompt.py    # Prompt builder for scene context
│
└── physics/
    └── graph/
        ├── graph_ops.py          # Write operations (mutations)
        └── graph_queries.py      # Read operations (queries)
```

### File Responsibilities

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `agents/narrator/CLAUDE.md` | AI agent instructions and behavior rules | ~878 | OK |
| `tools/stream_dialogue.py` | Stream dialogue chunks via SSE | ~200 | OK |
| `engine/infrastructure/orchestration/narrator.py` | Claude CLI wrapper service | ~150 | OK |
| `engine/infrastructure/orchestration/narrator_prompt.py` | Prompt builder | ~100 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size
- **WATCH** (400-700 lines): Getting large
- **SPLIT** (>700 lines): Too large

> CLAUDE.md at 878 lines is large but acceptable — it's a comprehensive agent instruction file, not traditional code. The structure is well-organized with clear sections.

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** AI Agent with Tool Use

**Why this pattern:** The narrator needs:
- Persistent context (--continue flag for memory)
- Graph access (for world state)
- Streaming output (for real-time UX)
- Flexible behavior (LLM-driven decisions)

Traditional code can't provide the creative generation needed. An LLM agent with tool access can query, generate, and persist in a coherent loop.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Tool Use | `stream_dialogue.py`, `graph_ops.py` | Narrator interacts with world via tool calls |
| SSE Streaming | `narrator.py` → frontend | Real-time dialogue display |
| Prompt Engineering | `narrator_prompt.py` | Structured context for consistent behavior |
| Persistent Session | `--continue` flag | Narrator remembers entire playthrough |

### Anti-Patterns to Avoid

- **Stateless calls**: Don't call narrator without `--continue` — loses context
- **Direct JSON return**: Use tool calls for streaming, not monolithic JSON
- **Hardcoded responses**: Narrator should query and invent, not recite scripts
- **God prompt**: Keep CLAUDE.md organized with clear sections, not one giant blob

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Agent Instructions | CLAUDE.md | Orchestrator, tools | Claude CLI invocation |
| Graph Access | graph_ops, graph_queries | CLAUDE.md | Python tool calls |
| Output Streaming | stream_dialogue.py | Frontend | SSE events |

---

## ENTRY POINTS

| Entry Point | File | Triggered By |
|-------------|------|--------------|
| Narrator invocation | `narrator.py:call_narrator()` | Orchestrator on player action |
| Streaming dialogue | `tools/stream_dialogue.py` | Narrator tool call |
| Graph query | `graph_queries.py:search()` | Narrator tool call |
| Mutation apply | `graph_ops.py:apply()` | Narrator tool call |

---

## DATA FLOW

### Player Action → Narrator Response

```
┌─────────────────────┐
│  Player Action      │ (click word / type message)
└──────────┬──────────┘
           │ action_text, scene_context
           ▼
┌─────────────────────┐
│  Orchestrator       │ ← engine/infrastructure/orchestration/orchestrator.py
│  - builds prompt    │
│  - invokes Claude   │
└──────────┬──────────┘
           │ prompt + context
           ▼
┌─────────────────────┐
│  Claude CLI         │ ← claude --continue -p "..."
│  (Narrator Agent)   │
│  reads: CLAUDE.md   │
└──────────┬──────────┘
           │ tool calls
           ├─────────────────┐
           ▼                 ▼
┌─────────────────┐   ┌─────────────────┐
│ stream_dialogue │   │ graph_queries   │
│ (SSE output)    │   │ (read context)  │
└─────────────────┘   └─────────────────┘
           │                 │
           ▼                 ▼
┌─────────────────┐   ┌─────────────────┐
│ Frontend        │   │ graph_ops       │
│ (display)       │   │ (mutations)     │
└─────────────────┘   └─────────────────┘
```

### Tool Call Flow

```
┌─────────────────────┐
│  Narrator decides   │
│  to stream dialogue │
└──────────┬──────────┘
           │ Bash tool call
           ▼
┌─────────────────────────────────────────────────────┐
│  python3 tools/stream_dialogue.py                   │
│    -p {playthrough_id}                              │
│    -t dialogue                                      │
│    -s char_aldric                                   │
│    "But my niece — [Edda](Who's Edda?) — ..."      │
└──────────┬──────────────────────────────────────────┘
           │
           ├── Creates moment in graph (graph-native mode)
           ├── Parses inline clickables [word](speaks)
           ├── Streams via SSE to frontend
           └── Returns success
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
agents/narrator/CLAUDE.md
    └── uses → tools/stream_dialogue.py (Bash)
    └── uses → engine/physics/graph/graph_queries.py (Python)
    └── uses → engine/physics/graph/graph_ops.py (Python)

engine/infrastructure/orchestration/narrator.py
    └── imports → subprocess (Claude CLI)
    └── imports → narrator_prompt.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `claude` (CLI) | Agent execution | orchestration/narrator.py |
| `falkordb` | Graph database | graph_ops.py, graph_queries.py |
| `pydantic` | Schema validation | engine/models/ |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Agent memory | Claude `--continue` session | Playthrough | Persistent via CLI state |
| Graph state | FalkorDB | Global | Persistent |
| Current scene | Query result | Request | Ephemeral |
| Player profile | `playthroughs/{id}/PROFILE_NOTES.md` | Playthrough | File-based |

### State Transitions

The narrator doesn't have internal state transitions — it maintains context through:
1. **Claude `--continue`** — preserves conversation history
2. **Graph queries** — retrieves current world state
3. **File reads** — loads player profile, world injections

Orchestrator scene context uses graph world tick when available to derive
`time_of_day`/`day`, and reads `playthroughs/{id}/current_action.json` to
populate the recent action field.

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Orchestrator starts
2. On first player action:
   a. Build scene context (narrator_prompt.py)
   b. Invoke Claude CLI (first call, no --continue)
   c. Claude loads CLAUDE.md as system instructions
   d. Session established
3. System ready for subsequent calls with --continue
```

### Request Cycle

```
1. Player action arrives
2. Orchestrator builds prompt with context
3. Claude invoked with --continue
4. Narrator:
   a. Classifies action (conversational vs significant)
   b. Streams immediate response (dialogue tool)
   c. Queries graph (if needed)
   d. Invents (if graph sparse)
   e. Persists mutations (if invented)
   f. Signals completion
5. Frontend receives SSE stream
6. Graph updated with mutations
```

### Session Continuity

```
The --continue flag means:
- Full conversation history preserved
- Narrator remembers what it authored
- Callbacks possible ("remember when...")
- Character voices learned over time
```

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| Agent instructions | `agents/narrator/CLAUDE.md` | N/A | Full narrator behavior spec |
| Streaming tool | `tools/stream_dialogue.py` | graph-native | Output mode |
| Playthrough data | `playthroughs/{id}/` | N/A | Per-game state |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Reference |
|------|-----------|
| `agents/narrator/CLAUDE.md` | References TOOL_REFERENCE.md, INPUT_REFERENCE.md |
| `engine/infrastructure/orchestration/narrator.py` | Docstring references narrator docs |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM_Scene_Generation: Two modes | `CLAUDE.md:§2 The Two Paths` |
| BEHAVIORS: DialogueChunk | `tools/stream_dialogue.py` |
| BEHAVIORS: GraphMutation | `CLAUDE.md:§1 Invention Is Creation` |
| PATTERNS: Pre-baked trees | `CLAUDE.md:§3 What You Produce` |
| VALIDATION: V1 Classification | `CLAUDE.md:§2` decision logic |

---

## GAPS / IDEAS / QUESTIONS

### Current Gaps

- [ ] No automated tests for narrator output quality
- [ ] Voice consistency checking not implemented
- [ ] No regression tests for behavior changes

### Ideas

- IDEA: Add narrator output validator service
- IDEA: Implement LLM-judge for voice consistency
- IDEA: Create gold standard test sessions

### Questions

- QUESTION: How to test narrator behavior changes without full integration?
- QUESTION: Should CLAUDE.md be split into smaller files?

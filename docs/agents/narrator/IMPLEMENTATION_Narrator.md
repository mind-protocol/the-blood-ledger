# Narrator — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2024-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
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

The narrator is an AI agent configured by `agents/narrator/CLAUDE.md`, invoked by the orchestrator.

```
agents/narrator/CLAUDE.md                 # Agent instructions
agents/narrator/CLAUDE_old.md             # Archived legacy prompt
agents/narrator/.claude/                  # CLI state directory
engine/infrastructure/orchestration/agent_cli.py   # CLI wrapper
engine/infrastructure/orchestration/narrator.py    # Caller + prompt builder
engine/physics/graph/graph_ops.py         # Mutation apply
engine/physics/graph/graph_queries.py     # Graph read
tools/stream_dialogue.py                  # SSE streaming
```

### File Responsibilities

| File | Purpose | Status |
|------|---------|--------|
| `agents/narrator/CLAUDE.md` | Agent instructions and behavior rules | OK |
| `agents/narrator/CLAUDE_old.md` | Legacy prompt (unused) | Legacy |
| `engine/infrastructure/orchestration/agent_cli.py` | Agent CLI wrapper | OK |
| `engine/infrastructure/orchestration/narrator.py` | Narrator caller + prompt builder | OK |
| `engine/physics/graph/graph_ops.py` | Graph mutation apply | OK |
| `engine/physics/graph/graph_queries.py` | Graph read | OK |
| `tools/stream_dialogue.py` | Stream dialogue chunks | OK |

---

## ENTRY POINTS

| Entry Point | File | Triggered By |
|-------------|------|--------------|
| Narrator invocation | `engine/infrastructure/orchestration/narrator.py` | Orchestrator on player action |
| Streaming dialogue | `tools/stream_dialogue.py` | Narrator tool call |
| Graph query | `engine/physics/graph/graph_queries.py` | Narrator tool call |
| Mutation apply | `engine/physics/graph/graph_ops.py` | Narrator tool call |

---

## DATA FLOW (Condensed)

1. Orchestrator builds prompt with scene context + world injection.
2. `agent_cli.py` invokes the agent with `--continue` for thread memory.
3. Narrator streams dialogue chunks via `tools/stream_dialogue.py`.
4. Narrator queries the graph mid-stream for facts.
5. Mutations are applied via `graph_ops.py`.
6. Frontend receives SSE stream and any scene updates.

---

## CONFIGURATION

| Config | Location | Default |
|--------|----------|---------|
| Agent instructions | `agents/narrator/CLAUDE.md` | N/A |
| Agent provider | `AGENTS_MODEL` env | `claude` |
| Streaming tool | `tools/stream_dialogue.py` | graph-native |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Reference |
|------|-----------|
| `agents/narrator/CLAUDE.md` | References `TOOL_REFERENCE.md`, `INPUT_REFERENCE.md` |
| `engine/infrastructure/orchestration/narrator.py` | Docstring references narrator docs |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM: two modes | `agents/narrator/CLAUDE.md` ("The Two Paths") |
| BEHAVIORS: DialogueChunk | `tools/stream_dialogue.py` |
| BEHAVIORS: GraphMutation | `agents/narrator/CLAUDE.md` ("Invention Is Creation") |
| PATTERNS: pre-baked trees | `agents/narrator/CLAUDE.md` ("What You Produce") |
| VALIDATION: V1 classification | `agents/narrator/CLAUDE.md` |

---

## GAPS / IDEAS / QUESTIONS

- [ ] No automated tests for narrator output quality
- [ ] Voice consistency checking not implemented
- [ ] No regression tests for behavior changes

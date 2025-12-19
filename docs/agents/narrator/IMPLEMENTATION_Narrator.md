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

This is the high-level path for a narrator call, focusing on the concrete
runtime touchpoints and the order they occur in the current service.

1. Orchestrator builds prompt with scene context + world injection.
2. `agent_cli.py` invokes the agent with `--continue` for thread memory.
3. Narrator streams dialogue chunks via `tools/stream_dialogue.py`.
4. Narrator queries the graph mid-stream for facts.
5. Mutations are applied via `graph_ops.py`.
6. Frontend receives SSE stream and any scene updates.

---

## SCHEMA

The narrator returns a JSON object that matches the NarratorOutput contract,
anchored by the SceneTree schema. The concrete shape lives in
`docs/agents/narrator/INPUT_REFERENCE.md` and
`docs/agents/narrator/TOOL_REFERENCE.md`, with scene, time_elapsed, mutations,
and seeds forming the stable output envelope.

---

## LOGIC CHAINS

Request flow chains through the orchestrator: a player action triggers the
call in `engine/infrastructure/orchestration/narrator.py`, the prompt is built
from scene_context/world_injection, the CLI returns JSON, and the response is
parsed and streamed while optional graph queries and mutations happen in-band.

---

## CONCURRENCY MODEL

Narrator calls are synchronous within a single service instance: `run_agent`
blocks until the CLI returns, and `session_started` tracks the conversation
thread for that instance. Parallel playthroughs should use separate service
instances or request contexts to avoid shared session state.

---

## CONFIGURATION

Configuration is intentionally minimal; the narrator is driven by the prompt
builder and agent CLI defaults, with only a few environment hooks exposed.

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

- [ ] No automated tests for narrator output quality or schema drift detection
- [ ] Voice consistency checking not implemented across scenes and sessions
- [ ] No regression tests for behavior changes across playthrough resets

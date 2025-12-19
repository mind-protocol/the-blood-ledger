# Narrator — Algorithm: Scene Generation

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical (condensed)
DEPENDS_ON: graph.json, character backstories
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
THIS:            ALGORITHM_Scene_Generation.md (you are here)
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            agents/narrator/CLAUDE.md
```

---

## Purpose

Define the minimal, reliable generation flow: how the narrator classifies actions, streams dialogue, queries the graph, invents when needed, and emits the correct output shape.

---

## High-Level Flow

1. Gather scene context and any world injection.
2. Build prompt from context + instructions.
3. Call agent with persistent thread (`--continue`).
4. Stream dialogue immediately.
5. Query graph mid-stream for facts.
6. Invent if the graph is sparse and persist as mutations.
7. Return output in the required schema.

---

## Inputs and Outputs

- Input structure: `INPUT_REFERENCE.md`
- Output schema: `TOOL_REFERENCE.md`

---

## Two Modes

### Conversational (<5 minutes)

- Stream dialogue chunks.
- Return `scene: {}` and omit `time_elapsed`.
- No world tick.

### Significant (>=5 minutes)

- Stream transition dialogue.
- Return full `SceneTree` and include `time_elapsed`.
- Triggers world tick and possible world injection next call.

---

## Core Steps (Algorithm)

```text
classify_action(action)
stream_dialogue_first()
query_graph_if_needed()
invent_missing_facts()
persist_mutations()
if significant:
  build_scene_tree()
  include time_elapsed
else:
  scene = {}
return NarratorOutput
```

---

## Rolling Window (Summary)

The narrator pre-generates one layer of clickable responses and generates the next layer in the background as the player clicks. For full details, see `HANDOFF_Rolling_Window_Architecture.md`.

---

## Thread Continuity (Summary)

Use a single persistent thread per playthrough. The narrator remembers prior output via `--continue`; summarize early history only if the thread becomes too long.

---

## Quality Checks (Minimum)

- Immediate first chunk (stream-first rule).
- Every invention is paired with a mutation.
- Clickables appear in text.
- Mode classification matches time_elapsed rules.

---

*"Talk first. Query as you speak. Invent when the graph is silent."*

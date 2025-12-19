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

## Overview

This algorithm coordinates scene narration with graph-backed truth, keeping a persistent thread while deciding when to synthesize new facts. It emphasizes stream-first delivery, explicit mode classification, and pairing any invented details with mutations so canon stays consistent.

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

Inputs include the current playthrough context, graph snapshots, and action metadata defined in `INPUT_REFERENCE.md`. Output must conform to the narrator tool schema in `TOOL_REFERENCE.md`, including mode-specific fields like `scene` and optional `time_elapsed`.

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

## Data Structures

- `NarratorOutput`: response envelope containing streamed dialogue and optional `scene` tree payload.
- `SceneTree`: structured scene graph used when significant actions warrant a full refresh.
- `ActionClassification`: derived mode label (conversational vs significant) used to branch behavior.
- `MutationBatch`: list of mutations that persist invented facts back into the graph.

---

## Core Steps (Algorithm)

The core steps intentionally keep narration responsive first, then reconcile with graph truth before returning the structured payload.

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

## Algorithm: generate_scene_output

1. Normalize inputs (action, context, graph slice, prior thread state).
2. Classify action into conversational or significant mode.
3. Emit first dialogue chunk immediately to satisfy stream-first latency.
4. Query graph for facts or resolve clickables as needed.
5. Invent only when graph lacks required facts; collect mutations.
6. Persist mutations to canon storage before final response.
7. If significant, build `SceneTree` and include `time_elapsed`.
8. Return `NarratorOutput` with dialogue stream metadata and payload.

---

## Rolling Window (Summary)

The narrator pre-generates one layer of clickable responses and generates the next layer in the background as the player clicks. For full details, see `HANDOFF_Rolling_Window_Architecture.md`.

---

## Thread Continuity (Summary)

Use a single persistent thread per playthrough. The narrator remembers prior output via `--continue`; summarize early history only if the thread becomes too long.

---

## Key Decisions

- Keep a single persistent thread per playthrough to preserve continuity.
- Stream first, then query or invent, to protect responsiveness.
- Only include `time_elapsed` and full `SceneTree` for significant actions.
- Require every invention to have corresponding mutations in canon.

---

## Data Flow

Action input enters classification, prompt assembly, and immediate streaming. Graph queries or click resolution feed into invention checks, which yield a mutation batch persisted to storage. The final structured response merges dialogue, optional `SceneTree`, and timing metadata.

---

## Complexity

Classification and prompt assembly are O(1) relative to input size. Graph queries and mutation persistence dominate time, scaling with the number of retrieved facts and mutations, while streaming work scales with emitted dialogue chunks.

---

## Helper Functions

- `classify_action`: determines conversational vs significant mode.
- `stream_dialogue_first`: emits initial narration chunk without blocking.
- `query_graph_if_needed`: fetches canonical facts for clickables or context.
- `invent_missing_facts`: synthesizes details when the graph is sparse.
- `persist_mutations`: writes new facts back to canon storage.
- `build_scene_tree`: constructs the structured scene payload for significant actions.

---

## Interactions

- Graph layer for canonical facts and mutation persistence.
- Orchestration layer for thread state and prompt assembly.
- Frontend stream consumer for immediate dialogue chunks.
- World tick pipeline triggered after significant actions.

---

## Quality Checks (Minimum)

- Immediate first chunk (stream-first rule).
- Every invention is paired with a mutation.
- Clickables appear in text.
- Mode classification matches time_elapsed rules.

---

## Gaps / Ideas / Questions

- How aggressively should rolling-window depth adapt to player latency?
- What metadata helps audit invented facts versus retrieved facts?
- Should significant-action thresholds vary by scenario pacing?

---

*"Talk first. Query as you speak. Invent when the graph is silent."*

# Narrator — Behaviors: What the Narrator Produces

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## Two Response Modes

| Mode | Threshold | Output |
|------|-----------|--------|
| Conversational | <5 minutes | Dialogue chunks + mutations + `scene: {}` |
| Significant | >=5 minutes | Dialogue chunks + mutations + full SceneTree + time_elapsed |

---

## Dialogue Chunks

- Streamed in real-time as the narrator generates.
- Chunks with `speaker` are dialogue; chunks without `speaker` are narration.
- First chunk must arrive quickly (stream-first rule).

Schema: `TOOL_REFERENCE.md`.

---

## Graph Mutations

- Every invention must be persisted as a mutation.
- Mutations must link to existing graph nodes (or nodes in the same batch).
- Mutation schemas are defined in `engine/models/` (see `TOOL_REFERENCE.md`).

---

## SceneTree (Significant Actions)

- Full scene tree is returned only for significant actions.
- Clickables must either include a pre-baked response or a waitingMessage.
- New clickables may appear in responses to extend the scene.

Schema: `TOOL_REFERENCE.md`.

---

## time_elapsed Rules

- Only include `time_elapsed` for significant actions.
- Conversational actions omit it entirely.

---

## World Injection Handling

When world injection is present (see `INPUT_REFERENCE.md`):
- `witnessed` breaks are woven directly into narration.
- `heard` breaks arrive as news from characters or messengers.
- `will_hear` breaks are noted but not surfaced yet.
- `interruption` with high urgency overrides the current flow.

---

## Quality Indicators

- Voice consistency: characters sound distinct and stable.
- Response time: first chunk within 1-2 seconds.
- Connection density: new content links to existing graph state.
- Setup/payoff: seeds are tracked and paid off later.

---

*"The narrator doesn't just produce text. It produces a world that grows through conversation."*

# Async Architecture - Algorithm

**Purpose:** Entry point for the async architecture algorithms.

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Async_Architecture.md
BEHAVIORS:      ./BEHAVIORS_Travel_Experience.md
VALIDATION:     ./VALIDATION_Async_Architecture.md
IMPLEMENTATION: ./IMPLEMENTATION_Async_Architecture.md
TEST:           ./TEST_Async_Architecture.md
THIS:           ALGORITHM_Async_Architecture.md (entry point)
SYNC:           ./SYNC_Async_Architecture.md
```

---

## Index

See `docs/infrastructure/async/ALGORITHM/ALGORITHM_Overview.md` for the overview and links to all algorithm parts.

---

## OVERVIEW

This entry point summarizes the end-to-end async travel flow and anchors the
shared terms used by the detailed algorithm parts (runner, hooks, SSE,
waypoints, images, discussion trees). Use it as the canonical map for how the
pieces coordinate at runtime.

---

## DATA STRUCTURES

- **Injection queue (JSONL):** `playthroughs/<id>/injection_queue.jsonl` lines
  with `{timestamp, source, payload}` for hook interruptions.
- **SSE event payloads:** `{type, playthrough_id, data}` for map, image, and
  moment updates emitted by graph writes.
- **Runner TaskOutput payload:** JSON summary with `playthrough_id`, waypoint
  list, and completion metadata returned at task completion.
- **Waypoint record:** `{place_id, position, sequence_index}` written as the
  runner traverses travel segments.
- **Discussion tree JSON:** per-character JSON with topic nodes and branch
  depth, pruned as branches are consumed.

---

## ALGORITHM: Coordinate_Async_Travel

Primary function name: `Coordinate_Async_Travel`

1. Narrator starts streaming travel narration immediately for the player.
2. Narrator spawns the Runner as a background task to generate waypoints,
   tick energy, and write new places into the graph.
3. Graph writes emit SSE events; the frontend listens and updates map state,
   fog, and images as events arrive.
4. Hook interruptions are appended to the injection queue when player UI or
   character activation occurs; narrator consumes these in-band.
5. When the Runner finishes, Narrator reads TaskOutput and stitches the final
   completion data into the travel narrative wrap-up.

---

## KEY DECISIONS

- Hook interruptions are separate from Runner completion; TaskOutput handles
  completion to avoid misusing the hook channel.
- Graph is the coordination point for real-time updates, reducing synchronous
  orchestration and enabling SSE fan-out.
- Discussion trees are ephemeral JSON artifacts; they are regenerated instead
  of archived to keep travel dialogue fresh.

---

## DATA FLOW

Runner → Graph writes → SSE stream → Frontend map/render updates.
Frontend UI or graph activation → Injection queue → Hook → Narrator interrupt.
Runner completion → TaskOutput → Narrator wrap-up narration and state update.

---

## COMPLEXITY

Runtime scales with waypoints and emitted events. For `W` waypoints and `E`
events, the runner work is `O(W + E)` and the frontend applies events in
`O(E)`; queue writes are `O(1)` per interruption.

---

## HELPER FUNCTIONS

- `emit_graph_sse_event(event)` — serialize and send SSE payloads per write.
- `append_injection_event(playthrough_id, payload)` — JSONL append for hook use.
- `read_task_output(task_id)` — collect runner completion metadata.
- `build_waypoint(place, index)` — normalize waypoint fields for storage.

---

## INTERACTIONS

- **Narrator ↔ Runner:** Narrator spawns Runner and later reads TaskOutput.
- **Runner ↔ Graph:** Runner writes places, tensions, and waypoint markers.
- **Graph ↔ Frontend:** Graph emits SSE events that drive map and UI updates.
- **Frontend ↔ Hook:** UI actions append to the injection queue for narration.

---

## GAPS / IDEAS / QUESTIONS

- SSE reconnection strategy is still open; needs a replay buffer decision.
- Injection queue format split (JSONL vs JSON) should be reconciled.
- Image generation throttling is undefined when many places are created fast.

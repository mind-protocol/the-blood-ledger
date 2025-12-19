# Async Architecture - Algorithm: Runner Protocol

**Purpose:** Runner background execution and TaskOutput completion handling.

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Async_Architecture.md
BEHAVIORS:      ../BEHAVIORS_Travel_Experience.md
VALIDATION:     ../VALIDATION_Async_Architecture.md
IMPLEMENTATION: ../IMPLEMENTATION_Async_Architecture.md
OVERVIEW:       ALGORITHM_Overview.md
THIS:           ALGORITHM_Runner_Protocol.md (you are here)
SYNC:           ../SYNC_Async_Architecture.md
```

---

## Runner Protocol

**Purpose:** How Narrator spawns Runner as a background task, and how to read its output.

### Invocation

Narrator spawns Runner using `bash` with `run_in_background=true`:

```python
bash(
    command='''
        timeout 600 && \
        cd agents/runner && \
        claude -p "TravelTask: origin=place_camp, destination=place_york, \
                   travellers=[char_rolf, char_aldric], time_span=3days" \
        --dangerously-skip-permissions \
        --allowedTools "Write,Read,graph_query,graph_write" \
        --add-dir ../../
    ''',
    run_in_background=true
)
```

**After invocation:**
- Narrator continues streaming immediately (doesn't wait).
- Runner works in background, writing to graph as it goes.
- Frontend sees place creation via SSE.

**Multiple Runners:** Can run simultaneously (e.g., player traveling while characters move elsewhere).

### Reading Output

When Runner completes, system sends a reminder:

```
<system-reminder>
Background bash ba7e4e6 has new output: 162 lines...
</system-reminder>
```

Narrator reads via `TaskOutput`:

```python
result = TaskOutput(task_id="ba7e4e6")
```

### During Processing

While Runner works, it writes directly to graph:

**Waypoint Creation**
```
Runner computes route segment ->
  Creates place node in graph ->
    Graph triggers image generation ->
    Graph SSE broadcasts place_created ->
      Frontend updates map
```

**Energy Ticking**
```
Runner processes segment ->
  Ticks energy values ->
    Writes to graph (internal state, frontend doesn't need)
```

**Break Resolution**
```
Tension flips ->
  Runner resolves break ->
    Creates narrative in graph ->
    Updates character positions ->
      If character in player's group -> writes to injection_queue
      Runner STOPS and waits for injection to be handled
```

**Key:** Runner stops when it creates an injection. It doesn't continue in parallel. The injection response determines what happens next.

**Note:** Injections can also be triggered by non-Narrator activated nodes (e.g., world events, other characters acting independently).

**Visibility Updates**
```
Player "passes through" waypoint ->
  Updates player_knows_place ->
    Graph SSE broadcasts visibility_update ->
      Frontend reveals fog
```

### Completion Payload

Runner outputs JSON to stdout with `type`, `destination`, `time_elapsed`, `waypoints_created`, and a `destination_state` summary.

**Payload Types**

| Type | Meaning | Narrator Action |
|------|---------|-----------------|
| `travel_complete` | Journey finished normally | Generate arrival scene |
| `encounter` | Something happened mid-journey | Generate encounter scene, then continue or re-spawn |
| `arrival_change` | Destination state changed during travel | Incorporate change into arrival |

### Narrator Handling

```python
result = TaskOutput(task_id)

if result["type"] == "travel_complete":
    generate_arrival_scene(result["destination_state"])

elif result["type"] == "encounter":
    generate_encounter_scene(result)
    # May need to re-spawn Runner for remaining journey

elif result["type"] == "arrival_change":
    generate_modified_arrival(result)
```

### Key Clarifications

**Runner completion uses TaskOutput, NOT hook.**

Hook is for interruptions:
- Character speaks
- Player UI action

TaskOutput is for expected completions:
- Runner finished processing
- Background task done

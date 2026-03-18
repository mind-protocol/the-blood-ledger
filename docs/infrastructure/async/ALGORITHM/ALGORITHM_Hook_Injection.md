# Async Architecture - Algorithm: Hook Injection

**Purpose:** How the world interrupts the Narrator mid-stream.

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Async_Architecture.md
BEHAVIORS:      ../BEHAVIORS_Travel_Experience.md
VALIDATION:     ../VALIDATION_Async_Architecture.md
IMPLEMENTATION: ../IMPLEMENTATION_Async_Architecture.md
OVERVIEW:       ALGORITHM_Overview.md
THIS:           ALGORITHM_Hook_Injection.md (you are here)
SYNC:           ../SYNC_Async_Architecture.md
```

---

## Principle

Hook injection is for **INTERRUPTIONS ONLY**.

NOT for:
- Runner completion (use TaskOutput)
- Normal state updates (use SSE)

Hook fires when:
- A character in the player's group is activated via narrative
- Player uses UI (stop button, location click, portrait click)

---

## OVERVIEW

Hook injection uses a file-backed JSONL queue to feed interrupt events into the Narrator via PostToolUse. Writers append to the queue, the hook consumes the oldest entry, and the Narrator receives the payload as additional context.

---

## DATA STRUCTURES

- Injection entry: `{type, character?, trigger?, prompt?, current_position?}` as a single JSON object per line.
- Queue file: `playthroughs/default/injection_queue.jsonl` containing FIFO entries.
- Hook payload: `additionalContext` JSON string passed back to the Narrator.

---

## ALGORITHM: Process_Hook_Injection

Primary function name: `Process_Hook_Injection`

1. Check for the injection queue file at the configured path.
2. If the file exists, read all lines into memory.
3. If at least one line exists, parse the first JSON object.
4. Rewrite the queue file without the consumed line.
5. Emit the parsed object as hook `additionalContext`.
6. If no lines exist, return an empty hook decision.

---

## KEY DECISIONS

- Use JSONL for simple FIFO semantics without a DB dependency.
- Limit hook scope to interruptions only; completion and state updates use other channels.
- Keep the hook reader stateless to avoid long-lived processes in the hook lifecycle.

---

## DATA FLOW

Writer -> JSONL append -> hook reader -> additionalContext -> Narrator handling -> UI update.

---

## COMPLEXITY

Queue operations are `O(n)` for file rewrite per hook invocation; the queue is intentionally small so this stays acceptable.

---

## HELPER FUNCTIONS

- `append_jsonl(path, payload)` — append a JSON object per line.
- `read_first_line(path)` — return oldest entry for hook processing.
- `rewrite_without_first(path)` — persist remaining entries in the queue.

---

## INTERACTIONS

- Frontend or Runner writes to the queue via `/api/inject` or internal calls.
- Hook script consumes queue entries and emits payloads to the Narrator.
- Narrator interprets payload types and adjusts the narrative stream.

---

## GAPS / IDEAS / QUESTIONS

- Gap: no locking for concurrent writers; may need file locks if writers increase.
- Idea: add structured logging around queue reads and hook latency.
- Question: should per-playthrough queues replace the default queue path?

## Injection File

```
playthroughs/default/injection_queue.jsonl
```

One JSON object per line. First in, first out.

## Writers

**Graph/Runner - Character Activation**

When a narrative activates a character in the player's group:

```python
injection = {
    "type": "character_speaks",
    "character": "char_aldric",
    "trigger": "narr_patrol_spotted",
    "prompt": "Aldric grabs your arm. 'Wait. Movement ahead.'"
}
append_jsonl(INJECTION_FILE, injection)
```

**Frontend - Player UI**

The frontend posts UI actions to `/api/inject`, which appends the JSON payload to the injection queue.

## Hook Script

File: `engine/scripts/check_injection.py`

Configured in: `agents/narrator/.claude/hooks.json`

Runs on every `PostToolUse` hook **for Narrator only** (not general dev sessions).

```python
import json
import os

INJECTION_FILE = "playthroughs/default/injection_queue.jsonl"

if os.path.exists(INJECTION_FILE):
    with open(INJECTION_FILE) as f:
        lines = f.readlines()

    if lines:
        # Take first injection
        injection = json.loads(lines[0])

        # Rewrite file with remaining injections
        with open(INJECTION_FILE, 'w') as f:
            f.writelines(lines[1:])

        # Return to Claude Code
        print(json.dumps({
            "decision": None,
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": json.dumps(injection)
            }
        }))
        exit()

# No injection
print(json.dumps({"decision": None}))
```

## Narrator Receives

The `additionalContext` field contains the injection. Narrator handles based on type:

```python
# In Narrator's context
injection = json.loads(additional_context)

if injection["type"] == "character_speaks":
    # Insert dialogue, then continue
    stream_dialogue(injection["character"], injection["prompt"])

elif injection["type"] == "player_abort":
    # Generate stop scene at current position
    generate_stop_scene(injection["current_position"])
```

## Injection Types

**character_speaks**

Meaning: Companion reacts to something

```json
{
  "type": "character_speaks",
  "character": "char_aldric",
  "prompt": "Aldric grabs your arm. 'Normans ahead.'"
}
```

Narrator Action: Insert dialogue/action, then continue

**character_acts**

Meaning: Companion does something unprompted

Narrator Action: Describe action, adjust scene

**player_abort**

Meaning: Player pressed stop

Narrator Action: Generate stop scene at current position

**location_change**

Meaning: Player clicked destination on map

Narrator Action: Acknowledge, potentially redirect travel

## When Character Activation Triggers Hook

```
Runner resolves break ->
  Creates narrative in graph ->
    Narrative activates character ->
      Character is in player's group? ->
        YES: Write to injection_queue ->
              Hook fires on next PostToolUse ->
                Narrator receives, handles
        NO: Just update graph (no hook)
```

## Key Clarifications

| Situation | Mechanism |
|-----------|-----------|
| Runner finishes | TaskOutput |
| Character speaks | Hook injection |
| Player clicks UI | Hook injection |
| Place created | Graph SSE |
| Image ready | Graph SSE |

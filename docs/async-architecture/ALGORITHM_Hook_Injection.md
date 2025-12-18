# Hook Injection — Algorithm

**Purpose:** How the world interrupts the Narrator mid-stream.

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

## Injection File

```
playthroughs/default/injection_queue.jsonl
```

One JSON object per line. First in, first out.

---

## Writers

### Graph/Runner — Character Activation

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

### Frontend — Player UI

When player clicks stop button:

```javascript
fetch('/api/inject', {
  method: 'POST',
  body: JSON.stringify({
    type: 'player_abort',
    current_position: currentPlaceId
  })
});
```

Backend appends to file:

```python
append_jsonl(INJECTION_FILE, request.json)
```

---

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

---

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

---

## Injection Types

### character_speaks

**Meaning:** Companion reacts to something

```json
{
  "type": "character_speaks",
  "character": "char_aldric",
  "prompt": "Aldric grabs your arm. 'Normans ahead.'"
}
```

**Narrator Action:** Insert dialogue/action, then continue

---

### character_acts

**Meaning:** Companion does something unprompted

```json
{
  "type": "character_acts",
  "character": "char_aldric",
  "action": "draws sword",
  "reason": "tension_danger broke"
}
```

**Narrator Action:** Describe action, adjust scene

---

### player_abort

**Meaning:** Player pressed stop

```json
{
  "type": "player_abort",
  "current_position": "place_humber_crossing"
}
```

**Narrator Action:** Generate stop scene at current position

---

### location_change

**Meaning:** Player clicked destination on map

```json
{
  "type": "location_change",
  "new_destination": "place_lincoln"
}
```

**Narrator Action:** Acknowledge, potentially redirect travel

---

## When Character Activation Triggers Hook

```
Runner resolves break →
  Creates narrative in graph →
    Narrative activates character →
      Character is in player's group? →
        YES: Write to injection_queue →
              Hook fires on next PostToolUse →
                Narrator receives, handles
        NO: Just update graph (no hook)
```

---

## Key Clarifications

| Situation | Mechanism |
|-----------|-----------|
| Runner finishes | TaskOutput |
| Character speaks | Hook injection |
| Player clicks UI | Hook injection |
| Place created | Graph SSE |
| Image ready | Graph SSE |

Hook is the **interrupt pin**. Everything else has its own channel.

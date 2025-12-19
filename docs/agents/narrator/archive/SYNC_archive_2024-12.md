# Narrator Archive - 2024-12

```
CREATED: 2025-12-19
PURPOSE: Archive long-form narrator documentation removed during size reduction
SOURCE: docs/agents/narrator/*
```

---

## Archived Sections (2025-12-19)

This archive preserves long-form detail removed to reduce the narrator module size. Content here is not necessarily current; use it as historical reference.

---

## HANDOFF_Rolling_Window_Architecture (Full Detail)

```
# Handoff - Rolling Window Architecture

```
CREATED: 2024-12-16
STATUS: Decision made, awaiting implementation
FOR: Backend developer
```

---

## The Problem

Pre-generating 2 layers of clickable responses creates combinatorial explosion:

```
Root scene: 5 clickables
Layer 1:    5 x 5 = 25 responses
Layer 2:    25 x 5 = 125 responses
```

125+ scene packages per generation is too expensive and slow.

---

## The Solution: Rolling Window

Generate **1 layer ahead**. As player clicks, generate next layer in background and push to frontend.

```
+-----------------------------------------------------------------+
|                         ROLLING WINDOW                          |
|                                                                 |
|  1. Scene loads with layer 1 pre-generated (5 responses)       |
|  2. Player clicks "blade"                                       |
|  3. Frontend shows "blade" response immediately (cached)        |
|  4. Backend starts generating layer 2 for new clickables        |
|  5. Backend pushes updates via SSE when ready                   |
|  6. Frontend patches scene tree                                 |
|  7. Player never waits                                          |
|                                                                 |
+-----------------------------------------------------------------+
```

---

## Why SSE (Not WebSocket)

| Requirement | SSE | WebSocket |
|-------------|-----|-----------|
| Server -> Client push | yes | yes |
| Client -> Server | Not needed (use HTTP POST) | yes (overkill) |
| Complexity | Low | Higher |
| Auto-reconnect | Built-in | Manual |
| HTTP/2 compatible | Yes | Separate protocol |

**Decision: Use SSE for scene updates.**

Player actions (clicks) go through normal HTTP. Scene tree updates push via SSE.

---

## API Design

### Click Action (HTTP POST)

```
POST /api/scene/click
Content-Type: application/json

{
  "scene_id": "camp_night",
  "word": "blade",
  "path": ["root"]  # breadcrumb to current position in tree
}
```

**Response:**

```json
{
  "status": "ok",
  "response_cached": true,
  "generation_queued": true
}
```

- `response_cached: true` - Frontend can show response immediately
- `generation_queued: true` - Backend is generating next layer

### Scene Updates (SSE)

```
GET /api/scene/stream
Accept: text/event-stream
```

**Events:**

```
event: scene_update
data: {
  "scene_id": "camp_night",
  "path": ["root", "blade"],
  "clickables": {
    "Wulfric": {
      "speaks": "Who was Wulfric?",
      "intent": "ask_about_family",
      "response": { ... }
    },
    "hands": {
      "speaks": "Your hands stopped.",
      "intent": "observation",
      "response": { ... }
    }
  }
}

event: generation_complete
data: {
  "scene_id": "camp_night",
  "path": ["root", "blade"],
  "depth": 1
}
```

### Scene State (HTTP GET)

For initial load or reconnection:

```
GET /api/scene/{scene_id}
```

Returns full scene tree with all currently-generated responses.

---

## Frontend Responsibilities

1. **On scene load:** Connect to SSE stream, fetch initial scene state
2. **On click:**
   - Immediately render cached response (optimistic)
   - POST click to backend
   - If `response_cached: false`, show brief loading state
3. **On SSE `scene_update`:** Patch scene tree at specified path
4. **On disconnect:** Reconnect SSE, fetch current state to sync

---

## Backend Responsibilities

1. **Scene generation:** Call narrator with `--continue`, parse JSON output
2. **Caching:** Store scene trees in memory/Redis, keyed by `scene_id`
3. **Background generation:** Queue layer 2 generation on click
4. **SSE broadcast:** Push updates to connected clients for that scene
5. **Graph tick:** After `time_elapsed`, run graph tick, check for flips

---

## Generation Queue

Use a simple job queue (Redis, or in-memory for MVP):

```python
@on_click(scene_id, word, path)
def handle_click():
    # 1. Return cached response immediately
    response = cache.get(scene_id, path + [word])

    # 2. Queue generation for new clickables
    for clickable in response.clickables:
        if not cache.has(scene_id, path + [word, clickable]):
            queue.enqueue(generate_response, scene_id, path + [word, clickable])

    return response

@worker
def generate_response(scene_id, path):
    # 1. Call narrator
    response = narrator.generate(scene_id, path)

    # 2. Cache it
    cache.set(scene_id, path, response)

    # 3. Push to frontend
    sse.broadcast(scene_id, {
        "event": "scene_update",
        "path": path[:-1],  # parent path
        "clickables": { path[-1]: response }
    })
```

---

## Edge Cases

### Player clicks before generation completes

Show brief loading indicator ("Aldric considers..."). SSE will push response when ready.

```
event: generation_started
data: { "path": ["root", "blade", "Wulfric"], "eta_ms": 2000 }
```

### Player clicks rapidly (skips ahead)

Each click queues generation. Later clicks may arrive before earlier ones complete. Frontend should handle out-of-order updates gracefully (patch by path).

### Reconnection

On SSE reconnect, frontend should:
1. Fetch current scene state via HTTP GET
2. Diff against local state
3. Patch any missing responses

---

## Narrator Prompt Implications

The narrator CLAUDE.md has been updated to reflect:

- **Layer 1:** Always generate (every clickable has a response)
- **Layer 2:** Rolling window - generated in background

The narrator doesn't need to know about SSE/HTTP. It just generates scene packages on demand.

---

## Open Questions

1. **Prioritization:** If player is clicking fast, which paths to generate first? (Suggest: most recent click path)

2. **TTL:** How long to cache scene trees? (Suggest: per-session, cleared on scene change or graph flip)

3. **Prefetch heuristics:** Should we predict likely clicks and pre-generate? (Suggest: defer to V2)

---

## Files Changed

- `agents/narrator/CLAUDE.md` - Updated depth strategy to rolling window
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` - This file

---

## Next Steps

1. [ ] Implement SSE endpoint (`/api/scene/stream`)
2. [ ] Implement click handler (`POST /api/scene/click`)
3. [ ] Implement generation queue (Redis or in-memory)
4. [ ] Frontend: SSE client + scene tree patching
5. [ ] Frontend: Loading state for uncached responses

---

*"The player never waits. The narrator works ahead. The backend orchestrates."*
```

---

## TOOL_REFERENCE: Complete Example + JSON Schema (Archived)

### Complete Example

```json
{
  "scene": {
    "narration": {
      "raw": "The fire has burned down to embers, casting Aldric's face in shifting orange light. He sits across from you with his blade laid across his knees, drawing the whetstone along its edge in slow, deliberate strokes.",
      "clickables": ["fire", "blade", "embers"]
    },
    "speech": {
      "speaker": "char_aldric",
      "text": {
        "raw": "Can't sleep either?",
        "clickables": ["sleep"]
      }
    },
    "voices": [
      {
        "source": "narr_oath",
        "text": "Three days to York. Three days until you find him.",
        "weight": 0.9,
        "clickables": ["York"]
      },
      {
        "source": "narr_aldric_loyalty",
        "text": "He never sleeps when you don't.",
        "weight": 0.7,
        "clickables": []
      }
    ],
    "clickable": {
      "fire": {
        "speaks": "I'll get more wood.",
        "intent": "practical",
        "response": {
          "narration": {
            "raw": "You rise, and the cold finds you immediately. The treeline is a dark edge against the stars.",
            "clickables": ["cold", "treeline"]
          },
          "speech": {
            "speaker": "char_aldric",
            "text": {
              "raw": "I'll come.",
              "clickables": []
            }
          },
          "voices": [],
          "clickable": {}
        }
      },
      "blade": {
        "speaks": "That blade's seen some use.",
        "intent": "ask_about_past",
        "response": {
          "narration": {
            "raw": "His hands still for a moment before the whetstone resumes.",
            "clickables": ["hands"]
          },
          "speech": {
            "speaker": "char_aldric",
            "text": {
              "raw": "It was Wulfric's.",
              "clickables": ["Wulfric"]
            }
          },
          "voices": [],
          "clickable": {
            "Wulfric": {
              "speaks": "Who was Wulfric?",
              "intent": "ask_about_person",
              "response": {
                "narration": {
                  "raw": "He doesn't look up.",
                  "clickables": []
                },
                "speech": {
                  "speaker": "char_aldric",
                  "text": {
                    "raw": "My brother.",
                    "clickables": ["brother"]
                  }
                },
                "voices": [
                  {
                    "source": "narr_aldric_loyalty",
                    "text": "In all these weeks, he's never mentioned a brother.",
                    "weight": 0.8,
                    "clickables": []
                  }
                ],
                "clickable": {}
              }
            }
          }
        }
      }
    }
  },
  "time_elapsed": "10 minutes",
  "mutations": [
    {
      "type": "new_narrative",
      "payload": {
        "id": "narr_aldric_brother",
        "name": "Aldric's brother Wulfric",
        "content": "Aldric had a brother named Wulfric. The blade was his.",
        "type": "memory",
        "about": {
          "characters": ["char_aldric"]
        },
        "tone": "mournful"
      }
    }
  ],
  "seeds": [
    {
      "setup": "Aldric's brother Wulfric mentioned",
      "intended_payoff": "When death/loss themes arise"
    }
  ]
}
```

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["scene", "time_elapsed"],
  "properties": {
    "scene": {
      "type": "object",
      "required": ["narration", "voices", "clickable"],
      "properties": {
        "narration": { "$ref": "#/definitions/textWithClickables" },
        "speech": {
          "type": "object",
          "required": ["speaker", "text"],
          "properties": {
            "speaker": { "type": "string" },
            "text": { "$ref": "#/definitions/textWithClickables" }
          }
        },
        "voices": {
          "type": "array",
          "items": { "$ref": "#/definitions/voice" }
        },
        "clickable": {
          "type": "object",
          "additionalProperties": { "$ref": "#/definitions/clickable" }
        }
      }
    },
    "time_elapsed": { "type": "string" },
    "mutations": {
      "type": "array",
      "items": { "$ref": "#/definitions/mutation" }
    },
    "seeds": {
      "type": "array",
      "items": { "$ref": "#/definitions/seed" }
    }
  },
  "definitions": {
    "textWithClickables": {
      "type": "object",
      "required": ["raw", "clickables"],
      "properties": {
        "raw": { "type": "string" },
        "clickables": { "type": "array", "items": { "type": "string" } }
      }
    },
    "voice": {
      "type": "object",
      "required": ["source", "text", "weight", "clickables"],
      "properties": {
        "source": { "type": "string" },
        "text": { "type": "string" },
        "weight": { "type": "number", "minimum": 0, "maximum": 1 },
        "clickables": { "type": "array", "items": { "type": "string" } }
      }
    },
    "clickable": {
      "type": "object",
      "required": ["speaks", "intent", "response"],
      "properties": {
        "speaks": { "type": "string" },
        "intent": { "type": "string" },
        "response": { "$ref": "#/properties/scene" }
      }
    },
    "mutation": {
      "type": "object",
      "required": ["type", "payload"],
      "properties": {
        "type": { "enum": ["new_narrative", "update_belief", "adjust_focus"] },
        "payload": { "type": "object" }
      }
    },
    "seed": {
      "type": "object",
      "required": ["setup", "intended_payoff"],
      "properties": {
        "setup": { "type": "string" },
        "intended_payoff": { "type": "string" }
      }
    }
  }
}
```

---

## INPUT_REFERENCE: Complete Example Input (Archived)

```yaml
NARRATOR INSTRUCTION
====================

SCENE_CONTEXT:
  location:
    id: place_camp
    name: "The Camp"
    type: camp
    atmosphere:
      weather: [cold, clear]
      mood: watchful
      details:
        - "fire burning low"
        - "stars visible through bare branches"
        - "horses hobbled nearby"

  time:
    time_of_day: night
    day: 3
    season: winter

  present:
    - id: char_aldric
      name: Aldric
      brief: "Your companion. Terse, loyal, haunted by something he won't discuss."
      modifiers: []

    - id: char_player
      name: Rolf
      brief: "The player character."
      modifiers: []

  active_narratives:
    - id: narr_oath
      weight: 0.9
      summary: "You swore to find Edmund and reclaim what he stole"
      type: oath
      tone: cold

    - id: narr_aldric_loyalty
      weight: 0.7
      summary: "Aldric follows you by choice, not obligation. Why?"
      type: bond
      tone: warm

    - id: narr_thornwick_memory
      weight: 0.5
      summary: "Thornwick burned. Your home is ash."
      type: memory
      tone: bitter

  tensions:
    - id: tension_confrontation
      description: "Edmund draws closer. The reckoning approaches."
      pressure: 0.6
      breaking_point: 0.9

    - id: tension_aldric_secret
      description: "Aldric carries something he hasn't shared."
      pressure: 0.3
      breaking_point: 0.9

  player_state:
    pursuing: "Find Edmund in York"
    recent: "Camped after two days on the road from Thornwick"
    modifiers: []

WORLD_INJECTION:
  null

GENERATION_INSTRUCTION:
  Generate the opening scene for this camp moment.
  Player has just settled by the fire.
  Aldric is sharpening his blade across from them.

  Include:
  - Atmospheric narration (2-3 sentences)
  - Aldric's opening line (if any)
  - 2-3 voices from active narratives
  - 3-6 clickable words with responses
  - time_elapsed estimate

  Output JSON matching NarratorOutput schema.
```

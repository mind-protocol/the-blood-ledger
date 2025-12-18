# Narrator Tool Reference

Definitive JSON schemas for Narrator output. Use in prompts via `@docs/engine/narrator/TOOL_REFERENCE.md`

---

## How To Use

### 1. From Orchestrator (Production)

The orchestrator calls the Narrator via Claude CLI:

```bash
# First call (starts persistent session)
claude -p "$(cat narrator_prompt.txt)" --output-format json

# Subsequent calls (continues session)
claude --continue -p "$(cat narrator_prompt.txt)" --output-format json
```

The `--continue` flag maintains context across the entire playthrough.

### 2. Testing a Prompt

```bash
# Test with a scene context
claude -p "
NARRATOR INSTRUCTION
════════════════════

SCENE_CONTEXT:
  location:
    name: 'The Camp'
    type: camp
    atmosphere:
      weather: [cold, clear]
      mood: watchful

  present:
    - id: char_aldric
      name: Aldric
      brief: 'Your companion. Terse, loyal.'

  active_narratives:
    - id: narr_oath
      weight: 0.9
      summary: 'You swore to find Edmund'

Generate opening scene. Output JSON.
" --output-format json
```

### 3. Validating Output

```python
from engine.models import Narrative, NarrativeType
import json

# Parse Narrator output
output = json.loads(narrator_response)

# Validate mutations
for mutation in output.get('mutations', []):
    if mutation['type'] == 'new_narrative':
        # Validate against Pydantic model
        Narrative(
            id=mutation['payload']['id'],
            name=mutation['payload']['name'],
            content=mutation['payload']['content'],
            type=NarrativeType(mutation['payload']['type']),
            # ...
        )
```

### 4. Script Locations

```
engine/orchestration/narrator.py       # Narrator caller (Claude CLI wrapper)
engine/orchestration/narrator_prompt.py # Prompt builder
engine/orchestration/mutations.py       # Mutation applier
engine/models/                          # Pydantic models
```

---

## Complete Output Schema

```typescript
interface NarratorOutput {
  scene: ScenePackage;
  time_elapsed: string;           // REQUIRED - drives world simulation
  mutations?: GraphMutation[];    // Changes discovered during generation
  seeds?: Seed[];                 // Setups for future payoff
}
```

---

## Scene Package

```typescript
interface ScenePackage {
  narration: TextWithClickables;
  speech?: SpeechBlock;
  voices: Voice[];
  clickable: Record<string, Clickable>;
}

interface TextWithClickables {
  raw: string;              // Full prose text
  clickables: string[];     // Words that can be clicked (3-6)
}

interface SpeechBlock {
  speaker: string;          // Character ID (e.g., "char_aldric")
  text: TextWithClickables;
}

interface Voice {
  source: string;           // Narrative ID (e.g., "narr_oath")
  text: string;             // What the narrative whispers
  weight: number;           // 0.0-1.0, determines prominence
  clickables: string[];     // Words that can be clicked
}

interface Clickable {
  speaks: string;           // What player says when clicking
  intent: string;           // Tag for tracking
  response: ScenePackage;   // Full nested response
}
```

### Intent Tags

Standard intent tags for tracking player patterns:

| Intent | Meaning |
|--------|---------|
| `ask_about_past` | Inquiring about history/backstory |
| `ask_about_person` | Asking about someone |
| `challenge` | Confrontational |
| `practical` | Action-oriented |
| `emotional` | Expressing/seeking emotion |
| `explore` | Investigating environment |
| `confirm` | Seeking validation |
| `deny` | Rejecting something |

---

## Time Elapsed

**REQUIRED on every output. Drives world simulation.**

```typescript
time_elapsed: string;  // e.g., "10 minutes", "2 hours", "1 day"
```

### Guidelines

| Scene Type | Estimate |
|------------|----------|
| Brief reaction | "1-2 minutes" |
| Single exchange | "3-5 minutes" |
| Conversation turn | "5-10 minutes" |
| Deep dialogue | "20-30 minutes" |
| Extended scene | "1 hour" |
| Rest/camp | "4-8 hours" |
| Travel (short) | "2-4 hours" |
| Travel (long) | "1-3 days" |

---

## Graph Mutations

Mutations the Narrator discovers during generation.

```typescript
interface GraphMutation {
  type: 'new_narrative' | 'update_belief' | 'adjust_focus';
  payload: NewNarrativePayload | UpdateBeliefPayload | AdjustFocusPayload;
}
```

### New Narrative

```typescript
interface NewNarrativePayload {
  id: string;               // e.g., "narr_aldric_brother"
  name: string;             // Short label
  content: string;          // The story itself
  type: NarrativeType;      // From schema
  about: {
    characters?: string[];  // Character IDs involved
    places?: string[];      // Place IDs involved
    things?: string[];      // Thing IDs involved
  };
  tone?: NarrativeTone;     // Emotional color
  truth?: number;           // 0-1, director only
}
```

#### Narrative Types (from schema)

Events: `memory`, `account`, `rumor`
Characters: `reputation`, `identity`
Relationships: `bond`, `oath`, `debt`, `blood`, `enmity`, `love`, `service`
Things: `ownership`, `claim`
Places: `control`, `origin`
Meta: `belief`, `prophecy`, `lie`, `secret`

#### Narrative Tones

`bitter`, `proud`, `shameful`, `defiant`, `mournful`, `cold`, `righteous`, `hopeful`, `fearful`, `warm`, `dark`, `sacred`

### Update Belief

```typescript
interface UpdateBeliefPayload {
  character: string;        // Character ID
  narrative: string;        // Narrative ID
  heard?: number;           // 0-1, how much they know
  believes?: number;        // 0-1, how certain
  doubts?: number;          // 0-1, active uncertainty
  denies?: number;          // 0-1, rejects as false
  source?: BeliefSource;    // How they learned
  from_whom?: string;       // Character ID who told them
}
```

#### Belief Sources

`witnessed`, `told`, `inferred`, `assumed`, `taught`

### Adjust Focus

```typescript
interface AdjustFocusPayload {
  narrative: string;        // Narrative ID
  focus: number;            // 0.1-3.0 multiplier
  reason: string;           // Why adjusting
}
```

---

## Seeds

Continuity notes for future payoff.

```typescript
interface Seed {
  setup: string;            // What was planted
  intended_payoff: string;  // When/how it should pay off
}
```

---

## Complete Example

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

---

## Validation Rules

1. **`time_elapsed` is REQUIRED** — Never omit
2. **`clickables` array must match words in `raw`** — Exact string match
3. **`source` in Voice must be valid narrative ID**
4. **`speaker` must be valid character ID**
5. **Nested responses must be complete ScenePackages**
6. **Mutation types must follow schema exactly**
7. **3-6 clickables per scene state** — Not more, not fewer

---

## JSON Schema (for programmatic validation)

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

# World Runner Tool Reference

Definitive JSON schemas for World Runner output. Use in prompts via `@docs/agents/world-runner/TOOL_REFERENCE.md`

---

## Complete Output Schema

```typescript
interface WorldRunnerOutput {
  thinking: string;                    // Brief reasoning trace
  graph_mutations: GraphMutations;     // Changes to apply to graph
  world_injection: WorldInjection;     // Context for Narrator
}
```

---

## CHAIN

PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
INPUTS:          ./INPUT_REFERENCE.md
TOOLS:           ./TOOL_REFERENCE.md
SYNC:            ./SYNC_World_Runner.md

---

## Graph Mutations

All changes to apply to the graph after a flip.

```typescript
interface GraphMutations {
  new_narratives?: NewNarrative[];
  new_beliefs?: NewBelief[];
  tension_updates?: TensionUpdate[];
  new_tensions?: NewTension[];
  character_movements?: CharacterMovement[];
  modifier_changes?: ModifierChange[];
}
```

### New Narrative

```typescript
interface NewNarrative {
  id: string;                 // e.g., "narr_edmund_move"
  name: string;               // Short label
  content: string;            // The story - what happened, what is believed
  interpretation?: string;    // What it means - emotional/thematic weight
  type: NarrativeType;        // From schema
  about: {
    characters?: string[];    // Character IDs
    relationship?: string[];  // Pair of character IDs (for bond/enmity)
    places?: string[];        // Place IDs
    things?: string[];        // Thing IDs
  };
  tone?: NarrativeTone;       // Emotional color
  truth?: number;             // 0-1, director only (how true is this?)
  focus?: number;             // 0.1-3.0, pacing multiplier
}
```

#### Narrative Types

**Events:** `memory`, `account`, `rumor`
**Characters:** `reputation`, `identity`
**Relationships:** `bond`, `oath`, `debt`, `blood`, `enmity`, `love`, `service`
**Things:** `ownership`, `claim`
**Places:** `control`, `origin`
**Meta:** `belief`, `prophecy`, `lie`, `secret`

#### Narrative Tones

`bitter`, `proud`, `shameful`, `defiant`, `mournful`, `cold`, `righteous`, `hopeful`, `fearful`, `warm`, `dark`, `sacred`

### New Belief

```typescript
interface NewBelief {
  character: string;          // Character ID who now believes
  narrative: string;          // Narrative ID they believe
  heard: number;              // 0-1, how much they know
  believes?: number;          // 0-1, how certain
  doubts?: number;            // 0-1, active uncertainty
  denies?: number;            // 0-1, rejects as false
  source: BeliefSource;       // How they learned
  from_whom?: string;         // Character ID who told them
}
```

#### Belief Sources

| Source | Meaning |
|--------|---------|
| `witnessed` | Saw it happen |
| `told` | Someone told them |
| `inferred` | Figured out from evidence |
| `assumed` | Believes without evidence |
| `taught` | Learned as established fact |

### Tension Update

```typescript
interface TensionUpdate {
  id: string;                 // Tension ID
  pressure?: number;          // New pressure level (0-1)
  resolved?: boolean;         // If true, tension is done
  reason: string;             // Why this change
}
```

### New Tension

```typescript
interface NewTension {
  id: string;                 // e.g., "tension_retaliation"
  narratives: string[];       // Narrative IDs involved
  description: string;        // What this tension is about
  pressure: number;           // Starting pressure (0-1)
  pressure_type: PressureType;
  breaking_point?: number;    // Default 0.9
  base_rate?: number;         // For gradual, default 0.001
  trigger_at?: string;        // For scheduled, when it must break
  progression?: TensionStep[]; // For scheduled/hybrid
  narrator_notes?: string;    // Notes for how to handle the break
}

type PressureType = 'gradual' | 'scheduled' | 'hybrid';

interface TensionStep {
  at: string;                 // Time point, e.g., "Day 15"
  pressure?: number;          // For scheduled
  pressure_floor?: number;    // For hybrid
}
```

### Character Movement

```typescript
interface CharacterMovement {
  character: string;          // Character ID
  from?: string;              // Place ID (optional)
  to: string;                 // Place ID
  visible?: boolean;          // Default true
}
```

### Modifier Change

```typescript
interface ModifierChange {
  node: string;               // Node ID (character, place, or thing)
  add?: Modifier;             // Modifier to add
  remove?: string;            // Modifier type to remove
}

interface Modifier {
  type: ModifierType;
  severity: 'mild' | 'moderate' | 'severe';
  duration?: string;          // "until healed", "3 days", etc.
  source: string;             // What caused this
}
```

#### Modifier Types

**Character:** `wounded`, `sick`, `hungry`, `exhausted`, `drunk`, `grieving`, `inspired`, `afraid`, `angry`, `hopeful`, `suspicious`
**Place:** `burning`, `flooded`, `besieged`, `abandoned`, `celebrating`, `haunted`, `watched`, `safe`
**Thing:** `damaged`, `hidden`, `contested`, `blessed`, `cursed`, `stolen`

---

## World Injection

Context provided to the Narrator for the next scene.

```typescript
interface WorldInjection {
  time_since_last: string;              // Time span processed
  breaks: Break[];                       // What broke and how
  news_arrived?: NewsItem[];            // News that reached player's location
  tension_changes?: Record<string, string>; // Changes to surface
  interruption?: Interruption | null;   // If current scene should be interrupted
  atmosphere_shift?: string;            // New atmospheric detail
  narrator_notes?: string;              // Guidance for Narrator
}
```

### Break

```typescript
interface Break {
  tension_id: string;         // Which tension broke
  narrative: string;          // Primary narrative involved
  event: string;              // What specifically happened
  location: string;           // Where it happened
  player_awareness: PlayerAwareness;
  witnesses?: string[];       // Character IDs who saw it
}

type PlayerAwareness =
  | 'witnessed'   // Player was there
  | 'encountered' // Player will pass through
  | 'heard'       // News reached player
  | 'will_hear'   // News will reach destination
  | 'unknown';    // Player has no way of knowing
```

### News Item

```typescript
interface NewsItem {
  narrative: string;          // Narrative ID
  summary: string;            // Brief description
  source: string;             // Who brought the news
  reliability: number;        // 0-1, how accurate
}
```

### Interruption

```typescript
interface Interruption {
  type: InterruptionType;
  character?: string;         // For 'arrival' or 'message'
  event?: string;             // For 'event'
  urgency: 'low' | 'medium' | 'high' | 'critical';
  description: string;
}

type InterruptionType = 'arrival' | 'message' | 'event';
```

---

## Complete Example

```json
{
  "thinking": "Edmund's confrontation tension flipped. Given Rolf's oath and Edmund's location in York, Edmund would have received word of Rolf's approach and made a preemptive political move. This creates a new retaliation tension.",

  "graph_mutations": {
    "new_narratives": [
      {
        "id": "narr_edmund_move",
        "name": "Edmund made his move",
        "content": "Edmund's allies in York have begun spreading word that Rolf's claim to Thornwick is illegitimate, based on documents Edmund 'discovered' among their father's effects.",
        "interpretation": "Edmund strikes first, using politics rather than steel.",
        "type": "account",
        "about": {
          "characters": ["char_edmund", "char_rolf"],
          "places": ["place_york"]
        },
        "tone": "cold",
        "truth": 0.3
      },
      {
        "id": "narr_thornwick_documents",
        "name": "The disputed documents",
        "content": "Documents purportedly from the old lord suggest Thornwick was always meant for Edmund alone.",
        "type": "claim",
        "about": {
          "characters": ["char_edmund"],
          "things": ["thing_thornwick_deed"],
          "places": ["place_thornwick"]
        },
        "tone": "cold",
        "truth": 0.1
      }
    ],

    "new_beliefs": [
      {
        "character": "char_wulfstan",
        "narrative": "narr_edmund_move",
        "heard": 1.0,
        "believes": 0.8,
        "source": "told",
        "from_whom": "char_merchant"
      },
      {
        "character": "char_gospatric",
        "narrative": "narr_edmund_move",
        "heard": 1.0,
        "believes": 0.3,
        "doubts": 0.6,
        "source": "told"
      }
    ],

    "tension_updates": [
      {
        "id": "tension_confrontation",
        "pressure": 0.0,
        "resolved": true,
        "reason": "Confrontation occurred - Edmund acted first"
      }
    ],

    "new_tensions": [
      {
        "id": "tension_retaliation",
        "narratives": ["narr_edmund_move", "narr_rolf_oath"],
        "description": "Rolf will not accept Edmund's political attack quietly. His oath demands response.",
        "pressure": 0.4,
        "pressure_type": "hybrid",
        "breaking_point": 0.9,
        "base_rate": 0.002,
        "progression": [
          { "at": "Day 18", "pressure_floor": 0.5 },
          { "at": "Day 20", "pressure_floor": 0.7 }
        ],
        "narrator_notes": "Rolf's response will be physical, not political. He doesn't play Edmund's game."
      }
    ],

    "character_movements": [
      {
        "character": "char_edmund",
        "from": "place_york_hall",
        "to": "place_castle",
        "visible": false
      }
    ],

    "modifier_changes": [
      {
        "node": "char_messenger",
        "add": {
          "type": "exhausted",
          "severity": "moderate",
          "duration": "until rested",
          "source": "Hard riding from York"
        }
      },
      {
        "node": "place_york",
        "add": {
          "type": "tense",
          "severity": "mild",
          "source": "Rumors of the dispute spreading"
        }
      }
    ]
  },

  "world_injection": {
    "time_since_last": "2 days",

    "breaks": [
      {
        "tension_id": "tension_confrontation",
        "narrative": "narr_edmund_move",
        "event": "Edmund's allies moved against Rolf's claim publicly in York",
        "location": "place_york",
        "player_awareness": "will_hear",
        "witnesses": ["char_wulfstan", "char_gospatric", "char_merchant"]
      }
    ],

    "news_arrived": [],

    "tension_changes": {
      "tension_retaliation": "created at 0.4"
    },

    "interruption": null,

    "atmosphere_shift": "The road to York feels different now. Merchants pass without meeting your eyes.",

    "narrator_notes": "Player will learn of Edmund's move when they reach York or meet someone from there. The political landscape has shifted - Edmund has allies, Rolf has a harder path."
  }
}
```

---

## Validation Rules

1. **`thinking` is REQUIRED** — Reasoning must be traceable
2. **All IDs must be valid** — Character, place, narrative IDs must exist or be created
3. **`about` must reference existing nodes** — Or nodes being created in same mutation
4. **`truth` is director-only** — Characters never see this field
5. **Belief `heard` must be > 0 for other fields to matter**
6. **Tension `narratives` must exist** — Or be created in same mutation
7. **`player_awareness` must be accurate** — Based on player location

---

## Processing Order

When applying mutations:

1. **New narratives first** — Create before referencing
2. **New beliefs second** — Now narratives exist to believe
3. **Tension updates third** — Existing tensions modified
4. **New tensions fourth** — New clusters created
5. **Character movements fifth** — Physical state changes
6. **Modifier changes last** — Temporary states applied

---

## JSON Schema (for programmatic validation)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["thinking", "graph_mutations", "world_injection"],
  "properties": {
    "thinking": { "type": "string" },
    "graph_mutations": {
      "type": "object",
      "properties": {
        "new_narratives": {
          "type": "array",
          "items": { "$ref": "#/definitions/newNarrative" }
        },
        "new_beliefs": {
          "type": "array",
          "items": { "$ref": "#/definitions/newBelief" }
        },
        "tension_updates": {
          "type": "array",
          "items": { "$ref": "#/definitions/tensionUpdate" }
        },
        "new_tensions": {
          "type": "array",
          "items": { "$ref": "#/definitions/newTension" }
        },
        "character_movements": {
          "type": "array",
          "items": { "$ref": "#/definitions/characterMovement" }
        },
        "modifier_changes": {
          "type": "array",
          "items": { "$ref": "#/definitions/modifierChange" }
        }
      }
    },
    "world_injection": {
      "type": "object",
      "required": ["time_since_last", "breaks"],
      "properties": {
        "time_since_last": { "type": "string" },
        "breaks": {
          "type": "array",
          "items": { "$ref": "#/definitions/break" }
        },
        "news_arrived": { "type": "array" },
        "tension_changes": { "type": "object" },
        "interruption": { "type": ["object", "null"] },
        "atmosphere_shift": { "type": "string" },
        "narrator_notes": { "type": "string" }
      }
    }
  },
  "definitions": {
    "newNarrative": {
      "type": "object",
      "required": ["id", "name", "content", "type", "about"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "content": { "type": "string" },
        "interpretation": { "type": "string" },
        "type": { "type": "string" },
        "about": { "type": "object" },
        "tone": { "type": "string" },
        "truth": { "type": "number", "minimum": 0, "maximum": 1 },
        "focus": { "type": "number", "minimum": 0.1, "maximum": 3.0 }
      }
    },
    "newBelief": {
      "type": "object",
      "required": ["character", "narrative", "heard", "source"],
      "properties": {
        "character": { "type": "string" },
        "narrative": { "type": "string" },
        "heard": { "type": "number", "minimum": 0, "maximum": 1 },
        "believes": { "type": "number", "minimum": 0, "maximum": 1 },
        "doubts": { "type": "number", "minimum": 0, "maximum": 1 },
        "denies": { "type": "number", "minimum": 0, "maximum": 1 },
        "source": { "type": "string" },
        "from_whom": { "type": "string" }
      }
    },
    "tensionUpdate": {
      "type": "object",
      "required": ["id", "reason"],
      "properties": {
        "id": { "type": "string" },
        "pressure": { "type": "number", "minimum": 0, "maximum": 1 },
        "resolved": { "type": "boolean" },
        "reason": { "type": "string" }
      }
    },
    "newTension": {
      "type": "object",
      "required": ["id", "narratives", "description", "pressure", "pressure_type"],
      "properties": {
        "id": { "type": "string" },
        "narratives": { "type": "array", "items": { "type": "string" } },
        "description": { "type": "string" },
        "pressure": { "type": "number", "minimum": 0, "maximum": 1 },
        "pressure_type": { "enum": ["gradual", "scheduled", "hybrid"] },
        "breaking_point": { "type": "number", "minimum": 0, "maximum": 1 },
        "base_rate": { "type": "number" },
        "trigger_at": { "type": "string" },
        "progression": { "type": "array" },
        "narrator_notes": { "type": "string" }
      }
    },
    "characterMovement": {
      "type": "object",
      "required": ["character", "to"],
      "properties": {
        "character": { "type": "string" },
        "from": { "type": "string" },
        "to": { "type": "string" },
        "visible": { "type": "boolean" }
      }
    },
    "modifierChange": {
      "type": "object",
      "required": ["node"],
      "properties": {
        "node": { "type": "string" },
        "add": { "type": "object" },
        "remove": { "type": "string" }
      }
    },
    "break": {
      "type": "object",
      "required": ["tension_id", "narrative", "event", "location", "player_awareness"],
      "properties": {
        "tension_id": { "type": "string" },
        "narrative": { "type": "string" },
        "event": { "type": "string" },
        "location": { "type": "string" },
        "player_awareness": { "enum": ["witnessed", "encountered", "heard", "will_hear", "unknown"] },
        "witnesses": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

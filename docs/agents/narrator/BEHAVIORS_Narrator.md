# Narrator — Behaviors: What the Narrator Produces

```
CREATED: 2024-12-16
UPDATED: 2024-12-16
STATUS: Canonical (updated for conversational-first flow)
```

---

## Two Response Modes

The narrator operates in two modes based on action classification:

| Mode | Threshold | Output |
|------|-----------|--------|
| **Conversational** | <5 minutes | Dialogue chunks + mutations + `{}` (empty scene) |
| **Significant** | ≥5 minutes | Dialogue chunks + mutations + full SceneTree + time_elapsed |

---

## Dialogue Chunks

Streamed in real-time as the narrator generates:

```typescript
interface DialogueChunk {
  speaker?: string;  // Character ID if dialogue, omit for narration
  text: string;      // The content
}
```

**Examples:**
```json
{ "speaker": "Aldric", "text": "Ahah, kids..." }
{ "text": "He looks into the fire, something shifting behind his eyes." }
{ "speaker": "Aldric", "text": "No. Never had the life for it." }
```

**Rules:**
- Chunks with `speaker` are dialogue (rendered with quotes)
- Chunks without `speaker` are narration (rendered italic)
- Stream chunked for natural pacing
- Query graph between chunks as needed

---

## Graph Mutations

Changes invented during generation that must be persisted:

```typescript
interface GraphMutation {
  type: 'new_character' | 'new_edge' | 'new_narrative' | 'update_belief' | 'adjust_focus';
  payload: Record<string, unknown>;
}
```

### Mutation Types

| Type | When | Example |
|------|------|---------|
| `new_character` | Invented during conversation | Aldric's niece Edda |
| `new_edge` | New relationship discovered | Aldric -[:KIN]-> Edda |
| `new_narrative` | Backstory, memory, rumor | "Edda trained near Thornwick" |
| `update_belief` | Character learns something | Player now knows about Edda |
| `adjust_focus` | Pacing change | Increase weight of a narrative |

### new_character

```typescript
interface NewCharacterPayload {
  id: string;              // e.g., "char_edda"
  name: string;
  traits?: string[];
  location?: string;       // Place ID
}
```

### new_edge

```typescript
interface NewEdgePayload {
  from: string;            // Node ID
  to: string;              // Node ID
  type: string;            // Edge type: KIN, KNOWS, OWES, etc.
  properties?: Record<string, any>;
}
```

### new_narrative

```typescript
interface NewNarrativePayload {
  id: string;
  name: string;
  content: string;
  type: string;            // memory, account, rumor, bond, oath, etc.
  about: {
    characters?: string[];
    places?: string[];
    things?: string[];
  };
  truth?: number;          // 0-1, director only
}
```

### update_belief

```typescript
interface UpdateBeliefPayload {
  character: string;       // Character ID
  narrative: string;       // Narrative ID
  believes?: number;       // 0-1
  heard?: number;          // 0-1
  doubts?: number;         // 0-1
}
```

### adjust_focus

```typescript
interface AdjustFocusPayload {
  narrative: string;       // Narrative ID
  focus: number;           // 0.1-3.0 multiplier for pacing
  reason: string;
}
```

---

## Scene Package (Significant Actions Only)

For significant actions, a full SceneTree is generated:

```typescript
interface SceneTree {
  id: string;
  location: {
    place: string;          // Graph place ID
    name: string;           // Display name
    region: string;         // Location description
    time: string;           // Time of day
  };
  present: string[];        // Character IDs present
  atmosphere: string[];     // Atmospheric text lines
  narration: SceneTreeNarration[];
  voices: SceneTreeVoice[];
  freeInput?: SceneTreeFreeInput;
  exits?: {
    travel?: SceneTreeExit;
    wait?: SceneTreeExit;
  };
}
```

### SceneTreeNarration

```typescript
interface SceneTreeNarration {
  text: string;
  speaker?: string;         // If this is dialogue
  clickable?: Record<string, SceneTreeClickable>;
}
```

### SceneTreeClickable

```typescript
interface SceneTreeClickable {
  speaks: string;           // What player says when clicking
  intent: string;           // Tag for tracking
  response?: SceneTreeResponse;  // Pre-baked response (optional)
  waitingMessage?: string;  // Shown while LLM generates (required if no response)
}
```

### SceneTreeResponse

```typescript
interface SceneTreeResponse {
  type?: 'narration';       // Optional - defaults to speech if speaker present
  speaker?: string;         // Character speaking (if dialogue)
  text: string;             // The response text
  then?: SceneTreeNarration; // Follow-up narration with more clickables
  clickable?: Record<string, SceneTreeClickable>; // New clickables in response
}
```

---

## Complete Output Schema

```typescript
interface NarratorOutput {
  dialogue: DialogueChunk[];        // Streamed response chunks
  mutations: GraphMutation[];       // Changes invented during generation
  scene: SceneTree | {};            // Full scene OR empty for conversational
  time_elapsed?: string;            // Only for significant actions (≥5 min)
  seeds?: Seed[];                   // Setups for future payoff
}

interface Seed {
  setup: string;           // What was planted
  intended_payoff: string; // When it should pay off
}
```

---

## time_elapsed Guidelines

**Only include for significant actions.** Conversational responses omit this field.

| Action Type | Estimate | Triggers World? |
|-------------|----------|-----------------|
| Quick question | — | No |
| Character observation | — | No |
| Short exchange | — | No |
| Extended conversation | "10-20 minutes" | Yes |
| Deep dialogue | "30 minutes" | Yes |
| Short travel | "2-4 hours" | Yes |
| Long travel | "1-3 days" | Yes |
| Rest/camp | "4-8 hours" | Yes |
| Combat | "5-30 minutes" | Yes |

**The ~5 minute threshold:** Below this, the action is conversational. Above, it's significant and triggers the world runner.

---

## Input: World Injection

The narrator may receive a world injection (from World Runner after flips):

```typescript
interface WorldInjection {
  time_since_last: string;
  breaks: NarrativeBreak[];
  news_arrived: string[];
  tension_changes: Record<string, number>;
  interruption: Interruption | null;
  atmosphere_shift: string;
  narrator_notes: string;
}
```

### How to Handle

| Injection Type | Narrator Action |
|----------------|-----------------|
| `breaks` (witnessed) | Weave directly into dialogue |
| `breaks` (heard) | Deliver as news via character/messenger |
| `breaks` (will_hear) | Note for later, don't include yet |
| `interruption` (high) | Break current flow, this takes over |
| `interruption` (medium) | Weave into next beat naturally |
| `atmosphere_shift` | Include in narration chunks |
| `narrator_notes` | Suggestions, not commands |

---

## Quality Indicators

| Indicator | Target | Meaning |
|-----------|--------|---------|
| Voice consistency | High | Characters sound like themselves |
| Response time | Immediate | First chunk streams within 1-2s |
| Invention quality | Canonical | Invented content fits the world |
| Connection density | High | New content links to existing graph |
| Setup/payoff tracking | Complete | Know what's planted, what's owed |

---

## Example: Conversational Response

Player: "Aldric, do you have kids?"

```json
{
  "dialogue": [
    { "speaker": "Aldric", "text": "Ahah, kids..." },
    { "text": "He looks into the fire, something shifting behind his eyes." },
    { "speaker": "Aldric", "text": "No. Never had the life for it." },
    { "speaker": "Aldric", "text": "But my niece — Edda — she's the finest archer north of the Humber." },
    { "text": "He glances at you, something like curiosity in his expression." },
    { "speaker": "Aldric", "text": "Actually... she trained near Thornwick. Might've known your people, before." }
  ],
  "mutations": [
    {
      "type": "new_character",
      "payload": {
        "id": "char_edda",
        "name": "Edda",
        "traits": ["archer", "skilled"],
        "location": "place_jorvik_region"
      }
    },
    {
      "type": "new_edge",
      "payload": {
        "from": "char_aldric",
        "to": "char_edda",
        "type": "KIN",
        "properties": { "relation": "niece" }
      }
    },
    {
      "type": "new_narrative",
      "payload": {
        "id": "narr_edda_thornwick",
        "name": "Edda's connection to Thornwick",
        "content": "Aldric's niece Edda trained near Thornwick. She may have known the player's people.",
        "type": "memory",
        "about": { "characters": ["char_edda"], "places": ["place_thornwick"] }
      }
    }
  ],
  "scene": {}
}
```

No scene refresh. No time elapsed. Conversation continues. World stays frozen.

---

*"The narrator doesn't just produce text. It produces a world that grows through conversation."*

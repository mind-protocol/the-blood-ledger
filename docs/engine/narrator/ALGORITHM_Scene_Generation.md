# Narrator — Algorithm: Scene Generation

```
CREATED: 2024-12-16
UPDATED: 2024-12-16
STATUS: Canonical (updated for conversational-first flow)
DEPENDS_ON: graph.json, character backstories
```

---

## Purpose

This document specifies how the narrator generates responses, both for conversational actions (dialogue only) and significant actions (full scene trees).

---

## Two Generation Modes

### Conversational (Default)

For questions, observations, character interactions — anything <5 minutes:

```
1. Classify action as conversational
2. Stream dialogue chunks immediately
3. Query graph for facts mid-stream
4. Invent when graph is sparse
5. Output mutations
6. Return empty scene {}
```

### Significant

For travel, rest, combat, major decisions — anything ≥5 minutes:

```
1. Classify action as significant
2. Stream transition dialogue
3. Query graph for context
4. Generate full SceneTree
5. Output mutations
6. Return scene + time_elapsed
```

---

## Input: Scene Context

Before generation, gather from graph:

```typescript
interface SceneContext {
  place: Place;                    // Where this happens
  present: Character[];            // Who is here
  activeNarratives: Narrative[];   // High-weight narratives (become voices)
  tensions: Tension[];             // What might break
  recentHistory: ChronicleEntry[]; // What just happened
  playerState: {
    day: number;
    goals: string[];               // What player is pursuing
    patterns: PlayerPatterns;      // How they've been playing
  };
}
```

---

## Conversational Generation

### Step 0: Classify

Determine if action is conversational (<5 min) or significant (≥5 min):

| Conversational | Significant |
|----------------|-------------|
| "Do you have kids?" | "Let's break camp" |
| "Tell me about York" | "I attack him" |
| Clicking a character detail | Travel |
| Observation | Rest |

### Step 1: Stream Immediately

Don't wait for context. Start with character voice:

```json
{ "speaker": "Aldric", "text": "Ahah, kids..." }
```

### Step 2: Query Graph

Mid-stream, query for facts:

```
Query: "Does Aldric have family or children?"
Graph: Sister (deceased). Niece exists, sparse details.
```

### Step 3: Continue with Facts

```json
{ "text": "He looks into the fire, something shifting behind his eyes." }
{ "speaker": "Aldric", "text": "No. Never had the life for it." }
```

### Step 4: Invent When Sparse

The graph says niece exists but nothing more. Invent:

```
Invent: Niece named Edda. Archer. Lives near Jorvik.
```

```json
{ "speaker": "Aldric", "text": "But my niece — Edda — she's the finest archer north of the Humber." }
```

### Step 5: Look for Connections

Query again for connection opportunities:

```
Query: "Where did the player grow up?"
Graph: Thornwick, same region.
```

```json
{ "text": "He glances at you, something like curiosity in his expression." }
{ "speaker": "Aldric", "text": "Actually... she trained near Thornwick. Might've known your people." }
```

### Step 6: Output Mutations

Everything invented becomes a mutation:

```json
{
  "mutations": [
    { "type": "new_character", "payload": { "id": "char_edda", "name": "Edda", "traits": ["archer"] } },
    { "type": "new_edge", "payload": { "from": "char_aldric", "to": "char_edda", "type": "KIN" } },
    { "type": "new_narrative", "payload": { "id": "narr_edda_thornwick", "content": "Edda trained near Thornwick..." } }
  ]
}
```

### Step 7: Return Empty Scene

```json
{ "scene": {} }
```

Conversation continues. World stays frozen. No time passes.

---

## Significant Generation

### Step 1: Stream Transition

Even significant actions get immediate response:

```json
{ "text": "You stamp out the embers. The moor stretches dark before you." }
{ "text": "Aldric gathers the horses without a word." }
```

### Step 2: Query for Context

```
Query: "What's between here and York?"
Query: "Any world events pending?"
Query: "What tensions involve present characters?"
```

### Step 3: Weave Injections

If `world_injection.md` exists, weave events:

```json
{ "speaker": "Aldric", "text": "Smoke to the north. Too much for a farmstead." }
```

### Step 4: Generate Full SceneTree

Build complete scene for arrival or next moment:

```typescript
interface SceneTree {
  id: string;
  location: SceneLocation;
  present: string[];
  atmosphere: string[];
  narration: SceneTreeNarration[];
  voices: SceneTreeVoice[];
  freeInput?: SceneTreeFreeInput;
}
```

### Step 5: Output with time_elapsed

```json
{
  "dialogue": [...],
  "mutations": [...],
  "scene": { /* full SceneTree */ },
  "time_elapsed": "4 hours"
}
```

This triggers the world runner.

---

## SceneTree Structure

For significant actions, generate a full scene:

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
  atmosphere: string[];     // 2-3 atmospheric lines
  narration: SceneTreeNarration[];
  voices: SceneTreeVoice[];
  freeInput?: {
    enabled: boolean;
    handler: string;
    context: string[];
  };
}
```

### SceneTreeNarration

```typescript
interface SceneTreeNarration {
  text: string;                                     // 2-3 sentences
  speaker?: string;                                 // If dialogue
  clickable?: Record<string, SceneTreeClickable>;   // Embedded clickables
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

---

## Character Voice Guidelines

### Aldric
- Short sentences. Doesn't waste words.
- Saxon rhythms. Direct.
- Avoids talking about feelings directly.
- When pressed, deflects or goes silent.
- When he does open up, it's powerful because it's rare.

**Examples:**
- "Keeps my hands busy."
- "Everyone knows what the Harrying was."
- "Nothing worth saying."

### Edmund (when encountered)
- More words than necessary. Justifying.
- Defensive but trying to seem reasonable.
- Believes his own story.
- Mentions practical concerns.

**Examples:**
- "You don't understand what it was like. Father was dying, someone had to—"
- "I saved the family. You would have lost everything."

---

## Voice Generation

Voices come from high-weight narratives. For each:

```typescript
function generateVoiceText(narrative: Narrative, context: SceneContext): string {
  // The voice speaks the narrative's emotional truth in this moment
  // Weighted by narrative.weight and relevance to current scene
}
```

**Voice characteristics:**
- Present tense or immediate relevance
- Short (one line)
- Emotional, not informational
- May contradict each other (tension!)

**Examples:**
- From narr_edmund_betrayal: "Three days to York. He's close now."
- From narr_aldric_thornwick: "He hasn't spoken since Thornwick."
- From narr_blood_brothers: "He's still your brother."

---

## Clickable Word Selection

Words should be clickable when:

1. **They're specific** — Names, places, concrete nouns
2. **They carry emotional weight** — "brother", "oath", "fire"
3. **They open threads** — Clicking reveals or deepens
4. **They're actionable** — Player could respond to them

Words should NOT be clickable when:
- They're generic ("the", "and", "very")
- Clicking would feel arbitrary
- There's no meaningful response

**Target:** 3-6 clickable words per narration block.

---

## Invention Guidelines

When the graph is sparse, invent. But invented content must:

1. **Fit the world** — Norman England, 1067
2. **Connect to existing** — Link to known characters, places
3. **Be persisted** — Output as mutations
4. **Create callbacks** — Plant seeds for later

**What to invent:**
- Character backstory details
- Family relationships
- Locations they've been
- Skills and traits
- Connections to player's history

**What NOT to invent:**
- Major plot points without setup
- Contradictions to established facts
- Genre-breaking elements

---

## Background Generation

When player is in scene N:
1. Serve scene N (already generated)
2. Background: generate scenes N+1, N+2 (likely next scenes)
3. As player clicks, extend current tree if needed

**Priority queue:**
1. Current scene extensions (player is clicking)
2. High-probability next scenes
3. Possible next scenes
4. Distant future scenes

---

## Quality Control

Before serving, scene trees should pass:

- [ ] All clickables have responses OR waitingMessage
- [ ] No dead ends (every path has exit or continuation)
- [ ] Character voices are consistent
- [ ] Clickable words make sense in context
- [ ] Invented content fits the world
- [ ] Emotional beats land properly

---

*"Talk first. Query as you speak. Invent when the graph is silent. The world grows through conversation."*

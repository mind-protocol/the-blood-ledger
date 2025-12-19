# World Runner — Behaviors: What It Produces

```
CREATED: 2024-12-16
UPDATED: 2024-12-16
STATUS: Canonical
```

---

## The Injection Interface

The Runner returns an Injection — the contract between Runner and Narrator:

```typescript
interface Injection {
  // Core: Was player interrupted?
  interrupted: boolean;

  // If interrupted (player-affecting flip happened)
  at_minute?: number;            // When during the action
  remaining?: number;            // Time left to complete
  event?: Event;                 // What happened (LLM-generated)

  // If completed (no interruption)
  completed?: boolean;
  time_elapsed?: number;         // Full duration

  // Always present
  world_changes: WorldChange[];  // What happened elsewhere
  news_available: News[];        // What player could hear on arrival
}
```

---

## Injection: Interrupted

When a flip affects the player, Runner stops immediately and returns:

```typescript
{
  interrupted: true,
  at_minute: 500,          // 8 hours 20 min into 2-day journey
  remaining: 2380,         // 39 hours 40 min left
  event: {
    type: "ambush",
    location: "place_road",
    description: "Bandits block the road ahead",
    characters: ["char_bandit_leader", "char_bandit_1", "char_bandit_2"],
    narrator_notes: "Three men. Armed with axes. One has a Norman sword."
  },
  world_changes: [
    { type: "tension_resolved", id: "tension_road_ambush" }
  ],
  news_available: []
}
```

**What Narrator does:** Writes the ambush scene. Player responds. When resolved, Narrator calls Runner again with `remaining: 2380` to continue.

---

## Injection as Markdown (Narrator Input)

The injection goes into the Narrator's context as **structured markdown** with full node details:

```markdown
# WORLD INJECTION
═════════════════

## Status: INTERRUPTED

**At minute:** 500 (8h 20m into journey)
**Remaining:** 2380 minutes (39h 40m)

---

## EVENT: Ambush on the Road

**Type:** ambush
**Location:** place_road_north

Three men block the road ahead. Armed. One carries a Norman sword.

---

## CLUSTER: Relevant Nodes

### Tension (Flipped)

**tension_road_ambush**
- pressure: 0.95 → FLIPPED
- breaking_point: 0.90
- narratives: [narr_bandit_territory, narr_road_danger]

### Narratives

**narr_bandit_territory**
- content: "Wulfric's band controls this stretch of road. They take what they want from travelers."
- type: claim
- truth: 0.9
- weight: 0.72
- about: place_road_north, char_wulfric

**narr_road_danger**
- content: "The northern road is dangerous since the Normans stopped patrolling."
- type: rumor
- truth: 0.8
- weight: 0.65

### Characters Present

**char_wulfric** (bandit leader)
- name: "Wulfric"
- traits: [ruthless, practical, saxon_loyalist]
- current_location: place_road_north
- beliefs:
  - narr_norman_oppression: heard=1.0, believes=1.0
  - narr_bandit_territory: heard=1.0, believes=1.0

**char_bandit_1**
- name: "Osric"
- traits: [nervous, young]
- current_location: place_road_north

**char_bandit_2**
- name: "Godwin"
- traits: [cruel, scarred]
- current_location: place_road_north

### Place

**place_road_north**
- name: "The Northern Road"
- description: "A muddy track through dense forest. Easy to ambush."
- region: place_york_region
- atmosphere: tense, isolated

### Player Party

**char_player** (you)
- current_location: place_road_north (traveling)
- destination: place_york

**char_aldric** (companion)
- current_location: place_road_north (with player)
- beliefs about bandits:
  - narr_road_danger: heard=0.8, believes=0.6
- traits: [loyal, cautious, skilled_fighter]

---

## WORLD CHANGES (Background)

- tension_road_ambush: RESOLVED (flipped)
- narr_ambush_encounter: CREATED

---

## NEWS AVAILABLE

(none yet — player was traveling)

---
```

**Why markdown:**
- Narrator is an LLM — reads markdown naturally
- Node names are explicit (char_wulfric, place_road_north)
- All fields present for scene writing
- Structured but readable

---

## Injection: Completed

When player action finishes without interruption:

```typescript
{
  interrupted: false,
  completed: true,
  time_elapsed: 2880,      // Full 2 days
  world_changes: [
    { type: "narrative_created", id: "narr_edmund_move", summary: "Edmund moved politically in York" },
    { type: "tension_resolved", id: "tension_confrontation" },
    { type: "tension_created", id: "tension_retaliation", pressure: 0.4 }
  ],
  news_available: [
    { summary: "Edmund's allies spoke against you in York", source: "travelers", reliability: 0.7 },
    { summary: "Norman patrol passed through yesterday", source: "innkeeper", reliability: 0.9 }
  ]
}
```

**As markdown for Narrator:**

```markdown
# WORLD INJECTION
═════════════════

## Status: COMPLETED

**Time elapsed:** 2880 minutes (2 days)
**Action completed:** Travel to York

---

## WORLD CHANGES (While You Traveled)

### Narratives Created

**narr_edmund_move**
- content: "Edmund's allies in York have begun spreading word that Rolf's claim to Thornwick is illegitimate."
- type: account
- truth: 0.3
- about: char_edmund, char_rolf, place_york

### Tensions Resolved

**tension_confrontation** → RESOLVED
- Edmund acted first, politically

### Tensions Created

**tension_retaliation**
- pressure: 0.4
- narratives: [narr_edmund_move, narr_rolf_oath]
- description: "Rolf will not accept Edmund's attack quietly"

---

## NEWS AVAILABLE

| Summary | Source | Reliability |
|---------|--------|-------------|
| "Edmund's allies spoke against you in York" | travelers | 0.7 |
| "Norman patrol passed through yesterday" | innkeeper | 0.9 |

---

## ARRIVAL: York

**place_york**
- name: "York"
- description: "The great northern city. Norman banners fly from the walls."
- atmosphere: tense, watchful
- modifiers: [politically_charged]

---
```

**What Narrator does:** Writes arrival scene. Weaves in news naturally. Uses world_changes to inform what's different.

---

## Injection Queue (In-Scene Events)

Beyond interrupts, the Runner can push events to `injection_queue.json` for the Narrator to weave in.

**Use case:** A character in the current scene wants to say or do something — not urgent enough to interrupt, but should happen.

```json
// playthroughs/{id}/injection_queue.json
[
  {
    "type": "character_action",
    "character": "char_aldric",
    "action": "speaks",
    "content": "Aldric clears his throat. 'We should make camp soon. The light is failing.'",
    "urgency": "low",
    "trigger": "time_elapsed > 4 hours without rest"
  },
  {
    "type": "character_reaction",
    "character": "char_mildred",
    "action": "reacts",
    "content": "Mildred's hand moves to her knife when she hears the sound in the trees.",
    "urgency": "medium",
    "trigger": "tension_ambush.pressure > 0.7"
  }
]
```

**Flow:**
1. Runner detects condition (time, tension threshold, proximity)
2. Runner appends to `injection_queue.json`
3. Narrator reads queue before generating response
4. Narrator weaves in naturally, clears processed items

**Not an interrupt** — the scene continues. But the character acts within it.

```markdown
## INJECTION QUEUE

**char_aldric** wants to speak:
> "We should make camp soon. The light is failing."
- trigger: 4+ hours without rest
- urgency: low

**char_mildred** reacts:
> Mildred's hand moves to her knife when she hears the sound.
- trigger: tension_ambush.pressure > 0.7
- urgency: medium
```

---

## Event (For Interrupts)

When a player-affecting flip happens, Runner generates an Event:

```typescript
interface Event {
  type: EventType;
  location: string;              // Place ID
  description: string;           // What's happening
  characters: string[];          // Who's involved
  narrator_notes?: string;       // Guidance for scene writing
}

type EventType =
  | 'ambush'      // Combat encounter
  | 'encounter'   // Non-combat meeting
  | 'discovery'   // Player finds something
  | 'arrival'     // Someone arrives
  | 'message'     // News reaches player
  | 'event'       // Something happens nearby
```

**Example Event:**

```typescript
{
  type: "encounter",
  location: "place_road",
  description: "A wounded man staggers from the treeline",
  characters: ["char_wounded_saxon"],
  narrator_notes: "He's been attacked by the same bandits. Could warn player or ask for help."
}
```

---

## WorldChange (For Background Events)

Things that happened but didn't interrupt:

```typescript
interface WorldChange {
  type: WorldChangeType;
  id: string;                    // Node ID
  summary?: string;              // Brief description
  pressure?: number;             // For tensions
}

type WorldChangeType =
  | 'narrative_created'
  | 'narrative_updated'
  | 'tension_created'
  | 'tension_resolved'
  | 'tension_pressure_changed'
  | 'character_moved'
  | 'belief_changed'
```

**The Narrator uses these to:**
- Know what happened while player was busy
- Inform scene descriptions ("York feels tense")
- Prepare for player questions ("What happened while I was traveling?")

---

## News (What Player Could Hear)

Information available at destination or from NPCs:

```typescript
interface News {
  summary: string;               // What happened (player-facing)
  narrative_id?: string;         // Link to graph narrative
  source: string;                // "travelers", "innkeeper", "messenger"
  reliability: number;           // 0-1, how accurate
  location_heard?: string;       // Where player could hear this
}
```

**Narrator decides when to reveal news:**
- Player arrives at destination → check news_available
- Player talks to NPC → NPC might mention news
- Player asks "What's happening?" → surface relevant news

---

## Time Estimates (for Narrator)

When Narrator decides to call Runner, use these estimates:

| Action | max_minutes |
|--------|-------------|
| Brief conversation | 5-15 |
| Deep conversation | 20-60 |
| Search a location | 30-120 |
| Make camp / rest | 240-480 |
| Rest overnight | 480-600 |
| Travel (nearby) | 60-240 |
| Travel (regional) | 480-1440 |
| Travel (distant) | 1440-4320 |

---

## Graph Mutations (Applied During Run)

The Runner applies changes to the graph as it runs:

```typescript
interface GraphMutations {
  new_narratives: NewNarrative[];
  new_beliefs: NewBelief[];
  tension_updates: TensionUpdate[];
  new_tensions: NewTension[];
  character_movements: CharacterMovement[];
}
```

These are applied during the tick loop, NOT returned. By the time Injection comes back, mutations are already in the graph.

---

## Output by Duration

### Short (5-60 minutes)

```typescript
// Player searches the ruins for an hour
{
  interrupted: false,
  completed: true,
  time_elapsed: 60,
  world_changes: [],              // Nothing major in an hour
  news_available: []
}
```

Likely outcome: No interruption, minimal world changes. The world ticks but nothing breaks.

### Medium (hours)

```typescript
// Player rests overnight (8 hours)
{
  interrupted: false,
  completed: true,
  time_elapsed: 480,
  world_changes: [
    { type: "tension_pressure_changed", id: "tension_ambush", pressure: 0.72 }
  ],
  news_available: [
    { summary: "Patrol passed in the night", source: "companion" }
  ]
}
```

Likely outcome: Tension builds. Maybe minor news. Interruption possible but not common.

### Long (days)

```typescript
// Player travels 2 days to York
{
  interrupted: true,
  at_minute: 500,
  remaining: 2380,
  event: {
    type: "ambush",
    location: "place_road",
    description: "Bandits block the road"
  },
  world_changes: [...],
  news_available: [...]
}
```

Likely outcome: Interruption likely. Multiple world changes. News accumulates.

### Very Long (weeks)

```typescript
// Player waits a week for reinforcements
{
  interrupted: true,             // Almost certainly interrupted
  at_minute: 4320,               // 3 days in
  remaining: 5760,
  event: {...},
  world_changes: [
    // Many events
    { type: "narrative_created", id: "narr_feud_breaks" },
    { type: "tension_resolved", id: "tension_feud" },
    { type: "tension_created", id: "tension_war" },
    ...
  ],
  news_available: [
    // Major news
    { summary: "The feud has become open war" },
    { summary: "York prepares for siege" }
  ]
}
```

Likely outcome: Multiple interruptions likely. World transforms significantly.

---

## The Resume Pattern

When Narrator receives an interrupted Injection:

```
1. Narrator writes the interrupt scene
   "Bandits block the road ahead. Three men with axes."

2. Player responds / resolves encounter
   "I negotiate. / I fight. / I flee."

3. Narrator resolves, then calls Runner again:
   run_world(
     action: "continue_travel",
     max_minutes: injection.remaining,  // 2380
     player_context: updated_context
   )

4. Runner continues until next interrupt or completion
```

**The Narrator tracks remaining time.** Runner just runs from current state.

---

*"Runner runs the world. Narrator tells the story. Injection is how they communicate."*

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

## CHAIN

PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service.md
TEST:            ./TEST_World_Runner_Coverage.md
SYNC:            ./SYNC_World_Runner.md

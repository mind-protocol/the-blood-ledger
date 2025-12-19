# Narrator Input Reference

What the Narrator receives from the Orchestrator.

---

## Script Locations

```
engine/infrastructure/orchestration/narrator.py  # Narrator caller + prompt builder
engine/models/                                   # Pydantic models for validation
```

---

## Prompt Structure

```
NARRATOR INSTRUCTION
════════════════════

{SCENE_CONTEXT}

{WORLD_INJECTION if flips occurred}

{GENERATION_INSTRUCTION}

Output JSON matching the schema. Include time_elapsed estimate.
```

---

## Scene Context (Always Provided)

```typescript
interface SceneContext {
  location: LocationContext;
  time: TimeContext;
  present: CharacterBrief[];
  active_narratives: ActiveNarrative[];
  tensions: TensionBrief[];
  player_state: PlayerState;
}

interface LocationContext {
  id: string;                   // e.g., "place_camp"
  name: string;                 // e.g., "The Camp"
  type: PlaceType;              // From schema
  atmosphere: {
    weather: string[];          // e.g., ["cold", "clear"]
    mood: string;               // e.g., "watchful"
    details: string[];          // e.g., ["fire burning low"]
  };
}

interface TimeContext {
  time_of_day: string;          // "dawn", "morning", "afternoon", "evening", "night"
  day: number;                  // Day number since game start
  season?: string;              // "winter", "spring", etc.
}

interface CharacterBrief {
  id: string;                   // e.g., "char_aldric"
  name: string;                 // e.g., "Aldric"
  brief: string;                // e.g., "Your companion. Terse, loyal, haunted."
  modifiers?: string[];         // Active modifiers, e.g., ["wounded"]
}

interface ActiveNarrative {
  id: string;                   // e.g., "narr_oath"
  weight: number;               // 0-1, sorted by weight
  summary: string;              // e.g., "You swore to find Edmund"
  type: string;                 // From schema
  tone?: string;                // Emotional color
}

interface TensionBrief {
  id: string;                   // e.g., "tension_confrontation"
  description: string;          // e.g., "Edmund draws closer"
  pressure: number;             // 0-1
  breaking_point: number;       // Usually 0.9
}

interface PlayerState {
  pursuing: string;             // Current objective
  recent: string;               // What just happened
  modifiers?: string[];         // Active modifiers
}
```

---

## World Injection (If Flips Occurred)

Provided when World Runner has processed flips since last scene.

```typescript
interface WorldInjection {
  time_since_last: string;      // Time span processed
  breaks: Break[];              // What broke and how
  news_arrived?: NewsItem[];    // News that reached player
  tension_changes?: Record<string, string>;
  interruption?: Interruption | null;
  atmosphere_shift?: string;
  narrator_notes?: string;
}

interface Break {
  tension_id: string;
  narrative: string;
  event: string;
  location: string;
  player_awareness: 'witnessed' | 'encountered' | 'heard' | 'will_hear' | 'unknown';
  witnesses?: string[];
}

interface NewsItem {
  narrative: string;
  summary: string;
  source: string;
  reliability: number;
}

interface Interruption {
  type: 'arrival' | 'message' | 'event';
  character?: string;
  event?: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  description: string;
}
```

---

## Complete Example Input

```yaml
NARRATOR INSTRUCTION
════════════════════

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
  null  # No flips since last scene

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

---

## Handling World Injection

When `world_injection` is present:

| Player Awareness | How to Handle |
|------------------|---------------|
| `witnessed` | Weave directly into narration - player saw it happen |
| `encountered` | Player will see aftermath - describe changed scene |
| `heard` | Deliver via character speech or messenger |
| `will_hear` | Note for when player reaches destination |
| `unknown` | Don't reveal yet |

### Interruption Handling

| Urgency | Response |
|---------|----------|
| `low` | Can wait - mention later in scene |
| `medium` | Should address soon - character notices |
| `high` | Interrupts current moment |
| `critical` | Scene break - this takes over |

---

## Query Patterns

Before generating, Narrator may query the graph for:

1. **New narratives since last scene**
   ```
   What narratives were created in the last {time_elapsed}?
   ```

2. **Character movements**
   ```
   Who has arrived at {location}?
   Who has left?
   ```

3. **Tension states**
   ```
   What tensions involve present characters?
   What's closest to breaking?
   ```

4. **Character details**
   ```
   What does {character} believe about {narrative}?
   What's {character}'s backstory.wound?
   ```

5. **Recent breaks**
   ```
   What tensions broke in the last {time_span}?
   ```

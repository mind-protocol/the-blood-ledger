# World Runner Input Reference

What the World Runner receives from the Orchestrator.

---

## Script Location

```
engine/infrastructure/orchestration/world_runner.py  # World Runner caller
engine/models/                                        # Pydantic models for validation
```

---

## Prompt Structure

```
WORLD RUNNER INSTRUCTION
════════════════════════

You process flips detected by the graph tick.

{FLIP_CONTEXT}

{GRAPH_CONTEXT}

{PLAYER_CONTEXT}

Determine what happened. Output JSON matching WorldRunnerOutput schema.
```

---

## Flip Context (Why You're Called)

```typescript
interface FlipContext {
  time_span: string;            // Duration processed, e.g., "2 days"
  flips: Flip[];                // Tensions that crossed breaking_point
}

interface Flip {
  tension_id: string;           // e.g., "tension_confrontation"
  pressure: number;             // Current pressure (>= breaking_point)
  breaking_point: number;       // Usually 0.9
  trigger_reason: string;       // Why it flipped
  narratives: string[];         // Narrative IDs in tension
  involved_characters: string[]; // Character IDs involved
  location: string;             // Place ID where it's centered
}
```

---

## Graph Context (What You Need to Know)

```typescript
interface GraphContext {
  relevant_narratives: NarrativeDetail[];
  character_locations: Record<string, string>;
  character_beliefs: Record<string, Record<string, BeliefState>>;
}

interface NarrativeDetail {
  id: string;
  name: string;
  content: string;
  type: string;
  weight: number;
  tone?: string;
  truth?: number;               // Director-only
  believers: string[];          // Character IDs who believe
  about: {
    characters?: string[];
    places?: string[];
    things?: string[];
  };
}

interface BeliefState {
  heard: number;                // 0-1
  believes: number;             // 0-1
  doubts?: number;              // 0-1
  denies?: number;              // 0-1
}
```

---

## Player Context (Where Player Is)

```typescript
interface PlayerContext {
  location: string;             // Place ID
  engaged_with?: string;        // Character ID player is talking to
  traveling_to?: string;        // Destination if traveling
  recent_action?: string;       // What player just did
}
```

---

## Complete Example Input

```yaml
WORLD RUNNER INSTRUCTION
════════════════════════

You process flips detected by the graph tick.

TIME_SPAN: 2 days

FLIPS:
  - tension_id: tension_confrontation
    pressure: 0.95
    breaking_point: 0.90
    trigger_reason: "Pressure accumulated over 2 days of travel. Rolf approaches York where Edmund is."
    narratives:
      - narr_edmund_betrayal
      - narr_rolf_oath
    involved_characters:
      - char_edmund
      - char_rolf
    location: place_york

GRAPH_CONTEXT:

  relevant_narratives:
    - id: narr_edmund_betrayal
      name: "Edmund's Betrayal"
      content: "Edmund stole Thornwick, forged documents, left Rolf to burn. Or so Rolf believes."
      type: enmity
      weight: 0.85
      tone: bitter
      truth: 0.6  # Truth is complicated
      believers: [char_rolf, char_aldric]
      about:
        characters: [char_edmund, char_rolf]
        places: [place_thornwick]
        things: [thing_thornwick_deed]

    - id: narr_rolf_oath
      name: "Rolf's Oath"
      content: "I swore to reclaim what Edmund took. To make him answer for Thornwick."
      type: oath
      weight: 0.78
      tone: cold
      truth: 1.0  # He did swear this
      believers: [char_rolf, char_aldric]
      about:
        characters: [char_rolf, char_edmund]

    - id: narr_edmund_defense
      name: "Edmund's Version"
      content: "Father meant Thornwick for me alone. The fire was Norman raiders, not me."
      type: belief
      weight: 0.4
      tone: defiant
      truth: 0.4  # Partly true
      believers: [char_edmund]
      about:
        characters: [char_edmund, char_rolf]

  character_locations:
    char_edmund: place_york
    char_rolf: place_road_to_york
    char_aldric: place_road_to_york
    char_wulfstan: place_york
    char_gospatric: place_york

  character_beliefs:
    char_rolf:
      narr_edmund_betrayal: { heard: 1.0, believes: 1.0 }
      narr_rolf_oath: { heard: 1.0, believes: 1.0 }
      narr_edmund_defense: { heard: 0.3, believes: 0.0, denies: 0.9 }

    char_edmund:
      narr_edmund_betrayal: { heard: 0.5, believes: 0.0, denies: 1.0 }
      narr_rolf_oath: { heard: 0.8, believes: 0.9 }
      narr_edmund_defense: { heard: 1.0, believes: 1.0 }

    char_aldric:
      narr_edmund_betrayal: { heard: 1.0, believes: 0.7, doubts: 0.3 }
      narr_rolf_oath: { heard: 1.0, believes: 1.0 }

PLAYER_CONTEXT:
  location: place_road_to_york
  engaged_with: char_aldric
  traveling_to: place_york
  recent_action: "Camping for the night, one day from York"

Determine what happened during this time span.
Consider:
- Edmund knows Rolf is coming (rumors travel)
- Edmund has allies in York
- What would Edmund do with a day's warning?

Output JSON matching WorldRunnerOutput schema.
```

---

## Processing Guidance

### What Caused the Flip?

| Flip Pattern | What to Consider |
|--------------|------------------|
| **Contradicting beliefs under pressure** | Believers in opposing narratives were forced together |
| **Oath at moment of truth** | Oath conditions became present |
| **Debt beyond tolerance** | Debt unresolved too long |
| **Secret under exposure** | Knower and subject in same location |
| **Power vacuum collapsing** | Multiple claims + claimants converging |

### Scale to Time Span

| Duration | What Can Happen |
|----------|-----------------|
| Minutes | Almost nothing changes |
| Hours | Local tensions might break |
| A day | Regional events possible, news travels |
| Days | Multiple breaks, cascades likely |
| Weeks | World transforms significantly |

### Cascade Check

After determining the break, check if it destabilizes other tensions:
- New contradictions created?
- Proximity changes that increase pressure?
- Belief changes that create conflicts?

Report cascades for the engine to process.

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

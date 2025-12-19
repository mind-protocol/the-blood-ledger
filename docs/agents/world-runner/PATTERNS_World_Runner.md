# World Runner — Patterns: Why This Shape

```
CREATED: 2024-12-16
UPDATED: 2024-12-16
STATUS: Canonical
```

---

## The Core Insight

**The Runner owns time. The Narrator owns story.**

When the player decides to travel to York, the Narrator hands control to the Runner: "Run the world for 2 days." The Runner simulates those 2 days tick by tick — until something happens to the player, or the journey completes.

The Narrator authors what the player experiences. The Runner authors what happens.

---

## The Interrupt/Resume Pattern

```
NARRATOR                              RUNNER
   │                                     │
   │ "Travel to York" (2 days)           │
   │─────────────────────────────────────►
   │                                     │ runs tick loop...
   │                                     │ tick 1, tick 2, ...
   │                                     │ tick 100: FLIP affects player
   │         Injection (interrupted)     │
   │◄─────────────────────────────────────
   │                                     │
   │ writes ambush scene                 │
   │ player resolves encounter           │
   │                                     │
   │ "Continue to York" (remaining time) │
   │─────────────────────────────────────►
   │                                     │ resumes tick loop...
   │                                     │ completes
   │         Injection (completed)       │
   │◄─────────────────────────────────────
   │                                     │
   │ writes arrival scene                │
   ▼                                     ▼
```

**Key pattern:** Runner runs until interrupted OR completed. Narrator handles the interruption, then resumes.

They're separate because they're different skills:
- Narrator: Creative authorship, voice, atmosphere
- World Runner: Tick loop, tension tracking, interrupt detection

---

## Stateless vs Persistent

**Narrator: Persistent (--continue)**
- Single conversation thread
- Remembers what it authored
- Creative continuity matters
- Foreshadowing, callbacks, voice consistency

**World Runner: Stateless**
- Each call is independent
- Runs tick loop from current graph state
- Returns Injection + applies graph mutations
- No memory needed — the graph IS the memory

```
Runner call:
  Input:
    - action: "travel_to_york"
    - max_minutes: 2880
    - player_context: {location, path, companions}

  Output:
    - Injection: interrupted? at_minute? event? world_changes? news?
    - Graph mutations applied during run

Next call reads updated graph.
Resume pattern handled by Narrator, not Runner.
```

---

## Why Separation Matters

### Focus

The Narrator can focus on the moment — this conversation, this character, this emotion. It doesn't track what's happening in Durham or how many minutes have passed.

### The World Keeps Moving

Multiple storylines advance at once. The feud doesn't pause for the player's journey. The rebellion continues. News travels. All of this happens inside the Runner's tick loop.

### Coherence

When things happen offscreen, they're consistent. The Runner applies the same tension-break logic everywhere. No special rules for what the player can't see.

### Clean Interrupts

When something happens TO the player (not just near them), the Runner stops and hands back control. The Narrator writes that moment, player responds, then Runner resumes.

---

## When Does Runner Run?

**Runner runs when the player does something that takes time.**

| Player Action | Runner Called? | max_minutes |
|---------------|----------------|-------------|
| Say one line | No | — |
| Conversation (5+ min) | Maybe | 5-30 |
| Search a room | Yes | 30-120 |
| Rest for the night | Yes | 480 |
| Travel to York | Yes | 2880 |

The Narrator decides when to invoke the Runner. Rule of thumb: if action takes < 5 minutes, don't bother. If it takes hours or days, definitely run.

---

## What The World Runner Is NOT

### Not A Simulation

It doesn't tick every entity every minute. It processes what matters — narratives under tension, approaching deadlines, traveling news.

### Not Random Events

There's no "40% chance of bandit attack." Events emerge from narrative tension. If there's no tension about bandits, no bandits appear.

### Not A Time System

Time is a trigger, not a simulation. "3 days passed" means "check what could have broken in 3 days," not "simulate 4,320 minutes."

### Not The Narrator's Boss

The injection is information, not instruction. The Narrator decides how to weave it in, what to emphasize, when to reveal.

---

## The Injection Contract

The Runner returns an Injection — structured data the Narrator uses:

```typescript
interface Injection {
  interrupted: boolean;

  // If interrupted
  at_minute?: number;           // When it happened
  remaining?: number;           // Time left
  event?: Event;                // What happened (for Narrator to write)

  // If completed
  completed?: boolean;
  time_elapsed?: number;

  // Always present
  world_changes: WorldChange[]; // What happened elsewhere
  news_available: News[];       // What player could hear
}
```

**Interrupted:** Runner hit a player-affecting flip. Narrator writes the scene. After player resolves it, Narrator calls Runner again with `remaining` time.

**Completed:** Runner finished the full duration. Narrator can summarize the journey, reveal news, write arrival.

---

## Urgency Becomes Real

Because the World Runner tracks time:

- **Deadlines matter.** "Three days to York" means something.
- **Waiting has cost.** Stay too long at camp, Edmund gets further ahead.
- **Rushing has risk.** Push through without rest, arrive exhausted.
- **The world reacts.** Long absence means things changed in your absence.

---

## Connection to Energy/Weight

The World Runner operates on the same narrative web as the Narrator:

- **High-weight narratives** are checked for breaks
- **Tensions** (contradictions with believers nearby) might resolve
- **Focus** affects how quickly tensions build
- **Breaks** create new narratives, redistribute weight

The World Runner is the engine's way of saying: "Given this configuration and this time, what would happen?"

---

## The Player Experience

The player doesn't see the Runner. They see:

- "Bandits block the road ahead" — interrupted mid-journey
- Arriving in York to hear "Edmund moved against you yesterday"
- The ferryman mentions news from Durham
- Consequences of their timing choices

The machinery is hidden. The world feels alive. Time feels real.

---

## The Critical Function: affects_player()

What makes a flip interrupt vs background?

```python
def affects_player(flip, player_context):
    # Spatial: Is the flip at player's current location?
    if flip.location == player_location_at_tick(player_context):
        return True

    # Direct: Does the flip involve the player?
    if "char_player" in flip.involved_characters:
        return True

    # Companion: Does it involve someone WITH the player?
    if flip.involves(player_context.companions):
        return True

    # Critical urgency reaching player's area?
    if flip.urgency == "critical" and nearby(flip.location, player):
        return True

    return False
```

**Key distinction:**
- Edmund makes a political move in York → world_changes (player hears later)
- Bandits attack player on the road → INTERRUPT (player must respond now)

---

*"The Runner runs the world. The Narrator tells the story. They meet at Injections."*

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

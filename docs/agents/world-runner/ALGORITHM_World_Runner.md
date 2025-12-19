# World Runner — Algorithm: How It Works

```
CREATED: 2024-12-16
UPDATED: 2024-12-16
STATUS: Canonical
```

---

## Core Principle: Runner Owns the Tick Loop

**The Runner doesn't just process a time span — it runs the world.**

```python
def run_world(action: str, max_minutes: int, player_context: PlayerContext) -> Injection:
    tick = 0
    minutes_elapsed = 0

    while minutes_elapsed < max_minutes:
        # Run one graph tick (5 min)
        run_graph_tick()
        minutes_elapsed += 5
        tick += 1

        # Check for flips
        flips = check_thresholds()

        for flip in flips:
            if affects_player(flip, player_context):
                # Interrupt — something happened TO THE PLAYER
                return Injection(
                    interrupted=True,
                    at_minute=minutes_elapsed,
                    remaining=max_minutes - minutes_elapsed,
                    event=process_flip(flip)  # LLM generates what happened
                )

        # Process non-player flips (world keeps moving)
        for flip in flips:
            process_flip(flip)  # Creates narratives, but no injection

    # Completed without interruption
    return Injection(
        interrupted=False,
        completed=True,
        time_elapsed=max_minutes
    )
```

**Key insight:** The Runner runs until either:
1. A flip affects the player → INTERRUPT, return immediately
2. Time runs out → COMPLETE, return summary

---

## Graph Ticks vs Narrative Flips

**Graph ticks are mechanical. Narrative flips are story.**

- Graph ticks: math-only updates (no LLM), run every 5 minutes of world time.
- Narrative flips: reasoning about what happens when tension breaks (LLM).

```typescript
function graphTick(graph: Graph, time_elapsed: Duration): TickResult {
  for (const tension of graph.tensions) {
    tension.pressure += time_elapsed * tension.base_rate * tension.focus;
  }

  for (const narrative of graph.narratives) {
    narrative.weight = computeWeight(narrative, graph);
  }

  for (const narrative of graph.narratives) {
    if (distanceFromPlayer(narrative, graph) > threshold) {
      narrative.weight *= decay_factor;
    }
  }

  const flips = graph.tensions.filter(t => t.pressure > t.breaking_point);
  return { flips };
}
```

```typescript
interface FlipRequest {
  tension: Tension;
  graph_context: GraphSnapshot;
  trigger_reason: string;
}

interface FlipResult {
  event: string;
  new_narratives: Narrative[];
  belief_changes: BeliefChange[];
  cascades: FlipRequest[];
}
```

**Tick frequency:** if `time_elapsed < 5 min` → no tick. If `time_elapsed ≥ 5 min` → tick. Only call the Runner when flips are detected.

---

## The Full Flow

```
Narrator: "You travel to York. Two days on foot."
    │
    └── Calls Runner:
          action: "travel_to_york"
          max_minutes: 2880  # 2 days
          player_path: [place_camp → place_road → place_york]
    │
    ▼
Runner runs tick loop...
    tick 1: nothing
    tick 2: nothing
    ...
    tick 100: tension_ambush flips, player on road
    │
    └── INTERRUPT
            │
            ▼
        Injection:
          interrupted: True
          at_minute: 500
          remaining: 2380
          event: "Bandits block the road ahead"
    │
    ▼
Narrator receives injection, writes scene
    │
    ▼
After scene resolves, Narrator calls Runner again:
    action: "continue_travel"
    max_minutes: 2380  # Remaining time
```

---

## The Trigger

```
Narrator says something takes time:
  - "You travel to York" → max_minutes: 2880
  - "You rest for the night" → max_minutes: 480
  - "You search the ruins" → max_minutes: 120
  - "You wait until dawn" → max_minutes: variable

Runner is called with:
  - action: what player is doing
  - max_minutes: how long it should take
  - player_context: location, path, engagement
```

---

## Player Context

The Runner needs to know where the player is — and where they'll be:

```typescript
interface PlayerContext {
  location: string;           // Current place ID
  path?: string[];            // For travel: [start, ..., destination]
  engaged_with?: string;      // Character ID if in conversation
  action: string;             // What player is doing
}
```

**Path awareness is critical.** When player travels:
- Runner knows the path: `[place_camp → place_road → place_york]`
- Can calculate where player is at any given tick
- Flip on `place_road` at tick 100? Check if player is there yet.

```python
def player_location_at_tick(player_context: PlayerContext, tick: int) -> str:
    if not player_context.path:
        return player_context.location

    # Calculate position along path based on tick
    progress = tick * 5 / total_travel_minutes
    index = int(progress * (len(player_context.path) - 1))
    return player_context.path[min(index, len(player_context.path) - 1)]
```

---

## affects_player() — The Load-Bearing Function

When a flip happens, does it interrupt the player?

```python
def affects_player(flip: Flip, player_context: PlayerContext) -> bool:
    player_loc = player_location_at_tick(player_context, current_tick)

    # Spatial: flip at player's current location?
    if flip.location == player_loc:
        return True

    # Direct: flip involves player character?
    if "char_player" in flip.involved_characters:
        return True

    # Companion: flip involves someone traveling with player?
    if any(c in player_context.companions for c in flip.involved_characters):
        return True

    # High-stakes: flip is critical enough to reach player?
    if flip.urgency == "critical" and nearby(flip.location, player_loc):
        return True

    return False
```

**Key distinction:**
- Aldric gets ambushed 50 miles away → flip happens, but NO interrupt (player doesn't see it)
- Aldric gets ambushed while traveling with player → INTERRUPT

---

## Stateless Between Calls

The Runner itself is stateless — each call is independent:

```
INPUT
├── action: what player is doing
├── max_minutes: how long
├── player_context: location, path, companions
└── graph state: read from DB

OUTPUT
├── Injection (interrupted? event? remaining time?)
└── Graph mutations (applied to DB)

NEXT CALL
├── Fresh instance
├── Reads updated graph
└── No memory of previous calls needed
```

**The graph IS the memory.** Flip processed → graph mutated → next call sees new state.

---

## Graph Ticks vs Narrative Flips

**Graph ticks are mechanical.** Math-only updates every 5 minutes or more.

**Narrative flips are story.** LLM reasoning only when a tension breaks.

```
graph_tick:
  trigger: time_elapsed >= 5 minutes
  does:
    - tension.pressure += time * base_rate * focus
    - narrative.weight = compute_weight(...)
    - decay distant narratives
  llm: no

narrative_flip:
  trigger:
    - tension.pressure > breaking_point
    - OR contradiction/oath/secret/power-vacuum breaks
  does:
    - determine what happens
    - spawn narratives, belief changes, cascades
  llm: yes
```

**Flow:** Tick → detect flips → run Runner only for flips.

---

## Step 1: Energy Flow

For the given time duration, energy flows through the graph:

```
For each high-weight narrative:
  1. Support flows: A supports B → weight flows A→B
  2. Elaboration flows: A elaborates B → weight flows both ways
  3. Contradiction amplifies: A contradicts B → both gain pressure
  4. Belief intensity: strong beliefs pump energy
  5. Distance decay: far from player → weight decays
```

**Time scaling:**
- Minutes: minimal flow
- Hours: noticeable shifts
- Days: significant redistribution
- Weeks: major reconfigurations

---

## Step 2: Identify Breaks

Check all high-tension narratives for break conditions:

```
For each narrative N with weight > threshold:

  Check: Contradiction under pressure?
    - Does N contradict another narrative M?
    - Are believers in N and M in proximity?
    - Has pressure accumulated beyond tolerance?

  Check: Oath at moment of truth?
    - Is N an oath type?
    - Are the oath's conditions now satisfied?
    - Is the swearer in position to act/fail?

  Check: Debt beyond tolerance?
    - Is N a debt type?
    - How long has it been unresolved?
    - Is creditor patience exhausted?

  Check: Secret under exposure?
    - Is N a secret?
    - Are knower and subject in same location?
    - Is there pressure to reveal?

  Check: Power vacuum collapsing?
    - Does N involve control/authority?
    - Are multiple claims active?
    - Are claimants in conflict proximity?

If any check true → N must break
```

---

## Step 3: Process Breaks

For each narrative that must break:

```
1. Generate the break event
   - What specifically happens?
   - Where does it happen?
   - Who witnesses it?

2. Create spawned narratives
   - New narratives that result
   - With connections to source
   - With initial belief states

3. Update beliefs
   - Who learns about this?
   - How does their certainty change?
   - Does anyone's belief flip?

4. Check for cascades
   - Does this break create new unsustainable tensions?
   - If yes → those narratives also break
   - Process recursively until stable

5. Record for injection
   - Add to breaks list
   - Note player awareness level
```

---

## Step 4: Cascade Resolution

Breaks can trigger other breaks:

```
Queue = [initial breaks]
Processed = []
All_breaks = []

While Queue not empty:
  break = Queue.pop()

  If break in Processed:
    continue

  Process break
  All_breaks.add(break)
  Processed.add(break.narrative)

  # Check if break created new unstable tensions
  For each new_narrative created by break:
    If new_narrative now unsustainable:
      Queue.add(new_narrative)

  # Check if belief changes destabilized anything
  For each belief_change in break:
    For each narrative that believer holds:
      If now unsustainable:
        Queue.add(narrative)

Return All_breaks
```

---

## Step 5: News Propagation

After breaks are processed:

```
For each break:
  origin = break.location
  significance = break.weight

  # Calculate spread distance based on time and significance
  spread_distance = time_passed * significance * infrastructure_factor

  For each location within spread_distance:
    # News may mutate as it travels
    mutation_chance = distance / spread_distance

    If random() < mutation_chance:
      news = mutate(break.event)
    Else:
      news = break.event

    # Characters at location may hear
    For each character at location:
      If character.information_access >= threshold:
        Update character.heard(break.narrative)
```

---

## Step 6: Build and Return Injection

The Runner returns structured data the Narrator uses:

```typescript
interface Injection {
  // Interrupt status
  interrupted: boolean;

  // If interrupted (player-affecting flip happened)
  at_minute?: number;        // When during the action
  remaining?: number;        // Time left to complete action
  event?: Event;             // What happened (LLM-generated)

  // If completed (no interruption)
  completed?: boolean;
  time_elapsed?: number;

  // Always present
  world_changes: WorldChange[];  // What happened elsewhere
  news_available: News[];        // What player could hear on arrival
}
```

### Interrupted Injection

```typescript
// Player traveling to York, ambushed on the road
{
  interrupted: true,
  at_minute: 500,
  remaining: 2380,
  event: {
    type: "ambush",
    description: "Bandits block the road ahead",
    location: "place_road",
    characters: ["char_bandit_leader"],
    narrator_notes: "Three men, armed, blocking the path"
  },
  world_changes: [
    { type: "tension_resolved", id: "tension_ambush" },
    { type: "narrative_created", id: "narr_road_ambush" }
  ],
  news_available: []
}
```

### Completed Injection

```typescript
// Player rested for the night, nothing happened to them
{
  interrupted: false,
  completed: true,
  time_elapsed: 480,
  world_changes: [
    { type: "narrative_created", id: "narr_edmund_move" },
    { type: "tension_resolved", id: "tension_confrontation" }
  ],
  news_available: [
    { summary: "Edmund's allies moved in York", source: "travelers" }
  ]
}
```

---

## Time Scale: Tick Count

The Runner runs in 5-minute ticks:

| Duration | Ticks | What Happens |
|----------|-------|--------------|
| 30 min | 6 | Few checks, fast |
| 4 hours | 48 | Local tensions might break |
| 1 day | 288 | Multiple checks, breaks likely |
| 2 days | 576 | Many ticks, cascades expected |
| 1 week | 2016 | Major world changes possible |

**Performance consideration:** Long durations = many ticks. May need batching or acceleration for week+ spans.

---

## Player Intersection Detection

```
For each break or news item:

  Witnessed?
    break.location == player.location

  Encountered?
    break.location on player.travel_path
    AND time_of_break overlaps player.travel_time

  Heard?
    news.reached.includes(player.location)
    OR news.reached.includes(player.destination)

  Will hear?
    news.will_reach.includes(player.destination)
    AND player.arrival_time > news.arrival_time

  Unknown?
    None of the above
```

---

## Implementation Architecture

### The Tick Loop (Python)

```python
class WorldRunner:
    def __init__(self, graph: GraphTick):
        self.graph = graph

    def run(
        self,
        action: str,
        max_minutes: int,
        player_context: PlayerContext
    ) -> Injection:
        """Run the world until player is interrupted or time expires."""
        tick = 0
        minutes = 0
        world_changes = []
        news = []

        while minutes < max_minutes:
            # 1. Run graph tick (mechanical, no LLM)
            result = self.graph.run(
                elapsed_minutes=5,
                player_id=player_context.player_id,
                player_location=self._player_loc_at(player_context, minutes)
            )
            minutes += 5
            tick += 1

            # 2. Check for player-affecting flips
            for flip in result.flips:
                if self._affects_player(flip, player_context, minutes):
                    # INTERRUPT - call LLM to generate event
                    event = self._process_flip_for_player(flip)
                    return Injection(
                        interrupted=True,
                        at_minute=minutes,
                        remaining=max_minutes - minutes,
                        event=event,
                        world_changes=world_changes,
                        news_available=news
                    )

            # 3. Process non-player flips (world moves)
            for flip in result.flips:
                changes = self._process_flip_background(flip)
                world_changes.extend(changes)

            # 4. Propagate news
            news.extend(self._propagate_news(minutes))

        # Completed without interruption
        return Injection(
            interrupted=False,
            completed=True,
            time_elapsed=max_minutes,
            world_changes=world_changes,
            news_available=news
        )
```

### LLM Only for Events

```
Graph Tick (run_graph_tick):
  - Pure math, no LLM
  - Fast (milliseconds)
  - Runs every 5 minutes of game time

Flip Processing (process_flip):
  - LLM required
  - Only when flip detected
  - Generates: event description, new narratives, belief changes
```

### Graph Queries Needed

The World Runner needs:
- `get_all_tensions()` — Current tension states
- `get_narrative(id)` — Narrative details
- `get_path_between(a, b)` — Travel distance
- `get_character_location(id)` — Where someone is
- Update queries for tension pressure, narrative weight

### Performance Optimization

For long durations:
- **Batch ticks:** Run 10-50 ticks, then check flips
- **Pressure threshold pre-check:** Skip full tick if no tensions near breaking
- **Regional parallelism:** Process distant regions in parallel

---

## What Triggers the Runner?

**Narrator calls Runner as async Task.**

```python
# Narrator spawns Runner as background task
runner_task = Task(
    run_world,
    action="travel_to_york",
    max_minutes=2880,
    player_context=player_context
)

# Narrator continues (or waits for result)
injection = await runner_task
```

| Player Action | Narrator Spawns Task With |
|---------------|---------------------------|
| "I travel to York" | `action="travel", max_minutes=2880, path=[...]` |
| "I rest until morning" | `action="rest", max_minutes=480` |
| "I search the ruins" | `action="search", max_minutes=120` |
| "I wait for Edmund" | `action="wait", max_minutes=???` |

**Special case: Waiting.** "Wait for Edmund" has no fixed duration. Runner might run until:
- Edmund arrives (flip affecting player)
- Something else happens
- Narrator-set maximum reached

---

## Flip Context: The Cluster

When a flip happens, Runner returns the **cluster** around the flipped node:

```python
def get_flip_cluster(flip: Flip) -> List[Node]:
    """
    Get all nodes linked to the flipped tension/narrative.
    Max ~30 nodes. All fields except embeddings.
    """
    cluster = []

    # The flipped tension itself
    cluster.append(get_tension(flip.tension_id))

    # Narratives in the tension
    for narr_id in flip.narratives:
        cluster.append(get_narrative(narr_id))

    # Characters who believe those narratives
    for narr_id in flip.narratives:
        believers = get_believers(narr_id)
        cluster.extend(believers[:10])  # Limit per narrative

    # Places involved
    cluster.extend(get_places_in_narratives(flip.narratives))

    # Connected narratives (1 hop)
    for narr_id in flip.narratives:
        linked = get_linked_narratives(narr_id)
        cluster.extend(linked[:5])

    return cluster[:30]  # Hard cap
```

**Why the cluster matters:** The Narrator needs context to write the scene. Not just "bandits attack" but:
- Who are the bandits? (char_bandit_leader: name, traits, beliefs)
- What narrative flipped? (narr_road_danger: content, truth, weight)
- Who's involved? (char_aldric: current state, beliefs about bandits)
- Where exactly? (place_road_north: description, atmosphere)

--- 

*"The Runner runs the world. The Narrator tells the story. They meet at Injections."*

---

## CHAIN

PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
INPUTS:          ./INPUT_REFERENCE.md
TOOLS:           ./TOOL_REFERENCE.md
SYNC:            ./SYNC_World_Runner.md

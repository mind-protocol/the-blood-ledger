# Archived: SYNC_World_Runner_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

Archived on: 2025-12-18
Original file: SYNC_World_Runner_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md

---

## What Changed

### The Interrupt/Resume Pattern

```
Old: Narrator → "20 minutes passed" → Runner processes → injection
New: Narrator → "Travel to York (2 days)" → Runner runs ticks →
     → INTERRUPT at minute 500 → Narrator writes scene →
     → Narrator calls Runner again with remaining 2380 minutes
```

### New Injection Interface

```typescript
interface Injection {
  interrupted: boolean;
  at_minute?: number;
  remaining?: number;
  event?: Event;
  completed?: boolean;
  time_elapsed?: number;
  world_changes: WorldChange[];
  news_available: News[];
}
```

### affects_player() is Load-Bearing

The Runner only interrupts for flips that affect the player:
- Flip at player's current location
- Flip involving player character
- Flip involving companion traveling with player
- Critical-urgency flip nearby

Non-player flips are processed but don't interrupt.

---












## Implementation Status

### Exists

- `engine/physics/tick.py` — GraphTick class (mechanical tick, no LLM)
- `engine/physics/constants.py` — Physics constants
- `engine/orchestration/world_runner.py` — WorldRunnerService (calls LLM for flips)

### Needs Update

The existing code needs to be updated for the new design:

1. **WorldRunner class** — Add the tick loop
2. **Injection dataclass** — New interface
3. **affects_player()** — Player path awareness
4. **Resume handling** — Narrator calls with remaining time

### Implementation Plan

```
Phase 1: Core Loop
├── [ ] Create Injection dataclass (models/injection.py)
├── [ ] Create PlayerContext dataclass
├── [ ] Create Event, WorldChange, News dataclasses
├── [ ] Implement WorldRunner.run() with tick loop
├── [ ] Implement affects_player() with path awareness
├── [ ] Implement get_flip_cluster() — 30 nodes max, all fields
└── [ ] Connect to existing GraphTick

Phase 2: Injection Output
├── [ ] Implement injection_to_markdown() formatter
├── [ ] Implement cluster_to_markdown() for node details
├── [ ] Create injection_queue.json handler
├── [ ] Implement in-scene character action detection
└── [ ] Test markdown output readability

Phase 3: Integration
├── [ ] Update Narrator to call Runner as async Task
├── [ ] Narrator reads injection_queue.json before response
├── [ ] Handle interrupted injections (write scene, resume)
├── [ ] Handle completed injections (write arrival)
└── [ ] Test with travel scenario

Phase 4: Polish (Future)
├── [ ] Performance optimization for long durations
├── [ ] Parallel processing for distant regions
├── [ ] News propagation during tick loop
└── [ ] Cascading flip handling
```

---












## Key Design Decisions

### Runner Owns Time

The Runner runs the tick loop, not the Narrator. This means:
- Runner knows exactly what tick the interrupt happened at
- Runner tracks remaining time for resume
- Narrator just calls "run for N minutes" and handles what comes back

### Narrator Calls Runner as Async Task

```python
runner_task = Task(run_world, action="travel", max_minutes=2880, ...)
injection = await runner_task
```

Runner is spawned asynchronously. Narrator can continue or wait.

### Injection is Structured Markdown

The injection that goes to Narrator is **detailed markdown**, not just data:
- Full node names (char_wulfric, place_road_north)
- All fields except embeddings
- Cluster of ~30 nodes around the flip
- Readable by LLM

### Flip Returns Cluster

When a flip happens, Runner queries the cluster around the flipped node:
- The tension itself
- Narratives in the tension
- Characters who believe those narratives (max 10 per)
- Places involved
- Connected narratives (1 hop, max 5 per)
- Hard cap: 30 nodes total

### Injection Queue for In-Scene Events

Runner can push to `injection_queue.json` for non-interrupt events:
- Character wants to speak/act within current scene
- Not urgent enough to interrupt, but should happen
- Narrator reads queue and weaves in naturally

### Graph Mutations Applied During Run

Mutations are applied to the graph AS the Runner runs, not returned. By the time Injection comes back, the graph already reflects the new state.

### LLM Only for Events

```
Graph Tick: Pure math (ms) — runs every 5 game-minutes
Flip Processing: LLM call (seconds) — only when threshold crossed
```

Most ticks = no LLM. World advances cheaply. LLM only for "what happened?"

### Stateless Runner, Stateful Graph

Runner has no memory between calls. All state lives in the graph. Resume works because:
- Graph reflects current state
- Narrator tracks remaining time
- Fresh Runner call picks up from current graph

---












## Open Questions

### Performance at Scale

2-day travel = 576 ticks. Week = 2016 ticks. Options:
- Batch ticks (run 10-50, then check flips)
- Early exit if no tension near breaking
- Parallel processing by region

### Parallel Processing (Future)

For long durations with multiple regions:
```
Runner spawns:
  - Region A processor (Durham area)
  - Region B processor (York area)
  - Region C processor (Player's path)

Merge results. Only Region C can interrupt.
```

Not for V1, but architecture should allow it.

### What Triggers Runner?

Currently: Narrator decides. Could be:
- Player says "I travel to York" → Narrator calls Runner
- Player says "I wait" → Narrator calls Runner with max
- Conversation > 5 minutes → Narrator might call Runner

Need to define when Narrator invokes Runner vs just advancing time narratively.

---












## Connection to Other Systems

### Narrator → Runner

```
Narrator: run_world(
  action: "travel_to_york",
  max_minutes: 2880,
  player_context: {
    location: "place_camp",
    path: ["place_camp", "place_road", "place_york"],
    companions: ["char_aldric"]
  }
)

Runner: runs tick loop, returns Injection
```

### Runner → Graph

Runner reads:
- All tensions (via GraphQueries)
- Narrative weights
- Character locations
- Travel paths

Runner writes (during run):
- Tension pressure updates
- New narratives from flips
- Belief changes
- Character movements

### Runner → Narrator

Via Injection:
- `interrupted: true` → Narrator writes interrupt scene
- `completed: true` → Narrator writes completion scene
- `world_changes` → Narrator knows what happened
- `news_available` → Narrator can reveal to player

---












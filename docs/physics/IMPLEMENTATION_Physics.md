# Physics — Implementation: Code Architecture and Structure

```
STATUS: DESIGNING
CREATED: 2024-12-18
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Physics.md
BEHAVIORS:       ./BEHAVIORS_Physics.md
ALGORITHM:       ./ALGORITHM_Energy.md (M1-M6, M11-M13), ./ALGORITHM_Physics.md,
                 ./ALGORITHM_Handlers.md, ./ALGORITHM_Input.md, ./ALGORITHM_Actions.md,
                 ./ALGORITHM_Questions.md, ./ALGORITHM_Speed.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:      ./VALIDATION_Physics.md
THIS:            IMPLEMENTATION_Physics.md (you are here)
                 - Code Architecture (top)
                 - Runtime Patterns (bottom): scene, time, movement, backstory
TEST:            ./TEST_Physics.md, ../../engine/tests/test_moment_graph.py
SYNC:            ./SYNC_Physics.md
```

---

## CODE STRUCTURE

```
engine/
├── physics/
│   ├── __init__.py              # Exports GraphTick, TickResult
│   ├── tick.py                  # Physics tick loop (v1 exists, v2 WIP)
│   └── constants.py             # Energy/decay constants (exists)
│
├── handlers/                    # TO CREATE
│   ├── __init__.py              # Exports CharacterHandler, dispatch
│   ├── base.py                  # BaseHandler class
│   ├── player.py                # Player handler (special)
│   ├── companion.py             # Companion handler
│   ├── npc.py                   # NPC handler
│   └── grouped.py               # Grouped character handler
│
├── canon/                       # TO CREATE
│   ├── __init__.py              # Exports CanonHolder
│   ├── holder.py                # Canon Holder (records, then links)
│   └── conflict.py              # Conflict resolution
│
├── moment_graph/
│   ├── __init__.py              # Exports MomentGraph facade (exists)
│   ├── queries.py               # Query layer (exists)
│   ├── traversal.py             # Click/wait traversal (exists)
│   └── surface.py               # Surfacing algorithm (exists)
│
├── orchestration/
│   ├── __init__.py              # Exports Orchestrator
│   ├── orchestrator.py          # Main coordinator (exists)
│   ├── narrator.py              # Claude CLI caller (exists)
│   ├── world_runner.py          # Background world (exists)
│   └── speed.py                 # TO CREATE: Speed controller
│
├── models/
│   ├── __init__.py              # Exports all models
│   ├── nodes.py                 # Moment, Narrative, etc. (exists)
│   ├── links.py                 # Link types (exists)
│   └── tensions.py              # Tension detection (computed, not stored)
│
├── api/
│   ├── __init__.py              # Exports FastAPI app
│   ├── app.py                   # FastAPI entry (exists)
│   └── moments.py               # Moments endpoints (exists)
│
├── db/
│   ├── __init__.py              # Exports graph clients
│   ├── graph_queries.py         # Read operations (exists)
│   └── graph_ops.py             # Write operations (exists)
│
└── tests/
    ├── test_moment_graph.py     # Moment graph tests (exists)
    ├── test_implementation.py   # Behavior tests (exists)
    └── test_behaviors.py        # Physics tests (exists)
```

### File Responsibilities

| File | Purpose | Status |
|------|---------|--------|
| `physics/tick.py` | Physics tick: inject, decay, propagate, detect flips | v1 EXISTS, v2 WIP |
| `physics/constants.py` | All energy/decay/pressure constants | EXISTS |
| `handlers/base.py` | BaseHandler abstract class | TO CREATE |
| `handlers/companion.py` | Handler for companion characters | TO CREATE |
| `canon/holder.py` | Canon Holder: record, then links | TO CREATE |
| `moment_graph/queries.py` | Fast graph queries (<50ms) | EXISTS |
| `moment_graph/traversal.py` | Click/wait/status transitions | EXISTS |
| `orchestration/orchestrator.py` | Ties physics, handlers, canon together | EXISTS, needs v2 update |
| `orchestration/speed.py` | Speed controller (1x/2x/3x + The Snap) | TO CREATE |
| `api/moments.py` | REST endpoints for frontend | EXISTS |

---

## SCHEMA

### Moment (Node)

```yaml
Moment:
  required:
    - id: str                    # {place}_{day}_{time}_{type}_{timestamp}
    - text: str                  # The actual spoken/narrated content
    - type: MomentType           # narration | dialogue | action | thought | description
    - status: MomentStatus       # possible | active | spoken | dormant | decayed
    - weight: float              # 0.0-1.0, computed by physics
    - tick_created: int          # When created
  optional:
    - tick_spoken: int           # When spoken (if spoken)
    - tick_decayed: int          # When decayed (if decayed)
    - tone: str                  # bitter, hopeful, urgent, etc.
    - energy: float              # v2: current energy level (0.0-1.0)
  constraints:
    - weight >= 0.0 AND weight <= 1.0
    - status transitions: possible -> active -> spoken; possible -> decayed
```

### ATTACHED_TO (Link)

```yaml
ATTACHED_TO:
  from: Moment
  to: Character | Place | Thing | Narrative
  properties:
    - presence_required: bool    # Must target be present?
    - weight: float              # How strongly attached (0.0-1.0)
```

### THEN (Link)

```yaml
THEN:
  from: Moment
  to: Moment
  properties:
    - tick: int                  # When link created
    - player_caused: bool        # Did player trigger this?
  constraints:
    - Created by Canon Holder AFTER moment becomes spoken
    - Never pre-created (emergence, not script)
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Physics tick | `physics/tick.py:79` (GraphTick.run) | Scheduler / elapsed time |
| Click word | `moment_graph/traversal.py:38` (handle_click) | Frontend click event |
| Player input | `api/moments.py` (WIP) | Free text input from frontend |
| Flip detected | `physics/tick.py:514` (_detect_flips) | Physics finds weight >= 0.8 |
| Handler dispatch | `handlers/__init__.py` (TO CREATE) | Flip triggers handler |
| Canon record | `canon/holder.py` (TO CREATE) | Handler returns moment |
| Speed change | `orchestration/speed.py` (TO CREATE) | Direct address / interrupt |

---

## DATA FLOW

### Physics Tick Flow

```
┌─────────────────────┐
│   Elapsed Time      │ (from orchestrator)
└──────────┬──────────┘
           │ elapsed_minutes
           ▼
┌─────────────────────┐
│   GraphTick.run()   │ ← physics/tick.py
│   - inject energy   │
│   - decay           │
│   - propagate       │
│   - detect flips    │
└──────────┬──────────┘
           │ TickResult { flips, energy_total, ... }
           ▼
┌─────────────────────┐
│  Orchestrator       │ ← For each flip, dispatch handler
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Character Handlers │ ← One per flipped character
│  (parallel)         │
└──────────┬──────────┘
           │ generated moments (async)
           ▼
┌─────────────────────┐
│  Canon Holder       │ ← Record to graph, create THEN links
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Frontend (SSE)     │ ← Push to client
└─────────────────────┘
```

### Player Input Flow

```
┌─────────────────────┐
│  Frontend Input     │ "I want to ask Aldric about his father"
└──────────┬──────────┘
           │ raw text
           ▼
┌─────────────────────┐
│  Input Parser       │ ← Extract entities, intent
│  api/moments.py     │
└──────────┬──────────┘
           │ InputResult { type, refs, text }
           ▼
┌─────────────────────┐
│  Create Moment      │ ← type=question, attached to Aldric
│  graph_ops.py       │
└──────────┬──────────┘
           │ moment_id
           ▼
┌─────────────────────┐
│  Energy Tick        │ ← Character pumps → narrative → moment weight
│  physics/tick.py    │
└──────────┬──────────┘
           │ (weight recomputed from sources)
           ▼
┌─────────────────────┐
│  Normal Tick Loop   │ ← Moment may flip same tick
└─────────────────────┘
```

### Handler to Canon Flow

```
┌─────────────────────┐
│  Flip Detected      │ Character X, moment M
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Handler for X      │ ← Claude CLI with scope
│  handlers/X.py      │
│  (async, parallel)  │
└──────────┬──────────┘
           │ HandlerOutput { moment, attachments, narratives }
           ▼
┌─────────────────────┐
│  Await Handler      │ ← Orchestrator waits for response
└──────────┬──────────┘
           │ completed HandlerOutput
           ▼
┌─────────────────────┐
│  Canon Holder       │
│  1. Record moment   │ ← FIRST: write to graph
│  2. Create THEN     │ ← SECOND: link from previous
│  3. Push to display │ ← THIRD: notify frontend
└─────────────────────┘
```

---

## LOGIC CHAINS

### LC1: Flip Detection

**Purpose:** Determine when a moment should trigger a handler

```
moment.weight
  → physics/tick.py:_detect_flips()     # Check weight >= 0.8
    → For each moment attached to character
      → If weight >= FLIP_THRESHOLD
        → Add to flips list
          → Return flips

```

**Data transformation:**
- Input: `moment.weight` — float 0.0-1.0
- Check: `weight >= 0.8` — deterministic threshold
- Output: `List[FlipInfo]` — character_id, moment_id, weight

### LC2: Energy Injection

**Purpose:** Player input immediately affects graph state

```
player_input
  → api/moments.py:handle_input()       # Parse input
    → graph_ops.py:create_moment()      # Create moment node
      → physics/tick.py:inject()        # Add energy
        → weight update

```

**Data transformation:**
- Input: `str` — raw player text
- After parse: `InputResult` — type, entities, processed text
- After create: `moment_id` — new moment in graph
- After inject: moment has energy, ready for tick processing

### LC3: Handler Execution

**Purpose:** Generate character response when moment flips

```
flip_info
  → handlers/__init__.py:dispatch()     # Select handler
    → handlers/{type}.py:run()          # Run with scope
      → Claude CLI call                 # LLM generation
        → HandlerOutput                 # Moment + attachments

```

**Data transformation:**
- Input: `FlipInfo` — character_id, moment_id
- After dispatch: `Handler` instance for character type
- After scope: `HandlerScope` — what handler can see/create
- After LLM: `HandlerOutput` — moment text, attachments, mutations

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
orchestrator.py
    └── imports → physics/tick.py
    └── imports → handlers/__init__.py (TO CREATE)
    └── imports → canon/holder.py (TO CREATE)
    └── imports → moment_graph/queries.py
    └── imports → api/moments.py

physics/tick.py
    └── imports → db/graph_queries.py
    └── imports → db/graph_ops.py
    └── imports → physics/constants.py

handlers/base.py (TO CREATE)
    └── imports → models/nodes.py
    └── imports → db/graph_queries.py

canon/holder.py (TO CREATE)
    └── imports → db/graph_ops.py
    └── imports → moment_graph/traversal.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `falkordb` | Graph database | `db/graph_*.py` |
| `pydantic` | Model validation | `models/*.py` |
| `fastapi` | REST API | `api/app.py` |
| `subprocess` | Claude CLI calls | `orchestration/narrator.py`, `handlers/*.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Graph state | FalkorDB | Global | Persistent |
| Current tick | `Orchestrator.tick` | Session | Per playthrough |
| Active handlers | `Orchestrator.pending_handlers` | Request | Per tick cycle |
| Speed mode | `SpeedController.mode` | Session | Player controlled |
| Canon queue | `CanonHolder.queue` | Request | Per handler batch |

### State Transitions

```
moment.status:
  possible ──[weight>=0.8]──► active ──[spoken]──► spoken
      │                                               │
      └──[decay]──► decayed                          └──► (in history)

speed.mode:
  1x ──[3x_click]──► 3x ──[direct_address]──► 1x (The Snap)
      ──[2x_click]──► 2x ──[direct_address]──► 1x
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Connect to FalkorDB (graph_queries, graph_ops)
2. Load physics constants
3. Initialize GraphTick
4. Initialize Orchestrator (ties everything together)
5. Start API server
6. System ready for player input
```

### Main Loop (Orchestrator Tick Cycle)

```
1. Receive elapsed time from frontend
2. Run physics tick → get flips
3. For each flip:
   a. Dispatch handler (async)
   b. Collect results
4. Send completed handlers to Canon Holder
5. Canon Holder records to graph
6. Canon Holder creates THEN links
7. Push new moments to frontend (SSE)
8. Return updated state
```

### Shutdown

```
1. Complete pending handlers (or timeout)
2. Flush canon queue
3. Close graph connections
4. Save session state (optional)
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Physics tick | Sync | Fast, no I/O except graph queries |
| Character handlers | Async parallel | Multiple handlers run simultaneously |
| Canon Holder | Sequential queue | Order matters for THEN links |
| Graph writes | Sync (FalkorDB handles) | Atomic per operation |
| Frontend SSE | Async | Push as canon records |

**Critical insight:** Handlers are parallel, but Canon is sequential. This maintains causality while maximizing throughput.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `DECAY_RATE` | `physics/constants.py` | `0.02` | Base decay per tick |
| `FLIP_THRESHOLD` | `physics/constants.py` | `0.8` | Weight at which moment flips |
| `PUMP_RATE` | `physics/constants.py` | `0.1` | Character energy → narratives per tick |
| `TENSION_DRAW` | `physics/constants.py` | `0.2` | How much tension pulls from participants |
| `ACTUALIZATION_COST` | `physics/constants.py` | `0.5` | Energy cost per moment flip |
| `MIN_TICK_MINUTES` | `physics/constants.py` | `5` | Minimum elapsed time for tick |
| `HANDLER_TIMEOUT` | `handlers/base.py` | `30s` | Max time for handler response |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `physics/tick.py` | 1-35 | Docstring references ALGORITHM_Physics |
| `moment_graph/traversal.py` | 1-6 | Docstring references moment graph docs |
| `physics/constants.py` | 1-25 | Docstring references VALIDATION_Complete_Spec |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM_Physics: Step 1 (Inject) | `physics/tick.py:_flow_energy_to_narratives` (partial) |
| ALGORITHM_Physics: Step 2 (Decay) | `physics/tick.py:_decay_energy` |
| ALGORITHM_Physics: Step 3 (Propagate) | `physics/tick.py:_propagate_energy` |
| ALGORITHM_Physics: Step 4 (Detect) | `physics/tick.py:_detect_flips` |
| ALGORITHM_Handlers: dispatch | TO IMPLEMENT in `handlers/__init__.py` |
| ALGORITHM_Canon: record | TO IMPLEMENT in `canon/holder.py` |
| ALGORITHM_Speed: controller | TO IMPLEMENT in `orchestration/speed.py` |
| BEHAVIOR B1 (click word) | `moment_graph/traversal.py:handle_click` |
| BEHAVIOR B2 (wait trigger) | `moment_graph/traversal.py:process_wait_triggers` |
| VALIDATION I1 (graph truth) | All graph operations use FalkorDB |
| VALIDATION I2 (THEN after) | TO IMPLEMENT in `canon/holder.py` |

---

## IMPLEMENTATION PRIORITIES

### Phase 1: Core v2 Updates (CURRENT)

1. **Update `physics/tick.py`**
   - Add moment weight tracking (not just narrative weight)
   - Add `FLIP_THRESHOLD` constant
   - Return flip info for moments, not just tensions

2. **Create `handlers/` module**
   - `base.py` — BaseHandler with scope isolation
   - `companion.py` — First handler type
   - `__init__.py` — Dispatcher

3. **Create `canon/holder.py`**
   - Record moment to graph
   - Create THEN links (after, not before)
   - Push to frontend queue

### Phase 2: Speed Controller

4. **Create `orchestration/speed.py`**
   - 1x/2x/3x modes
   - Interrupt detection
   - "The Snap" transition

### Phase 3: Integration

5. **Update `orchestrator.py`**
   - Wire physics → handlers → canon
   - Handle async handler results
   - Integrate speed controller

---

## GAPS / IDEAS / QUESTIONS

- [ ] `handlers/` module does not exist yet — needs creation
- [ ] `canon/holder.py` does not exist yet — needs creation
- [ ] `orchestration/speed.py` does not exist yet — needs creation
- [ ] Physics tick still uses narrative-centric model, needs moment-centric update
- [ ] Player input → energy injection path not fully implemented
- IDEA: Handler pre-generation during 2x/3x modes
- IDEA: Canon Holder batching for efficiency
- QUESTION: How to handle handler timeout gracefully?
- QUESTION: What happens if handler fails mid-generation?

---

# RUNTIME PATTERNS

Infrastructure patterns for scene queries, time, movement, and backstory generation.

---

## SCENE AS QUERY

There is no scene object. "Scene" is a query result.

```python
def get_scene():
    return {
        "place": query("MATCH (p:Character {id: 'char_player'})-[:AT]->(loc) RETURN loc"),
        "present": query("MATCH (c:Character)-[:AT]->(loc) WHERE player AT loc RETURN c"),
        "things": query("MATCH (t:Thing)-[:AT]->(loc) RETURN t"),
        "time": get_current_datetime(),
        "moments": get_live_moments()  # From moment graph
    }
```

**Player Experience:** There's no "loading scene." You're always somewhere, with someone, and things are happening. Transitions are about movement, not scene switches.

### Place Determines Backdrop

```yaml
Place:
  id: place_york_market
  name: "York Market"
  atmosphere:
    weather: [rain, cold]
    mood: tense
    details: ["merchants hawking", "Norman soldiers watching", "mud underfoot"]
```

Narrator uses `place.atmosphere` for color. Not stored in scene — queried from place.

### Character Location State

```yaml
Character → Place (AT):
  present: bool         # Actually here now
  visible: bool         # Can be seen (false = hiding)
  arriving: bool        # Just arrived (triggers entrance moments)
  leaving: bool         # About to leave (triggers exit moments)
  traveling_to: place_id
  travel_progress: float
  travel_eta_minutes: int
```

---

## TIME PASSAGE

### Time-Costing Actions

| Action | Time Cost | Trigger |
|--------|-----------|---------|
| Conversation turn | 1-5 minutes | Per moment spoken |
| Click traversal | 1 minute | Per click |
| Free input response | 2-3 minutes | Per exchange |
| Short action | 5-30 minutes | Player choice |
| Long action | Hours | Player choice |
| Travel | From route data | Player initiates |
| Waiting | Player specified | "Wait until evening" |

```python
def on_moment_spoken(moment):
    # Conversation takes time
    time_cost = estimate_moment_duration(moment)  # 1-5 min based on length
    advance_time(minutes=time_cost)

def on_player_action(action):
    if action.type == "short":  # "I search the room"
        advance_time(minutes=action.duration or 15)
    elif action.type == "long":  # "I rest"
        advance_time(hours=action.duration or 1)
```

### Time Passage Effects

```python
def advance_time(minutes):
    old_time = current_time()
    new_time = old_time + timedelta(minutes=minutes)

    # Tick the world
    ticks = minutes // 5
    for _ in range(ticks):
        run_graph_tick()

    # Check for scheduled events
    events = query("""
        MATCH (e:Event)
        WHERE e.scheduled_time > $old AND e.scheduled_time <= $new
        RETURN e
    """, old=old_time, new=new_time)

    for event in events:
        inject_event(event)

    # Check for time-of-day transitions
    if crosses_threshold(old_time, new_time, "dusk"):
        inject_atmosphere_change("dusk")

    # Update character states (tiredness, hunger if tracked)
    update_character_states(minutes)
```

**Player Experience:** Conversations have opportunity cost. Talk too long and suddenly it's dark. The patrol arrived while you were arguing.

---

## CHARACTER MOVEMENT

### Leave = Moment + Action

```yaml
Moment:
  id: moment_aldric_check_brother
  text: "I should go check on my brother."
  type: dialogue
  status: possible

  # This moment IS an action
  action: travel
  action_target: place_wulfric_farm

  ATTACHED_TO → char_aldric
    presence_required: true
  ATTACHED_TO → narr_wulfric_injured
    presence_required: true  # Surfaces when this narrative active
```

```python
def on_moment_spoken(moment):
    if moment.action == "travel":
        runner.travel_character(
            char_id=moment.speaker,
            destination=moment.action_target,
            async=True  # World keeps going without them
        )

        update("""
            MATCH (c:Character {id: $id})-[r:AT]->(p:Place)
            SET r.present = false,
                r.traveling_to = $dest,
                r.travel_progress = 0
        """, id=moment.speaker, dest=moment.action_target)
```

**Player Experience:** "I should check on my brother." Aldric stands, nods to you, and walks away. He's gone. Not vanished — traveling.

### Return = Narrative with Conditions

```yaml
Moment:
  id: moment_aldric_promises_return
  text: "I'll be back by nightfall."
  type: dialogue

  on_spoken: |
    create_narrative(
      id="narr_aldric_will_return",
      content="Aldric said he'll be back by nightfall",
      type="promise",
      about=[char_aldric],
      deadline="nightfall"
    )

Moment:
  id: moment_aldric_returns
  text: "Aldric appears on the road, raising a hand in greeting."
  type: narration
  status: dormant

  ATTACHED_TO → narr_aldric_will_return
    presence_required: true  # Promise must exist
  ATTACHED_TO → char_aldric
    presence_required: true  # Aldric must be here
```

When Aldric's travel completes:
1. `char_aldric AT player_location` becomes true
2. `moment_aldric_returns` presence requirements satisfied
3. Moment surfaces
4. Promise narrative can resolve (kept or broken based on time)

### Arrival = Travel Completion + Moment

```python
def on_character_arrives(char_id, location_id):
    # Update location state
    update("""
        MATCH (c:Character {id: $id})
        MATCH (dest:Place {id: $loc})
        MERGE (c)-[r:AT]->(dest)
        SET r.present = true, r.arriving = true
    """, id=char_id, loc=location_id)

    # Find arrival moments for this character
    arrival_moments = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $id})
        WHERE m.type = 'arrival' OR m.text CONTAINS 'arrives'
        AND m.status = 'dormant'
        SET m.status = 'possible', m.weight = 0.9
        RETURN m
    """, id=char_id)
```

---

## CHARACTER INTRODUCTION PATTERNS

| Situation | What Happens |
|-----------|--------------|
| "I'll fetch him" | NPC travels away, returns with friend |
| "He lives in York" | Player can travel there |
| "He's coming here" | NPC is traveling, will arrive |
| Stranger arrives | Their own moment brought them |

### Fetch Pattern

```yaml
Moment:
  id: moment_aldric_fetch_brother
  text: "I'll go get him. Wait here."
  type: dialogue

  action: travel_and_return
  action_target: place_wulfric_farm
  action_bring: char_wulfric
```

```python
def handle_travel_and_return(moment):
    char_id = moment.speaker
    destination = moment.action_target
    bring = moment.action_bring
    origin = get_character_location(char_id)

    runner.travel_character(char_id, destination, async=True)

    on_arrival(char_id, destination, callback=lambda:
        runner.travel_characters([char_id, bring], origin, async=True)
    )
```

### Go To Them Pattern

```yaml
Moment:
  id: moment_aldric_brother_location
  text: "My brother lives at the farm north of York."
  type: dialogue

  on_spoken: |
    create_belief(player, narr_wulfric_location, heard=1.0)
    reveal_place(place_wulfric_farm)  # Now on map
```

### Stranger Arrives Pattern

NPCs have their own moments that trigger their own travel:

```yaml
Moment:
  id: moment_wulfric_seeks_aldric
  text: "I must find my brother."
  type: thought
  status: possible

  action: travel
  action_target: char_aldric.location  # Dynamic

  ATTACHED_TO → char_wulfric
  ATTACHED_TO → narr_wulfric_worried
```

**Player Experience:** A stranger arrives at camp. "I'm looking for Aldric. He's my brother." You never asked for this. The world brought him.

---

## QUERY MOMENTS (Backstory Generation)

Citizens wondering about themselves IS content, and triggers backstory generation.

### The Query Moment

```yaml
Moment:
  id: moment_aldric_wonder_father
  text: "What would my father think of me now?"
  type: thought
  status: possible
  weight: 0.4

  query: "Who is Aldric's father? What was their relationship?"
  query_type: backstory_gap
  query_filled: false

  ATTACHED_TO → char_aldric
    presence_required: true
```

### Query Triggers Generation

```python
def on_moment_spoken(moment):
    if moment.query and not moment.query_filled:
        queue_backstory_generation(
            query=moment.query,
            about=get_attached_character(moment),
            triggered_by=moment.id
        )

async def generate_backstory(query, about, triggered_by):
    context = get_character_context(about)

    prompt = f"""
    Character: {context.character.name}
    Current identity: {format_context(context)}

    Question to answer: {query}

    Generate:
    1. A backstory fact (Narrative node)
    2. 1-3 memory moments that could surface later
    """

    result = await llm(prompt, structured=BackstoryResult)

    # Create the narrative
    narr = create_narrative(result.fact)

    # Create memory moments, linked to the wondering
    for memory in result.memories:
        m = create_moment(memory)
        create_link(triggered_by, "ANSWERED_BY", m.id)
        attach(m, about)
        attach(m, narr)

    update("MATCH (m:Moment {id: $id}) SET m.query_filled = true", id=triggered_by)
```

### The ANSWERED_BY Link

```cypher
# What has Aldric wondered about?
MATCH (m:Moment)
WHERE m.query IS NOT NULL
AND (m)-[:ATTACHED_TO]->(:Character {id: 'char_aldric'})
RETURN m.text, m.query, m.query_filled

# Full trace: wondering → answer → narrative
MATCH (wonder:Moment)-[:ANSWERED_BY]->(answer:Moment)-[:ATTACHED_TO]->(n:Narrative)
RETURN wonder.text, answer.text, n.content
```

**Player Experience:** Days later, in a forge, Aldric speaks unprompted: "My father was a blacksmith. He wanted me to follow him." You remember him wondering. Now you know.

---

## FLASHBACK PATTERN

Backstory through environment. Places trigger memories.

```yaml
Moment:
  id: moment_aldric_forge_memory
  text: "My father used to work a forge like this. The smell... I'd forgotten."
  type: dialogue
  status: dormant

  ATTACHED_TO → char_aldric
    presence_required: true
  ATTACHED_TO → narr_aldric_father_blacksmith
    presence_required: true  # Player must know this
  ATTACHED_TO → place_type_forge
    presence_required: true  # Must be in a forge
```

**Player Experience:** You enter a forge. Aldric pauses. "My father used to work a forge like this." He didn't volunteer this backstory — the environment pulled it out of him. Places have power over memory.

---

## FORWARD-ONLY CITIZENS

Citizens generate forward, not backward. They don't contradict history.

### Rules

1. Citizens only generate `possible` moments, never `spoken`
2. Citizens never modify existing moments
3. If a citizen generates something that contradicts history, it's discarded
4. THEN links are immutable — the history is sacred

**Player Experience:** Characters don't suddenly forget what they said. The game's memory is perfect. Callbacks work because the past is fixed.

---

## IMPLEMENTATION CHECKLIST (Runtime Patterns)

- [ ] Scene as query (no scene object)
- [ ] Place atmosphere integration
- [ ] Character AT state (present, visible, arriving, traveling_to)
- [ ] Time-costing actions (conversation turns, short/long actions)
- [ ] Time passage effects (events, atmosphere transitions)
- [ ] Leave = moment with action (travel action type)
- [ ] Return = narrative with conditions (promise tracking)
- [ ] Arrival = travel completion triggers presence-gated moments
- [ ] Fetch pattern (travel_and_return action with action_bring)
- [ ] Go To Them pattern (reveal_place on mention)
- [ ] Stranger Arrives pattern (NPCs have own travel moments)
- [ ] Query moments (query field on moments, query_filled flag)
- [ ] Query triggers backstory generation (async narrator pipeline)
- [ ] ANSWERED_BY links (trace question → answer)
- [ ] Forward-only citizen generation rules
- [ ] Flashback pattern (backstory + place triggers)

---

*"The boring infrastructure is what makes the magic work."*

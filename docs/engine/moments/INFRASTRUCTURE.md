# INFRASTRUCTURE — The Boring-But-Essential Patterns

```
CREATED: 2024-12-17
STATUS: Design
AVERAGE RATING: 8.8/10
```

---

## CHAIN

```
ARCHITECTURE: ./ARCHITECTURE_Overview.md
PHASES:       ./PHASE_1_Core_Graph.md → ./PHASE_5_Natural_Dynamics.md
THIS:         INFRASTRUCTURE.md (you are here)
SCHEMA:       ./SCHEMA_Moments.md
ALGORITHMS:   ./ALGORITHM_View_Query.md, ./ALGORITHM_Transitions.md, ./ALGORITHM_Lifecycle.md
```

Scene decomposition. Time mechanics. Movement. Introductions. Backstory gaps.

---

## Scene Slicing

There is no scene object. "Scene" is a query result.

### What "Scene" Actually Is

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

**Rating: 7/10** — Invisible infrastructure. Player doesn't feel it, but everything breaks without it.

---

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

**Player Experience:** Each location feels distinct. York is tense and muddy. The monastery is quiet and cold. Atmosphere comes from WHERE, not from a scene file.

**Rating: 8/10** — Creates sense of place. Simple but essential.

---

### Characters Have Location State

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

**Player Experience:** Aldric isn't just "in the scene" — he's here, visible, not leaving. When that changes, you see it happen.

**Rating: 7/10** — State management. Invisible but required.

---

## Time Passage Triggers

When does time move forward?

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

**Player Experience:** Conversations take time. If you talk for an hour, an hour passes. The Norman patrol that was "coming at dusk" might arrive mid-conversation. Time pressure is real.

**Rating: 9/10** — Creates urgency. Time isn't free. Choices about what to discuss have weight.

---

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

**Player Experience:** Talk too long and suddenly it's dark. The patrol arrived while you were arguing. Time moves and the world responds. Conversations have opportunity cost.

**Rating: 9/10** — Makes time meaningful. "Just one more question" has consequences.

---

## Characters Leaving

Leave isn't a special system. It's just a moment with an action.

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
        # Narrator recognizes action, calls Runner async
        runner.travel_character(
            char_id=moment.speaker,
            destination=moment.action_target,
            async=True  # World keeps going without them
        )

        # Character is now traveling
        update("""
            MATCH (c:Character {id: $id})-[r:AT]->(p:Place)
            SET r.present = false,
                r.traveling_to = $dest,
                r.travel_progress = 0
        """, id=moment.speaker, dest=moment.action_target)
```

**Player Experience:** "I should check on my brother." Aldric stands, nods to you, and walks away. He's gone. Not vanished — traveling. You might see him on the road if you follow.

**Rating: 9/10** — Departure is dialogue, not system event. Natural.

---

### Return = Narrative with Conditions

When someone leaves, they might promise to return:

```yaml
Moment:
  id: moment_aldric_promises_return
  text: "I'll be back by nightfall."
  type: dialogue

  # Creates a promise narrative when spoken
  on_spoken: |
    create_narrative(
      id="narr_aldric_will_return",
      content="Aldric said he'll be back by nightfall",
      type="promise",
      about=[char_aldric],
      deadline="nightfall"
    )

Narrative:
  id: narr_aldric_will_return
  content: "Aldric said he'll be back"
  type: promise
  deadline: nightfall

  # Links to arrival moment
  TRIGGERS → moment_aldric_returns
    when: aldric_at_player_location

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

When Aldric's travel completes and he reaches player's location:
1. `char_aldric AT player_location` becomes true
2. `moment_aldric_returns` presence requirements satisfied
3. Moment surfaces
4. Promise narrative can resolve (kept or broken based on time)

**Player Experience:** He said nightfall. It's past midnight when he finally appears. "I'm sorry. It took longer than I thought." The promise narrative tracked it. Now there's tension.

**Rating: 9/10** — Promises are tracked. Returns are dramatic. Time matters.

---

## Characters Arriving

Arrivals are just the completion of someone else's travel.

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
    # They become possible when character is present
    arrival_moments = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $id})
        WHERE m.type = 'arrival' OR m.text CONTAINS 'arrives' OR m.text CONTAINS 'appears'
        AND m.status = 'dormant'
        SET m.status = 'possible', m.weight = 0.9
        RETURN m
    """, id=char_id)

    # Clear arriving flag after moment spoken
    for m in arrival_moments:
        m.on_spoken = lambda: clear_arriving_flag(char_id)
```

**Player Experience:** The door opens. Someone enters. You see who it is. Arrivals are moments, not pop-ins.

**Rating: 9/10** — Entrances have weight. "Who's that?" is possible.

---

## Characters Introducing Friends

There's no special introduction system. People come and go.

### The Patterns

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

  ATTACHED_TO → char_aldric
  ATTACHED_TO → narr_need_help  # Surfaces when you need help
```

```python
def handle_travel_and_return(moment):
    char_id = moment.speaker
    destination = moment.action_target
    bring = moment.action_bring
    origin = get_character_location(char_id)

    # Character leaves
    runner.travel_character(char_id, destination, async=True)

    # When they arrive at destination
    on_arrival(char_id, destination, callback=lambda:
        # Now both travel back
        runner.travel_characters([char_id, bring], origin, async=True)
    )
```

**Player Experience:** "I'll go get him." Aldric leaves. Time passes. The door opens — Aldric returns with a stranger. "This is my brother Wulfric."

**Rating: 9/10** — NPCs have agency to fetch people. Your network expands through theirs.

---

### Go To Them Pattern

```yaml
Moment:
  id: moment_aldric_brother_location
  text: "My brother lives at the farm north of York. If you want to meet him, that's where he'll be."
  type: dialogue

  # Creates knowledge
  on_spoken: |
    create_belief(player, narr_wulfric_location, heard=1.0)
    reveal_place(place_wulfric_farm)  # Now on map

  ATTACHED_TO → char_aldric
  CAN_LEAD_TO → moment_player_ask_directions
    trigger: click
    require_words: ["brother", "farm", "where"]
```

**Player Experience:** "He lives at the farm." Now there's a new place on your map. A reason to travel. You'll meet Wulfric on your own terms.

**Rating: 8/10** — Information creates exploration. NPCs point you outward.

---

### Stranger Arrives Pattern

NPCs have their own moments that trigger their own travel:

```yaml
# Wulfric's own moment, nothing to do with player
Moment:
  id: moment_wulfric_seeks_aldric
  text: "I must find my brother."
  type: thought
  status: possible

  action: travel
  action_target: char_aldric.location  # Dynamic — wherever Aldric is

  ATTACHED_TO → char_wulfric
  ATTACHED_TO → narr_wulfric_worried  # His own concerns
```

Wulfric has his own story. His own worries. His own reasons to travel. He might show up because *he* decided to, not because the player did anything.

**Player Experience:** A stranger arrives at camp. "I'm looking for Aldric. He's my brother." You never asked for this. The world brought him.

**Rating: 10/10** — NPCs have their own agency. The world isn't player-centric.

---

## Wondering as Query Moments

Citizens wondering about themselves IS content, and triggers backstory generation.

### The Query Moment

```yaml
Moment:
  id: moment_aldric_wonder_father
  text: "What would my father think of me now?"
  type: thought
  status: possible
  weight: 0.4

  # This moment is also a query
  query: "Who is Aldric's father? What was their relationship?"
  query_type: backstory_gap
  query_filled: false

  ATTACHED_TO → char_aldric
    presence_required: true
```

**Player Experience:** Aldric stares at the fire. "What would my father think of me now?" He's wondering. You're witnessing his inner life. And somewhere, the narrator is deciding who his father was.

**Rating: 9/10** — Gaps are visible. Characters wonder aloud. Mystery becomes content.

---

### Query Triggers Generation

```python
def on_moment_spoken(moment):
    # If this moment has an unfilled query
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

    Make it:
    - Consistent with existing facts
    - Dramatically interesting
    - Connectable to current situation
    """

    result = await llm(prompt, structured=BackstoryResult)

    # Create the narrative
    narr = create_narrative(result.fact)

    # Create memory moments, linked to the wondering
    for memory in result.memories:
        m = create_moment(memory)
        create_link(triggered_by, "ANSWERED_BY", m.id)
        attach(m, about)
        attach(m, narr)  # Surfaces when narrative is relevant

    # Mark query as filled
    update("MATCH (m:Moment {id: $id}) SET m.query_filled = true", id=triggered_by)
```

**Player Experience:** Days later, in a forge, Aldric speaks unprompted: "My father was a blacksmith. He wanted me to follow him." You remember him wondering. Now you know.

**Rating: 10/10** — Questions get answers. The trace is preserved. Backstory earns its reveals.

---

### The ANSWERED_BY Link

```cypher
# What has Aldric wondered about?
MATCH (m:Moment)
WHERE m.query IS NOT NULL
AND (m)-[:ATTACHED_TO]->(:Character {id: 'char_aldric'})
RETURN m.text, m.query, m.query_filled

# What answered his wondering about his father?
MATCH (wonder:Moment {query_type: 'backstory_gap'})-[:ANSWERED_BY]->(answer:Moment)
WHERE wonder.query CONTAINS 'father'
RETURN wonder.text AS question, answer.text AS answer

# Full trace: wondering → answer → narrative
MATCH (wonder:Moment)-[:ANSWERED_BY]->(answer:Moment)-[:ATTACHED_TO]->(n:Narrative)
RETURN wonder.text, answer.text, n.content
```

**Player Experience:** If you wanted, you could trace every piece of backstory to the moment that prompted it. The game remembers how it learned things. Provenance is preserved.

**Rating: 8/10** — Debug gold. Also satisfying for players who notice patterns.

---

## Forward-Only Citizens

Citizens generate forward, not backward. They don't contradict history.

### Rules

1. Citizens only generate `possible` moments, never `spoken`
2. Citizens never modify existing moments
3. If a citizen generates something that contradicts history, it's discarded
4. THEN links are immutable — the history is sacred

**Player Experience:** Characters don't suddenly forget what they said. The game's memory is perfect. Callbacks work because the past is fixed.

**Rating: 9/10** — Prevents contradiction. Essential for trust.

---

## Flashback Pattern

Backstory through environment. Places trigger memories.

### Schema

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

**Rating: 10/10** — Backstory earns its reveal through context. Discovery, not exposition.

---

## Rating Summary

| Pattern | Rating | Core Value |
|---------|--------|------------|
| Scene = Query | 7/10 | No scene object, just state |
| Place Atmosphere | 8/10 | Locations feel distinct |
| Character Location State | 7/10 | Required infrastructure |
| Time-Costing Actions | 9/10 | Conversations have opportunity cost |
| Time Passage Effects | 9/10 | World responds to time |
| Leave = Moment + Action | 9/10 | Departure is dialogue, not system |
| Return = Narrative + Conditions | 9/10 | Promises tracked, returns dramatic |
| Arrival = Travel Completion | 9/10 | Entrances have weight |
| Fetch Pattern | 9/10 | NPCs bring people to you |
| Go To Them Pattern | 8/10 | Information creates exploration |
| Stranger Arrives | 10/10 | NPCs have their own agency |
| Query Moment | 9/10 | Gaps are visible content |
| Query Triggers Generation | 10/10 | Questions get answers |
| ANSWERED_BY Link | 8/10 | Provenance preserved |
| Forward-Only Citizens | 9/10 | Prevents contradiction |
| Flashback Pattern | 10/10 | Backstory via environment |

**Infrastructure Average: 8.8/10**

---

## Implementation Checklist

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

## The Key Insight

**Everything is moments.**

- Leave = moment with action
- Arrival = moment triggered by presence
- Questions = moments that trigger generation
- Answers = moments linked back to questions

No special systems. Just moments and links.

---

*"The boring infrastructure is what makes the magic work."*

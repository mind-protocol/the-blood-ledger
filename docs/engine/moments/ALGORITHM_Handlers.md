# Moments — Algorithm: Character Handlers

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_Handlers.md (you are here)
ALGORITHMS:  ./ALGORITHM_Physics.md, ./ALGORITHM_Canon.md, ./ALGORITHM_Questions.md
SCHEMA:      ./SCHEMA_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
TEST:        ./TEST_Moments.md
IMPL:        ../../engine/handlers/character_handler.py
```

---

## Core Principle

**One handler per character. Triggered on flip. That's it.**

No arbitrary triggers. No cooldowns. No caps. The physics determines when handlers run.

---

## When Handlers Run

**On flip.** When a moment ATTACHED_TO this character crosses the flip threshold.

```python
def on_moment_flip(moment: Moment):
    """
    Called by Canon Holder when a moment flips.
    Triggers handler for the attached character.
    """
    character = query("""
        MATCH (m:Moment {id: $id})-[:ATTACHED_TO]->(c:Character)
        RETURN c
    """, id=moment.id)

    if character:
        run_handler(character.id, triggered_by=moment)
```

### Why No Other Triggers

- Character important and close? → More energy per tick → flips more often → handler runs more
- Character distant or minor? → Less energy → flips rarely → handler runs rarely

**The physics IS the scheduling.**

No cooldowns needed. Handler produces moments with weight. Those moments exist in the graph. Until they actualize or decay, character has potentials.

If potentials depleted → character's nodes have low weight → more energy flows to them (importance injection is low, but proximity injection still applies) → eventually something flips → handler runs.

---

## What Handler Receives

```python
@dataclass
class HandlerContext:
    character: Character          # Identity, beliefs, relationships, voice
    location: Place               # Where they are
    present: List[Character]      # Who else is here
    recent_history: List[Moment]  # Last N actualized moments they witnessed
    trigger: Moment               # What flipped to cause this run
    speed: SpeedSetting           # Current game speed (for prompt framing)
```

### Context Assembly

```python
def build_handler_context(character_id: str, trigger: Moment) -> HandlerContext:
    character = get_character(character_id)
    location = get_character_location(character_id)
    present = get_characters_at(location.id)

    recent_history = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT 10
    """, char_id=character_id)

    return HandlerContext(
        character=character,
        location=location,
        present=present,
        recent_history=recent_history,
        trigger=trigger,
        speed=get_current_speed()
    )
```

---

## What Handler Produces

```python
@dataclass
class HandlerOutput:
    moments: List[MomentDraft]      # New potential moments
    links: List[LinkDraft]           # CAN_LEAD_TO, ATTACHED_TO, REFERENCES
    questions: List[str]             # Queries for Question Answerer
```

### MomentDraft

```python
@dataclass
class MomentDraft:
    text: str                        # The content
    type: str                        # dialogue, thought, action, narration
    action: Optional[str]            # travel, take, attack, give (if action)
    tone: Optional[str]              # whispered, shouted, cold, warm
    # Note: NO weight field. Physics assigns weight.
```

### Handler Does NOT Set Weight

Handler outputs text + links. Physics assigns weight based on:
- Relevance to trigger (semantic proximity to triggering moment)
- Character's current importance

No handler can "force" a high-weight moment. It proposes. Physics evaluates.

---

## Handler Implementation

```python
async def run_handler(character_id: str, triggered_by: Moment) -> HandlerOutput:
    """
    Run the character's handler. Returns new potentials.
    """
    context = build_handler_context(character_id, triggered_by)

    # Build prompt based on character type and speed
    prompt = build_handler_prompt(context)

    # LLM call
    response = await llm.complete(prompt)

    # Parse structured output
    output = parse_handler_response(response)

    # Inject into graph (physics assigns weights)
    inject_handler_output(character_id, output)

    return output
```

### Prompt Framing by Speed

```python
def build_handler_prompt(context: HandlerContext) -> str:
    base = f"""
    You are {context.character.name}.
    {context.character.voice_description}

    Location: {context.location.name}
    Present: {', '.join(c.name for c in context.present)}

    What just happened: {context.trigger.text}
    Recent history: {format_history(context.recent_history)}

    Generate potential moments (things you might say, think, or do).
    """

    # Speed-aware framing
    if context.speed == '2x':
        base += """
        You're on a journey. Generate brief atmospheric moments,
        not full dialogue. Unless something important needs to be said.
        """
    elif context.speed == '3x':
        base += """
        Time is passing quickly. Only generate moments if something
        critical demands attention.
        """

    return base
```

---

## Weight Assignment (Physics Side)

```python
def inject_handler_output(character_id: str, output: HandlerOutput):
    """
    Inject handler output into graph. Physics assigns weights.
    """
    character = get_character(character_id)
    character_importance = calculate_importance(character_id)

    for draft in output.moments:
        # Calculate initial weight
        relevance = calculate_relevance(draft, output.trigger)
        initial_weight = relevance * character_importance * BASE_WEIGHT_FACTOR

        # Clamp to valid range
        initial_weight = max(0.1, min(0.7, initial_weight))

        # Create moment
        moment_id = create_moment(
            text=draft.text,
            type=draft.type,
            action=draft.action,
            tone=draft.tone,
            weight=initial_weight,
            status='possible'
        )

        # Create ATTACHED_TO link
        create_link('ATTACHED_TO', moment_id, character_id, {
            'presence_required': True,
            'persistent': True
        })

    # Process additional links
    for link in output.links:
        create_link(link.type, link.from_id, link.to_id, link.properties)

    # Queue questions for async answering
    for question in output.questions:
        question_answerer.queue(character_id, question)
```

---

## Handler Scaling

| Character Type | Handler Complexity |
|----------------|-------------------|
| Major (companions, antagonists) | Full LLM, rich context |
| Minor (named NPCs) | Lighter LLM, focused context |
| Grouped (guards, crowd) | Single handler for group |

### Grouped Characters

"The Guards" can be a single character node until narrative needs differentiation.

```yaml
Character:
  id: char_guards
  name: "The Guards"
  type: group
```

They flip. Their handler runs. They act as one. 20 peasants = 1 handler, not 20 LLM calls.

### Splitting Groups

Triggered by direct address or action targeting individual:

```python
def handle_direct_address(input_text: str, target: str):
    """
    Player addresses individual in a group.
    """
    # "You there, guard on the left!"
    if is_group_member_address(target):
        group = get_parent_group(target)
        individual = split_from_group(group, target)
        # individual now has own node, inherits group properties
```

Handler can also request split:

```python
# In handler output
{
    "split_request": {
        "from_group": "char_guards",
        "new_character": {
            "name": "The Tall Guard",
            "reason": "He steps forward, breaking ranks"
        }
    }
}
```

---

## Parallel Execution

Multiple flips = multiple parallel handler calls.

```python
async def process_flips(flipped_moments: List[Moment]):
    """
    Run handlers in parallel for all flipped moments.
    """
    tasks = []

    for moment in flipped_moments:
        character = get_attached_character(moment)
        if character:
            task = run_handler(character.id, triggered_by=moment)
            tasks.append(task)

    # Parallel execution
    results = await asyncio.gather(*tasks)

    # Each handler only writes its own character
    # No conflicts because of isolation
```

### Why Parallel Is Safe

Each handler only writes for its character. Handler isolation is an invariant. No conflicts possible.

4 flips = 4 parallel LLM calls. Wall-clock time is ~one call, not four sequential.

---

## Reaction Scope

**Handlers only write for their own character.**

Aldric speaks. Mildred flinches. Who writes the flinch?

NOT Aldric's handler.

```
Aldric speaks (moment actualizes)
  → Energy propagates to Mildred (she witnessed, ATTACHED_TO link)
  → Her weight increases
  → She flips
  → Her handler runs
  → She generates flinch potential
  → Flinch may actualize
```

Each handler only writes its own character. Reactions propagate through energy.

---

## Pre-Generation Strategy

The graph should never be sparse for active characters.

```python
def on_character_enters_scene(character_id: str, location_id: str):
    """
    Pre-generate potentials when character enters.
    """
    # Create a synthetic "arrival" moment
    arrival = create_moment(
        text=f"{character.name} arrives.",
        type='narration',
        weight=0.5,
        status='active'
    )

    # Trigger handler with arrival as trigger
    run_handler(character_id, triggered_by=arrival)

    # By the time player engages, potentials exist
```

If truly novel (player says something completely unexpected):
- Energy flows → player character receives it (always present)
- Player character's handler runs
- "You're not sure anyone knows how to respond to that."

The player character is the fallback. They always have something.

---

## What Handler Does NOT Do

- Decide what actualizes (only proposes)
- Write for other characters (scope isolation)
- Modify world state directly (that's Action Processing)
- Set weights (that's Physics)

---

## Invariants

1. **Scope isolation:** Handler only writes for its character
2. **Triggered by flip:** No other triggers (physics is scheduler)
3. **No weight control:** Handler proposes, physics assigns weight
4. **Parallel safe:** Multiple handlers can run simultaneously

---

*"The physics IS the scheduling."*

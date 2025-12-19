# Physics — Algorithm: Action Processing

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Actions.md (you are here)
ALGORITHMS:     ./ALGORITHM_Physics.md, ./ALGORITHM_Canon.md, ./ALGORITHM_Handlers.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
IMPL:           ../../engine/orchestration/orchestrator.py (action queue)
```

---

## Core Principle

**Moments with action fields modify world state.**

Everything is a moment. But moments with `action` field have consequences beyond display. They change the graph structure (AT links, health, possessions, relationships).

---

## Why Actions Are Special

| Moment Type | Affects Display | Affects Graph State |
|-------------|-----------------|---------------------|
| dialogue | Yes | No |
| thought | Yes | No |
| narration | Yes | No |
| action | Yes | **Yes** |

Physics doesn't distinguish — all propagate energy the same way.
Canon Holder doesn't distinguish — all get THEN links.
**Action Processing distinguishes** — only actions modify world state.

---

## Action Queue

Actions are processed sequentially to prevent conflicts.

```python
class ActionQueue:
    """
    Sequential queue for world-state-modifying actions.
    Order determined by canon arrival order.
    """
    def __init__(self):
        self.queue = []

    def add(self, moment: Moment):
        if moment.action:
            self.queue.append(moment)

    def process_next(self) -> Optional[ActionResult]:
        if not self.queue:
            return None

        moment = self.queue.pop(0)
        return process_action(moment)
```

---

## Action Processing Steps

```python
def process_action(moment: Moment) -> ActionResult:
    """
    Process a single action moment.
    """
    # 1. VALIDATE — Is action still possible?
    if not validate_action(moment):
        return ActionResult(
            success=False,
            moment=moment,
            reason="Action no longer valid"
        )

    # 2. EXECUTE — Modify graph state
    execute_action(moment)

    # 3. CONSEQUENCES — Generate consequence moments
    consequences = generate_consequences(moment)

    # 4. INJECT — Consequences enter graph with energy
    for consequence in consequences:
        inject_consequence(consequence)

    return ActionResult(success=True, moment=moment, consequences=consequences)
```

---

## Step 1: Validate

Check if action is still possible given current state.

```python
def validate_action(moment: Moment) -> bool:
    """
    Validate action against current world state.
    """
    action = moment.action
    actor = get_actor(moment)

    if action == 'travel':
        # Can actor travel to destination?
        destination = moment.action_target
        return can_travel_to(actor, destination)

    elif action == 'take':
        # Is thing still present and unowned?
        thing = moment.action_target
        return is_thing_available(thing, actor.location)

    elif action == 'attack':
        # Is target still present and alive?
        target = moment.action_target
        return is_target_attackable(target, actor)

    elif action == 'give':
        # Does actor have the thing? Is recipient present?
        thing = moment.action_target
        recipient = moment.action_recipient
        return actor_has_thing(actor, thing) and is_present(recipient, actor.location)

    return True
```

### Why Validation?

Between canon recording and action processing, state may have changed:
- Another action executed first
- Time passed
- World event occurred

Validation catches stale actions.

---

## Step 2: Execute

Modify graph state based on action type.

```python
def execute_action(moment: Moment):
    """
    Execute the action — modify graph state.
    """
    action = moment.action
    actor = get_actor(moment)

    if action == 'travel':
        execute_travel(actor, moment.action_target)

    elif action == 'take':
        execute_take(actor, moment.action_target)

    elif action == 'attack':
        execute_attack(actor, moment.action_target)

    elif action == 'give':
        execute_give(actor, moment.action_target, moment.action_recipient)
```

### Travel

```python
def execute_travel(actor: Character, destination_id: str):
    """
    Move character to new location.
    """
    # Remove old AT link
    query("""
        MATCH (c:Character {id: $char_id})-[r:AT]->(:Place)
        DELETE r
    """, char_id=actor.id)

    # Create new AT link
    query("""
        MATCH (c:Character {id: $char_id})
        MATCH (p:Place {id: $place_id})
        CREATE (c)-[:AT]->(p)
    """, char_id=actor.id, place_id=destination_id)

    # Handle moment dormancy (see ALGORITHM_Lifecycle.md)
    handle_location_change(actor.id, destination_id)
```

### Take

```python
def execute_take(actor: Character, thing_id: str):
    """
    Character takes a thing.
    """
    # Remove thing's AT link
    query("""
        MATCH (t:Thing {id: $thing_id})-[r:AT]->(:Place)
        DELETE r
    """, thing_id=thing_id)

    # Create CARRIES link
    query("""
        MATCH (c:Character {id: $char_id})
        MATCH (t:Thing {id: $thing_id})
        CREATE (c)-[:CARRIES]->(t)
    """, char_id=actor.id, thing_id=thing_id)
```

### Attack

```python
def execute_attack(actor: Character, target_id: str):
    """
    Character attacks target.
    """
    target = get_character(target_id)

    # Calculate damage (simplified)
    damage = calculate_damage(actor, target)

    # Update target health
    query("""
        MATCH (c:Character {id: $target_id})
        SET c.health = c.health - $damage
    """, target_id=target_id, damage=damage)

    # Check for death
    if target.health - damage <= 0:
        execute_death(target_id)

    # Update relationship
    query("""
        MATCH (a:Character {id: $actor_id})
        MATCH (t:Character {id: $target_id})
        MERGE (a)-[r:RELATIONSHIP]->(t)
        SET r.hostility = coalesce(r.hostility, 0) + 0.5
    """, actor_id=actor.id, target_id=target_id)
```

### Give

```python
def execute_give(actor: Character, thing_id: str, recipient_id: str):
    """
    Character gives thing to recipient.
    """
    # Remove actor's CARRIES link
    query("""
        MATCH (c:Character {id: $actor_id})-[r:CARRIES]->(t:Thing {id: $thing_id})
        DELETE r
    """, actor_id=actor.id, thing_id=thing_id)

    # Create recipient's CARRIES link
    query("""
        MATCH (c:Character {id: $recipient_id})
        MATCH (t:Thing {id: $thing_id})
        CREATE (c)-[:CARRIES]->(t)
    """, recipient_id=recipient_id, thing_id=thing_id)
```

---

## Step 3: Generate Consequences

Actions produce consequence moments.

```python
def generate_consequences(moment: Moment) -> List[Moment]:
    """
    Generate consequence moments from action.
    """
    consequences = []
    action = moment.action
    actor = get_actor(moment)

    if action == 'travel':
        # Departure noticed
        consequences.append(create_consequence(
            text=f"{actor.name} leaves.",
            type='narration',
            attached_to=moment.location  # Old location
        ))
        # Arrival noticed
        consequences.append(create_consequence(
            text=f"{actor.name} arrives.",
            type='narration',
            attached_to=moment.action_target  # New location
        ))

    elif action == 'take':
        thing = get_thing(moment.action_target)
        consequences.append(create_consequence(
            text=f"{actor.name} takes the {thing.name}.",
            type='narration',
            attached_to=actor.id
        ))

    elif action == 'attack':
        target = get_character(moment.action_target)
        consequences.append(create_consequence(
            text=f"{actor.name} strikes at {target.name}.",
            type='action',
            attached_to=actor.id
        ))
        # Witness reactions will be generated by their handlers

    elif action == 'give':
        thing = get_thing(moment.action_target)
        recipient = get_character(moment.action_recipient)
        consequences.append(create_consequence(
            text=f"{actor.name} gives the {thing.name} to {recipient.name}.",
            type='narration',
            attached_to=actor.id
        ))

    return consequences
```

---

## Step 4: Inject Consequences

Consequence moments enter graph and may trigger further physics.

```python
def inject_consequence(consequence: Moment):
    """
    Inject consequence moment into graph.
    """
    # Create moment with initial energy
    moment_id = create_moment(
        text=consequence.text,
        type=consequence.type,
        weight=CONSEQUENCE_INITIAL_WEIGHT,  # e.g., 0.6
        status='possible'
    )

    # Create links
    create_link('ATTACHED_TO', moment_id, consequence.attached_to, {
        'presence_required': True,
        'persistent': False  # Consequences are ephemeral
    })

    # Physics takes over — consequence may flip, trigger handlers
```

---

## Mutex Handling

If two characters attempt same action on same target:

```python
def handle_action_mutex(action_a: Moment, action_b: Moment):
    """
    Two actions targeting same thing/character.
    First in queue succeeds, second gets blocked.
    """
    # First action already processed (it's first in queue)
    # Second action validation will fail

    # Generate "blocked" consequence
    actor_b = get_actor(action_b)
    blocked_consequence = create_consequence(
        text=f"{actor_b.name} reaches for it, but too late.",
        type='narration',
        attached_to=actor_b.id
    )

    inject_consequence(blocked_consequence)

    # Blocked consequence triggers actor_b's handler
    # Handler can generate reaction: frustration, new plan, etc.
```

---

## Action Types Reference

| Action | Modifies | Consequences |
|--------|----------|--------------|
| `travel` | Character AT links | Departure/arrival notices |
| `take` | Thing AT/CARRIES links | Observation moment |
| `attack` | Health, relationships | Strike moment, witness reactions |
| `give` | CARRIES links | Transfer observation |
| `speak` | Nothing (just moment) | None |

---

## Sequential Processing

Actions MUST be sequential.

```
Aldric grabs sword (action enters queue)
Mildred grabs sword (action enters queue)
    ↓
Process Aldric's action (succeeds, sword now CARRIED by Aldric)
    ↓
Process Mildred's action (validation fails, sword not available)
    ↓
Mildred gets "blocked" consequence
    ↓
Mildred's handler triggered (generates frustration/reaction)
```

This is not mutex detection — it's natural sequencing. First in queue wins.

---

## What Action Processing Does NOT Do

- Run in parallel (must be sequential)
- Generate dialogue (that's Handlers)
- Decide action priority (that's Canon order)

---

## Invariants

1. **Sequential execution:** One action at a time
2. **Validation first:** Check before execute
3. **Consequences propagate:** Actions generate observable moments
4. **State consistency:** No conflicting graph modifications

---

*"Actions are where moments change the world."*

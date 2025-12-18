# Moments — Algorithm: Canon Holder

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_Canon.md (you are here)
ALGORITHMS:  ./ALGORITHM_Physics.md, ./ALGORITHM_Handlers.md, ./ALGORITHM_Actions.md
SCHEMA:      ./SCHEMA_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
TEST:        ./TEST_Moments.md
IMPL:        ../../engine/canon/canon_holder.py
```

---

## Core Principle

**Canon Holder records what becomes real. It creates history.**

Canon Holder does not decide what happens. Physics decides (via flip detection). Canon Holder records, orders, and emits.

---

## When Active

Continuously. As flips are detected by Physics, Canon Holder records them.

---

## What Canon Holder Does

```python
def record(moment: Moment):
    """
    Record a flipped moment as canon.
    """
    # 1. ORDER — Moments are processed in weight order
    # (Physics already sends them sorted)

    # 2. RECORD — Create THEN links (history)
    create_history_links(moment)

    # 3. ACCOUNT — Track duration for time passage
    accumulate_duration(moment)

    # 4. EMIT — Send to display queue
    display_queue.add(moment)

    # 5. TRIGGER — If action moment, queue for action processing
    if moment.action:
        action_queue.add(moment)

    # 6. NOTIFY — Trigger handlers for attached characters
    trigger_character_handlers(moment)
```

---

## Step 1: Ordering

Flipped moments arrive in weight order (highest first). This is the canonical sequence.

```python
def receive_flips(moments: List[Moment]):
    """
    Receive flipped moments from Physics.
    Already sorted by weight descending.
    """
    for moment in moments:
        record(moment)
```

---

## Step 2: Create History Links (THEN)

Every actualized moment gets THEN links connecting it to history.

```python
def create_history_links(moment: Moment):
    """
    Create THEN links recording what this moment followed.
    THEN links are immutable history.
    """
    current_tick = get_current_tick()

    # Link to previous active moments at this location
    previous = query("""
        MATCH (m:Moment {status: 'spoken'})
        WHERE m.tick_spoken < $tick
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT 3
    """, tick=current_tick)

    for prev in previous:
        create_link('THEN', prev.id, moment.id, {
            'tick': current_tick,
            'player_caused': is_player_caused(moment)
        })

    # Update moment status
    query("""
        MATCH (m:Moment {id: $id})
        SET m.status = 'spoken',
            m.tick_spoken = $tick
    """, id=moment.id, tick=current_tick)
```

### THEN Link Properties

```yaml
THEN:
  from: Moment (what came before)
  to: Moment (what came after)
  tick: int               # When this transition happened
  player_caused: bool     # Player triggered vs system triggered
```

### Immutability

**THEN links are never deleted or modified.** They are permanent history.

---

## Step 3: Duration Accounting

Every moment has duration. Canon Holder tracks accumulated time.

```python
def accumulate_duration(moment: Moment):
    """
    Track time passage as moments actualize.
    """
    scene_state.elapsed_time += moment.duration

    # Check for time-triggered events
    if scene_state.elapsed_time >= next_scheduled_event.time:
        inject_scheduled_event(next_scheduled_event)

    # Check for time-of-day transitions
    if should_transition_time_of_day(scene_state.elapsed_time):
        inject_time_transition()
```

### Duration by Type

| Moment Type | Duration Range |
|-------------|----------------|
| Thought | 1 unit |
| Dialogue | 1-5 units (by length) |
| Short action | 5-30 units |
| Long action | Hours |

---

## Step 4: Emit to Display

Canon moments enter the display queue for frontend rendering.

```python
def emit_to_display(moment: Moment):
    """
    Send canon moment to display queue.
    """
    display_payload = {
        'id': moment.id,
        'text': moment.text,
        'type': moment.type,
        'speaker': resolve_speaker(moment) if moment.type == 'dialogue' else None,
        'tone': moment.tone,
        'duration': moment.duration,
        'clickable_words': get_clickable_words(moment),
        'weight': moment.weight  # For display filtering at speed
    }

    display_queue.add(display_payload)
```

---

## Simultaneous Actions Are Drama

**Old thinking:** Aldric grabs sword + Mildred grabs sword = mutex = resolve conflict.

**New thinking:** Both actualize. Both canon.

```
"Aldric reaches for the sword."
"Mildred's hand closes on the hilt at the same moment."
```

That's not a problem. That's a scene. The consequences play out:
- Struggle moment generated
- Tension increases
- Drama emerges

Canon Holder does NOT block simultaneous actions. It records them both.

---

## True Mutex (Rare)

True mutex = logically impossible, not just dramatic.

### Same Character, Incompatible Actions

```
Aldric "walks east" AND Aldric "walks west" (same tick)
```

This is impossible. Resolution:

```python
def detect_same_character_mutex(moments: List[Moment]) -> List[Tuple[Moment, Moment]]:
    """
    Find moments where same character has incompatible actions.
    """
    by_character = group_by_character(moments)

    conflicts = []
    for char_id, char_moments in by_character.items():
        action_moments = [m for m in char_moments if m.action]
        if len(action_moments) > 1:
            # Check compatibility
            for a, b in combinations(action_moments, 2):
                if are_incompatible(a.action, b.action):
                    conflicts.append((a, b))

    return conflicts
```

### Resolution

Higher weight wins. Lower becomes potential for next tick.

```python
def resolve_mutex(moment_a: Moment, moment_b: Moment):
    """
    Higher weight wins. Loser returns to potential.
    """
    winner, loser = (moment_a, moment_b) if moment_a.weight > moment_b.weight else (moment_b, moment_a)

    # Winner proceeds to canon
    record(winner)

    # Loser returns to possible, decayed
    query("""
        MATCH (m:Moment {id: $id})
        SET m.status = 'possible',
            m.weight = m.weight * 0.5
    """, id=loser.id)
```

### What's Incompatible

| Action A | Action B | Mutex? |
|----------|----------|--------|
| travel east | travel west | Yes |
| attack X | attack X | No (both attack) |
| take sword | take sword | No (drama: struggle) |
| speak | speak | No (both speak) |

Most "conflicts" are actually drama to embrace.

---

## History Links Are Queryable

THEN chains form traversable history.

```python
def get_character_history(character_id: str, limit: int = 20) -> List[Moment]:
    """
    What did this character witness?
    """
    return query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT $limit
    """, char_id=character_id, limit=limit)

def get_place_history(place_id: str, limit: int = 20) -> List[Moment]:
    """
    What happened at this place?
    """
    return query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(p:Place {id: $place_id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT $limit
    """, place_id=place_id, limit=limit)

def get_conversation_chain(moment_id: str) -> List[Moment]:
    """
    Follow THEN links to reconstruct conversation.
    """
    return query("""
        MATCH path = (start:Moment {id: $id})-[:THEN*]->(end:Moment)
        RETURN nodes(path) AS moments
        ORDER BY length(path) DESC
        LIMIT 1
    """, id=moment_id)
```

The graph IS the log. No separate history storage.

---

## What Canon Holder Does NOT Do

- Generate new content (that's Handlers)
- Block drama (simultaneous actions are fine)
- Second-guess physics (if it flipped, it's canon)
- Modify world state (that's Action Processing)

---

## Invariants

1. **Once canon, always canon:** THEN links never deleted
2. **Order matters:** Weight order is canonical sequence
3. **Drama welcome:** Simultaneous actions are scenes, not conflicts
4. **History traversable:** THEN chains are queryable

---

*"Once Canon Holder records, it happened."*

# Moments — Algorithm: Transitions

```
CREATED: 2024-12-17
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_Transitions.md (you are here)
ALGORITHMS:  ./ALGORITHM_View_Query.md, ./ALGORITHM_Lifecycle.md
SCHEMA:      ./SCHEMA_Moments.md
API:         ./API_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
IMPL:        ../../engine/orchestration/, ../../engine/api/app.py
```

---

## What Transitions Do

A transition moves the conversation from one moment to another. It:
1. Actualizes the target moment
2. Creates a THEN link (history)
3. Optionally consumes the origin moment

---

## Click Transition

Player clicks a word in an active moment.

```python
def handle_click(player_id: str, moment_id: str, word: str) -> List[Moment]:
    """
    Handle player clicking a word.
    Returns list of newly activated moments.
    """
    # 1. Find the transition
    link = query("""
        MATCH (m:Moment {id: $moment_id})-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE r.trigger = 'click'
          AND $word IN r.require_words
        RETURN r, next
        ORDER BY next.weight DESC
        LIMIT 1
    """, moment_id=moment_id, word=word.lower())

    if not link:
        return []  # No transition for this word

    # 2. Actualize the target
    activated = actualize_moment(link.next.id)

    # 3. Create history link
    create_then_link(
        from_id=moment_id,
        to_id=link.next.id,
        tick=current_tick(),
        player_caused=True
    )

    # 4. Consume origin if specified
    if link.r.consumes_origin:
        update("""
            MATCH (m:Moment {id: $id})
            SET m.status = 'spoken', m.tick_spoken = $tick
        """, id=moment_id, tick=current_tick())

    return activated
```

---

## Wait Transition

Time passes, player hasn't acted.

```python
def check_wait_transitions(active_moment_ids: List[str], current_tick: int) -> List[Moment]:
    """
    Check for wait transitions that should fire.
    Called each tick or after player inactivity.
    """
    activated = []

    links = query("""
        MATCH (m:Moment)-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE m.id IN $active_ids
          AND r.trigger = 'wait'
          AND m.tick_spoken IS NOT NULL
          AND (current_tick - m.tick_spoken) >= r.wait_ticks
        RETURN m, r, next
    """, active_ids=active_moment_ids)

    for link in links:
        # Actualize target
        activated.extend(actualize_moment(link.next.id))

        # Create history
        create_then_link(
            from_id=link.m.id,
            to_id=link.next.id,
            tick=current_tick,
            player_caused=False  # System triggered
        )

        # Consume if specified
        if link.r.consumes_origin:
            update("""
                MATCH (m:Moment {id: $id})
                SET m.status = 'spoken'
            """, id=link.m.id)

    return activated
```

---

## Actualize Moment

Make a moment active.

```python
def actualize_moment(moment_id: str) -> List[Moment]:
    """
    Transition a moment to active status.
    Returns the moment and any auto-triggered follow-ups.
    """
    # Update status
    moment = update("""
        MATCH (m:Moment {id: $id})
        SET m.status = 'active',
            m.tick_spoken = $tick,
            m.weight = CASE WHEN m.weight < 0.8 THEN 0.8 ELSE m.weight END
        RETURN m
    """, id=moment_id, tick=current_tick())

    result = [moment]

    # Check for auto-transitions
    auto_links = query("""
        MATCH (m:Moment {id: $id})-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE r.trigger = 'auto'
        RETURN next
    """, id=moment_id)

    for link in auto_links:
        result.extend(actualize_moment(link.next.id))
        create_then_link(moment_id, link.next.id, current_tick(), False)

    return result
```

---

## Create THEN Link

Record what happened.

```python
def create_then_link(from_id: str, to_id: str, tick: int, player_caused: bool):
    """
    Create a THEN link recording the transition.
    THEN links are permanent history.
    """
    query("""
        MATCH (from:Moment {id: $from_id})
        MATCH (to:Moment {id: $to_id})
        CREATE (from)-[:THEN {
            tick: $tick,
            player_caused: $player_caused
        }]->(to)
    """, from_id=from_id, to_id=to_id, tick=tick, player_caused=player_caused)
```

---

## Bidirectional Transitions

When bidirectional is true, the link works both ways.

```cypher
CAN_LEAD_TO:
  from: moment_a
  to: moment_b
  bidirectional: true
  require_words: ["more"]
```

Query must check both directions:

```python
def find_transition(moment_id: str, word: str):
    return query("""
        // Forward direction
        MATCH (m:Moment {id: $id})-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE r.trigger = 'click' AND $word IN r.require_words
        RETURN 'forward' AS direction, r, next

        UNION

        // Reverse direction (if bidirectional)
        MATCH (m:Moment {id: $id})<-[r:CAN_LEAD_TO]-(prev:Moment)
        WHERE r.trigger = 'click'
          AND $word IN r.require_words
          AND r.bidirectional = true
        RETURN 'reverse' AS direction, r, prev AS next
    """, id=moment_id, word=word.lower())
```

---

## Weight Transfer

Transitions can transfer weight from origin to target.

```python
def apply_weight_transfer(link, origin_moment, target_moment):
    if link.weight_transfer and link.weight_transfer > 0:
        transfer = origin_moment.weight * link.weight_transfer
        target_moment.weight = min(1.0, target_moment.weight + transfer)
```

This prevents infinite loops in bidirectional graphs — each traversal costs weight.

---

## Consume Origin

When consumes_origin is true:
- Origin moment status → 'spoken'
- Origin moment is no longer active
- Its transitions are no longer available

This creates one-way advancement. The conversation moved on.

When consumes_origin is false:
- Origin stays active
- Multiple paths remain open
- Player can still click other words in origin

---

## Multiple Transitions Same Word

If multiple CAN_LEAD_TO links have the same word in require_words:

```
moment_a ──[require_words: ["sword"]]──> moment_about_weapon
moment_a ──[require_words: ["sword"]]──> moment_about_fighting
```

Resolution: **Pick by target weight.** Highest weight target wins.

```python
links = query("""
    MATCH (m:Moment {id: $id})-[r:CAN_LEAD_TO]->(next:Moment)
    WHERE r.trigger = 'click' AND $word IN r.require_words
    RETURN r, next
    ORDER BY next.weight DESC
    LIMIT 1
""")
```

---

## Free Text Input

Player types instead of clicking.

```python
def handle_free_input(player_id: str, text: str) -> Moment:
    """
    Player typed something. Create a player moment.
    """
    # Create the player's moment
    moment_id = generate_id("moment")

    query("""
        CREATE (m:Moment {
            id: $id,
            text: $text,
            type: 'dialogue',
            status: 'spoken',
            tick_created: $tick,
            tick_spoken: $tick,
            weight: 1.0
        })
    """, id=moment_id, text=text, tick=current_tick())

    # Player is the speaker
    query("""
        MATCH (p:Character {id: $player_id})
        MATCH (m:Moment {id: $moment_id})
        CREATE (p)-[:CAN_SPEAK {weight: 1.0}]->(m)
    """, player_id=player_id, moment_id=moment_id)

    # Attach to current location
    location = get_player_location(player_id)
    query("""
        MATCH (m:Moment {id: $moment_id})
        MATCH (loc:Place {id: $loc_id})
        CREATE (m)-[:ATTACHED_TO {
            presence_required: false,
            persistent: true
        }]->(loc)
    """, moment_id=moment_id, loc_id=location.id)

    # Link from previous active moment
    previous = query("""
        MATCH (m:Moment {status: 'active'})-[:ATTACHED_TO]->(loc:Place {id: $loc_id})
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT 1
    """, loc_id=location.id)

    if previous:
        create_then_link(previous.id, moment_id, current_tick(), True)

    return get_moment(moment_id)
```

---

## Transition Flow Summary

```
Player clicks word in moment_a
    ↓
Find CAN_LEAD_TO link matching word
    ↓
Actualize target moment (status → active)
    ↓
Create THEN link (history)
    ↓
If consumes_origin: moment_a status → spoken
    ↓
Check for auto-transitions from target
    ↓
Return newly activated moments
    ↓
Frontend updates view
```

---

*"The conversation is a graph you walk, not a tree you descend."*

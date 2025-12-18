# Moments — Algorithm: Lifecycle

```
CREATED: 2024-12-17
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_Lifecycle.md (you are here)
ALGORITHMS:  ./ALGORITHM_View_Query.md, ./ALGORITHM_Transitions.md
SCHEMA:      ./SCHEMA_Moments.md
API:         ./API_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
IMPL:        ../../engine/db/graph_ops.py, ../../engine/orchestration/
```

---

## Status States

```
                    ┌─────────────┐
                    │  possible   │ ← Created by Narrator
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │  active  │     │ dormant  │     │ decayed  │
   └────┬─────┘     └────┬─────┘     └──────────┘
        │                │                 ▲
        │                │ (return)        │
        ▼                ▼                 │
   ┌──────────┐     ┌──────────┐          │
   │  spoken  │     │  active  │──────────┘
   └──────────┘     └──────────┘   (weight → 0)
```

| Status | Meaning |
|--------|---------|
| possible | Created, not yet shown. Weight determines if/when surfaces. |
| active | Currently visible. Can be interacted with. |
| spoken | Actualized. Part of history. Has outgoing THEN links. |
| dormant | Player left. Will reactivate on return (if persistent). |
| decayed | Weight dropped below threshold. Garbage collected. |

---

## Weight Decay

Each tick, unrealized moments decay:

```python
def decay_weights(current_tick: int):
    """
    Apply weight decay to possible moments.
    Called each world tick.
    """
    # Decay all possible moments
    update("""
        MATCH (m:Moment)
        WHERE m.status = 'possible'
        SET m.weight = m.weight * $decay_rate
    """, decay_rate=0.99)  # 1% decay per tick

    # Mark decayed
    update("""
        MATCH (m:Moment)
        WHERE m.status = 'possible' AND m.weight < $threshold
        SET m.status = 'decayed', m.tick_decayed = $tick
    """, threshold=0.1, tick=current_tick)
```

### Decay Rate

| Parameter | Value | Effect |
|-----------|-------|--------|
| decay_rate | 0.99 | 1% loss per tick |
| decay_threshold | 0.1 | Below this → decayed |

### Decay Timeline

| Initial Weight | Ticks to Decay |
|----------------|----------------|
| 1.0 | ~230 ticks |
| 0.8 | ~210 ticks |
| 0.5 | ~160 ticks |
| 0.3 | ~110 ticks |

---

## Weight Boost

Active moments resist decay and can gain weight:

```python
def boost_active_moments():
    """
    Active moments gain weight from visibility.
    """
    # Counter-decay for active moments
    update("""
        MATCH (m:Moment)
        WHERE m.status = 'active'
        SET m.weight = m.weight * 1.01  # Slight gain
    """)

    # Cap at 1.0
    update("""
        MATCH (m:Moment)
        WHERE m.weight > 1.0
        SET m.weight = 1.0
    """)
```

### Boost On Transition

When a moment is actualized:

```python
def on_actualize(moment_id: str):
    update("""
        MATCH (m:Moment {id: $id})
        SET m.weight = CASE
            WHEN m.weight < 0.8 THEN 0.8
            ELSE m.weight
        END
    """, id=moment_id)
```

---

## Dormancy

When player leaves a location, place-attached moments go dormant.

```python
def on_player_leaves(location_id: str):
    """
    Handle moments when player leaves a location.
    """
    # Persistent moments → dormant
    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(p:Place {id: $loc_id})
        WHERE r.persistent = true
          AND m.status IN ['possible', 'active']
        SET m.status = 'dormant'
    """, loc_id=location_id)

    # Non-persistent moments → deleted
    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(p:Place {id: $loc_id})
        WHERE r.persistent = false
        DETACH DELETE m
    """, loc_id=location_id)
```

### Character Leaves

Same logic for characters:

```python
def on_character_leaves(character_id: str, player_location_id: str):
    """
    Handle moments when a character leaves player's location.
    """
    # Check if character still in same location as player
    same_location = query("""
        MATCH (c:Character {id: $char_id})-[:AT]->(loc:Place {id: $loc_id})
        RETURN count(*) > 0
    """, char_id=character_id, loc_id=player_location_id)

    if same_location:
        return  # Character still with player, moments travel

    # Character left — handle their attached moments
    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE r.presence_required = true
          AND r.persistent = true
          AND m.status IN ['possible', 'active']
        SET m.status = 'dormant'
    """, char_id=character_id)

    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE r.presence_required = true
          AND r.persistent = false
        DETACH DELETE m
    """, char_id=character_id)
```

---

## Reactivation

When player returns to a location or character:

```python
def on_player_arrives(location_id: str):
    """
    Reactivate dormant moments at this location.
    """
    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(p:Place {id: $loc_id})
        WHERE m.status = 'dormant'
        SET m.status = 'possible'
    """, loc_id=location_id)

def on_character_rejoins(character_id: str):
    """
    Reactivate dormant moments attached to this character.
    """
    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status = 'dormant'
        SET m.status = 'possible'
    """, char_id=character_id)
```

### Dormant Weight

Dormant moments don't decay. Their weight is frozen.

---

## Garbage Collection

Decayed moments are deleted periodically:

```python
def garbage_collect(current_tick: int):
    """
    Remove decayed moments that are old enough.
    Keep recent decays for debugging.
    """
    retention_ticks = 100  # Keep for 100 ticks after decay

    update("""
        MATCH (m:Moment)
        WHERE m.status = 'decayed'
          AND m.tick_decayed < $cutoff
        DETACH DELETE m
    """, cutoff=current_tick - retention_ticks)
```

---

## dies_with_target

When a target node is destroyed:

```python
def on_node_destroyed(node_id: str):
    """
    Handle moments attached to a destroyed node.
    """
    update("""
        MATCH (m:Moment)-[r:ATTACHED_TO]->(target {id: $node_id})
        WHERE r.dies_with_target = true
        DETACH DELETE m
    """, node_id=node_id)
```

Example: Character dies → their secrets die with them.

---

## Lifecycle Events

### Moment Created

```python
def create_moment(text: str, type: str, weight: float = 0.8) -> str:
    moment_id = generate_id("moment")

    query("""
        CREATE (m:Moment {
            id: $id,
            text: $text,
            type: $type,
            status: 'possible',
            weight: $weight,
            tick_created: $tick,
            tick_spoken: null,
            tick_decayed: null
        })
    """, id=moment_id, text=text, type=type, weight=weight, tick=current_tick())

    return moment_id
```

### Moment Activated

```python
def activate_moment(moment_id: str):
    update("""
        MATCH (m:Moment {id: $id})
        SET m.status = 'active',
            m.tick_spoken = $tick
    """, id=moment_id, tick=current_tick())
```

### Moment Spoken (Consumed)

```python
def mark_spoken(moment_id: str):
    update("""
        MATCH (m:Moment {id: $id})
        SET m.status = 'spoken'
    """, id=moment_id)
```

---

## Tick Processing

Each world tick:

```python
def process_moment_tick(current_tick: int):
    """
    Called each world tick.
    """
    # 1. Decay weights
    decay_weights(current_tick)

    # 2. Boost active moments
    boost_active_moments()

    # 3. Check wait transitions
    active_ids = query("MATCH (m:Moment {status: 'active'}) RETURN m.id")
    check_wait_transitions(active_ids, current_tick)

    # 4. Garbage collect (occasionally)
    if current_tick % 10 == 0:
        garbage_collect(current_tick)
```

---

## Lifecycle Summary

| Event | Status Change | Weight Effect |
|-------|---------------|---------------|
| Created | → possible | Initial weight (default 0.8) |
| Visible | possible → active | Boost to 0.8 if lower |
| Clicked/Spoken | active → spoken | N/A |
| Left behind | active → dormant | Frozen |
| Returned | dormant → possible | Unfrozen |
| Decayed | possible → decayed | Dropped below 0.1 |
| Garbage collected | decayed → (deleted) | N/A |

---

*"Some moments are never flipped. They stay possibilities, or decay."*

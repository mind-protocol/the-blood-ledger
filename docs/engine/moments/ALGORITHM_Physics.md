# Moments — Algorithm: Physics Tick

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
THIS:        ALGORITHM_Physics.md (you are here)
ALGORITHMS:  ./ALGORITHM_Handlers.md, ./ALGORITHM_Canon.md, ./ALGORITHM_Speed.md
SCHEMA:      ./SCHEMA_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
TEST:        ./TEST_Moments.md
IMPL:        ../../engine/physics/tick.py
```

---

## Core Principle

**The graph is always running.**

The tick is not "processing a cascade." The tick is one heartbeat of a continuous system. The graph never stops. Speed controls how fast we tick and what we display.

---

## What Triggers a Tick

| Trigger | Notes |
|---------|-------|
| Time interval | Based on current speed setting |
| Player input | May trigger immediate tick |
| Handler completion | New potentials ready to integrate |

---

## Tick Steps (Sequential)

```python
def physics_tick(current_time: float):
    """
    One heartbeat of the continuous system.
    Steps must execute in order.
    """
    # 1. INJECT — Energy enters the system
    inject_energy()

    # 2. DECAY — Weights decrease over time
    apply_decay(current_time)

    # 3. PROPAGATE — Energy flows through links
    propagate_energy()

    # 4. DETECT — Find moments that crossed threshold
    flipped = detect_flips()

    # 5. EMIT — Send flipped moments to Canon Holder
    for moment in flipped:
        canon_holder.record(moment)
```

---

## Step 1: Energy Injection

Energy enters the system each tick. Characters receive energy based on importance and proximity.

### Importance (Dynamic)

```python
def calculate_importance(character_id: str) -> float:
    """
    Importance = sum of weights of all moments attached to this character.
    Character with many high-weight potentials = important right now.
    """
    moments = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status IN ['possible', 'active']
        RETURN sum(m.weight) AS total
    """, char_id=character_id)

    return moments.total or 0.0
```

Importance is not a property. It's derived from the graph state. It changes constantly.

### Proximity (Binary)

```python
def calculate_proximity(character_id: str, player_location_id: str) -> float:
    """
    You're here or you're not. No gradient.
    """
    is_present = query("""
        MATCH (c:Character {id: $char_id})-[:AT]->(p:Place {id: $loc_id})
        RETURN count(*) > 0
    """, char_id=character_id, loc_id=player_location_id)

    return 1.0 if is_present else 0.0
```

Characters not at player's location get zero injection here. They're in World Runner's domain.

### Injection Formula

```python
def inject_energy():
    """
    Each present character receives energy.
    Energy flows to their attached moments.
    """
    player_location = get_player_location()
    present_characters = get_characters_at(player_location.id)

    for character in present_characters:
        importance = calculate_importance(character.id)
        proximity = 1.0  # They're present

        energy = importance * proximity * INJECTION_MULTIPLIER

        # Energy goes to the character's moments
        query("""
            MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
            WHERE m.status = 'possible'
            SET m.weight = m.weight + $energy
        """, char_id=character.id, energy=energy)
```

---

## Step 2: Decay

Weights decrease over time. This is time-based, not tick-based.

```python
def apply_decay(current_time: float):
    """
    Decay is proportional to elapsed time.
    At 3x speed, ticks are faster but decay rate per real-time stays constant.
    """
    elapsed = current_time - last_tick_time
    decay_factor = 1.0 - (DECAY_RATE * elapsed)

    query("""
        MATCH (m:Moment)
        WHERE m.status = 'possible'
        SET m.weight = m.weight * $decay_factor
    """, decay_factor=decay_factor)
```

### Why Time-Based

If decay were tick-based, 3x speed would decay everything to zero before it could actualize. Time-based decay means the same real-world time produces the same decay regardless of tick rate.

---

## Step 3: Propagation

Energy flows through links. Transfer is lossy.

```python
def propagate_energy():
    """
    Energy spreads from high-weight nodes to connected nodes.
    Transfer efficiency determines how much is lost.
    """
    # Get all active/high-weight moments
    sources = query("""
        MATCH (m:Moment)
        WHERE m.weight > $propagation_threshold
        RETURN m
    """, propagation_threshold=0.3)

    for source in sources:
        # Find connected moments via CAN_LEAD_TO
        targets = query("""
            MATCH (source:Moment {id: $id})-[r:CAN_LEAD_TO]->(target:Moment)
            WHERE target.status = 'possible'
            RETURN target, r.weight_transfer AS transfer
        """, id=source.id)

        for target in targets:
            transferred = source.weight * target.transfer * TRANSFER_EFFICIENCY
            query("""
                MATCH (m:Moment {id: $id})
                SET m.weight = m.weight + $energy
            """, id=target.id, energy=transferred)
```

---

## Step 4: Detection

Identify moments that crossed the flip threshold.

```python
def detect_flips() -> List[Moment]:
    """
    Deterministic: weight >= threshold means flip.
    No randomness in v1.
    """
    flipped = query("""
        MATCH (m:Moment)
        WHERE m.status = 'possible'
          AND m.weight >= $threshold
        SET m.status = 'active'
        RETURN m
        ORDER BY m.weight DESC
    """, threshold=FLIP_THRESHOLD)

    return flipped
```

### Deterministic vs Probabilistic

For v1, flipping is deterministic. `weight >= 0.8` = flip.

Probabilistic (weight = probability per tick) adds organic feel but complicates reasoning. Can add later if mechanical feel is a problem.

---

## Step 5: Emit to Canon Holder

Flipped moments are sent to Canon Holder for recording and display.

```python
def emit_flips(flipped: List[Moment]):
    """
    Canon Holder receives flipped moments in weight order.
    It handles: ordering, recording THEN links, emitting to display.
    """
    for moment in sorted(flipped, key=lambda m: m.weight, reverse=True):
        canon_holder.record(moment)

        # Trigger handlers for attached characters
        character = get_attached_character(moment)
        if character:
            trigger_handler(character.id, triggered_by=moment)
```

---

## Parameters (Sensible Defaults)

These are starting points, not sacred. Tune in playtest.

| Parameter | Default | Notes |
|-----------|---------|-------|
| `FLIP_THRESHOLD` | 0.8 | When weight crosses this, moment flips |
| `DECAY_RATE` | 0.05 | 5% per time unit |
| `TRANSFER_EFFICIENCY` | 0.7 | 30% lost on propagation |
| `INJECTION_MULTIPLIER` | 0.1 | Scales importance to energy |
| `PROPAGATION_THRESHOLD` | 0.3 | Only propagate from nodes above this |

---

## Graph States

The graph is always running but exhibits different states:

| State | Characteristics |
|-------|-----------------|
| **Active** | High energy, many flips, drama unfolding |
| **Quiet** | Low energy, few flips, equilibrium |
| **Critical** | Energy building, thresholds approaching, tension rising |

But never **stopped**.

---

## Tick Rate by Speed

| Speed | Ticks Per Second | Notes |
|-------|------------------|-------|
| 1x | ~0.2 | One tick per moment duration |
| 2x | ~2.0 | Rapid, filtered display |
| 3x | Max system speed | Only interrupts shown |

See ALGORITHM_Speed.md for full speed controller logic.

---

## What Physics Does NOT Do

- Generate new moments (that's Handlers)
- Decide what content to create (that's Handlers)
- Record history (that's Canon Holder)
- Modify world state (that's Action Processing)
- Start or stop cascades (there is no cascade boundary)

Physics only: inject, decay, propagate, detect.

---

## Invariants

1. **Energy conservation:** Energy in = energy out + decay losses
2. **Continuous:** Graph never stops, only changes rate
3. **Deterministic flips:** Same state → same flips (for v1)
4. **Time-based decay:** Speed doesn't change total decay over real time

---

*"The tick is one heartbeat of a continuous system."*

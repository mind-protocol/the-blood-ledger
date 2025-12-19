# Canon Holder — Algorithm

```
UPDATED: 2025-12-19
STATUS: IMPLEMENTED
```

---

## Overview

Canon Holder is the gatekeeper. When a moment becomes canon (spoken), everything follows from that recording.

**No moment reaches the player without passing through Canon Holder.**

---

## Constants

```python
SURFACE_THRESHOLD = 0.3      # salience needed to flip possible → active
MAX_MOMENTS_PER_TICK = 3     # pacing limit
ACTUALIZATION_COST = 0.6     # energy multiplier on spoken (keeps 40%)
```

---

## Q1: Detect Ready Moments (possible → active)

Find moments ready to surface.

```cypher
MATCH (m:Moment)
WHERE m.status = 'possible'
  AND (m.weight * m.energy) >= $threshold
RETURN m.id, m.weight, m.energy, m.type, m.text
ORDER BY (m.weight * m.energy) DESC
```

Parameters: `threshold = 0.3`

For each result, check presence requirements (Q2).

---

## Q2: Check Presence Requirements

A moment can only surface if all presence-required targets are at player's location.

```cypher
MATCH (m:Moment {id: $moment_id})-[a:ATTACHED_TO {presence_required: true}]->(target)
WHERE NOT (target)-[:AT {present: 1.0}]->(:Place {id: $player_location})
RETURN count(target) AS missing_count
```

Parameters: `moment_id`, `player_location`

**Rule:** If `missing_count > 0`, moment cannot surface.

**Note:** Direct place match only. No CONTAINS traversal. Character in `place_merchants_hall` is NOT present if player is in `place_york_market`.

---

## Q3: Get Player Location

```cypher
MATCH (p:Character {id: 'char_player'})-[:AT {present: 1.0}]->(loc:Place)
RETURN loc.id AS player_location
```

---

## Q4: Flip Moment to Active

```cypher
MATCH (m:Moment {id: $moment_id})
SET m.status = 'active'
RETURN m
```

---

## Q5: Determine Speaker

Highest-weight CAN_SPEAK link from present, awake character.

```cypher
MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $moment_id})
MATCH (c)-[:AT {present: 1.0}]->(loc:Place {id: $player_location})
WHERE c.state = 'awake' AND c.alive = true
RETURN c.id AS speaker_id, r.strength AS strength
ORDER BY r.strength DESC
LIMIT 1
```

Parameters: `moment_id`, `player_location`

**Rules:**
- Returns NULL for narration moments (no CAN_SPEAK links)
- If no valid speaker for dialogue, moment stays active (not spoken)
- Speaker is NOT stored on moment — derived from SAID link created on record

---

## Q6: Record Moment to Canon (active → spoken)

Transaction: multiple mutations in sequence.

### Step 1: Update moment status

```cypher
MATCH (m:Moment {id: $moment_id})
SET m.status = 'spoken',
    m.tick_spoken = $tick,
    m.energy = m.energy * 0.4
RETURN m
```

### Step 2: Create SAID link (if speaker)

```cypher
MATCH (c:Character {id: $speaker_id})
MATCH (m:Moment {id: $moment_id})
CREATE (c)-[:SAID {tick: $tick}]->(m)
```

Skip if `speaker_id` is NULL (narration).

### Step 3: Create THEN link (if previous)

```cypher
MATCH (prev:Moment {id: $previous_id})
MATCH (m:Moment {id: $moment_id})
CREATE (prev)-[:THEN {tick: $tick, player_caused: $player_caused}]->(m)
```

Skip if `previous_id` is NULL (first moment).

---

## Q7: Get Last Spoken Moment

For THEN link chaining.

```cypher
MATCH (m:Moment {status: 'spoken'})
WHERE m.tick_spoken IS NOT NULL
RETURN m.id AS moment_id, m.tick_spoken AS tick
ORDER BY m.tick_spoken DESC
LIMIT 1
```

---

## Q8: Flip to Dormant (player leaves)

```cypher
MATCH (m:Moment {status: 'active'})-[a:ATTACHED_TO {presence_required: true, persistent: true}]->(target)
WHERE NOT (target)-[:AT {present: 1.0}]->(:Place {id: $new_location})
SET m.status = 'dormant'
RETURN m.id
```

---

## Q9: Reactivate Dormant (player returns)

```cypher
MATCH (m:Moment {status: 'dormant'})-[a:ATTACHED_TO {presence_required: true}]->(target)
WHERE (target)-[:AT {present: 1.0}]->(:Place {id: $player_location})
WITH m, count(a) AS required_count
MATCH (m)-[a2:ATTACHED_TO {presence_required: true}]->(target2)
WHERE (target2)-[:AT {present: 1.0}]->(:Place {id: $player_location})
WITH m, required_count, count(a2) AS present_count
WHERE required_count = present_count
SET m.status = 'active'
RETURN m.id
```

---

## Q10: Decay Check

```cypher
MATCH (m:Moment)
WHERE m.weight < 0.01 AND m.status <> 'decayed'
SET m.status = 'decayed'
RETURN m.id
```

---

## Process Flow

### detect_and_surface()

Called by tick loop.

```python
def detect_and_surface():
    player_location = query(Q3)
    
    # Find ready moments
    candidates = query(Q1, threshold=SURFACE_THRESHOLD)
    
    for m in candidates:
        # Check presence
        missing = query(Q2, moment_id=m.id, player_location=player_location)
        if missing > 0:
            continue
        
        # Check speaker for dialogue
        if m.type == 'dialogue':
            speaker = query(Q5, moment_id=m.id, player_location=player_location)
            if not speaker:
                continue
        
        # Flip to active
        query(Q4, moment_id=m.id)
        broadcast('moment_activated', {moment_id: m.id, weight: m.weight, text: m.text})
```

### process_ready_moments()

Called after surfacing, processes active → spoken.

```python
def process_ready_moments():
    player_location = query(Q3)
    previous = query(Q7)  # Last spoken moment
    
    active = query("""
        MATCH (m:Moment {status: 'active'})
        RETURN m ORDER BY (m.weight * m.energy) DESC
    """)
    
    processed = 0
    for m in active:
        if processed >= MAX_MOMENTS_PER_TICK:
            break
        
        # Determine speaker
        speaker_id = None
        if m.type == 'dialogue':
            result = query(Q5, moment_id=m.id, player_location=player_location)
            if not result:
                continue  # No speaker, skip
            speaker_id = result.speaker_id
        
        # Record to canon
        query(Q6_step1, moment_id=m.id, tick=current_tick)
        
        if speaker_id:
            query(Q6_step2, speaker_id=speaker_id, moment_id=m.id, tick=current_tick)
        
        if previous:
            query(Q6_step3, previous_id=previous.id, moment_id=m.id, 
                  tick=current_tick, player_caused=False)
        
        # Broadcast
        broadcast('moment_spoken', {
            moment_id: m.id,
            text: m.text,
            speaker: speaker_id,
            tick: current_tick
        })
        
        previous = m
        processed += 1
```

---

## SSE Events

| Event | When | Payload |
|-------|------|---------|
| `moment_activated` | Q4 executes | `{moment_id, weight, text}` |
| `moment_spoken` | Q6 completes | `{moment_id, text, speaker, tick}` |
| `moment_decayed` | Q8 or Q10 | `{moment_id}` |

---

## Integration Points

| Caller | When | Function |
|--------|------|----------|
| Tick loop | Every tick | `detect_and_surface()`, `process_ready_moments()` |
| Click handler | After traversal | `process_ready_moments()` (for target moment) |
| Narrator | After generation | Creates moments as 'possible', physics surfaces them |
| Location change | Player moves | Q8 (dormant), Q9 (reactivate) |

---

## Chain

- PATTERNS: `docs/infrastructure/canon/PATTERNS_Canon.md`
- BEHAVIORS: `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- **ALGORITHM: This file**
- VALIDATION: `docs/infrastructure/canon/VALIDATION_Canon.md`
- IMPLEMENTATION: `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- SYNC: `docs/infrastructure/canon/SYNC_Canon.md`

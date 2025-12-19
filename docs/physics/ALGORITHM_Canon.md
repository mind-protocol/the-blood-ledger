# Physics — Algorithm: Canon Holder

```
CREATED: 2024-12-18
STATUS: Canonical
UPDATED: 2024-12-18
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Canon.md (you are here)
ALGORITHMS:     ./ALGORITHM_Physics.md, ./ALGORITHM_Energy.md, ./ALGORITHM_Handlers.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
IMPL:           ../../engine/canon/holder.py
```

---

## Core Principle

**Everything is moments. Canon Holder is the gatekeeper.**

Canon Holder records what becomes real. It doesn't decide what happens — physics and handlers do that. Canon Holder makes it permanent.

---

## The Flow

```
Energy flows
  → salience crosses threshold
  → moment flips possible → active
  → Handler generates (if needed)
  → Canon Holder records
  → moment becomes spoken
  → THEN link created
  → Actions processed
  → Strength mechanics triggered
  → Time advances
```

---

## Canon Holder Responsibilities

| Responsibility | What It Does |
|----------------|--------------|
| **Record** | Flip moment `active` → `spoken` |
| **Link** | Create THEN link to previous moment |
| **Time** | Advance game time based on moment duration |
| **Trigger** | Process actions (travel, take, etc.) |
| **Strength** | Apply strength mechanics (Activation, Evidence, etc.) |
| **Notify** | Push to frontend |

---

## The Code Shape

```python
def record_to_canon(moment, previous_moment=None):
    """
    Moment becomes canon. Everything follows from this.
    """
    # 1. Status change
    moment.status = 'spoken'
    moment.tick_spoken = current_tick

    # 2. Energy cost (actualization)
    moment.energy *= (1 - ACTUALIZATION_COST)

    # 3. THEN link (history chain)
    if previous_moment:
        create_link(previous_moment, 'THEN', moment, {
            'tick': current_tick,
            'player_caused': is_player_input()
        })

    # 4. Time passage
    duration = estimate_moment_duration(moment)
    advance_time(minutes=duration)

    # 5. Strength mechanics
    apply_activation(moment)  # M1: speaker's beliefs reinforced
    apply_evidence(moment)    # M2: witnesses' beliefs affected
    apply_association(moment) # M3: co-occurring narratives linked

    # 6. Actions
    if moment.action:
        process_action(moment)

    # 7. Notify frontend
    push_to_display(moment)
```

---

## Flip Detection

Canon Holder doesn't detect flips. It *records* them.

**Who detects flips?**

Physics tick detects when moments cross the salience threshold.

```python
def detect_ready_moments():
    """
    Find moments ready to surface.
    Called each tick or on energy change.
    """
    return query("""
        MATCH (m:Moment)
        WHERE m.status = 'possible'
          AND (m.weight * m.energy) >= $threshold
          AND all_presence_requirements_met(m)
        RETURN m
        ORDER BY (m.weight * m.energy) DESC
    """, threshold=SURFACE_THRESHOLD)
```

**What happens with multiple?**

```python
def process_ready_moments(ready):
    """
    Multiple moments can be ready. Process in order.
    """
    previous = get_last_spoken_moment()

    for moment in ready:
        # Check still valid (state may have changed)
        if not still_valid(moment):
            continue

        # Flip to active
        moment.status = 'active'

        # Handler needed?
        if needs_handler(moment):
            # Async - handler will call record_to_canon when done
            dispatch_handler(moment, previous)
        else:
            # Direct record
            record_to_canon(moment, previous)

        previous = moment
```

---

## Status Progression

```
possible ──[salience >= threshold]──> active ──[canon recorded]──> spoken
    │                                    │
    │                                    └──[handler fails]──> possible (retry)
    │
    └──[energy decays below minimum]──> decayed

spoken ──[never changes]──> (permanent history)

dormant ──[presence satisfied + energy]──> possible
```

| Status | Meaning |
|--------|---------|
| `possible` | Could happen, competing for attention |
| `active` | Crossed threshold, being processed |
| `spoken` | Canon. Happened. Immutable. |
| `dormant` | Waiting for conditions (place, person) |
| `decayed` | Lost relevance, pruned |

---

## Who Speaks?

```python
def determine_speaker(moment):
    """
    Highest-weight CAN_SPEAK link from present character.
    """
    speakers = query("""
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $id})
        WHERE c.state = 'awake'
          AND (c)-[:AT]->(:Place)<-[:AT]-(:Character {id: 'player'})
        RETURN c, r.strength
        ORDER BY r.strength DESC
        LIMIT 1
    """, id=moment.id)

    return speakers[0] if speakers else None
```

---

## Rate Limiting

```python
MAX_MOMENTS_PER_TICK = 5
MIN_MOMENT_GAP_MS = 100  # For display pacing

def process_ready_moments(ready):
    processed = 0
    for moment in ready:
        if processed >= MAX_MOMENTS_PER_TICK:
            break  # Rest next tick

        # ... process ...
        processed += 1
```

**Player Experience:** Cascades can happen, but not overwhelming. 5 moments max per tick. Display paces them for readability.

---

## Actualization Cost

When a moment is recorded, it partially drains energy from the moment itself:

```python
ACTUALIZATION_COST = 0.6

def actualize_energy(moment):
    """
    Partial drain — recent speech still has presence.
    """
    moment.energy *= (1 - ACTUALIZATION_COST)
```

**Why partial (0.6):** Just-spoken moments still have presence. They fade naturally rather than vanishing.

---

## Strength Mechanics Applied

Canon Holder triggers three of the six strength mechanics on record:

### M1: Activation

```python
def apply_activation(moment):
    """
    Speaker's beliefs reinforced by speaking.
    """
    speaker = moment.speaker
    narratives = moment.attached_narratives()

    for narrative in narratives:
        link = get_link(speaker, 'BELIEVES', narrative)
        if link:
            base = 0.05 if moment.type == 'dialogue' else 0.03
            reinforce_link(link, amount=base)

        # ABOUT links activated
        for about_link in narrative.outgoing_about():
            reinforce_link(about_link, amount=0.03)
```

### M2: Evidence

```python
def apply_evidence(moment):
    """
    Witnesses' beliefs affected by what they saw.
    """
    witnesses = get_present_characters(moment.location)
    moment_narratives = moment.attached_narratives()

    for witness in witnesses:
        for narr in moment_narratives:
            # Confirming evidence
            for supported in get_linked(narr, 'SUPPORTS'):
                link = get_link(witness, 'BELIEVES', supported)
                if link:
                    reinforce_link(link, amount=narr.weight * 0.15)

            # Contradicting evidence
            for contradicted in get_linked(narr, 'CONTRADICTS'):
                link = get_link(witness, 'BELIEVES', contradicted)
                if link:
                    challenge_link(link, amount=narr.weight * 0.20)
```

### M3: Association

```python
def apply_association(moment):
    """
    Co-occurring narratives become linked.
    """
    current = moment.attached_narratives()

    # Recent narratives in same conversation
    recent = query("""
        MATCH (m:Moment)-[:THEN*1..3]->(current:Moment {id: $id})
        MATCH (m)-[:ATTACHED_TO]->(n:Narrative)
        WHERE m.tick > $threshold
        RETURN DISTINCT n
    """, id=moment.id, threshold=current_tick - 10)

    for a in current:
        for b in recent:
            if a.id != b.id:
                link = get_link(a, 'SUPPORTS', b)
                if link:
                    reinforce_link(link, amount=0.03)
                elif strength > 0.05:
                    create_link(a, 'SUPPORTS', b, strength=0.03)
```

---

## Action Processing

If moment has an action, Canon Holder triggers the action processor:

```python
def process_action(moment):
    """
    Execute world-changing action.
    """
    action = moment.action
    actor = moment.speaker
    target = get_action_target(moment)

    if action == 'travel':
        # Change AT link
        move_character(actor, target)

    elif action == 'take':
        # Change CARRIES link
        take_thing(actor, target)

    elif action == 'give':
        # Change CARRIES link
        give_thing(actor, target, recipient)

    elif action == 'attack':
        # Complex — may trigger combat
        initiate_combat(actor, target)

    elif action == 'use':
        # Thing-specific effects
        use_thing(actor, target)

    # Apply Commitment mechanic (M5)
    apply_commitment(actor, moment)
```

---

## Time Passage

```python
def estimate_moment_duration(moment):
    """
    How long does this moment take in game time?
    """
    base_minutes = {
        'dialogue': 0.5,
        'thought': 0.1,
        'action': 1.0,
        'narration': 0.2,
        'montage': 5.0
    }.get(moment.type, 0.5)

    # Adjust by text length
    words = len(moment.text.split())
    word_factor = 1 + (words / 50) * 0.5

    return base_minutes * word_factor


def advance_time(minutes):
    """
    Move game time forward.
    """
    game_state.current_time += timedelta(minutes=minutes)

    # Check for time-based events
    check_scheduled_events()

    # Decay check (large time jumps)
    if minutes > 30:
        run_decay_cycle()
```

---

## THEN Links

History chain. Created by Canon Holder, never manually.

```python
def create_then_link(previous, current):
    """
    Link moments in history.
    """
    create_link(previous, 'THEN', current, {
        'tick': current_tick,
        'player_caused': is_player_input(),
        'time_gap_minutes': time_between(previous, current)
    })
```

**Query pattern:** `MATCH (m1)-[:THEN*]->(m2)` for conversation history.

---

## Frontend Notification

```python
def push_to_display(moment):
    """
    Send moment to frontend for display.
    """
    payload = {
        'id': moment.id,
        'text': moment.text,
        'type': moment.type,
        'speaker': moment.speaker.name if moment.speaker else None,
        'tone': moment.tone,
        'clickable_words': extract_clickable(moment),
        'timestamp': game_state.current_time
    }

    websocket.send('moment', payload)
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
def detect_same_character_mutex(moments):
    """
    Find moments where same character has incompatible actions.
    """
    by_character = group_by_character(moments)

    conflicts = []
    for char_id, char_moments in by_character.items():
        action_moments = [m for m in char_moments if m.action]
        if len(action_moments) > 1:
            for a, b in combinations(action_moments, 2):
                if are_incompatible(a.action, b.action):
                    conflicts.append((a, b))

    return conflicts


def resolve_mutex(moment_a, moment_b):
    """
    Higher weight wins. Loser returns to potential.
    """
    winner, loser = (moment_a, moment_b) if moment_a.weight > moment_b.weight else (moment_b, moment_a)

    # Winner proceeds to canon
    record_to_canon(winner)

    # Loser returns to possible, decayed
    loser.status = 'possible'
    loser.weight *= 0.5
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

## History Is Queryable

THEN chains form traversable history.

```python
def get_character_history(character_id, limit=20):
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


def get_conversation_chain(moment_id):
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

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| `SURFACE_THRESHOLD` | 0.3 | salience (weight × energy) needed |
| `ACTUALIZATION_COST` | 0.6 | Partial energy drain on record |
| `MAX_MOMENTS_PER_TICK` | 5 | Rate limit |
| `MIN_MOMENT_GAP_MS` | 100 | Display pacing |

---

## Invariants

1. **Immutability:** Once `spoken`, a moment never changes status
2. **THEN chain:** Every `spoken` moment (except first) has exactly one incoming THEN link
3. **Time monotonic:** Game time only moves forward
4. **Rate limited:** Max 5 moments per tick
5. **Strength applied:** All three mechanics (Activation, Evidence, Association) run on every record
6. **Drama welcome:** Simultaneous actions are scenes, not conflicts

---

## What Canon Holder Does NOT Do

- Generate content (that's Handlers)
- Compute energy flow (that's Physics tick)
- Block drama (simultaneous actions are fine)
- Store tension (tension is computed)
- Decide what should happen (that's Physics + Handlers)

Canon Holder only: record, link, trigger, notify.

---

*"Canon Holder makes it real. Everything else is possibility."*

# Physics — Algorithm: Physics Tick

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
THIS:           ALGORITHM_Physics.md (you are here)
ALGORITHMS:     ./ALGORITHM_Energy.md, ./ALGORITHM_Handlers.md, ./ALGORITHM_Canon.md, ./ALGORITHM_Speed.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
IMPL:           ../../engine/physics/tick.py
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

    Energy model: see ALGORITHM_Energy.md for full details.
    Energy IS proximity — no separate focus tracking needed.
    """
    # 1. PUMP — Characters inject energy into narratives
    character_pumping()

    # 2. TRANSFER — Energy flows through narrative links
    transfer_energy()

    # 3. TENSION — Structural tensions concentrate energy
    tensions = detect_tensions()
    tension_injection(tensions)

    # 4. DECAY — Energy leaves the system
    apply_decay()

    # 5. WEIGHT — Recompute moment weights from sources
    recompute_moment_weights()

    # 6. DETECT — Find moments that crossed threshold
    flipped = detect_flips()

    # 7. EMIT — Send flipped moments to Canon Holder
    for moment in flipped:
        canon_holder.record(moment)

    # 8. BREAKS — Return any structural breaks for handling
    breaks = [t for t in tensions if is_unsustainable(t)]
    return breaks
```

---

## Step 1: Character Pumping

Characters are batteries. They pump energy into narratives they believe.

```python
def character_pumping():
    """
    Characters inject energy into narratives via BELIEVES links.
    Pump rate modified by state only. No proximity filter.
    Energy flow through the graph handles relevance.
    See ALGORITHM_Energy.md for full details.
    """
    for char in graph.characters:
        # Baseline regeneration
        char.energy = min(char.energy + BASELINE_REGEN, MAX_CHARACTER_ENERGY)

        # State modifier (dead/unconscious = 0, sleeping = 0.2, awake = 1.0)
        state_mod = get_state_modifier(char.state)
        if state_mod == 0:
            continue

        pump_budget = char.energy * PUMP_RATE * state_mod  # 0.1 * state

        # Distribute by belief strength only - no proximity filter
        beliefs = char.believes_links()
        total_strength = sum(link.strength for link in beliefs)

        if total_strength == 0:
            continue

        for link in beliefs:
            narrative = link.target
            proportion = link.strength / total_strength
            transfer = pump_budget * proportion
            narrative.energy += transfer
            char.energy -= transfer
```

**Why characters pump:** Characters are the engine. They care, therefore the story matters. No characters caring = no energy = no drama.

**Why no proximity filter:** Energy IS proximity. We don't pre-filter what characters pump into. We let them pump into everything they believe, and energy flow through the graph (CONTRADICTS, SUPPORTS, ABOUT links) determines what matters. High energy = close to attention. Low energy = far from attention.

---

## Step 2: Energy Transfer

Links route energy between narratives. Zero-sum between linked nodes.

```python
def transfer_energy():
    """
    Narrative-to-narrative and narrative-to-subject transfers.
    See ALGORITHM_Energy.md for full transfer mechanics.
    """
    # Narrative links
    for link in graph.narrative_links:
        if link.type == 'CONTRADICTS':
            transfer_contradiction(link)   # Bidirectional, 0.15 each way
        elif link.type == 'SUPPORTS':
            transfer_support(link)         # Equilibrating, 0.10
        elif link.type == 'ELABORATES':
            transfer_elaboration(link)     # Parent → child, 0.15
        elif link.type == 'SUBSUMES':
            transfer_subsumption(link)     # Specific → general, 0.10
        elif link.type == 'SUPERSEDES':
            transfer_supersession(link)    # Old → new + drain, 0.25

    # ABOUT links (focal point pulls)
    for link in graph.about_links:
        transfer_about(link)               # Subject pulls, 0.05
```

**Why zero-sum:** Links don't create energy — they route it. Conservation makes the system predictable.

---

## Step 3: Tension Injection

Detected tensions concentrate energy from participants into the crisis.

```python
def tension_injection(tensions):
    """
    Structural tensions draw energy from involved characters.
    Tension is computed, not stored. See ALGORITHM_Energy.md.
    """
    for tension in tensions:
        if tension['pressure'] <= 0.3:
            continue

        # Draw from participants
        total_drawn = 0
        for char in tension['characters']:
            draw = min(char.energy * tension['pressure'] * TENSION_DRAW,
                      char.energy * 0.5)
            char.energy -= draw
            total_drawn += draw

        # Inject into related narratives
        for narrative in tension['narratives']:
            narrative.energy += total_drawn / len(tension['narratives'])
```

**Why draw from characters:** Tension doesn't create energy — it concentrates it. The participants feel drained because the crisis pulls them in.

---

## Step 4: Decay

Energy leaves the system. This is the sink.

```python
def apply_decay():
    """
    Constant drain on all energy.
    Core narratives (oath, blood, debt) decay slower.
    """
    # Narrative decay
    for narrative in graph.narratives:
        rate = DECAY_RATE  # 0.02
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25
        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_ENERGY)

    # Character decay
    for char in graph.characters:
        char.energy *= (1 - DECAY_RATE)
        char.energy = max(char.energy, MIN_ENERGY)
```

**Why decay:** Without decay, everything accumulates forever. Decay creates forgetting. Old grievances fade unless someone keeps pumping.

---

## Step 5: Moment Weight Computation

Moment weight is derived from attached sources — not accumulated.

```python
def recompute_moment_weights():
    """
    Weight = sum of energy from speakers + attached narratives + present characters.
    """
    for moment in graph.moments:
        if moment.status not in ['possible', 'active']:
            continue

        weight = 0

        # From characters who can speak it
        for link in moment.incoming_can_speak():
            char = link.source
            if char.is_present:
                weight += char.energy * link.strength

        # From attached narratives
        for link in moment.outgoing_attached_to():
            if isinstance(link.target, Narrative):
                weight += link.target.energy * link.strength

        # From attached present characters
        for link in moment.outgoing_attached_to():
            if isinstance(link.target, Character) and link.target.is_present:
                weight += link.target.energy * link.strength

        moment.weight = weight
```

**Why derived:** Moments don't have independent energy. They surface when their sources are energized. This prevents weight accumulation bugs.

---

## Step 6: Flip Detection

Identify moments that crossed the threshold.

```python
def detect_flips() -> List[Moment]:
    """
    Deterministic: weight >= threshold means flip.
    """
    flipped = []
    for moment in graph.moments:
        if moment.status == 'possible' and moment.weight >= FLIP_THRESHOLD:
            moment.status = 'active'
            flipped.append(moment)

    return sorted(flipped, key=lambda m: m.weight, reverse=True)
```

### Deterministic vs Probabilistic

For v1, flipping is deterministic. `weight >= 0.8` = flip.

Probabilistic (weight = probability per tick) adds organic feel but complicates reasoning. Can add later if mechanical feel is a problem.

---

## Step 7: Emit to Canon Holder

Flipped moments are sent to Canon Holder for recording and display.

```python
def emit_flips(flipped: List[Moment]):
    """
    Canon Holder receives flipped moments in weight order.
    Actualization costs energy — drawn from sources.
    """
    for moment in flipped:
        # Actualization cost
        cost = moment.weight * ACTUALIZATION_COST  # 0.5
        speakers = moment.can_speak_characters()
        if speakers:
            for speaker in speakers:
                speaker.energy -= cost / len(speakers)

        # Record to canon
        canon_holder.record(moment)

        # Trigger handlers for attached characters
        character = get_attached_character(moment)
        if character:
            trigger_handler(character.id, triggered_by=moment)
```

**Why actualization costs:** Speaking takes effort. The moment draws from those who produced it. This prevents infinite chatter.

---

## Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `FLIP_THRESHOLD` | 0.8 | When weight crosses this, moment flips |
| `BASELINE_REGEN` | 0.01 | Character energy regen per tick |
| `PUMP_RATE` | 0.1 | Character energy → narratives per tick |
| `DECAY_RATE` | 0.02 | 2% per tick |
| `TENSION_DRAW` | 0.2 | How much tension pulls from participants |
| `ACTUALIZATION_COST` | 0.5 | Energy cost per moment flip |
| `MIN_ENERGY` | 0.01 | Floor — can always revive |
| `MAX_CHARACTER_ENERGY` | 10.0 | Ceiling — prevent runaway |
| `MAX_NARRATIVE_ENERGY` | 5.0 | Ceiling — keep bounded |

See ALGORITHM_Energy.md for transfer factors, state modifiers, and proximity rules.

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
- Author tensions (tensions emerge from structure)

Physics only: pump, transfer, decay, detect.

---

## Invariants

1. **Energy conservation:** Pumps in = decay + actualization out (links are zero-sum)
2. **Continuous:** Graph never stops, only changes rate
3. **Deterministic flips:** Same state → same flips (for v1)
4. **Derived weights:** Moment weight is computed, not accumulated

---

## Relationship to ALGORITHM_Energy.md

This file defines the **tick cycle** — when and in what order things happen.

ALGORITHM_Energy.md defines the **energy mechanics** — how energy flows, what creates it, what consumes it.

| This File | Energy File |
|-----------|-------------|
| Tick orchestration | Transfer formulas |
| Step ordering | Link type behaviors |
| Parameter values | Emergent behaviors |
| What happens when | Why it works |

---

*"The tick is one heartbeat of a continuous system."*

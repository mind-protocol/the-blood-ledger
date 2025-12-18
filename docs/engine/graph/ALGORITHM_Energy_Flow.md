# Graph — Algorithm: Energy Flow

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## Per-Tick Processing

Every tick (5 minutes game time), the graph engine runs this sequence:

```
1. Compute character energies
2. Flow energy from characters to narratives
3. Propagate energy between narratives
4. Decay energy
5. Tick pressures
6. Detect flips
```

---

## Step 1: Compute Character Energies

```python
def compute_character_energy(character, player):
    # Relationship intensity: how much player cares
    intensity = 0
    for narrative in graph.narratives_about(character):
        if player.believes(narrative):
            intensity += player.belief_strength(narrative)

    # Geographical proximity
    proximity = compute_proximity(character.location, player.location)

    return intensity * proximity

def compute_proximity(char_loc, player_loc):
    if char_loc == player_loc:
        return 1.0
    elif same_region(char_loc, player_loc):
        return 0.7
    elif adjacent_region(char_loc, player_loc):
        return 0.4
    else:
        days = travel_days(char_loc, player_loc)
        if days == 1: return 0.2
        elif days == 2: return 0.1
        else: return 0.05
```

---

## Step 2: Flow Energy Into Narratives

```python
BELIEF_FLOW_RATE = 0.1

def flow_energy_from_characters():
    for character in graph.characters:
        for narrative in character.believed_narratives():
            belief_strength = character.belief_strength(narrative)
            flow = character.energy * belief_strength * BELIEF_FLOW_RATE
            narrative.energy += flow
```

---

## Step 3: Propagate Between Narratives

Different link types flow differently. Contradictions heat both sides. Supersession drains the old.

```python
MAX_HOPS = 3

# Link type factors — each type has its own propagation strength
LINK_FACTORS = {
    'contradicts': 0.30,   # high — arguments need two hot takes
    'supports': 0.20,      # medium — allies rise together
    'elaborates': 0.15,    # lower — details inherit from parent
    'subsumes': 0.10,      # lowest — many specifics feed one general
    'supersedes': 0.25,    # draining — new gains, old loses
}

def propagate_energy():
    # Collect all transfers first (avoid order dependency)
    transfers = []
    drains = []  # for supersession

    for narrative in graph.narratives:
        for link in narrative.outgoing_links:
            target = link.target
            factor = LINK_FACTORS[link.type]
            transfer = narrative.energy * link.strength * factor

            if link.type == 'contradicts':
                # Bidirectional: contradiction heats both sides
                transfers.append((target, transfer))
                # Reverse direction handled when processing from target

            elif link.type == 'supports':
                # Bidirectional: allies rise together
                transfers.append((target, transfer))

            elif link.type == 'elaborates':
                # Unidirectional: general → specific
                transfers.append((target, transfer))

            elif link.type == 'subsumes':
                # Unidirectional: specific → general
                transfers.append((target, transfer))

            elif link.type == 'supersedes':
                # Draining: old loses, new gains
                transfers.append((target, transfer))
                drains.append((narrative, transfer * 0.5))

    # Apply transfers
    for target, amount in transfers:
        target.energy += amount

    # Apply drains (supersession)
    for source, drain in drains:
        source.energy -= drain
```

---

## Step 4: Decay Energy

```python
# Dynamic — adjusted by criticality feedback
decay_rate = 0.02
MIN_WEIGHT = 0.01

def decay_energy():
    for narrative in graph.narratives:
        # Apply decay
        narrative.energy *= (1 - decay_rate)

        # Floor at minimum
        if narrative.energy < MIN_WEIGHT:
            narrative.energy = MIN_WEIGHT

def decay_with_exceptions():
    """Version with exception handling"""
    global decay_rate

    for narrative in graph.narratives:
        # Skip recently active
        if narrative.last_active_tick >= current_tick - 10:
            continue

        # Core narratives decay slower
        rate = decay_rate
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25

        # Focused narratives decay slower
        if narrative.focus > 1.0:
            rate /= narrative.focus

        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_WEIGHT)

def check_conservation():
    """
    Soft global constraint on total energy.
    Open system: not conservation, but prevents runaway.
    """
    global decay_rate

    TARGET_MIN_ENERGY = 10.0  # scale with graph size
    TARGET_MAX_ENERGY = 50.0  # scale with graph size

    total_energy = sum(n.energy for n in graph.narratives)

    if total_energy > TARGET_MAX_ENERGY:
        decay_rate *= 1.05  # cool down
    if total_energy < TARGET_MIN_ENERGY:
        decay_rate *= 0.95  # heat up

def adjust_criticality():
    """
    Maintain system near critical threshold.
    decay_rate is THE KNOB — safe to adjust.
    """
    global decay_rate

    avg_pressure = mean([t.pressure for t in graph.tensions])
    hot_count = sum(1 for t in graph.tensions if t.pressure > 0.7)
    recent_breaks = count_breaks_in_last_hour()

    # System too cold — let it heat
    if avg_pressure < 0.3 or hot_count == 0:
        decay_rate *= 0.9

    # System too hot — dampen
    if avg_pressure > 0.6 or recent_breaks > 3:
        decay_rate *= 1.1

    # Clamp to sane range
    decay_rate = max(0.005, min(decay_rate, 0.1))

# NEVER DYNAMICALLY ADJUST:
# - breaking_point (changes story meaning)
# - belief_flow_rate (changes character importance)
# - link propagation factors (changes story structure)
```

---

## Step 5: Tick Pressures

```python
BASE_RATE = 0.001  # per minute
DEFAULT_BREAKING_POINT = 0.9

def tick_pressures(time_elapsed_minutes):
    for tension in graph.tensions:
        if tension.pressure_type == 'gradual':
            tick_gradual(tension, time_elapsed_minutes)
        elif tension.pressure_type == 'scheduled':
            tick_scheduled(tension)
        elif tension.pressure_type == 'hybrid':
            tick_hybrid(tension, time_elapsed_minutes)

        # Check for flip
        if tension.pressure >= tension.breaking_point:
            mark_for_flip(tension)

def tick_gradual(tension, time_elapsed):
    focus = average_focus(tension.narratives)
    max_weight = max_narrative_weight(tension.narratives)

    delta = time_elapsed * BASE_RATE * focus * max_weight
    tension.pressure = min(tension.pressure + delta, 1.0)

def tick_scheduled(tension):
    for checkpoint in tension.progression:
        if current_time >= checkpoint.at:
            tension.pressure = max(tension.pressure, checkpoint.pressure)

def tick_hybrid(tension, time_elapsed):
    # Tick gradual component
    focus = average_focus(tension.narratives)
    max_weight = max_narrative_weight(tension.narratives)
    ticked = tension.pressure + (time_elapsed * BASE_RATE * focus * max_weight)

    # Find scheduled floor
    floor = 0
    for checkpoint in tension.progression:
        if current_time >= checkpoint.at:
            floor = max(floor, checkpoint.pressure_floor)

    # Use higher of ticked or floor
    tension.pressure = min(max(ticked, floor), 1.0)
```

---

## Step 6: Detect Flips

```python
def detect_flips():
    flipped = []
    for tension in graph.tensions:
        if tension.pressure >= tension.breaking_point:
            flipped.append(tension)
    return flipped
```

When flips are detected, the orchestrator calls the World Runner.

---

## Full Tick

```python
def graph_tick(time_elapsed_minutes):
    """Complete tick cycle - no LLM, pure computation"""

    # 1. Character energies (relationship × proximity)
    for character in graph.characters:
        character.energy = compute_character_energy(character, player)

    # 2. Flow into narratives (characters pump)
    flow_energy_from_characters()

    # 3. Propagate between narratives (link-type dependent)
    propagate_energy()

    # 4. Decay
    decay_with_exceptions()

    # 5. Check conservation (soft global constraint)
    check_conservation()

    # 6. Adjust criticality (dynamic decay_rate)
    adjust_criticality()

    # 7. Pressure ticks
    tick_pressures(time_elapsed_minutes)

    # 8. Detect flips
    flipped = detect_flips()

    return flipped  # Orchestrator handles these
```

---

## Automatic Tension from Approach

When characters move, proximity changes. Energy follows automatically.

```python
# Edmund's energy as player approaches York
#
# Day 1 (one day travel):
#   Edmund: intensity=4.0, proximity=0.2 → energy=0.8
#
# Day 2 (same region):
#   Edmund: intensity=4.0, proximity=0.7 → energy=2.8
#
# No one decided this. Physics decided this.
# Confrontation tension rises because Edmund's narratives heat up.
```

---

## Parameters Summary

| Parameter | Value | Notes |
|-----------|-------|-------|
| belief_flow_rate | 0.1 | Character → Narrative (FIXED) |
| max_propagation_hops | 3 | Prevents infinite chains |
| decay_rate | 0.02 (dynamic) | Adjusted by conservation + criticality |
| decay_rate_min | 0.005 | Floor for dynamic adjustment |
| decay_rate_max | 0.1 | Ceiling for dynamic adjustment |
| min_weight | 0.01 | Never fully zero |
| base_rate | 0.001 | Pressure per minute |
| default_breaking_point | 0.9 | When flips trigger (NEVER TOUCH) |
| tick_threshold | 5 min | Minimum time between ticks |

---

## Link Type Factors

| Link Type | Factor | Direction | Effect |
|-----------|--------|-----------|--------|
| **contradicts** | 0.30 | Bidirectional | Both sides heat — argument needs two takes |
| **supports** | 0.20 | Bidirectional | Allies rise together — doubt one, doubt all |
| **elaborates** | 0.15 | General → Specific | Details inherit from parent |
| **subsumes** | 0.10 | Specific → General | Many specifics feed bigger picture |
| **supersedes** | 0.25 | Draining | New gains, old loses 50% of transfer |

---

## Conservation Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| target_min_energy | 10.0 | Scale with graph size |
| target_max_energy | 50.0 | Scale with graph size |
| adjustment_factor | 0.05 | How fast decay adjusts (5% per check) |

---

## Never Adjust Dynamically

| Parameter | Why |
|-----------|-----|
| breaking_point | Changes story meaning |
| belief_flow_rate | Changes character importance |
| link propagation factors | Changes story structure |

Only `decay_rate` is safe to adjust — it's the temperature knob, not the story knob.

---

*"Pure physics. No authorial injection. The story emerges from the web."*

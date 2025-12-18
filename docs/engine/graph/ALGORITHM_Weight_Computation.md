# Graph — Algorithm: Weight Computation

```
CREATED: 2024-12-16
STATUS: Canonical
```

---

## What Weight Means

Weight is the computed importance of a narrative. It determines:
- What surfaces in the Narrator's context
- What the player hears as voices
- How fast related tensions build

**Weight is never set directly. It emerges from structure.**

---

## Weight Formula

```python
def compute_weight(narrative):
    raw_weight = (
        belief_intensity(narrative) *
        player_connection_factor(narrative) *
        (1 + contradiction_bonus(narrative)) *
        recency_factor(narrative)
    )

    # Clamp and apply focus evolution
    return clamp(raw_weight * focus_evolution(narrative), 0, 1)
```

---

## Component: Belief Intensity

How strongly characters believe this narrative, weighted by their importance to player.

```python
def belief_intensity(narrative):
    total = 0
    for believer in narrative.believers:
        importance = believer.connection_to_player
        belief_strength = believer.belief_strength(narrative)
        total += importance * belief_strength
    return total
```

**Believer importance** is computed from:
- Direct relationship with player
- Proximity (physical and graph distance)
- Recent interactions

---

## Component: Player Connection

How connected this narrative is to the player.

```python
def player_connection_factor(narrative):
    # Direct: player believes it
    if player.believes(narrative):
        return 1.0

    # Indirect: about someone player knows
    for subject in narrative.about:
        if player.knows(subject):
            distance = graph_distance(player, subject)
            return 1.0 / (1 + distance)

    # Distant: no direct connection
    return 0.1
```

---

## Component: Contradiction Bonus

Narratives that contradict other believed narratives gain weight.

```python
def contradiction_bonus(narrative):
    bonus = 0
    for other in narrative.contradicts:
        if player.believes(other):
            # Bonus is limited by weaker of the two
            bonus += min(narrative.weight, other.weight) * 0.5
    return bonus
```

**Why:** Contradictions create tension. Tension demands attention.

---

## Component: Recency Factor

When was this narrative last relevant?

```python
def recency_factor(narrative):
    ticks_since_active = current_tick - narrative.last_active_tick

    if ticks_since_active <= 10:
        return 1.0
    elif ticks_since_active <= 50:
        return 0.8
    elif ticks_since_active <= 100:
        return 0.5
    else:
        return 0.2
```

---

## Focus Evolution

Focus affects how fast weight changes, not the value itself.

```python
def focus_evolution(narrative):
    """
    focus > 1.0: weight rises faster, falls slower
    focus < 1.0: weight rises slower, falls faster
    focus = 1.0: normal evolution
    """
    if narrative.weight_increasing:
        return narrative.focus
    else:
        return 1.0 / narrative.focus
```

**The Narrator sets focus.** This is how authorial intent shapes the graph without overriding it.

---

## When Weight Is Recomputed

Weight is recomputed each tick, after energy flow:

```python
def recompute_weights():
    for narrative in graph.narratives:
        old_weight = narrative.weight
        narrative.weight = compute_weight(narrative)
        narrative.weight_increasing = narrative.weight > old_weight
```

---

## Weight Thresholds

| Weight Range | Meaning |
|--------------|---------|
| 0.8 - 1.0 | Critical — always in context |
| 0.5 - 0.8 | Active — usually in context |
| 0.2 - 0.5 | Relevant — included if space |
| 0.01 - 0.2 | Dormant — rarely surfaces |

---

## Example Computation

**Narrative:** `narr_edmund_betrayal`

| Component | Value | Notes |
|-----------|-------|-------|
| Belief intensity | 1.8 | Player (1.0 × 1.0) + Aldric (0.8 × 1.0) |
| Player connection | 1.0 | Player believes it directly |
| Contradiction bonus | 0.3 | Contradicts "Edmund was forced" (0.6 weight) |
| Recency factor | 1.0 | Active 5 ticks ago |
| Focus | 1.2 | Narrator wants this prominent |

```
raw_weight = 1.8 × 1.0 × 1.3 × 1.0 = 2.34
clamped = clamp(2.34 × 1.0, 0, 1) = 1.0
```

This narrative is at maximum weight — always in context.

---

*"Weight emerges from structure. The story earns its importance."*

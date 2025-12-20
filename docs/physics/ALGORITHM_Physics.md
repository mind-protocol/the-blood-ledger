# Physics — Algorithm: System Overview

```
CREATED: 2024-12-18
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Physics.md (you are here)
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
HEALTH:         ./HEALTH_Physics.md
SYNC:           ./SYNC_Physics.md

---

## Consolidation Note

This document consolidates the physics algorithm chain into a single canonical file.
Former standalone docs are now sections here: ALGORITHM_Energy, ALGORITHM_Input,
ALGORITHM_Actions, ALGORITHM_Handlers, ALGORITHM_Canon, ALGORITHM_Speed,
and ALGORITHM_Questions.

---

## OVERVIEW

This algorithm describes the physics engine that moves energy through the
graph, detects flips, and hands off work to handlers, canon, and display
control. The intent is to keep all authoritative state in the graph while
the tick cycle applies deterministic propagation rules.

---

## DATA STRUCTURES

- Graph nodes for Characters, Narratives, Moments with `weight` and `energy`.
- Graph links for BELIEVES/ABOUT/SUPPORTS/etc. with `strength` and optional
  routing attributes like `presence_required` and `require_words`.
- Tick context: current tick index, decay constants, and pending flip results.
- Queues: handler outputs (potential moments) and canon records (actualized).

---

## ALGORITHM: Physics Tick Cycle

Primary function: `run_physics_tick()` (conceptual name for the per-tick loop).

1. Load active characters and their BELIEVES/ORIGINATED links.
2. Pump character energy into narratives using link strengths.
3. Route narrative energy across narrative-to-narrative links (zero-sum).
4. Push energy to moments via ATTACHED_TO and CAN_SPEAK links.
5. Apply decay and clamp weights/energy to minimum thresholds.
6. Compute salience and detect flips for moments and narratives.
7. Emit flip results to handlers and canon recording pipeline.
8. Persist updated weights/energy to the graph and return tick summary.

---

## KEY DECISIONS

- Energy is the proximity signal; no separate proximity layer exists.
- Links only route energy; creation happens via character pumps or input.
- The graph is the only source of truth; ticks never cache authoritative state.
- Zero-sum transfers preserve energy while decay and actualization drain it.

---

## DATA FLOW

Graph queries load current node/link state → tick computes injections and
transfers → updates are written back to the graph → flip events are surfaced
to handlers and canon holder → display layer filters by speed settings.

---

## COMPLEXITY

Per tick cost is proportional to the number of active characters, their
adjacent BELIEVES/ABOUT links, and reachable narrative edges. Worst case is
O(V+E) over the active subgraph; practical runs are bounded by salience
filters and query limits in graph ops.

---

## HELPER FUNCTIONS

- `salience(node)` multiplies weight and energy to rank surfacing.
- `reinforce_link()` and `challenge_link()` adjust strengths with clamps.
- `apply_decay()` reduces energy/weight based on real-time elapsed.
- `is_interrupt()` classifies moments for 3x snap-to-1x transitions.

---

## INTERACTIONS

- Handlers read flip outputs to generate new potential moments.
- Canon holder records actualized moments and THEN links.
- Speed controller adjusts tick interval and display filtering rules.
- GraphOps/GraphQueries provide the mutation and read API used by ticks.

---

## GAPS / IDEAS / QUESTIONS

- Handler runtime and canon holder code are planned but not fully implemented.
- Energy constants (pump rates, thresholds) still need playtesting.
- Question Answerer async integration depends on infrastructure readiness.

---

## Energy Mechanics

### Core Principles

**1. Links don't create energy. They route it.**

Energy conservation within the narrative layer. Characters are external pumps. Decay and actualization are sinks.

**2. Strength is authored initially, evolved structurally.**

Narrator sets initial link strength. Events modify it. Time decays it. No magic numbers — earned through play.

**3. Energy IS proximity.**

We don't compute "proximity" as a separate concept. Energy levels encode relevance. High energy = close to attention. Low energy = far from attention. Physics handles it.

**4. Physical gating is link attributes, not functions.**

`presence_required: bool` on ATTACHED_TO links. `AT` links for character location. Graph queries, not code.

---

## NODE TYPES

All nodes that participate in the energy economy have both:
- **Weight**: Importance over time (slow, event-driven)
- **Energy**: Current activation (fast, flow-driven)

| Node | Weight | Energy | Notes |
|------|--------|--------|-------|
| **Character** | Yes | Yes | Batteries — pump energy out |
| **Narrative** | Yes | Yes | Circuits — route energy between |
| **Moment** | Yes | Yes | Spend energy on actualization |
| **Place** | No | No | Container only |
| **Thing** | No | No | Focal point only (via ABOUT links) |

### Weight vs Energy

| Property | Weight | Energy |
|----------|--------|--------|
| **What** | Importance over time | Current activation |
| **Timescale** | Slow (hours/days) | Fast (ticks/seconds) |
| **Changes by** | Events, reinforcement, decay | Flow, injection, spending |
| **Range** | 0.01 - 1.0 | 0.01 - 10.0 (chars) / 5.0 (narr/moment) |
| **Analogy** | Long-term memory strength | Working memory activation |

### Why Both Matter

| State | Meaning |
|-------|---------|
| High weight, low energy | Important but dormant — "the oath exists but no one's thinking about it" |
| Low weight, high energy | Active but trivial — "we're discussing lunch" |
| High weight, high energy | Important AND active — "the betrayal surfaces NOW" |
| Low weight, low energy | Forgotten — will decay away |

### Surfacing / Relevance

```python
def salience(node):
    """How much should this surface right now?"""
    return node.weight * node.energy
```

High salience = surfaces, dominates attention, triggers events.

### Character Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `weight` | float | Importance to story (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 10.0) |
| `state` | enum | `awake`, `sleeping`, `unconscious`, `dead` |

### Narrative Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `type` | enum | `fact`, `belief`, `oath`, `debt`, `secret`, `rumor`, `relationship` |
| `weight` | float | Importance to story (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 5.0) |
| `visibility` | enum | `public`, `secret`, `known_to_few` |
| `deadline` | datetime? | For debts, oaths with time pressure |
| `conditions` | string[]? | For oaths — when does it activate? |

### Moment Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `text` | string | The content |
| `type` | enum | `narration`, `dialogue`, `action`, `thought`, `description` |
| `status` | enum | `possible`, `active`, `spoken`, `dormant`, `decayed` |
| `weight` | float | Importance over time (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 5.0) |
| `tone` | string? | `bitter`, `hopeful`, `urgent`, etc. |
| `tick_created` | int | When created |
| `tick_spoken` | int? | When actualized |

---

## LINK TYPES

### Character Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **BELIEVES** | Char → Narr | Char pumps into Narr | Core relationship |
| **ORIGINATED** | Char → Narr | Char pumps harder (*1.5) | Authorship |
| **AT** | Char → Place | NO flow | Spatial |
| **CARRIES** | Char → Thing | NO flow | Possession |

### Narrative Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **ABOUT** | Narr → Char/Place/Thing | Reverse: subject pulls | Focal point |
| **CONTRADICTS** | Narr ↔ Narr | Bidirectional exchange | Conflict |
| **SUPPORTS** | Narr ↔ Narr | Equilibrating | Alliance |
| **ELABORATES** | Narr → Narr | Parent → child | Detail |
| **SUBSUMES** | Narr → Narr | Specific → general | Aggregation |
| **SUPERSEDES** | Narr → Narr | Draining (old → new) | Replacement |

### Moment Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **CAN_SPEAK** | Char → Moment | Char energy → weight | Who speaks |
| **ATTACHED_TO** | Moment → Any | Target energy → weight | Relevance |
| **CAN_LEAD_TO** | Moment → Moment | On traversal | Conversation |
| **THEN** | Moment → Moment | NO (historical) | Canon chain |

### Link Properties

| Link | Properties |
|------|------------|
| **BELIEVES** | `strength: float`, `role: str?` (creditor/debtor/witness/etc) |
| **ORIGINATED** | `strength: float` |
| **ABOUT** | `strength: float`, `role: str?` (subject/location/object) |
| **CONTRADICTS** | `strength: float` |
| **SUPPORTS** | `strength: float` |
| **ELABORATES** | `strength: float` |
| **SUBSUMES** | `strength: float` |
| **SUPERSEDES** | `strength: float` |
| **CAN_SPEAK** | `strength: float` |
| **ATTACHED_TO** | `strength: float`, `presence_required: bool` |
| **CAN_LEAD_TO** | `strength: float`, `require_words: str[]`, `trigger: enum` |

---

## NARRATIVE TYPES

Semantic meaning lives in narrative typing, not special link types.

| Narrative Type | Special Fields | Tension Pattern |
|----------------|----------------|-----------------|
| `fact` | — | — |
| `belief` | — | Contradiction |
| `oath` | `conditions: str[]` | Conditions met |
| `debt` | `amount: float?`, `deadline: datetime?` | Time + proximity |
| `secret` | `visibility: secret` | Knower meets subject |
| `rumor` | `source: char_id?` | Spread pattern |
| `relationship` | `valence: positive/negative` | — |

**Example: Debt as Structure (not special links)**

```yaml
Narrative:
  id: narr_debt_to_merchant
  type: debt
  text: "You owe the merchant 50 silver"
  amount: 50
  deadline: 1067-03-15
```

```
merchant ──[BELIEVES {strength: 0.9, role: creditor}]──> narr_debt_to_merchant
player ──[BELIEVES {strength: 0.6, role: debtor}]──> narr_debt_to_merchant
narr_debt_to_merchant ──[ABOUT]──> merchant
narr_debt_to_merchant ──[ABOUT]──> player
```

Tension detection queries this structure — no special OWES/OWED_BY links needed.

---

## LINK STRENGTH

### Principle

**Strength = authored initially, evolved structurally**

Narrator sets initial value. Six mechanics modify it over time. No magic — earned through play.

### Timescales (No Circularity)

| Property | Changes | Timescale |
|----------|---------|-----------|
| **Energy** | Every tick | Seconds |
| **Weight** | Derived from energy | Seconds |
| **Strength** | On events | Minutes to hours |

Strength is slow. Energy is fast. Strength is effectively constant within a tick cycle.

### Default Initial Strength

| Link | Default | Notes |
|------|---------|-------|
| BELIEVES | 0.5 | Narrator sets based on conviction |
| ORIGINATED | 0.8 | You care about your own stories |
| CONTRADICTS | Computed | Semantic opposition score |
| SUPPORTS | Computed | Semantic similarity score |
| ELABORATES | 0.5 | How central is detail to parent |
| SUBSUMES | 0.5 | How much specific feeds general |
| SUPERSEDES | 0.9 | Replacement is decisive |
| ABOUT | 0.7 | Derived from narrative centrality |

### Base Functions

```python
def reinforce_link(link, amount=0.05):
    """Something confirmed/repeated this connection"""
    link.strength = min(link.strength + amount, 1.0)
    link.last_reinforced = current_tick

def challenge_link(link, amount=0.1):
    """Something contradicted/weakened this connection"""
    link.strength = max(link.strength - amount, 0.1)  # Never fully zero
    link.last_challenged = current_tick

def decay_link_strength(link):
    """Slow decay if not reinforced (part of Activation mechanic)"""
    ticks_since = current_tick - link.last_reinforced
    if ticks_since > 100:  # ~8 hours game time
        decay = 0.001 * (ticks_since - 100)
        link.strength = max(link.strength - decay, 0.1)
```

---

## STRENGTH MECHANICS (Six Categories)

### Principle

All strength changes reduce to six abstract mechanics. Specific scenarios (betrayal, oaths, gossip, trauma) emerge from combinations.

| Mechanic | Principle | Direction |
|----------|-----------|-----------|
| **Activation** | Use it or lose it | Reinforce on use, decay on neglect |
| **Evidence** | World confirms or denies | Reinforce or challenge |
| **Association** | Co-activation creates connection | Create/strengthen links |
| **Source** | Trust transfers | Initial strength inherited |
| **Commitment** | Action locks in belief | Reinforce after acting |
| **Intensity** | Emotional weight imprints | Modifier on strength change |

---

### M1: ACTIVATION

**Principle:** Links strengthen when used, decay when neglected.

**"Used" means:**
- Referenced in a moment (spoken, thought, narrated)
- Queried by player (asked about)
- Traversed (conversation followed this path)

```python
def apply_activation(link, context):
    """
    Link was used — reinforce it.
    """
    base = 0.03

    # Speaking is stronger than thinking
    if context.type == 'dialogue':
        base = 0.05

    # Direct address is strongest
    if context.direct_address:
        base = 0.08

    reinforce_link(link, amount=base)
```

**Detection:** Canon Holder, when recording any moment.

```python
def record_moment(moment):
    referenced = moment.attached_narratives()
    speaker = moment.speaker

    for narrative in referenced:
        # Speaker's belief activated
        link = get_link(speaker, 'BELIEVES', narrative)
        if link:
            apply_activation(link, moment)

        # ABOUT links activated
        for about_link in narrative.outgoing_about():
            apply_activation(about_link, moment)
```

**Examples:**
- Aldric mentions Edmund → Aldric's BELIEVES links to Edmund narratives activate
- Player asks about the sword → All ABOUT links to sword activate
- Character thinks about their father → Their BELIEVES links to father narratives activate

---

### M2: EVIDENCE

**Principle:** Events in the world confirm or deny beliefs.

```python
def apply_evidence(link, confirms: bool, evidence_weight: float, proximity: float):
    """
    Something happened that confirms or denies this belief.

    evidence_weight: how strong is the evidence (0.1 = rumor, 1.0 = witnessed firsthand)
    proximity: how close was the witness (1.0 = present, 0.5 = heard about)
    """
    effect = evidence_weight * proximity

    if confirms:
        reinforce_link(link, amount=effect * 0.15)
    else:
        challenge_link(link, amount=effect * 0.20)
```

**Detection:** Canon Holder, checking for SUPPORTS/CONTRADICTS relationships.

```python
def record_moment(moment):
    witnesses = get_present_characters(moment.location)
    moment_narratives = moment.attached_narratives()

    for witness in witnesses:
        proximity = compute_proximity(witness, moment.location)

        for narr in moment_narratives:
            # Check what this evidence supports
            supported = get_linked(narr, 'SUPPORTS')
            for supported_narr in supported:
                link = get_link(witness, 'BELIEVES', supported_narr)
                if link:
                    apply_evidence(link, confirms=True,
                                   evidence_weight=narr.weight,
                                   proximity=proximity)

            # Check what this evidence contradicts
            contradicted = get_linked(narr, 'CONTRADICTS')
            for contra_narr in contradicted:
                link = get_link(witness, 'BELIEVES', contra_narr)
                if link:
                    apply_evidence(link, confirms=False,
                                   evidence_weight=narr.weight,
                                   proximity=proximity)
```

**Examples:**
- Edmund caught stealing → Confirms "Edmund is untrustworthy" for witnesses
- Brother's body found → Contradicts "My brother is alive"
- Aldric saves your life → Confirms "Aldric is loyal"

---

### M3: ASSOCIATION

**Principle:** Things that occur together become linked.

```python
def apply_association(narr_a, narr_b, strength: float = 0.03):
    """
    Two narratives co-occurred — strengthen or create SUPPORTS link.
    """
    link = get_link(narr_a, 'SUPPORTS', narr_b)

    if link:
        reinforce_link(link, amount=strength)
    else:
        # Create new association if co-occurrence is strong enough
        if strength > 0.05:
            create_link(narr_a, 'SUPPORTS', narr_b, strength=strength)
```

**Detection:** Canon Holder, tracking conversation context.

```python
def record_moment(moment):
    current = moment.attached_narratives()

    # Recent narratives in same conversation
    recent = query("""
        MATCH (m:Moment)-[:THEN*1..3]->(current:Moment {id: $id})
        MATCH (m)-[:ATTACHED_TO]->(n:Narrative)
        WHERE m.tick > $threshold
        RETURN DISTINCT n
    """, id=moment.id, threshold=current_tick - 10)

    # Co-occurring narratives associate
    for a in current:
        for b in recent:
            if a.id != b.id:
                apply_association(a, b)
```

**Examples:**
- "The Normans burned the village" + "They burned York too" → SUPPORTS link forms
- Mention sword + mention father in same conversation → Association strengthens
- Character talks about debt + talks about fear → Emotional association forms

---

### M4: SOURCE

**Principle:** New beliefs inherit strength from source credibility.

```python
def compute_initial_strength(receiver, source, narrative):
    """
    How strongly does receiver believe this, given who told them?
    """
    BASE_STRENGTH = 0.4

    # How much does receiver trust source?
    trust_narratives = query("""
        MATCH (r:Character {id: $receiver})-[b:BELIEVES]->(n:Narrative)
        WHERE n.type = 'relationship'
          AND (n)-[:ABOUT]->(:Character {id: $source})
        RETURN n, b.strength
    """, receiver=receiver.id, source=source.id)

    if not trust_narratives:
        credibility = 0.5  # Unknown source = neutral
    else:
        # Average trust from relationship narratives
        credibility = mean([b.strength for n, b in trust_narratives])

    # Direct witness vs secondhand
    if source.witnessed(narrative):
        directness = 1.0
    else:
        directness = 0.6  # Gossip discount

    return BASE_STRENGTH * credibility * directness
```

**Detection:** Handler, when creating new BELIEVES link.

```python
def character_learns(receiver, narrative, source):
    """
    Character learns something from another character.
    """
    initial = compute_initial_strength(receiver, source, narrative)
    create_link(receiver, 'BELIEVES', narrative, strength=initial)
```

**Examples:**
- Trusted friend tells you Edmund betrayed you → High initial strength
- Stranger tells you the same → Lower initial strength
- Enemy tells you something → Maybe you believe the opposite
- Gossip (X told Y who told you) → Compounding discount

---

### M5: COMMITMENT

**Principle:** Acting on a belief locks it in.

```python
def apply_commitment(character, narrative, action_cost: float):
    """
    Character acted on this belief. Reinforce it.

    action_cost: how much did the action cost? (0.1 = trivial, 1.0 = major sacrifice)
    """
    link = get_link(character, 'BELIEVES', narrative)
    if link:
        # Higher cost = stronger commitment
        reinforce_link(link, amount=0.05 + (action_cost * 0.10))
```

**Detection:** Action processor, when moment with action field actualizes.

```python
def process_action(moment):
    if not moment.action:
        return

    actor = moment.speaker

    # What beliefs motivated this action?
    motivating = query("""
        MATCH (m:Moment {id: $id})-[:ATTACHED_TO]->(n:Narrative)
        MATCH (c:Character {id: $actor})-[:BELIEVES]->(n)
        RETURN n
    """, id=moment.id, actor=actor.id)

    action_cost = estimate_action_cost(moment.action)

    for narrative in motivating:
        apply_commitment(actor, narrative, action_cost)
```

**Examples:**
- Accuse Edmund publicly → Locked into "Edmund is guilty"
- Give away money → Locked into belief that justified it
- Risk your life for someone → Strongly locked into trusting them

---

### M6: INTENSITY

**Principle:** High-emotion contexts amplify strength changes.

```python
def compute_intensity_modifier(context):
    """
    How emotionally intense is this moment?
    Returns multiplier for strength changes.
    """
    base = 1.0

    # Tension pressure
    active_tensions = detect_tensions()
    max_pressure = max([t['pressure'] for t in active_tensions], default=0)
    base += max_pressure * 0.5  # Up to +0.5 from tension

    # Danger
    if context.danger_level:
        base += context.danger_level * 0.3  # Up to +0.3 from danger

    # Emotional weight of moment
    if context.tone in ['grief', 'rage', 'terror', 'ecstasy']:
        base += 0.3
    elif context.tone in ['sad', 'angry', 'afraid', 'joyful']:
        base += 0.15

    return min(base, 2.0)  # Cap at 2x
```

**Application:** Wraps all other mechanics.

```python
def record_moment(moment):
    intensity = compute_intensity_modifier(moment)

    # All strength changes multiplied by intensity
    for narrative in moment.attached_narratives():
        link = get_link(moment.speaker, 'BELIEVES', narrative)
        if link:
            apply_activation(link, moment)
            link.last_change *= intensity  # Amplify the change
```

**Examples:**
- Learn something during battle → Stronger imprint
- Confession during high tension → More impactful
- Casual mention during calm → Normal strength change
- Traumatic revelation → 2x strength effect

---

### Summary

| Mechanic | Trigger | Effect Range |
|----------|---------|--------------|
| Activation | Link referenced/used | +0.03 to +0.08 |
| Evidence+ | Confirming event witnessed | +0.05 to +0.15 |
| Evidence- | Contradicting event witnessed | -0.05 to -0.30 |
| Association | Co-occurrence | +0.03, create if none |
| Source | New belief from someone | initial × credibility |
| Commitment | Acted on belief | +0.05 to +0.15 |
| Intensity | High-stress context | ×1.0 to ×2.0 multiplier |

### Agents That Modify Strength

| Agent | Mechanics Applied |
|-------|-------------------|
| **Canon Holder** | Activation, Evidence, Association |
| **Input Parser** | Activation |
| **Handler** | Source (when character learns), Evidence (deciding response) |
| **Action Processor** | Commitment |
| **All** | Intensity (wraps other mechanics) |

### Emergent Scenarios

| Scenario | Mechanics Involved |
|----------|-------------------|
| Betrayal | Evidence- (strong), Intensity (high) |
| Oath made | Activation, Commitment, Intensity |
| Oath broken | Evidence- (strong), Intensity (high) |
| Gossip spreads | Source (compounding discount), Association |
| Trauma | Evidence, Intensity (×2.0) |
| Trusted friend tells you | Source (high credibility) |
| Enemy's accusation | Source (low/negative credibility) |
| Public declaration | Activation (strong), Commitment |
| Place triggers memory | Activation (via ATTACHED_TO place) |

---

### Why Conservation

| Approach | Problem |
|----------|---------|
| Links create energy | System explodes. Requires arbitrary dampening. |
| No conservation | Tuning nightmare. Magic numbers everywhere. |
| **Conservation + external pumps** | Predictable. "Heat" emerges from structure. |

"Arguments heat both sides" because both sides have believers pumping — not because contradiction creates energy from nothing.

---

### The Energy Equation

```
Per tick:

  ΔE_system = injection - decay - actualization

Where:
  injection    = Σ (character pumping)
  decay        = Σ (narrative.energy * decay_rate)
  actualization = Σ (moment.weight) for moments that flip
```

Links redistribute within the system. They don't change total energy.

---

## ENERGY SOURCES

### S1: Character Pumping

Characters inject energy into narratives they care about.

**Core insight:** We don't compute "proximity" separately. Energy levels ARE proximity. Characters pump into narratives proportional to belief strength. Energy flow through the graph handles the rest.

#### Character Energy Sources

| Source | Amount | When |
|--------|--------|------|
| **Baseline** | 0.01 per tick | Always (existing) |
| **Being talked about** | from ABOUT links | Others discuss you |
| **Player focus** | 1.0 / targets | Direct attention |
| **Arrival** | 0.5 one-time | Enter scene |

#### Character State

| State | Pump Modifier | Notes |
|-------|---------------|-------|
| `awake` | 1.0 | Full pumping |
| `sleeping` | 0.2 | Dreams, weak influence |
| `unconscious` | 0.0 | No pumping |
| `dead` | 0.0 | No pumping (narratives persist through others) |

```python
def get_state_modifier(state):
    return {
        'awake': 1.0,
        'sleeping': 0.2,
        'unconscious': 0.0,
        'dead': 0.0
    }.get(state, 1.0)
```

#### Pump Calculation

```python
PUMP_RATE = 0.1
BASELINE_REGEN = 0.01

def character_tick(character):
    """
    Character pumps energy into narratives.
    No proximity calculation - energy flow handles relevance.
    """
    # Baseline regeneration
    character.energy = min(
        character.energy + BASELINE_REGEN,
        MAX_CHARACTER_ENERGY
    )

    # State modifier
    state_mod = get_state_modifier(character.state)
    if state_mod == 0:
        return

    # Pump budget
    pump_budget = character.energy * PUMP_RATE * state_mod

    # Distribute by belief strength only
    beliefs = character.outgoing_belief_links()
    total_strength = sum(link.strength for link in beliefs)

    if total_strength == 0:
        return

    for link in beliefs:
        narrative = link.target
        proportion = link.strength / total_strength
        transfer = pump_budget * proportion
        narrative.energy += transfer
        character.energy -= transfer
```

**Why no proximity filter?**

Energy flow through the graph handles "relevance" automatically:
1. Player focuses on Edmund → Edmund's narratives get energy
2. Those narratives transfer to related narratives (SUPPORTS, ELABORATES)
3. High energy narratives surface
4. Low energy narratives don't

We don't pre-filter what characters pump into. We let them pump into everything they believe, and physics determines what matters.

#### Dead Characters

Dead characters don't pump. But their narratives persist through the living.

```
Edmund dies
  → Edmund.state = 'dead'
  → Edmund stops pumping
  → narr_edmund_betrayal persists
  → Aldric still pumps into it (his belief)
  → The narrative lives through believers
```

---

### S2: Player Focus Injection

What the player attends to receives energy.

```python
def player_focus_injection(player, focus_targets):
    """
    Player attention injects energy into scene.
    Focus targets: characters addressed, things examined, topics raised.
    """
    FOCUS_INJECTION = 1.0  # Per input

    for target in focus_targets:
        if isinstance(target, Character):
            target.energy += FOCUS_INJECTION / len(focus_targets)
        elif isinstance(target, Narrative):
            target.energy += FOCUS_INJECTION / len(focus_targets)
        elif isinstance(target, Thing):
            # Things don't hold energy — redirect to related narratives
            for narrative in narratives_about(target):
                narrative.energy += (FOCUS_INJECTION / len(focus_targets)) / count
```

**Why:** Player attention is the camera. What you look at lights up.

---

### S3: World Events

External events inject energy.

```python
def world_event_injection(event):
    """
    News, arrivals, discoveries inject energy.
    """
    if event.type == 'arrival':
        # Character arrives — they bring their energy with them
        event.character.energy += ARRIVAL_BOOST  # 0.5

    elif event.type == 'news':
        # News creates/energizes a narrative
        narrative = event.narrative
        narrative.energy += NEWS_INJECTION  # 0.3

    elif event.type == 'discovery':
        # Discovery energizes existing narrative
        narrative = event.narrative
        narrative.energy += DISCOVERY_INJECTION  # 0.5
```

**Why:** The world beyond the player injects surprise.

---

### S4: Tension Pressure (Structural)

Detected tensions inject energy into related narratives.

```python
def tension_injection(tensions):
    """
    Structural tensions push energy toward crisis.
    Not created from nothing — drawn from participants.
    """
    for tension in tensions:
        pressure = tension['pressure']

        if pressure > 0.3:  # Only meaningful tensions
            # Draw energy from involved characters
            characters = tension['characters']
            draw_per_char = pressure * TENSION_DRAW  # 0.2

            total_drawn = 0
            for char in characters:
                drawn = min(char.energy * draw_per_char, char.energy * 0.5)
                char.energy -= drawn
                total_drawn += drawn

            # Inject into related narratives
            narratives = tension['narratives']
            for narrative in narratives:
                narrative.energy += total_drawn / len(narratives)
```

**Why:** Tension doesn't create energy — it concentrates it. The participants feel drained because their energy is being pulled into the crisis.

---

## ENERGY SINKS

### K1: Decay

Constant drain on all energy.

```python
DECAY_RATE = 0.02  # 2% per tick

def apply_decay():
    """
    Energy bleeds out of the system.
    Core narratives decay slower.
    """
    for narrative in graph.narratives:
        rate = DECAY_RATE

        # Core types resist decay
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25

        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_ENERGY)  # 0.01 floor

    for character in graph.characters:
        character.energy *= (1 - rate)
        character.energy = max(character.energy, MIN_ENERGY)
```

**Why:** Without decay, everything accumulates forever. Decay creates forgetting.

---

### K2: Actualization

When moments flip, energy is spent.

```python
def moment_actualization(moment):
    """
    Flipping a moment costs energy.
    Energy comes from attached sources.
    """
    cost = moment.weight * ACTUALIZATION_COST  # 0.5

    # Draw from speakers
    speakers = moment.can_speak_characters()
    if speakers:
        cost_per_speaker = cost / len(speakers)
        for speaker in speakers:
            speaker.energy -= cost_per_speaker

    # Draw from attached narratives
    attached = moment.attached_narratives()
    if attached:
        cost_per_narrative = cost / len(attached)
        for narrative in attached:
            narrative.energy -= cost_per_narrative

    moment.status = 'spoken'
```

**Why:** Speaking takes effort. The moment doesn't come from nowhere — it draws from those who produced it.

---

## ENERGY TRANSFER (Links)

### Principle

Links transfer energy between nodes. **Zero-sum between linked nodes.**

```
Transfer from A to B via link:
  A.energy -= transfer_amount
  B.energy += transfer_amount
```

Transfer amount depends on:
- Source energy (can't give what you don't have)
- Link strength (stronger connection = faster flow)
- Link type factor (some links conduct better)

---

### T1: CONTRADICTS (Bidirectional)

Both sides pull from each other simultaneously.

```python
CONTRADICT_FACTOR = 0.15  # Per direction, so 0.30 total exchange

def transfer_contradiction(link):
    """
    Contradiction: bidirectional exchange.

    A ←──CONTRADICTS──→ B

    A pulls from B. B pulls from A.
    Net effect: energy equalizes, both stay hot if either is hot.
    """
    A = link.source
    B = link.target
    strength = link.strength

    # A pulls from B
    transfer_A = B.energy * strength * CONTRADICT_FACTOR
    B.energy -= transfer_A
    A.energy += transfer_A

    # B pulls from A
    transfer_B = A.energy * strength * CONTRADICT_FACTOR
    A.energy -= transfer_B
    B.energy += transfer_B
```

**Why bidirectional:** You can't think about one side of an argument without the other coming to mind. Contradiction is mutual.

**Why high factor (0.30 total):** Arguments are sticky. They grab attention.

**Emergent behavior:** If Edmund pumps "I was right" and Aldric pumps "Edmund betrayed us", both narratives stay hot because:
1. Characters pump in
2. Contradiction exchanges between them
3. Neither can cool while the other is hot

---

### T2: SUPPORTS (Bidirectional)

Allies share fate.

```python
SUPPORT_FACTOR = 0.10  # Per direction

def transfer_support(link):
    """
    Support: bidirectional sharing.

    A ←──SUPPORTS──→ B

    Energy equalizes. Doubt one, doubt all.
    """
    A = link.source
    B = link.target
    strength = link.strength

    # Energy flows toward equilibrium
    diff = A.energy - B.energy
    transfer = diff * strength * SUPPORT_FACTOR

    A.energy -= transfer
    B.energy += transfer
```

**Why equilibrium:** Supporting narratives should have similar energy. If one rises, it lifts the others. If one falls, it drags the others.

**Lower factor than contradiction:** Agreement is less grabby than conflict.

---

### T3: ELABORATES (Unidirectional, Parent → Child)

Details inherit from their source.

```python
ELABORATE_FACTOR = 0.15

def transfer_elaboration(link):
    """
    Elaboration: parent feeds child.

    A ──ELABORATES──→ B

    Parent energizes details. Not reverse.
    """
    parent = link.source
    child = link.target
    strength = link.strength

    transfer = parent.energy * strength * ELABORATE_FACTOR
    parent.energy -= transfer
    child.energy += transfer
```

**Why unidirectional:** "Edmund betrayed us" (parent) energizes "Edmund opened the gate" (detail). The detail doesn't energize the parent — it's downstream.

---

### T4: SUBSUMES (Unidirectional, Specific → General)

Many specifics feed one generalization.

```python
SUBSUME_FACTOR = 0.10

def transfer_subsumption(link):
    """
    Subsumption: specific feeds general.

    A ──SUBSUMES──→ B

    "He lied" + "He stole" + "He cheated" → "He's untrustworthy"
    """
    specific = link.source
    general = link.target
    strength = link.strength

    transfer = specific.energy * strength * SUBSUME_FACTOR
    specific.energy -= transfer
    general.energy += transfer
```

**Why low factor:** Each specific contributes a little. The general accumulates from many sources.

---

### T5: SUPERSEDES (Draining)

New truth drains old.

```python
SUPERSEDE_FACTOR = 0.25

def transfer_supersession(link):
    """
    Supersession: old feeds new, loses in the process.

    A ──SUPERSEDES──→ B (A is old, B is new)

    "Edmund is in York" → "Edmund fled York"
    """
    old = link.source
    new = link.target
    strength = link.strength

    transfer = old.energy * strength * SUPERSEDE_FACTOR
    old.energy -= transfer
    new.energy += transfer

    # Additional drain: old loses extra (world moved on)
    old.energy *= (1 - SUPERSEDE_FACTOR * 0.5)
```

**Why draining:** Supersession isn't just transfer — the old becomes irrelevant. It loses more than it gives.

---

### T6: ABOUT (Focal Point Pulls)

Being talked about attracts energy.

```python
ABOUT_FACTOR = 0.05

def transfer_about(link):
    """
    About: focal point pulls from narratives.

    Narrative ──ABOUT──→ Character/Thing

    Reverse flow: the subject draws energy from stories about them.
    """
    narrative = link.source
    subject = link.target

    if isinstance(subject, Character):
        transfer = narrative.energy * link.strength * ABOUT_FACTOR
        narrative.energy -= transfer
        subject.energy += transfer
    # Things don't hold energy — skip
```

**Why reverse flow:** Being the subject of attention energizes you. Aldric is talked about → Aldric becomes more present.

---

### T7: CAN_LEAD_TO (Moment to Moment)

Energy flows through conversation structures.

```python
CAN_LEAD_TO_FACTOR = 0.15

def transfer_can_lead_to(link):
    """
    Conversation potential: energy flows to connected moments.

    Moment_A ──[CAN_LEAD_TO]──> Moment_B

    Unidirectional by default. Bidirectional if link.bidirectional = true.
    """
    origin = link.source
    destination = link.target
    strength = link.strength

    # Forward flow
    transfer = origin.energy * strength * CAN_LEAD_TO_FACTOR
    origin.energy -= transfer
    destination.energy += transfer

    # Reverse flow only if bidirectional
    if link.bidirectional:
        reverse = destination.energy * strength * CAN_LEAD_TO_FACTOR
        destination.energy -= reverse
        origin.energy += reverse
```

**Why unidirectional default:** Conversations flow forward. "What happened next?" pulls energy downstream.

**When bidirectional:** Parallel options, back-and-forth debates, revisitable topics.

---

### T8: CAN_SPEAK (Character to Moment)

Characters energize moments they can speak.

```python
CAN_SPEAK_FACTOR = 0.1

def transfer_can_speak(link):
    """
    Character can speak this moment → character energy flows in.

    Character ──[CAN_SPEAK]──> Moment
    """
    character = link.source
    moment = link.target
    strength = link.strength

    # Only if character is awake and present
    if character.state != 'awake':
        return

    transfer = character.energy * strength * CAN_SPEAK_FACTOR
    character.energy -= transfer
    moment.energy += transfer
```

**Why:** Characters energize their potential speech. More invested character → more energy into what they might say.

---

### T9: ATTACHED_TO (Moment from Sources)

Moments draw energy from what they're attached to.

```python
ATTACHED_TO_FACTOR = 0.1

def transfer_attached_to(link):
    """
    Moment attached to something → draws energy from it.

    Moment ──[ATTACHED_TO]──> Character | Narrative | Place | Thing

    Reverse flow: source energizes the moment.
    """
    moment = link.source
    target = link.target
    strength = link.strength

    # Only nodes with energy
    if not hasattr(target, 'energy'):
        return

    # Reverse flow: target → moment
    transfer = target.energy * strength * ATTACHED_TO_FACTOR
    target.energy -= transfer
    moment.energy += transfer
```

**Why reverse:** A moment about Edmund draws energy when Edmund is hot. Relevance emerges from what's energized.

---

### Actualization (Energy Spent)

When moment flips `active` → `spoken`:

```python
ACTUALIZATION_COST = 0.6

def actualize_moment(moment):
    """
    Moment becomes canon. Energy partially spent.
    """
    # Partial drain — recent speech still has presence
    cost = moment.energy * ACTUALIZATION_COST
    moment.energy -= cost

    # Status change
    moment.status = 'spoken'
    moment.tick_spoken = current_tick

    # Remaining energy decays normally from here
```

**Why partial (0.6):** Just-spoken moments still have presence. They fade naturally rather than vanishing.

---

### Moment Decay by Status

| Status | Decay Rate | Notes |
|--------|------------|-------|
| `possible` | 0.02 | Normal — unused possibilities fade |
| `active` | 0.01 | Slower — something is happening |
| `spoken` | 0.03 | Faster — it's done, recedes into past |
| `dormant` | 0.005 | Very slow — waiting to reactivate |
| `decayed` | N/A | No energy, no decay |

---

## MOMENT ENERGY & WEIGHT

Moments have both weight (importance) and energy (activation). Both matter for surfacing.

### Surfacing Logic

```python
def salience(moment):
    """How much should this moment surface right now?"""
    return moment.weight * moment.energy

def should_surface(moment):
    """Does this moment cross the threshold?"""
    return salience(moment) >= SURFACE_THRESHOLD
```

### Energy Flow Into Moments

Moments receive energy from:
- Characters via CAN_SPEAK links (T8)
- Narratives/Characters via ATTACHED_TO links (T9)
- Other moments via CAN_LEAD_TO links (T7)
- Player focus injection

Energy flows OUT via:
- CAN_LEAD_TO links to other moments
- Actualization (partial spend)
- Decay

### Weight Evolution

Weight changes slowly via the six strength mechanics:
- Activation (moment spoken)
- Evidence (confirms/denies attached narratives)
- Association (co-occurs with important content)
- Commitment (player acted on this)
- Intensity (high-stress context)

```python
def reinforce_moment_weight(moment, amount):
    moment.weight = min(moment.weight + amount, 1.0)
    moment.last_reinforced = current_tick
```

### Example

```
moment_aldric_confession:
  weight: 0.8   # Important (has been building)
  energy: 0.3   # Not currently active
  salience: 0.24  # Below threshold

Player asks about Edmund:
  → energy injected into Edmund-related content
  → narr_edmund_betrayal heats up
  → moment_aldric_confession attached to that narrative
  → energy flows into moment (T9)
  → energy: 0.3 → 0.7
  → salience: 0.56  # Crosses threshold
  → Moment surfaces
```

---

## FULL TICK CYCLE

```python
def energy_tick():
    """
    Complete energy cycle. Order matters.
    """

    # 1. Characters pump into narratives
    for char in graph.characters:
        character_tick(char)

    # 2. Narrative-to-narrative transfer
    for link in graph.narrative_links:
        if link.type == 'CONTRADICTS':
            transfer_contradiction(link)
        elif link.type == 'SUPPORTS':
            transfer_support(link)
        elif link.type == 'ELABORATES':
            transfer_elaboration(link)
        elif link.type == 'SUBSUMES':
            transfer_subsumption(link)
        elif link.type == 'SUPERSEDES':
            transfer_supersession(link)

    # 3. ABOUT links (focal point pulls)
    for link in graph.about_links:
        transfer_about(link)

    # 4. Moment energy flow
    for link in graph.can_speak_links:
        transfer_can_speak(link)

    for link in graph.attached_to_links:
        transfer_attached_to(link)

    for link in graph.can_lead_to_links:
        transfer_can_lead_to(link)

    # 5. Tension injection (structural pressure)
    tensions = detect_tensions()
    tension_injection(tensions)

    # 6. Decay (energy leaves system)
    apply_decay()

    # 7. Detect breaks
    breaks = [t for t in tensions if is_unsustainable(t)]

    return breaks


def apply_decay():
    """
    Energy decays from all nodes.
    Weight decays much slower, only without reinforcement.
    """
    # Energy decay (fast)
    for narrative in graph.narratives:
        rate = ENERGY_DECAY_RATE  # 0.02
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25
        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_ENERGY)

    for character in graph.characters:
        character.energy *= (1 - ENERGY_DECAY_RATE)
        character.energy = max(character.energy, MIN_ENERGY)

    for moment in graph.moments:
        rate = get_moment_decay_rate(moment.status)
        moment.energy *= (1 - rate)
        moment.energy = max(moment.energy, MIN_ENERGY)

        # Check for status transition
        if moment.status == 'possible' and moment.energy < DECAY_THRESHOLD:
            moment.status = 'decayed'

    # Weight decay (slow, only without reinforcement)
    for node in graph.all_weighted_nodes:
        if current_tick - node.last_reinforced > WEIGHT_DECAY_DELAY:
            node.weight *= (1 - WEIGHT_DECAY_RATE)  # 0.001
            node.weight = max(node.weight, MIN_WEIGHT)


def get_moment_decay_rate(status):
    return {
        'possible': 0.02,
        'active': 0.01,
        'spoken': 0.03,
        'dormant': 0.005,
        'decayed': 0.0
    }.get(status, 0.02)
```

---

## PHYSICAL GATING

Physical presence is not "proximity." It's a binary gate.

### How It Works

**Link attribute:** `presence_required: bool` on ATTACHED_TO

**Location:** `AT` link from Character to Place

### Gating Queries

**Can this moment actualize here?**

```cypher
MATCH (m:Moment {id: $moment_id})-[r:ATTACHED_TO {presence_required: true}]->(target)
OPTIONAL MATCH (target)-[:AT]->(p:Place)
WITH m, target, p
WHERE p IS NULL OR p.id = $current_place
RETURN count(*) = 0 AS blocked
```

If any `presence_required` target is not at current place → moment cannot actualize.

**Can these characters interact?**

```cypher
MATCH (a:Character {id: $char_a})-[:AT]->(p:Place)<-[:AT]-(b:Character {id: $char_b})
RETURN p IS NOT NULL AS can_interact
```

Same place → can interact. Different places → cannot.

### What This Replaces

| Old Concept | New Reality |
|-------------|-------------|
| `physical_proximity(a, b)` | Graph query on AT links |
| `narrative_proximity(n, focus)` | **Deleted** — energy IS proximity |
| `compute_focus(scene)` | **Deleted** — energy injection handles it |
| `can_actualize(moment)` | Query presence_required attachments |
| `can_interact(a, b)` | Query AT links |

### Example

```yaml
Moment:
  id: moment_aldric_confession
  text: "I need to tell you something about Edmund."

ATTACHED_TO:
  - target: char_aldric
    presence_required: true   # Aldric must be here
  - target: narr_edmund_secret
    presence_required: false  # Narrative doesn't need to be "present"
```

Aldric at camp, player at camp → moment can actualize.
Aldric in York, player at camp → moment blocked.

No function call. Graph structure encodes the rule.

---

## PARAMETERS

### Transfer Factors

| Link Type | Factor | Direction | Notes |
|-----------|--------|-----------|-------|
| CONTRADICTS | 0.15 * 2 | Bidirectional | High conductivity |
| SUPPORTS | 0.10 | Equilibrating | Allies share fate |
| ELABORATES | 0.15 | Parent → Child | Details inherit |
| SUBSUMES | 0.10 | Specific → General | Many feed one |
| SUPERSEDES | 0.25 | Old → New + drain | Replacement |
| ABOUT | 0.05 | Narrative → Subject | Being talked about |
| CAN_LEAD_TO | 0.15 | Origin → Destination | Conversation flow |
| CAN_SPEAK | 0.10 | Character → Moment | Speech potential |
| ATTACHED_TO | 0.10 | Target → Moment (reverse) | Relevance inheritance |

### Moment Decay Rates

| Status | Decay Rate | Notes |
|--------|------------|-------|
| `possible` | 0.02 | Unused possibilities fade |
| `active` | 0.01 | Something is happening |
| `spoken` | 0.03 | Done, recedes into past |
| `dormant` | 0.005 | Waiting to reactivate |

### Actualization

| Parameter | Value | Notes |
|-----------|-------|-------|
| ACTUALIZATION_COST | 0.6 | Partial drain on flip |

### Source Rates

| Source | Rate | Notes |
|--------|------|-------|
| Character pumping | 0.10 * energy | Per tick, distributed by belief strength |
| Origination bonus | *1.5 | Authors care more |
| Secret holding bonus | *1.2 | Secrets held tighter |
| Player focus | 1.0 | Per input, split across targets |
| Arrival boost | 0.5 | Character enters scene |
| News injection | 0.3 | Information arrives |
| Discovery injection | 0.5 | Something revealed |

### Sink Rates

| Sink | Rate | Notes |
|------|------|-------|
| Energy decay (narratives) | 0.02 | Per tick |
| Energy decay (core types) | 0.005 | Oaths, blood, debts (*0.25) |
| Energy decay (characters) | 0.02 | Per tick |
| Weight decay | 0.001 | Only after WEIGHT_DECAY_DELAY ticks without reinforcement |
| Actualization cost | 0.6 * energy | When moment flips |

### Weight Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| WEIGHT_DECAY_DELAY | 100 | Ticks before weight starts decaying |
| WEIGHT_DECAY_RATE | 0.001 | Very slow |
| MIN_WEIGHT | 0.01 | Never fully zero |
| SURFACE_THRESHOLD | 0.3 | salience (weight * energy) needed to surface |

### Floors & Ceilings

| Parameter | Value | Why |
|-----------|-------|-----|
| MIN_ENERGY | 0.01 | Never fully zero — can always revive |
| MIN_WEIGHT | 0.01 | Never fully zero — can always matter again |
| MAX_CHARACTER_ENERGY | 10.0 | Prevent runaway accumulation |
| MAX_NARRATIVE_ENERGY | 5.0 | Keep narratives bounded |
| MAX_MOMENT_ENERGY | 5.0 | Keep moments bounded |

---

## EMERGENT BEHAVIORS

### "Arguments Heat Both Sides"

Not because CONTRADICTS creates energy.

Because:
1. Aldric pumps into "Edmund betrayed us"
2. Edmund pumps into "I was right"
3. CONTRADICTS transfers between them (zero-sum)
4. Both stay hot because both have pumps

If Edmund dies → no pump → his side cools → argument fades.

### "Approach Creates Tension"

Not because we compute proximity. Because physical presence changes who pumps where.

1. Player travels toward York
2. Player arrives at York (AT link changes)
3. Edmund is now present (same location)
4. Edmund pumps into his narratives locally
5. Player's attention on Edmund → energy injection
6. Edmund's narratives heat up (via ABOUT reverse flow)
7. Contradiction with player's beliefs gets energy from both sides
8. Structural tension detected (both believers present + hot narratives)
9. Break becomes inevitable

**The AT link changing is the trigger.** Energy flow does the rest.

### "Forgotten Things Bite Back"

Not because hidden timer. Because neglected narratives still get pumped.

1. Debt narrative exists
2. Creditor pumps into it (constant, from their belief)
3. Player doesn't pump (doesn't believe it strongly, or doesn't think about it)
4. But creditor keeps pumping → narrative stays warm
5. Creditor travels toward player (AT link changes)
6. Now both present → can interact
7. Tension detection finds: debt narrative hot + creditor present + debtor present
8. Break: creditor demands payment

**You can't make someone else stop caring by ignoring them.**

### "The World Feels Alive"

Not because NPCs have complex AI.

Because:
1. Every character pumps into what they believe
2. Energy flows through narrative network
3. Tensions emerge from structure
4. Moments surface based on weight
5. The system has its own metabolism

No one decided "now is dramatic." The structure created drama.

### "Thinking About Someone Far Away"

Not proximity calculation. Energy injection.

1. Player says "I wonder what Aldric is doing"
2. Input parser detects reference to char_aldric
3. Energy injected into char_aldric
4. Aldric's energy flows to narratives about him (ABOUT reverse)
5. Those narratives surface (high energy = high weight moments)
6. Player "thinks about" Aldric — his stories come to mind

Aldric isn't "closer." His narratives are hotter. Same effect, no proximity concept.

---

## M11: FLIP DETECTION

Physics tick detects when moments cross the salience threshold. Canon Holder records them.

### Status Progression

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

### Detection Query

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

### Processing Multiple Ready Moments

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

### Rate Limiting

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

### Speaker Resolution

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

## M12: CANON HOLDER

**Everything is moments. Canon Holder is the gatekeeper.**

Canon Holder records what becomes real. It doesn't decide what happens — physics and handlers do that. Canon Holder makes it permanent.

### The Flow

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

### Canon Holder Responsibilities

| Responsibility | What It Does |
|----------------|--------------|
| **Record** | Flip moment `active` → `spoken` |
| **Link** | Create THEN link to previous moment |
| **Time** | Advance game time based on moment duration |
| **Trigger** | Process actions (travel, take, etc.) |
| **Strength** | Apply strength mechanics (Activation, Evidence, etc.) |
| **Notify** | Push to frontend |

### Recording Function

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

### Strength Mechanics on Record

Canon Holder triggers three of the six strength mechanics:

#### M1: Activation

```python
def apply_activation(moment):
    """Speaker's beliefs reinforced by speaking."""
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

#### M2: Evidence

```python
def apply_evidence(moment):
    """Witnesses' beliefs affected by what they saw."""
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

#### M3: Association

```python
def apply_association(moment):
    """Co-occurring narratives become linked."""
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

### Time Passage

```python
def estimate_moment_duration(moment):
    """How long does this moment take in game time?"""
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
    """Move game time forward."""
    game_state.current_time += timedelta(minutes=minutes)

    # Check for time-based events
    check_scheduled_events()

    # Decay check (large time jumps)
    if minutes > 30:
        run_decay_cycle()
```

### Action Processing

```python
def process_action(moment):
    """Execute world-changing action."""
    action = moment.action
    actor = moment.speaker
    target = get_action_target(moment)

    if action == 'travel':
        move_character(actor, target)

    elif action == 'take':
        take_thing(actor, target)

    elif action == 'give':
        give_thing(actor, target, recipient)

    elif action == 'attack':
        initiate_combat(actor, target)

    elif action == 'use':
        use_thing(actor, target)

    # Apply Commitment mechanic (M5)
    apply_commitment(actor, moment)
```

### THEN Links

History chain. Created by Canon Holder, never manually.

```python
def create_then_link(previous, current):
    """Link moments in history."""
    create_link(previous, 'THEN', current, {
        'tick': current_tick,
        'player_caused': is_player_input(),
        'time_gap_minutes': time_between(previous, current)
    })
```

**Query pattern:** `MATCH (m1)-[:THEN*]->(m2)` for conversation history.

### Frontend Notification

```python
def push_to_display(moment):
    """Send moment to frontend for display."""
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

### Simultaneous Actions Are Drama

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

### True Mutex (Rare)

True mutex = logically impossible, not just dramatic.

#### Same Character, Incompatible Actions

```
Aldric "walks east" AND Aldric "walks west" (same tick)
```

This is impossible. Resolution:

```python
def detect_same_character_mutex(moments):
    """Find moments where same character has incompatible actions."""
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
    """Higher weight wins. Loser returns to potential."""
    winner, loser = (moment_a, moment_b) if moment_a.weight > moment_b.weight else (moment_b, moment_a)

    # Winner proceeds to canon
    record_to_canon(winner)

    # Loser returns to possible, decayed
    loser.status = 'possible'
    loser.weight *= 0.5
```

#### What's Incompatible

| Action A | Action B | Mutex? |
|----------|----------|--------|
| travel east | travel west | Yes |
| attack X | attack X | No (both attack) |
| take sword | take sword | No (drama: struggle) |
| speak | speak | No (both speak) |

Most "conflicts" are actually drama to embrace.

### What Canon Holder Does NOT Do

- Generate content (that's Handlers)
- Compute energy flow (that's Physics tick)
- Block drama (simultaneous actions are fine)
- Store tension (tension is computed)
- Decide what should happen (that's Physics + Handlers)

Canon Holder only: record, link, trigger, notify.

---

## M13: AGENT DISPATCH

Four agents at three levels.

### The Agents

| Agent | Level | Responsibility | Timing |
|-------|-------|----------------|--------|
| **Runner** | World | Pressure, time, events, breaks | Tick-based |
| **Narrator** | Scene | Architecture, backstory, consequences | On demand |
| **Citizen** | Character | Dialogue, thoughts, freeform | Parallel async |
| **Canon Holder** | Record | Makes moments canon, THEN links | On flip |

### Runner (World)

```python
async def runner_tick():
    energy_tick()

    # Detect and process breaks
    tensions = detect_tensions()
    breaks = [t for t in tensions if is_unsustainable(t)]

    while breaks:
        for tension in breaks:
            await narrator_break(tension)  # Narrator generates consequences
        tensions = detect_tensions()
        breaks = [t for t in tensions if is_unsustainable(t)]

    # Scheduled events
    for event in get_due_events(current_tick):
        inject_event(event)

    update_travel_progress()
    check_time_transitions()
```

### Narrator (Scene)

```python
async def narrator_backstory(query_moment):
    """Query moment spoken → generate backstory."""
    character = get_attached_character(query_moment)
    result = await llm(backstory_prompt(character, query_moment.query))

    narrative = create_narrative(result.fact)
    create_link(character, 'BELIEVES', narrative, strength=0.8)
    create_link(character, 'ORIGINATED', narrative, strength=0.9)

    for memory in result.memories:
        m = create_moment(memory, status='dormant')
        attach(m, character)
        attach(m, narrative)
        create_link(query_moment, 'ANSWERED_BY', m)

    query_moment.query_filled = True


async def narrator_break(tension):
    """Tension broke → generate consequences."""
    result = await llm(break_prompt(tension))

    for consequence in result.consequences:
        create_moment(consequence, status='possible', weight=0.7, energy=0.9)
```

### Citizen (Character)

```python
async def citizen_respond(character, player_input):
    """Player addressed this character."""
    identity = build_character_context(character)
    result = await llm(respond_prompt(character, identity, player_input))

    m = create_moment(result.text, type='dialogue', status='possible', weight=0.6, energy=0.8)
    create_link(character, 'CAN_SPEAK', m, strength=0.9)
    return m


async def citizen_think(character):
    """Background thinking."""
    identity = build_character_context(character)
    drives = get_character_drives(character)
    result = await llm(think_prompt(character, identity, drives))

    for thought in result.thoughts:
        m = create_moment(thought.text, type=thought.type, status='possible', weight=0.3, energy=0.4)
        create_link(character, 'CAN_SPEAK', m, strength=0.7)


async def citizen_react(character, witnessed_moment):
    """Witnessed something → react."""
    result = await llm(react_prompt(character, witnessed_moment))

    if result.reacts:
        m = create_moment(result.text, status='possible', weight=0.4, energy=0.6)
        create_link(character, 'CAN_SPEAK', m, strength=0.8)
```

### Main Loop

```python
async def main_loop():
    while game_running:
        await runner_tick()

        ready = detect_ready_moments()
        for moment in ready[:MAX_MOMENTS_PER_TICK]:
            speaker = determine_speaker(moment)

            if moment.needs_generation:
                await narrator_fill_text(moment)
            if moment.query and not moment.query_filled:
                await narrator_backstory(moment)

            record_to_canon(moment, speaker, previous)
            previous = moment

            for witness in get_witnesses(moment, exclude=speaker):
                asyncio.create_task(citizen_react(witness, moment))

        if tempo.should_generate_more():
            for char in get_present_characters():
                asyncio.create_task(citizen_think(char))

        await asyncio.sleep(TICK_INTERVAL)


def on_player_input(text):
    matches = semantic_match(text)
    if matches:
        for m, score in matches:
            m.energy += score * 0.5
        return

    responder = select_responder(get_present_characters(), text)
    asyncio.create_task(citizen_respond(responder, text))
```

---

## WHAT WE DON'T DO

| Anti-pattern | Why Avoid |
|--------------|-----------|
| Set energy directly | Energy emerges from structure |
| Create energy from links | Violates conservation, unpredictable |
| Compute proximity separately | Energy IS proximity |
| Use functions for physical gating | Link attributes (presence_required, AT) |
| Arbitrary dampening | Hides broken dynamics |
| Magic thresholds | "0.7" means nothing without structure |
| Author tensions | Tensions emerge, aren't declared |

---

*"Characters pump. Links route. Decay drains. Energy IS proximity. The story emerges."*


---

## Physics Tick

### Core Principle

**The graph is always running.**

The tick is not "processing a cascade." The tick is one heartbeat of a continuous system. The graph never stops. Speed controls how fast we tick and what we display.

---

### What Triggers a Tick

| Trigger | Notes |
|---------|-------|
| Time interval | Based on current speed setting |
| Player input | May trigger immediate tick |
| Handler completion | New potentials ready to integrate |

---

### Tick Steps (Sequential)

```python
def physics_tick(current_time: float):
    """
    One heartbeat of the continuous system.
    Steps must execute in order.

    Energy model: see the Energy Mechanics section for full details.
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

### Step 1: Character Pumping

Characters are batteries. They pump energy into narratives they believe.

```python
def character_pumping():
    """
    Characters inject energy into narratives via BELIEVES links.
    Pump rate modified by state only. No proximity filter.
    Energy flow through the graph handles relevance.
    See the Energy Mechanics section for full details.
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

### Step 2: Energy Transfer

Links route energy between narratives. Zero-sum between linked nodes.

```python
def transfer_energy():
    """
    Narrative-to-narrative and narrative-to-subject transfers.
    See the Energy Mechanics section for full transfer mechanics.
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

### Step 3: Tension Injection

Detected tensions concentrate energy from participants into the crisis.

```python
def tension_injection(tensions):
    """
    Structural tensions draw energy from involved characters.
    Tension is computed, not stored. See the Energy Mechanics section.
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

### Step 4: Decay

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

### Step 5: Moment Weight Computation

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

### Step 6: Flip Detection

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

#### Deterministic vs Probabilistic

For v1, flipping is deterministic. `weight >= 0.8` = flip.

Probabilistic (weight = probability per tick) adds organic feel but complicates reasoning. Can add later if mechanical feel is a problem.

---

### Step 7: Emit to Canon Holder

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

### Parameters

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

See the Energy Mechanics section for transfer factors, state modifiers, and proximity rules.

---

### Graph States

The graph is always running but exhibits different states:

| State | Characteristics |
|-------|-----------------|
| **Active** | High energy, many flips, drama unfolding |
| **Quiet** | Low energy, few flips, equilibrium |
| **Critical** | Energy building, thresholds approaching, tension rising |

But never **stopped**.

---

### Tick Rate by Speed

| Speed | Ticks Per Second | Notes |
|-------|------------------|-------|
| 1x | ~0.2 | One tick per moment duration |
| 2x | ~2.0 | Rapid, filtered display |
| 3x | Max system speed | Only interrupts shown |

See the Speed Controller section for full speed controller logic.

---

### What Physics Does NOT Do

- Generate new moments (that's Handlers)
- Decide what content to create (that's Handlers)
- Record history (that's Canon Holder)
- Modify world state (that's Action Processing)
- Author tensions (tensions emerge from structure)

Physics only: pump, transfer, decay, detect.

---

### Invariants

1. **Energy conservation:** Pumps in = decay + actualization out (links are zero-sum)
2. **Continuous:** Graph never stops, only changes rate
3. **Deterministic flips:** Same state → same flips (for v1)
4. **Derived weights:** Moment weight is computed, not accumulated

---

### Relationship to the Energy Mechanics section

This file defines the **tick cycle** — when and in what order things happen.

the Energy Mechanics section defines the **energy mechanics** — how energy flows, what creates it, what consumes it.

| This File | Energy File |
|-----------|-------------|
| Tick orchestration | Transfer formulas |
| Step ordering | Link type behaviors |
| Parameter values | Emergent behaviors |
| What happens when | Why it works |

---

*"The tick is one heartbeat of a continuous system."*


---

## Canon Holder

### Core Principle

**Everything is moments. Canon Holder is the gatekeeper.**

Canon Holder records what becomes real. It doesn't decide what happens — physics and handlers do that. Canon Holder makes it permanent.

---

### The Flow

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

### Canon Holder Responsibilities

| Responsibility | What It Does |
|----------------|--------------|
| **Record** | Flip moment `active` → `spoken` |
| **Link** | Create THEN link to previous moment |
| **Time** | Advance game time based on moment duration |
| **Trigger** | Process actions (travel, take, etc.) |
| **Strength** | Apply strength mechanics (Activation, Evidence, etc.) |
| **Notify** | Push to frontend |

---

### The Code Shape

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

### Flip Detection

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

### Status Progression

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

### Who Speaks?

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

### Rate Limiting

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

### Actualization Cost

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

### Strength Mechanics Applied

Canon Holder triggers three of the six strength mechanics on record:

#### M1: Activation

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

#### M2: Evidence

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

#### M3: Association

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

### Action Processing

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

### Time Passage

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

### THEN Links

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

### Frontend Notification

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

### Simultaneous Actions Are Drama

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

### True Mutex (Rare)

True mutex = logically impossible, not just dramatic.

#### Same Character, Incompatible Actions

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

#### What's Incompatible

| Action A | Action B | Mutex? |
|----------|----------|--------|
| travel east | travel west | Yes |
| attack X | attack X | No (both attack) |
| take sword | take sword | No (drama: struggle) |
| speak | speak | No (both speak) |

Most "conflicts" are actually drama to embrace.

---

### History Is Queryable

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

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| `SURFACE_THRESHOLD` | 0.3 | salience (weight × energy) needed |
| `ACTUALIZATION_COST` | 0.6 | Partial energy drain on record |
| `MAX_MOMENTS_PER_TICK` | 5 | Rate limit |
| `MIN_MOMENT_GAP_MS` | 100 | Display pacing |

---

### Invariants

1. **Immutability:** Once `spoken`, a moment never changes status
2. **THEN chain:** Every `spoken` moment (except first) has exactly one incoming THEN link
3. **Time monotonic:** Game time only moves forward
4. **Rate limited:** Max 5 moments per tick
5. **Strength applied:** All three mechanics (Activation, Evidence, Association) run on every record
6. **Drama welcome:** Simultaneous actions are scenes, not conflicts

---

### What Canon Holder Does NOT Do

- Generate content (that's Handlers)
- Compute energy flow (that's Physics tick)
- Block drama (simultaneous actions are fine)
- Store tension (tension is computed)
- Decide what should happen (that's Physics + Handlers)

Canon Holder only: record, link, trigger, notify.

---

*"Canon Holder makes it real. Everything else is possibility."*


---

## Character Handlers

### Core Principle

**One handler per character. Triggered on flip. That's it.**

No arbitrary triggers. No cooldowns. No caps. The physics determines when handlers run.

---

### When Handlers Run

**On flip.** When a moment ATTACHED_TO this character crosses the flip threshold.

```python
def on_moment_flip(moment: Moment):
    """
    Called by Canon Holder when a moment flips.
    Triggers handler for the attached character.
    """
    character = query("""
        MATCH (m:Moment {id: $id})-[:ATTACHED_TO]->(c:Character)
        RETURN c
    """, id=moment.id)

    if character:
        run_handler(character.id, triggered_by=moment)
```

#### Why No Other Triggers

- Character important and close? → More energy per tick → flips more often → handler runs more
- Character distant or minor? → Less energy → flips rarely → handler runs rarely

**The physics IS the scheduling.**

No cooldowns needed. Handler produces moments with weight. Those moments exist in the graph. Until they actualize or decay, character has potentials.

If potentials depleted → character's moments have low weight → character keeps pumping into narratives → those narratives energize new moments → eventually something flips → handler runs.

---

### What Handler Receives

```python
@dataclass
class HandlerContext:
    character: Character          # Identity, beliefs, relationships, voice
    location: Place               # Where they are
    present: List[Character]      # Who else is here
    recent_history: List[Moment]  # Last N actualized moments they witnessed
    trigger: Moment               # What flipped to cause this run
    speed: SpeedSetting           # Current game speed (for prompt framing)
```

#### Context Assembly

```python
def build_handler_context(character_id: str, trigger: Moment) -> HandlerContext:
    character = get_character(character_id)
    location = get_character_location(character_id)
    present = get_characters_at(location.id)

    recent_history = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT 10
    """, char_id=character_id)

    return HandlerContext(
        character=character,
        location=location,
        present=present,
        recent_history=recent_history,
        trigger=trigger,
        speed=get_current_speed()
    )
```

---

### What Handler Produces

```python
@dataclass
class HandlerOutput:
    moments: List[MomentDraft]      # New potential moments
    links: List[LinkDraft]           # CAN_LEAD_TO, ATTACHED_TO, REFERENCES
    questions: List[str]             # Queries for Question Answerer
```

#### MomentDraft

```python
@dataclass
class MomentDraft:
    text: str                        # The content
    type: str                        # dialogue, thought, action, narration
    action: Optional[str]            # travel, take, attack, give (if action)
    tone: Optional[str]              # whispered, shouted, cold, warm
    # Note: NO weight field. Physics assigns weight.
```

#### Handler Does NOT Set Weight

Handler outputs text + links. Physics derives weight from:
- CAN_SPEAK link strength (set by handler based on relevance to trigger)
- Character's current energy
- ATTACHED_TO link strengths to narratives/characters

Weight = sum of (source.energy × link.strength). Energy IS proximity — no separate calculation.

No handler can "force" a high-weight moment. It proposes. Physics evaluates.

---

### Handler Implementation

```python
async def run_handler(character_id: str, triggered_by: Moment) -> HandlerOutput:
    """
    Run the character's handler. Returns new potentials.
    """
    context = build_handler_context(character_id, triggered_by)

    # Build prompt based on character type and speed
    prompt = build_handler_prompt(context)

    # LLM call
    response = await llm.complete(prompt)

    # Parse structured output
    output = parse_handler_response(response)

    # Inject into graph (physics assigns weights)
    inject_handler_output(character_id, output)

    return output
```

#### Prompt Framing by Speed

```python
def build_handler_prompt(context: HandlerContext) -> str:
    base = f"""
    You are {context.character.name}.
    {context.character.voice_description}

    Location: {context.location.name}
    Present: {', '.join(c.name for c in context.present)}

    What just happened: {context.trigger.text}
    Recent history: {format_history(context.recent_history)}

    Generate potential moments (things you might say, think, or do).
    """

    # Speed-aware framing
    if context.speed == '2x':
        base += """
        You're on a journey. Generate brief atmospheric moments,
        not full dialogue. Unless something important needs to be said.
        """
    elif context.speed == '3x':
        base += """
        Time is passing quickly. Only generate moments if something
        critical demands attention.
        """

    return base
```

---

### Moment Injection (Physics Side)

```python
def inject_handler_output(character_id: str, output: HandlerOutput):
    """
    Inject handler output into graph.

    Weight is derived from energy, not set directly.
    We set link strengths which determine energy flow → weight.
    See the Energy Mechanics section for full model.
    """
    character = get_character(character_id)

    for draft in output.moments:
        # Calculate link strength (how much character energy flows to this moment)
        relevance = calculate_relevance(draft, output.trigger)
        link_strength = max(0.3, min(0.9, relevance))

        # Create moment (weight will be computed by physics tick)
        moment_id = create_moment(
            text=draft.text,
            type=draft.type,
            action=draft.action,
            tone=draft.tone,
            weight=0.0,  # Derived, not set
            status='possible'
        )

        # Create CAN_SPEAK link (character energy → moment weight)
        create_link('CAN_SPEAK', character_id, moment_id, {
            'strength': link_strength
        })

        # Create ATTACHED_TO link
        create_link('ATTACHED_TO', moment_id, character_id, {
            'strength': link_strength,
            'presence_required': True,
            'persistent': True
        })

    # Process additional links
    for link in output.links:
        create_link(link.type, link.from_id, link.to_id, link.properties)

    # Queue questions for async answering
    for question in output.questions:
        question_answerer.queue(character_id, question)
```

---

### Handler Scaling

| Character Type | Handler Complexity |
|----------------|-------------------|
| Major (companions, antagonists) | Full LLM, rich context |
| Minor (named NPCs) | Lighter LLM, focused context |
| Grouped (guards, crowd) | Single handler for group |

#### Grouped Characters

"The Guards" can be a single character node until narrative needs differentiation.

```yaml
Character:
  id: char_guards
  name: "The Guards"
  type: group
```

They flip. Their handler runs. They act as one. 20 peasants = 1 handler, not 20 LLM calls.

#### Splitting Groups

Triggered by direct address or action targeting individual:

```python
def handle_direct_address(input_text: str, target: str):
    """
    Player addresses individual in a group.
    """
    # "You there, guard on the left!"
    if is_group_member_address(target):
        group = get_parent_group(target)
        individual = split_from_group(group, target)
        # individual now has own node, inherits group properties
```

Handler can also request split:

```python
## In handler output
{
    "split_request": {
        "from_group": "char_guards",
        "new_character": {
            "name": "The Tall Guard",
            "reason": "He steps forward, breaking ranks"
        }
    }
}
```

---

### Parallel Execution

Multiple flips = multiple parallel handler calls.

```python
async def process_flips(flipped_moments: List[Moment]):
    """
    Run handlers in parallel for all flipped moments.
    """
    tasks = []

    for moment in flipped_moments:
        character = get_attached_character(moment)
        if character:
            task = run_handler(character.id, triggered_by=moment)
            tasks.append(task)

    # Parallel execution
    results = await asyncio.gather(*tasks)

    # Each handler only writes its own character
    # No conflicts because of isolation
```

#### Why Parallel Is Safe

Each handler only writes for its character. Handler isolation is an invariant. No conflicts possible.

4 flips = 4 parallel LLM calls. Wall-clock time is ~one call, not four sequential.

---

### Reaction Scope

**Handlers only write for their own character.**

Aldric speaks. Mildred flinches. Who writes the flinch?

NOT Aldric's handler.

```
Aldric speaks (moment actualizes)
  → Energy propagates to Mildred (she witnessed, ATTACHED_TO link)
  → Her weight increases
  → She flips
  → Her handler runs
  → She generates flinch potential
  → Flinch may actualize
```

Each handler only writes its own character. Reactions propagate through energy.

---

### Pre-Generation Strategy

The graph should never be sparse for active characters.

```python
def on_character_enters_scene(character_id: str, location_id: str):
    """
    Pre-generate potentials when character enters.
    """
    # Create a synthetic "arrival" moment
    arrival = create_moment(
        text=f"{character.name} arrives.",
        type='narration',
        weight=0.5,
        status='active'
    )

    # Trigger handler with arrival as trigger
    run_handler(character_id, triggered_by=arrival)

    # By the time player engages, potentials exist
```

If truly novel (player says something completely unexpected):
- Energy flows → player character receives it (always present)
- Player character's handler runs
- "You're not sure anyone knows how to respond to that."

The player character is the fallback. They always have something.

---

### What Handler Does NOT Do

- Decide what actualizes (only proposes)
- Write for other characters (scope isolation)
- Modify world state directly (that's Action Processing)
- Set weights (that's Physics)

---

### Invariants

1. **Scope isolation:** Handler only writes for its character
2. **Triggered by flip:** No other triggers (physics is scheduler)
3. **No weight control:** Handler proposes, physics assigns weight
4. **Parallel safe:** Multiple handlers can run simultaneously

---

*"The physics IS the scheduling."*


---

## Action Processing

### Core Principle

**Moments with action fields modify world state.**

Everything is a moment. But moments with `action` field have consequences beyond display. They change the graph structure (AT links, health, possessions, relationships).

---

### Why Actions Are Special

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

### Action Queue

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

### Action Processing Steps

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

### Step 1: Validate

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

#### Why Validation?

Between canon recording and action processing, state may have changed:
- Another action executed first
- Time passed
- World event occurred

Validation catches stale actions.

---

### Step 2: Execute

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

#### Travel

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

#### Take

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

#### Attack

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

#### Give

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

### Step 3: Generate Consequences

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

### Step 4: Inject Consequences

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

### Mutex Handling

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

### Action Types Reference

| Action | Modifies | Consequences |
|--------|----------|--------------|
| `travel` | Character AT links | Departure/arrival notices |
| `take` | Thing AT/CARRIES links | Observation moment |
| `attack` | Health, relationships | Strike moment, witness reactions |
| `give` | CARRIES links | Transfer observation |
| `speak` | Nothing (just moment) | None |

---

### Sequential Processing

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

### What Action Processing Does NOT Do

- Run in parallel (must be sequential)
- Generate dialogue (that's Handlers)
- Decide action priority (that's Canon order)

---

### Invariants

1. **Sequential execution:** One action at a time
2. **Validation first:** Check before execute
3. **Consequences propagate:** Actions generate observable moments
4. **State consistency:** No conflicting graph modifications

---

*"Actions are where moments change the world."*


---

## Player Input Processing

### Core Principle

**Player input is a perturbation, not an ignition.**

The graph is already running. Player input adds energy. Energy propagates. Things flip. This is not "starting a cascade" — it's perturbing a living system.

---

### Input Flow

```
Player submits text
    ↓
[SEQUENTIAL] Parse, create moment, link, inject
    ↓
[PHYSICS] Energy spreads through links
    ↓
[PHYSICS] Tick detects flips
    ↓
[CANON] Records, emits to display
    ↓
[PARALLEL] Character handlers triggered
```

---

### Step 1: Parse

Extract references from input text (names, places, things).

```python
def parse_input(text: str, context: SceneContext) -> ParseResult:
    """
    Extract references (names, places, things).
    UI may have already assisted with autocomplete.
    """
    references = []

    # Character names
    for char in context.present_characters:
        if char.name.lower() in text.lower():
            references.append(Reference(type='character', id=char.id, name=char.name))
        # Also check nicknames, titles
        for alias in char.aliases:
            if alias.lower() in text.lower():
                references.append(Reference(type='character', id=char.id, name=alias))

    # Place names
    if context.location.name.lower() in text.lower():
        references.append(Reference(type='place', id=context.location.id, name=context.location.name))

    # Thing names
    for thing in context.visible_things:
        if thing.name.lower() in text.lower():
            references.append(Reference(type='thing', id=thing.id, name=thing.name))

    return ParseResult(text=text, references=references)
```

#### UI-Assisted Recognition

Recognition happens at input time, not query time.

```
Player types: "Al"
    ↓
UI shows dropdown: "Aldric"
    ↓
Player selects
    ↓
Text shows: "Aldric" (highlighted)
    ↓
Reference already recognized before submit
```

Direct address strengthens the energy link. "Aldric, what do you think?" hits harder than "What does everyone think?"

---

### Step 2: Create Moment

Create a moment node for the player's input.

```python
def create_player_moment(parsed: ParseResult, player: Character, location: Place) -> Moment:
    """
    Create moment for player's speech.
    """
    moment_id = generate_id('moment')

    query("""
        CREATE (m:Moment {
            id: $id,
            text: $text,
            type: 'dialogue',
            status: 'spoken',
            weight: 1.0,
            tick_created: $tick,
            tick_spoken: $tick
        })
    """, id=moment_id, text=parsed.text, tick=current_tick())

    return get_moment(moment_id)
```

Player moments are immediately `spoken` (canon). They're not potentials — the player said them.

---

### Step 3: Create Links

Link the moment to relevant nodes.

```python
def create_input_links(moment: Moment, parsed: ParseResult, context: SceneContext):
    """
    Create links from player moment to relevant nodes.
    """
    # ATTACHED_TO player (they said it)
    create_link('ATTACHED_TO', moment.id, context.player.id, {
        'presence_required': False,
        'persistent': True
    })

    # ATTACHED_TO current location
    create_link('ATTACHED_TO', moment.id, context.location.id, {
        'presence_required': False,
        'persistent': True
    })

    # ATTACHED_TO all present characters (they heard it)
    for char in context.present_characters:
        create_link('ATTACHED_TO', moment.id, char.id, {
            'presence_required': False,
            'persistent': True
        })

    # REFERENCES for recognized names/things (strong energy transfer)
    for ref in parsed.references:
        create_link('REFERENCES', moment.id, ref.id, {
            'weight': 1.0  # Direct reference = strong link
        })

    # CAN_SPEAK link (player spoke this)
    create_link('CAN_SPEAK', context.player.id, moment.id, {
        'weight': 1.0
    })
```

---

### Step 4: Inject Energy

Add energy to the system based on input.

```python
def inject_input_energy(moment: Moment, parsed: ParseResult, context: SceneContext):
    """
    Player input injects energy. Referenced nodes receive based on strength.
    """
    base_energy = INPUT_ENERGY_BASE  # e.g., 0.5

    # Direct references get full energy
    for ref in parsed.references:
        if ref.type == 'character':
            # Boost all moments attached to this character
            query("""
                MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
                WHERE m.status = 'possible'
                SET m.weight = m.weight + $energy
            """, char_id=ref.id, energy=base_energy)

    # All present characters get partial energy (they heard)
    for char in context.present_characters:
        if char.id not in [r.id for r in parsed.references]:
            query("""
                MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
                WHERE m.status = 'possible'
                SET m.weight = m.weight + $energy
            """, char_id=char.id, energy=base_energy * 0.3)
```

#### Names Have Power

```python
## "Aldric, what do you think?"
## Aldric directly referenced → full energy boost

## "What does everyone think?"
## No direct reference → distributed partial energy
```

Direct address targets energy. Indirect speech diffuses it.

---

### Step 5: Trigger Physics

After injection, physics takes over.

```python
def process_input(text: str):
    """
    Full input processing pipeline.
    """
    context = get_current_scene_context()

    # 1. Parse
    parsed = parse_input(text, context)

    # 2. Create moment
    moment = create_player_moment(parsed, context.player, context.location)

    # 3. Create links
    create_input_links(moment, parsed, context)

    # 4. Inject energy
    inject_input_energy(moment, parsed, context)

    # 5. Emit player moment to display (immediate)
    display_queue.add(moment)

    # 6. Trigger physics tick (may be immediate based on settings)
    physics.tick()

    return moment
```

---

### Energy Must Land

When energy enters, it must go somewhere.

```python
def ensure_energy_lands(context: SceneContext):
    """
    If no moments flip after input, energy returns to player character.
    Player character always has a handler → something always happens.
    """
    # After physics tick, check if anything flipped
    if not any_moments_flipped():
        # No response from NPCs
        # Energy flows back to player character
        player_fallback_energy = FALLBACK_ENERGY

        query("""
            MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $player_id})
            WHERE m.status = 'possible'
            SET m.weight = m.weight + $energy
        """, player_id=context.player.id, energy=player_fallback_energy)

        # Player character's handler will produce observation
        # "The silence stretches. No one meets your eye."
```

There is no "nothing happens." There is only "the silence stretches."

---

### Auto-Pause on Input

At any speed, typing auto-pauses or auto-drops to 1x.

```python
def on_input_start():
    """
    Player began typing. Pause or slow down.
    """
    if current_speed() in ['2x', '3x']:
        set_speed('1x')
        # Or: pause until submit
```

Player can resume speed after input processed.

---

### What Input Processing Does NOT Do

- Generate NPC responses (that's Handlers)
- Decide what happens (that's Physics + Canon)
- Block on LLM (input creates moment immediately)

---

### Invariants

1. **Immediate moment creation:** Player input becomes moment instantly
2. **Energy injection:** Input always adds energy to system
3. **Something happens:** Energy must land somewhere (player fallback)
4. **Direct address matters:** Named references get more energy

---

*"Player input is a perturbation, not an ignition."*


---

## Question Answering

### Core Principle

**When a handler queries the graph and gets sparse results, invent the missing information.**

Question Answering fills gaps in world knowledge. It creates backstory, relationships, and history that didn't exist until needed.

---

### When Questions Arise

Handler asks a question. Graph returns sparse/nothing.

```python
## In character handler
def generate_response(context: HandlerContext):
    # Handler needs to know about father
    father_info = query_graph("Who is my father?", context.character.id)

    if father_info.is_sparse():
        # Queue question for answering
        question_answerer.queue(
            asker=context.character.id,
            question="Who is my father?",
            context=context
        )
        # Handler continues with what it knows
        # Does NOT block waiting for answer
```

---

### Not Async in "Fire and Forget" Sense

The session runs until it completes. It produces nodes. Nodes enter graph with initial weight.

```
Handler runs
  → asks "Who is my father?"
  → Question Answerer session starts (parallel)
  → Handler continues with what it knows
  → Handler finishes, outputs potentials
  → Later: QA completes, injects nodes with energy
  → Those nodes propagate naturally via physics
```

Handler never waits for QA. QA is fire-and-complete, not fire-and-wait.

---

### Question Answerer Flow

```python
async def answer_question(asker_id: str, question: str, context: dict):
    """
    Answer a question by inventing consistent information.
    Session runs until complete, then injects results.
    """
    # 1. GATHER — Get relevant existing facts
    existing = gather_relevant_facts(asker_id, question)

    # 2. GENERATE — Invent answer via LLM
    answer = await generate_answer(question, existing, context)

    # 3. VALIDATE — Check consistency
    if not validate_consistency(answer, existing):
        answer = await regenerate_with_constraints(question, existing, answer.conflicts)

    # 4. INJECT — Create nodes in graph
    inject_answer(asker_id, question, answer)
```

---

### Step 1: Gather Existing Facts

Query graph for anything relevant to constrain the answer.

```python
def gather_relevant_facts(asker_id: str, question: str) -> ExistingFacts:
    """
    Find existing information that constrains the answer.
    """
    asker = get_character(asker_id)

    facts = ExistingFacts()

    # Character's existing family
    facts.family = query("""
        MATCH (c:Character {id: $id})-[:FAMILY*1..2]-(relative:Character)
        RETURN relative
    """, id=asker_id)

    # Character's origin place
    facts.origin = query("""
        MATCH (c:Character {id: $id})-[:FROM]->(p:Place)
        RETURN p
    """, id=asker_id)

    # Character's existing beliefs/narratives
    facts.beliefs = query("""
        MATCH (c:Character {id: $id})-[:BELIEVES]->(n:Narrative)
        RETURN n
    """, id=asker_id)

    # Historical events character witnessed
    facts.history = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken
        LIMIT 20
    """, id=asker_id)

    return facts
```

---

### Step 2: Generate Answer

Use LLM to invent consistent answer.

```python
async def generate_answer(question: str, existing: ExistingFacts, context: dict) -> Answer:
    """
    Generate answer using LLM.
    """
    prompt = f"""
    A character in Norman England (1067) is wondering: "{question}"

    Existing facts about this character:
    - Family: {format_family(existing.family)}
    - Origin: {existing.origin}
    - Beliefs: {format_beliefs(existing.beliefs)}
    - Recent history: {format_history(existing.history)}

    Invent an answer that:
    1. Does NOT contradict any existing facts
    2. Fits the historical setting (Norman Conquest era)
    3. Creates potential for drama
    4. Feels specific and real, not generic

    Return structured output:
    - New characters (if any): name, relationship, status (alive/dead), traits
    - New places (if any): name, type, relationship to character
    - New events (if any): what happened, when, who was involved
    - Potential moments: memories that could surface
    """

    response = await llm.complete(prompt)
    return parse_answer(response)
```

---

### Step 3: Validate Consistency

Check that invented information doesn't contradict existing graph.

```python
def validate_consistency(answer: Answer, existing: ExistingFacts) -> bool:
    """
    Ensure answer doesn't contradict existing facts.
    """
    # Check family conflicts
    for new_char in answer.new_characters:
        if new_char.relationship == 'father':
            existing_father = find_existing_father(existing.family)
            if existing_father and existing_father.id != new_char.id:
                return False  # Conflict: already has different father

    # Check place conflicts
    for new_place in answer.new_places:
        if new_place.relationship == 'birthplace':
            existing_origin = existing.origin
            if existing_origin and existing_origin.id != new_place.id:
                return False  # Conflict: already has different origin

    # Check temporal conflicts
    for new_event in answer.new_events:
        if conflicts_with_history(new_event, existing.history):
            return False

    return True
```

---

### Step 4: Inject Answer

Create nodes in graph with initial energy.

```python
def inject_answer(asker_id: str, question: str, answer: Answer):
    """
    Inject answer into graph. Physics takes over from here.
    """
    # Create new character nodes
    for new_char in answer.new_characters:
        char_id = create_character(
            name=new_char.name,
            status=new_char.status,
            traits=new_char.traits
        )

        # Create relationship link
        create_link('FAMILY', asker_id, char_id, {
            'relationship': new_char.relationship
        })

    # Create new place nodes
    for new_place in answer.new_places:
        place_id = create_place(
            name=new_place.name,
            type=new_place.type
        )

        # Create relationship link
        create_link('FROM', asker_id, place_id, {
            'relationship': new_place.relationship
        })

    # Create potential memory moments
    for memory in answer.potential_moments:
        moment_id = create_moment(
            text=memory.text,
            type='thought',
            weight=ANSWER_INITIAL_WEIGHT,  # e.g., 0.4
            status='possible'
        )

        create_link('ATTACHED_TO', moment_id, asker_id, {
            'presence_required': True,
            'persistent': True
        })

    # Create ANSWERED_BY link for traceability
    question_moment = create_moment(
        text=f"[Question: {question}]",
        type='meta',
        weight=0.0,  # Not for display
        status='answered'
    )

    for node_id in answer.all_created_node_ids():
        create_link('ANSWERED_BY', question_moment, node_id, {})
```

---

### No Special Mechanism for Integration

The answer doesn't "boost" anything specially. It creates nodes. Nodes have energy. Energy propagates. That's it.

```python
## After injection, physics handles integration:

## New father character exists
## Memory moments attached to asker exist
## These have initial weight (e.g., 0.4)

## Next tick:
## - Energy propagates through FAMILY links
## - Memory moments may get boosted if relevant
## - If weight crosses threshold, memory surfaces

## No special "integrate answer" logic
## Just physics
```

If the answer is relevant, its energy reaches relevant moments. If not, it decays like everything else.

---

### Constraints

Invented information must:

| Constraint | Why |
|------------|-----|
| Not contradict existing graph | Consistency |
| Fit established facts | Coherence |
| Fit historical setting | Immersion |
| Create potential drama | Gameplay value |
| Be specific, not generic | Memorability |

---

### Example: "Who is my father?"

```
Handler for Aldric asks: "Who is my father?"
Graph returns: nothing (sparse)

Question Answerer runs:

Existing facts:
- Aldric is Saxon
- Aldric is from York
- Aldric has a brother (Edmund)
- Aldric witnessed the Norman invasion

Generated answer:
- New character: Wulfstan (father, deceased)
  - Traits: blacksmith, stubborn, proud
  - Death: killed defending York against Normans
- New moment: "Father's hammer still hangs in the forge."
- New moment: "He said 'never bow' the day before they came."

Injected:
- Character node: char_wulfstan
- FAMILY link: Aldric -> Wulfstan (father)
- Moment: "Father's hammer..." (weight 0.4, possible)
- Moment: "He said 'never bow'..." (weight 0.4, possible)
- ANSWERED_BY links for traceability

Later:
- Conversation touches on fathers
- Energy propagates to Aldric's moments
- Memory crosses threshold
- Aldric says: "He said 'never bow' the day before they came."
```

---

### What Question Answerer Does NOT Do

- Block handlers (they continue without waiting)
- Force moments to surface (physics decides)
- Override existing facts (must be consistent)
- Generate dialogue directly (creates potentials)

---

### Invariants

1. **Non-blocking:** Handlers never wait for answers
2. **Consistency:** Answers cannot contradict existing graph
3. **Physics integration:** No special boost, just node injection
4. **Traceability:** ANSWERED_BY links track what was invented

---

*"The answer doesn't boost anything specially. It creates nodes. Nodes have energy. That's it."*


---

## Speed Controller

### Core Principle

**The player controls the speed of time, not the content.**

At 1x, every moment breathes. At 2x, time compresses but conversation persists. At 3x, the world rushes until drama demands attention.

Speed changes display, not reality. The same events happen at any speed.

---

### The Interface

```
[⏸]  [ 1x 🗣️ ]  [ 2x 🚶 ]  [ 3x ⏩ ]  [_____________________ input field]
```

---

### Three Speeds

| Speed | Name | Feel | Tick Rate |
|-------|------|------|-----------|
| **1x 🗣️** | Conversation | Present | ~0.2/sec (one per moment) |
| **2x 🚶** | Journey | Montage | ~2/sec (rapid) |
| **3x ⏩** | Skip | Fast-forward | Max system speed |

---

### What Each Speed Shows

#### 1x — Everything

```python
def display_at_1x(moment: Moment) -> bool:
    """At 1x, everything displays."""
    return True
```

- Every moment displays fully
- Natural pacing, deliberate
- Player reads, absorbs, responds

#### 2x — Montage with Conversation

```python
def display_at_2x(moment: Moment) -> bool:
    """
    At 2x, world compresses but conversation persists.
    """
    if moment.type == 'dialogue':
        return True  # Conversation always shows
    if moment.weight >= HIGH_WEIGHT_THRESHOLD:  # e.g., 0.7
        return True  # Important moments show
    if moment.type == 'montage':
        return True  # Atmospheric moments show (muted)

    return False  # Skip low-weight non-dialogue
```

Two things at once: travel and intimacy. Like film.

#### 3x — Only Interrupts

```python
def display_at_3x(moment: Moment) -> bool:
    """
    At 3x, only interrupts break through.
    """
    return is_interrupt(moment)
```

- World runs as fast as system processes
- Display shows blur/motion, streaming text
- Only interrupt moments break through

---

### Display Distinction at 2x

| Type | Visual Style |
|------|--------------|
| World/montage | Muted color, smaller, italic, flows upward |
| Conversation | Full color, larger, centered, pauses for reading |

```python
def get_display_style(moment: Moment, speed: str) -> DisplayStyle:
    if speed == '2x':
        if moment.type in ['dialogue', 'thought']:
            return DisplayStyle.FULL  # Vivid, centered
        else:
            return DisplayStyle.MUTED  # Compressed, streaming

    return DisplayStyle.FULL
```

---

### Weight Filtering

| Weight | 1x | 2x | 3x |
|--------|-----|-----|-----|
| High (≥0.7) | Full display | Full display | Only if interrupt |
| Medium (0.4-0.7) | Full display | Brief or skip | Skip |
| Low (<0.4) | Full display | Skip | Skip |

```python
def should_display(moment: Moment, speed: str) -> bool:
    if speed == '1x':
        return True

    elif speed == '2x':
        if moment.type == 'dialogue':
            return True
        return moment.weight >= 0.4

    elif speed == '3x':
        return is_interrupt(moment)

    return True
```

---

### Interrupt Conditions

Interrupts trigger auto-pause to 1x.

```python
def is_interrupt(moment: Moment) -> bool:
    """
    Check if moment should interrupt fast-forward.
    """
    # Player character directly addressed
    if player_directly_addressed(moment):
        return True

    # Combat initiated
    if moment.action == 'attack':
        return True

    # Major character arrival
    if is_major_arrival(moment):
        return True

    # Tension threshold crossed
    if tension_boiling_over(moment):
        return True

    # Decision point (player choices available)
    if has_player_choices(moment):
        return True

    # Discovery (new significant narrative)
    if is_significant_discovery(moment):
        return True

    # Danger to player or companions
    if threatens_player_or_companions(moment):
        return True

    return False
```

#### Interrupt Definitions (Weight/Link Based)

| Interrupt Type | Definition |
|----------------|------------|
| Direct address | Player character's name in REFERENCES link |
| Combat | Moment with `action: attack` becomes canon |
| Major arrival | Character with importance > 0.7 enters scene |
| Tension boils | Detected tension pressure > 0.9 (computed from structure) |
| Decision point | Moment with multiple CAN_LEAD_TO from player |
| Discovery | Narrative node created with player in ATTACHED_TO |
| Danger | Moment with THREATENS → player or companion |

All weight-based or link-based. No magic.

---

### The Snap — 3x to 1x Transition

When interrupt detected at 3x, the transition is visceral.

```python
async def execute_snap(interrupt_moment: Moment):
    """
    The Snap: transition from 3x to 1x.
    """
    # Phase 1: Running (player sees this already)
    # - Motion blur effect
    # - Muted colors
    # - Text small, streaming upward

    # Phase 2: The Beat (300-500ms)
    await display_freeze()
    await asyncio.sleep(0.4)  # The pause where dread lives

    # Phase 3: Arrival
    set_speed('1x')
    display_moment_vivid(interrupt_moment)
    # - Crystal clear, full color
    # - Large, centered, deliberate
```

#### Visual Phases

**Phase 1: Running (3x)**
- Motion blur effect
- Muted colors
- Text small, streaming upward, fading fast
- Sound: whoosh/wind (if audio)

**Phase 2: The Beat**
- Screen sharpens (freeze)
- Silence — 300-500ms pause
- Nothing displays
- Tension in the gap

**Phase 3: Arrival (1x)**
- Crystal clear, full color
- Interrupt moment appears
- Large, centered, deliberate
- Sound: ambient returns

The pause is where dread lives. "Something's happening."

---

### Tick Rate by Speed

```python
def get_tick_interval(speed: str) -> float:
    """
    Seconds between physics ticks.
    """
    if speed == '1x':
        return 5.0  # One tick per ~5 seconds (moment duration)
    elif speed == '2x':
        return 0.5  # Rapid ticks
    elif speed == '3x':
        return 0.0  # As fast as possible

    return 5.0
```

---

### Decay and Speed

Decay is time-based, not tick-based. Speed doesn't change total decay.

```python
def calculate_decay(elapsed_real_time: float) -> float:
    """
    Decay based on real time, not tick count.
    3x doesn't decay faster than 1x.
    """
    return DECAY_RATE * elapsed_real_time
```

At 3x, ticks are faster but decay rate per real-time stays constant. Otherwise 3x would decay everything to zero.

---

### Montage Generation

At 2x, system seeds atmospheric summary moments.

```python
def generate_montage_moments(context: SceneContext):
    """
    Generate brief atmospheric moments for journey feel.
    Called by handlers when speed is 2x.
    """
    montage_options = [
        "The road winds through the valley.",
        "Clouds gather on the horizon.",
        "The sun hangs low.",
        "Birdsong fades as evening approaches.",
    ]

    moment = create_moment(
        text=random.choice(montage_options),
        type='montage',
        weight=0.3,  # Low weight, background
        status='possible'
    )

    return moment
```

Not a separate system. Same handlers, context-aware output. The speed is in the prompt context.

---

### Player Input at Any Speed

```python
def on_player_starts_typing():
    """
    Player began typing. Auto-pause or slow down.
    """
    current = get_current_speed()

    if current in ['2x', '3x']:
        set_speed('1x')  # Or pause
        # Player can resume after input processed
```

- Player can type at any speed
- Typing auto-pauses (or auto-drops to 1x)
- Submit processes normally
- Player chooses to resume / change speed

---

### Canon vs Display

**Canon is canon regardless of display.**

```python
## At 3x, low-weight moments:
## - Actualize in graph ✓
## - Create THEN links ✓
## - Become history ✓
## - Display to player ✗ (filtered)

## Player can review history later
def get_skipped_moments(time_range: TimeRange) -> List[Moment]:
    """
    What happened while I was skipping?
    """
    return query("""
        MATCH (m:Moment)
        WHERE m.status = 'spoken'
          AND m.tick_spoken >= $start
          AND m.tick_spoken <= $end
        RETURN m
        ORDER BY m.tick_spoken
    """, start=time_range.start, end=time_range.end)
```

Speed changes rendering, not reality.

---

### Journey Conversations (2x Pattern)

At 2x, travel compresses but conversation persists.

```
The road stretches. (montage, muted)
"I never told you about my brother." (dialogue, vivid)
The sun sets. (montage, muted)
"What happened?" (dialogue, vivid)
You make camp. (montage, muted)
"The Normans." (dialogue, vivid)
```

Two things at once: travel and intimacy. Like film. A day passes in minutes, but the conversation is whole.

---

### Speed State

```python
@dataclass
class SpeedState:
    current: str  # '1x', '2x', '3x'
    paused: bool
    last_interrupt: Optional[Moment]
    time_at_speed: Dict[str, float]  # Track time spent at each speed

def set_speed(new_speed: str):
    state.current = new_speed
    physics.set_tick_interval(get_tick_interval(new_speed))
    display.set_filter(get_display_filter(new_speed))
```

---

### What Speed Controller Does NOT Do

- Change what happens (only what displays)
- Affect canon (history is complete at any speed)
- Change decay rate (time-based, not tick-based)
- Block physics (graph always runs)

---

### Invariants

1. **Speed doesn't change content:** Same events at any speed
2. **Canon is complete:** All moments recorded regardless of display
3. **Time-based decay:** 3x doesn't decay faster
4. **Interrupts break through:** Critical moments always shown

---

*"The player is a viewer with a remote. Fast-forward through the boring parts."*

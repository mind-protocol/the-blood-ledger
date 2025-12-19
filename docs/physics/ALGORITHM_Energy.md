# Graph — Algorithm: Energy Mechanics

```
STATUS: DRAFT
CREATED: 2024-12-18
UPDATED: 2024-12-18
REPLACES: ALGORITHM_Energy_Flow.md (partial)
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Energy.md (you are here)
                - M1-M6: Strength Mechanics
                - M11: Flip Detection
                - M12: Canon Holder
                - M13: Agent Dispatch
ALGORITHMS:     ./ALGORITHM_Physics.md, ./ALGORITHM_Handlers.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
IMPL:           ../../engine/physics/energy.py
```

---

## Core Principles

**1. Links don't create energy. They route it.**

Energy conservation within the narrative layer. Characters are external pumps. Decay and actualization are sinks.

**2. Strength is authored initially, evolved structurally.**

Narrator sets initial link strength. Events modify it. Time decays it. No magic numbers — earned through play.

**3. Energy IS proximity.**

We don't compute "proximity" as a separate concept. Energy levels encode relevance. High energy = close to attention. Low energy = far from attention. Physics handles it.

**4. Physical gating is link attributes, not functions.**

`presence_required: bool` on ATTACHED_TO links. `AT` links for character location. Graph queries, not code.

---

# NODE TYPES

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

## Weight vs Energy

| Property | Weight | Energy |
|----------|--------|--------|
| **What** | Importance over time | Current activation |
| **Timescale** | Slow (hours/days) | Fast (ticks/seconds) |
| **Changes by** | Events, reinforcement, decay | Flow, injection, spending |
| **Range** | 0.01 - 1.0 | 0.01 - 10.0 (chars) / 5.0 (narr/moment) |
| **Analogy** | Long-term memory strength | Working memory activation |

## Why Both Matter

| State | Meaning |
|-------|---------|
| High weight, low energy | Important but dormant — "the oath exists but no one's thinking about it" |
| Low weight, high energy | Active but trivial — "we're discussing lunch" |
| High weight, high energy | Important AND active — "the betrayal surfaces NOW" |
| Low weight, low energy | Forgotten — will decay away |

## Surfacing / Relevance

```python
def salience(node):
    """How much should this surface right now?"""
    return node.weight * node.energy
```

High salience = surfaces, dominates attention, triggers events.

## Character Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `weight` | float | Importance to story (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 10.0) |
| `state` | enum | `awake`, `sleeping`, `unconscious`, `dead` |

## Narrative Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `type` | enum | `fact`, `belief`, `oath`, `debt`, `secret`, `rumor`, `relationship` |
| `weight` | float | Importance to story (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 5.0) |
| `visibility` | enum | `public`, `secret`, `known_to_few` |
| `deadline` | datetime? | For debts, oaths with time pressure |
| `conditions` | string[]? | For oaths — when does it activate? |

## Moment Attributes

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

# LINK TYPES

## Character Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **BELIEVES** | Char → Narr | Char pumps into Narr | Core relationship |
| **ORIGINATED** | Char → Narr | Char pumps harder (*1.5) | Authorship |
| **AT** | Char → Place | NO flow | Spatial |
| **CARRIES** | Char → Thing | NO flow | Possession |

## Narrative Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **ABOUT** | Narr → Char/Place/Thing | Reverse: subject pulls | Focal point |
| **CONTRADICTS** | Narr ↔ Narr | Bidirectional exchange | Conflict |
| **SUPPORTS** | Narr ↔ Narr | Equilibrating | Alliance |
| **ELABORATES** | Narr → Narr | Parent → child | Detail |
| **SUBSUMES** | Narr → Narr | Specific → general | Aggregation |
| **SUPERSEDES** | Narr → Narr | Draining (old → new) | Replacement |

## Moment Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **CAN_SPEAK** | Char → Moment | Char energy → weight | Who speaks |
| **ATTACHED_TO** | Moment → Any | Target energy → weight | Relevance |
| **CAN_LEAD_TO** | Moment → Moment | On traversal | Conversation |
| **THEN** | Moment → Moment | NO (historical) | Canon chain |

## Link Properties

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

# NARRATIVE TYPES

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

# LINK STRENGTH

## Principle

**Strength = authored initially, evolved structurally**

Narrator sets initial value. Six mechanics modify it over time. No magic — earned through play.

## Timescales (No Circularity)

| Property | Changes | Timescale |
|----------|---------|-----------|
| **Energy** | Every tick | Seconds |
| **Weight** | Derived from energy | Seconds |
| **Strength** | On events | Minutes to hours |

Strength is slow. Energy is fast. Strength is effectively constant within a tick cycle.

## Default Initial Strength

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

## Base Functions

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

# STRENGTH MECHANICS (Six Categories)

## Principle

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

## M1: ACTIVATION

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

## M2: EVIDENCE

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

## M3: ASSOCIATION

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

## M4: SOURCE

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

## M5: COMMITMENT

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

## M6: INTENSITY

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

## Summary

| Mechanic | Trigger | Effect Range |
|----------|---------|--------------|
| Activation | Link referenced/used | +0.03 to +0.08 |
| Evidence+ | Confirming event witnessed | +0.05 to +0.15 |
| Evidence- | Contradicting event witnessed | -0.05 to -0.30 |
| Association | Co-occurrence | +0.03, create if none |
| Source | New belief from someone | initial × credibility |
| Commitment | Acted on belief | +0.05 to +0.15 |
| Intensity | High-stress context | ×1.0 to ×2.0 multiplier |

## Agents That Modify Strength

| Agent | Mechanics Applied |
|-------|-------------------|
| **Canon Holder** | Activation, Evidence, Association |
| **Input Parser** | Activation |
| **Handler** | Source (when character learns), Evidence (deciding response) |
| **Action Processor** | Commitment |
| **All** | Intensity (wraps other mechanics) |

## Emergent Scenarios

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

## Why Conservation

| Approach | Problem |
|----------|---------|
| Links create energy | System explodes. Requires arbitrary dampening. |
| No conservation | Tuning nightmare. Magic numbers everywhere. |
| **Conservation + external pumps** | Predictable. "Heat" emerges from structure. |

"Arguments heat both sides" because both sides have believers pumping — not because contradiction creates energy from nothing.

---

## The Energy Equation

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

# ENERGY SOURCES

## S1: Character Pumping

Characters inject energy into narratives they care about.

**Core insight:** We don't compute "proximity" separately. Energy levels ARE proximity. Characters pump into narratives proportional to belief strength. Energy flow through the graph handles the rest.

### Character Energy Sources

| Source | Amount | When |
|--------|--------|------|
| **Baseline** | 0.01 per tick | Always (existing) |
| **Being talked about** | from ABOUT links | Others discuss you |
| **Player focus** | 1.0 / targets | Direct attention |
| **Arrival** | 0.5 one-time | Enter scene |

### Character State

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

### Pump Calculation

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

### Dead Characters

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

## S2: Player Focus Injection

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

## S3: World Events

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

## S4: Tension Pressure (Structural)

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

# ENERGY SINKS

## K1: Decay

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

## K2: Actualization

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

# ENERGY TRANSFER (Links)

## Principle

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

## T1: CONTRADICTS (Bidirectional)

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

## T2: SUPPORTS (Bidirectional)

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

## T3: ELABORATES (Unidirectional, Parent → Child)

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

## T4: SUBSUMES (Unidirectional, Specific → General)

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

## T5: SUPERSEDES (Draining)

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

## T6: ABOUT (Focal Point Pulls)

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

## T7: CAN_LEAD_TO (Moment to Moment)

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

## T8: CAN_SPEAK (Character to Moment)

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

## T9: ATTACHED_TO (Moment from Sources)

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

## Actualization (Energy Spent)

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

## Moment Decay by Status

| Status | Decay Rate | Notes |
|--------|------------|-------|
| `possible` | 0.02 | Normal — unused possibilities fade |
| `active` | 0.01 | Slower — something is happening |
| `spoken` | 0.03 | Faster — it's done, recedes into past |
| `dormant` | 0.005 | Very slow — waiting to reactivate |
| `decayed` | N/A | No energy, no decay |

---

# MOMENT ENERGY & WEIGHT

Moments have both weight (importance) and energy (activation). Both matter for surfacing.

## Surfacing Logic

```python
def salience(moment):
    """How much should this moment surface right now?"""
    return moment.weight * moment.energy

def should_surface(moment):
    """Does this moment cross the threshold?"""
    return salience(moment) >= SURFACE_THRESHOLD
```

## Energy Flow Into Moments

Moments receive energy from:
- Characters via CAN_SPEAK links (T8)
- Narratives/Characters via ATTACHED_TO links (T9)
- Other moments via CAN_LEAD_TO links (T7)
- Player focus injection

Energy flows OUT via:
- CAN_LEAD_TO links to other moments
- Actualization (partial spend)
- Decay

## Weight Evolution

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

## Example

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

# FULL TICK CYCLE

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

# PHYSICAL GATING

Physical presence is not "proximity." It's a binary gate.

## How It Works

**Link attribute:** `presence_required: bool` on ATTACHED_TO

**Location:** `AT` link from Character to Place

## Gating Queries

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

## What This Replaces

| Old Concept | New Reality |
|-------------|-------------|
| `physical_proximity(a, b)` | Graph query on AT links |
| `narrative_proximity(n, focus)` | **Deleted** — energy IS proximity |
| `compute_focus(scene)` | **Deleted** — energy injection handles it |
| `can_actualize(moment)` | Query presence_required attachments |
| `can_interact(a, b)` | Query AT links |

## Example

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

# PARAMETERS

## Transfer Factors

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

## Moment Decay Rates

| Status | Decay Rate | Notes |
|--------|------------|-------|
| `possible` | 0.02 | Unused possibilities fade |
| `active` | 0.01 | Something is happening |
| `spoken` | 0.03 | Done, recedes into past |
| `dormant` | 0.005 | Waiting to reactivate |

## Actualization

| Parameter | Value | Notes |
|-----------|-------|-------|
| ACTUALIZATION_COST | 0.6 | Partial drain on flip |

## Source Rates

| Source | Rate | Notes |
|--------|------|-------|
| Character pumping | 0.10 * energy | Per tick, distributed by belief strength |
| Origination bonus | *1.5 | Authors care more |
| Secret holding bonus | *1.2 | Secrets held tighter |
| Player focus | 1.0 | Per input, split across targets |
| Arrival boost | 0.5 | Character enters scene |
| News injection | 0.3 | Information arrives |
| Discovery injection | 0.5 | Something revealed |

## Sink Rates

| Sink | Rate | Notes |
|------|------|-------|
| Energy decay (narratives) | 0.02 | Per tick |
| Energy decay (core types) | 0.005 | Oaths, blood, debts (*0.25) |
| Energy decay (characters) | 0.02 | Per tick |
| Weight decay | 0.001 | Only after WEIGHT_DECAY_DELAY ticks without reinforcement |
| Actualization cost | 0.6 * energy | When moment flips |

## Weight Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| WEIGHT_DECAY_DELAY | 100 | Ticks before weight starts decaying |
| WEIGHT_DECAY_RATE | 0.001 | Very slow |
| MIN_WEIGHT | 0.01 | Never fully zero |
| SURFACE_THRESHOLD | 0.3 | salience (weight * energy) needed to surface |

## Floors & Ceilings

| Parameter | Value | Why |
|-----------|-------|-----|
| MIN_ENERGY | 0.01 | Never fully zero — can always revive |
| MIN_WEIGHT | 0.01 | Never fully zero — can always matter again |
| MAX_CHARACTER_ENERGY | 10.0 | Prevent runaway accumulation |
| MAX_NARRATIVE_ENERGY | 5.0 | Keep narratives bounded |
| MAX_MOMENT_ENERGY | 5.0 | Keep moments bounded |

---

# EMERGENT BEHAVIORS

## "Arguments Heat Both Sides"

Not because CONTRADICTS creates energy.

Because:
1. Aldric pumps into "Edmund betrayed us"
2. Edmund pumps into "I was right"
3. CONTRADICTS transfers between them (zero-sum)
4. Both stay hot because both have pumps

If Edmund dies → no pump → his side cools → argument fades.

## "Approach Creates Tension"

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

## "Forgotten Things Bite Back"

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

## "The World Feels Alive"

Not because NPCs have complex AI.

Because:
1. Every character pumps into what they believe
2. Energy flows through narrative network
3. Tensions emerge from structure
4. Moments surface based on weight
5. The system has its own metabolism

No one decided "now is dramatic." The structure created drama.

## "Thinking About Someone Far Away"

Not proximity calculation. Energy injection.

1. Player says "I wonder what Aldric is doing"
2. Input parser detects reference to char_aldric
3. Energy injected into char_aldric
4. Aldric's energy flows to narratives about him (ABOUT reverse)
5. Those narratives surface (high energy = high weight moments)
6. Player "thinks about" Aldric — his stories come to mind

Aldric isn't "closer." His narratives are hotter. Same effect, no proximity concept.

---

# M11: FLIP DETECTION

Physics tick detects when moments cross the salience threshold. Canon Holder records them.

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

## Detection Query

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

## Processing Multiple Ready Moments

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

## Speaker Resolution

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

# M12: CANON HOLDER

**Everything is moments. Canon Holder is the gatekeeper.**

Canon Holder records what becomes real. It doesn't decide what happens — physics and handlers do that. Canon Holder makes it permanent.

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

## Canon Holder Responsibilities

| Responsibility | What It Does |
|----------------|--------------|
| **Record** | Flip moment `active` → `spoken` |
| **Link** | Create THEN link to previous moment |
| **Time** | Advance game time based on moment duration |
| **Trigger** | Process actions (travel, take, etc.) |
| **Strength** | Apply strength mechanics (Activation, Evidence, etc.) |
| **Notify** | Push to frontend |

## Recording Function

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

## Strength Mechanics on Record

Canon Holder triggers three of the six strength mechanics:

### M1: Activation

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

### M2: Evidence

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

### M3: Association

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

## Time Passage

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

## Action Processing

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

## THEN Links

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

## Frontend Notification

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

## True Mutex (Rare)

True mutex = logically impossible, not just dramatic.

### Same Character, Incompatible Actions

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

### What's Incompatible

| Action A | Action B | Mutex? |
|----------|----------|--------|
| travel east | travel west | Yes |
| attack X | attack X | No (both attack) |
| take sword | take sword | No (drama: struggle) |
| speak | speak | No (both speak) |

Most "conflicts" are actually drama to embrace.

## What Canon Holder Does NOT Do

- Generate content (that's Handlers)
- Compute energy flow (that's Physics tick)
- Block drama (simultaneous actions are fine)
- Store tension (tension is computed)
- Decide what should happen (that's Physics + Handlers)

Canon Holder only: record, link, trigger, notify.

---

# M13: AGENT DISPATCH

Four agents at three levels.

## The Agents

| Agent | Level | Responsibility | Timing |
|-------|-------|----------------|--------|
| **Runner** | World | Pressure, time, events, breaks | Tick-based |
| **Narrator** | Scene | Architecture, backstory, consequences | On demand |
| **Citizen** | Character | Dialogue, thoughts, freeform | Parallel async |
| **Canon Holder** | Record | Makes moments canon, THEN links | On flip |

## Runner (World)

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

## Narrator (Scene)

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

## Citizen (Character)

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

## Main Loop

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

# WHAT WE DON'T DO

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

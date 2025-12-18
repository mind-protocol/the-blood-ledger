# PHASE 5 — Natural Dynamics

```
CREATED: 2024-12-17
STATUS: Design
PHASE: 5 of 5
REQUIRES: Phase 4
AVERAGE RATING: 9.3/10
```

Dialogue that breathes. Moments that evolve. Characters that react to names, to contradictions, to time.

---

## Patterns

### P5.1 Char-to-Char Required Words

CAN_LEAD_TO links between NPC moments use `require_words`. When Aldric says something containing "sword", Mildred's response about swords can trigger.

**Mechanism:**

```python
def on_moment_spoken(moment, speaker_id):
    words_in_moment = extract_significant_words(moment.text)

    # Find moments from OTHER characters that require these words
    triggered = query("""
        MATCH (other:Character)-[:CAN_SPEAK]->(response:Moment)
        MATCH (response)-[r:CAN_LEAD_TO]-(spoken:Moment {id: $spoken_id})
        WHERE other.id != $speaker_id
        AND ANY(word IN r.require_words WHERE word IN $words)
        AND response.status = 'possible'
        RETURN response, r.weight_transfer
    """, spoken_id=moment.id, speaker_id=speaker_id, words=words_in_moment)

    for t in triggered:
        t.response.weight += t.weight_transfer
```

**Player Experience:** Conversations between NPCs feel natural. Mildred doesn't respond to everything Aldric says — only when he mentions something she cares about. The player watches real dialogue unfold, not scripted ping-pong.

**Rating: 9/10** — This makes group scenes feel alive. NPCs actually listen to each other.

---

### P5.2 Autonomous Announcement

Some moments have `trigger: autonomous` with conditions. When conditions met + weight threshold, character just speaks without prompt.

**Schema:**

```yaml
Moment:
  id: moment_aldric_leadership_challenge
  text: "Enough! We need to decide who leads this band."
  type: dialogue
  status: possible
  weight: 0.4

CAN_LEAD_TO:
  from: (any active tension moment)
  to: moment_aldric_leadership_challenge
  trigger: autonomous
  require_tension_above: 0.7  # Leadership tension must be high
  require_chars_present: 3    # Needs audience
```

**Mechanism:**

```python
def check_autonomous_triggers():
    candidates = query("""
        MATCH (m:Moment {status: 'possible'})
        MATCH (m)<-[r:CAN_LEAD_TO {trigger: 'autonomous'}]-()
        WHERE m.weight > 0.6
        RETURN m, r
    """)

    for c in candidates:
        if check_autonomous_conditions(c.r):
            activate_moment(c.m)
            # No player action caused this
            mark_as_autonomous(c.m)
```

**Player Experience:** The player is mid-conversation about supplies when Aldric suddenly stands and demands leadership be settled. It wasn't in response to anything the player said — Aldric had been building to this. Characters have their own agendas that erupt at dramatic moments.

**Rating: 10/10** — This is what makes characters feel like people, not chatbots waiting for input.

---

### P5.3 Moment Rumination (Derivative Moments)

When context changes (location, time, presence), moments can spawn derivatives. "I love this city" → "I miss this city" when away.

**Mechanism:**

```python
def on_context_change(char_id, change_type, old_value, new_value):
    # Find moments affected by this change
    affected = query("""
        MATCH (c:Character {id: $char_id})-[:CAN_SPEAK]->(m:Moment)
        MATCH (m)-[:ATTACHED_TO]->(target)
        WHERE target.id = $old_value
        RETURN m
    """, char_id=char_id, old_value=old_value)

    for m in affected:
        # Generate derivative
        derivative = generate_derivative(m, change_type, new_value)
        if derivative:
            create_moment(
                text=derivative.text,
                type="thought",
                status="possible",
                weight=m.weight * 0.5
            )
            link_as_derivative(m, derivative)

def generate_derivative(moment, change_type, context):
    """Transform moment based on context change."""

    transforms = {
        ('location_left', 'love'): lambda t: t.replace("I love", "I miss"),
        ('location_left', 'hate'): lambda t: t.replace("I hate", "I'm glad to leave"),
        ('time_passed', 'will'): lambda t: t.replace("I will", "I should have"),
        ('char_died', 'love'): lambda t: f"I remember when {extract_subject(t)}...",
    }

    sentiment = detect_sentiment(moment.text)
    key = (change_type, sentiment)

    if key in transforms:
        return Moment(text=transforms[key](moment.text))

    return None
```

**Player Experience:** Aldric said "I love this city" in York. Days later, on the road, he mutters "I miss that city." The player didn't ask about York. But Aldric *remembers*, and his feelings evolved with distance. Characters aren't static — their relationship to their memories changes with context.

**Rating: 8/10** — Beautiful when it works. Risks feeling mechanical if transforms are too predictable. Needs variety.

---

### P5.4 Context Modifiers

When referencing old moments, prepend temporal/contextual modifiers. "Last week I told you..." or "Remember at the crossing when..."

**Mechanism:**

```python
def add_context_modifier(moment, current_tick, current_location):
    # Find what this moment references
    source = query("""
        MATCH (m:Moment {id: $id})-[:REFERENCES]->(original:Moment)
        RETURN original, original.tick_spoken, original.location
    """, id=moment.id)

    if not source:
        return moment.text

    # Calculate temporal distance
    tick_diff = current_tick - source.tick_spoken

    if tick_diff < 12:  # Same day (assuming 5min ticks)
        time_phrase = "Earlier"
    elif tick_diff < 288:  # Within week
        time_phrase = "A few days ago"
    elif tick_diff < 1440:  # Within month
        time_phrase = "Weeks ago"
    else:
        time_phrase = "Long ago"

    # Add location if different
    if source.location != current_location:
        location_name = get_place_name(source.location)
        modifier = f"{time_phrase}, at {location_name},"
    else:
        modifier = f"{time_phrase},"

    # Prepend
    return f"{modifier} {moment.text}"
```

**Example Outputs:**
- "Last week, at the crossing, you promised me."
- "Earlier, you said you'd help."
- "Long ago, at York, I told you about my brother."

**Player Experience:** When Aldric references a past conversation, he actually references it properly. The player thinks "oh right, that conversation!" Callbacks feel earned, not cheap. The world has temporal depth — things happened *before*, in *places*.

**Rating: 9/10** — Huge immersion boost. Makes continuity tangible. Player feels their history matters.

---

### P5.5 Moment Evolution (Reinforcement)

When similar moments are spoken repeatedly, they intensify. "I dislike him" → "I hate him" → "I want him dead."

**Schema:**

```yaml
Moment:
  id: moment_aldric_dislike_edmund
  text: "I dislike Edmund."
  intensity: 1
  evolution_chain: [moment_aldric_hate_edmund, moment_aldric_kill_edmund]
  reinforcement_count: 0

Moment:
  id: moment_aldric_hate_edmund
  text: "I hate Edmund."
  intensity: 2

Moment:
  id: moment_aldric_kill_edmund
  text: "I want Edmund dead."
  intensity: 3
```

**Mechanism:**

```python
def on_moment_spoken(moment):
    # Check if this reinforces a theme
    similar = query("""
        MATCH (m:Moment {status: 'spoken'})
        WHERE m.id != $id
        AND vector_similarity(m.embedding, $emb) > 0.85
        AND m.speaker = $speaker
        RETURN count(m) AS reinforcement
    """, id=moment.id, emb=moment.embedding, speaker=moment.speaker)

    if similar.reinforcement >= 2:
        # Evolve to next intensity
        if moment.evolution_chain:
            next_id = moment.evolution_chain[0]
            next_moment = get_moment(next_id)
            next_moment.weight += 0.4  # Make evolution more likely
            next_moment.evolution_chain = moment.evolution_chain[1:]

def check_evolution_threshold(char_id, theme_embedding):
    """If same theme expressed 3+ times, auto-evolve."""
    count = query("""
        MATCH (c:Character {id: $char_id})-[:CAN_SPEAK]->(m:Moment {status: 'spoken'})
        WHERE vector_similarity(m.embedding, $emb) > 0.8
        RETURN count(m)
    """, char_id=char_id, emb=theme_embedding)

    if count >= 3:
        trigger_evolution(char_id, theme_embedding)
```

**Player Experience:** First time Aldric mentions Edmund, it's mild irritation. Player notices but doesn't think much of it. Second time, "I really don't like that man." Third time, "I *hate* Edmund." The player watches a character radicalize through their own conversations. They could have intervened. They didn't. Now Aldric wants blood.

**Rating: 10/10** — This is character development happening *in play*, not in cutscenes. Player agency creates consequences they didn't directly choose.

---

### P5.6 Name Activation

When a character's name is mentioned in any moment, that character's attention spikes. Their moments get weight boost. They might react.

**Mechanism:**

```python
def on_moment_spoken(moment):
    # Extract names mentioned
    names = extract_character_names(moment.text)

    for name in names:
        char = get_character_by_name(name)
        if not char:
            continue

        # Is this character present?
        if is_present(char.id):
            # Strong activation - they heard their name
            boost_character_moments(char.id, 0.4)
            queue_potential_reaction(char.id, moment, "heard_name")
        else:
            # Weak activation - talked about behind their back
            # Creates "ears burning" moment for later
            create_gossip_about(char.id, moment)

def boost_character_moments(char_id, amount):
    update("""
        MATCH (c:Character {id: $id})-[:CAN_SPEAK]->(m:Moment {status: 'possible'})
        SET m.weight = m.weight + $amount
    """, id=char_id, amount=amount)
```

**Player Experience:** Player is talking to Mildred about Aldric (who is present but silent). They say "Aldric never listens." Aldric, who was staring at the fire, suddenly looks up. A moment surfaces: "I'm standing right here, you know." The player mentioned someone and that person *noticed*. Names have power.

**Rating: 9/10** — Creates "oh shit" moments. Player learns that talking about people when they're present has consequences. Social dynamics become real.

---

### P5.7 Heavy Modifier Reaction

When a major graph change occurs (strong contradiction, belief destroyed, relationship broken), affected characters generate immediate reaction moments.

**Mechanism:**

```python
def on_belief_contradicted(char_id, old_belief, new_evidence):
    """Character learns something that contradicts deeply held belief."""

    contradiction_strength = compute_contradiction(old_belief, new_evidence)

    if contradiction_strength > 0.8:  # Major contradiction
        # Generate crisis moment
        context = get_citizen_context(char_id)

        prompt = f"""
        {build_citizen_prompt(context)}

        You just learned: {new_evidence.content}

        This contradicts what you believed: {old_belief.content}
        Contradiction strength: {contradiction_strength}

        Generate an immediate reaction. This is a crisis of belief.
        """

        reaction = await llm(prompt, structured=Moment)

        m = create_moment(
            text=reaction.text,
            type="dialogue",
            status="active",  # Immediate, not possible
            weight=1.0,       # Maximum weight
            tone="shocked"
        )

        # This interrupts normal flow
        mark_as_interrupt(m)

def on_relationship_destroyed(char_a, char_b, event):
    """Bond broken (betrayal, death, etc)."""

    # Both characters react
    for char_id in [char_a, char_b]:
        if not is_alive(char_id):
            continue

        m = create_moment(
            text=generate_relationship_break_reaction(char_id, event),
            type="dialogue",
            status="active",
            weight=1.0,
            tone="devastated"
        )
```

**Example Triggers:**
- Aldric learns his brother was a traitor → immediate crisis moment
- Player betrays Mildred → she reacts NOW, not next time weight flips
- Someone dies → present characters react immediately

**Player Experience:** The player reveals a terrible truth. There's no "Aldric considers this" — Aldric's face changes, he steps back, and words come out that aren't in any prepared tree. The game's emotional beats feel REAL because the reaction is immediate and proportional. Big moments get big reactions.

**Rating: 10/10** — This is the difference between "game reacted to my choice" and "I just broke Aldric." Emotional impact requires immediate response.

---

## Rating Summary

| ID | Pattern | Rating | Why It Matters |
|----|---------|--------|----------------|
| P5.1 | Char-to-Char Words | 9/10 | Group conversations flow |
| P5.2 | Autonomous Announcement | 10/10 | Characters have agendas |
| P5.3 | Moment Rumination | 8/10 | Feelings evolve with context |
| P5.4 | Context Modifiers | 9/10 | History is tangible |
| P5.5 | Moment Evolution | 10/10 | Characters radicalize through play |
| P5.6 | Name Activation | 9/10 | Names have power |
| P5.7 | Heavy Modifier Reaction | 10/10 | Big moments get big reactions |

**Phase 5 Average: 9.3/10**

---

## Implementation Checklist

- [ ] Char-to-char required words matching
- [ ] Autonomous announcement triggers
- [ ] Moment rumination (derivative spawning)
- [ ] Context modifiers for old references
- [ ] Moment evolution chains (reinforcement)
- [ ] Name activation and attention
- [ ] Heavy modifier crisis reactions

---

*"Phase 5 makes characters human. They build, they break, they remember patterns. The graph is psychology."*

# PHASE 3 — Citizen Autonomy

```
CREATED: 2024-12-17
STATUS: Design
PHASE: 3 of 5
REQUIRES: Phase 2
AVERAGE RATING: 9.0/10
```

Characters as bounded agents. Background thought. Parallel generation.

---

## Patterns

### P3.1 Activated Cluster as System Prompt
Character's identity = query of connected nodes (beliefs, relationships, wounds).

**Player Experience:** Aldric feels consistent across every conversation because he IS consistent — his identity comes from his actual history in the graph. Different from other characters because his graph IS different. No two playthroughs produce identical Aldric.

**Rating: 9/10** — Characters feel authored but unique. The graph IS their soul.

---

### P3.2 Peripheral Vision
Citizen "sees" linked nodes: present characters, nearby things, active tensions.

**Player Experience:** Aldric mentions the sword on the table without you pointing it out. He notices Mildred is tense. Characters are aware of their environment. The player isn't the only one with eyes.

**Rating: 8/10** — Makes characters feel present in the scene, not just responding to player.

---

### P3.3 Background Thought Generation
Citizens generate potential moments asynchronously. Questions. Desires. Observations.

**Player Experience:** There's always something to discover. Characters have been thinking while you weren't looking. Return to Aldric after an hour and he has new things to say. The possibility space refills itself.

**Rating: 9/10** — Solves content exhaustion. The well never runs dry.

---

### P3.4 Citizen Responds to Freeform
Character LLM handles dialogue directed at them. Narrator discharged.

**Player Experience:** Ask Aldric something weird and HE answers, in HIS voice. Not generic narrator prose. Each character has their own response style. Talk to Mildred about the same thing — different answer, different voice.

**Rating: 10/10** — Characters become individuals, not narrator puppets. This is personhood.

---

### P3.5 Drive-Based Exploration
Curiosity → questions about unknowns.
Anxiety → worry about threats.
Greed → focus on opportunities.

**Player Experience:** Why does Mildred keep asking about the treasure? Because she's greedy. Why does Aldric worry about the Normans? Because he's afraid. Characters have REASONS for what they talk about. Personality expressed through attention.

**Rating: 9/10** — Characters feel motivated, not random. Player learns to read them.

---

### P3.6 Tempo Adaptation
Generation rate adapts to player pace. Fast player → more content. Slow → less.

**Player Experience:** Speed readers get a torrent. Careful readers get space. The game matches YOUR rhythm. Never overwhelmed, never starved. Feels personalized even though it's mechanical.

**Rating: 8/10** — Quality of life. Invisible when working, annoying when wrong.

---

## Behaviors

### B3.1 Characters Think
Idle moments → Aldric's thoughts surface. "He stares at the fire."

**Player Experience:** You catch Aldric in an unguarded moment. His inner life is visible. He wasn't waiting for you to talk — he was somewhere else. Characters have depths you only glimpse.

**Rating: 9/10** — Creates intimacy. Player feels like they're seeing the real person.

---

### B3.2 Proactive Dialogue
Character has something to say → initiates without player prompt.

**Player Experience:** "I need to tell you something." Aldric has agency. He's not a vending machine. Sometimes HE drives the conversation. Player learns to listen, not just extract.

**Rating: 10/10** — The marker of a real character. They have needs.

---

### B3.3 Different Voices
Each character's moments feel different. Voice from their cluster.

**Player Experience:** You can tell who's speaking without checking the name. Mildred's sharpness, Aldric's melancholy, Godwin's bluster. Characters aren't interchangeable. Casting matters.

**Rating: 9/10** — Makes the party feel like individuals. Essential for ensemble stories.

---

### B3.4 Drive Manifestation
Greedy character → moments about treasure, deals, value surface more.

**Player Experience:** "Of course Mildred cares about that." Player builds mental model of each character. Predictions work. Characters are READABLE. This makes relationships possible.

**Rating: 9/10** — Legible psychology. Player can learn and anticipate.

---

### B3.5 Never Overwhelm
Content generation pauses if player hasn't consumed recent moments.

**Player Experience:** You're never drowning. If you're slow, the game slows. If you're fast, it speeds up. Pressure without panic. The game is patient.

**Rating: 8/10** — Accessibility feature. Crucial for broader audience.

---

### B3.6 Instant Freeform Response
Player addresses character → that citizen responds (not narrator).

**Player Experience:** "What do YOU think, Aldric?" And Aldric answers. Not a narrator summary of what Aldric might think. HIS words. Direct address works.

**Rating: 10/10** — Makes conversation feel like conversation. Characters are real participants.

---

## Mechanisms

### M3.1 Activated Cluster Query

```python
def get_citizen_context(char_id):
    return query("""
        MATCH (c:Character {id: $id})
        OPTIONAL MATCH (c)-[b:BELIEVES]->(n:Narrative)
        OPTIONAL MATCH (c)-[:AT]->(loc:Place)
        OPTIONAL MATCH (c)-[:KNOWS]->(other:Character)
        OPTIONAL MATCH (t:Tension)-[:INVOLVES]->(c)
        OPTIONAL MATCH (c)-[:CARRIES]->(thing:Thing)
        RETURN c,
               collect(DISTINCT n) AS beliefs,
               loc,
               collect(DISTINCT other) AS relationships,
               collect(DISTINCT t) AS tensions,
               collect(DISTINCT thing) AS possessions
    """, id=char_id)
```

---

### M3.2 System Prompt Builder

```python
def build_citizen_prompt(context):
    return f"""
    You are {context.character.name}.

    ## Who You Are
    {context.character.backstory}

    ## What You Believe
    {format_beliefs(context.beliefs)}

    ## Your Relationships
    {format_relationships(context.relationships)}

    ## What Weighs On You
    {format_tensions(context.tensions)}

    ## Your Voice
    Tone: {context.character.voice.tone}
    Style: {context.character.voice.style}
    """
```

---

### M3.3 Background Thought Generation

```python
async def citizen_think(char_id):
    context = get_citizen_context(char_id)
    peripheral = get_peripheral_vision(char_id)
    drives = get_character_drives(char_id)

    prompt = f"""
    {build_citizen_prompt(context)}

    ## What You Notice
    {format_peripheral(peripheral)}

    ## What Drives You Now
    Strongest drive: {drives.strongest.name} ({drives.strongest.intensity})

    Generate 1-2 thoughts or potential things you might say.
    These may or may not surface depending on circumstances.
    """

    thoughts = await llm(prompt, structured=MomentList)

    for thought in thoughts:
        m = create_moment(
            text=thought.text,
            type="thought" if thought.internal else "dialogue",
            status="possible",
            weight=thought.salience * drives.strongest.intensity
        )
        create_link(char_id, "CAN_SPEAK", m.id, weight=1.0)
        attach(m, char_id, presence_required=True, persistent=True)
```

---

### M3.4 Citizen Freeform Response

```python
async def citizen_respond(char_id, player_input):
    context = get_citizen_context(char_id)
    recent = get_recent_moments_with(char_id, limit=10)

    prompt = f"""
    {build_citizen_prompt(context)}

    ## Recent Exchange
    {format_moments(recent)}

    ## Player Says
    "{player_input}"

    How do you respond?
    """

    response = await llm(prompt, structured=MomentList)

    for m in response.moments:
        inject_moment(m, speaker=char_id, status='active')

    return response
```

---

### M3.5 Drive System

```python
@dataclass
class Drive:
    name: str  # curiosity, anxiety, greed, loyalty, vengeance
    intensity: float
    focus: str  # What specifically

def get_character_drives(char_id):
    # Computed from tensions, beliefs, personality
    tensions = get_character_tensions(char_id)
    personality = get_character_personality(char_id)

    drives = []

    if any(t.type == 'secret' for t in tensions):
        drives.append(Drive('anxiety', 0.7, 'the secret'))

    if personality.curious and has_unknowns_nearby(char_id):
        drives.append(Drive('curiosity', 0.6, 'the stranger'))

    # etc

    return sorted(drives, key=lambda d: d.intensity, reverse=True)
```

---

### M3.6 Tempo Controller

```python
class TempoController:
    def __init__(self):
        self.player_last_input = now()
        self.moments_pending = 0
        self.moments_shown = 0

    def player_reading_speed(self):
        elapsed = time_since(self.player_last_input)
        if elapsed < 1:
            return 999  # Active
        return self.moments_shown / elapsed

    def should_generate_more(self):
        if self.moments_pending > 3:
            return False
        if self.player_reading_speed() < 0.3:
            return False  # Slow reader
        return True

    def generation_interval(self):
        speed = self.player_reading_speed()
        if speed > 1.0:
            return 2.0  # Fast reader, generate often
        elif speed > 0.5:
            return 5.0
        else:
            return 10.0  # Slow, barely generate
```

---

### M3.7 Parallel Main Loop

```python
async def main_loop():
    tempo = TempoController()

    while game_running:
        tasks = [
            runner_tick(),
            surface_ready_moments(),
        ]

        if tempo.should_generate_more():
            for char_id in get_present_characters():
                tasks.append(citizen_think(char_id))

        await asyncio.gather(*tasks)
        await asyncio.sleep(tempo.generation_interval())
```

---

## Rating Summary

| ID | Pattern/Behavior | Rating | Why It Matters |
|----|------------------|--------|----------------|
| P3.1 | Activated Cluster | 9/10 | Graph IS their soul |
| P3.2 | Peripheral Vision | 8/10 | Characters see the scene |
| P3.3 | Background Thought | 9/10 | Content well never dry |
| P3.4 | Citizen Freeform Response | 10/10 | Characters are individuals |
| P3.5 | Drive-Based Exploration | 9/10 | Motivated attention |
| P3.6 | Tempo Adaptation | 8/10 | Matches player rhythm |
| B3.1 | Characters Think | 9/10 | Intimacy through glimpses |
| B3.2 | Proactive Dialogue | 10/10 | Characters have needs |
| B3.3 | Different Voices | 9/10 | Ensemble feels individual |
| B3.4 | Drive Manifestation | 9/10 | Readable psychology |
| B3.5 | Never Overwhelm | 8/10 | Accessibility |
| B3.6 | Instant Freeform | 10/10 | Direct address works |

**Phase 3 Average: 9.0/10**

---

## Implementation Checklist

- [ ] Activated cluster query
- [ ] System prompt builder
- [ ] Background thought generation
- [ ] Citizen freeform response
- [ ] Drive system
- [ ] Tempo controller
- [ ] Parallel async loop

---

*"Phase 3 makes characters live. They think, they care, they speak when it matters to them."*

# PHASE 2 — Energy & Emergence

```
CREATED: 2024-12-17
STATUS: Design
PHASE: 2 of 5
REQUIRES: Phase 1
AVERAGE RATING: 8.8/10
```

Semantic input. Energy flow. Moments surface from pressure, not authorship.

---

## Patterns

### P2.1 Semantic Boost
Free input → embed → boost similar moments → may flip without LLM.

**Player Experience:** Type "tell me about your family" and Aldric responds — but no loading. The right moment was already there, waiting. Player feels heard. The game understood what they meant, not just what they typed.

**Rating: 10/10** — This is the magic. Free input without LLM latency. Players will think you're cheating.

---

### P2.2 Embedding Proximity Energy
Linked moments with similar embeddings share energy. Activation spreads.

**Player Experience:** Ask about Aldric's brother, and suddenly moments about his father, his childhood, his wounds are all closer to surfacing. One topic opens a constellation. Conversations feel associative, not mechanical.

**Rating: 8/10** — Creates natural conversation flow. Invisible but powerful.

---

### P2.3 Tension-to-Moment Energy
High tension pressure → boost weight of attached moments.

**Player Experience:** The leadership question has been brewing. Suddenly everyone's talking about it — not because the player asked, but because the tension is *ripe*. Story emerges from pressure, not prompts.

**Rating: 9/10** — This is emergent narrative. The game has dramatic timing without scripting.

---

### P2.4 Wait Trigger
`trigger: wait, wait_ticks: 3` → auto-fires if player silent.

**Player Experience:** Player stares at the screen, uncertain. Aldric shifts. "You're quiet." The silence wasn't empty — it was noticed. NPCs don't freeze when player freezes. The world continues.

**Rating: 9/10** — Transforms awkward pauses into dramatic moments. Player feels present.

---

### P2.5 Bidirectional Links
`bidirectional: true` → conversation can flow both ways.

**Player Experience:** Ask about the sword, get answer. Later, circle back to the sword from a different angle. Conversations aren't one-way streets. Player can revisit topics naturally.

**Rating: 7/10** — Important for natural dialogue but invisible when working. Frustrating when missing.

---

### P2.6 Weight Transfer
Traversing link transfers weight: `target.weight += link.weight_transfer`.

**Player Experience:** Deep into a conversation, the really important stuff starts surfacing. The player earned it by engaging. Investment pays off. Surface-level players get surface-level content.

**Rating: 8/10** — Rewards engagement. Creates conversation "depth" feeling.

---

## Behaviors

### B2.1 Freeform Without LLM
Player types → semantic match → moment surfaces. No narrator call.

**Player Experience:** "Wait, there's no loading? How did it know what I meant?" Players will test this, trying to break it. When they can't, trust skyrockets. The game feels *responsive* to meaning, not just keywords.

**Rating: 10/10** — This is the impossible-feeling feature. Core to the entire pitch.

---

### B2.2 Characters Initiate
Weight accumulates → threshold crossed → character speaks unprompted.

**Player Experience:** You're not driving. Aldric is a person with things to say. He might bring something up before you ask. NPCs feel like they have interior lives. Player becomes a participant, not an interrogator.

**Rating: 10/10** — The difference between "NPC" and "character." This is where they become alive.

---

### B2.3 Tension Bleeds Into Dialogue
Aldric's guilt tension high → guilt-related moments surface more.

**Player Experience:** "Why does Aldric keep talking about his brother?" Because he can't stop thinking about it. The player sees psychology, not code. Characters feel haunted by their issues, not just defined by them.

**Rating: 9/10** — Creates character consistency without repetition. They're shaped by their pressures.

---

### B2.4 Associative Chains
Activating one moment boosts semantically similar neighbors.

**Player Experience:** One topic leads to another, naturally. "Speaking of swords... my brother had a sword..." The player doesn't see the associative jump as mechanical. It feels like memory working.

**Rating: 8/10** — Makes conversations feel organic. Invisible infrastructure.

---

### B2.5 Silence Has Weight
Player quiet → wait triggers fire → NPCs fill the silence.

**Player Experience:** The player can LISTEN. They don't have to constantly perform. Sit back, and characters will talk to each other, think out loud, fill the space. Player becomes audience sometimes, and that's okay.

**Rating: 9/10** — Respects different play styles. Some players want to watch, not just drive.

---

## Mechanisms

### M2.1 Semantic Freeform Handler

```python
def handle_free_input(player_id, text):
    input_emb = embed(text)

    matches = query("""
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        RETURN m, vector_similarity(m.embedding, $emb) AS score
        ORDER BY score DESC LIMIT 5
    """, emb=input_emb)

    for match in matches:
        if match.score > 0.65:
            match.m.weight += match.score * 0.5

    flips = check_for_flips()
    if flips:
        return flips

    # Only if nothing matches
    return queue_narrator_generation(text)
```

---

### M2.2 Embedding Proximity Propagation

```python
def propagate_embedding_energy(moment):
    neighbors = query("""
        MATCH (m:Moment {id: $id})-[:CAN_LEAD_TO]-(neighbor:Moment)
        RETURN neighbor, vector_similarity(m.embedding, neighbor.embedding) AS sim
    """, id=moment.id)

    for n in neighbors:
        if n.sim > 0.7:
            n.neighbor.weight += moment.weight * n.sim * 0.1
```

---

### M2.3 Tension Energy Flow

```python
def tension_to_moments(tension):
    moments = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(t:Tension {id: $id})
        RETURN m
    """, id=tension.id)

    for m in moments:
        m.weight += tension.pressure * 0.2
```

---

### M2.4 Wait Trigger Check

```python
def check_wait_triggers(tick):
    links = query("""
        MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO]->(next)
        WHERE r.trigger = 'wait'
        AND (tick - m.tick_spoken) >= r.wait_ticks
        RETURN m, r, next
    """)

    for link in links:
        activate(link.next)
        create_then_link(link.m, link.next, player_caused=False)
```

---

### M2.5 Flip Detection

```python
def check_for_flips():
    flipped = query("""
        MATCH (m:Moment)
        WHERE m.status = 'possible' AND m.weight > 0.8
        RETURN m ORDER BY m.weight DESC
    """)

    for m in flipped:
        m.status = 'active'

    return flipped
```

---

## Rating Summary

| ID | Pattern/Behavior | Rating | Why It Matters |
|----|------------------|--------|----------------|
| P2.1 | Semantic Boost | 10/10 | Free input without latency |
| P2.2 | Embedding Proximity | 8/10 | Natural conversation flow |
| P2.3 | Tension-to-Moment Energy | 9/10 | Emergent dramatic timing |
| P2.4 | Wait Trigger | 9/10 | Silence has weight |
| P2.5 | Bidirectional Links | 7/10 | Natural but invisible |
| P2.6 | Weight Transfer | 8/10 | Rewards engagement |
| B2.1 | Freeform Without LLM | 10/10 | The magic trick |
| B2.2 | Characters Initiate | 10/10 | NPCs become characters |
| B2.3 | Tension Bleeds Into Dialogue | 9/10 | Psychology through attention |
| B2.4 | Associative Chains | 8/10 | Organic conversation |
| B2.5 | Silence Has Weight | 9/10 | Respects different play styles |

**Phase 2 Average: 8.8/10**

---

## Implementation Checklist

- [ ] Semantic embedding on moments
- [ ] Freeform → semantic boost → flip
- [ ] Tension pressure → moment weight
- [ ] Wait trigger auto-fire
- [ ] Embedding proximity propagation
- [ ] Flip threshold detection

---

*"Phase 2 makes the graph breathe. Moments surface because they're ready, not because the LLM said so."*

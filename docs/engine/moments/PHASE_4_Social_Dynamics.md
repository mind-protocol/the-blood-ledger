# PHASE 4 — Social Dynamics

```
CREATED: 2024-12-17
STATUS: Design
PHASE: 4 of 5
REQUIRES: Phase 3
AVERAGE RATING: 9.3/10
```

Multi-agent interaction. Gossip. Reactions. Character-to-character conversation.

---

## Patterns

### P4.1 Witness Reaction
Character witnesses moment → generates reaction moment (mechanical + LLM).

**Player Experience:** Say something cutting to Aldric. Mildred, watching, smirks. She'll remember this. Witnesses aren't invisible. Actions have audience. The player realizes: this isn't private.

**Rating: 10/10** — Social dynamics become real. Third parties matter. Every scene is observed.

---

### P4.2 Character-to-Character Dialogue
NPCs talk to each other, not just player. Player can observe or intervene.

**Player Experience:** Aldric and Mildred argue. You can jump in or watch it unfold. You're not the center of every conversation. The party has relationships independent of you. Feels like travelling with real people.

**Rating: 10/10** — The "Mass Effect party banter" everyone wanted but better. You can engage or not.

---

### P4.3 Gossip Propagation
Character learns something → may tell others (creates BELIEVES links).

**Player Experience:** You told Aldric a secret. A week later, Mildred knows. How? Aldric told her. Information spreads. Secrets are hard to keep. The world has memory and mouth.

**Rating: 9/10** — Creates consequence for sharing. Secrets become gameplay.

---

### P4.4 Private vs Public
Moments attached to subset of present characters = private conversation.

**Player Experience:** Alone with Aldric, he confesses something. Mildred arrives — the moment vanishes. Some things are only said in private. Player learns to create intimacy by controlling presence.

**Rating: 9/10** — Makes party composition matter. Creates reason to split up.

---

### P4.5 Group Dynamics
Multiple characters present → dynamics emerge. Alliances. Tensions. Cross-talk.

**Player Experience:** Three people around the fire, and suddenly it's complicated. Aldric says something, Mildred bristles, Godwin tries to smooth it over. Group scenes have GROUP energy.

**Rating: 9/10** — Ensemble storytelling. Rare in games. Feels like a real party.

---

### P4.6 Narrative-Driven Energy
When narrative becomes active → all attached moments get energy boost.

**Player Experience:** The betrayal comes to light, and suddenly everyone's talking about trust, about loyalty, about what happened. The story focuses. Everything aligns. Dramatic convergence.

**Rating: 8/10** — Creates thematic coherence. Story beats feel like story beats.

---

### P4.7 Party Memory
Companions remember what happened when together. Shared moments.

**Player Experience:** Return to the crossing with Aldric. "This is where we first met." He remembers because he WAS there. Companions share your history. It's YOUR history together.

**Rating: 10/10** — Relationships built on shared experience. This is bonding.

---

## Behaviors

### B4.1 Aldric Reacts to Mildred
Mildred says something → Aldric's reaction moment surfaces.

**Player Experience:** "Did you see Aldric's face when Mildred said that?" The player notices inter-character tension. NPCs have opinions about each other. Drama without player involvement.

**Rating: 9/10** — Creates passive drama. Player becomes observer of relationships.

---

### B4.2 Overhearing
Player talks to Aldric → Mildred (present) hears → affects her beliefs.

**Player Experience:** You confide in Aldric, forgetting Mildred is there. Later, she knows. You didn't tell her — she overheard. Presence has consequences. The player learns to check who's listening.

**Rating: 10/10** — Classic dramatic mechanic. Creates paranoia and care.

---

### B4.3 Gossip Spreads
Mildred learns secret → later, alone with Godwin → may tell him.

**Player Experience:** "How does he KNOW?" Information has legs. You can't control it once it's out. The player learns to be careful. Secrets are currency, and currency circulates.

**Rating: 9/10** — Makes information warfare possible. Adds strategy layer.

---

### B4.4 Private Confession
Alone with Aldric → private moments surface. Others present → they don't.

**Player Experience:** "He only tells me things when we're alone." Intimacy is earned through privacy. The player actively manages party composition for conversations.

**Rating: 9/10** — Creates gameplay around relationships. Party management matters.

---

### B4.5 NPCs Argue
Two characters with conflicting beliefs → argument moments surface.

**Player Experience:** You haven't done anything, but Aldric and Mildred are at each other's throats. Their beef is THEIR beef. You can mediate or fan flames. Party cohesion is your responsibility... or not.

**Rating: 10/10** — Creates drama you can watch, join, or exploit. Ensemble story.

---

### B4.6 Story Beats Surface
Narrative "the betrayal" becomes focus → related moments boost.

**Player Experience:** Everything is about the betrayal now. Everyone's talking about it. The story is HAPPENING. Player feels swept up in events. Coherent drama, not random chatter.

**Rating: 8/10** — Makes story arcs feel like story arcs. Thematic focus.

---

### B4.7 "Remember When We..."
Return to location with companion → shared dormant moments reactivate.

**Player Experience:** "This is where we fought the wolves." "I remember." Shared history creates shared nostalgia. Companions feel like old friends. The relationship has weight.

**Rating: 10/10** — This is what makes companions matter. Shared memory is love.

---

## Mechanisms

### M4.1 Witness Reaction System

```python
def on_moment_spoken(moment, speaker_id):
    witnesses = get_present_characters()
    witnesses.remove(speaker_id)

    for witness_id in witnesses:
        # Mechanical check: do they care?
        relevance = compute_relevance(moment, witness_id)

        if relevance > 0.5:
            # Queue reaction generation
            queue_reaction(witness_id, moment, relevance)

async def generate_reaction(witness_id, moment, relevance):
    context = get_citizen_context(witness_id)

    prompt = f"""
    {build_citizen_prompt(context)}

    You just witnessed: "{moment.text}" (said by {moment.speaker})

    Your relevance to this: {relevance}

    Generate a brief reaction (or None if you'd stay silent).
    """

    reaction = await llm(prompt, structured=OptionalMoment)

    if reaction:
        m = create_moment(
            text=reaction.text,
            type="dialogue",
            status="possible",
            weight=relevance * 0.6
        )
        create_link(witness_id, "CAN_SPEAK", m.id, weight=1.0)
        create_link(moment.id, "CAN_LEAD_TO", m.id,
                   trigger="auto", weight_transfer=0.3)
```

---

### M4.2 Character-to-Character Conversation

```python
async def npc_to_npc_exchange(char_a, char_b):
    # Check if they have things to say to each other
    shared_tensions = get_shared_tensions(char_a, char_b)
    conflicting_beliefs = get_conflicting_beliefs(char_a, char_b)

    if not shared_tensions and not conflicting_beliefs:
        return

    # A speaks to B
    context_a = get_citizen_context(char_a)

    prompt = f"""
    {build_citizen_prompt(context_a)}

    You're with {char_b.name}.

    Shared concerns: {format_tensions(shared_tensions)}
    You disagree about: {format_conflicts(conflicting_beliefs)}

    Do you say something to them? (Not to the player, to them directly.)
    """

    utterance = await llm(prompt, structured=OptionalMoment)

    if utterance:
        m = create_moment(
            text=utterance.text,
            type="dialogue",
            status="possible",
            weight=0.6
        )
        create_link(char_a, "CAN_SPEAK", m.id, weight=1.0)
        # Attached to BOTH characters (private)
        attach(m, char_a, presence_required=True, persistent=True)
        attach(m, char_b, presence_required=True, persistent=True)
```

---

### M4.3 Gossip Mechanism

```python
async def check_gossip_opportunity(char_id):
    # What do they know that others don't?
    secrets = query("""
        MATCH (c:Character {id: $id})-[:BELIEVES]->(n:Narrative)
        WHERE n.type = 'secret' OR n.tone = 'scandalous'
        RETURN n
    """, id=char_id)

    if not secrets:
        return

    # Who's present that doesn't know?
    present = get_present_characters()
    present.remove(char_id)

    for other in present:
        for secret in secrets:
            knows = check_believes(other, secret.id)
            if not knows:
                # Would they tell?
                relationship = get_relationship(char_id, other)
                disposition = get_gossip_disposition(char_id)

                probability = disposition * relationship.trust

                if random() < probability:
                    queue_gossip(char_id, other, secret)

async def execute_gossip(teller_id, listener_id, narrative):
    context = get_citizen_context(teller_id)

    prompt = f"""
    {build_citizen_prompt(context)}

    You know something {listener_id.name} doesn't:
    {narrative.content}

    How do you tell them? (Whispered? Direct? Hinted?)
    """

    telling = await llm(prompt, structured=Moment)

    m = create_moment(
        text=telling.text,
        type="dialogue",
        status="possible",
        weight=0.7,
        tone="whispered"
    )

    # Private to these two
    attach(m, teller_id, presence_required=True, persistent=True)
    attach(m, listener_id, presence_required=True, persistent=True)

    # When spoken, listener gains belief
    m.on_spoken = lambda: create_belief(listener_id, narrative.id,
                                        source='told', from_whom=teller_id)
```

---

### M4.4 Private Conversation Gating

```python
def is_moment_visible(moment, viewer_id):
    attachments = get_attachments(moment, presence_required=True)

    char_attachments = [a for a in attachments if a.type == 'Character']

    if not char_attachments:
        return True  # Public

    # Private: viewer must be one of attached characters
    attached_ids = [a.target.id for a in char_attachments]

    return viewer_id in attached_ids
```

---

### M4.5 Group Dynamics Check

```python
async def check_group_dynamics():
    present = get_present_characters()

    if len(present) < 2:
        return

    # Find tension pairs
    for a, b in combinations(present, 2):
        tension = get_tension_between(a, b)

        if tension and tension.pressure > 0.7:
            # Conflict brewing
            await generate_conflict_moment(a, b, tension)

        alliance = get_alliance(a, b)
        if alliance and alliance.strength > 0.7:
            # Might back each other up
            await generate_support_moment(a, b, alliance)
```

---

### M4.6 Narrative Energy Boost

```python
def on_narrative_activated(narrative):
    """When a narrative becomes focus, boost all related moments."""

    moments = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(n:Narrative {id: $id})
        RETURN m
    """, id=narrative.id)

    for m in moments:
        m.weight += 0.3 * narrative.focus

    # Also boost semantically similar moments
    similar = query("""
        MATCH (m:Moment)
        WHERE vector_similarity(m.embedding, $emb) > 0.7
        RETURN m
    """, emb=narrative.embedding)

    for m in similar:
        m.weight += 0.1 * narrative.focus
```

---

### M4.7 Shared Party Memory

```python
def on_moment_spoken_with_party(moment, present_party):
    """All party members form memory of shared moment."""

    for member in present_party:
        attach(moment, member, presence_required=False, persistent=True)

    # Link to current location for "remember when we were here"
    location = get_current_location()
    attach(moment, location, presence_required=False, persistent=True)

def on_party_returns_to_location(location, party):
    """Reactivate shared moments."""

    shared = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(p:Place {id: $loc_id})
        WHERE m.status = 'dormant'
        AND ALL(member IN $party WHERE EXISTS((m)-[:ATTACHED_TO]->(member)))
        RETURN m
    """, loc_id=location.id, party=[p.id for p in party])

    for m in shared:
        m.status = 'possible'
        m.weight = 0.6  # "Remember when we..."
```

---

## Rating Summary

| ID | Pattern/Behavior | Rating | Why It Matters |
|----|------------------|--------|----------------|
| P4.1 | Witness Reaction | 10/10 | Actions have audience |
| P4.2 | Char-to-Char Dialogue | 10/10 | Party banter evolved |
| P4.3 | Gossip Propagation | 9/10 | Secrets become gameplay |
| P4.4 | Private vs Public | 9/10 | Party composition matters |
| P4.5 | Group Dynamics | 9/10 | Ensemble energy |
| P4.6 | Narrative-Driven Energy | 8/10 | Thematic coherence |
| P4.7 | Party Memory | 10/10 | Shared memory is love |
| B4.1 | Aldric Reacts to Mildred | 9/10 | Passive drama |
| B4.2 | Overhearing | 10/10 | Classic dramatic mechanic |
| B4.3 | Gossip Spreads | 9/10 | Information warfare |
| B4.4 | Private Confession | 9/10 | Intimacy gameplay |
| B4.5 | NPCs Argue | 10/10 | Drama you can watch/join |
| B4.6 | Story Beats Surface | 8/10 | Story arcs feel real |
| B4.7 | Remember When | 10/10 | Companions matter |

**Phase 4 Average: 9.3/10**

---

## Implementation Checklist

- [ ] Witness reaction system
- [ ] Character-to-character dialogue
- [ ] Gossip mechanism
- [ ] Private conversation gating
- [ ] Group dynamics detection
- [ ] Narrative energy boost
- [ ] Shared party memory

---

*"Phase 4 makes the group breathe. They see, they react, they remember together."*

# PHASE 1 — Core Graph Mechanics

```
CREATED: 2024-12-17
STATUS: Implementation Target
PHASE: 1 of 5
AVERAGE RATING: 8.8/10
```

Basic moment traversal. No LLM on hot path.

---

## Patterns

### P1.1 Click Traversal
Player clicks word → traverse CAN_LEAD_TO → instant response.

**Player Experience:** No loading spinner. No "thinking...". Click a word, see the response. The game feels like a physical book you're turning, not a chatbot you're waiting on. Instant gratification trains players to explore freely.

**Rating: 10/10** — Foundation of everything. If this isn't instant, nothing else matters.

---

### P1.2 Weight-Based Surfacing
Moments with weight > threshold become active. Below threshold → decay.

**Player Experience:** The conversation feels curated without feeling scripted. Important things surface. Irrelevant tangents fade. Player doesn't see the weight math — they just notice that NPCs "know what to talk about" and don't ramble about stale topics.

**Rating: 8/10** — Invisible when working. Essential but not directly felt.

---

### P1.3 Presence Gating
Moment visible only if all `presence_required: true` attachments satisfied.

**Player Experience:** Aldric won't talk about the sword unless the sword is actually there. Mildred won't gossip about Edmund unless Edmund is absent. Conversations feel context-aware. The player learns: "who's in the room matters."

**Rating: 9/10** — Creates "oh, I should bring the sword" and "let's talk privately" gameplay.

---

### P1.4 Persistent vs Ephemeral
`persistent: true` → survives scene change (dormant).
`persistent: false` → pruned when target leaves.

**Player Experience:** Leave a conversation, travel for days, return — pick up where you left off. "You never answered my question" hits different when it's been a week of game-time. Alternatively, small talk doesn't haunt you forever.

**Rating: 9/10** — This is what makes NPCs feel like they remember. Core to the "living world" promise.

---

### P1.5 Speaker Resolution
Multiple CAN_SPEAK links. Highest weight present character speaks.

**Player Experience:** Enter a room with three Saxons. *Someone* comments on your arrival — whoever has the most reason to. The player doesn't see dice rolling. They just see that whoever speaks makes sense. Groups feel organic.

**Rating: 8/10** — Subtle but prevents the "why did THAT guy talk?" problem.

---

### P1.6 Multiple Entry Points
`require_words: ["brother", "sword", "past"]` → all lead to same moment.

**Player Experience:** Player asks about the sword. Later, different player asks about Aldric's past. Both reach the same emotional confession. Multiple valid paths to meaningful moments. Replayability without feeling like you're unlocking a puzzle.

**Rating: 9/10** — Players feel clever for finding different routes. Reduces "did I miss something?" anxiety.

---

## Behaviors

### B1.1 Instant Click Response
Player clicks → moment surfaces in <50ms. No LLM.

**Player Experience:** The game respects your time. You can rapid-fire through a conversation or linger. Your rhythm, not the server's. Players describe this as "snappy" — highest compliment for UI.

**Rating: 10/10** — The feel of the game. Everything builds on this.

---

### B1.2 Dormant Reactivation
Return to place → dormant moments become possible again.

**Player Experience:** "I've been here before, but now..." The crossing where you met Aldric still echoes with that first conversation. Places have memory. Player feels like they're writing history, not consuming content.

**Rating: 9/10** — Makes the world feel lived-in. Places become meaningful.

---

### B1.3 Conversation Persistence
Leave mid-conversation → return → pick up where you left off.

**Player Experience:** "Wait, we weren't done talking about—" "I know." Aldric remembers. The player doesn't have to restart relationships. Companions feel like companions, not NPCs that reset.

**Rating: 10/10** — Single most important relationship feature. Without this, NPCs are goldfish.

---

### B1.4 Weight Decay
Unused possibilities fade. `weight *= 0.99` per tick.

**Player Experience:** Miss your chance to ask about the sword, and eventually Aldric stops thinking about it. Urgency without timers. The player learns: if something feels important, pursue it now.

**Rating: 7/10** — Important for pruning, but can frustrate if player wanted to return to a topic. Needs tuning.

---

### B1.5 Consumption
`consumes_origin: true` → origin becomes "spoken" after traversal.

**Player Experience:** Once you've asked about the brother, that exact question is "used up." But responses might open new questions. Conversations progress rather than loop. No "Skyrim guard" problem.

**Rating: 8/10** — Prevents repetition. Essential for immersion.

---

## Mechanisms

### M1.1 Current View Query

```python
def get_current_view(player_id):
    location = get_player_location(player_id)
    present_chars = get_characters_at(location)
    present_things = get_things_at(location)
    known_narratives = get_player_beliefs(player_id)

    live_moments = query("""
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active']
        WITH m, [(m)-[r:ATTACHED_TO WHERE r.presence_required]->(t) | t] AS required
        WHERE ALL(t IN required WHERE is_present(t))
        RETURN m ORDER BY m.weight DESC LIMIT 20
    """)

    transitions = query("""
        MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO]->(next)
        RETURN m.id, r.require_words, next.id
    """)

    return { location, present_chars, live_moments, transitions }
```

---

### M1.2 Click Handler

```python
def handle_click(moment_id, word):
    link = find_link(moment_id, word)
    if link.consumes_origin:
        mark_spoken(moment_id)
    create_then_link(moment_id, link.target, player_caused=True)
    activate(link.target)
    return link.target
```

---

### M1.3 Weight Update

```python
def update_weights(tick):
    for m in get_possible_moments():
        age = tick - m.tick_created
        m.weight *= (0.99 ** age)
        if m.weight < 0.1:
            m.status = 'decayed'
```

---

### M1.4 Scene Transition

```python
def on_player_leaves(location_id):
    # Prune non-persistent
    delete_moments(location_id, persistent=False)
    # Dormant persistent
    set_dormant(location_id, persistent=True)

def on_player_arrives(location_id):
    reactivate_dormant(location_id)
```

---

## Rating Summary

| ID | Pattern/Behavior | Rating | Why It Matters |
|----|------------------|--------|----------------|
| P1.1 | Click Traversal | 10/10 | No latency = everything feels responsive |
| P1.2 | Weight-Based Surfacing | 8/10 | Invisible curation |
| P1.3 | Presence Gating | 9/10 | Context-aware conversations |
| P1.4 | Persistent vs Ephemeral | 9/10 | NPCs remember |
| P1.5 | Speaker Resolution | 8/10 | Groups feel organic |
| P1.6 | Multiple Entry Points | 9/10 | No "missed content" anxiety |
| B1.1 | Instant Click Response | 10/10 | The game feel |
| B1.2 | Dormant Reactivation | 9/10 | Places have memory |
| B1.3 | Conversation Persistence | 10/10 | NPCs aren't goldfish |
| B1.4 | Weight Decay | 7/10 | Needed but can frustrate |
| B1.5 | Consumption | 8/10 | Prevents repetition |

**Phase 1 Average: 8.8/10**

---

## Implementation Checklist

- [ ] Moment node schema
- [ ] ATTACHED_TO, CAN_LEAD_TO, CAN_SPEAK, THEN links
- [ ] Click traversal (instant)
- [ ] Weight decay per tick
- [ ] Presence gating query
- [ ] Current view API
- [ ] Dormant/reactivate on location change

---

*"Phase 1 is the foundation. Everything else builds on instant graph traversal."*

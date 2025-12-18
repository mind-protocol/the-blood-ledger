# Vision — Validation: How We Know It's Working

```
CREATED: 2024-12-16
STATUS: Draft — validating with Nicolas
```

---

## The Core Question

> **Does it feel like real relationships with people who remember?**

Everything else is in service of this. If we build all the systems and the answer is "no," we've failed. If we cut corners but the answer is "yes," we've succeeded.

---

## Validation by Layer

### Layer 1: The Graph Holds State Correctly

**Test:** Can we represent Rolf's starter story?
- Characters exist with proper attributes
- Narratives exist with types, truth values, connections
- Beliefs link characters to narratives with correct states
- Relationships emerge from narrative queries

**Proof:** Query the graph for "what does Rolf believe about Edmund?" and get a meaningful answer.

**Status:** Not yet tested (graph not implemented)

---

### Layer 2: Weight/Energy Focuses Attention

**Test:** Given a graph with many narratives, do the right ones surface?
- Player beliefs should have high weight
- Connected narratives should gain weight
- Distant/disconnected narratives should have low weight
- Top-N selection should capture "what the story is about"

**Proof:** Generate context for a scene. Does it include the relevant narratives? Does it exclude the noise?

**Status:** Not yet tested (weight computation not implemented)

---

### Layer 3: Tension Detection Works

**Test:** Can the system identify narratives that must break?
- Contradictions with believers in proximity
- Oaths at moment of truth
- Debts beyond tolerance
- Secrets under exposure

**Proof:** Given Rolf and Edmund in the same room, with their contradicting beliefs about The Betrayal vs The Salvation, the system identifies this as unsustainable.

**Status:** Not yet tested (tension detection not implemented)

---

### Layer 4: Break Resolution Generates Good Events

**Test:** When a narrative breaks, does the LLM generate specific, traceable events?
- Event is specific to these characters, this place, this moment
- Event creates new narratives that connect to the graph
- Event feels like it couldn't have happened in a generic world
- Event is consistent with character beliefs and personalities

**Proof:** Run 10 break resolutions. Are they specific? Consistent? Interesting?

**Status:** Not yet tested (break resolution not implemented)

---

### Layer 5: Scene Rendering Is Engaging

**Test:** Are scenes short, vivid, grounded?
- Atmosphere in 2-3 lines (not walls of text)
- Voices speak relevant narratives (not random commentary)
- Choices emerge from situation (not generic options)
- Player feels present (not reading about someone else)

**Proof:** Show scenes to players. Do they lean forward or lean back?

**Status:** Not yet tested (scene rendering not implemented)

---

### Layer 6: Memory Creates "They Remembered" Moments

**Test:** Do past actions return organically?
- character references something player did
- Reference is organic (not forced callback)
- Player feels the world has memory

**Proof:** Play for several hours. Count "they remembered" moments. Do they feel earned?

**Status:** Not yet tested (requires full playthrough)

---

### Layer 7: Characters Feel Real

**Test:** Do players care about characters?
- Can player describe companion's personality?
- Does player consider character feelings when choosing?
- Does player feel betrayal/loyalty as emotional?

**Proof:** Post-session interviews. "Tell me about Aldric."

**Status:** Not yet tested (requires player testing)

---

## Proof of Concept Milestones

What we need to prove at each stage:

### POC 1: Graph + Static Scene
**Prove:** We can represent the Rolf story and render a scene from it.
- Build graph schema
- Load Rolf's starter graph
- Generate one scene
- Does it feel right?

### POC 2: Weight + Context Selection
**Prove:** The right narratives make it into context.
- Implement weight computation
- Select top-N for a scene
- Is the context relevant?

### POC 3: Tension + Breaks
**Prove:** Breaks emerge from configuration.
- Implement tension detection
- Trigger a break (Rolf + Edmund meet)
- Does the resolution make sense?

### POC 4: World Update + Time
**Prove:** The world moves without the player.
- Implement world update
- Advance time
- Do distant events happen?
- Does news propagate?

### POC 5: Full Loop + Playthrough
**Prove:** The game is playable and engaging.
- Full scene → action → world update → scene loop
- Multiple sessions
- Does it feel like real relationships?

---

## Red Flags to Watch

Signs we're going wrong:

| Red Flag | What It Means |
|----------|---------------|
| Scenes are long | We're overwriting. Cut. |
| All choices feel the same | Choices aren't emerging from configuration. |
| characters feel interchangeable | Character beliefs aren't differentiating them. |
| Player ignores the Ledger | The Ledger isn't feeling relevant. |
| "What am I supposed to do?" | Goals aren't clear or aren't motivating. |
| "This is random" | Events aren't traceable to graph state. |
| "I don't care" | Relationships aren't landing. Core failure. |

---

## The Ultimate Test

Play the game for 10 hours. Then answer:

1. **Can you predict your companion's behavior?** "If I sent Aldric to negotiate, what would happen?" — and be *right*.

2. **Can you ask deep questions and get answers?** Ask Aldric about his grandmother. About what he believes. About why he stayed. Does he have real answers?

3. **Do you know your enemies as people?** Not "Edmund is the bad guy" but "Edmund believes he saved the family while I was away, and he's not entirely wrong."

4. **Did someone remember something you did — and act on it?**

5. **Would you describe an character the way you'd describe a real person?** Not stats, not role — their personality, their history, their contradictions.

If yes to all five, the vision is working.

**The single sentence test:**
> "I'll send Aldric because I know he'll come back — [specific reasons from your relationship]."

If the player can fill in that bracket with real, accurate information they learned through play, we've succeeded.

---

*"If they don't remember, we failed. If they do — and it changes things — we succeeded."*

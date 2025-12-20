# Vision — Patterns: Why This Design

```
CREATED: 2024-12-16
STATUS: Draft — validating with Nicolas
```

---

## CHAIN

- `docs/design/PATTERNS_Vision.md` (this doc)
- `docs/design/BEHAVIORS_Vision.md` (player-facing experience outcomes)
- `docs/design/ALGORITHM_Vision.md` (system-level drivers for the vision)
- `docs/design/VALIDATION_Vision.md` (proof and validation criteria)
- `docs/design/IMPLEMENTATION_Vision.md` (doc architecture and ownership)
- `docs/design/HEALTH_Vision_Doc_Integrity.md` (documentation health checks)
- `docs/design/TEST_Vision.md` (vision validation checklist)
- `docs/design/SYNC_Vision.md` (current state and handoffs)

---

## THE PROBLEM

Most narrative games fake relational depth with stats or scripts, which creates
shallow bonds and brittle consequences that fail to feel personal or earned.

---

## THE PATTERN

Model relationships as a living narrative graph where tension accumulates,
breaks, and resolves into specific story events instead of pre-authored arcs.

---

## PRINCIPLES

The guiding principles for this vision are summarized below and expanded in
the "Design Principles" section that follows, so decisions stay consistent.

---

## DEPENDENCIES

This vision depends on a graph-backed narrative model, reliable tension
signals, and an LLM layer that can interpret contradictions into scenes.

---

## INSPIRATIONS

Primary reference points include Game of Thrones, Crusader Kings 3, and The
Expanse, chosen for political intimacy, emergent character arcs, and scale.

---

## SCOPE

In scope: relationship-driven narrative play, emergent tension resolution, and
text-first delivery with selective sensory reinforcement. Out of scope: MMO
scale, tactical combat depth, and pre-authored quest-line branching.

---

## GAPS / IDEAS / QUESTIONS

Open questions remain around graph pruning, character depth generation, and
long-session consistency; answers should land before production commitments.

---

## The Core Insight

**The game is a web of narratives under tension, not a simulation of characters making decisions.**

Traditional games simulate agents — characters with stats, schedules, dialogue trees. The player interacts with these agents. Relationships are numbers. Memory is scripted flags.

The Blood Ledger inverts this. We simulate *stories* — narratives that exist, connect, contradict, and break. Characters are how stories express themselves. When Aldric speaks, it's his beliefs speaking through him. When Edmund acts, it's the tension in his narratives resolving.

This matters because:
- **Relationships become real.** Not `trust: 0.65` but "the oath he swore at the fire, the doubt seeded when he heard Edmund's version, the loyalty tested three times."
- **Memory becomes structural.** The game remembers because the graph remembers. That promise in hour one is a narrative with weight — it will speak when relevant, break when pressured.
- **Consequences become inevitable.** Tension accumulates. What cannot hold, breaks. Not scripted — emergent.

---

## The One-Sentence Pitch

> **Build real relationships that matter — with people who remember you and act accordingly. Characters that feel real because they are real.**

Not "experience a branching story." Not "manage a medieval kingdom."

*Build relationships.* The game is about the web of people around you — who owes you, who you owe, who trusts you, who fears you, who loves you despite what you've done.

---

## The Player Fantasy

**Start small. Rise through people.**

You begin with almost nothing — yourself and one or two companions. No army, no castle, no title.

You end (if you survive, if you succeed) as a lord. But the path there isn't grinding stats or following quest markers. It's:
- The oath you swore to get your first ally
- The debt you called in at the crucial moment
- The betrayal you committed (or refused)
- The reputation you built, story by story
- The lord who raised you up because you proved useful
- The rival you crushed, or converted, or married

**The fantasy is political.** Power comes from people. Combat matters, but the sword that wins the war is often the one that *doesn't* swing — because the right word in the right ear made fighting unnecessary.

**The fantasy is personal.** These aren't faction standings. These are *people*. Aldric who's been with you since the beginning. Mildred who joined reluctantly and now believes in you. Edmund who wronged you (or did you wrong him?).

When you become lord, you remember every step. And so do they.

---

## Reference Points

What this feels like (not what it copies):

**Game of Thrones** — Political intrigue, betrayal as engine, long memory.

**Crusader Kings 3** — Emergent character stories, dynasties, consequences.

**The Expanse** — Found family, loyalty under pressure, intimacy inside scale.

**What we take:** relationships as the core system, emergence over authorship, intimacy within scale, compounding consequences.

**What we leave:** visual spectacle, mechanical bloat, predetermined arcs.

---

## Market Validation (Archived Summary)

CK3 community feedback aligns with the vision: players want people who remember,
uncertainty instead of omniscience, a living world with personal consequences,
companions who matter, and stories over numbers. The detailed quotes and
mapping table are archived in `docs/design/archive/SYNC_archive_2024-12.md`.

---

## Design Principles

When making decisions, we follow these:

### 1. Narratives Over Mechanics

If we can express something as a narrative in the graph, we don't need a separate system.

- Reputation? Narratives others believe about you.
- Relationships? Narratives connecting you to them.
- Resources? Narratives about who controls what.

The graph IS the game state. Additional systems are overhead.

### 2. Emergence Over Scripting

Events come from tension, not triggers.

- No "at hour 5, the bandit attack fires"
- No "if player chose X, then Y happens"
- Instead: "these narratives contradict under pressure → something breaks"

The LLM resolves *what* breaks into *what happens* — specifically for these characters, this place, this moment.

### 3. Uncertainty Over Omniscience

The player's beliefs may be wrong.

- narr_betrayal (truth: 0.3) — Player believes Edmund stole their inheritance
- narr_salvation (truth: 0.9) — Edmund believes he saved the family

The player starts righteous. They may discover they were the villain. Or they may never learn. Truth is in the graph; belief is what characters have.

### 4. Weight Over Equality

Not everything matters equally. Energy focuses attention.

- High-weight narratives speak louder, appear in context, break sooner
- Low-weight narratives fade to background, may never surface
- The player experiences a focused story, not a simulation of everything

This is how a vast world feels intimate — energy clusters around what matters to *this* player.

### 5. Specificity Over Genericity

Events are *this character, this place, this moment*.

- Not "a bandit attacks"
- But "Wulfric, who you spared at the bridge and who now serves Gospatric, recognizes you in the York market"

The LLM generates from the particular configuration. Events could not happen in a generic medieval world. They emerge from *this* graph.

---

## The Technical Bet

We believe LLM + Graph can deliver this because:

**Graphs capture narrative state.**
- Nodes: characters, places, things, narratives
- Links: beliefs, presence, connections
- Queryable: "who believes what about whom"

**LLMs interpret structural tension.**
- Given contradicting beliefs, proximity, pressure → determine what breaks
- Generate specific events from particular configurations
- Maintain voice consistency for characters

**Together they enable emergence that's impossible to author.**
- No team could write every possible combination
- But the graph holds the state, the LLM resolves the tension
- The result: stories that feel authored but weren't

---

## The Central Risk

**Engagement in a text-heavy medium.**

If the game feels like reading a novel with occasional multiple-choice prompts, we've failed. Text games can feel:
- Slow (walls of text)
- Passive (reading, not doing)
- Abstract (no grounding)
- Disconnected (choices don't feel impactful)

**How we counter this:**

| Risk | Counter |
|------|---------|
| Walls of text | Short, punchy scene rendering. Atmosphere in 2-3 lines. |
| Passive reading | The graph speaks — voices interrupt, react, comment. You're in dialogue with your own debts and oaths. |
| Abstract | Multiple views ground the experience: Map (where), Faces (who), Ledger (what's owed), Scene (now). |
| Disconnected choices | Consequences are visible. The Ledger shows what you've done. People reference it. |

**Additional engagement levers:**
- Image generation for key moments (faces, places, scenes)
- The Ledger as a physical artifact you're "keeping"
- Companion voices creating a sense of party, not solitude
- Pacing controlled by tension — slow builds, explosive releases

**The test:** Does the player lean forward or lean back? We need lean-forward engagement — "what happens if I..." not "what happens next."

---

## What Success Looks Like

**The Ultimate Test:**
> You know your companions and enemies well enough to *predict and rely on them*.

"I'll send Aldric to negotiate with Lord Gospatric because I know he'll come back — he swore an oath and he's never broken one, and his family had dealings with Gospatric's father before the conquest. He'll handle the formality well."

That's not a stat check. That's *knowing someone*.

"I won't send Mildred. She's been distant since the village, and I think she blames me. If she saw an opportunity to leave, she might take it."

That's relationship as *understanding*, not as number.

**Deep relationships mean:**
- You can ask Aldric about his grandmother, how he was raised, what he believes
- He has answers — consistent, specific, discoverable over time
- Those answers inform how he'll behave in situations you haven't seen yet
- You build a mental model of him that's *accurate*

**In a single session:**
- Player feels they made meaningful choices
- At least one moment of "oh shit, they remembered that"
- The world felt alive — something happened they didn't cause
- They want to come back

**Over a playthrough:**
- The rise to power feels earned, not granted
- Relationships feel specific, not generic
- The player can trace their path — "I became lord because..."
- Moments are memorable — "remember when Aldric..."
- **You can predict your companions' behavior and be right**

**As a game:**
- Players tell stories about their playthroughs
- Different players have genuinely different experiences
- The narrative graph produces emergent stories worth telling
- Text-primary doesn't feel like a limitation
- **Players describe characters like they're describing real people**

---

## Answered Questions

1. **Failure states.** Yes, you can die. Death is real. Future consideration: "restart from 10 days before" using DB state snapshots. For now, death is final.

2. **Session length.** Potentially infinite. Play as long as you want. No artificial session boundaries.

3. **Replayability.** Yes. Full vision: be anyone, anywhere, anytime. Current constraint: Norman England 1067, limited starting locations. But designed for replay — different character, different companions, different path.

4. **Multiplayer.** Not a consideration for V1.

5. **Scope control.** Ship V1 soon. Learn from reality, not speculation.

## Open Questions

Things still to resolve:

1. **Graph pruning.** How do distant/irrelevant narratives get archived?
2. **Character depth generation.** How do we create backstories rich enough to support deep questioning?
3. **Consistency at scale.** How do we maintain character consistency over many sessions?

---

*"What you do is written down. They remember."*

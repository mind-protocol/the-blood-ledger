# The Opening — Pattern

```
STATUS: DRAFT
CREATED: 2024-12-16
```

═══════════════════════════════════════════════════════════════════════════════
## CHAIN
═══════════════════════════════════════════════════════════════════════════════

```
THIS:        PATTERNS_Opening.md (you are here)
BEHAVIORS:   ./BEHAVIORS_Opening.md
ALGORITHM:   ./ALGORITHM_Opening.md
CONTENT:     ./CONTENT.md
VALIDATION:  ./VALIDATION_Opening.md
TEST:        ./TEST_Opening.md
SYNC:        ./SYNC_Opening.md
```

═══════════════════════════════════════════════════════════════════════════════
## THE PROBLEM
═══════════════════════════════════════════════════════════════════════════════

Most openings frontload exposition or mechanics, which forces the player into
passive intake before any relationship or personal stake can form.

═══════════════════════════════════════════════════════════════════════════════
## THE PATTERN
═══════════════════════════════════════════════════════════════════════════════

Use a fixed, authored sequence of open questions, delivered by a companion who
evaluates the player, so the player's answers become the dynamic content.

═══════════════════════════════════════════════════════════════════════════════
## PRINCIPLES
═══════════════════════════════════════════════════════════════════════════════

The opening must feel like a real conversation, preserve silence and rhythm,
and let the companion respond as a person rather than a service interface.

═══════════════════════════════════════════════════════════════════════════════
## DEPENDENCIES
═══════════════════════════════════════════════════════════════════════════════

Relies on the authored script in `CONTENT.md`, a consistent companion voice,
and the bootstrap flow that turns the script into playable scene beats.

═══════════════════════════════════════════════════════════════════════════════
## INSPIRATIONS
═══════════════════════════════════════════════════════════════════════════════

Campfire confession scenes, low-key travel conversations, and character-driven
openings from story RPGs informed the tone and pacing of this pattern.

═══════════════════════════════════════════════════════════════════════════════
## SCOPE
═══════════════════════════════════════════════════════════════════════════════

In scope: the opening conversation, its authored questions, and companion
responses that shape the initial relationship. Out of scope: combat tutorials,
system explanations, or dynamic question generation.

═══════════════════════════════════════════════════════════════════════════════
## THE INSIGHT
═══════════════════════════════════════════════════════════════════════════════

Most games open with exposition, tutorials, or action.

We open with a fire, a companion, and a conversation that *sees* the player.

**What we discovered:** A completely static set of questions — written in advance,
knowing nothing about the player — created the most engaging moment in the entire
design process. Not because the questions were dynamic. Because they were *real*.

The questions asked what games never ask:
- "What gets you out of your bedroll before dawn?"
- "What do you need?"
- "Do you want me to speak my mind, or hold my tongue?"

The player's answers are the dynamic part. The questions can be carved in stone.

═══════════════════════════════════════════════════════════════════════════════
## THE DESIGN PHILOSOPHY
═══════════════════════════════════════════════════════════════════════════════

### 1. The Companion Is Evaluating, Not Serving

Aldric hasn't decided about you yet. He's watching. Testing. This creates:
- Tension (will he stay?)
- Respect (he's not a yes-man)
- Reality (real people evaluate each other)

### 2. Questions Are Genuinely Open

No right answer. No expected path. No "choose your class."

| Don't ask | Ask |
|-----------|-----|
| "Are you a warrior or a scholar?" | "What gets you out of bed?" |
| "Choose your motivation: revenge/duty/gold" | "What happens when this is over?" |
| "How do you want companions to address you?" | "Do I speak my mind, or hold my tongue?" |

### 3. Silence Has Weight

Pauses. Waiting. The fire crackling. Not rushing to the next prompt.
The companion thinks about what you said before responding.

### 4. The Companion Finds Themselves In Your Answers

Aldric doesn't just extract information. He recognizes himself:
- "I've never fit either."
- "I've felt that rage."
- "I like that word. Nemesis."

This transforms interrogation into connection.

### 5. The Relationship Changes Based On Revelation

The conversation must *matter*. Something concrete shifts:
- "I'll translate for you" — an offer based on what was learned
- "Partners" — the dynamic crystallizes
- The companion's behavior going forward reflects what they heard

### 6. Activity Carries The Rhythm

Questions interspersed with:
- Poking the fire
- Walking in silence
- Crossing a stream
- Working a whetstone

Not a static interview. Life happening around the conversation.

═══════════════════════════════════════════════════════════════════════════════
## WHY THIS WORKS
═══════════════════════════════════════════════════════════════════════════════

**The player is being known.**

Not filling out a character sheet. Not choosing from menus. Being *asked* things
that matter by someone who seems to care about the answers.

This creates:
- Immediate attachment to the companion
- Investment in the relationship
- A sense that this game will *listen*
- All the psychological data we need, gathered naturally

**Static questions, dynamic answers.**

The LLM doesn't need to generate questions. It needs to:
1. Present the authored questions with life and timing
2. Listen to the answers
3. Build a player profile from what it heard
4. Have the companion reflect back authentically

This is cheaper, more reliable, and more powerful than dynamic generation.

═══════════════════════════════════════════════════════════════════════════════
## WHAT THIS PATTERN DOES NOT SOLVE
═══════════════════════════════════════════════════════════════════════════════

- Does not work if the questions are bad (everything depends on craft)
- Does not work if the companion feels robotic (performance matters)
- Does not guarantee the player engages (some will skip)
- Does not handle players who refuse to answer honestly

═══════════════════════════════════════════════════════════════════════════════
## GAPS / IDEAS / QUESTIONS
═══════════════════════════════════════════════════════════════════════════════

- [ ] How long should the opening be? Risk of fatigue vs depth of profiling
- [ ] What if player gives terse answers? Probe deeper or move on?
- [ ] Should companion have follow-up questions based on answer content?
- [ ] How to handle player who wants to skip to "the game"?
- IDEA: Companion could revisit themes from opening later ("You told me once...")
- IDEA: Player's opening answers could become clickable memories

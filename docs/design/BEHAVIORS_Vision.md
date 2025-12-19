# Vision — Behaviors: The Player Experience

```
CREATED: 2024-12-16
STATUS: Draft — validating with Nicolas
```

---

## CHAIN

```
PATTERNS:   ./PATTERNS_Vision.md
THIS:       BEHAVIORS_Vision.md (you are here)
ALGORITHM:  ./ALGORITHM_Vision.md
VALIDATION: ./VALIDATION_Vision.md
IMPLEMENTATION: ./IMPLEMENTATION_Vision.md
TEST:       ./TEST_Vision.md
SYNC:       ./SYNC_Vision.md
```

---

## BEHAVIORS

These behaviors define the lived experience: how scenes, choices, ledger
weight, and voices feel to the player without requiring them to understand
internal systems or hidden state.

---

## CHAIN

- `docs/design/PATTERNS_Vision.md` (design intent and scope)
- `docs/design/BEHAVIORS_Vision.md` (this doc)
- `docs/design/ALGORITHM_Vision.md` (systems that create the behaviors)
- `docs/design/VALIDATION_Vision.md` (proof points and success criteria)
- `docs/design/IMPLEMENTATION_Vision.md` (doc architecture and ownership)
- `docs/design/TEST_Vision.md` (validation checklist and coverage)
- `docs/design/SYNC_Vision.md` (current state, handoffs, open questions)

---

## BEHAVIORS

At the highest level, the player should feel present, weighted by obligation,
and guided by specific relationships rather than abstract stats or checklists.
These behaviors are detailed below as moment-to-moment actions, view-specific
experiences, and the arc that shapes a full playthrough.

---

## What the Player Does

### Moment to Moment

**In a scene**, the player:
- Reads a short, atmospheric description (2-3 lines of sensory grounding)
- Hears voices — their narratives speaking (debts, oaths, companions commenting)
- Sees choices emerge from the situation
- Chooses, or waits, or moves, or talks

**Between scenes**, the player can:
- Check the Map (where things are, where they could go)
- Check the Ledger (what's owed, what's sworn)
- Check the Faces (who they know, what they know about them)
- Check the Chronicle (what happened, as they believe it)
- Write in their journal (optional reflection)

**Over a session**, the player:
- Makes progress toward their goal (or gets pulled into something else)
- Builds or damages relationships through choices
- Learns things (news arrives, secrets emerge, truths surface)
- Experiences at least one "the world moved without me" moment

---

### The Feeling We're Creating

**Presence, not observation.**
You're not reading about someone else. You're *there*. The voices in your head are your voices — your debts, your oaths, your companions. The choices are your choices.

**Weight, not freedom.**
Total freedom feels meaningless. We create weight through consequences. You *can* break your oath, but Aldric will know. You *can* ignore the debt, but it will speak louder. Freedom exists within a web of obligations.

**Intimacy, not scale.**
The world is large, but your experience is intimate. You know a handful of people deeply. The drama is personal before it's political. Aldric's doubt matters more than the king's decree.

**Discovery, not revelation.**
Things aren't revealed to you in cutscenes. You discover them — by going places, talking to people, paying attention. The ferryman's secret isn't triggered by a quest stage. It's there, waiting, and you might find it. Or not.

---

## The Arc of a Playthrough

### Beginning: The Fire

You have nothing but:
- A name and a face (chosen)
- A drive (chosen: BLOOD, OATH, or SHADOW)
- One companion (chosen)
- A goal (established through opening conversation)

You're small. The world is large. You know almost nothing about what's happening beyond your campfire.

**The feeling:** Vulnerability. Possibility. "Where do I even start?"

### Early Game: The Road

You're traveling, surviving, building your first web.
- Meet people, form impressions, make small bargains
- Your companion reveals more of themselves
- The world reveals itself through news and encounters
- Your target (Edmund, or whoever) is a distant goal

**The feeling:** Discovery. Learning the rules. "Every person might matter."

### Mid Game: The Web Thickens

Your network grows. You're known.
- People reference your past actions
- Old choices return as consequences
- You're pulled into larger conflicts (the feud, the rebellion)
- Your goal comes closer (or further, or transforms)

**The feeling:** Momentum. Entanglement. "I'm in too deep now."

### Late Game: The Reckoning

Tensions break. Big things happen.
- Your accumulated debts and oaths come due
- Relationships are tested decisively
- You either rise or fall
- The story of your rise (or fall) becomes clear

**The feeling:** Culmination. "Everything I did led here."

### End: The Lord (or the Grave)

If you succeed:
- You have power (land, title, followers)
- But power came with costs
- Your ledger is full of what you did to get here
- Your companions have their own feelings about the journey

If you fail:
- The story ends, but it was still *your* story
- You understand why you failed (traceable to choices)
- The world continues without you

---

## Observable Behaviors by View

### The Scene

**What player sees:**
- Location name and type (THE ROAD TO YORK)
- Atmospheric text (2-3 lines: weather, light, sound, texture)
- Situation (what's happening, who's present)
- Voices (high-weight narratives speaking)
- Choices (what you can do)

**What player does:**
- Reads, absorbs, chooses
- Feels grounded in a specific place and moment
- Experiences their internal web reacting to the situation

**Success indicator:** Player pauses before choosing. Player references something a voice said.

### The Map

**What player sees:**
- Regions and places (fog of war for unknown)
- Their current location
- Known character locations (via narratives)
- Opportunities and dangers they've heard about

**What player does:**
- Plans routes
- Understands spatial relationships
- Decides where to go next

**Success indicator:** Player uses map to make strategic decisions about travel.

### The Chronicle

**What player sees:**
- Events as they believe them happened
- Chronological record of their journey
- Their own memories and what they've been told

**What player does:**
- Reviews what happened
- Notices their own beliefs (some may be wrong)
- Optionally writes their own reflections

**Success indicator:** Player consults chronicle to remember past events, references it when making decisions.

### The Ledger

**What player sees:**
- DEBTS (who owes them, who they owe)
- OATHS (what's been sworn)
- BLOOD (family, violence, the heavy stuff)

**What player does:**
- Tracks obligations
- Plans around what's owed
- Feels the weight of accumulated choices

**Success indicator:** Player consults ledger before making promises. Player feels tension when ledger entries conflict.

### The Faces

**What player sees:**
- Characters they know
- For each: all the narratives they believe about that person
- Computed disposition (trust/warmth) from narrative sum
- Known location, relationships

**What player does:**
- Reviews relationships
- Understands why they feel certain ways about people
- Plans interactions based on history

**Success indicator:** Player clicks a face before a major interaction. Player says "I trust them because..."

---

## Key Experience Moments

These are the moments we're designing toward:

- Clear goal and next step ("I know what I need to do")
- Familiar places that feel owned ("I know this place")
- The world remembers and moves without you
- Past oaths and debts speak in tense moments
- Companions become knowable, reliable people
- Climactic convergence ("Everything led here")

---

## INPUTS / OUTPUTS

**Inputs we rely on:** player choices (actions, dialogue, travel), current
graph state (narratives, debts, oaths), and view context (scene, map, ledger,
faces, chronicle). These inputs shape what appears and when it matters.

**Outputs we expect:** concrete narrative moments, updated ledger entries,
shifts in relationship understanding, and a clear next step the player can
take without feeling railroaded or lost.

---

## EDGE CASES

- Player idles or refuses to choose; the system should surface pressure or
time-based movement so the world still advances without breaking immersion.
- Sparse or conflicting narrative data; scenes should still ground the player
with clear, limited options rather than empty or confusing output.
- High churn between views; the UI should remain consistent so the player
does not lose the thread of the current moment.

---

## Core Drives (Archived Summary)

Primary motivational focus is Social Influence (deep relationships), Ownership
(the Ledger as a personal artifact), and Unpredictability (emergent outcomes),
with Epic Meaning, Development, Creativity, and Loss Avoidance supporting.
Detailed Octalysis mappings and behavioral targets are archived in
`docs/design/archive/SYNC_archive_2024-12.md`.

---

## ANTI-BEHAVIORS

### "Let me check my quest log."
If the player treats the Ledger as a checklist of objectives, we've failed. The Ledger is weight, not tasks.

### "What's the optimal choice?"
If the player is min-maxing relationship points, we've failed. Choices should feel like *choices*, not optimization problems.

### "I'll reload."
If the player instinctively wants to save-scum, we've failed. Consequences should feel like story, not punishment.

### "Skip skip skip."
If the player skips text to get to choices, we've failed. The text should be engaging, not obstacle.

### "Who is this again?"
If the player can't remember characters, we've failed. Characters should be memorable through their relationship to the player, not their name.

---

## Grounding (Summary)

Text is primary, supported by images for key scenes and faces. Audio and ambient sound are future enhancements, not V1 commitments.

---

## Engagement Levers (Archived Summary)

Engagement relies on the voices mechanic, brevity, stakes, rhythm, visual
grounding, and the Ledger as a tangible artifact. The detailed list is archived
in `docs/design/archive/SYNC_archive_2024-12.md`.

---

## Metrics (Archived Summary)

Experience measurement ideas (session length, return rate, choice deliberation,
view usage, player stories, memory moments, emotional responses) live in
`docs/design/archive/SYNC_archive_2024-12.md`.

---

## GAPS / IDEAS / QUESTIONS

- How much image support is needed before text-only sessions feel thin?
- What cadence of "world moves without you" moments keeps tension high but
does not overwhelm player agency or comprehension?
- Which view (map, ledger, faces, chronicle) needs the earliest prototype to
validate the experience before full system build-out?

---

*"You're not reading a story. You're in one. And everyone's watching what you do."*

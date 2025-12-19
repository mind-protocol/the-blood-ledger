# Scene View — Patterns: Design Philosophy

```
CREATED: 2024-12-16
STATUS: DESIGNING
LINKS_TO:
  - docs/design/BEHAVIORS_Vision.md (key experience moments)
  - docs/design/ALGORITHM_Vision.md (scene creation system)
```

---

## CHAIN

```
THIS:  PATTERNS_Scene.md
SYNC:  ./SYNC_Scene.md
IMPL:  frontend/components/scene/SceneView.tsx
```

---

## THE PROBLEM

The scene view must compress atmosphere, stakes, voices, and choices into a
single, readable frame without overwhelming the player or diluting the tension
that makes a moment feel playable instead of merely descriptive.

---

## THE PATTERN

Present a structured scene stack (header, banner, atmosphere, situation,
voices, actions) with short text blocks and weighted voice callouts, so the
player can absorb context quickly and act without wading through long prose.

---

## Purpose

The Scene view is THE game. Everything else supports it.

This is where the player:
- Perceives the world (atmosphere, location, who's present)
- Hears voices (their narratives speaking)
- Makes choices
- Talks to characters
- Experiences consequences

If Scene doesn't work, nothing else matters.

---

## The Core Question

**Does this feel engaging?**

Not "is it correct" or "does it follow the spec" — does it feel *good* to play?

The scene view is the test of the entire vision. If players lean forward, we're winning. If they skim to get to choices, we're losing.

---

## PRINCIPLES

### 1. Brevity Over Completeness

**Atmosphere in 2-3 lines. Not walls of text.**

```
Good:
Grey sky. Mud. The trees still drip from last night's rain.
A figure on the road ahead. Hood up. Walking stick.

Bad:
The sky stretches grey and heavy above you, the clouds pregnant with
the promise of more rain. The road beneath your feet is churned to
mud by countless travelers who have passed this way before, and the
trees that line the path still carry the remnants of last night's
downpour on their branches, droplets falling occasionally with soft
sounds. Ahead, you notice a figure approaching...
```

**Open question:** How do we ensure the LLM stays brief? System prompt? Post-processing? Examples?

### 2. Voices Create Presence

**Your narratives speak to you. You're not alone in your head.**

The "graph speaks" mechanic is our differentiator. In a scene, you don't just read description — you hear your debts, oaths, and companions commenting.

```
ALDRIC: "One man. Could be bait."
THE DEBT TO EDMUND: "Every day wasted is a day he breathes."
THE OATH: "This is not why we came north."
```

**Open questions:**
- How many voices per scene? Too many = noise, too few = lonely
- How do we select which narratives speak? (Weight? Relevance? Both?)
- Visual treatment of voices vs narration vs dialogue?

### 3. Choices Emerge, Not Menu

**Choices should feel like "what would I do?" not "which option?"**

Bad: Generic options that could appear anywhere
Good: Options specific to this situation, these characters, this moment

**Open question:** How do choices emerge?
- LLM generates from context?
- Template + fill?
- Always include certain types (talk, wait, leave)?

### 4. Characters Speak In Character

**characters have voice shaped by their beliefs.**

Aldric doesn't speak like Edmund doesn't speak like Mildred. Each has:
- Tone (quiet, sardonic, warm)
- Style (direct, circuitous, formal)
- Concerns (what they bring up, what they avoid)

**Open question:** How do we maintain character consistency?
- Character sheets in prompt?
- Few-shot examples?
- Fine-tuning someday?

### 5. Images Ground, Not Decorate

**Every scene has an image. The image does work.**

The image shows:
- Where you are (location, time of day, weather)
- The atmosphere (safe? tense? intimate?)
- Who's present (if relevant)

**Open questions:**
- How do we generate consistent style?
- How do we handle character faces in scene images?
- Latency — can we pre-generate? Or must be dynamic?

---

## SCOPE

This pattern governs the scene presentation layer (layout, pacing, voice
rendering, and action affordances) in the frontend; it does not define backend
scene generation, persistence, or any LLM prompting mechanics.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/components/scene/CenterStage.tsx` | Animated text pacing and reading-time flow |
| `frontend/components/scene/SceneBanner.tsx` | Scene imagery framing and fallbacks |
| `frontend/components/moment/` | Moment stream rendering used by the scene view |
| `frontend/hooks/useMoments.ts` | Moment data source for live scene updates |

---

## INSPIRATIONS

These patterns lean on tabletop session vignettes, succinct narrative cards in
story-driven games, and cinematic establishing shots that foreground mood
before action, keeping focus on tension and choice.

---

## What We Don't Know Yet

Being honest about uncertainties:

1. **The right amount of text.** How short is too short? Design doc says 2-3 lines atmosphere, but is that enough?

2. **Voice selection.** Which narratives speak? How many? This feels critical and underspecified.

3. **Choice generation.** How to make choices feel emergent, not canned.

4. **Image generation pipeline.** Style consistency, speed, prompt engineering.

5. **Conversation flow.** When you talk to someone, how does that work? Scene within scene? Modal? Different view?

6. **The feedback loop.** How does player action create new scene? What's the cycle?

---

## GAPS / IDEAS / QUESTIONS

We still need to validate the optimal voice count and clarify how choices are
generated and presented, especially when the scene is quiet or introspective.
The current UI supports these hooks, but the experience design is unsettled.

---

## What We're Testing

The fake-backend prototype should help us learn:

- [ ] Does brief text feel engaging or thin?
- [ ] Do voices create presence or confusion?
- [ ] Do choices feel meaningful?
- [ ] Does the image help or distract?
- [ ] What's the right pacing/rhythm?
- [ ] What's missing that we didn't anticipate?

---

## Reference: Scene Structure (from Design Doc)

Every scene contains:

| Element | Purpose |
|---------|---------|
| Header | Where you are (place name, type) |
| Atmosphere | 2-3 lines sensory grounding |
| Situation | What's happening, who's present |
| Voices | Your narratives speaking |
| Choices | What you can do |

Scene types:
- THE CAMP, THE ROAD, THE HALL, THE HOLD
- THE VILLAGE, THE FOREST, THE CHURCH
- THE BATTLEFIELD, THE TAVERN, THE GATE

---

## My Current Thinking

**The voices are the magic.** If we nail voices — your debts and oaths speaking to you in moments of decision — we have something genuinely new. If we don't, we're just another text game with pretty pictures.

**Brevity is harder than length.** Getting the LLM to write short, vivid prose consistently is a prompt engineering challenge.

**The image needs to feel essential.** Not decoration. The image should make you feel "I'm here" in a way text alone can't.

**Choices are the weak point.** How do we make them feel emergent? This might be where we iterate most.

---

## Links

- Vision: `docs/design/BEHAVIORS_Vision.md` (key experience moments)
- System: `docs/design/ALGORITHM_Vision.md` (scene creation in systems list)
- Design doc: `data/init/BLOOD_LEDGER_DESIGN_DOCUMENT.md` (scene examples)

---

*"The scene is where everything collapses into experience. Get this right."*

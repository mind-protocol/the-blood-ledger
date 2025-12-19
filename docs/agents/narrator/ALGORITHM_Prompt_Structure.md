# Narrator — Algorithm: Prompt Structure and Generation Flow

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical (consolidated)
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
PATTERNS:        ./PATTERNS_World_Building.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md
THIS:            ALGORITHM_Prompt_Structure.md
```

---

## Purpose

This document consolidates the narrator generation flow: prompt assembly, thread continuity, scene generation modes, rolling window pre-generation, and output schemas.

---

## The Orchestration

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                              │
│                                                                  │
│  1. Read world_injection.md (if exists)                           │
│  2. Read graph state                                              │
│  3. Build prompt                                                  │
│  4. Call: claude --continue -p "{prompt}" --output-format json    │
│  5. Parse response                                                │
│  6. Apply graph mutations                                         │
│  7. Clear world_injection.md                                      │
│  8. Write scene tree to /data/scenes/                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Locations

```
playthroughs/{playthrough_id}/world_injection.md    # From World Runner (if flips occurred)
/data/state/graph.json                               # Current world state
/data/scenes/{scene_id}.json                         # Output scene trees
```

---

## The Thread (Continuity)

Single persistent conversation with the narrator. Never reset within a playthrough.

```
[System Prompt]
[Scene 1 generation]
[Scene 1 output]
[Scene 2 generation]
[Scene 2 output]
...continuing indefinitely with --continue
```

**The narrator remembers everything it authored.**

### Why Continuity Matters

- **Foreshadowing:** Seeds planted earlier can pay off later.
- **Consistency:** Character voices and patterns stay coherent.
- **Accumulated Knowledge:** The narrator remembers prior scenes, clickables, and setup arcs.

### When to Start Fresh

- **New playthrough:** New thread
- **Same playthrough:** Same thread

### Thread Management

If the thread exceeds context:

```
[System Prompt]
[Summary: Scenes 1-10]
[Full: Scenes 11-15]
[Current generation]
```

### Thread vs Graph

| Thread | Graph |
|--------|-------|
| What was authored | What's true |
| Narrator's memory | World's memory |
| Voice and style | Facts and connections |
| Seeds and setups | Narratives and beliefs |

### Error Handling

- **Thread lost:** Start new thread, summarize recent scenes, continue
- **Thread corrupted:** Graph mutations take precedence, narrator self-corrects

---

## Prompt Structure

```
claude --continue -p "
NARRATOR INSTRUCTION
════════════════════

You are the persistent narrator of The Blood Ledger.
You remember everything you have authored in this playthrough.

{WORLD_INJECTION if exists}

{SCENE_CONTEXT}

{GENERATION_INSTRUCTION}

Output JSON matching the schema. Include time_elapsed estimate.
" --output-format json
```

---

## World Injection Block

When `playthroughs/{playthrough_id}/world_injection.md` exists, include:

```
WORLD INJECTION
───────────────

Time since last scene: {time_since_last}

{if breaks}
NARRATIVE BREAKS:
{for each break}
- {break.narrative}: {break.event}
  Player awareness: {break.player_awareness}
{end for}
{end if}

{if news_arrived}
NEWS THAT REACHED PLAYER:
{for each news}
- {news}
{end for}
{end if}

{if tension_changes}
TENSION SHIFTS:
{for each tension, delta}
- {tension}: {delta > 0 ? '+' : ''}{delta}
{end for}
{end if}

{if interruption}
⚠️ INTERRUPTION
Type: {interruption.type}
Description: {interruption.description}
Urgency: {interruption.urgency}

Narrator instruction: {interruption.narrator_instruction}
{end if}

{if atmosphere_shift}
Atmosphere: {atmosphere_shift}
{end if}

{if narrator_notes}
Notes: {narrator_notes}
{end if}

───────────────
```

---

## Scene Context Block

Always included:

```
SCENE CONTEXT
─────────────

Location: {place.name}
  {place.description}

Time: {time_of_day}, Day {day}

Present:
{for each character}
- {character.name}: {character.brief_description}
{end for}

Active narratives (voices):
{for each narrative, sorted by weight}
- [{narrative.weight}] {narrative.summary}
{end for}

Current tensions:
{for each tension}
- {tension.description} (pressure: {tension.pressure}/{tension.breaking_point})
{end for}

Player state:
- Pursuing: {player.goals}
- Recent: {player.recent_actions}

─────────────
```

---

## Generation Modes

### Conversational (Default)

For questions, observations, character interactions — anything <5 minutes:

```
1. Classify action as conversational
2. Stream dialogue chunks immediately
3. Query graph for facts mid-stream
4. Invent when graph is sparse
5. Output mutations
6. Return empty scene {}
```

### Significant

For travel, rest, combat, major decisions — anything ≥5 minutes:

```
1. Classify action as significant
2. Stream transition dialogue
3. Query graph for context
4. Generate full SceneTree
5. Output mutations
6. Return scene + time_elapsed
```

---

## Generation Instructions

### For Scene Generation (no interruption)

```
GENERATE SCENE
──────────────

Generate the scene package:

1. NARRATION
   - 2-3 sentences, present tense, sensory
   - Italic tone (scene-setting)
   - Include 2-3 clickable words

2. SPEECH (if character would speak)
   - One character speaks
   - In their voice
   - Include 1-2 clickable words

3. VOICES
   - 2-3 internal thoughts from active narratives
   - Highest-weight narratives speak loudest
   - Each voice has clickable concepts

4. CLICKABLES
   - For each clickable word, provide:
     - speaks: what player says when clicking
     - intent: tag for tracking
     - response: full response package (narration + speech + new clickables)
   - Generate 2 layers deep

5. TIME_ELAPSED
   - Estimate how much time this scene represents
   - Brief exchange: "2 minutes"
   - Conversation turn: "10 minutes"
   - Deep conversation: "30 minutes"

Output as JSON.
```

### For Interruption Handling

```
HANDLE INTERRUPTION
───────────────────

An interruption has occurred: {interruption.description}

Weave this into the scene:
1. Break the current moment naturally
2. Show how present characters react
3. The interruption becomes the new focus
4. Previous clickables may no longer apply

Generate:
- Narration showing the interruption
- Character reactions
- New clickables responding to the interruption
- TIME_ELAPSED for the interruption moment

The player must respond to this before continuing previous threads.
```

---

## Required Output Schema (Prompt JSON)

```typescript
interface NarratorOutput {
  scene: ScenePackage;

  // REQUIRED: Triggers graph ticks
  time_elapsed: string;  // "5 minutes", "2 hours", "3 days"

  // Graph changes from this generation
  mutations: GraphMutation[];

  // Seeds planted for future
  seeds?: {
    setup: string;
    intended_payoff: string;
  }[];
}

interface ScenePackage {
  narration: TextWithClickables;
  speech?: {
    speaker: string;
    text: TextWithClickables;
  };
  voices: VoiceWithClickables[];
  clickable: Record<string, Clickable>;
}

interface Clickable {
  speaks: string;
  intent: string;
  response: ScenePackage;  // Nested response
}
```

---

## SceneTree Structure (Legacy Scene Outputs)

```typescript
interface SceneTree {
  id: string;
  location: {
    place: string;          // Graph place ID
    name: string;           // Display name
    region: string;         // Location description
    time: string;           // Time of day
  };
  present: string[];        // Character IDs present
  atmosphere: string[];     // 2-3 atmospheric lines
  narration: SceneTreeNarration[];
  voices: SceneTreeVoice[];
  freeInput?: {
    enabled: boolean;
    handler: string;
    context: string[];
  };
}

interface SceneTreeNarration {
  text: string;                                     // 2-3 sentences
  speaker?: string;                                 // If dialogue
  clickable?: Record<string, SceneTreeClickable>;   // Embedded clickables
}

interface SceneTreeClickable {
  speaks: string;           // What player says when clicking
  intent: string;           // Tag for tracking
  response?: SceneTreeResponse;  // Pre-baked response (optional)
  waitingMessage?: string;  // Shown while LLM generates (required if no response)
}
```

---

## Time Elapsed Guidelines

The narrator MUST estimate time for every response:

| Scene Type | Time Estimate |
|------------|---------------|
| Brief reaction | "1 minute" |
| Single exchange | "2-3 minutes" |
| Conversation turn | "5-10 minutes" |
| Deep dialogue | "20-30 minutes" |
| Extended scene | "1 hour" |
| Rest/camp | "4-8 hours" |
| Travel (short) | "2-4 hours" |
| Travel (long) | "1-3 days" |

**This drives the entire world simulation.** Without time_elapsed, graph ticks can't run.

---

## Handling Different Injection Types

### Breaks (player_awareness: 'witnessed')

Player saw it happen. Weave directly into scene:

```
The narration shows the event unfolding.
Characters react in real-time.
This IS the scene.
```

### Breaks (player_awareness: 'heard')

Player heard about it. Deliver as news:

```
A character tells them.
Or: they overhear conversation.
Or: a messenger arrives.
The player learns, doesn't witness.
```

### Breaks (player_awareness: 'will_hear')

Will reach player later. Don't include yet:

```
Narrator notes this for later.
When player reaches relevant location, deliver then.
```

### Interruption (urgency: 'high')

Must change scene immediately:

```
Break current conversation.
"Aldric's hand goes to his sword—"
The interruption takes over.
Previous clickables suspended.
```

### Interruption (urgency: 'medium')

Can weave in naturally:

```
Work into next beat.
Character might mention it.
Doesn't have to break flow.
```

### Atmosphere Shift

Subtle environmental change:

```
Include in narration.
"The fire has burned low."
"Dawn light creeps in."
Mood, not plot.
```

---

## Character Voice Guidelines

### Aldric
- Short sentences. Doesn't waste words.
- Saxon rhythms. Direct.
- Avoids talking about feelings directly.
- When pressed, deflects or goes silent.
- When he does open up, it's powerful because it's rare.

**Examples:**
- "Keeps my hands busy."
- "Everyone knows what the Harrying was."
- "Nothing worth saying."

### Edmund (when encountered)
- More words than necessary. Justifying.
- Defensive but trying to seem reasonable.
- Believes his own story.
- Mentions practical concerns.

**Examples:**
- "You don't understand what it was like. Father was dying, someone had to—"
- "I saved the family. You would have lost everything."

---

## Voice Generation

Voices come from high-weight narratives. For each:

```typescript
function generateVoiceText(narrative: Narrative, context: SceneContext): string {
  // The voice speaks the narrative's emotional truth in this moment
  // Weighted by narrative.weight and relevance to current scene
}
```

**Voice characteristics:**
- Present tense or immediate relevance
- Short (one line)
- Emotional, not informational
- May contradict each other (tension!)

**Examples:**
- From narr_edmund_betrayal: "Three days to York. He's close now."
- From narr_aldric_thornwick: "He hasn't spoken since Thornwick."
- From narr_blood_brothers: "He's still your brother."

---

## Clickable Word Selection

Words should be clickable when:

1. **They're specific** — Names, places, concrete nouns
2. **They carry emotional weight** — "brother", "oath", "fire"
3. **They open threads** — Clicking reveals or deepens
4. **They're actionable** — Player could respond to them

Words should NOT be clickable when:
- They're generic ("the", "and", "very")
- Clicking would feel arbitrary
- There's no meaningful response

**Target:** 3-6 clickable words per narration block.

---

## Invention Guidelines

When the graph is sparse, invent. But invented content must:

1. **Fit the world** — Norman England, 1067
2. **Connect to existing** — Link to known characters, places
3. **Be persisted** — Output as mutations
4. **Create callbacks** — Plant seeds for later

**What to invent:**
- Character backstory details
- Family relationships
- Locations they've been
- Skills and traits
- Connections to player's history

**What NOT to invent:**
- Major plot points without setup
- Contradictions to established facts
- Genre-breaking elements

---

## Background Generation

When player is in scene N:
1. Serve scene N (already generated)
2. Background: generate scenes N+1, N+2 (likely next scenes)
3. As player clicks, extend current tree if needed

**Priority queue:**
1. Current scene extensions (player is clicking)
2. High-probability next scenes
3. Possible next scenes
4. Distant future scenes

---

## Quality Control

Before serving, scene trees should pass:

- [ ] All clickables have responses OR waitingMessage
- [ ] No dead ends (every path has exit or continuation)
- [ ] Character voices are consistent
- [ ] Clickable words make sense in context
- [ ] Invented content fits the world
- [ ] Emotional beats land properly

---

## Rolling Window Generation

**Generate current + N layers ahead. As player clicks, generate next layer in background.**

```
Time →

Player sees:     [Layer 0]
Already exists:  [Layer 0] [Layer 1] [Layer 2]
                     ↑
                  player is here

Player clicks → Layer 1 becomes Layer 0
Background:     Generate new Layer 2
```

### The Window

```typescript
interface RollingWindow {
  current: SceneState;              // What player sees now
  depth1: Map<string, SceneState>;  // Responses to current clickables
  depth2: Map<string, SceneState>;  // Responses to depth1 clickables
  generating: Set<string>;          // Currently being generated
}
```

**Window size: 2 layers ahead**
- Current: rendered
- Depth 1: instant on click
- Depth 2: ready when depth 1 becomes current

### On Scene Load

1. Check if scene tree exists in cache
2. If yes: load current + depth 1 + depth 2
3. If no: generate current, then depth 1, then depth 2
4. Render current immediately (even before depth 2 ready)

```typescript
async function loadScene(sceneId: string): Promise<RollingWindow> {
  // Try cache first
  const cached = await cache.get(sceneId);
  if (cached && cached.depth2) {
    return cached;
  }

  // Generate progressively
  const current = await generateSceneState(sceneId);
  render(current); // Show immediately

  const depth1 = await generateResponses(current.clickable);

  // Background: don't block
  generateDepth2(depth1).then(d2 => {
    window.depth2 = d2;
  });

  return { current, depth1, depth2: new Map() };
}
```

### On Click

```typescript
async function handleClick(word: string): Promise<void> {
  const response = window.depth1.get(word);

  // Instant: swap in response
  window.current = response;
  window.depth1 = window.depth2.get(word) || new Map();
  render(window.current);

  // Background: generate new depth 2
  generateDepth2(window.depth1).then(d2 => {
    window.depth2 = d2;
  });
}
```

### Generation Priority

Prioritize by:

1. **Weight** — Higher weight clickables first
2. **Position** — Words earlier in text first
3. **Type** — Voices before narration

```typescript
function prioritizeClickables(clickables: Clickable[]): Clickable[] {
  return clickables.sort((a, b) => {
    // Voices first
    if (a.source === 'voice' && b.source !== 'voice') return -1;
    // Then by weight
    return b.weight - a.weight;
  });
}
```

### Handling Slow Generation

```typescript
async function handleClick(word: string): Promise<void> {
  const response = window.depth1.get(word);

  window.current = response;
  render(window.current);

  // Check if depth 2 ready
  if (!window.depth2.has(word)) {
    // Show subtle indicator while generating
    showThinkingIndicator();

    // Generate just what we need
    const newDepth1 = await generateResponses(response.clickable);
    window.depth1 = newDepth1;

    hideThinkingIndicator();
  } else {
    window.depth1 = window.depth2.get(word);
  }

  // Continue background generation
  generateDepth2(window.depth1);
}
```

### Scene Transitions

```typescript
interface SceneTransition {
  type: 'transition';
  next: string;           // Scene ID
  narration?: string;     // "You stand. The cold hits."
}

async function handleTransition(transition: SceneTransition): Promise<void> {
  // Show transition narration
  if (transition.narration) {
    render({ narration: transition.narration });
    await delay(1500); // Let player read
  }

  // Pre-fetch was hopefully running
  const nextScene = await loadScene(transition.next);
  render(nextScene.current);
}
```

### Caching Strategy

```typescript
interface SceneCache {
  // Full trees for visited scenes
  visited: Map<string, SceneTree>;

  // Partial trees for likely scenes
  prefetched: Map<string, RollingWindow>;

  // Generation queue
  queue: PriorityQueue<GenerationJob>;
}
```

**Cache lifetime:**
- Visited scenes: keep until session ends
- Prefetched scenes: keep 5 most likely
- Evict LRU when memory pressure

### Background Worker

```typescript
const generationWorker = {
  queue: new PriorityQueue(),

  async run() {
    while (true) {
      const job = await this.queue.pop();

      if (job.type === 'depth2') {
        await generateDepth2(job.clickables);
      } else if (job.type === 'prefetch') {
        await prefetchScene(job.sceneId);
      }
    }
  },

  prioritize(job: GenerationJob) {
    // Current scene depth > prefetch
    // Higher weight clickables > lower
    return job.priority;
  }
};
```

### Metrics to Track

| Metric | Target | Meaning |
|--------|--------|---------|
| Click-to-render | < 50ms | Instant feel |
| Depth 2 ready % | > 95% | Rarely wait |
| Generation time | < 2s | Fast enough to stay ahead |
| Cache hit rate | > 80% | Efficient reuse |

### Free Input Handling

```typescript
async function handleFreeInput(text: string): Promise<void> {
  showThinkingIndicator("Aldric considers...");

  const response = await generateFreeResponse({
    input: text,
    character: currentCharacter,
    context: getConversationContext(),
    graphContext: getRelevantNarratives()
  });

  hideThinkingIndicator();

  // Insert into current state
  window.current = {
    narration: response.narration,
    speech: response.speech,
    voices: window.current.voices, // Keep voices
    clickable: response.clickable
  };

  render(window.current);

  // Generate ahead from new state
  generateDepth1And2(window.current);
}
```

---

## The --continue Flag

The Narrator uses `--continue` to maintain thread:

```bash
# First scene of playthrough
claude -p "{initial_prompt}" --output-format json

# All subsequent scenes
claude --continue -p "{prompt}" --output-format json
```

**The thread is the narrator's memory.** It remembers:
- Every scene it authored
- Every seed it planted
- Character voice patterns
- Setups awaiting payoff

**Never reset the thread within a playthrough.**

---

## Orchestrator Pseudocode

```python
def generate_scene(scene_context):
    # 1. Check for world injection
    injection = None
    injection_path = f'playthroughs/{playthrough_id}/world_injection.md'
    if file_exists(injection_path):
        injection = read_json(injection_path)

    # 2. Build prompt
    prompt = build_prompt(scene_context, injection)

    # 3. Call narrator (--continue maintains thread)
    result = subprocess.run([
        'claude', '--continue',
        '-p', prompt,
        '--output-format', 'json'
    ], capture_output=True)

    # 4. Parse output
    output = json.loads(result.stdout)

    # 5. Apply mutations to graph
    apply_mutations(output['mutations'])

    # 6. Clear injection (consumed)
    if injection:
        delete_file(injection_path)

    # 7. Trigger graph tick with time_elapsed
    flips = graph_tick(output['time_elapsed'])

    # 8. If flips, run World Runner
    if flips:
        world_runner_output = run_world_runner(flips)
        write_json(injection_path, world_runner_output)

    # 9. Return scene for frontend
    return output['scene']
```

---

*"Talk first. Query as you speak. Invent when the graph is silent. The world grows through conversation."*

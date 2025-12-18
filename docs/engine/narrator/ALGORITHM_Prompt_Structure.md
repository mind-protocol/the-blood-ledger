# Narrator — Algorithm: Prompt Structure

```
CREATED: 2024-12-16
STATUS: Draft
```

---

## The Orchestration

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                              │
│                                                                  │
│  1. Read world_injection.md (if exists)                       │
│  2. Read graph state                                             │
│  3. Build prompt                                                 │
│  4. Call: claude --continue -p "{prompt}" --output-format json  │
│  5. Parse response                                               │
│  6. Apply graph mutations                                        │
│  7. Clear world_injection.md                                   │
│  8. Write scene tree to /data/scenes/                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Locations

```
playthroughs/{playthrough_id}/world_injection.md    # From World Runner (if flips occurred)
/data/state/graph.json              # Current world state
/data/scenes/{scene_id}.json        # Output scene trees
```

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

## Required Output Schema

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

*"The narrator receives the world's state. The narrator returns the world's story. Time flows through both."*

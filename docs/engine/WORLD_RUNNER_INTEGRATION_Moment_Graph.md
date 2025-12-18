# World Runner Integration: Moment Graph Architecture

```
STATUS: Integration Guide
CREATED: 2024-12-17
AFFECTS: agents/world_runner/CLAUDE.md, engine/orchestration/world_runner.py
```

This document specifies how World Runner integrates with the Moment Graph system.

---

## Current World Runner Role

From `agents/world_runner/CLAUDE.md`:

> You are the **author of consequence**. When a tension breaks, you determine what *specifically* happened.

**Current outputs:**
1. `mutations/wr_{flip_id}.yaml` — Graph changes
2. `playthroughs/{id}/injection_queue.json` — Actions for Narrator

---

## What Changes

### World Runner Gains Moment Authority

World Runner now has authority over **moments** as well as narratives:

| Before | After |
|--------|-------|
| Creates narratives | Creates narratives AND moments |
| Updates beliefs | Updates beliefs AND moment weights |
| Reports cascades | Reports cascades AND moment activations |

### Why This Matters

When a tension breaks:
1. **What happened** → Narrative (existing)
2. **How it surfaces to player** → Moment (NEW)

Example: The leadership tension breaks.
- **Narrative:** "Aldric publicly challenged Rolf's leadership at the York gates."
- **Moment:** Aldric's voice: "We need to decide this. Now."

---

## Extended Mutation Format

### Current Format (CLAUDE.md)

```yaml
# mutations/wr_{flip_id}.yaml
thinking: |
  ...reasoning...

event:
  summary: "..."
  location: place_id
  witnesses: [char_ids]
  caused_by: [narr_ids]

nodes: []      # narratives, characters, places, things
links: []      # beliefs, relationships
updates: []    # tensions
movements: []  # character locations
cascades: []   # tension IDs to re-check
```

### Extended Format (Moment Graph)

```yaml
# mutations/wr_{flip_id}.yaml
thinking: |
  Why this tension broke and what specifically happened.
  How it should surface to the player.

event:
  summary: "Aldric publicly challenged Rolf's leadership at the York gates."
  location: place_york_gates
  witnesses: [char_mildred, char_godwin]
  caused_by: [narr_leadership_tension, narr_aldric_doubt]

nodes:
  # Narratives (existing)
  - type: narrative
    id: narr_leadership_challenged
    name: "Leadership Challenged"
    content: "Aldric openly questioned whether Rolf should lead."
    narrative_type: account
    tone: tense
    about:
      characters: [char_aldric, char_rolf]

  # Moments (NEW) — How events surface
  - type: moment
    id: moment_aldric_challenge
    text: "Aldric steps forward. 'We need to decide who leads this band. Now.'"
    moment_type: dialogue
    status: possible
    weight: 0.85  # High weight — will likely flip to active
    tone: defiant

  - type: moment
    id: moment_mildred_reaction
    text: "Mildred's hand moves to her knife, watching both men."
    moment_type: narration
    status: possible
    weight: 0.6

  - type: moment
    id: moment_rolf_response_option
    text: "What do you say?"
    moment_type: hint
    status: possible
    weight: 0.5

links:
  # Beliefs (existing)
  - type: belief
    character: char_aldric
    narrative: narr_leadership_challenged
    heard: 1.0
    believes: 1.0
    originated: 1.0
    source: witnessed

  # CAN_SPEAK links (NEW)
  - type: can_speak
    character: char_aldric
    moment: moment_aldric_challenge
    weight: 1.0

  # ATTACHED_TO links (NEW)
  - type: attached_to
    moment: moment_aldric_challenge
    target: char_aldric
    target_type: character
    presence_required: true
    persistent: true

  - type: attached_to
    moment: moment_aldric_challenge
    target: tension_leadership
    target_type: tension
    presence_required: true  # Surfaces when tension is active

  # CAN_LEAD_TO links (NEW)
  - type: can_lead_to
    from: moment_aldric_challenge
    to: moment_rolf_response_option
    trigger: auto
    weight_transfer: 0.4
    consumes_origin: true

updates:
  - tension: tension_leadership
    pressure: 0.0  # Reset after break
    resolved: false  # Not resolved, just released

movements:
  - character: char_aldric
    to: place_york_gates
    visible: true

cascades: []

# NEW: Moment activations to report
moment_activations:
  - moment_id: moment_aldric_challenge
    reason: "Tension break surfaced this moment"
```

---

## Extended Injection Queue Format

### Current Format (CLAUDE.md)

```json
{
  "injections": [
    {
      "type": "event",
      "event": "...",
      "awareness": "will_hear",
      "delivery": "...",
      "key_nodes": [],
      "connected_narratives": [],
      "narrator_notes": "..."
    }
  ]
}
```

### Extended Format (Moment Graph)

```json
{
  "injections": [
    {
      "type": "event",
      "event": "Aldric challenged Rolf's leadership at the York gates.",
      "awareness": "witnessed",
      "delivery": null,
      "key_nodes": ["narr_leadership_challenged"],
      "connected_narratives": ["narr_aldric_doubt", "narr_rolf_oath"],
      "narrator_notes": "This is a turning point. Build tension before resolution."
    },
    {
      "type": "moment_activation",
      "moment_id": "moment_aldric_challenge",
      "status": "active",
      "weight_boost": 0.2,
      "narrator_notes": "This moment should surface immediately."
    },
    {
      "type": "moment_creation",
      "moment": {
        "id": "moment_crowd_murmur",
        "text": "The gathered Saxons exchange uneasy glances.",
        "type": "narration",
        "status": "possible",
        "weight": 0.4,
        "tone": "tense"
      },
      "links": [
        {
          "type": "attached_to",
          "target": "place_york_gates",
          "target_type": "place",
          "presence_required": true
        }
      ],
      "narrator_notes": "Background atmosphere."
    }
  ]
}
```

### New Injection Types

| Type | When to Use | What Narrator Does |
|------|-------------|-------------------|
| `event` | Discrete world event | Narrate how player learns |
| `character_action` | NPC does something | Inject into scene |
| `player_action` | Instinctive reaction | Describe player's body |
| `atmospheric` | Mood shift | Background details |
| `moment_activation` | Surface existing moment | Set status=active |
| `moment_creation` | Create new moment | Add to graph + surface |

---

## Updated World Runner Process

### Step 1: Understand Flips (Same)

Query graph for tension details, narratives, characters involved.

### Step 2: Determine What Happened (Same)

Generate specific event with witnesses, location, causation.

### Step 3: Create Narratives (Same)

New narratives for beliefs about what happened.

### Step 4: Create Moments (NEW)

For each significant aspect of the event:

1. **Direct dialogue** — What characters say
   - Create moment with `type: dialogue`
   - Add `can_speak` link to speaker
   - Add `attached_to` with `presence_required: true`

2. **Actions/reactions** — What characters do
   - Create moment with `type: action` or `narration`
   - Attach to witnessing characters

3. **Response options** — What player can do
   - Create hint moments
   - Link via `can_lead_to` from dialogue

### Step 5: Wire Traversals (NEW)

Create `can_lead_to` links:
- From dialogue to response options
- From actions to reactions
- Set appropriate triggers (click, auto, wait)

### Step 6: Report Activations (NEW)

In mutation output, list moments that should activate:
```yaml
moment_activations:
  - moment_id: moment_aldric_challenge
    reason: "Tension break caused this"
```

### Step 7: Write Injection Queue (Enhanced)

Include moment activations/creations alongside events.

---

## World Runner Agent Instructions Update

Add to `agents/world_runner/CLAUDE.md`:

```markdown
## Moment Creation Guidelines

When a tension breaks, create moments that:

### 1. Surface the Event
The event happened — now it needs to reach the player.

**If player witnessed:**
- Create dialogue moment for the speaker
- Create narration moment for actions
- Set `status: active` (immediate)

**If player will hear:**
- Create arrival/messenger moment
- Set `status: possible` (waiting for conditions)
- Attach to the news-bringer character

### 2. Enable Response
Give the player ways to engage:

- Create hint moments with response options
- Wire `can_lead_to` links from dialogue
- Use `trigger: click` with `require_words`

### 3. Preserve Context
Attach moments to their context:

- Character who speaks: `presence_required: true`
- Place where it happens: `presence_required: true`
- Narrative that caused it: `presence_required: true`
- `persistent: true` for important moments

### 4. Control Surfacing
Use weight to control when moments surface:

- `weight: 0.9` — Will surface immediately
- `weight: 0.6` — May surface naturally
- `weight: 0.3` — Waiting for boost
- `weight: 0.1` — Unlikely to surface without trigger

### Moment Output Template

For each flip, include in your output:

```yaml
nodes:
  # The core dialogue/action
  - type: moment
    id: moment_{flip_id}_main
    text: "..."
    moment_type: dialogue
    status: possible
    weight: 0.85
    tone: ...

  # Witness reactions
  - type: moment
    id: moment_{flip_id}_reaction_{witness}
    text: "..."
    moment_type: narration
    status: possible
    weight: 0.5

links:
  # Speaker
  - type: can_speak
    character: {speaker_id}
    moment: moment_{flip_id}_main
    weight: 1.0

  # Context attachments
  - type: attached_to
    moment: moment_{flip_id}_main
    target: {character_id}
    target_type: character
    presence_required: true
    persistent: true

  # Traversals
  - type: can_lead_to
    from: moment_{flip_id}_main
    to: moment_{flip_id}_response
    trigger: click
    require_words: [...]

moment_activations:
  - moment_id: moment_{flip_id}_main
    reason: "Flip resolution"
```
```

---

## Code Changes

### `engine/orchestration/world_runner.py`

Update `_build_prompt()` to include moment instructions:

```python
def _build_prompt(
    self,
    flips: List[Dict[str, Any]],
    graph_context: Dict[str, Any],
    player_context: Dict[str, Any],
    time_span: str
) -> str:
    """Build the world runner prompt."""
    import yaml

    parts = [
        "WORLD RUNNER INSTRUCTION",
        "=" * 24,
        "",
        f"TIME_SPAN: {time_span}",
        "",
        "FLIPS:",
        yaml.dump(flips, default_flow_style=False),
        "",
        "GRAPH_CONTEXT:",
        yaml.dump(graph_context, default_flow_style=False),
        "",
        "PLAYER_CONTEXT:",
        yaml.dump(player_context, default_flow_style=False),
        "",
        "Determine what happened during this time span.",
        "For each flip, determine:",
        "1. What specifically occurred",
        "2. Who witnessed it",
        "3. What new narratives emerge",
        "4. How beliefs change",
        "5. Any cascading effects",
        "",
        "MOMENT GRAPH INSTRUCTIONS:",
        "For each flip, also create MOMENTS that surface the event:",
        "- Dialogue moments for what characters say",
        "- Action/narration moments for what happens",
        "- Hint moments for player response options",
        "- Wire can_lead_to links for traversal",
        "- Set appropriate weight (0.85+ for immediate surface)",
        "",
        "Output JSON matching WorldRunnerOutput schema.",
        "Include moment_activations list for moments that should surface.",
    ]

    return "\n".join(parts)
```

Update `_fallback_response()` to include moment fields:

```python
def _fallback_response(self) -> Dict[str, Any]:
    """Return a minimal fallback response."""
    return {
        "thinking": "Fallback response - World Runner unavailable",
        "graph_mutations": {
            "new_narratives": [],
            "new_beliefs": [],
            "tension_updates": [],
            "new_tensions": [],
            "character_movements": [],
            "modifier_changes": [],
            # NEW
            "new_moments": [],
            "moment_links": [],
            "moment_activations": []
        },
        "world_injection": {
            "time_since_last": "unknown",
            "breaks": [],
            "news_arrived": [],
            "tension_changes": {},
            "interruption": None,
            "atmosphere_shift": None,
            "narrator_notes": "World Runner unavailable - minimal response",
            # NEW
            "moment_injections": []
        }
    }
```

---

## Validation

### Mutation File Validation

```python
def validate_moment_mutation(mutation: Dict) -> List[str]:
    """Validate moment-related mutation content."""
    errors = []

    for node in mutation.get('nodes', []):
        if node.get('type') == 'moment':
            # Required fields
            if not node.get('id'):
                errors.append(f"Moment missing id")
            if not node.get('text'):
                errors.append(f"Moment {node.get('id')} missing text")
            if not node.get('moment_type'):
                errors.append(f"Moment {node.get('id')} missing moment_type")

            # Weight bounds
            weight = node.get('weight', 0.5)
            if not 0 <= weight <= 1:
                errors.append(f"Moment {node.get('id')} weight {weight} out of bounds")

    for link in mutation.get('links', []):
        if link.get('type') == 'can_speak':
            if not link.get('character'):
                errors.append("can_speak link missing character")
            if not link.get('moment'):
                errors.append("can_speak link missing moment")

        if link.get('type') == 'can_lead_to':
            if not link.get('from'):
                errors.append("can_lead_to link missing from")
            if not link.get('to'):
                errors.append("can_lead_to link missing to")

    return errors
```

---

## Example: Leadership Tension Break

### Input (Flip)

```yaml
- tension_id: tension_leadership
  pressure: 0.95
  breaking_point: 0.9
  trigger_reason: "Pressure exceeded breaking point"
  narratives:
    - narr_rolf_oath
    - narr_aldric_doubt
```

### Output (World Runner)

```yaml
thinking: |
  The leadership tension has broken. Aldric has been doubting Rolf's decisions,
  and the pressure finally caused him to speak up publicly.

  This happens at York gates because:
  1. Public setting adds weight
  2. Both characters are present
  3. Stakes are highest when visible to others

  The player should experience this directly - they're there when it happens.

event:
  summary: "Aldric openly challenged Rolf's leadership at the York gates."
  location: place_york_gates
  witnesses: [char_mildred, char_godwin, char_player]
  caused_by: [narr_rolf_oath, narr_aldric_doubt]

nodes:
  - type: narrative
    id: narr_leadership_challenged
    name: "The Challenge"
    content: "Aldric publicly questioned whether Rolf should lead the band."
    narrative_type: account
    tone: tense
    about:
      characters: [char_aldric, char_rolf]

  - type: moment
    id: moment_aldric_challenge_001
    text: "Aldric steps forward, jaw set. 'We need to decide who leads this band. Now.'"
    moment_type: dialogue
    status: possible
    weight: 0.9
    tone: defiant

  - type: moment
    id: moment_mildred_watches
    text: "Mildred's hand moves to her knife hilt, eyes darting between the two men."
    moment_type: narration
    status: possible
    weight: 0.6

  - type: moment
    id: moment_crowd_tense
    text: "The gathered Saxons fall silent, watching."
    moment_type: narration
    status: possible
    weight: 0.4

links:
  - type: belief
    character: char_aldric
    narrative: narr_leadership_challenged
    heard: 1.0
    believes: 1.0
    originated: 1.0
    source: witnessed

  - type: belief
    character: char_mildred
    narrative: narr_leadership_challenged
    heard: 1.0
    believes: 1.0
    source: witnessed

  - type: can_speak
    character: char_aldric
    moment: moment_aldric_challenge_001
    weight: 1.0

  - type: attached_to
    moment: moment_aldric_challenge_001
    target: char_aldric
    target_type: character
    presence_required: true
    persistent: true

  - type: attached_to
    moment: moment_aldric_challenge_001
    target: tension_leadership
    target_type: tension
    presence_required: true

  - type: attached_to
    moment: moment_mildred_watches
    target: char_mildred
    target_type: character
    presence_required: true

updates:
  - tension: tension_leadership
    pressure: 0.3  # Reduced but not gone

cascades: []

moment_activations:
  - moment_id: moment_aldric_challenge_001
    reason: "Leadership tension break - direct confrontation"
```

---

## Summary

| World Runner Responsibility | Before | After |
|----------------------------|--------|-------|
| Event determination | Yes | Yes |
| Narrative creation | Yes | Yes |
| Belief updates | Yes | Yes |
| **Moment creation** | No | **Yes** |
| **Moment wiring** | No | **Yes** |
| **Activation reporting** | No | **Yes** |

The World Runner remains the author of consequence. Now it also authors how consequences surface to the player through the moment graph.

---

*"What happened is one thing. How the player experiences it is another. The World Runner now controls both."*

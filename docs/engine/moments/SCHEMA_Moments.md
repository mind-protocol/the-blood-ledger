# Moments — Schema Reference

```
CREATED: 2024-12-17
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Moments.md
BEHAVIORS:   ./BEHAVIORS_Moments.md
ALGORITHMS:  ./ALGORITHM_View_Query.md, ./ALGORITHM_Transitions.md, ./ALGORITHM_Lifecycle.md
THIS:        SCHEMA_Moments.md (you are here)
API:         ./API_Moments.md
VALIDATION:  ./VALIDATION_Moments.md
SYNC:        ./SYNC_Moments.md
IMPL:        ../../engine/db/graph_ops.py
```

---

## Moment Node

```yaml
Moment:
  # Identity
  id: string              # moment_{uuid} or moment_{descriptive_name}

  # Content
  text: string            # The actual text content
  type: string            # narration | dialogue | action | possibility | hint

  # State
  status: string          # possible | active | spoken | dormant | decayed
  weight: float           # 0.0 - 1.0, determines visibility priority

  # Timestamps (ticks)
  tick_created: int       # When created
  tick_spoken: int        # When actualized (null if never)
  tick_decayed: int       # When decayed (null if still live)

  # Display hints
  tone: string            # whispered | shouted | cold | warm | questioning | etc

  # Search
  embedding: float[]      # 768-dim vector for semantic search
```

### Type Values

| Type | Meaning |
|------|---------|
| narration | Descriptive text, no speaker |
| dialogue | Spoken by a character |
| action | Something happening |
| possibility | Internal thought or option |
| hint | Meta-information for player |

### Status Values

| Status | Meaning |
|--------|---------|
| possible | Created, waiting to surface |
| active | Currently visible |
| spoken | Actualized, part of history |
| dormant | Frozen, waiting for return |
| decayed | Weight dropped, pending deletion |

---

## Link: CAN_SPEAK

Who can speak a moment. Direction: Character → Moment.

```yaml
CAN_SPEAK:
  from: Character
  to: Moment

  weight: float           # Priority (0.0 - 1.0)
                          # Highest weight present character speaks
```

### Resolution Rules

1. Get all CAN_SPEAK links pointing to moment
2. Filter to characters currently present
3. Return character with highest weight
4. If none present, moment has no speaker (becomes narration or hidden)

---

## Link: ATTACHED_TO

What a moment is attached to. Direction: Moment → Target.

```yaml
ATTACHED_TO:
  from: Moment
  to: Character | Place | Thing | Narrative | Tension

  presence_required: bool   # true = target must be present for moment visible
                            # false = enriches but doesn't gate

  persistent: bool          # true = goes dormant when target leaves, reactivates on return
                            # false = deleted when target leaves

  dies_with_target: bool    # true = moment deleted if target is destroyed
                            # false = moment survives target destruction
```

### Valid Targets

| Target Type | Presence Meaning |
|-------------|------------------|
| Character | Character is in same location as player |
| Place | Player is at this place |
| Thing | Thing is present (at location or carried by present character) |
| Narrative | Player believes this narrative |
| Tension | Tension is active |

### Visibility Rule

A moment is visible when **ALL** attachments with `presence_required: true` have their targets present.

---

## Link: CAN_LEAD_TO

Defines conversation transitions. Direction: Moment → Moment.

```yaml
CAN_LEAD_TO:
  from: Moment
  to: Moment

  # Trigger
  trigger: string           # player | wait | auto
  require_words: [string]   # Words that trigger this transition (if trigger=player)
  wait_ticks: int           # Ticks before auto-fire (if trigger=wait)

  # Directionality
  bidirectional: bool       # true = can traverse both ways
                            # false = one-way only

  # Effects
  consumes_origin: bool     # true = origin status → spoken after traversal
                            # false = origin stays active

  weight_transfer: float    # Portion of origin weight given to target (0.0 - 1.0)
```

### Trigger Values

| Trigger | When Fires |
|---------|------------|
| player | Player clicks a word in require_words or types matching input |
| wait | wait_ticks have passed since origin became active |
| auto | Immediately when origin becomes active |

### Multiple Words

`require_words` is an array. Any matching word triggers the transition:

```yaml
require_words: ["understand", "why", "explain"]
# Clicking any of these words in the origin fires this transition
```

---

## Link: THEN

Records actualized history. Direction: Moment → Moment.

```yaml
THEN:
  from: Moment
  to: Moment

  tick: int                 # When this transition happened
  player_caused: bool       # true = player triggered (click/input)
                            # false = system triggered (wait/auto)
```

### Immutability

THEN links are never deleted. They form the permanent conversation history.

---

## Example Graph

```
# Characters
char_aldric (Character)
char_player (Character)

# Places
place_camp (Place)

# Moments
moment_fire_crackles (Moment)
  text: "The fire crackles, throwing shadows."
  type: narration
  status: active

moment_aldric_question (Moment)
  text: "Three days now. You haven't said why."
  type: dialogue
  status: possible
  weight: 0.9

moment_player_answer (Moment)
  text: "Vengeance."
  type: dialogue
  status: possible
  weight: 0.8

# Links
char_aldric -[CAN_SPEAK {weight: 1.0}]-> moment_aldric_question
char_player -[CAN_SPEAK {weight: 1.0}]-> moment_player_answer

moment_fire_crackles -[ATTACHED_TO {presence_required: true, persistent: true}]-> place_camp
moment_aldric_question -[ATTACHED_TO {presence_required: true, persistent: true}]-> char_aldric
moment_player_answer -[ATTACHED_TO {presence_required: true, persistent: true}]-> char_player

moment_fire_crackles -[CAN_LEAD_TO {
  trigger: player,
  require_words: ["fire", "shadows"],
  consumes_origin: false
}]-> moment_aldric_question

moment_aldric_question -[CAN_LEAD_TO {
  trigger: player,
  require_words: ["why", "days"],
  consumes_origin: true
}]-> moment_player_answer

# After player clicks "why":
moment_fire_crackles -[THEN {tick: 47, player_caused: true}]-> moment_aldric_question
moment_aldric_question -[THEN {tick: 48, player_caused: true}]-> moment_player_answer
```

---

## Cypher Examples

### Create Moment

```cypher
CREATE (m:Moment {
  id: 'moment_aldric_question',
  text: 'Three days now. You haven\'t said why.',
  type: 'dialogue',
  status: 'possible',
  weight: 0.9,
  tick_created: 45,
  tick_spoken: null,
  tick_decayed: null,
  tone: 'questioning'
})
```

### Create CAN_SPEAK

```cypher
MATCH (c:Character {id: 'char_aldric'})
MATCH (m:Moment {id: 'moment_aldric_question'})
CREATE (c)-[:CAN_SPEAK {weight: 1.0}]->(m)
```

### Create ATTACHED_TO

```cypher
MATCH (m:Moment {id: 'moment_aldric_question'})
MATCH (c:Character {id: 'char_aldric'})
CREATE (m)-[:ATTACHED_TO {
  presence_required: true,
  persistent: true,
  dies_with_target: false
}]->(c)
```

### Create CAN_LEAD_TO

```cypher
MATCH (from:Moment {id: 'moment_fire_crackles'})
MATCH (to:Moment {id: 'moment_aldric_question'})
CREATE (from)-[:CAN_LEAD_TO {
  trigger: 'player',
  require_words: ['fire', 'shadows'],
  bidirectional: false,
  consumes_origin: false,
  weight_transfer: 0.5
}]->(to)
```

### Create THEN

```cypher
MATCH (from:Moment {id: 'moment_aldric_question'})
MATCH (to:Moment {id: 'moment_player_answer'})
CREATE (from)-[:THEN {
  tick: 48,
  player_caused: true
}]->(to)
```

### Query Live Moments

```cypher
MATCH (m:Moment)
WHERE m.status IN ['possible', 'active']
WITH m, [(m)-[r:ATTACHED_TO WHERE r.presence_required = true]->(target) | target] AS required
WHERE ALL(target IN required WHERE
  (target:Place AND target.id = $location_id)
  OR (target:Character AND target.id IN $present_char_ids)
  OR (target:Thing AND target.id IN $present_thing_ids)
  OR (target:Narrative AND target.id IN $known_narrative_ids)
)
RETURN m
ORDER BY m.weight DESC
LIMIT 20
```

### Resolve Speaker

```cypher
MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $moment_id})
WHERE c.id IN $present_character_ids
RETURN c.id AS speaker
ORDER BY r.weight DESC
LIMIT 1
```

### Get Transitions

```cypher
MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO]->(next:Moment)
WHERE m.id IN $active_moment_ids
  AND next.status IN ['possible', 'dormant']
RETURN m.id AS from_id, r.require_words AS words, next.id AS to_id
```

---

*"The schema is the contract. Moments, links, and queries."*

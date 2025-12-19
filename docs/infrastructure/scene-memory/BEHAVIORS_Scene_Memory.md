# Scene Memory System — Behavior

```
STATUS: DRAFT
CREATED: 2024-12-16
```

===============================================================================
## CHAIN
===============================================================================

```
PATTERNS:    ./PATTERNS_Scene_Memory.md
THIS:        BEHAVIORS_Scene_Memory.md (you are here)
ALGORITHM:   ./ALGORITHM_Scene_Memory.md
VALIDATION:  ./VALIDATION_Scene_Memory.md
SYNC:        ./SYNC_Scene_Memory.md
```

===============================================================================
## OVERVIEW
===============================================================================

This document specifies **what** the system does — inputs, outputs, observable
behaviors — without specifying **how**.

===============================================================================
## ACTORS
===============================================================================

| Actor | Role |
|-------|------|
| **Narrator** | Produces scene output with named elements |
| **Player** | Clicks, types, chooses — all named actions |
| **System** | Expands names, stores scenes, creates beliefs |
| **Graph** | Stores everything, answers queries |

===============================================================================
## INPUT: NARRATOR OUTPUT
===============================================================================

The narrator produces structured output for each scene.

### Schema

```typescript
interface NarratorOutput {
  scene: {
    when: string              // "Day 5, dusk"
    where: place_id           // "place_crossing"
    present: character_id[]   // Who's there
  }
  narration: NarrationElement[]
  mutations: Mutation[]
}

interface NarrationElement {
  name: string                // Unique identifier for this moment
  text: string                // The actual text shown
  speaker?: character_id      // If dialogue (omit for narration)
  clickable?: {
    [word: string]: {
      speaks: string          // What shows on hover/click
      name: string            // Identifier for this hint
    }
  }
}

interface Mutation {
  type: "new_narrative" | "update_narrative" | "new_belief" | ...
  id: string
  content: string
  sources: string[]           // Names of moments/actions
  // ... other fields per type
}
```

### Example

```json
{
  "scene": {
    "when": "Day 5, dusk",
    "where": "place_crossing",
    "present": ["char_player", "char_aldric"]
  },
  "narration": [
    {
      "name": "blade_broken",
      "text": "The blade lies in two pieces at his feet.",
      "clickable": {
        "blade": {
          "speaks": "That was his father's sword.",
          "name": "blade_hint"
        }
      }
    },
    {
      "name": "aldric_done",
      "speaker": "char_aldric",
      "text": "It's done. He's done."
    }
  ],
  "mutations": [
    {
      "type": "new_narrative",
      "id": "narr_sword_broken",
      "content": "Aldric's father's sword broke killing the Dane",
      "sources": ["blade_broken", "aldric_done"]
    }
  ]
}
```

===============================================================================
## INPUT: PLAYER ACTIONS
===============================================================================

Three types of player input, all named.

### Click

Player clicks a highlighted word.

```json
{
  "type": "click",
  "name": "rolf_asks_about_blade",
  "clicked": "blade",
  "from": "blade_hint"
}
```

### Freeform

Player types custom input.

```json
{
  "type": "freeform",
  "name": "rolf_picks_up_shards",
  "text": "I gather the broken pieces carefully."
}
```

### Choice

Player selects from offered options.

```json
{
  "type": "choice",
  "name": "rolf_stays_silent",
  "selected": "say_nothing"
}
```

===============================================================================
## OUTPUT: MOMENT NODES
===============================================================================

Every narration element, clickable hint, and player action becomes a Moment node.

### Moment Schema

```yaml
Moment:
  id: string                    # crossing_d5_dusk_blade_broken
  text: string                  # The actual text
  type: string                  # narration | dialogue | player_click | player_freeform | player_choice | hint
  tick: int                     # World tick when this occurred
  embedding: float[]            # Vector for semantic search (if text > 20 chars)
```

### ID Pattern

```
{place}_{day}_{time}_{short_name}
```

### Input → Output

| Narrator writes | Moment ID stored |
|-----------------|------------------|
| `blade_broken` | `crossing_d5_dusk_blade_broken` |
| `blade_hint` | `crossing_d5_dusk_blade_hint` |
| `aldric_done` | `crossing_d5_dusk_aldric_done` |

| Player action | Moment ID stored |
|---------------|------------------|
| `rolf_asks_blade` | `crossing_d5_dusk_rolf_asks_blade` |
| `rolf_picks_shards` | `crossing_d5_dusk_rolf_picks_shards` |

### Moment Links

```
Character ──[SAID]──> Moment          (if dialogue)
Moment ──[AT]──> Place                (where it occurred)
Moment ──[THEN]──> Moment             (sequence within scene)
Scene ──[CONTAINS]──> Moment          (scene contains moments)
Narrative ──[FROM]──> Moment          (narrative sourced from moment)
```

===============================================================================
## OUTPUT: STORED SCENE
===============================================================================

Each scene becomes a node in the graph. Moments are separate nodes linked to it.

### Schema

```yaml
Scene:
  id: string                    # scene_d5_dusk_crossing
  when: string                  # "Day 5, dusk"
  tick: int                     # World tick at scene start
```

No embedded narration — moments are linked nodes.

### Links

```
Scene ──[AT]──> Place
Scene ──[INVOLVES]──> Character (for each present)
Scene ──[CONTAINS]──> Moment (for each moment in scene)
Scene ──[CREATES]──> Narrative (for each narrative created)
```

===============================================================================
## OUTPUT: STORED NARRATIVES
===============================================================================

Narratives link to their source moments via FROM relationships.

### Schema

```yaml
Narrative:
  id: string
  content: string               # Short summary
  detail: string                # Full description (optional)
  embedding: float[]            # Vector for semantic search
  occurred_at: string           # "Day 5, dusk"
  tick: int                     # World tick when created
```

No `sources` array — relationships via graph links.

### Links

```
Narrative ──[FROM]──> Moment (for each source moment)
Narrative ──[ABOUT]──> Thing (optional, for key objects)
```

### Example

```yaml
narr_sword_broken:
  id: narr_sword_broken
  content: "Aldric's sword broke killing the Dane"
  occurred_at: "Day 5, dusk"
  tick: 142
```

```
narr_sword_broken ──[FROM]──> crossing_d5_dusk_blade_broken
narr_sword_broken ──[FROM]──> crossing_d5_dusk_aldric_done
```

Relationships derived from:
- **Place:** Follow FROM → Moment → AT → Place
- **Characters:** Follow FROM → Moment ← SAID ← Character
- **Things:** Explicit ABOUT links when relevant

===============================================================================
## OUTPUT: AUTOMATIC BELIEFS
===============================================================================

All present characters gain beliefs about created narratives.

### Behavior

```
For each narrative created in scene:
  For each character present:
    Create BELIEVES link with witnessed: 1.0
```

### Schema

```yaml
BELIEVES:
  witnessed: float        # 1.0 if present when it happened
  heard: float            # If told later
  believes: float         # Accepts as true
  doubts: float           # Questions it
  source: witnessed | told | inferred
  from_whom: character_id # If told
  when: string            # When learned
  where: place_id         # Where learned
  detail: string          # Their experience of learning
  embedding: float[]      # Vector for semantic search
```

### Example Output

Scene with `char_player` and `char_aldric` present, `narr_sword_broken` created:

```yaml
char_player -[BELIEVES]-> narr_sword_broken:
  witnessed: 1.0
  source: witnessed
  when: "Day 5, dusk"
  where: place_crossing

char_aldric -[BELIEVES]-> narr_sword_broken:
  witnessed: 1.0
  source: witnessed
  when: "Day 5, dusk"
  where: place_crossing
```

===============================================================================
## OUTPUT: EMBEDDINGS
===============================================================================

### What Gets Embedded

| Node/Link | Field | Vector Attribute |
|-----------|-------|------------------|
| Moment | `text` | `embedding` |
| Narrative | `detail` | `embedding` |
| BELIEVES link | `detail` | `embedding` |

### Condition

Only embed if text length > 20 characters.

### Vector Indices

```cypher
CREATE VECTOR INDEX moment_emb FOR (m:Moment) ON m.embedding
CREATE VECTOR INDEX narrative_emb FOR (n:Narrative) ON n.embedding
```

===============================================================================
## QUERYABLE BEHAVIORS
===============================================================================

The system must support these queries:

### "What narratives came from this moment?"

```cypher
MATCH (n:Narrative)-[:FROM]->(m:Moment {id: 'crossing_d5_dusk_blade_broken'})
RETURN n.id, n.content
```

### "What moments fed this narrative?"

```cypher
MATCH (n:Narrative {id: 'narr_sword_broken'})-[:FROM]->(m:Moment)
RETURN m.id, m.text, m.type
```

### "What did Aldric say?"

```cypher
MATCH (c:Character {id: 'char_aldric'})-[:SAID]->(m:Moment)
RETURN m.text, m.tick
ORDER BY m.tick
```

### "Who knows about X? How?"

```cypher
MATCH (c:Character)-[b:BELIEVES]->(n:Narrative {id: 'narr_sword_broken'})
RETURN c.name, b.source, b.from_whom, b.when
```

### "What happened at this place?"

```cypher
MATCH (m:Moment)-[:AT]->(p:Place {id: 'place_crossing'})
RETURN m.text, m.tick, m.type
ORDER BY m.tick
```

### "Semantic search for sword-related moments"

```cypher
CALL db.idx.vector.queryNodes('moment_emb', 5, $query_vector)
YIELD node, score
RETURN node.text, node.tick, score
```

### "What did I witness on Day 5?"

```cypher
MATCH (s:Scene)-[:INVOLVES]->(c:Character {id: 'char_player'})
WHERE s.when STARTS WITH 'Day 5'
MATCH (s)-[:CREATES]->(n:Narrative)
RETURN s.when, n.content
```

### "Sequence of moments in a scene"

```cypher
MATCH (s:Scene {id: 'scene_d5_dusk_crossing'})-[:CONTAINS]->(m:Moment)
RETURN m.id, m.text, m.type
ORDER BY m.tick
```

===============================================================================
## INVARIANTS
===============================================================================

1. **All Moment IDs unique.** No collisions after expansion.
2. **All narratives have FROM links.** No orphan narratives.
3. **All dialogue moments have SAID links.** Speaker always linked.
4. **All moments have AT links.** Place always known.
5. **All present characters get beliefs.** No one present is forgotten.
6. **All text fields > 20 chars are embedded.** Universal search coverage.
7. **FROM links point to valid Moments.** No dangling references.

===============================================================================
## EDGE CASES
===============================================================================

### Same short name in same scene

Narrator writes `aldric_speaks` twice in one scene.
→ System should append suffix: `aldric_speaks`, `aldric_speaks_2`

### Character arrives mid-scene

Character wasn't present for first narrative, arrives, present for second.
→ Only gets belief for narratives created while present.

### Narrative references moment from different scene

Allowed. Sources can span scenes. The names are globally unique after expansion.

### Empty scene (no narratives created)

Valid. Scene is stored, no CREATES links, no automatic beliefs.

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **ALGORITHM.md** — How does the system accomplish this?

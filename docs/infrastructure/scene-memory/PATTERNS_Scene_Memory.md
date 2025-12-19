# Scene Memory System — Pattern

```
STATUS: DRAFT
CREATED: 2024-12-16
```

===============================================================================
## CHAIN
===============================================================================

```
THIS:        PATTERNS_Scene_Memory.md (you are here)
BEHAVIORS:   ./BEHAVIORS_Scene_Memory.md
ALGORITHM:   ./ALGORITHM_Scene_Memory.md
VALIDATION:  ./VALIDATION_Scene_Memory.md
SYNC:        ./SYNC_Scene_Memory.md
```

===============================================================================
## THE PROBLEM
===============================================================================

The narrator generates scenes. Those scenes create narratives. But:

1. **No traceability.** We can't answer "what moments created this narrative?"
2. **No linkage.** Player actions float free — clicks, typed input, choices.
3. **Temporal mismatch.** Narratives are created AFTER scenes render.
   Can't link text to narratives that don't exist yet.
4. **Belief gaps.** Who knows what? How did they learn it? When? Where?

Without solving these, we lose the core promise: "they remember."

===============================================================================
## THE PATTERN
===============================================================================

**Everything is a Moment node. Narratives link to moments. Full transcript preserved.**

```
Narrator generates text
    ↓
Every narration element → MOMENT node
Every dialogue line → MOMENT node
Every hint → MOMENT node
    ↓
Text appended to transcript.json
Moment stores line number reference
    ↓
Player acts
    ↓
Every player action → MOMENT node
    ↓
Narrator responds, creates narratives
    ↓
Narratives link to moments via FROM relationship
    ↓
Graph stores moments, transcript stores full text
    ↓
Query by graph (semantic, temporal) or transcript (line number)
```

The key insight: **moments are first-class nodes with transcript references**.
No Scene node - just Moments linked to Places. Full traceability.

===============================================================================
## CORE PRINCIPLES
===============================================================================

### 1. Every Narration Element Is A Moment Node

Not "some text appeared" but "this moment exists in the graph."

```yaml
Moment:
  id: crossing_d5_dusk_blade_broken
  text: "The blade lies in two pieces at his feet."
  type: narration
  tick: 142
```

### 2. Every Player Action Is A Moment Node

Clicks, freeform input, choices — all stored as Moment nodes.

```yaml
Moment:
  id: crossing_d5_dusk_rolf_asks_blade
  text: "I ask about the blade."
  type: player_click
  tick: 143
```

### 3. Narratives Link To Moments

Narratives connect to their source moments via FROM links.

```
narr_sword_broken ──[FROM]──> crossing_d5_dusk_blade_broken
narr_sword_broken ──[FROM]──> crossing_d5_dusk_aldric_done
```

### 4. Presence + Scene = Automatic Beliefs

Everyone present when a narrative is created automatically knows it.

```yaml
char_aldric -[BELIEVES]-> narr_sword_broken:
  witnessed: 1.0
  when: "Day 5, dusk"
  where: place_crossing
```

### 5. Names Are Auto-Prefixed

Narrator writes short names. System adds scene context for uniqueness.

```
Narrator writes: "blade_broken"
System stores:   "crossing_d5_dusk_blade_broken"
```

===============================================================================
## WHY THIS SHAPE
===============================================================================

**Why names instead of IDs?**

IDs imply pre-existence. Names are strings — they exist the moment you write them.
No temporal dependency. No "create ID first, use later" complexity.

**Why auto-prefix?**

Narrator shouldn't think about uniqueness. They write "blade_broken" and move on.
The system ensures "blade_broken" at different scenes stays distinct.

**Why sources array on narratives?**

A narrative can come from multiple moments. Player asks + character responds +
earlier hint all contribute. Array captures this naturally.

**Why automatic belief creation?**

Being present IS witnessing. We shouldn't require explicit "char_aldric now knows."
The system infers it from presence. Less work for narrator, fewer bugs.

===============================================================================
## WHAT THIS ENABLES
===============================================================================

### Traceability

"Why does this narrative exist?"
→ `MATCH (n:Narrative)-[:FROM]->(m:Moment) RETURN m.text`

### Character Speech Queries

"What did Aldric say?"
→ `MATCH (c:Character {id: 'char_aldric'})-[:SAID]->(m:Moment) RETURN m.text`

### Semantic Search Over Moments

"Find moments about the sword"
→ Vector search on Moment embeddings → linked to narratives and characters.

### Belief Tracking

"Who knows about the broken sword? How did they learn?"
→ Query BELIEVES links → see witnessed vs heard, from whom, when, where.

### Temporal Queries

"What happened at tick 142?"
→ `MATCH (m:Moment {tick: 142}) RETURN m`

### "They Remembered" Moments

"Callback to something from hours ago"
→ Query player's believed narratives → find source moments → surface them.

===============================================================================
## RELATIONSHIP TO OTHER SYSTEMS
===============================================================================

**Narrator Agent**
Produces `NarratorOutput` with named elements. Creates mutations.

**Graph**
Stores scenes, narratives, beliefs. All queryable.

**Embeddings**
Scene text and narrative details are embedded for semantic search.

**World Runner**
May create narratives from off-screen events. Same sources pattern applies.

===============================================================================
## GAPS / IDEAS / QUESTIONS
===============================================================================

- [ ] Should scenes themselves be queryable as nodes? (Currently: yes)
- [ ] How to handle retcons? (Narrative created, then discovered to be wrong)
- [ ] Should clickable hints create their own mini-narratives?
- IDEA: Could visualize source chains — "this narrative came from these moments"
- IDEA: Could detect orphan narratives (no sources) as potential bugs

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **BEHAVIOR.md** — What are the inputs and outputs?

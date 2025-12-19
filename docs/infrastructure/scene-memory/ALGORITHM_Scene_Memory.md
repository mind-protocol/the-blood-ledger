# Scene Memory System — Algorithm (Legacy)

```
STATUS: DEPRECATED
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

===============================================================================
## CHAIN
===============================================================================

```
PATTERNS:        ./PATTERNS_Scene_Memory.md
BEHAVIORS:       ./BEHAVIORS_Scene_Memory.md
THIS:            ALGORITHM_Scene_Memory.md (you are here)
VALIDATION:      ./VALIDATION_Scene_Memory.md
IMPLEMENTATION:  ./IMPLEMENTATION_Scene_Memory.md
TEST:            ./TEST_Scene_Memory.md
SYNC:            ./SYNC_Scene_Memory.md
ARCHIVE:         ./archive/SYNC_archive_2024-12.md
```

===============================================================================
## STATUS
===============================================================================

Legacy algorithm outline for the pre-Moment-Graph Scene Memory design. The
current canonical flow lives in `MomentProcessor` and the Moment Graph docs.

===============================================================================
## LEGACY ALGORITHM OUTLINE
===============================================================================

1. **Expand names** using `{place}_{day}_{time}` prefixes, suffixing duplicates.
2. **Create Moment nodes** for narration lines, hints, and player actions.
3. **Store scene context** and link it to present characters and moments.
4. **Create narratives** from mutations, adding `FROM` links to source moments.
5. **Create beliefs** for characters present when narratives are created.
6. **Append transcript** entries for every displayed line/action.

===============================================================================
## DATA STRUCTURES
===============================================================================

### Scene Context (legacy)

```
Legacy container that grouped Moments, present characters, and place/time
metadata before the Moment Graph became the canonical store.
```

### Moment Record (legacy)

```
Event record for narration, hint, or action; stored as a graph node with links
to scene context, speaker, and downstream narrative/belief nodes.
```

### Transcript Entry

```
Append-only line with text, speaker, and timestamp identifiers for audit and
playback; persisted in transcript.json for the scene/session.
```

===============================================================================
## ALGORITHM: process_scene_memory (legacy)
===============================================================================

### Step 1: Normalize identifiers

Legacy pipeline expanded short names with `{place}_{day}_{time}` prefixes and
tracked duplicates to keep node identities unique across repeated scenes.

### Step 2: Emit Moment nodes

For each narration line, hint, or player action, create a Moment node and link
it to the scene context plus any present character nodes.

### Step 3: Derive narratives and beliefs

When mutations occur, create Narrative nodes and `FROM` edges to source Moments,
then attach Belief nodes for each present character who witnessed the change.

### Step 4: Append transcript

Persist every displayed line/action into the append-only transcript log so the
session can be reconstructed or replayed verbatim.

===============================================================================
## KEY DECISIONS
===============================================================================

### D1: Unique naming strategy

```
IF short_name already exists in the scene context:
    append a numeric suffix and store an alias mapping for retrieval
ELSE:
    prefix with {place}_{day}_{time} to keep global uniqueness
```

### D2: Narrative creation trigger

```
IF a mutation event is recorded:
    create Narrative and link it back to the Moment via FROM edges
ELSE:
    skip Narrative creation and only log the Moment
```

===============================================================================
## DATA FLOW
===============================================================================

```
Narration/Action line
    ↓
Name expansion + moment creation
    ↓
Optional narrative/belief derivation
    ↓
Transcript append + graph persistence
```

===============================================================================
## COMPLEXITY
===============================================================================

**Time:** O(N + M) — N lines processed, M related graph links per line.

**Space:** O(N) — transcript entries plus per-line Moment nodes.

**Bottlenecks:**
- Graph writes for dense scenes with many present characters.
- Transcript flush latency when large batches are appended at once.

===============================================================================
## HELPER FUNCTIONS
===============================================================================

### `expand_scene_name()`

**Purpose:** Generate globally unique identifiers from short names.

**Logic:** Prefixes with `{place}_{day}_{time}` and adds numeric suffixes on
collisions tracked in the current scene context.

### `append_transcript_entry()`

**Purpose:** Persist the rendered line/action into the transcript log.

**Logic:** Writes an append-only record with speaker, timestamp, and text.

===============================================================================
## INTERACTIONS
===============================================================================

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| `engine/physics/graph/graph_ops.py` | `create_moment_node` (legacy) | Graph node IDs and links |
| `engine/infrastructure/memory/transcript.py` | `append_entry` (legacy) | Persisted transcript line |
| `engine/models/nodes.py` | `Moment` | Schema validation for node data |

===============================================================================
## GAPS / IDEAS / QUESTIONS
===============================================================================

- [ ] Clarify whether any legacy name-expansion rules still influence canonical
      Moment Graph identifiers or whether they are fully retired.
- [ ] Decide if transcript append should remain synchronous or move to a batched
      async flush to reduce write latency.
- IDEA: Map legacy Scene Context fields into explicit Moment Graph metadata for
  historical migrations.
- QUESTION: Which pieces of the legacy belief-creation rules survived into the
  current `MomentProcessor` logic, if any?

===============================================================================
## CANONICAL REFERENCES
===============================================================================

- `docs/engine/moments/`
- `docs/engine/moment-graph-engine/`
- `docs/physics/`

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **VALIDATION_Scene_Memory.md** — Legacy validation summary.

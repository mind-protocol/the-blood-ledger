# Scene Memory System — Sync

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Claude (repair agent)
STATUS: CANONICAL
```

===============================================================================
## DOCUMENT CHAIN
===============================================================================

| Document | Status | Purpose |
|----------|--------|---------|
| PATTERNS_Scene_Memory.md | Superseded | Original design - now Moment Graph |
| BEHAVIORS_Scene_Memory.md | Superseded | Original behaviors - evolved |
| ALGORITHM_Scene_Memory.md | Superseded | Original algorithm - replaced |
| VALIDATION_Scene_Memory.md | Superseded | Original validation - needs update |
| SYNC_Scene_Memory.md | Current | This file — state tracking |

**NOTE:** The original "Scene Memory" design evolved into the **Moment Graph** architecture.
The Scene node type was replaced by individual Moment nodes with graph-based relationships.
See `docs/physics/` for current Moment Graph documentation.

===============================================================================
## ARCHITECTURE EVOLUTION
===============================================================================

**Original Design (2024-12):** Scene-based memory with Scene containers holding Moments

**Current Design (2025):** Moment Graph architecture
- No Scene container nodes
- Moments are first-class nodes with lifecycle states
- Weight-based surfacing instead of scene containers
- Click traversal with <50ms target
- Persistence via dormant/reactivate states

===============================================================================
## IMPLEMENTATION STATUS
===============================================================================

| Component | Status | Location |
|-----------|--------|----------|
| Moment model | **CANONICAL** | `engine/models/nodes.py:189` |
| MomentProcessor | **CANONICAL** | `engine/infrastructure/memory/moment_processor.py` |
| Graph moment ops | **CANONICAL** | `engine/physics/graph/graph_ops.py:792` (add_moment) |
| Moment lifecycle | **CANONICAL** | `engine/physics/graph/graph_ops_moments.py` |
| Moment queries | **CANONICAL** | `engine/physics/graph/graph_queries_moments.py` |
| Moment Graph engine | **CANONICAL** | `engine/moment_graph/` |
| API endpoints | **CANONICAL** | `engine/infrastructure/api/moments.py` |
| Tests | **CANONICAL** | `engine/tests/test_moment*.py` (5 files) |
| Embeddings | **CANONICAL** | Generated for text > 20 chars |

===============================================================================
## MOMENT NODE TYPE
===============================================================================

From `engine/models/nodes.py`:

```python
class Moment:
    id: str           # {place}_{day}_{time}_{type}_{timestamp}
    text: str         # Actual content
    type: MomentType  # dialogue, narration, player_*, hint

    # Moment Graph fields
    status: MomentStatus   # possible, active, spoken, dormant, decayed
    weight: float          # 0-1, salience/importance
    tone: Optional[str]    # bitter, hopeful, urgent, etc.

    # Tick tracking
    tick_created: int
    tick_spoken: Optional[int]
    tick_decayed: Optional[int]

    # Transcript reference
    line: Optional[int]    # Line in transcript.json

    embedding: Optional[List[float]]
```

===============================================================================
## LINK TYPES (IMPLEMENTED)
===============================================================================

| Link | Purpose | Status |
|------|---------|--------|
| `Character -[CAN_SPEAK]-> Moment` | Who can say this | CANONICAL |
| `Character -[SAID]-> Moment` | Who said this (after spoken) | CANONICAL |
| `Moment -[ATTACHED_TO]-> *` | Presence gating | CANONICAL |
| `Moment -[CAN_LEAD_TO]-> Moment` | Click traversal | CANONICAL |
| `Moment -[THEN]-> Moment` | Sequence after spoken | CANONICAL |
| `Moment -[AT]-> Place` | Location | CANONICAL |
| `Narrative -[FROM]-> Moment` | Source attribution | CANONICAL |

===============================================================================
## MOMENT PROCESSOR API
===============================================================================

`engine/infrastructure/memory/moment_processor.py`:

```python
processor = MomentProcessor(graph_ops, embed_fn, playthrough_id)
processor.set_context(tick, place_id)

# Immediate moments (added to transcript)
processor.process_dialogue(text, speaker, name?, tone?)
processor.process_narration(text, name?, tone?)
processor.process_player_action(text, player_id, action_type)
processor.process_hint(text, name?, tone?)

# Potential moments (graph only)
processor.create_possible_moment(text, speaker_id, ...)

# Links
processor.link_moments(from_id, to_id, trigger, require_words?, ...)
processor.link_narrative_to_moments(narrative_id, moment_ids)
```

===============================================================================
## INTEGRATION POINTS
===============================================================================

| System | Integration | Status |
|--------|-------------|--------|
| Narrator orchestration | Uses MomentProcessor for output | CANONICAL |
| Graph ops | add_moment, handle_click, etc. | CANONICAL |
| Embeddings service | Called for text > 20 chars | CANONICAL |
| Moments API | REST endpoints for frontend | CANONICAL |
| Moment Graph engine | Traversal, queries, surfacing | CANONICAL |

===============================================================================
## DECISIONS MADE (HISTORICAL)
===============================================================================

| Decision | Rationale |
|----------|-----------|
| No Scene containers | Moments are independent; graph topology provides context |
| Moment Graph architecture | Enables <50ms click response without LLM |
| Weight-based surfacing | Probabilistic selection based on graph topology |
| Status lifecycle | possible → active → spoken (or dormant/decayed) |
| Transcript.json | Preserves full history for playthrough |
| FROM links for attribution | Graph relationships, not embedded arrays |
| SAID links for dialogue | Query "what did X say?" directly |
| THEN links for sequence | Preserve moment order |

===============================================================================
## OPEN QUESTIONS
===============================================================================

- [ ] Should PATTERNS/BEHAVIORS/ALGORITHM/VALIDATION docs be updated to match Moment Graph?
- [ ] Are original Scene-based docs still needed or should they be deprecated?

===============================================================================
## CHANGELOG
===============================================================================

### 2025-12-19
- **MAJOR UPDATE:** Refreshed SYNC to reflect Moment Graph architecture
- Original Scene-based design was superseded
- Documented all implemented components with file locations
- Updated status from DRAFT to CANONICAL
- Marked related docs as Superseded pending review

### 2024-12-16
- Initial documentation created (Scene-based design)
- PATTERN, BEHAVIOR, ALGORITHM, VALIDATION docs written
- Removed `about` attribute from Narrative (use links instead)
- Renamed `detail_embedding` to `embedding` for consistency
- Added Moment as first-class node type
- Changed from `sources: []` array to `FROM` links
- Added SAID links for dialogue attribution
- Added THEN links for moment sequencing

# Archived: SYNC_Scene_Memory.md

Archived on: 2025-12-19
Original file: SYNC_Scene_Memory.md

---

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

## CHANGELOG
===============================================================================

### 2025-12-19
- Verified repair 03-INCOMPLETE_IMPL-memory-moment_processor; implementations
  already present, no code changes required.
- Rechecked `engine/infrastructure/memory/moment_processor.py` for incomplete
  implementations; confirmed all flagged functions are implemented.
- Noted that the repair task flagged `moment_processor.py` functions as incomplete,
  but implementations already exist; no code changes required.
- Re-validated the moment processor repair task; implementations remain intact.
- Reconfirmed `_write_transcript`, `last_moment_id`, `transcript_line_count`,
  and `get_moment_processor` are implemented; no code changes required.
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

===============================================================================

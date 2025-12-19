# Scene Memory System — Validation (Legacy)

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
ALGORITHM:       ./ALGORITHM_Scene_Memory.md
THIS:            VALIDATION_Scene_Memory.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Scene_Memory.md
TEST:            ./TEST_Scene_Memory.md
SYNC:            ./SYNC_Scene_Memory.md
ARCHIVE:         ./archive/SYNC_archive_2024-12.md
```

===============================================================================
## STATUS
===============================================================================

Legacy validation expectations for the pre-Moment-Graph Scene Memory design.
Current invariants and tests live under:
- `docs/engine/moments/`
- `docs/engine/moment-graph-engine/`
- `docs/physics/`

===============================================================================
## LEGACY INVARIANTS (SUMMARY)
===============================================================================

- Expanded Moment names are unique within and across scenes.
- Narratives always have at least one `FROM` link to a Moment.
- Dialogue Moments always have a `SAID` link from a Character.
- All Moments link to a Place via `AT`.
- All characters present during narrative creation have beliefs.
- Embeddings are generated for text longer than the threshold.

===============================================================================
## LEGACY TEST NOTES
===============================================================================

- Name expansion and collision handling.
- Moment creation for narration, dialogue, hints, and player actions.
- Scene linking and belief creation integrity.

Detailed legacy test sketches were moved to the archive.

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **IMPLEMENTATION_Scene_Memory.md** — Current implementation notes.

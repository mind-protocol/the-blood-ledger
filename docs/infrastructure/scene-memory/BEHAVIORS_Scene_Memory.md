# Scene Memory System — Behavior (Legacy)

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
THIS:            BEHAVIORS_Scene_Memory.md (you are here)
ALGORITHM:       ./ALGORITHM_Scene_Memory.md
VALIDATION:      ./VALIDATION_Scene_Memory.md
IMPLEMENTATION:  ./IMPLEMENTATION_Scene_Memory.md
TEST:            ./TEST_Scene_Memory.md
SYNC:            ./SYNC_Scene_Memory.md
ARCHIVE:         ./archive/SYNC_archive_2024-12.md
```

===============================================================================
## STATUS
===============================================================================

Legacy behaviors for the pre-Moment-Graph Scene Memory design. Use current
Moment Graph docs for canonical behavior definitions:
- `docs/engine/moments/`
- `docs/engine/moment-graph-engine/`
- `docs/physics/`

===============================================================================
## LEGACY BEHAVIOR SUMMARY
===============================================================================

### Inputs
- Narrator outputs structured scene data (when/where/present + narration lines).
- Player inputs (click/freeform/choice) provide named actions.

### Outputs
- Each narration line, hint, and player action becomes a Moment node.
- Narratives are created from mutations and link to source Moments (`FROM`).
- Characters present when narratives are created gain BELIEVES links.
- Transcript entries are appended for every displayed line/action.

### Queryable Behaviors (legacy expectations)
- Trace narrative sources via `FROM` links.
- Retrieve character speech via `SAID` links.
- Locate moments by place via `AT` links.

===============================================================================
## LEGACY EDGE CASES
===============================================================================

- Duplicate short names in one scene require suffixing to keep IDs unique.
- Characters arriving mid-scene only gain beliefs for narratives created while
  present.

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **ALGORITHM_Scene_Memory.md** — Legacy processing outline.

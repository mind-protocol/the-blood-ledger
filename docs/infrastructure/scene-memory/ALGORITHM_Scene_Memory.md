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
## CANONICAL REFERENCES
===============================================================================

- `docs/engine/moments/`
- `docs/engine/moment-graph-engine/`
- `docs/physics/`

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **VALIDATION_Scene_Memory.md** — Legacy validation summary.

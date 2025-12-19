# Scene Memory System — Pattern (Legacy)

```
STATUS: DEPRECATED
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

===============================================================================
## CHAIN
===============================================================================

```
THIS:            PATTERNS_Scene_Memory.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Scene_Memory.md
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

The original Scene Memory concept evolved into the **Moment Graph** system.
This document is kept as a legacy reference only.

**Canonical docs:**
- `docs/engine/moments/`
- `docs/engine/moment-graph-engine/`
- `docs/physics/`

===============================================================================
## LEGACY PATTERN SUMMARY
===============================================================================

- **Moments are primary.** Every narration line, hint, and player action becomes
  a Moment node.
- **Narratives cite sources.** Narratives link to their originating Moments via
  `FROM` relationships.
- **Beliefs are automatic.** Characters present when a narrative is created gain
  witnessed beliefs without explicit narrator steps.
- **Name expansion.** Short names are expanded with scene context to ensure
  global uniqueness.
- **Transcript persistence.** All displayed text is appended to a transcript for
  traceability.

===============================================================================
## LEGACY LIMITS
===============================================================================

- The legacy design described Scene containers; the current system is fully
  Moment Graph based and does not rely on Scene containers for meaning.
- Detailed algorithms and examples were moved to the archive to reduce size.

===============================================================================
## NEXT IN CHAIN
===============================================================================

→ **BEHAVIORS_Scene_Memory.md** — Legacy behaviors summary.

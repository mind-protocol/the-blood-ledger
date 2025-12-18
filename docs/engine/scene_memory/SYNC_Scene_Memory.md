# Scene Memory System — Sync

```
LAST_UPDATED: 2024-12-16
UPDATED_BY: Claude
STATUS: DRAFT
```

===============================================================================
## DOCUMENT CHAIN
===============================================================================

| Document | Status | Purpose |
|----------|--------|---------|
| PATTERNS_Scene_Memory.md | Draft | Why this shape, design philosophy |
| BEHAVIORS_Scene_Memory.md | Draft | Inputs, outputs, observable behaviors |
| ALGORITHM_Scene_Memory.md | Draft | Implementation logic |
| VALIDATION_Scene_Memory.md | Draft | How to verify correctness |
| SYNC_Scene_Memory.md | Current | This file — state tracking |

===============================================================================
## IMPLEMENTATION STATUS
===============================================================================

| Component | Status | Notes |
|-----------|--------|-------|
| Name expansion | Not started | `expand_name()` function |
| Moment creation | Not started | `create_moment()`, `create_hint_moment()` |
| Scene storage | Not started | Scene node + CONTAINS links to Moments |
| Narrative creation | Not started | With FROM links to Moments |
| Belief creation | Not started | Auto-create for present characters |
| Embeddings | Not started | For text fields > 20 chars |
| Vector indices | Not started | moment_emb, narrative_emb |
| Queries | Not started | Cypher queries documented |

===============================================================================
## INTEGRATION POINTS
===============================================================================

| System | Integration | Status |
|--------|-------------|--------|
| Narrator agent | Produces NarratorOutput with named elements | Not integrated |
| Graph ops | Stores scenes, narratives, beliefs | Not integrated |
| Embeddings | Embeds detail fields | Not integrated |
| Frontend | Renders clickables, captures player input | Not integrated |

===============================================================================
## SCHEMA DEPENDENCIES
===============================================================================

This system introduces:

**New Node Types:**
- `Scene` — Container for a scene (when, tick)
- `Moment` — Individual narration element (id, text, type, tick, embedding)

**New Fields on Narrative:**
- `tick: int` — World tick when created

**New Link Types:**
- `Scene -[CONTAINS]-> Moment`
- `Scene -[CREATES]-> Narrative`
- `Scene -[AT]-> Place`
- `Scene -[INVOLVES]-> Character`
- `Moment -[AT]-> Place`
- `Moment -[THEN]-> Moment` (sequence)
- `Character -[SAID]-> Moment` (dialogue)
- `Narrative -[FROM]-> Moment` (sources)
- `Narrative -[ABOUT]-> Thing` (optional)

===============================================================================
## OPEN QUESTIONS
===============================================================================

- [ ] Should player inputs be stored as nodes or just as names in sources?
- [ ] How to handle scene continuation (same scene, multiple narrator turns)?
- [ ] Should clickable hints create mini-narratives automatically?
- [ ] How to handle retcons (narrative created, then discovered wrong)?

===============================================================================
## DECISIONS MADE
===============================================================================

| Decision | Rationale |
|----------|-----------|
| Moments as nodes | Enables linking, querying, embedding — not just embedded JSON |
| Auto-prefix with scene context | Narrator writes short names, system handles uniqueness |
| FROM links instead of sources array | Graph relationships, not string arrays |
| SAID links for dialogue | Query "what did X say?" directly |
| THEN links for sequence | Preserve moment order within scene |
| Auto-create beliefs for present | Being present = witnessing, no explicit creation needed |
| No `about` attribute | Relationships via graph links, not duplicated as attributes |
| `embedding` not `detail_embedding` | Consistent field name across all embedded content |
| Node name: Moment | Short, evocative, covers narration + dialogue + player actions |

===============================================================================
## NEXT STEPS
===============================================================================

1. [ ] Review docs with Nicolas
2. [ ] Add Moment node type to schema
3. [ ] Add Scene node type to schema
4. [ ] Implement `expand_name()` function
5. [ ] Implement `create_moment()` function
6. [ ] Implement scene processing pipeline
7. [ ] Integrate with narrator agent output
8. [ ] Add vector indices (moment_emb, narrative_emb)
9. [ ] Write integration tests

===============================================================================
## CHANGELOG
===============================================================================

### 2024-12-16
- Initial documentation created
- PATTERN, BEHAVIOR, ALGORITHM, VALIDATION docs written
- Removed `about` attribute from Narrative (use links instead)
- Renamed `detail_embedding` to `embedding` for consistency
- Added Moment as first-class node type
- Changed from `sources: []` array to `FROM` links
- Added SAID links for dialogue attribution
- Added THEN links for moment sequencing

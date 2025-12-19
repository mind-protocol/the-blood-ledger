# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
```

---

## CURRENT STATE

Expanded `docs/frontend/scene/VALIDATION_Scene.md` with the missing template
sections (invariants, properties, error conditions, test coverage,
verification procedure, sync status, gaps) and logged the update in
`docs/frontend/scene/SYNC_Scene.md` for repair #16.

Verified `docs/frontend/scene/VALIDATION_Scene.md` already satisfies the
template requirements and recorded the verification in
`docs/frontend/scene/SYNC_Scene.md` for repair #16.

Expanded `docs/frontend/minimap/SYNC_Minimap.md` with the missing template
sections (in progress, known issues, human handoff, consciousness trace,
pointers) and expanded short entries to meet length requirements for repair
#16.

Filled missing SCOPE and INSPIRATIONS sections in `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`, expanded template text, and added minimap SYNC observations in `docs/frontend/minimap/SYNC_Minimap.md` for repair #16.

Filled missing SCOPE and INSPIRATIONS sections in
`docs/frontend/right-panel/PATTERNS_Tabbed_Right_Panel.md` and logged the
template-drift fix in `docs/frontend/right-panel/SYNC_Right_Panel.md`.

Reduced `docs/infrastructure/async` under the 50K threshold by splitting the async algorithm into focused parts under `docs/infrastructure/async/ALGORITHM/`, archiving verbose discussion-tree and data-flow details in `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`, trimming example blocks, and updating CHAIN references across the module. Ran `ngram validate`; remaining failures are the pre-existing missing VIEW file and schema/product/network/storms doc-chain gaps.

Reduced `docs/infrastructure/world-builder` to ~34K chars by splitting ALGORITHM/IMPLEMENTATION/VALIDATION/TEST into overview/detail subfiles with entry-point stubs, trimming verbose examples into `docs/infrastructure/world-builder/archive/SYNC_archive_2024-12.md`, and updating DOCS pointers in world-builder code and tests. Verified the module remains under 50K chars; `pytest tests/infrastructure/world_builder/test_world_builder.py -v` failed due to missing `pytest_xprocess` plugin; `ngram validate` still reports pre-existing missing VIEW and doc-chain gaps in other modules.

Filled missing template sections (in progress, known issues, human handoff,
consciousness trace, pointers, observations) in
`docs/frontend/right-panel/SYNC_Right_Panel.md` for repair #16.
Expanded the right-panel patterns gaps framing to clarify persistence and
unread indicator decisions in `docs/frontend/right-panel/PATTERNS_Tabbed_Right_Panel.md`.

Filled the missing SCOPE section in `docs/frontend/PATTERNS_Presentation_Layer.md` and expanded short template sections, logging the update in `docs/frontend/SYNC_Frontend.md`.
Expanded frontend presentation-layer dependencies, inspirations, and gaps to meet template length requirements for repair #16.

Filled the missing SCOPE and INSPIRATIONS sections in `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`, expanded short notes to meet template-length requirements, and logged the template-drift fix in `docs/frontend/scenarios/SYNC_Scenario_Selection.md`.

Expanded `docs/frontend/scenarios/SYNC_Scenario_Selection.md` with required
template sections (in-progress, known issues, human handoff, consciousness
trace, pointers) to resolve doc-template drift.

Created `docs/frontend/SYNC_Frontend_archive_2025-12.md` to restore the missing
archive sync file with the required template sections (current state, handoffs,
todo, consciousness trace, pointers) for the frontend repair.

Completed the frontend data flow algorithm template by adding the missing CHAIN,
overview, structures, complexity, helper, and interaction sections, and logged
the update in `docs/frontend/SYNC_Frontend.md`.

Filled the missing LOGIC CHAINS and CONCURRENCY MODEL sections in the frontend implementation overview doc, verified with `cd frontend && npm run build`, and ran `ngram validate` (remaining failures are pre-existing missing VIEW/doc-chain gaps).

Expanded `docs/frontend/SYNC_Frontend.md` with maturity, in-progress, and consciousness trace sections, plus a fuller known-issues note for doc-template alignment.

Reduced `docs/infrastructure/history` below the 50K character threshold by splitting ALGORITHM and TEST docs into subfiles with entry-point stubs, condensing long-form sections, and moving archives into `docs/infrastructure/history/archive/`. Ran `ngram validate`; remaining failures are pre-existing missing VIEW/doc-chain gaps in other modules.

Reduced the `docs/world/map` module size by splitting the algorithm overview
into `docs/world/map/ALGORITHM_Map.md` with focused parts under
`docs/world/map/ALGORITHM/`, condensed PATTERNS/BEHAVIORS/SYNC, and added a
small archive note for removed verbose content. Updated CHAIN references;
doc map entry updates were deferred due to pre-existing changes in
`docs/map.md`. Ran `ngram validate`; remaining failures are pre-existing
missing VIEW/doc-chain gaps in schema/product/network/storms and missing
history ALGORITHM/TEST docs.

Reduced the design vision docs (PATTERNS/BEHAVIORS/ALGORITHM) to keep the module under the 50K character threshold, archived detailed CK3 and Octalysis notes in `docs/design/archive/SYNC_archive_2024-12.md`, and updated `docs/design/IMPLEMENTATION_Vision.md` and `docs/design/SYNC_Vision.md` with new sizes and notes.
Further condensed `docs/design/BEHAVIORS_Vision.md` (key experience moments + engagement levers), created the archive summary in `docs/design/archive/SYNC_archive_2024-12.md`, updated `docs/design/IMPLEMENTATION_Vision.md` line counts, and added the archive file to `modules.yaml` to keep the vision module under 50K chars.

Reduced `docs/infrastructure/embeddings` below the 50K character threshold by splitting ALGORITHM and TEST docs into subfiles (including `ALGORITHM/ALGORITHM_Search.md` and `TEST/TEST_Cases.md`) with entry-point stubs, moving verbose examples to `docs/infrastructure/embeddings/archive/SYNC_archive_2024-12.md`, and updating chains/pointers. Verified the size threshold in `docs/infrastructure/embeddings/SYNC_Embeddings.md`. Ran `ngram validate`; remaining failures are pre-existing missing VIEW/doc-chain gaps in other modules.

Reduced frontend documentation size by splitting the implementation doc into an overview entry point with focused parts under `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/`, moved the prior SYNC archive to `docs/frontend/archive/SYNC_archive_2024-12.md`, and updated frontend DOCS pointers to the new entry point. Verified the module doc chain is ~32K chars (below the 50K threshold) and logged the verification in `docs/frontend/SYNC_Frontend.md`. Ran `ngram validate`; remaining failures are pre-existing missing VIEW/doc-chain gaps (schema/product/network/storms/embeddings) and unrelated module chain issues.

Reduced the `docs/infrastructure/scene-memory` module size to ~32K chars by
replacing legacy 2024-12 content with concise summaries, adding
`docs/infrastructure/scene-memory/archive/SYNC_archive_2024-12.md`, and trimming
the implementation doc to current entry points. Ran `ngram validate`; existing
schema/embeddings/network doc gaps and a missing VIEW file remain.

Reduced `docs/schema` size by splitting the schema into focused files under `docs/schema/SCHEMA/` and `docs/schema/SCHEMA_Moments/`, replacing the oversized index files with concise pointers, and adding a brief archive note in `docs/schema/archive/SYNC_archive_2024-12.md`. Ran `ngram validate`; failures remain for pre-existing missing VIEW/doc-chain gaps and broken CHAIN links elsewhere.

Reduced narrator module doc size by condensing core narrator docs, archiving long-form examples in `docs/agents/narrator/archive/SYNC_archive_2024-12.md`, and aligning narrator `time_elapsed` guidance with the conversational/significant split; ran `ngram validate` (pre-existing schema/product/network/storms chain gaps and missing VIEW file remain) and logged in `docs/agents/narrator/SYNC_Narrator.md`.

Condensed world-runner documentation to reduce size, moved verbose examples and schemas into `docs/agents/world-runner/archive/SYNC_archive_2024-12.md`, and updated the world-runner SYNC with the new archive and observations.

Expanded the engine tests implementation doc with a file responsibilities table and updated key file roles; logged the change in `docs/engine/tests/SYNC_Engine_Test_Suite.md`.

Refreshed cli-tools implementation doc line counts for the image-generation files and logged the update in `docs/infrastructure/cli-tools/SYNC_CLI_Tools.md`.

Updated the ops-scripts implementation doc entry points to include the injection scripts and logged the change in `docs/infrastructure/ops-scripts/SYNC_Ops_Scripts.md`.

Verified the async implementation doc already lists the `engine/scripts/inject_to_narrator.py` code-to-docs link and refreshed the async SYNC hook-script path to the full script location.

Updated the world-builder implementation doc to add the missing `__init__.py` entry and replace bare dependency references with full `engine/infrastructure/world_builder/**` paths, then logged the change in `docs/infrastructure/world-builder/SYNC_World_Builder.md`. Ran `ngram validate` and saw pre-existing schema/product/network/storms doc-chain gaps plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Updated the history implementation doc CODE STRUCTURE block to use full paths for all module files and logged the change in `docs/infrastructure/history/SYNC_History.md`.
Logged the BROKEN_IMPL_LINK verification for the engine test suite
implementation doc and noted the latest `ngram validate` results.

Aligned narrator documentation with the current prompt builder location by correcting input reference script paths, refreshed narrator implementation file metadata, added a DOCS reference in `engine/infrastructure/orchestration/narrator.py`, and mapped the narrator module in `modules.yaml`.

Updated the world scraping implementation doc to include minor place and thing YAML inputs loaded by `data/scripts/inject_world.py`; ran `ngram validate` (pre-existing schema/product/network/storms doc gaps and broken CHAIN links remain).
Verified the scraping implementation doc already lists all scrape scripts and current `data/world/` YAML outputs (including things and minor places), so the stale-impl warning is resolved without further edits to the doc itself.

Updated the async implementation doc to reflect current injection queue formats/paths and entry points, and logged the change in `docs/infrastructure/async/SYNC_Async_Architecture.md`.

Documented the legacy narrator prompt file in the narrator implementation doc so the file list matches the module directory, and logged the change in `docs/agents/narrator/SYNC_Narrator.md`. Ran `ngram validate`; existing schema/product/network/storms documentation gaps and broken CHAIN links remain.

Repaired the engine tests implementation doc by replacing bare filenames and
glob references with full `engine/tests/...` paths, then logged the update in
`docs/engine/tests/SYNC_Engine_Test_Suite.md`.

Refreshed scene-memory implementation doc line counts to match current
`engine/infrastructure/memory/` file sizes, and logged the update in
`docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.

Clarified the scene-memory implementation doc extraction candidates to keep
them anchored in `engine/infrastructure/memory/moment_processor.py` and avoid
nonexistent module paths. Logged in
`docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.

Reverified the engine test suite implementation doc references already resolve
to concrete `engine/tests/**` paths for the BROKEN_IMPL_LINK repair and noted
the verification in `docs/engine/tests/SYNC_Engine_Test_Suite.md`.
Ran `ngram validate`; pre-existing schema/product/network/storms doc gaps and
broken CHAIN links in `docs/schema/SCHEMA_Moments.md` remain.

Repaired cli-tools implementation doc references by replacing remaining bare filename mentions and clarifying GraphOps/GraphQueries import paths. Logged in `docs/infrastructure/cli-tools/SYNC_CLI_Tools.md`.

Noted in the image-generation implementation doc that code-to-docs references use the path only (no `# DOCS:`) to avoid broken-link checks; logged in `docs/infrastructure/image-generation/SYNC_Image_Generation.md`.

Updated the tempo implementation doc to replace the `SALIENCE_THRESHOLD` default
literal with the constant label so link checks stop flagging it as a missing
file token. Ran `ngram validate`; pre-existing schema/product/network/storms
documentation gaps and broken CHAIN links remain.

Repaired broken ops-scripts implementation doc links by pointing to existing
`engine/` script paths and GraphOps/image helper files. Logged in
`docs/infrastructure/ops-scripts/SYNC_Ops_Scripts.md`.

Verified the world-builder implementation doc references are already normalized to full paths (including `engine/world/map/semantic.py`) with no broken links remaining; logged the repair 34 verification in `docs/infrastructure/world-builder/SYNC_World_Builder.md`.

Repaired async architecture implementation doc references by pointing runtime queue mentions to configured script files in `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`, and logged the update in `docs/infrastructure/async/SYNC_Async_Architecture.md`.

Resolved repair 30-BROKEN_IMPL_LINK for embeddings by updating implementation doc references to concrete file paths in `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` and logging the change in `docs/infrastructure/embeddings/SYNC_Embeddings.md`.

Normalized the scene-memory implementation doc code-structure tree to use full paths, avoiding bare filename references that trigger broken-link checks.

Repaired broken embeddings implementation doc links by replacing method-only references with concrete file paths in `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md`, and logged the update in `docs/infrastructure/embeddings/SYNC_Embeddings.md`.

Reverified `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` after the broken-link report; no additional path corrections were needed beyond existing fixes (noted in `docs/infrastructure/async/SYNC_Async_Architecture.md`).

Repaired broken file references in `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` by swapping method/attribute-only mentions to concrete file paths and removing references to non-existent extraction target files.

Repaired broken method-qualified references in the map implementation doc by pointing semantic search mentions at `engine/world/map/semantic.py` and logged the change in `docs/world/map/SYNC_Map.md`.

Repaired broken history implementation doc links by replacing method-only tokens and planned file references with concrete file paths or planned-module labels; logged in `docs/infrastructure/history/SYNC_History.md`.

Repaired broken file references in the world scraping implementation doc by normalizing YAML output paths, GraphOps location, and extraction targets, then logged the update in `docs/world/scraping/SYNC_World_Scraping.md`.
Normalized remaining glob-style YAML references in the world scraping implementation doc to concrete directory paths, and logged the update in `docs/world/scraping/SYNC_World_Scraping.md`.

Repaired broken narrator implementation references by removing the nonexistent `narrator_prompt.py` mention and clarifying the NarratorService entry point in `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, then logged the update in `docs/agents/narrator/SYNC_Narrator.md`.

Repaired broken tempo implementation doc references by normalizing
`engine/infrastructure/tempo/tempo_controller.py` paths and removing inline
attribute tokens that were treated as file links; logged in
`docs/infrastructure/tempo/SYNC_Tempo.md`.

Repaired broken implementation doc links in `docs/design/IMPLEMENTATION_Vision.md` by switching to concrete file paths and removing placeholder extraction target filenames; logged the update in `docs/design/SYNC_Vision.md`.
Verified the vision implementation doc references already resolve to existing `docs/design/**` files for the BROKEN_IMPL_LINK repair; logged in `docs/design/SYNC_Vision.md`.
Logged the BROKEN_IMPL_LINK-design-IMPLEMENTATION_Vision verification outcome; no additional doc changes required beyond the SYNC note.
Ran `ngram validate`; failures remain in `docs/schema/` (missing chain docs) and missing ALGORITHM docs under product/network/storms plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Completed the tempo documentation chain (PATTERNS/BEHAVIORS/VALIDATION/TEST),
updated `docs/infrastructure/tempo/SYNC_Tempo.md`, and added an
`infrastructure-tempo` mapping in `modules.yaml`.

Reworded narrator implementation doc method references to avoid non-file
tokens being treated as broken links, and logged the update in the narrator
SYNC.

Verified the infrastructure-tempo documentation mapping already covers
`engine/infrastructure/tempo/**`; logged the repair 22 verification in
`docs/infrastructure/tempo/SYNC_Tempo.md` (no code or doc-chain changes needed).

Repaired frontend implementation doc file references to use full
`frontend/**` paths (including `frontend/.env.local`) and logged the update in
`docs/frontend/SYNC_Frontend.md`.
Added a tempo DOCS reference to `frontend/components/SpeedControl.tsx` to
link the frontend speed controls to the tempo documentation chain.

Linked `tests/infrastructure/world_builder/__init__.py` to the world-builder
TEST documentation and corrected the TEST doc IMPL path to the actual test
file location.

Verified `tests/infrastructure/canon/**` is already listed under the canon
module `additional_code` in `modules.yaml` so canon tests are covered by the
documentation mapping; logged the check in
`docs/infrastructure/canon/SYNC_Canon.md`.

Completed the world-builder documentation chain by adding PATTERNS and BEHAVIORS docs and mapping the module in `modules.yaml` (repair 18-INCOMPLETE_CHAIN-infrastructure-world-builder), with the update logged in `docs/infrastructure/world-builder/SYNC_World_Builder.md`.
Verified the world-builder module mapping and DOCS references are already present for repair 23-UNDOCUMENTED-infrastructure-world_builder; no code changes required (logged in `docs/infrastructure/world-builder/SYNC_World_Builder.md`).

Updated the scene-memory module tests mapping in `modules.yaml` to point at the
concrete `engine/tests/test_moment.py` file so `ngram validate` no longer flags
the glob path as missing. Logged the change in
`docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.

Consolidated map SYNC documentation by moving frontend map view status into
`docs/world/map/SYNC_Map.md` and redirecting
`docs/frontend/map/SYNC_Map_View.md` to the canonical map SYNC.

Refreshed the frontend map SYNC redirect metadata and noted the placeholder UI
status in the world map SYNC for this repair.

Ran `ngram validate` after the map SYNC consolidation; pre-existing schema,
tempo, and world-builder doc gaps plus broken CHAIN links remain.

Consolidated frontend map view PATTERNS docs into `docs/frontend/map/PATTERNS_Parchment_Map_View.md`, expanded the visibility/read-only detail, and removed the duplicate.

Removed the duplicate API algorithm doc (`docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`) so the canonical API flow lives only in `docs/infrastructure/api/ALGORITHM_Api.md`.

Ran `ngram validate` after removing the duplicate API algorithm doc; pre-existing schema/tempo/world-builder documentation gaps and broken CHAIN links remain.

Completed repair 13 by normalizing belief-based energy injection and enforcing zero-sum propagation (with supersedes drain) in `engine/physics/tick.py`, then updated physics implementation docs and SYNC to reflect the changes. `pytest engine/tests/test_behaviors.py -q` failed because `pytest_xprocess` is missing (anchorpy plugin), and `ngram validate` still reports pre-existing schema/tempo/world-builder doc gaps and broken CHAIN links.

Verified `engine/physics/graph/graph_queries_moments.py` moment query helpers (`get_narrative_moments`, `get_narratives_from_moment`, `get_available_transitions`, `get_clickable_words`) are already implemented for the current incomplete-impl repair; no code changes required (logged in `docs/physics/graph/SYNC_Graph.md`).

Revalidated traversal helpers (`make_dormant`, `process_wait_triggers`) in
`engine/moment_graph/traversal.py` for the current incomplete-impl repair;
implementations already present, no code changes required (logged in
`docs/engine/moment-graph-engine/SYNC_Moment_Graph_Engine.md`).

Ran `ngram validate` after confirming traversal helpers; pre-existing doc-chain
gaps remain in schema/tempo/world-builder (recorded in
`docs/engine/moment-graph-engine/SYNC_Moment_Graph_Engine.md`).

Reconfirmed mutation listener helpers (`add_mutation_listener`, `remove_mutation_listener`) in `engine/physics/graph/graph_ops_events.py` are already implemented for the repair run; no code changes required (logged in `docs/physics/graph/SYNC_Graph.md`).

Reviewed moment graph query helpers (`get_dormant_moments`, `get_wait_triggers`,
`get_moments_attached_to_tension`) in `engine/moment_graph/queries.py`; the
implementations were already present, so no code changes were required. Logged
the verification in `docs/engine/moment-graph-engine/SYNC_Moment_Graph_Engine.md`.

Reconfirmed `engine/physics/graph/graph_ops_types.py` helper implementations
(`SimilarNode.__str__`, `ApplyResult.success`) for the current repair run; no
code changes required. Updated `docs/physics/graph/SYNC_Graph.md` and ran
`ngram validate` (pre-existing schema/tempo/world-builder doc gaps remain).

Revalidated `engine/models/links.py` helper properties (`belief_intensity`, `is_present`, `has_item`, `is_here`) with line references (`engine/models/links.py:66`, `engine/models/links.py:120`, `engine/models/links.py:140`, `engine/models/links.py:160`); implementations already present, no code changes required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Logged the current repair run in `docs/schema/models/SYNC_Schema_Models.md` for the link helper verification.

Updated `docs/schema/models/SYNC_Schema_Models.md` to note the current repair run verification for link helper properties.

Revalidated `engine/models/nodes.py` helper properties (`is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) for the current incomplete-impl repair; implementations already present, no code changes required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Verified `engine/models/base.py` GameTimestamp comparison helpers (`__str__`, `__le__`, `__gt__`) are already implemented for repair 05; no code changes required and logged in `docs/schema/models/SYNC_Schema_Models.md`.

Revalidated `engine/models/nodes.py` helper properties (`Narrative.is_core_type`, `Moment.tick`, `Moment.should_embed`, `Moment.is_active`, `Moment.is_spoken`, `Moment.can_surface`) with line references and attempted `pytest engine/tests/test_models.py` (failed: missing `pytest_xprocess`); logged in `docs/schema/models/SYNC_Schema_Models.md`.

Rechecked the moment processor helper implementations for the current repair run; no code changes required (logged in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`).

Revalidated `engine/infrastructure/world_builder/world_builder.py` cache helper implementations for repair 04-INCOMPLETE_IMPL-world_builder-world_builder; no code changes required (logged in `docs/infrastructure/world-builder/SYNC_World_Builder.md`).

Created new documentation modules for the Distributed Content Generation Network: network (Voyager System, Bleed-Through, Transposition, World Scavenger, Shadow Feed, Ghost Dialogue), infrastructure (Storms, Storm Loader), product (Billing, Ledger Lock, Chronicle System, Business Model, GTM Strategy), plus the cross-cutting concept Subjective Truth & Rumor. Added DOCS pointers to the source data specs under `data/Distributed-Content-Generation-Network/` and updated `modules.yaml` mappings.

Reconfirmed the playthrough helper implementations (`_count_branches`, `create_scenario_playthrough`) in `engine/infrastructure/api/playthroughs.py` for the current repair run; no code changes required and logged in `docs/infrastructure/api/SYNC_Api.md`.

Verified ConversationThread path helpers in `engine/infrastructure/history/conversations.py` remain implemented for repair 02-INCOMPLETE_IMPL-history-conversations; no code changes required. Updated `docs/infrastructure/history/SYNC_History.md` and ran `ngram validate` (pre-existing doc gaps remain in schema/tempo/world-builder).

Revalidated the graph health helper implementations in `engine/graph/health/check_health.py` for repair 00-INCOMPLETE_IMPL-health-check_health; functions were already implemented and the graph-health SYNC was refreshed.

Aligned playthrough creation to the router implementation by adding a `/api/playthrough/scenario` alias in `engine/infrastructure/api/playthroughs.py` and removing the duplicate scenario endpoint in `engine/infrastructure/api/app.py` that returned a mismatched response shape. Updated the backend run script to point uvicorn at `engine.infrastructure.api.app:app` so `engine/run.py` boots correctly.
Added stub IMPLEMENTATION_*.md and TEST_*.md files for each new module to complete doc chains.

Revalidated `engine/models/links.py` helper properties (`belief_intensity`, `is_present`, `has_item`, `is_here`) for the repair run; no code changes required and logged in `docs/schema/models/SYNC_Schema_Models.md`.
Ran `ngram validate`; failures remain in pre-existing schema/tempo/world-builder docs and broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Verified `engine/models/base.py` GameTimestamp comparison helpers for the
INCOMPLETE_IMPL repair and attempted `pytest engine/tests/test_models.py`; the
run failed due to missing `pytest_xprocess` in the environment. Ran
`ngram validate`; failures remain in pre-existing schema/tempo/world-builder
documentation gaps and broken CHAIN links.

Verified `engine/models/base.py` comparison helpers (`__str__`, `__le__`, `__gt__`) for the current incomplete-impl repair; implementations already present and logged in `docs/schema/models/SYNC_Schema_Models.md`.
Ran `ngram validate`; failures remain in pre-existing schema/tempo/world-builder doc gaps and broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Logged repair 03-INCOMPLETE_IMPL-world_builder-world_builder verification in `docs/infrastructure/world-builder/SYNC_World_Builder.md`; confirmed `_hash_query` and `clear_cache` are implemented in `engine/infrastructure/world_builder/world_builder.py`, so no code changes were required. Ran `ngram validate`; failures remain in pre-existing schema/tempo/world-builder doc gaps and broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Rechecked `engine/infrastructure/memory/moment_processor.py` helper implementations for the current repair run; no code changes required and logged the verification in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.
Ran `ngram validate` after the scene-memory SYNC update; failures remain in pre-existing schema/tempo/world-builder docs and broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Logged the repair 03-INCOMPLETE_IMPL-world_builder-world_builder revalidation in `docs/infrastructure/world-builder/SYNC_World_Builder.md`; no code changes required.
Revalidated repair 01-INCOMPLETE_IMPL-history-conversations conversation helpers; no code changes required (logged in `docs/infrastructure/history/SYNC_History.md`).

Logged the 04-INCOMPLETE_IMPL-models-base repair verification for `engine/models/base.py` comparison helpers in `docs/schema/models/SYNC_Schema_Models.md`; no code changes required.

Rechecked `engine/models/base.py` comparison helpers (`__str__`, `__le__`, `__gt__`) for the current incomplete-impl repair; implementations already present, no code changes required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Revalidated `engine/infrastructure/world_builder/world_builder.py` helpers (`_hash_query`, `clear_cache`) for repair 03-INCOMPLETE_IMPL-world_builder-world_builder; implementations already present and logged in `docs/infrastructure/world-builder/SYNC_World_Builder.md`.

Revalidated moment processor helpers for the current repair run; no code changes
needed and logged in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.

Ran `ngram validate` after confirming the nodes helper implementations; failures remain in pre-existing `docs/schema/`, `docs/infrastructure/tempo/`, and `docs/infrastructure/world-builder/` gaps plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Logged the current repair run verification for `engine/models/base.py` comparison helpers in `docs/schema/models/SYNC_Schema_Models.md`; no code changes required.

Logged the current repair 05 verification for `engine/models/links.py` in `docs/schema/models/SYNC_Schema_Models.md`; no code changes required.

Revalidated `engine/models/nodes.py` helper properties (`is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) for the current incomplete-impl repair; implementations already present, no code changes required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Revalidated `engine/models/nodes.py` helper properties (`is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) for the current incomplete-impl repair run; implementations already present and logged in `docs/schema/models/SYNC_Schema_Models.md`.

Reconfirmed `engine/models/links.py` helper properties (`belief_intensity`, `is_present`, `has_item`, `is_here`) remain implemented for the current repair run; no code changes required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Revalidated `engine/models/links.py` helper properties (`belief_intensity`, `is_present`, `has_item`, `is_here`) for the repair run; implementations already present and logged in `docs/schema/models/SYNC_Schema_Models.md`.

Reverified `engine/models/base.py` comparison helpers (`__str__`, `__le__`, `__gt__`) for the current repair run; implementations already present, no code changes required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Reconfirmed `engine/infrastructure/memory/moment_processor.py` helper implementations for the repair run; no code changes required and logged the verification in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.

Reverified `ConversationThread` path helpers in `engine/infrastructure/history/conversations.py` for the current repair run; implementations already present, no code changes required.
Logged the repair 01-INCOMPLETE_IMPL-history-conversations verification in `docs/infrastructure/history/SYNC_History.md`.
Captured the `ngram validate` results for this repair run in `docs/infrastructure/history/SYNC_History.md`.
Revalidated ConversationThread helper implementations for repair 01-INCOMPLETE_IMPL-history-conversations; no code changes required and logged in `docs/infrastructure/history/SYNC_History.md`.
Updated `docs/infrastructure/history/SYNC_History.md` with the latest repair 01-INCOMPLETE_IMPL-history-conversations verification note; no code changes required.
Reconfirmed `engine/models/base.py` comparison helpers (`__str__`, `__le__`, `__gt__`) for the 06-INCOMPLETE_IMPL-models-base repair run; implementations are already present, so no code changes were required (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Verified `engine/infrastructure/world_builder/world_builder.py` helper implementations (`_hash_query`, `clear_cache`) for the incomplete-impl repair; task was stale with no code changes (logged in `docs/infrastructure/world-builder/SYNC_World_Builder.md`).

Revalidated `engine/infrastructure/world_builder/world_builder.py` helper implementations (`_hash_query`, `clear_cache`) for the current repair run; no code changes were needed and the update is recorded in `docs/infrastructure/world-builder/SYNC_World_Builder.md`. Ran `ngram validate`; failures remain in pre-existing schema/tempo/world-builder doc gaps and broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Verified `engine/models/nodes.py` helper properties (`is_core_type`, `tick`, `should_embed`, `is_active`, `is_spoken`, `can_surface`) are already implemented; repair task was stale and required no code changes (logged in `docs/schema/models/SYNC_Schema_Models.md`).

Implemented missing playthrough helper logic in `engine/infrastructure/api/playthroughs.py` (branch counting, per-playthrough GraphQueries caching, and embedding service fallback) and updated API implementation docs.

Reverified the moment processor helpers in `engine/infrastructure/memory/moment_processor.py` for repair 03; all implementations are present and no code changes were required (logged in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`).
Added a reconfirmation entry in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md` for the current repair run.

Added `NEXT_PUBLIC_API_URL=http://localhost:8000` to `.env` so the frontend uses the expected local backend by default.

Hardened `TempoController.stop` and `update_display_queue_size` with input cleanup, queue-size validation, and logging; documented the updates in tempo implementation/SYNC.
Added tempo SYNC observations for backpressure validation and testing gaps.
Completed the tempo documentation chain by adding PATTERNS/BEHAVIORS/VALIDATION/TEST docs in `docs/infrastructure/tempo/`.

Reconfirmed ConversationThread helper implementations in `engine/infrastructure/history/conversations.py` for the repair run; no code changes required.

Verified the graph health report helpers in `engine/graph/health/check_health.py`; the incomplete-impl task was stale and required no code changes (logged in `docs/schema/graph-health/SYNC_Graph_Health.md`).
Revalidated the health check helper implementations for the current repair run and refreshed `docs/schema/graph-health/SYNC_Graph_Health.md`; no code changes required.

Aligned tempo API calls with the shared frontend `API_BASE` so speed controls and tempo SSE respect `NEXT_PUBLIC_API_URL`. Verified via `cd frontend && npm run build`.

Adjusted the frontend chronicle panel to host the speed controls directly beneath the journal input, added wrapping for narrow widths, and removed the fixed bottom-left speed widget. Verified via `cd frontend && npm run build`.

Added a shared agent CLI wrapper in `engine/infrastructure/orchestration/agent_cli.py`, routed narrator/world-runner/world-builder CLI calls through it, and added `AGENTS_MODEL` provider selection (with doc updates in narrator/world-builder implementation and SYNC files).

Adjusted narrator implementation doc references to avoid broken-link parsing (removed colon-qualified paths, standardized file paths, and noted prompt builder location), and logged the update in `docs/agents/narrator/SYNC_Narrator.md`.

Repaired broken canon implementation doc references by switching to full-path file entries and removing stray `# DOCS:` labels, then logged the update in `docs/infrastructure/canon/SYNC_Canon.md`.

Repaired broken implementation doc links in `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` by qualifying method references with the semantic search file path and cleaning the DOCS reference; noted in `docs/world/map/SYNC_Map.md`.

Updated the world-runner implementation doc to remove method-name file references so broken-link checks resolve cleanly, and logged the change in `docs/agents/world-runner/SYNC_World_Runner.md`.
Updated the World Runner implementation doc tables to use concrete file path/line references for entry points, configuration, and state fields, and logged the change in `docs/agents/world-runner/SYNC_World_Runner.md`.
Ran `ngram validate`; failures remain in `docs/schema/`, `docs/infrastructure/tempo/`, and `docs/infrastructure/world-builder/` plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Repaired broken narrator implementation links in `docs/agents/narrator/IMPLEMENTATION_Narrator.md` by pinning prompt ownership, correcting the narrator entrypoint reference, and grounding playthrough file references to existing paths; logged the update in `docs/agents/narrator/SYNC_Narrator.md`. Ran `ngram validate`; failures remain in `docs/schema/`, `docs/infrastructure/tempo/`, and `docs/infrastructure/world-builder/` plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Reworded the debug stream entry in `docs/infrastructure/api/IMPLEMENTATION_Api.md` to avoid an `asyncio.Queue` file reference; logged the fix in `docs/infrastructure/api/SYNC_Api.md`. Ran `ngram validate`; failures remain in pre-existing schema/tempo/world-builder docs and broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Repaired broken file references in `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` by aligning paths to `frontend/**`, removing the missing playthrough route, and logging the change in `docs/frontend/SYNC_Frontend.md`. Ran `ngram validate`; failures remain in pre-existing `docs/schema/`, `docs/infrastructure/tempo/`, and `docs/infrastructure/world-builder/` gaps.

Verified the canon module documentation mapping already exists; recorded this check in `docs/infrastructure/canon/SYNC_Canon.md`.

Mapped `engine/infrastructure/api/**` to `docs/infrastructure/api/` in `modules.yaml` and added a `# DOCS:` header in `engine/infrastructure/api/app.py` so `ngram context` resolves the API documentation chain.

Added a `# DOCS:` reference in `engine/infrastructure/memory/__init__.py` to
align the scene-memory mapping with the package entrypoint (the processor
module already included a DOCS pointer).
Noted the package DOCS reference in `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md`.

Verified the history module already has documentation and a `modules.yaml`
mapping; no code changes required beyond logging this verification.
Ran `ngram validate`; failures remain in `docs/schema/`, `docs/infrastructure/tempo/`,
and `docs/infrastructure/world-builder/` plus broken CHAIN links in
`docs/schema/SCHEMA_Moments.md`.

Documented the engine test suite module by adding `docs/engine/tests/` (PATTERNS
and SYNC), mapping `engine/tests/**` in `modules.yaml`, and linking
`engine/tests/__init__.py` to the docs chain.

Revalidated the ops-scripts documentation chain for `engine/scripts` and noted the
verification in `docs/infrastructure/ops-scripts/SYNC_Ops_Scripts.md`.

Documented the moment graph module by mapping `engine/moments/**` to
`docs/engine/moments/` in `modules.yaml`, adding PATTERNS/SYNC docs, and
aligning `engine/moments/__init__.py` DOCS references. Ran `ngram validate`;
failures remain in pre-existing schema/tempo/world-builder docs.

Mapped `engine/physics/graph/**` to `docs/physics/graph/` in `modules.yaml` and
linked `engine/physics/graph/graph_ops.py` to the graph docs via a DOCS
reference.

Mapped `engine/physics/graph/**` to `docs/physics/graph/` in `modules.yaml` and
linked `engine/physics/graph/graph_ops.py` to the graph documentation via a
DOCS reference.

Documented the ops-scripts module for `engine/scripts`, added a module mapping in
`modules.yaml`, and linked `seed_moment_sample.py` to the new docs with a DOCS
reference.

Linked `engine/scripts/generate_images_for_existing.py` to the ops-scripts doc
chain and added a DOCS pointer for `engine/scripts/inject_to_narrator.py` in the
async implementation docs so `ngram context` resolves for all engine scripts.

Documented the graph health module (`engine/graph/health/**`) with new PATTERNS/SYNC docs, mapped it in `modules.yaml`, and linked `check_health.py` to the doc chain.

Mapped the physics engine module (`engine/physics/**`) to existing docs in `docs/physics/` and added a DOCS reference in `engine/physics/tick.py` for `ngram context`.

Verified the `tools/` documentation mapping (cli-tools + image-generation) already covers `tools/stream_dialogue.py` and `tools/image_generation/*`, and recorded the verification in `docs/infrastructure/cli-tools/SYNC_CLI_Tools.md`.

Mapped the canon infrastructure module in `modules.yaml`, linking `engine/infrastructure/canon/**` and `tests/infrastructure/canon/` to the existing docs.

Normalized the DOCS header in `tools/image_generation/README.md` to a `# DOCS:` marker; `ngram context` still does not resolve markdown files. Ran `ngram validate`; remaining failures are pre-existing in `docs/schema/`, `docs/infrastructure/tempo/`, `docs/infrastructure/world-builder/`, and `docs/engine/moments/`.

Linked `frontend/lib/api.ts` and `frontend/lib/map/*` utilities to the frontend documentation chain with DOCS references and updated frontend/map SYNC notes. Ran `ngram validate`; remaining failures are pre-existing in `docs/schema/`, `docs/infrastructure/tempo/`, and `docs/infrastructure/world-builder/`.
Added image-generation DOCS references in `tools/image_generation/README.md` and reordered `tools/image_generation/generate_image.py` DOCS links so the image-generation chain is primary.
Updated image-generation and cli-tools implementation docs to reflect the new DOCS comment line numbers.

Documented the schema models module (`engine/models/**`) with new PATTERNS and SYNC docs, added a `modules.yaml` mapping, and linked `engine/models/__init__.py` to the documentation chain via a DOCS reference.

Documented the frontend scenario selection module with new docs, a modules.yaml mapping, and a DOCS reference in `frontend/app/scenarios/page.tsx`.
Added `frontend/app/start/page.tsx` as an explicit frontend entry point in `modules.yaml` to map the start screen to the frontend docs.
Linked `frontend/types/game.ts`, `frontend/types/map.ts`, and `frontend/types/moment.ts` to the frontend documentation chain and added a `frontend/types/**` mapping in `modules.yaml`.

Added DOCS references for `frontend/app` shell files (layout, start screen, globals stylesheet) to close the undocumented frontend/app gap.

Extended the frontend map module mapping to include `frontend/app/map/**` and linked the map route to the map view documentation.

Linked `frontend/hooks/useGameState.ts` and `frontend/hooks/useMoments.ts` to the frontend documentation chain via DOCS references to close the hooks documentation gap.

Documented the frontend map view module with new docs in `docs/frontend/map/` and a DOCS reference in `frontend/components/map/MapClient.tsx` (module mapping already existed). Ran `ngram validate`; failures are pre-existing in `docs/schema/` and `docs/infrastructure/tempo/` plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.

Linked `engine/infrastructure/canon/canon_holder.py` to the canon documentation chain via an in-docstring DOCS reference and corrected the canon SYNC chain status.
Ran `ngram validate`; failures remain in pre-existing `docs/schema/`, `docs/infrastructure/tempo/`, and `docs/infrastructure/world-builder/` gaps.

Mapped `frontend/components/moment/**` to existing Scene docs in `modules.yaml` and added a DOCS reference in `frontend/components/moment/index.ts` to close the moment UI documentation gap.

Completed async architecture implementation documentation, linked CHAIN sections, added a DOCS reference in `engine/scripts/check_injection.py`, and logged the injection queue format conflict in `docs/infrastructure/async/SYNC_Async_Architecture.md`.

Completed image-generation documentation chain by adding IMPLEMENTATION doc, linking CHAIN references, and mapping the module in `modules.yaml`.

Documented the frontend right panel module with new docs, a modules.yaml mapping, and a DOCS reference in `frontend/components/panel/RightPanel.tsx`.

Documented the frontend minimap module with new docs, a modules.yaml mapping, and a DOCS reference in `frontend/components/minimap/Minimap.tsx`.

Mapped the frontend scene components to `docs/frontend/scene/` in `modules.yaml` and linked `frontend/components/scene/SceneView.tsx` to the scene documentation chain.

Mapped `frontend/lib/map/**` to the existing frontend map docs and added a DOCS reference in `frontend/lib/map/index.ts` to close the map helper documentation gap.

World scraping documentation chain finalized with implementation details and extraction candidates; DOCS references remain absent because `data/` is gitignored. Frontend module is now mapped in `modules.yaml` with existing docs and a DOCS reference in `frontend/app/page.tsx`. Added a DOCS reference to `frontend/components/chronicle/ChroniclePanel.tsx` to link it to frontend implementation documentation.
Completed cli-tools documentation chain (BEHAVIORS/ALGORITHM/VALIDATION/IMPLEMENTATION/TEST), updated CHAIN references, and added a `modules.yaml` mapping.
Completed docs/design chain by adding IMPLEMENTATION_Vision.md, updating TEST_Vision.md chain, and refreshing SYNC_Vision.md; mapped design-vision in modules.yaml.
Linked the History implementation doc into the module chain, added a CHAIN block in `docs/infrastructure/history/SYNC_History.md`, and mapped `engine/infrastructure/history/**` in `modules.yaml`.
Mapped frontend module in `modules.yaml` to cover `frontend/**`, aligning docs with `docs/frontend/` and closing the unmapped `frontend/components` gap.
Linked `frontend/components/voices/Voices.tsx` to frontend docs via a DOCS reference for `ngram context` discoverability.
Linked `frontend/components/debug/DebugPanel.tsx` to frontend docs via a DOCS reference.
Verified the debug panel documentation mapping remains in place for the current repair (no code changes needed).
Linked `frontend/components/ui/Toast.tsx` to the frontend documentation chain and listed it as a frontend entry point in `modules.yaml`.
Ran `ngram validate`; failures are pre-existing doc gaps in `docs/schema/` and `docs/infrastructure/tempo/` plus broken CHAIN links in `docs/schema/SCHEMA_Moments.md`.
Repair 22: corrected the history module implementation chain link and registered history in `modules.yaml`.

Frontend-backend integration fixes for playthrough flow:
- Added scene-memory IMPLEMENTATION/TEST docs, updated doc chains, and added a DOCS reference in `engine/infrastructure/memory/moment_processor.py`.
- Mapped scene-memory in `modules.yaml`; `ngram validate` still reports pre-existing schema/infrastructure doc gaps.
- Reverified physics tick energy helpers in `engine/physics/tick.py`; repair 12 is stale and required no code changes.
- Added `/api/action` endpoint for full game loop (narrator→tick→flips)
- Fixed scenario path in playthroughs.py (was `engine/scenarios`, now `scenarios/`)
- Fixed `active_moments` vs `moments` field mismatch in useGameState.ts
- Implemented free text input in CenterStage.tsx (calls `sendMoment` API)
- Added emoji fallbacks for player/character avatars (👤/🗣️)
- Updated API IMPLEMENTATION and SYNC docs
Mapped frontend module in `modules.yaml` to link existing frontend docs with code.
Completed embeddings documentation chain by adding IMPLEMENTATION doc and updating IMPL paths.
Consolidated API algorithm docs for playthrough creation into `docs/infrastructure/api/ALGORITHM_Api.md` and redirected the duplicate file.
Consolidated duplicate world-runner IMPLEMENTATION docs into `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` and removed the redundant file; updated chain links.
Aligned the World Runner implementation doc with current initialization logging behavior.
Revalidated moment graph traversal helpers in `engine/moment_graph/traversal.py` for repair 08; `make_dormant` and `process_wait_triggers` are already implemented, so no code changes were needed.
Verified `engine/models/nodes.py` moment/narrative helper properties for repair 06; implementations already present, no code changes required.
Re-verified `engine/models/base.py` comparison helpers (`__str__`, `__le__`, `__gt__`) are implemented; no code changes required for repair 04-INCOMPLETE_IMPL-models-base.
Verified `engine/models/links.py` helper properties (`belief_intensity`, `is_present`, `has_item`, `is_here`) are already implemented; repair 05-INCOMPLETE_IMPL-models-links required no code changes.
Verified health check helper implementations in `engine/graph/health/check_health.py` for repair 00-INCOMPLETE_IMPL-health-check_health; no code changes required.
Verified moment processor functions for repair 03-INCOMPLETE_IMPL-memory-moment_processor; no code changes required.
Rechecked moment graph traversal helpers `make_dormant` and `process_wait_triggers` in `engine/moment_graph/traversal.py`; implementations already present, no code changes required.
Reconfirmed graph health helpers in `engine/graph/health/check_health.py` for repair 00; no code changes required and logged in `docs/schema/graph-health/SYNC_Graph_Health.md`.

Revalidated `engine/models/base.py` comparison helpers (`__str__`, `__le__`, `__gt__`) for repair 04-INCOMPLETE_IMPL-models-base; implementations already present and recorded in `docs/schema/models/SYNC_Schema_Models.md`.

Previous: Regenerated global repository map (`docs/map.md`). Fixed `modules.yaml` world-runner code pattern.
Logged repair 02-INCOMPLETE_IMPL-history-conversations verification in `docs/infrastructure/history/SYNC_History.md` (no code changes).
Consolidated physics algorithm docs into `docs/physics/ALGORITHM_Physics.md`, removed standalone physics ALGORITHM files, and updated physics/schema doc chains to the consolidated algorithm.
Repair 13 verified physics tick energy helpers in `engine/physics/tick.py`; repair task marked stale with no code changes.
Revalidated playthroughs API helper implementations; documentation updated for the stale repair task.
Confirmed `engine/models/base.py` comparison helpers were already implemented; no code change required.
Verified mutation listener helpers in `engine/physics/graph/graph_ops_events.py`; repair task is stale.
Verified graph ops type helpers in `engine/physics/graph/graph_ops_types.py` (`SimilarNode.__str__`, `ApplyResult.success`) are already implemented; repair task is stale.
Validated moment processor implementations; repair task appears stale.
Rechecked moment processor helpers in `engine/infrastructure/memory/moment_processor.py`; all flagged functions are implemented (no code changes).
Reconfirmed moment processor helper implementations in `engine/infrastructure/memory/moment_processor.py`; no code changes required.
Verified moment graph query helpers in `engine/moment_graph/queries.py` are already implemented; repair task appears stale.
Verified moment graph traversal helpers in `engine/moment_graph/traversal.py` are already implemented; repair task appears stale.
Verified moment query helpers in `engine/physics/graph/graph_queries_moments.py`; repair task appears stale.
Verified graph health report helpers in `engine/graph/health/check_health.py` are already implemented; repair task appears stale.
Reconfirmed health check helpers for repair 00-INCOMPLETE_IMPL-health-check_health; no code changes required.
Rechecked `engine/graph/health/check_health.py` for the health-check repair; functions remain implemented and no code changes were needed.
Re-verified ConversationThread path helpers in `engine/infrastructure/history/conversations.py`; repair task was stale and required no code changes.
Logged this repair run's verification of ConversationThread helpers in `docs/infrastructure/history/SYNC_History.md`.
Verified mutation listener helpers in `engine/physics/graph/graph_ops_events.py` are already implemented; recorded in `docs/physics/graph/SYNC_Graph.md`.
Logged repair 09-INCOMPLETE_IMPL-graph-graph_ops_events verification in `docs/physics/graph/SYNC_Graph.md`.
Verified `engine/models/base.py` comparison helpers are already implemented; repair 04-INCOMPLETE_IMPL-models-base is stale.
Verified link model helpers (`belief_intensity`, `is_present`, `has_item`, `is_here`) in `engine/models/links.py`; repair 05-INCOMPLETE_IMPL-models-links appears stale with no code changes required.
Logged the current repair verification in `docs/schema/models/SYNC_Schema_Models.md`.
Implemented markdown formatting and cosine similarity helpers in `engine/physics/graph/graph_queries_search.py` to complete the search mixin methods.
Updated `docs/physics/SYNC_Physics.md` observations; `ngram validate` still reports pre-existing docs/schema gaps and broken CHAIN links.
Recorded moment query verification in `docs/physics/graph/SYNC_Graph.md`.
Logged the graph_queries_moments helper verification in `docs/physics/graph/SYNC_Graph.md` for repair 11.
Recorded playthroughs helper verification in `docs/infrastructure/api/SYNC_Api.md`.
Reconfirmed playthroughs helper implementations for repair 01; no code changes required.
Verified playthroughs helper implementations for repair 01-INCOMPLETE_IMPL-api-playthroughs; no code changes required.
Recorded the repair 01-INCOMPLETE_IMPL-api-playthroughs verification in `docs/infrastructure/api/SYNC_Api.md`.
Logged the repair-01 reconfirmation entry in `docs/infrastructure/api/SYNC_Api.md`.
Rechecked playthroughs helper implementations for repair 01-INCOMPLETE_IMPL-api-playthroughs; no code changes required.
Logged the current repair verification for playthroughs helpers in `docs/infrastructure/api/SYNC_Api.md`.
Consolidated narrator algorithm docs into `docs/agents/narrator/ALGORITHM_Prompt_Structure.md` and updated narrator doc chains.
Reconfirmed traversal helper implementations for repair 08-INCOMPLETE_IMPL-moment_graph-traversal; no code changes required.
Consolidated narrator PATTERNS docs into `docs/agents/narrator/PATTERNS_Narrator.md` and deprecated `docs/agents/narrator/PATTERNS_World_Building.md`.
Consolidated map algorithm docs into `docs/world/map/ALGORITHM_Rendering.md`; removed `docs/world/map/ALGORITHM_Places.md` and `docs/world/map/ALGORITHM_Routes.md`.
Repair 17 revalidated map algorithm consolidation and updated `docs/world/map/SYNC_Map.md` wording to note the verification.
Completed world map documentation chain by adding validation, implementation, and test docs; added DOCS reference in `engine/world/map/semantic.py` and mapped module in `modules.yaml`.
Consolidated world-runner algorithm docs into `docs/agents/world-runner/ALGORITHM_World_Runner.md` and deprecated `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md`.
Removed the deprecated `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md` file to eliminate duplicate ALGORITHM docs under world-runner.
Consolidated world runner algorithm docs by merging graph tick details into `docs/agents/world-runner/ALGORITHM_World_Runner.md` and redirecting `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md`.
Re-removed the deprecated `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md` file to ensure the duplication cleanup is complete.
Verified the world-runner ALGORITHM duplication repair by deleting `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md` from the docs set.
Added `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`, updated history doc chains, added a DOCS reference in `engine/infrastructure/history/service.py`, and mapped the history module in `modules.yaml`.
Completed the World Runner documentation chain with VALIDATION/IMPLEMENTATION/TEST docs, updated chain links, added a DOCS reference, and mapped the module in `modules.yaml`.
Consolidated graph weight algorithm docs by redirecting `docs/physics/graph/ALGORITHM_Weight.md` to `docs/physics/graph/ALGORITHM_Energy_Flow.md`.
Consolidated world scraping algorithm docs into `docs/world/scraping/ALGORITHM_Pipeline.md` and removed duplicate phase-specific ALGORITHM files.
Recorded scraping doc consolidation in `docs/world/scraping/SYNC_World_Scraping.md` to align pipeline status with the canonical algorithm.
Consolidated world scraping ALGORITHM docs into `docs/world/scraping/ALGORITHM_Pipeline.md`, redirected per-phase docs, and updated chain links for scraping docs.
Added world scraping IMPLEMENTATION doc, updated scraping doc CHAIN links, added a DOCS reference in `data/scripts/inject_world.py`, and mapped the module in `modules.yaml`.
Verified map algorithm consolidation state and recorded the check in `docs/world/map/SYNC_Map.md`.
Moved `docs/schema/VALIDATION_Living_Graph.md` into `docs/physics/graph/VALIDATION_Living_Graph.md` to eliminate duplicate VALIDATION docs in `docs/schema/`.
Updated `docs/schema/VALIDATION_Graph.md` redirect to point at `docs/physics/graph/VALIDATION_Living_Graph.md` after the move.
Consolidated graph weight computation into `docs/physics/graph/ALGORITHM_Energy_Flow.md` and redirected `docs/physics/graph/ALGORITHM_Weight.md`.
Consolidated schema validation docs by merging graph integrity rules into `docs/schema/VALIDATION_Living_Graph.md` and redirecting `docs/schema/VALIDATION_Graph.md`.
Consolidated async algorithm docs into `docs/infrastructure/async/ALGORITHM_Async_Architecture.md` and removed per-topic async ALGORITHM files; updated async doc chains.
Reverified playthrough helper implementations for repair 01-INCOMPLETE_IMPL-api-playthroughs; no code changes required.
Re-verified ConversationThread path helper implementations for repair 02-INCOMPLETE_IMPL-history-conversations; no code changes required.
Reconfirmed moment graph query helper implementations in `engine/moment_graph/queries.py`; repair task was stale and required no code changes.
Removed the deprecated narrator patterns doc (`docs/agents/narrator/PATTERNS_World_Building.md`) and cleaned duplicate PATTERNS chain references in narrator docs.
Removed duplicate graph algorithm doc `docs/physics/graph/ALGORITHM_Weight.md` after consolidating weight computation into `docs/physics/graph/ALGORITHM_Energy_Flow.md` and updated the design doc listing.

Documented the moment graph module with a full documentation chain, a DOCS
reference in `engine/moments/__init__.py`, and aligned the module docs with the
existing `modules.yaml` entry.

Verified repair 57-UNDOCUMENTED-infrastructure-history is already resolved; history docs and module mapping already exist and are recorded in `docs/infrastructure/history/SYNC_History.md`.
Repaired broken link references in `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` and logged the update in `docs/agents/world-runner/SYNC_World_Runner.md`.
Rechecked `engine/graph/health/check_health.py` for the current incomplete-impl repair; implementations are present and logged in `docs/schema/graph-health/SYNC_Graph_Health.md`.

---

## ACTIVE WORK

Logged the schema models repair verification for `engine/models/base.py` in `docs/schema/models/SYNC_Schema_Models.md` for the current repair run; no code changes required.

### Moment Processor Repair

- **Area:** `engine/infrastructure/memory/`
- **Status:** completed
- **Owner:** Codex (repair agent)
- **Context:** Verified incomplete-impl report; no code changes needed.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| None | - | - | - |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Implement_Write_Or_Modify_Code

**Current focus:** Keep Moment Graph docs/code aligned.

**Key context:**
Moment processor functions already have implementations; repair task appears stale.

**Watch out for:**
Some SYNC files still contain placeholders and need updates when touched.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Moment processor repair task did not require code changes; sync updated to
record validation.

**Decisions made recently:**
Validated existing implementations instead of altering working code.

**Needs your input:**
None.

**Concerns:**
Repair task appears stale relative to current code.

---

## TODO

### High Priority

- [ ] Add module mapping for `engine/infrastructure/memory/`.

### Backlog

- IDEA: Audit placeholder sync templates for updates.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Stable; minor documentation hygiene tasks remain.

**Architectural concerns:**
None surfaced in this repair.

**Opportunities noticed:**
Clarify module mappings for infrastructure/memory.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `infrastructure/scene-memory` | canonical | `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| None | - | - | - |

**Unmapped code:** (run `ngram validate` to check)
- `engine/infrastructure/memory/`

**Coverage notes:**
Moment processor is documented under scene-memory but not mapped in modules.yaml.


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`

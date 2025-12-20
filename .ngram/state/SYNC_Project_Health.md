# SYNC: Project Health

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: ngram doctor
STATUS: CRITICAL
```

---

## CURRENT STATE

**Health Score:** 0/100

The project has critical issues that will significantly impact agent effectiveness. Address these before starting new work.

| Severity | Count |
|----------|-------|
| Critical | 58 |
| Warning | 344 |
| Info | 413 |

---

## ISSUES

### UNDOCUMENTED (43 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `frontend` - No documentation mapping (54 files)
  - Add mapping to modules.yaml
- `frontend/components` - No documentation mapping (34 files)
  - Add mapping to modules.yaml
- `frontend/components/voices` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/chronicle` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/panel` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `frontend/components/debug` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/minimap` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `frontend/components/moment` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `frontend/components/scene` - No documentation mapping (12 files)
  - Add mapping to modules.yaml
- `frontend/components/ui` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- ... and 33 more

### PLACEHOLDER (1 files)

**What's wrong:** Template placeholders mean the documentation was started but never completed. Agents loading these docs get no useful information.

**How to fix:** Fill in the placeholders with actual content, or delete the file if it's not needed yet.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `.ngram/repairs/2025-12-19_23-15-21/87-PLACEHOLDER-state-SYNC_Project_State/ISSUE.md` - Contains 3 template placeholder(s)
  - Fill in actual content

### BROKEN_IMPL_LINK (14 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 2 non-existent file(s)
  - Update or remove references: IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md, IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` - References 1 non-existent file(s)
  - Update or remove references: useMoments.clickWord
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md` - References 16 non-existent file(s)
  - Update or remove references: page.tsx, api.ts, map/page.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 2 non-existent file(s)
  - Update or remove references: narrator.py, stream_dialogue.py
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: places.yaml
- `docs/physics/IMPLEMENTATION_Physics.md` - References 11 non-existent file(s)
  - Update or remove references: engine/infrastructure/orchestration/speed.py, graph_ops.py, graph_queries_narratives.py
- `docs/product/billing/IMPLEMENTATION_Billing_Technical_Stack.md` - References 1 non-existent file(s)
  - Update or remove references: tick.py
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` - References 8 non-existent file(s)
  - Update or remove references: engine/infrastructure/embeddings/service.py:EmbeddingService.__init__, engine/infrastructure/embeddings/service.py:EmbeddingService.similarity, engine/infrastructure/embeddings/service.py:EmbeddingService._load_model
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: conversations/aldric.md
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 5 non-existent file(s)
  - Update or remove references: playthroughs.py, moments.py, sse_broadcast.py
- ... and 4 more

### INCOMPLETE_CHAIN (11 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/product/chronicle-system` - Missing: ALGORITHM
- `docs/product/gtm-strategy` - Missing: ALGORITHM
- `docs/product/billing` - Missing: ALGORITHM
- `docs/product/ledger-lock` - Missing: ALGORITHM
- `docs/network/world-scavenger` - Missing: ALGORITHM
- `docs/network/ghost-dialogue` - Missing: ALGORITHM
- `docs/network/shadow-feed` - Missing: ALGORITHM
- `docs/network/voyager-system` - Missing: ALGORITHM
- `docs/network/bleed-through` - Missing: ALGORITHM
- `docs/infrastructure/storm-loader` - Missing: ALGORITHM
- ... and 1 more

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/infrastructure/world_builder/world_builder.py` - Contains 2 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 3 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (5 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/world/scraping` - Total 54K chars (threshold: 50K)
- `docs/physics` - Total 225K chars (threshold: 50K)
- `docs/design` - Total 67K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 52K chars (threshold: 50K)
- `docs/infrastructure/api` - Total 55K chars (threshold: 50K)

### STALE_IMPL (5 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md` - 1 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 2 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 4 referenced files not found
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - 5 referenced files not found
- `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md` - 6 referenced files not found

### DOC_TEMPLATE_DRIFT (231 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONFIGURATION, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/frontend/SYNC_Frontend.md` - Missing: RECENT CHANGES
- `docs/frontend/ALGORITHM_Frontend_Data_Flow.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/frontend/SYNC_Frontend_archive_2025-12.md` - Missing: MATURITY
- `docs/frontend/TEST_Frontend_Coverage.md` - Missing: UNIT TESTS, INTEGRATION TESTS, EDGE CASES, TEST COVERAGE, HOW TO RUN, KNOWN TEST GAPS, FLAKY TESTS
- `docs/frontend/BEHAVIORS_Frontend_State_And_Interaction.md` - Missing: EDGE CASES, ANTI-BEHAVIORS
- `docs/frontend/VALIDATION_Frontend_Invariants.md` - Missing: PROPERTIES
- `docs/frontend/scene/SYNC_Scene_archive_2025-12.md` - Missing: CURRENT STATE, IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/frontend/scene/SYNC_Scene.md` - Missing: MATURITY, RECENT CHANGES
- `docs/frontend/scene/ALGORITHM_Scene.md` - Missing: ALGORITHM: {Primary Function Name}
- ... and 221 more

### NON_STANDARD_DOC_TYPE (36 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/map.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Player_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/physics/API_Physics.md` - Doc filename does not use a standard prefix
- `docs/product/chronicle-system/MECHANISMS_Chronicle_Pipeline.md` - Doc filename does not use a standard prefix
- ... and 26 more

### NAMING_CONVENTION (8 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/.env.example` - Naming convention violations task (1): 10 items
- `frontend/components/debug/DebugPanel.tsx` - Naming convention violations task (2): 10 items
- `frontend/components/panel/ConversationsTab.tsx` - Naming convention violations task (3): 10 items
- `frontend/components/scene/SceneBanner.tsx` - Naming convention violations task (4): 10 items
- `frontend/hooks/useTempo.ts` - Naming convention violations task (5): 10 items
- `docs/world/map/SYNC_Map_archive_2025-12.md` - Naming convention violations task (6): 10 items
- `docs/design/SYNC_Vision_archive_2025-12.md` - Naming convention violations task (7): 10 items
- `docs/infrastructure/history/ALGORITHM/ALGORITHM_Query_and_Record.md` - Naming convention violations task (8): 9 items

### DOC_GAPS (2 files)

**What's wrong:** A previous agent couldn't complete all work and left tasks in a GAPS section. These represent incomplete implementations, missing docs, or decisions that needed human input.

**How to fix:** Read the GAPS section in the SYNC file, complete the listed tasks, and mark them [x] done or remove the section when finished.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/SYNC_Physics.md` - 2 incomplete task(s) from previous session
- `docs/infrastructure/api/SYNC_Api.md` - 2 incomplete task(s) from previous session

### DOC_DUPLICATION (19 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/map/PATTERNS_Parchment_Map_View.md` - Multiple PATTERNS docs in `map/`
- `docs/frontend/map/SYNC_Map_View.md` - Multiple SYNC docs in `map/`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` - Multiple IMPLEMENTATION docs in `IMPLEMENTATION_Frontend_Code_Architecture/`
- `docs/world/map/ALGORITHM_Rendering.md` - Multiple ALGORITHM docs in `map/`
- `docs/world/map/ALGORITHM/ALGORITHM_Places.md` - Multiple ALGORITHM docs in `ALGORITHM/`
- `docs/product/chronicle-system/PATTERNS_Chronicle_Flywheel.md` - Multiple PATTERNS docs in `chronicle-system/`
- `docs/product/chronicle-system/VALIDATION_Chronicle_Invariants.md` - Multiple VALIDATION docs in `chronicle-system/`
- `docs/product/chronicle-system/BEHAVIORS_Chronicle_Types.md` - Multiple BEHAVIORS docs in `chronicle-system/`
- `docs/product/chronicle-system/IMPLEMENTATION_Chronicle_System.md` - Multiple IMPLEMENTATION docs in `chronicle-system/`
- `docs/product/business-model/BEHAVIORS_Retention_Mechanisms.md` - Multiple BEHAVIORS docs in `business-model/`
- ... and 9 more

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `.ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md` - Escalation marker needs decision

### HARDCODED_CONFIG (12 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- `frontend/app/start/page.tsx` - Contains hardcoded configuration values
- `frontend/lib/api.ts` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- ... and 2 more

---

## LATER

These are minor issues that don't block work but would improve project health:

- [ ] `engine/.pytest_cache/v/cache/lastfailed` - No DOCS: reference in file header
- [ ] `engine/.pytest_cache/v/cache/nodeids` - No DOCS: reference in file header
- [ ] `engine/graph/health/example_queries.cypher` - No DOCS: reference in file header
- [ ] `engine/graph/health/lint_terminology.py` - No DOCS: reference in file header
- [ ] `engine/graph/health/test_schema.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/api/moments.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/api/playthroughs.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/api/sse_broadcast.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/history/conversations.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/orchestration/agent_cli.py` - No DOCS: reference in file header
- ... and 403 more

---

## HANDOFF

**For the next agent:**

Before starting your task, consider addressing critical issues - especially if your work touches affected files. Monoliths and undocumented code will slow you down.

**Recommended first action:** Pick one MONOLITH file you'll be working in and split its largest function into a separate module.

---

*Generated by `ngram doctor`*
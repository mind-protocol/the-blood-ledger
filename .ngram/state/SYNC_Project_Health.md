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
| Critical | 48 |
| Warning | 351 |
| Info | 342 |

---

## ISSUES

### UNDOCUMENTED (34 files)

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
- ... and 24 more

### BROKEN_IMPL_LINK (14 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` - References 17 non-existent file(s)
  - Update or remove references: GameClient.tsx, scenarios/page.tsx, useGameState.ts
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - References 7 non-existent file(s)
  - Update or remove references: inject_world.py, phase1_geography.py, phase3_events.py
- `docs/product/billing/IMPLEMENTATION_Billing_Technical_Stack.md` - References 1 non-existent file(s)
  - Update or remove references: tick.py
- `docs/design/opening/IMPLEMENTATION_Opening.md` - References 9 non-existent file(s)
  - Update or remove references: scene.json, playthroughs.py, CONTENT.md
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` - References 3 non-existent file(s)
  - Update or remove references: service.py, EmbeddingService.model, engine/infrastructure/embeddings/service.py
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: conversations/aldric.md
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` - References 7 non-existent file(s)
  - Update or remove references: playthroughs/{playthrough_id}/injection_queue.json, playthroughs/narrator_state.json, engine/scripts/inject_to_narrator.py
- `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md` - References 1 non-existent file(s)
  - Update or remove references: IMPLEMENTATION/IMPLEMENTATION_Overview.md
- `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md` - References 8 non-existent file(s)
  - Update or remove references: query.py, sparsity.py, world_builder.py
- ... and 4 more

### INCOMPLETE_CHAIN (23 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend` - Missing: HEALTH
- `docs/product/chronicle-system` - Missing: ALGORITHM, HEALTH
- `docs/product/gtm-strategy` - Missing: ALGORITHM, HEALTH
- `docs/product/business-model` - Missing: HEALTH
- `docs/product/billing` - Missing: ALGORITHM, HEALTH
- `docs/product/ledger-lock` - Missing: ALGORITHM, HEALTH
- `docs/design` - Missing: HEALTH
- `docs/network/world-scavenger` - Missing: ALGORITHM, HEALTH
- `docs/network/ghost-dialogue` - Missing: ALGORITHM, HEALTH
- `docs/network/shadow-feed` - Missing: ALGORITHM, HEALTH
- ... and 13 more

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/world_builder/world_builder.py` - Contains 2 empty/incomplete function(s)

### LARGE_DOC_MODULE (2 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/design` - Total 67K chars (threshold: 50K)
- `docs/infrastructure/embeddings` - Total 51K chars (threshold: 50K)

### STALE_IMPL (7 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` - 1 referenced files not found
- `docs/design/opening/IMPLEMENTATION_Opening.md` - 3 referenced files not found
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` - 3 referenced files not found
- `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md` - 7 referenced files not found
- `docs/infrastructure/ops-scripts/IMPLEMENTATION_Engine_Scripts_Layout.md` - 2 referenced files not found
- `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md` - 1 referenced files not found
- `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md` - 7 referenced files not found

### DOC_TEMPLATE_DRIFT (194 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONFIGURATION, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/frontend/SYNC_Frontend.md` - Missing: RECENT CHANGES
- `docs/frontend/ALGORITHM_Frontend_Data_Flow.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/frontend/SYNC_Frontend_archive_2025-12.md` - Missing: MATURITY
- `docs/frontend/PATTERNS_Presentation_Layer.md` - Missing: DATA
- `docs/frontend/BEHAVIORS_Frontend_State_And_Interaction.md` - Missing: EDGE CASES, ANTI-BEHAVIORS
- `docs/frontend/VALIDATION_Frontend_Invariants.md` - Missing: PROPERTIES, HEALTH COVERAGE
- `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md` - Missing: DATA
- `docs/frontend/right-panel/PATTERNS_Tabbed_Right_Panel.md` - Missing: DATA
- `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md` - Missing: DATA
- ... and 184 more

### DOC_LINK_INTEGRITY (24 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/scripts/generate_images_for_existing.py` - Code file references docs but the bidirectional link is broken
- `frontend/app/globals.css` - Code file references docs but the bidirectional link is broken
- `frontend/app/layout.tsx` - Code file references docs but the bidirectional link is broken
- `frontend/app/map/page.tsx` - Code file references docs but the bidirectional link is broken
- `frontend/components/SpeedControl.tsx` - Code file references docs but the bidirectional link is broken
- `frontend/components/chronicle/ChroniclePanel.tsx` - Code file references docs but the bidirectional link is broken
- `frontend/components/debug/DebugPanel.tsx` - Code file references docs but the bidirectional link is broken
- `frontend/components/minimap/SunArc.tsx` - Code file references docs but the bidirectional link is broken
- `frontend/components/moment/index.ts` - Code file references docs but the bidirectional link is broken
- `frontend/components/ui/Toast.tsx` - Code file references docs but the bidirectional link is broken
- ... and 14 more

### CODE_DOC_DELTA_COUPLING (3 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `frontend/app/scenarios/page.tsx` - Code changed without corresponding doc or SYNC updates
- `frontend/components/map/MapClient.tsx` - Code changed without corresponding doc or SYNC updates
- `frontend/components/scene/SceneView.tsx` - Code changed without corresponding doc or SYNC updates

### NON_STANDARD_DOC_TYPE (50 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/TEST_Frontend_Coverage.md` - Doc filename does not use a standard prefix
- `docs/frontend/scene/TEST_Scene.md` - Doc filename does not use a standard prefix
- `docs/world/map/TEST_Map_Test_Coverage.md` - Doc filename does not use a standard prefix
- `docs/world/scraping/TEST_World_Scraping.md` - Doc filename does not use a standard prefix
- `docs/product/chronicle-system/TEST_Chronicle_System.md` - Doc filename does not use a standard prefix
- `docs/product/chronicle-system/MECHANISMS_Chronicle_Pipeline.md` - Doc filename does not use a standard prefix
- `docs/product/gtm-strategy/TEST_GTM_Strategy.md` - Doc filename does not use a standard prefix
- `docs/product/gtm-strategy/MECHANISMS_GTM_Programs.md` - Doc filename does not use a standard prefix
- `docs/product/business-model/TEST_Business_Model.md` - Doc filename does not use a standard prefix
- `docs/product/business-model/MECHANISMS_Margin_Defense.md` - Doc filename does not use a standard prefix
- ... and 40 more

### NAMING_CONVENTION (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/design/ALGORITHM_Vision.md` - Doc filename 'ALGORITHM_Vision.md' is too short/non-descriptive
- `docs/design/opening/BEHAVIORS_Opening.md` - Doc filename 'BEHAVIORS_Opening.md' is too short/non-descriptive
- `docs/frontend/SYNC_Frontend.md` - Doc filename 'SYNC_Frontend.md' is too short/non-descriptive
- `docs/frontend/scene/SYNC_Scene_archive_2025-12.md` - Naming convention violations task (4): 10 items
- `docs/infrastructure/canon/HEALTH_Canon.md` - Doc filename 'HEALTH_Canon.md' is too short/non-descriptive
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Search.md` - Doc filename 'ALGORITHM_Search.md' is too short/non-descriptive
- `docs/infrastructure/embeddings/TEST_Embeddings.md` - Doc filename 'TEST_Embeddings.md' is too short/non-descriptive
- `docs/infrastructure/history/TEST/TEST_Cases.md` - Doc filename 'TEST_Cases.md' is too short/non-descriptive
- `docs/infrastructure/storms/IMPLEMENTATION_Storms.md` - Doc filename 'IMPLEMENTATION_Storms.md' is too short/non-descriptive
- `docs/infrastructure/world-builder/ALGORITHM/ALGORITHM_Overview.md` - Doc filename 'ALGORITHM_Overview.md' is too short/non-descriptive
- ... and 11 more

### DOC_DUPLICATION (16 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/map/PATTERNS_Parchment_Map_View.md` - Multiple PATTERNS docs in `map/`
- `docs/frontend/map/SYNC_Map_View.md` - Multiple SYNC docs in `map/`
- `docs/product/chronicle-system/PATTERNS_Chronicle_Flywheel.md` - Multiple PATTERNS docs in `chronicle-system/`
- `docs/product/chronicle-system/VALIDATION_Chronicle_Invariants.md` - Multiple VALIDATION docs in `chronicle-system/`
- `docs/product/chronicle-system/BEHAVIORS_Chronicle_Types.md` - Multiple BEHAVIORS docs in `chronicle-system/`
- `docs/product/chronicle-system/IMPLEMENTATION_Chronicle_System.md` - Multiple IMPLEMENTATION docs in `chronicle-system/`
- `docs/product/business-model/BEHAVIORS_Retention_Mechanisms.md` - Multiple BEHAVIORS docs in `business-model/`
- `docs/product/business-model/PATTERNS_Market_Comparison.md` - Multiple PATTERNS docs in `business-model/`
- `docs/product/business-model/ALGORITHM_Hallucination_Defense.md` - Multiple ALGORITHM docs in `business-model/`
- `docs/product/billing/SYNC_Billing_System.md` - Multiple SYNC docs in `billing/`
- ... and 6 more

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `AGENTS.md` - Escalation marker needs decision

### HARDCODED_CONFIG (8 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `create_project_files_pack_from_maps_and_repo.py` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- `frontend/app/start/page.tsx` - Contains hardcoded configuration values
- `frontend/lib/api.ts` - Contains hardcoded configuration values

---

## LATER

These are minor issues that don't block work but would improve project health:

- [ ] `engine/.pytest_cache/v/cache/lastfailed` - No DOCS: reference in file header
- [ ] `engine/.pytest_cache/v/cache/nodeids` - No DOCS: reference in file header
- [ ] `engine/infrastructure/history/conversations.py` - No DOCS: reference in file header
- [ ] `engine/run.py` - No DOCS: reference in file header
- [ ] `engine/tests/test_behaviors.py` - No DOCS: reference in file header
- [ ] `engine/tests/test_history.py` - No DOCS: reference in file header
- [ ] `engine/tests/test_implementation.py` - No DOCS: reference in file header
- [ ] `engine/tests/test_integration_scenarios.py` - No DOCS: reference in file header
- [ ] `engine/tests/test_models.py` - No DOCS: reference in file header
- [ ] `engine/tests/test_moment_standalone.py` - No DOCS: reference in file header
- ... and 332 more

---

## HANDOFF

**For the next agent:**

Before starting your task, consider addressing critical issues - especially if your work touches affected files. Monoliths and undocumented code will slow you down.

**Recommended first action:** Pick one MONOLITH file you'll be working in and split its largest function into a separate module.

---

*Generated by `ngram doctor`*
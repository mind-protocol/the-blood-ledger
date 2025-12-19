# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (5 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tests/infrastructure/canon` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `tests/infrastructure/world_builder` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/moment_graph` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/tempo` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/world_builder` - No documentation mapping (6 files)
  - Add mapping to modules.yaml

### PLACEHOLDER (1 files)

**What's wrong:** Template placeholders mean the documentation was started but never completed. Agents loading these docs get no useful information.

**How to fix:** Fill in the placeholders with actual content, or delete the file if it's not needed yet.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `.ngram/state/SYNC_Project_State.md` - Contains 1 template placeholder(s)
  - Fill in actual content

### BROKEN_IMPL_LINK (19 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: useGameState.ts, moment.ts, scenarios/page.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: graph_ops.py, narrator.py, playthroughs/{id}/current_action.json
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: WorldRunnerService.__init__, WorldRunnerService.process_flips, agents/world_runner/CLAUDE_PROMPT.md
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: DOCS: docs/world/map/PATTERNS_Map.md, SemanticSearch.find, 0.3
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - References 17 non-existent file(s)
  - Update or remove references: data/scripts/scrape/narrative_rules.py, data/scripts/scrape/*.py, events.yaml
- `docs/design/IMPLEMENTATION_Vision.md` - References 14 non-existent file(s)
  - Update or remove references: ALGORITHM_Opening.md, docs/design/BEHAVIORS_Drives_And_Metrics.md, docs/design/*.md
- `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` - References 10 non-existent file(s)
  - Update or remove references: engine/infrastructure/memory/moment_ids.py, moment_processor.py, moment_processor.py:MomentProcessor.__init__
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` - References 9 non-existent file(s)
  - Update or remove references: EmbeddingService.embed_node, EmbeddingService._load_model, service.py
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - References 10 non-existent file(s)
  - Update or remove references: engine/infrastructure/history/queries.py, DOCS: docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md, HistoryService.record_player_history
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue
- ... and 9 more

### YAML_DRIFT (1 files)

**What's wrong:** modules.yaml references paths that don't exist. Agents trusting this manifest will look for code/docs that aren't there, wasting time and causing confusion.

**How to fix:** Update modules.yaml to match current file structure, or create the missing paths, or remove stale module entries.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `modules.yaml#scene-memory` - Module 'scene-memory' has 1 drift issue(s)
  - tests path 'engine/tests/test_moment*.py' not found

### INCOMPLETE_CHAIN (2 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/infrastructure/tempo` - Missing: PATTERNS, BEHAVIORS, VALIDATION, TEST
- `docs/infrastructure/world-builder` - Missing: PATTERNS, BEHAVIORS

### INCOMPLETE_IMPL (15 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/infrastructure/tempo/tempo_controller.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/world_builder/world_builder.py` - Contains 2 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 3 empty/incomplete function(s)
- ... and 5 more

### LARGE_DOC_MODULE (10 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 102K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 81K chars (threshold: 50K)
- `docs/world/map` - Total 94K chars (threshold: 50K)
- `docs/physics` - Total 236K chars (threshold: 50K)
- `docs/schema` - Total 69K chars (threshold: 50K)
- `docs/design` - Total 61K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 79K chars (threshold: 50K)
- `docs/infrastructure/history` - Total 57K chars (threshold: 50K)
- `docs/infrastructure/async` - Total 52K chars (threshold: 50K)
- `docs/infrastructure/world-builder` - Total 63K chars (threshold: 50K)

### STALE_IMPL (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - 5 referenced files not found
- `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` - 3 referenced files not found
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - 4 referenced files not found
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` - 3 referenced files not found
- `docs/infrastructure/ops-scripts/IMPLEMENTATION_Engine_Scripts_Layout.md` - 2 referenced files not found
- `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md` - 3 referenced files not found
- `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md` - 5 referenced files not found

### DOC_DUPLICATION (3 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/map/PATTERNS_Parchment_Map_View.md` - Multiple PATTERNS docs in `map/`
- `docs/frontend/map/SYNC_Map_View.md` - Multiple SYNC docs in `map/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### HARDCODED_CONFIG (14 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `frontend/components/SpeedControl.tsx` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- ... and 4 more

---


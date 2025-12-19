# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (38 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `frontend` - No documentation mapping (51 files)
  - Add mapping to modules.yaml
- `frontend/components` - No documentation mapping (32 files)
  - Add mapping to modules.yaml
- `frontend/components/voices` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/chronicle` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/panel` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `frontend/components/debug` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/minimap` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/moment` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `frontend/components/scene` - No documentation mapping (12 files)
  - Add mapping to modules.yaml
- `frontend/components/ui` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- ... and 28 more

### BROKEN_IMPL_LINK (3 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: hooks/transformers.ts, game-state.json, start/page.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: playthroughs/{id}/PROFILE_NOTES.md, graph_ops.py, engine/infrastructure/orchestration/narrator_prompt.py
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue

### INCOMPLETE_CHAIN (10 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/world-runner` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/map` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- `docs/infrastructure/cli-tools` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/infrastructure/image-generation` - Missing: IMPLEMENTATION

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 3 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_ops_events.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 107K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 65K chars (threshold: 50K)
- `docs/world/map` - Total 59K chars (threshold: 50K)
- `docs/physics` - Total 237K chars (threshold: 50K)
- `docs/schema` - Total 109K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 66K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/ALGORITHM_Prompt_Structure.md` - Multiple ALGORITHM docs in `narrator/`
- `docs/agents/narrator/PATTERNS_World_Building.md` - Multiple PATTERNS docs in `narrator/`
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Multiple ALGORITHM docs in `world-runner/`
- `docs/world/map/ALGORITHM_Rendering.md` - Multiple ALGORITHM docs in `map/`
- `docs/world/scraping/ALGORITHM_Pipeline.md` - Multiple ALGORITHM docs in `scraping/`
- `docs/physics/ALGORITHM_Input.md` - Multiple ALGORITHM docs in `physics/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`
- `docs/schema/VALIDATION_Graph.md` - Multiple VALIDATION docs in `schema/`
- `docs/infrastructure/async/ALGORITHM_Hook_Injection.md` - Multiple ALGORITHM docs in `async/`

### HARDCODED_CONFIG (12 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/lib/api.ts` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- `frontend/app/start/page.tsx` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- ... and 2 more

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (38 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `frontend` - No documentation mapping (51 files)
  - Add mapping to modules.yaml
- `frontend/components` - No documentation mapping (32 files)
  - Add mapping to modules.yaml
- `frontend/components/voices` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/chronicle` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/panel` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `frontend/components/debug` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/minimap` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `frontend/components/moment` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `frontend/components/scene` - No documentation mapping (12 files)
  - Add mapping to modules.yaml
- `frontend/components/ui` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- ... and 28 more

### BROKEN_IMPL_LINK (3 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: useMoments.ts, api.ts, env.local
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: playthroughs/{id}/PROFILE_NOTES.md, narrator.py, playthroughs/{id}/current_action.json
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue

### INCOMPLETE_CHAIN (10 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/world-runner` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/map` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- `docs/infrastructure/cli-tools` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/infrastructure/image-generation` - Missing: IMPLEMENTATION

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 3 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_ops_events.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 107K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 65K chars (threshold: 50K)
- `docs/world/map` - Total 59K chars (threshold: 50K)
- `docs/physics` - Total 237K chars (threshold: 50K)
- `docs/schema` - Total 109K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 66K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/ALGORITHM_Prompt_Structure.md` - Multiple ALGORITHM docs in `narrator/`
- `docs/agents/narrator/PATTERNS_World_Building.md` - Multiple PATTERNS docs in `narrator/`
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Multiple ALGORITHM docs in `world-runner/`
- `docs/world/map/ALGORITHM_Rendering.md` - Multiple ALGORITHM docs in `map/`
- `docs/world/scraping/ALGORITHM_Pipeline.md` - Multiple ALGORITHM docs in `scraping/`
- `docs/physics/ALGORITHM_Input.md` - Multiple ALGORITHM docs in `physics/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`
- `docs/schema/VALIDATION_Graph.md` - Multiple VALIDATION docs in `schema/`
- `docs/infrastructure/async/ALGORITHM_Hook_Injection.md` - Multiple ALGORITHM docs in `async/`

### HARDCODED_CONFIG (12 files)

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
- `frontend/lib/api.ts` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- ... and 2 more

---


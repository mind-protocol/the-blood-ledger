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
  - Update or remove references: page.tsx, GameClient.tsx, lib/api/moments.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: graph_ops.py, playthroughs/{id}/PROFILE_NOTES.md, narrator.py
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
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
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
  - Update or remove references: layout.tsx, GameClient.tsx, start/page.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: engine/infrastructure/orchestration/narrator_prompt.py, narrator.py, stream_dialogue.py
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
- `docs/physics` - Total 238K chars (threshold: 50K)
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

- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- `frontend/app/start/page.tsx` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
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
  - Update or remove references: map.ts, api.ts, lib/api/moments.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: narrator.py, narrator_prompt.py, graph_ops.py
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
- `docs/physics` - Total 238K chars (threshold: 50K)
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
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
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
  - Update or remove references: api.ts, playthroughs/[id]/page.tsx, map/page.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: stream_dialogue.py, playthroughs/{id}/current_action.json, engine/infrastructure/orchestration/narrator_prompt.py
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

### INCOMPLETE_IMPL (13 files)

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
- ... and 3 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 107K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 65K chars (threshold: 50K)
- `docs/world/map` - Total 59K chars (threshold: 50K)
- `docs/physics` - Total 239K chars (threshold: 50K)
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
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
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
  - Update or remove references: Providers.tsx, game-state.json, hooks/transformers.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: engine/infrastructure/orchestration/narrator_prompt.py, graph_ops.py, narrator.py
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

### INCOMPLETE_IMPL (13 files)

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
- ... and 3 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 102K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 64K chars (threshold: 50K)
- `docs/world/map` - Total 79K chars (threshold: 50K)
- `docs/physics` - Total 235K chars (threshold: 50K)
- `docs/schema` - Total 69K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 66K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/PATTERNS_World_Building.md` - Multiple PATTERNS docs in `narrator/`
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Multiple ALGORITHM docs in `world-runner/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`
- `docs/infrastructure/async/ALGORITHM_Hook_Injection.md` - Multiple ALGORITHM docs in `async/`

### HARDCODED_CONFIG (12 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/lib/api.ts` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
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
  - Update or remove references: useGameState.ts, hooks/transformers.ts, components/scene/CenterStageContent.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: playthroughs/{id}/PROFILE_NOTES.md, engine/infrastructure/orchestration/narrator_prompt.py, playthroughs/{id}/current_action.json
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue

### INCOMPLETE_CHAIN (10 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/world-runner` - Missing: IMPLEMENTATION, TEST
- `docs/world/map` - Missing: IMPLEMENTATION, TEST
- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- `docs/infrastructure/cli-tools` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/infrastructure/image-generation` - Missing: IMPLEMENTATION

### INCOMPLETE_IMPL (13 files)

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
- ... and 3 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 102K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 69K chars (threshold: 50K)
- `docs/world/map` - Total 83K chars (threshold: 50K)
- `docs/physics` - Total 235K chars (threshold: 50K)
- `docs/schema` - Total 110K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 66K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/PATTERNS_World_Building.md` - Multiple PATTERNS docs in `narrator/`
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Multiple ALGORITHM docs in `world-runner/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`
- `docs/schema/VALIDATION_Graph.md` - Multiple VALIDATION docs in `schema/`

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
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- ... and 2 more

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (35 files)

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
- ... and 25 more

### BROKEN_IMPL_LINK (6 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: Providers.tsx, api.ts, playthroughs/[id]/page.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: playthroughs/{id}/PROFILE_NOTES.md, narrator_prompt.py, stream_dialogue.py
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md, agents/world_runner/CLAUDE_PROMPT.md, WorldRunnerService.process_flips
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service.md` - References 5 non-existent file(s)
  - Update or remove references: WorldRunnerService.timeout, # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md, WorldRunnerService.process_flips
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: 0.3, DOCS: docs/world/map/PATTERNS_Map.md, SemanticSearch.find
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue

### INCOMPLETE_CHAIN (8 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- `docs/infrastructure/cli-tools` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/infrastructure/image-generation` - Missing: IMPLEMENTATION

### INCOMPLETE_IMPL (13 files)

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
- ... and 3 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 102K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 88K chars (threshold: 50K)
- `docs/world/map` - Total 94K chars (threshold: 50K)
- `docs/physics` - Total 235K chars (threshold: 50K)
- `docs/schema` - Total 69K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 66K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/PATTERNS_World_Building.md` - Multiple PATTERNS docs in `narrator/`
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Multiple ALGORITHM docs in `world-runner/`
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - Multiple IMPLEMENTATION docs in `world-runner/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`

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

### UNDOCUMENTED (33 files)

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
- ... and 23 more

### BROKEN_IMPL_LINK (6 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: components/scene/CenterStageContent.tsx,  DOCS: docs/frontend/PATTERNS_Presentation_Layer.md, Providers.tsx
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: stream_dialogue.py, narrator.py, playthroughs/{id}/current_action.json
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: WorldRunnerService.__init__, WorldRunnerService.process_flips, # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service.md` - References 5 non-existent file(s)
  - Update or remove references: WorldRunnerService.working_dir, WorldRunnerService.__init__, WorldRunnerService.process_flips
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: DOCS: docs/world/map/PATTERNS_Map.md, SemanticSearch.find, 0.3
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue

### INCOMPLETE_CHAIN (8 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- `docs/infrastructure/cli-tools` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/infrastructure/image-generation` - Missing: IMPLEMENTATION

### INCOMPLETE_IMPL (13 files)

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
- ... and 3 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 102K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 88K chars (threshold: 50K)
- `docs/world/map` - Total 94K chars (threshold: 50K)
- `docs/physics` - Total 235K chars (threshold: 50K)
- `docs/schema` - Total 69K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 66K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/PATTERNS_World_Building.md` - Multiple PATTERNS docs in `narrator/`
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Multiple ALGORITHM docs in `world-runner/`
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - Multiple IMPLEMENTATION docs in `world-runner/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`

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

### UNDOCUMENTED (35 files)

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
- ... and 25 more

### BROKEN_IMPL_LINK (7 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: api.ts, page.tsx, map.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: narrator_prompt.py, playthroughs/{id}/current_action.json, stream_dialogue.py
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: WorldRunnerService.process_flips, agents/world_runner/CLAUDE_PROMPT.md, # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service.md` - References 5 non-existent file(s)
  - Update or remove references: WorldRunnerService.process_flips, # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md, WorldRunnerService.working_dir
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: DOCS: docs/world/map/PATTERNS_Map.md, SemanticSearch.find, 0.3
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md` - References 6 non-existent file(s)
  - Update or remove references: # DOCS: docs/infrastructure/canon/IMPLEMENTATION_Canon.md, time.py, 0.6

### INCOMPLETE_CHAIN (8 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- `docs/infrastructure/cli-tools` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/infrastructure/image-generation` - Missing: IMPLEMENTATION

### INCOMPLETE_IMPL (13 files)

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
- ... and 3 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 102K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 88K chars (threshold: 50K)
- `docs/world/map` - Total 94K chars (threshold: 50K)
- `docs/physics` - Total 236K chars (threshold: 50K)
- `docs/schema` - Total 69K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 67K chars (threshold: 50K)

### STALE_IMPL (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - 28 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 5 referenced files not found

### DOC_DUPLICATION (3 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - Multiple IMPLEMENTATION docs in `world-runner/`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md` - Multiple ALGORITHM docs in `graph/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### HARDCODED_CONFIG (12 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- `frontend/app/start/page.tsx` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- ... and 2 more

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (11 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tests/infrastructure/canon` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/models` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `engine/moments` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/graph/health` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine/physics` - No documentation mapping (15 files)
  - Add mapping to modules.yaml
- `engine/physics/graph` - No documentation mapping (12 files)
  - Add mapping to modules.yaml
- `engine/tests` - No documentation mapping (14 files)
  - Add mapping to modules.yaml
- `engine/moment_graph` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/embeddings` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/tempo` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- ... and 1 more

### BROKEN_IMPL_LINK (15 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: playthroughs/[id]/page.tsx, layout.tsx, useMoments.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: playthroughs/{id}/current_action.json, graph_ops.py, narrator.py
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: WorldRunnerService.__init__, # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md, WorldRunnerService.process_flips
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: SemanticSearch.__init__, 0.3, DOCS: docs/world/map/PATTERNS_Map.md
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - References 17 non-existent file(s)
  - Update or remove references: routes.yaml, data/manual/holdings.yaml, data/scripts/scrape/*.py
- `docs/design/IMPLEMENTATION_Vision.md` - References 14 non-existent file(s)
  - Update or remove references: opening.json, SYNC_Opening.md, docs/design/opening/CLAUDE_Core_Loop.md
- `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` - References 10 non-existent file(s)
  - Update or remove references: MomentProcessor._current_place_id, MomentProcessor.transcript_path, moment_processor.py:MomentProcessor.__init__
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` - References 9 non-existent file(s)
  - Update or remove references: EmbeddingService.model, EmbeddingService.dimension, EmbeddingService.embed_batch
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - References 10 non-existent file(s)
  - Update or remove references: HistoryService.record_player_history, conversations.py, engine/infrastructure/history/recording.py
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue
- ... and 5 more

### YAML_DRIFT (1 files)

**What's wrong:** modules.yaml references paths that don't exist. Agents trusting this manifest will look for code/docs that aren't there, wasting time and causing confusion.

**How to fix:** Update modules.yaml to match current file structure, or create the missing paths, or remove stale module entries.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `modules.yaml#scene-memory` - Module 'scene-memory' has 1 drift issue(s)
  - tests path 'engine/tests/test_moment*.py' not found

### INCOMPLETE_CHAIN (1 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/infrastructure/tempo` - Missing: PATTERNS, BEHAVIORS, VALIDATION, TEST, SYNC

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/infrastructure/tempo/tempo_controller.py` - Contains 2 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 3 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (9 files)

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

### STALE_IMPL (7 files)

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
- `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md` - 3 referenced files not found

### DOC_DUPLICATION (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### HARDCODED_CONFIG (12 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/lib/api.ts` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- ... and 2 more

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (11 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tests/infrastructure/canon` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/models` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `engine/moments` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/graph/health` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine/physics` - No documentation mapping (15 files)
  - Add mapping to modules.yaml
- `engine/physics/graph` - No documentation mapping (12 files)
  - Add mapping to modules.yaml
- `engine/tests` - No documentation mapping (14 files)
  - Add mapping to modules.yaml
- `engine/moment_graph` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/embeddings` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/tempo` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- ... and 1 more

### BROKEN_IMPL_LINK (15 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: game.ts, GameClient.tsx, map.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: stream_dialogue.py, narrator_prompt.py, playthroughs/{id}/current_action.json
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: WorldRunnerService.process_flips, agents/world_runner/CLAUDE_PROMPT.md, WorldRunnerService.__init__
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: 0.3, SemanticSearch.__init__, SemanticSearch.find
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - References 17 non-existent file(s)
  - Update or remove references: routes.yaml, places.yaml, data/world/*.yaml
- `docs/design/IMPLEMENTATION_Vision.md` - References 14 non-existent file(s)
  - Update or remove references: opening.json, docs/design/opening/CLAUDE_Tool_Reference.md, docs/design/*.md
- `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` - References 10 non-existent file(s)
  - Update or remove references: MomentProcessor._last_moment_id, MomentProcessor.transcript_path, MomentProcessor._current_place_id
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` - References 9 non-existent file(s)
  - Update or remove references: EmbeddingService.embed, service.py, EmbeddingService.similarity
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - References 10 non-existent file(s)
  - Update or remove references: DOCS: docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md, service.py, engine/infrastructure/history/queries.py
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue
- ... and 5 more

### YAML_DRIFT (1 files)

**What's wrong:** modules.yaml references paths that don't exist. Agents trusting this manifest will look for code/docs that aren't there, wasting time and causing confusion.

**How to fix:** Update modules.yaml to match current file structure, or create the missing paths, or remove stale module entries.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `modules.yaml#scene-memory` - Module 'scene-memory' has 1 drift issue(s)
  - tests path 'engine/tests/test_moment*.py' not found

### INCOMPLETE_CHAIN (1 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/infrastructure/tempo` - Missing: PATTERNS, BEHAVIORS, VALIDATION, TEST

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/infrastructure/tempo/tempo_controller.py` - Contains 2 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 3 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (9 files)

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

### STALE_IMPL (7 files)

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
- `docs/infrastructure/cli-tools/IMPLEMENTATION_CLI_Tools_Architecture.md` - 3 referenced files not found

### DOC_DUPLICATION (3 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/map/PATTERNS_Parchment_Map_View.md` - Multiple PATTERNS docs in `map/`
- `docs/frontend/map/SYNC_Map_View.md` - Multiple SYNC docs in `map/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### HARDCODED_CONFIG (13 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/components/SpeedControl.tsx` - Contains hardcoded configuration values
- `frontend/components/chronicle/ChroniclePanel.tsx` - Contains hardcoded configuration values
- `frontend/components/debug/DebugPanel.tsx` - Contains hardcoded configuration values
- `frontend/app/scenarios/page.tsx` - Contains hardcoded configuration values
- `frontend/app/start/page.tsx` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- ... and 3 more

---


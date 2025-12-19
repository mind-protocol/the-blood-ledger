# Archived: SYNC_Project_Health.md

Archived on: 2025-12-19
Original file: SYNC_Project_Health.md

---

## ISSUES

### MONOLITH (3 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/api/app.py` - 1055 lines (threshold: 800)
  - Split: def create_app() (1150L, :112), async def create_playthrough() (152L, :846), async def send_moment() (100L, :1005)
- `engine/db/graph_ops.py` - 2455 lines (threshold: 800)
  - Split: class GraphOps() (2454L, :246), def apply() (383L, :411), def handle_click() (147L, :1755)
- `engine/db/graph_queries.py` - 1334 lines (threshold: 800)
  - Split: class GraphQueries() (1473L, :65), def _get_connected_cluster() (93L, :343), def get_live_moments() (82L, :1340)

### UNDOCUMENTED (4 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `tools/image_generation` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `engine/scripts` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/tests` - No documentation mapping (14 files)
  - Add mapping to modules.yaml

### PLACEHOLDER (1 files)

**What's wrong:** Template placeholders mean the documentation was started but never completed. Agents loading these docs get no useful information.

**How to fix:** Fill in the placeholders with actual content, or delete the file if it's not needed yet.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `.ngram/state/SYNC_Project_State.md` - Contains 1 template placeholder(s)
  - Fill in actual content

### BROKEN_IMPL_LINK (1 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/physics/IMPLEMENTATION_Physics.md` - References 43 non-existent file(s)
  - Update or remove references: 0.8, narrator.py, canon/holder.py

### YAML_DRIFT (1 files)

**What's wrong:** modules.yaml references paths that don't exist. Agents trusting this manifest will look for code/docs that aren't there, wasting time and causing confusion.

**How to fix:** Update modules.yaml to match current file structure, or create the missing paths, or remove stale module entries.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `modules.yaml#world-runner` - Module 'world-runner' has 1 drift issue(s)
  - code path 'agents/world-runner' not found

### STALE_SYNC (7 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/scene/SYNC_Scene.md` - Last updated 367 days ago
- `docs/agents/world-runner/SYNC_World_Runner.md` - Last updated 368 days ago
- `docs/world/map/SYNC_Map.md` - Last updated 368 days ago
- `docs/design/opening/SYNC_Opening.md` - Last updated 367 days ago
- `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md` - Last updated 368 days ago
- `docs/infrastructure/embeddings/SYNC_Embeddings.md` - Last updated 368 days ago
- `docs/infrastructure/history/SYNC_History.md` - Last updated 368 days ago

### INCOMPLETE_CHAIN (11 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/agents/narrator` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/agents/world-runner` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/map` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- ... and 1 more

### STUB_IMPL (1 files)

**What's wrong:** Stub implementations (TODO, NotImplementedError, pass) are placeholders that don't actually work. The code looks complete but fails at runtime.

**How to fix:** Implement the stub functions with actual logic, or mark the file as incomplete in SYNC.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/orchestration/orchestrator.py` - Contains 4 stub indicators

### INCOMPLETE_IMPL (15 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/api/app.py` - Contains 5 empty/incomplete function(s)
- `engine/api/moments.py` - Contains 5 empty/incomplete function(s)
- `engine/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/db/graph_ops.py` - Contains 6 empty/incomplete function(s)
- `engine/db/graph_queries.py` - Contains 6 empty/incomplete function(s)
- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- ... and 5 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 79K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 65K chars (threshold: 50K)
- `docs/world/map` - Total 58K chars (threshold: 50K)
- `docs/physics` - Total 229K chars (threshold: 50K)
- `docs/schema` - Total 109K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 63K chars (threshold: 50K)

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
- `engine/api/app.py` - Contains hardcoded configuration values
- `engine/db/graph_queries.py` - Contains hardcoded configuration values
- `engine/db/graph_ops.py` - Contains hardcoded configuration values
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

### MONOLITH (2 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/physics/graph/graph_ops.py` - 1989 lines (threshold: 800)
  - Split: class GraphOps() (1896L, :246), def apply() (383L, :411), def get_graph() (112L, :2142)
- `engine/physics/graph/graph_queries.py` - 1147 lines (threshold: 800)
  - Split: class GraphQueries() (1270L, :66), def _get_connected_cluster() (93L, :347), def get_live_moments() (82L, :1138)

### UNDOCUMENTED (2 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/scripts` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/tests` - No documentation mapping (14 files)
  - Add mapping to modules.yaml

### BROKEN_IMPL_LINK (1 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/physics/IMPLEMENTATION_Physics.md` - References 47 non-existent file(s)
  - Update or remove references: 0.02, handlers/companion.py, 0.2

### STALE_SYNC (7 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/scene/SYNC_Scene.md` - Last updated 367 days ago
- `docs/agents/world-runner/SYNC_World_Runner.md` - Last updated 368 days ago
- `docs/world/map/SYNC_Map.md` - Last updated 368 days ago
- `docs/design/opening/SYNC_Opening.md` - Last updated 367 days ago
- `docs/infrastructure/scene-memory/SYNC_Scene_Memory.md` - Last updated 368 days ago
- `docs/infrastructure/embeddings/SYNC_Embeddings.md` - Last updated 368 days ago
- `docs/infrastructure/history/SYNC_History.md` - Last updated 368 days ago

### INCOMPLETE_CHAIN (12 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- `docs/agents/narrator` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/agents/world-runner` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/map` - Missing: VALIDATION, IMPLEMENTATION, TEST
- `docs/world/scraping` - Missing: IMPLEMENTATION
- `docs/design` - Missing: IMPLEMENTATION
- `docs/infrastructure/scene-memory` - Missing: IMPLEMENTATION, TEST
- `docs/infrastructure/embeddings` - Missing: IMPLEMENTATION
- `docs/infrastructure/history` - Missing: IMPLEMENTATION
- `docs/infrastructure/async` - Missing: IMPLEMENTATION
- ... and 2 more

### STUB_IMPL (1 files)

**What's wrong:** Stub implementations (TODO, NotImplementedError, pass) are placeholders that don't actually work. The code looks complete but fails at runtime.

**How to fix:** Implement the stub functions with actual logic, or mark the file as incomplete in SYNC.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/infrastructure/orchestration/orchestrator.py` - Contains 4 stub indicators

### INCOMPLETE_IMPL (16 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/app.py` - Contains 4 empty/incomplete function(s)
- `engine/infrastructure/api/moments.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/history/conversations.py` - Contains 3 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/infrastructure/orchestration/orchestrator.py` - Contains 4 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- ... and 6 more

### LARGE_DOC_MODULE (7 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 79K chars (threshold: 50K)
- `docs/agents/world-runner` - Total 65K chars (threshold: 50K)
- `docs/world/map` - Total 58K chars (threshold: 50K)
- `docs/physics` - Total 229K chars (threshold: 50K)
- `docs/schema` - Total 109K chars (threshold: 50K)
- `docs/design` - Total 54K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 63K chars (threshold: 50K)

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


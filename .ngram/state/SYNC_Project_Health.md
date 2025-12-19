# SYNC: Project Health

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: ngram doctor
STATUS: CRITICAL
```

---

## CURRENT STATE

**Health Score:** 0/100

The project has critical issues that will significantly impact agent effectiveness. Address these before starting new work.

| Severity | Count |
|----------|-------|
| Critical | 26 |
| Warning | 49 |
| Info | 210 |

---

## ISSUES

### UNDOCUMENTED (9 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tests/infrastructure/canon` - No documentation mapping (2 files)
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

### BROKEN_IMPL_LINK (16 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md` - References 21 non-existent file(s)
  - Update or remove references: api.ts, map/page.tsx, moment.ts
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 7 non-existent file(s)
  - Update or remove references: narrator_prompt.py, playthroughs/{id}/PROFILE_NOTES.md, narrator.py
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: WorldRunnerService.__init__, agents/world_runner/CLAUDE_PROMPT.md, WorldRunnerService.process_flips
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: 0.3, SemanticSearch.find, SemanticSearch.__init__
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` - References 17 non-existent file(s)
  - Update or remove references: characters.yaml, data/manual/characters.yaml, data/world/*.yaml
- `docs/design/IMPLEMENTATION_Vision.md` - References 14 non-existent file(s)
  - Update or remove references: ALGORITHM_Opening.md, docs/design/opening/opening_part_*.json, docs/design/opening/CLAUDE_Core_Loop.md
- `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` - References 10 non-existent file(s)
  - Update or remove references: moment_processor.py:MomentProcessor.__init__, moment_processor.py, MomentProcessor.__init__
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md` - References 9 non-existent file(s)
  - Update or remove references: EmbeddingService.similarity, service.py, EmbeddingService.dimension
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` - References 10 non-existent file(s)
  - Update or remove references: service.py, conversations.py, engine/infrastructure/history/recording.py
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 1 non-existent file(s)
  - Update or remove references: asyncio.Queue
- ... and 6 more

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
- `docs/infrastructure/world-builder` - Missing: PATTERNS, BEHAVIORS, VALIDATION, TEST, SYNC

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

### HARDCODED_CONFIG (14 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `frontend/hooks/useTempo.ts` - Contains hardcoded configuration values
- `frontend/lib/api.ts` - Contains hardcoded configuration values
- `tools/image_generation/generate_image.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/run.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `frontend/components/SpeedControl.tsx` - Contains hardcoded configuration values
- ... and 4 more

---

## LATER

These are minor issues that don't block work but would improve project health:

- [ ] `engine/graph/health/check_health.py` - No DOCS: reference in file header
- [ ] `engine/graph/health/example_queries.cypher` - No DOCS: reference in file header
- [ ] `engine/graph/health/lint_terminology.py` - No DOCS: reference in file header
- [ ] `engine/graph/health/test_schema.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/api/moments.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/api/playthroughs.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/api/sse_broadcast.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/embeddings/service.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/history/conversations.py` - No DOCS: reference in file header
- [ ] `engine/infrastructure/orchestration/narrator.py` - No DOCS: reference in file header
- ... and 200 more

---

## HANDOFF

**For the next agent:**

Before starting your task, consider addressing critical issues - especially if your work touches affected files. Monoliths and undocumented code will slow you down.

**Recommended first action:** Pick one MONOLITH file you'll be working in and split its largest function into a separate module.

---

*Generated by `ngram doctor`*
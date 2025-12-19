# Repository Map: the-blood-ledger

*Generated: 2025-12-19 10:53*

- **Files:** 327
- **Directories:** 90
- **Total Size:** 3.0M
- **Doc Files:** 204
- **Code Files:** 118
- **Areas:** 8 (docs/ subfolders)
- **Modules:** 28 (subfolders in areas)
- **DOCS Links:** 58 (0.49 avg per code file)

- markdown: 204
- python: 73
- tsx: 33
- typescript: 9
- css: 1
- html: 1
- shell: 1

```mermaid
graph TD
    design_vision[design-vision]
    moment_graph[moment-graph]
    world_map[world-map]
    graph_health[graph-health]
    world_scraping[world-scraping]
    world_runner[world-runner]
    scene_memory[scene-memory]
    async_architecture[async-architecture]
    cli_tools[cli-tools]
    history[history]
    canon[canon]
    image_generation[image-generation]
    embeddings[embeddings]
    infrastructure_async[infrastructure-async]
    infrastructure_api[infrastructure-api]
    ops_scripts[ops-scripts]
    frontend[frontend]
    frontend_types[frontend-types]
    frontend_right_panel[frontend-right-panel]
    frontend_moment_components[frontend-moment-components]
    frontend_minimap[frontend-minimap]
    frontend_map[frontend-map]
    frontend_scenarios[frontend-scenarios]
    frontend_scene[frontend-scene]
    schema_models[schema-models]
    moment_graph_engine[moment-graph-engine]
    engine_test_suite[engine-test-suite]
    physics[physics]
    physics_graph[physics-graph]
```

| Module | Code | Docs | Lines | Files | Dependencies |
|--------|------|------|-------|-------|--------------|
| design-vision | `docs/design/**` | `docs/design/` | 0 | 0 | - |
| moment-graph | `engine/moments/**` | `docs/engine/moments/` | 25 | 1 | - |
| world-map | `engine/world/map/**` | `docs/world/map/` | 267 | 2 | - |
| graph-health | `engine/graph/health/**` | `docs/schema/graph-health/` | 1393 | 3 | - |
| world-scraping | `data/scripts/scrape/**` | `docs/world/scraping/` | 2070 | 5 | - |
| world-runner | `engine/infrastructure/orchestration/world_runner.py` | `docs/agents/world-runner/` | 127 | 1 | - |
| scene-memory | `engine/infrastructure/memory/**` | `docs/infrastructure/scene-memory/` | 512 | 2 | - |
| async-architecture | `engine/scripts/check_injection.py` | `docs/infrastructure/async/` | 40 | 1 | - |
| cli-tools | `tools/**` | `docs/infrastructure/cli-tools/` | 579 | 2 | - |
| history | `engine/infrastructure/history/**` | `docs/infrastructure/history/` | 688 | 3 | - |
| canon | `engine/infrastructure/canon/**` | `docs/infrastructure/canon/` | 389 | 3 | - |
| image-generation | `tools/image_generation/**` | `docs/infrastructure/image-generation/` | 247 | 1 | - |
| embeddings | `engine/infrastructure/embeddings/**` | `docs/infrastructure/embeddings/` | 150 | 2 | - |
| infrastructure-async | `engine/infrastructure/api/playthroughs.py` | `docs/infrastructure/async/` | 477 | 1 | - |
| infrastructure-api | `engine/infrastructure/api/**` | `docs/infrastructure/api/` | 1831 | 6 | - |
| ops-scripts | `engine/scripts/**` | `docs/infrastructure/ops-scripts/` | 414 | 4 | - |
| frontend | `frontend/**` | `docs/frontend/` | 3007511 | 14081 | - |
| frontend-types | `frontend/types/**` | `docs/frontend/` | 485 | 3 | - |
| frontend-right-panel | `frontend/components/panel/**` | `docs/frontend/right-panel/` | 239 | 4 | - |
| frontend-moment-components | `frontend/components/moment/**` | `docs/frontend/scene/` | 632 | 5 | - |
| frontend-minimap | `frontend/components/minimap/**` | `docs/frontend/minimap/` | 213 | 2 | - |
| frontend-map | `frontend/components/map/**` | `docs/frontend/map/` | 828 | 3 | - |
| frontend-scenarios | `frontend/app/scenarios/**` | `docs/frontend/scenarios/` | 194 | 1 | - |
| frontend-scene | `frontend/components/scene/**` | `docs/frontend/scene/` | 1051 | 12 | - |
| schema-models | `engine/models/**` | `docs/schema/models/` | 965 | 5 | - |
| moment-graph-engine | `engine/moment_graph/**` | `docs/engine/moment-graph-engine/` | 858 | 4 | - |
| engine-test-suite | `engine/tests/**` | `docs/engine/tests/` | 5517 | 14 | - |
| physics | `engine/physics/**` | `docs/physics/` | 4897 | 15 | - |
| physics-graph | `engine/physics/graph/**` | `docs/physics/graph/` | 4361 | 12 | - |

```
├── agents/ (85.9K)
│   ├── developer/ (6.4K)
│   │   └── CLAUDE.md (6.4K)
│   ├── narrator/ (43.2K)
│   │   ├── CLAUDE.md (9.8K)
│   │   └── CLAUDE_old.md (33.5K)
│   ├── world-builder/ (12.4K)
│   │   └── CLAUDE.md (12.4K)
│   └── world_runner/ (23.9K)
│       └── CLAUDE.md (23.9K)
├── docs/ (1.7M)
│   ├── agents/ (187.5K)
│   │   ├── narrator/ (102.1K)
│   │   │   ├── ALGORITHM_Scene_Generation.md (28.3K)
│   │   │   ├── BEHAVIORS_Narrator.md (9.1K)
│   │   │   ├── HANDOFF_Rolling_Window_Architecture.md (6.8K)
│   │   │   ├── IMPLEMENTATION_Narrator.md (12.1K)
│   │   │   ├── INPUT_REFERENCE.md (6.8K)
│   │   │   ├── PATTERNS_Narrator.md (2.1K)
│   │   │   ├── SYNC_Narrator.md (4.5K)
│   │   │   ├── TEST_Narrator.md (9.0K)
│   │   │   ├── TOOL_REFERENCE.md (12.6K)
│   │   │   ├── VALIDATION_Narrator.md (7.5K)
│   │   │   └── (..2 more files)
│   │   └── world-runner/ (85.4K)
│   │       ├── ALGORITHM_World_Runner.md (19.4K)
│   │       ├── BEHAVIORS_World_Runner.md (14.4K)
│   │       ├── IMPLEMENTATION_World_Runner_Service_Architecture.md (9.1K)
│   │       ├── INPUT_REFERENCE.md (6.6K)
│   │       ├── PATTERNS_World_Runner.md (8.9K)
│   │       ├── SYNC_World_Runner.md (3.8K)
│   │       ├── TEST_World_Runner_Coverage.md (2.2K)
│   │       ├── TOOL_REFERENCE.md (17.0K)
│   │       └── VALIDATION_World_Runner_Invariants.md (3.8K)
│   ├── design/ (142.9K)
│   │   ├── opening/ (70.5K)
│   │   │   ├── ALGORITHM_Opening.md (915)
│   │   │   ├── BEHAVIORS_Opening.md (6.8K)
│   │   │   ├── CLAUDE.md (26.2K)
│   │   │   ├── CONTENT.md (10.2K)
│   │   │   ├── GUIDE.md (9.5K)
│   │   │   ├── PATTERNS_Opening.md (6.9K)
│   │   │   ├── SYNC_Opening.md (2.2K)
│   │   │   ├── TEST_Opening.md (627)
│   │   │   └── VALIDATION_Opening.md (7.2K)
│   │   ├── scenarios/ (10.3K)
│   │   │   └── README.md (10.3K)
│   │   ├── ALGORITHM_Vision.md (12.5K)
│   │   ├── BEHAVIORS_Vision.md (17.2K)
│   │   ├── IMPLEMENTATION_Vision.md (7.3K)
│   │   ├── PATTERNS_Vision.md (13.9K)
│   │   ├── SYNC_Vision.md (3.9K)
│   │   ├── TEST_Vision.md (1.0K)
│   │   └── VALIDATION_Vision.md (6.2K)
│   ├── engine/ (46.7K)
│   │   ├── moment-graph-engine/ (18.3K)
│   │   │   ├── ALGORITHM_Click_Wait_Surfacing.md (3.1K)
│   │   │   ├── BEHAVIORS_Traversal_And_Surfacing.md (2.4K)
│   │   │   ├── IMPLEMENTATION_Moment_Graph_Runtime_Layout.md (2.4K)
│   │   │   ├── PATTERNS_Instant_Traversal_Moment_Graph.md (3.7K)
│   │   │   ├── SYNC_Moment_Graph_Engine.md (2.7K)
│   │   │   ├── TEST_Moment_Graph_Runtime_Coverage.md (1.8K)
│   │   │   └── VALIDATION_Moment_Traversal_Invariants.md (2.2K)
│   │   ├── moments/ (11.8K)
│   │   │   ├── ALGORITHM_Moment_Graph_Operations.md (1.3K)
│   │   │   ├── BEHAVIORS_Moment_Lifecycle.md (1.4K)
│   │   │   ├── IMPLEMENTATION_Moment_Graph_Stub.md (868)
│   │   │   ├── PATTERNS_Moments.md (3.7K)
│   │   │   ├── SYNC_Moments.md (2.1K)
│   │   │   ├── TEST_Moment_Graph_Coverage.md (1.3K)
│   │   │   └── VALIDATION_Moment_Graph_Invariants.md (1.1K)
│   │   └── tests/ (16.6K)
│   │       ├── ALGORITHM_Test_Run_Flow.md (1.7K)
│   │       ├── BEHAVIORS_Test_Coverage_Layers.md (2.1K)
│   │       ├── IMPLEMENTATION_Test_File_Layout.md (1.9K)
│   │       ├── PATTERNS_Spec_Linked_Test_Suite.md (3.8K)
│   │       ├── SYNC_Engine_Test_Suite.md (3.7K)
│   │       ├── TEST_Test_Suite_Coverage.md (1.8K)
│   │       └── VALIDATION_Test_Suite_Invariants.md (1.5K)
│   ├── frontend/ (85.5K)
│   │   ├── map/ (6.6K)
│   │   │   ├── PATTERNS_Interactive_Travel_Map.md (1.9K)
│   │   │   ├── PATTERNS_Parchment_Map_View.md (1.9K)
│   │   │   └── SYNC_Map_View.md (2.8K)
│   │   ├── minimap/ (3.6K)
│   │   │   ├── PATTERNS_Discovered_Location_Minimap.md (1.8K)
│   │   │   └── SYNC_Minimap.md (1.8K)
│   │   ├── right-panel/ (3.7K)
│   │   │   ├── PATTERNS_Tabbed_Right_Panel.md (2.0K)
│   │   │   └── SYNC_Right_Panel.md (1.7K)
│   │   ├── scenarios/ (3.7K)
│   │   │   ├── PATTERNS_Scenario_Selection.md (1.8K)
│   │   │   └── SYNC_Scenario_Selection.md (1.8K)
│   │   ├── scene/ (15.6K)
│   │   │   ├── ALGORITHM_Scene.md (1.3K)
│   │   │   ├── BEHAVIORS_Scene.md (1.3K)
│   │   │   ├── PATTERNS_Scene.md (5.7K)
│   │   │   ├── SYNC_Scene.md (5.5K)
│   │   │   ├── TEST_Scene.md (839)
│   │   │   └── VALIDATION_Scene.md (1.0K)
│   │   ├── ALGORITHM_Frontend_Data_Flow.md (4.2K)
│   │   ├── BEHAVIORS_Frontend_State_And_Interaction.md (6.6K)
│   │   ├── IMPLEMENTATION_Frontend_Code_Architecture.md (14.1K)
│   │   ├── PATTERNS_Presentation_Layer.md (4.5K)
│   │   ├── SYNC_Frontend.md (9.0K)
│   │   ├── SYNC_Frontend_archive_2025-12.md (3.4K)
│   │   ├── TEST_Frontend_Coverage.md (4.9K)
│   │   └── VALIDATION_Frontend_Invariants.md (5.7K)
│   ├── infrastructure/ (484.8K)
│   │   ├── api/ (26.3K)
│   │   │   ├── ALGORITHM_Api.md (14.4K)
│   │   │   ├── BEHAVIORS_Api.md (711)
│   │   │   ├── IMPLEMENTATION_Api.md (1.9K)
│   │   │   ├── PATTERNS_Api.md (784)
│   │   │   ├── SYNC_Api.md (6.8K)
│   │   │   ├── TEST_Api.md (627)
│   │   │   ├── VALIDATION_Api.md (716)
│   │   │   └── (..1 more files)
│   │   ├── async/ (54.0K)
│   │   │   ├── ALGORITHM_Async_Architecture.md (23.5K)
│   │   │   ├── BEHAVIORS_Travel_Experience.md (3.3K)
│   │   │   ├── IMPLEMENTATION_Async_Architecture.md (7.5K)
│   │   │   ├── PATTERNS_Async_Architecture.md (11.3K)
│   │   │   ├── SYNC_Async_Architecture.md (6.2K)
│   │   │   ├── TEST_Async_Architecture.md (1.1K)
│   │   │   └── VALIDATION_Async_Architecture.md (1.1K)
│   │   ├── canon/ (48.5K)
│   │   │   ├── ALGORITHM_Canon_Holder.md (7.4K)
│   │   │   ├── BEHAVIORS_Canon.md (5.2K)
│   │   │   ├── IMPLEMENTATION_Canon.md (11.6K)
│   │   │   ├── PATTERNS_Canon.md (4.2K)
│   │   │   ├── SYNC_Canon.md (5.0K)
│   │   │   ├── TEST_Canon.md (8.9K)
│   │   │   └── VALIDATION_Canon.md (6.1K)
│   │   ├── cli-tools/ (33.9K)
│   │   │   ├── ALGORITHM_CLI_Tool_Flows.md (4.8K)
│   │   │   ├── BEHAVIORS_CLI_Streaming_And_Image_Output.md (4.9K)
│   │   │   ├── IMPLEMENTATION_CLI_Tools_Architecture.md (7.3K)
│   │   │   ├── PATTERNS_CLI_Agent_Utilities.md (5.4K)
│   │   │   ├── SYNC_CLI_Tools.md (4.7K)
│   │   │   ├── TEST_CLI_Tool_Coverage.md (2.9K)
│   │   │   └── VALIDATION_CLI_Tool_Invariants.md (3.9K)
│   │   ├── embeddings/ (50.3K)
│   │   │   ├── ALGORITHM_Embeddings.md (8.3K)
│   │   │   ├── BEHAVIORS_Embeddings.md (6.5K)
│   │   │   ├── IMPLEMENTATION_Embeddings.md (5.9K)
│   │   │   ├── PATTERNS_Embeddings.md (6.1K)
│   │   │   ├── SYNC_Embeddings.md (5.1K)
│   │   │   ├── SYNC_Embeddings_archive_2025-12.md (2.5K)
│   │   │   ├── TEST_Embeddings.md (8.8K)
│   │   │   └── VALIDATION_Embeddings.md (7.1K)
│   │   ├── history/ (58.8K)
│   │   │   ├── ALGORITHM_History.md (10.6K)
│   │   │   ├── BEHAVIORS_History.md (7.1K)
│   │   │   ├── IMPLEMENTATION_History_Service_Architecture.md (6.5K)
│   │   │   ├── PATTERNS_History.md (5.6K)
│   │   │   ├── SYNC_History.md (5.6K)
│   │   │   ├── SYNC_History_archive_2025-12.md (6.1K)
│   │   │   ├── TEST_History.md (9.6K)
│   │   │   └── VALIDATION_History.md (7.6K)
│   │   ├── image-generation/ (25.8K)
│   │   │   ├── ALGORITHM_Image_Generation.md (1.2K)
│   │   │   ├── BEHAVIORS_Image_Generation.md (1.2K)
│   │   │   ├── IMPLEMENTATION_Image_Generation.md (8.1K)
│   │   │   ├── PATTERNS_Image_Generation.md (10.2K)
│   │   │   ├── SYNC_Image_Generation.md (3.4K)
│   │   │   ├── TEST_Image_Generation.md (877)
│   │   │   └── VALIDATION_Image_Generation.md (856)
│   │   ├── ops-scripts/ (11.9K)
│   │   │   ├── ALGORITHM_Seeding_And_Backfill_Flows.md (1.3K)
│   │   │   ├── BEHAVIORS_Operational_Script_Runbooks.md (1.5K)
│   │   │   ├── IMPLEMENTATION_Engine_Scripts_Layout.md (1.5K)
│   │   │   ├── PATTERNS_Operational_Seeding_And_Backfill_Scripts.md (2.5K)
│   │   │   ├── SYNC_Ops_Scripts.md (3.0K)
│   │   │   ├── TEST_Operational_Scripts.md (887)
│   │   │   └── VALIDATION_Operational_Script_Safety.md (1.2K)
│   │   ├── scene-memory/ (82.0K)
│   │   │   ├── ALGORITHM_Scene_Memory.md (18.9K)
│   │   │   ├── BEHAVIORS_Scene_Memory.md (12.5K)
│   │   │   ├── IMPLEMENTATION_Scene_Memory.md (8.7K)
│   │   │   ├── PATTERNS_Scene_Memory.md (6.7K)
│   │   │   ├── SYNC_Scene_Memory.md (7.9K)
│   │   │   ├── SYNC_Scene_Memory_archive_2025-12.md (3.3K)
│   │   │   ├── TEST_Scene_Memory.md (3.3K)
│   │   │   └── VALIDATION_Scene_Memory.md (20.7K)
│   │   ├── tempo/ (26.7K)
│   │   │   ├── ALGORITHM_Tempo_Controller.md (12.3K)
│   │   │   ├── IMPLEMENTATION_Tempo.md (9.6K)
│   │   │   └── SYNC_Tempo.md (4.8K)
│   │   └── world-builder/ (66.5K)
│   │       ├── ALGORITHM_World_Builder.md (16.4K)
│   │       ├── IMPLEMENTATION_World_Builder.md (23.1K)
│   │       ├── SYNC_World_Builder.md (6.0K)
│   │       ├── TEST_World_Builder.md (11.0K)
│   │       └── VALIDATION_World_Builder.md (10.0K)
│   ├── physics/ (333.5K)
│   │   ├── graph/ (91.9K)
│   │   │   ├── ALGORITHM_Energy_Flow.md (15.3K)
│   │   │   ├── BEHAVIORS_Graph.md (6.6K)
│   │   │   ├── PATTERNS_Graph.md (2.3K)
│   │   │   ├── SYNC_Graph.md (3.5K)
│   │   │   ├── SYNC_Graph_archive_2025-12.md (23.8K)
│   │   │   └── VALIDATION_Living_Graph.md (40.3K)
│   │   ├── ALGORITHM_Physics.md (138.7K)
│   │   ├── API_Physics.md (6.9K)
│   │   ├── BEHAVIORS_Physics.md (11.5K)
│   │   ├── IMPLEMENTATION_Physics.md (35.7K)
│   │   ├── PATTERNS_Physics.md (6.6K)
│   │   ├── SYNC_Physics.md (4.8K)
│   │   ├── SYNC_Physics_archive_2025-12.md (7.1K)
│   │   ├── TEST_Physics.md (16.6K)
│   │   └── VALIDATION_Physics.md (13.8K)
│   ├── schema/ (87.0K)
│   │   ├── graph-health/ (6.6K)
│   │   │   ├── PATTERNS_Graph_Health_Validation.md (2.8K)
│   │   │   └── SYNC_Graph_Health.md (3.8K)
│   │   ├── models/ (10.0K)
│   │   │   ├── PATTERNS_Pydantic_Schema_Models.md (2.1K)
│   │   │   └── SYNC_Schema_Models.md (7.9K)
│   │   ├── SCHEMA.md (48.2K)
│   │   ├── SCHEMA_Moments.md (22.0K)
│   │   └── (..1 more files)
│   ├── world/ (122.5K)
│   │   ├── map/ (95.3K)
│   │   │   ├── ALGORITHM_Rendering.md (57.6K)
│   │   │   ├── BEHAVIORS_Map.md (13.8K)
│   │   │   ├── IMPLEMENTATION_Map_Code_Architecture.md (7.5K)
│   │   │   ├── PATTERNS_Map.md (6.7K)
│   │   │   ├── SYNC_Map.md (3.7K)
│   │   │   ├── TEST_Map_Test_Coverage.md (2.5K)
│   │   │   └── VALIDATION_Map_Invariants.md (3.6K)
│   │   └── scraping/ (27.2K)
│   │       ├── ALGORITHM_Pipeline.md (8.8K)
│   │       ├── BEHAVIORS_World_Scraping.md (1.2K)
│   │       ├── IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md (5.1K)
│   │       ├── PATTERNS_World_Scraping.md (3.0K)
│   │       ├── SYNC_World_Scraping.md (5.2K)
│   │       ├── TEST_World_Scraping.md (932)
│   │       └── VALIDATION_World_Scraping.md (2.9K)
│   └── map.md (224.5K)
├── engine/ (922.9K)
│   ├── graph/ (119.2K)
│   │   └── health/ (119.2K)
│   │       ├── README.md (3.4K)
│   │       ├── check_health.py (14.1K) →
│   │       ├── example_queries.cypher (18.1K)
│   │       ├── lint_terminology.py (14.9K)
│   │       ├── query_outputs.md (23.3K)
│   │       ├── query_results.md (16.2K)
│   │       └── test_schema.py (29.3K)
│   ├── infrastructure/ (248.2K)
│   │   ├── api/ (80.1K)
│   │   │   ├── app.py (30.6K) →
│   │   │   ├── moments.py (17.3K)
│   │   │   ├── playthroughs.py (22.5K)
│   │   │   ├── sse_broadcast.py (2.8K)
│   │   │   ├── tempo.py (6.7K) →
│   │   │   └── (..1 more files)
│   │   ├── canon/ (14.5K)
│   │   │   ├── __init__.py (805) →
│   │   │   ├── canon_holder.py (10.2K) →
│   │   │   └── speaker.py (3.5K) →
│   │   ├── embeddings/ (6.1K)
│   │   │   ├── __init__.py (501) →
│   │   │   └── service.py (5.6K) →
│   │   ├── history/ (34.7K)
│   │   │   ├── README.md (6.7K)
│   │   │   ├── __init__.py (1.6K)
│   │   │   ├── conversations.py (6.7K)
│   │   │   └── service.py (19.8K) →
│   │   ├── memory/ (19.6K)
│   │   │   ├── moment_processor.py (19.4K) →
│   │   │   └── (..1 more files)
│   │   ├── orchestration/ (37.1K)
│   │   │   ├── __init__.py (522)
│   │   │   ├── agent_cli.py (6.2K)
│   │   │   ├── narrator.py (6.5K)
│   │   │   ├── orchestrator.py (19.2K)
│   │   │   └── world_runner.py (4.7K) →
│   │   ├── tempo/ (14.4K)
│   │   │   ├── tempo_controller.py (14.1K) →
│   │   │   └── (..1 more files)
│   │   ├── world_builder/ (41.6K)
│   │   │   ├── __init__.py (1.5K) →
│   │   │   ├── enrichment.py (13.5K) →
│   │   │   ├── query.py (8.1K) →
│   │   │   ├── query_moment.py (5.3K) →
│   │   │   ├── sparsity.py (6.6K) →
│   │   │   └── world_builder.py (6.6K) →
│   │   └── (..1 more files)
│   ├── models/ (38.0K)
│   │   ├── __init__.py (2.4K) →
│   │   ├── base.py (12.8K)
│   │   ├── links.py (7.2K)
│   │   ├── nodes.py (11.0K) →
│   │   └── tensions.py (4.6K)
│   ├── moment_graph/ (32.4K)
│   │   ├── __init__.py (541) →
│   │   ├── queries.py (15.2K)
│   │   ├── surface.py (9.0K)
│   │   └── traversal.py (7.7K)
│   ├── moments/ (896)
│   │   └── __init__.py (896) →
│   ├── physics/ (200.2K)
│   │   ├── graph/ (178.2K)
│   │   │   ├── graph_ops.py (28.6K) →
│   │   │   ├── graph_ops_apply.py (30.4K)
│   │   │   ├── graph_ops_events.py (2.0K)
│   │   │   ├── graph_ops_image.py (5.0K)
│   │   │   ├── graph_ops_links.py (19.9K)
│   │   │   ├── graph_ops_moments.py (20.0K)
│   │   │   ├── graph_queries.py (29.7K)
│   │   │   ├── graph_queries_moments.py (17.7K) →
│   │   │   ├── graph_queries_search.py (12.9K) →
│   │   │   ├── graph_query_utils.py (8.7K) →
│   │   │   └── (..2 more files)
│   │   ├── constants.py (3.7K)
│   │   ├── tick.py (17.7K) →
│   │   └── (..1 more files)
│   ├── scripts/ (18.4K)
│   │   ├── check_injection.py (1.4K) →
│   │   ├── generate_images_for_existing.py (11.4K) →
│   │   ├── inject_to_narrator.py (3.6K) →
│   │   └── seed_moment_sample.py (1.9K) →
│   ├── tests/ (243.1K)
│   │   ├── test_behaviors.py (18.3K)
│   │   ├── test_e2e_moment_graph.py (16.7K)
│   │   ├── test_history.py (15.1K)
│   │   ├── test_implementation.py (28.9K)
│   │   ├── test_integration_scenarios.py (19.9K)
│   │   ├── test_models.py (28.6K)
│   │   ├── test_moment_graph.py (33.3K)
│   │   ├── test_moments_api.py (15.5K)
│   │   ├── test_narrator_integration.py (16.5K)
│   │   ├── test_spec_consistency.py (18.7K)
│   │   └── (..4 more files)
│   ├── world/ (9.8K)
│   │   ├── map/ (9.7K)
│   │   │   ├── semantic.py (9.3K) →
│   │   │   └── (..1 more files)
│   │   └── (..1 more files)
│   ├── .env.example (540)
│   ├── Dockerfile (664)
│   ├── __init__.py (711)
│   ├── init_db.py (8.7K)
│   ├── run.py (1.8K)
│   └── (..1 more files)
├── frontend/ (208.2K)
│   ├── app/ (17.2K)
│   │   ├── map/ (182)
│   │   │   └── (..1 more files)
│   │   ├── scenarios/ (7.0K)
│   │   │   └── page.tsx (7.0K) →
│   │   ├── start/ (6.6K)
│   │   │   └── page.tsx (6.6K) →
│   │   ├── globals.css (1.6K)
│   │   ├── layout.tsx (916) →
│   │   └── page.tsx (778) →
│   ├── components/ (135.5K)
│   │   ├── chronicle/ (4.3K)
│   │   │   └── ChroniclePanel.tsx (4.3K) →
│   │   ├── debug/ (13.1K)
│   │   │   └── DebugPanel.tsx (13.1K) →
│   │   ├── map/ (27.4K)
│   │   │   ├── MapCanvas.tsx (22.7K)
│   │   │   ├── MapClient.tsx (4.7K) →
│   │   │   └── (..1 more files)
│   │   ├── minimap/ (7.8K)
│   │   │   ├── Minimap.tsx (3.8K) →
│   │   │   └── SunArc.tsx (4.0K) →
│   │   ├── moment/ (19.4K)
│   │   │   ├── ClickableText.tsx (3.6K)
│   │   │   ├── MomentDebugPanel.tsx (6.6K)
│   │   │   ├── MomentDisplay.tsx (5.4K)
│   │   │   ├── MomentStream.tsx (3.4K)
│   │   │   └── (..1 more files)
│   │   ├── panel/ (9.3K)
│   │   │   ├── ChronicleTab.tsx (1.6K)
│   │   │   ├── ConversationsTab.tsx (3.1K)
│   │   │   ├── LedgerTab.tsx (2.3K)
│   │   │   └── RightPanel.tsx (2.3K) →
│   │   ├── scene/ (39.1K)
│   │   │   ├── CenterStage.tsx (14.8K)
│   │   │   ├── CharacterRow.tsx (2.4K)
│   │   │   ├── Hotspot.tsx (2.6K)
│   │   │   ├── HotspotRow.tsx (2.8K)
│   │   │   ├── ObjectRow.tsx (2.1K)
│   │   │   ├── SceneBanner.tsx (2.5K)
│   │   │   ├── SceneHeader.tsx (1.1K)
│   │   │   ├── SceneImage.tsx (3.2K)
│   │   │   ├── SceneView.tsx (4.1K) →
│   │   │   ├── SettingStrip.tsx (2.1K)
│   │   │   └── (..2 more files)
│   │   ├── ui/ (3.1K)
│   │   │   └── Toast.tsx (3.1K) →
│   │   ├── voices/ (1.7K)
│   │   │   └── Voices.tsx (1.7K) →
│   │   ├── GameClient.tsx (3.7K)
│   │   ├── GameLayout.tsx (2.9K)
│   │   ├── SpeedControl.tsx (3.5K)
│   │   └── (..1 more files)
│   ├── hooks/ (23.2K)
│   │   ├── useGameState.ts (15.0K) →
│   │   ├── useMoments.ts (5.5K) →
│   │   └── useTempo.ts (2.7K) →
│   ├── lib/ (15.1K)
│   │   ├── map/ (3.6K)
│   │   │   ├── projection.ts (2.7K) →
│   │   │   ├── random.ts (781) →
│   │   │   └── (..1 more files)
│   │   └── api.ts (11.5K) →
│   ├── types/ (15.9K)
│   │   ├── game.ts (9.9K) →
│   │   ├── map.ts (4.1K) →
│   │   └── moment.ts (1.9K) →
│   └── (..4 more files)
├── prompts/ (4.4K)
│   └── discussion_generator.md (4.4K)
├── tests/ (50.8K)
│   └── infrastructure/ (50.8K)
│       ├── canon/ (17.6K)
│       │   ├── test_canon_holder.py (17.5K) →
│       │   └── (..1 more files)
│       └── world_builder/ (33.2K)
│           ├── test_world_builder.py (33.2K) →
│           └── (..1 more files)
├── tools/ (25.2K)
│   ├── image_generation/ (11.4K)
│   │   ├── README.md (2.3K)
│   │   └── generate_image.py (9.2K) →
│   └── stream_dialogue.py (13.7K) →
├── .gitignore (690)
├── .ngramignore (806)
├── AGENTS.md (22.0K)
├── CLAUDE.md (4.0K)
├── README.md (1.6K)
├── project_map.html (12.0K)
└── run.sh (1.0K)
```

**Sections:**
- # Blood Ledger Development
- ## The Game
- ## Nicolas
- ## Our Partnership
- ## My Role
- ## Mind Protocol Connection
- # Context Protocol
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change

**Code refs:**
- `stream_dialogue.py`

**Sections:**
- # Narrator Agent
- ## Quick Reference
- ## When You're Called
- ## Tool Calls
- # Semantic search - returns markdown for LLM consumption
- # Direct Cypher for complex queries
- # playthroughs/default/mutations/flip_aldric_edmund.yaml
- # New narratives (relationships ARE narratives)
- # New moments (type is always "thought")
- # Belief links
- # CAN_SPEAK links (who can voice each moment)
- # ATTACHED_TO links (presence requirements)
- ## Schema Reference
- # Family relationship
- # Sworn oath
- # Enmity
- # NARRATIVE (relationships, memories, knowledge)
- # MOMENT (always type: thought)
- # BELIEF (character believes narrative)
- # CAN_SPEAK (character can voice moment)
- # ATTACHED_TO (moment attached to entity)
- # CAN_LEAD_TO (moment can trigger another)
- # NARRATIVE_LINK (narrative relationships)
- # PRESENT (character at place)
- # CONTAINS (place hierarchy)
- # ABOUT (query→result connections)
- ## The Core Loop
- ## Moment Generation Guidelines
- ## Flip Types
- ## What You Don't Do
- ## File Locations

**Code refs:**
- `stream_dialogue.py`

**Doc refs:**
- `docs/engine/moments/SCHEMA_Moments.md`

**Sections:**
- # Narrator Agent
- ## Quick Reference
- # Query with natural language
- # Persist mutations
- ## 1. Execution Interface
- # Dialogue with inline clickables (graph-native — default)
- # Narration with clickables and tone
- # Signal time elapsed (significant actions only)
- # Signal completion
- # LEGACY MODE (not recommended) — Use --legacy-mode to write to scene.json
- ## 2. The Two Paths
- # First read PROFILE_NOTES.md for player context
- ## 3. What You Produce
- ## 4. Clickable Words
- ## 5. Party Dynamics
- ## 6. Player Psychology
- ## 7. The World
- ## 8. The Feelings We Create
- ## 9. Your Role
- ## 10. The Living World
- ## 11. Core Principles
- # Graph Schema Reference
- ## Nodes
- # For groups:
- # For action moments:
- # For query moments:
- ## Key Links

**Sections:**
- # World Builder Agent
- ## Quick Reference
- ## Core Insight
- ## When You're Called
- ## Tool Calls
- # Get character info
- # Direct Cypher
- # playthroughs/default/mutations/enrich_aldric_relatives.yaml
- # New characters
- # New place
- # New thing
- # RELATIONSHIPS AS NARRATIVES (not RELATED_TO links!)
- # Thought moments (type is always "thought")
- # BELIEF links (characters believe the relationship narratives)
- # PRESENT links (where characters are)
- # LOCATED links (where things are)
- # CAN_SPEAK links
- # ATTACHED_TO links
- # ABOUT links (connect all created content to query moment)
- ## Schema Reference
- # CHARACTER
- # PLACE
- # THING
- # NARRATIVE (includes relationships!)
- # MOMENT (always type: thought)
- # BELIEF (how characters know narratives/relationships)
- # PRESENT (character at place)
- # LOCATED (thing at place)
- # CAN_SPEAK
- # ATTACHED_TO
- # NARRATIVE_LINK (narrative relationships)
- # GEOGRAPHY (place connections)
- # CONTAINS (place hierarchy)
- # ABOUT (query→result connections - used by World Builder)
- ## The Setting
- ## Sparsity Triggers
- ## What You Don't Do
- ## File Locations
- ## Caching

**Sections:**
- # World Runner Agent
- ## Quick Reference
- ## 1. Global Context
- ## 2. Our Aim
- ## 3. Your Role
- ## 4. When You're Called
- ## 5. Execution Interface
- # Seeds and arc plans live in narrator_notes fields
- # Get tension details and involved narratives
- # Get character locations
- # Natural language search
- # If result indicates failure, read feedback and retry
- ## 6. Processing Steps
- ## 7. What You Produce
- # mutations/wr_{flip_id}.yaml
- ## 8. Guidelines
- ## 9. Authorship Principles
- # Graph Schema Reference
- ## Nodes
- # NOTE: "where" is expressed via OCCURRED_AT link to Place, not an attribute
- # NOTE: Speaker is NOT an attribute. Use SAID link: Character -[SAID]-> Moment
- ## Links
- # OCCURRED_AT link — no properties, just indicates where the narrative event took place
- # CONTAINS (hierarchy) — no attributes needed, relationship is binary
- # place_york CONTAINS place_york_market CONTAINS place_merchants_hall CONTAINS place_back_room
- # ROUTE (travel between settlements/regions) — computed from waypoints
- # Road type speeds (km/h on foot):
- # roman: 5.0, track: 3.5, path: 2.5, river: 8.0 (downstream), none: 1.5 (cross-country)
- ## Tensions
- ## Modifiers
- ## Moment Links

**Sections:**
- # Narrator — Algorithm: Scene Generation
- ## CHAIN
- ## Purpose
- ## The Orchestration
- ## File Locations
- ## Prompt Structure
- ## World Injection Block
- ## Scene Context Block
- ## Generation Instructions
- ## Required Output Schema
- ## Time Elapsed Guidelines
- ## Handling Different Injection Types
- ## Orchestrator Pseudocode
- # 1. Check for world injection
- # 2. Build prompt
- # 3. Call narrator (--continue maintains thread)
- # 4. Parse output
- # 5. Apply mutations to graph
- # 6. Clear injection (consumed)
- # 7. Trigger graph tick with time_elapsed
- # 8. If flips, run World Runner
- # 9. Return scene for frontend
- ## Two Generation Modes
- ## Input: Scene Context
- ## Conversational Generation
- ## Significant Generation
- ## SceneTree Structure
- ## Character Voice Guidelines
- ## Voice Generation
- ## Clickable Word Selection
- ## Invention Guidelines
- ## Background Generation
- ## Rolling Window Generation
- ## Thread Continuity
- # First scene of playthrough
- # All subsequent scenes
- ## Quality Control

**Sections:**
- # Narrator — Behaviors: What the Narrator Produces
- ## Two Response Modes
- ## Dialogue Chunks
- ## Graph Mutations
- ## Scene Package (Significant Actions Only)
- ## Complete Output Schema
- ## time_elapsed Guidelines
- ## Input: World Injection
- ## Quality Indicators
- ## Example: Conversational Response

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`

**Sections:**
- # Handoff — Rolling Window Architecture
- ## The Problem
- ## The Solution: Rolling Window
- ## Why SSE (Not WebSocket)
- ## API Design
- ## Frontend Responsibilities
- ## Backend Responsibilities
- ## Generation Queue
- # 1. Return cached response immediately
- # 2. Queue generation for new clickables
- # 1. Call narrator
- # 2. Cache it
- # 3. Push to frontend
- ## Edge Cases
- ## Narrator Prompt Implications
- ## Open Questions
- ## Files Changed
- ## Next Steps

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_queries.py`
- `narrator_prompt.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `playthroughs/kl/PROFILE_NOTES.md`

**Sections:**
- # Narrator — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Narrator Input Reference
- ## Script Locations
- ## Prompt Structure
- ## Scene Context (Always Provided)
- ## World Injection (If Flips Occurred)
- ## Complete Example Input
- ## Handling World Injection
- ## Query Patterns

**Doc refs:**
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`

**Sections:**
- # Narrator — Patterns: Why This Design
- ## Core Insight
- ## Design Principles
- ## Pre-Generation Model
- ## What the Narrator Controls
- ## Free Input (Exception)
- ## Workflow (High Level)
- ## CHAIN

**Code refs:**
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/physics/graph_tick.py`

**Doc refs:**
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/PATTERNS_World_Building.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/TEST_Narrator.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`

**Sections:**
- # Narrator — Current State
- ## CHAIN
- ## Documentation Status
- ## RECENT CHANGES
- ## Recent Updates
- ## Open Questions (Resolved)
- ## Remaining Work
- ## ARCHIVE

**Code refs:**
- `engine/tests/test_narrator_integration.py`

**Sections:**
- # Narrator — Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## BEHAVIORAL TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run narrator integration tests
- # Run with coverage
- # Run schema validation tests
- # Manual test: invoke narrator directly
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GOLD STANDARD SESSIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Narrator Tool Reference
- ## How To Use
- # First call (starts persistent session)
- # Subsequent calls (continues session)
- # Test with a scene context
- # Parse Narrator output
- # Validate mutations
- # Validate against Pydantic model
- # ...
- ## Complete Output Schema
- ## Scene Package
- ## Time Elapsed
- ## Graph Mutations
- ## Seeds
- ## Complete Example
- ## Validation Rules
- ## JSON Schema (for programmatic validation)

**Sections:**
- # Narrator — Validation: Behavioral Invariants and Output Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # Run narrator integration tests
- # Validate mutation schemas
- # Load narrator output and validate
- # Check clickable validity
- ## EXPERIENCE VALIDATION
- ## QUALITY GATES
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Runner — Algorithm: How It Works
- ## Core Principle: Runner Owns the Tick Loop
- # Run one graph tick (5 min)
- # Check for flips
- # Interrupt — something happened TO THE PLAYER
- # Process non-player flips (world keeps moving)
- # Completed without interruption
- ## Graph Ticks vs Narrative Flips
- ## The Full Flow
- ## The Trigger
- ## Player Context
- # Calculate position along path based on tick
- ## affects_player() — The Load-Bearing Function
- # Spatial: flip at player's current location?
- # Direct: flip involves player character?
- # Companion: flip involves someone traveling with player?
- # High-stakes: flip is critical enough to reach player?
- ## Stateless Between Calls
- ## Graph Ticks vs Narrative Flips
- ## Step 1: Energy Flow
- ## Step 2: Identify Breaks
- ## Step 3: Process Breaks
- ## Step 4: Cascade Resolution
- # Check if break created new unstable tensions
- # Check if belief changes destabilized anything
- ## Step 5: News Propagation
- # Calculate spread distance based on time and significance
- # News may mutate as it travels
- # Characters at location may hear
- ## Step 6: Build and Return Injection
- ## Time Scale: Tick Count
- ## Player Intersection Detection
- ## Implementation Architecture
- # 1. Run graph tick (mechanical, no LLM)
- # 2. Check for player-affecting flips
- # INTERRUPT - call LLM to generate event
- # 3. Process non-player flips (world moves)
- # 4. Propagate news
- # Completed without interruption
- ## What Triggers the Runner?
- # Narrator spawns Runner as background task
- # Narrator continues (or waits for result)
- ## Flip Context: The Cluster
- # The flipped tension itself
- # Narratives in the tension
- # Characters who believe those narratives
- # Places involved
- # Connected narratives (1 hop)
- ## CHAIN

**Sections:**
- # World Runner — Behaviors: What It Produces
- ## The Injection Interface
- ## Injection: Interrupted
- ## Injection as Markdown (Narrator Input)
- # WORLD INJECTION
- ## Status: INTERRUPTED
- ## EVENT: Ambush on the Road
- ## CLUSTER: Relevant Nodes
- ## WORLD CHANGES (Background)
- ## NEWS AVAILABLE
- ## Injection: Completed
- # WORLD INJECTION
- ## Status: COMPLETED
- ## WORLD CHANGES (While You Traveled)
- ## NEWS AVAILABLE
- ## ARRIVAL: York
- ## Injection Queue (In-Scene Events)
- ## INJECTION QUEUE
- ## Event (For Interrupts)
- ## WorldChange (For Background Events)
- ## News (What Player Could Hear)
- ## Time Estimates (for Narrator)
- ## Graph Mutations (Applied During Run)
- ## Output by Duration
- ## The Resume Pattern
- ## CHAIN
- ## CHAIN

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`

**Doc refs:**
- `agents/world_runner/CLAUDE.md`

**Sections:**
- # World Runner — Implementation: Service Architecture and Boundaries
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Runner Input Reference
- ## Script Location
- ## Prompt Structure
- ## Flip Context (Why You're Called)
- ## Graph Context (What You Need to Know)
- ## Player Context (Where Player Is)
- ## Complete Example Input
- ## Processing Guidance
- ## CHAIN

**Sections:**
- # World Runner — Patterns: Why This Shape
- ## The Core Insight
- ## The Interrupt/Resume Pattern
- ## Stateless vs Persistent
- ## Why Separation Matters
- ## When Does Runner Run?
- ## What The World Runner Is NOT
- ## The Injection Contract
- ## Urgency Becomes Real
- ## Connection to Energy/Weight
- ## The Player Experience
- ## The Critical Function: affects_player()
- # Spatial: Is the flip at player's current location?
- # Direct: Does the flip involve the player?
- # Companion: Does it involve someone WITH the player?
- # Critical urgency reaching player's area?
- ## CHAIN
- ## CHAIN

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/orchestration/world_runner.py`

**Doc refs:**
- `agents/world_runner/CLAUDE.md`

**Sections:**
- # World Runner — Sync: Current State
- ## Current State
- ## Documentation Status
- ## Integration
- ## Notes
- ## Updates
- ## CHAIN

**Sections:**
- # World Runner — Test: Coverage and Gaps
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # No test suite currently exists for this module.
- # Proposed location:
- # pytest tests/agents/world_runner/
- ## KNOWN TEST GAPS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Runner Tool Reference
- ## Complete Output Schema
- ## CHAIN
- ## Graph Mutations
- ## World Injection
- ## Complete Example
- ## Validation Rules
- ## Processing Order
- ## JSON Schema (for programmatic validation)

**Code refs:**
- `engine/infrastructure/orchestration/world_runner.py`

**Sections:**
- # World Runner — Validation: Service Invariants and Failure Behavior
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # No automated tests for World Runner service yet.
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # The Opening — Algorithm
- ## CHAIN

**Sections:**
- # The Opening — Behaviors: Player Experience
- ## CHAIN
- ## WHAT THE PLAYER EXPERIENCES
- ## INPUT / OUTPUT
- ## OBSERVABLE BEHAVIORS
- ## EDGE CASES
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `tools/stream_dialogue.py`

**Doc refs:**
- `docs/design/opening/GUIDE.md`

**Sections:**
- # Narrator Agent
- ## Quick Reference
- # Query with natural language
- # Persist mutations
- ## 1. Execution Interface
- # Dialogue with inline clickables
- # Narration with clickables
- # Scene with pre-baked responses
- # Signal time elapsed (significant actions only)
- # Signal completion
- ## 2. The Two Paths
- ## 3. What You Produce
- ## 4. Clickable Words
- ## 5. Player Psychology
- ## 6. The World
- ## 7. The Feelings We Create
- ## 8. Your Role
- ## 9. The Living World
- ## 10. Core Principles
- ## 11. Opening Sequence
- # Wait pattern
- # Check if answer arrived in hook
- # Player Profile (Opening)
- ## Answers So Far
- ## Emerging Pattern
- ## Payoff Elements (draft)
- # Graph Schema Reference
- ## Nodes
- ## Links
- ## Tensions
- ## Modifiers

**Sections:**
- # The Opening — Content
- ## THE STATIC QUESTIONS
- ## COMPANION REFLECTION TEMPLATE
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # The Opening — Narrator Guide
- ## What This Is
- ## Your Job
- ## The Beats
- ## What You're Learning
- ## The Pause
- ## The Payoff
- ## Tone Matching
- ## Edge Cases
- ## What Success Looks Like
- ## Example Payoff
- ## After the Payoff

**Sections:**
- # The Opening — Pattern
- ## CHAIN
- ## THE INSIGHT
- ## THE DESIGN PHILOSOPHY
- ## WHY THIS WORKS
- ## WHAT THIS PATTERN DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/orchestration/opening.py`
- `engine/orchestration/opening.py`

**Sections:**
- # The Opening — Sync
- ## Chain Reference
- ## Current State
- ## Code Locations
- ## Upcoming Work
- ## Notes

**Sections:**
- # The Opening — Tests
- ## CHAIN
- ## Planned Checks

**Sections:**
- # The Opening — Validation
- ## CHAIN
- ## SUCCESS CRITERIA
- ## INVARIANTS
- ## METRICS (if we instrument)
- ## TEST SCENARIOS
- ## POST-OPENING VERIFICATION
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/scenarios/page.tsx`

**Sections:**
- # Scenario System
- ## The Five Scenarios
- ## Directory Structure
- ## Scenario YAML Structure
- # =============================================================================
- # METADATA
- # =============================================================================
- # =============================================================================
- # PRE-EXISTING NODES (already in seed - reference only)
- # =============================================================================
- # =============================================================================
- # NEW NODES (created by this scenario)
- # =============================================================================
- # Player character
- # name/gender filled at runtime
- # Companion (if new)
- # Things
- # Narratives
- # =============================================================================
- # LINKS
- # =============================================================================
- # Location
- # Things carried
- # Beliefs
- # =============================================================================
- # COMPANION
- # =============================================================================
- # =============================================================================
- # OPENING
- # =============================================================================
- ## Things by Scenario
- ## Historical Grounding
- ## API Endpoint
- ## Playthrough Folder Structure
- ## Frontend Flow
- ## Companions
- ## Adding New Scenarios
- ## Design Principles

**Sections:**
- # Vision — Algorithm: Systems That Create Engagement
- ## Purpose
- ## Architecture: Two Layers
- ## Engine Systems (Preliminary)
- ## Presentation Systems (Preliminary)
- ## What's Missing?
- ## Systems → Drives (Preliminary Mapping)
- ## Implementation Thinking (Very Preliminary)
- ## Links to Detailed Documentation
- ## My Current Uncertainties
- ## Evolution Notes

**Sections:**
- # Vision — Behaviors: The Player Experience
- ## What the Player Does
- ## The Arc of a Playthrough
- ## Observable Behaviors by View
- ## Key Experience Moments
- ## Core Drives: Octalysis Framework
- ## Anti-Patterns to Avoid
- ## Grounding: Beyond Text
- ## Engagement Levers
- ## Metrics (If We Could Measure)

**Doc refs:**
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Drives_And_Metrics.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
- `docs/design/opening/ALGORITHM_Opening.md`
- `docs/design/opening/BEHAVIORS_Opening.md`
- `docs/design/opening/CLAUDE.md`
- `docs/design/opening/CLAUDE_Core_Loop.md`
- `docs/design/opening/CLAUDE_Tool_Reference.md`
- `docs/design/opening/CONTENT.md`
- `docs/design/opening/GUIDE.md`
- `docs/design/opening/PATTERNS_Opening.md`
- `docs/design/opening/SYNC_Opening.md`
- `docs/design/opening/TEST_Opening.md`
- `docs/design/opening/VALIDATION_Opening.md`
- `docs/design/scenarios/README.md`

**Sections:**
- # Vision - Implementation: Documentation Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Vision — Patterns: Why This Design
- ## The Core Insight
- ## The One-Sentence Pitch
- ## The Player Fantasy
- ## Reference Points
- ## Market Validation: What CK3 Players Actually Want
- ## Design Principles
- ## The Technical Bet
- ## The Central Risk
- ## What Success Looks Like
- ## Answered Questions
- ## Open Questions

**Sections:**
- # Vision — Sync: Current State
- ## Current State
- ## What's Been Established
- ## Answered Questions
- ## Clarified Success Metric
- ## Remaining Open Questions
- ## Decisions Needed
- ## Next Steps
- ## Handoff Notes

**Doc refs:**
- `docs/design/opening/CONTENT.md`

**Sections:**
- # Vision — Tests / Validation Signals
- ## CHAIN
- ## Experience Metrics
- ## Build Verification

**Sections:**
- # Vision — Validation: How We Know It's Working
- ## The Core Question
- ## Validation by Layer
- ## Proof of Concept Milestones
- ## Red Flags to Watch
- ## The Ultimate Test

**Code refs:**
- `engine/moment_graph/traversal.py`

**Sections:**
- # Moment Graph Engine — Algorithm: Click, Wait, Surfacing
- ## CHAIN
- ## CLICK TRAVERSAL
- ## WAIT TRIGGER TRAVERSAL
- ## SURFACING AND DECAY
- ## SCENE CHANGE
- ## TENSION BOOST

**Code refs:**
- `engine/moment_graph/__init__.py`

**Sections:**
- # Moment Graph Engine — Behaviors: Traversal And Surfacing
- ## CHAIN
- ## OBSERVABLE BEHAVIORS
- ## INPUTS AND OUTPUTS
- ## SIDE EFFECTS

**Code refs:**
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_queries.py`

**Sections:**
- # Moment Graph Engine — Implementation: Runtime Layout
- ## CHAIN
- ## FILES AND ROLES
- ## DATA FLOW
- ## DEPENDENCIES

**Code refs:**
- `engine/moment_graph/__init__.py`

**Sections:**
- # Moment Graph Engine — Patterns: Instant Traversal Hot Path
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/moment_graph/__init__.py`

**Sections:**
- # Moment Graph Engine — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Code refs:**
- `engine/moment_graph/traversal.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_moment_graph.py`

**Sections:**
- # Moment Graph Engine — Tests: Runtime Coverage
- ## CHAIN
- ## EXISTING TESTS
- ## HOW TO RUN
- # Requires FalkorDB running on localhost:6379
- ## GAPS

**Code refs:**
- `engine/moment_graph/traversal.py`

**Sections:**
- # Moment Graph Engine — Validation: Traversal Invariants
- ## CHAIN
- ## INVARIANTS
- ## PERFORMANCE EXPECTATIONS
- ## FAILURE MODES TO WATCH

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Algorithm: Graph Operations
- ## CHAIN
- ## OVERVIEW
- ## TARGET FLOW
- ## DATA SOURCES

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Behaviors: Moment Lifecycle
- ## CHAIN
- ## BEHAVIOR SUMMARY
- ## EXPECTED BEHAVIORS
- ## NOTES

**Code refs:**
- `engine/moments/__init__.py`

**Sections:**
- # Moment Graph — Implementation: Stub Layout
- ## CHAIN
- ## FILES
- ## CURRENT IMPLEMENTATION NOTES

**Code refs:**
- `engine/moments/__init__.py`

**Sections:**
- # Moment Graph — Patterns
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/engine/moments/SYNC_Moments.md`
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Code refs:**
- `engine/moments/__init__.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`

**Sections:**
- # Moment Graph — Test Coverage
- ## CHAIN
- ## CURRENT COVERAGE
- ## GAPS
- ## HOW TO RUN

**Code refs:**
- `engine/moments/__init__.py`

**Doc refs:**
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Moment Graph — Validation: Invariants
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION NOTES

**Code refs:**
- `engine/tests/__init__.py`

**Sections:**
- # Engine Test Suite — Algorithm: Test Run Flow
- ## CHAIN
- ## RUN FLOW
- ## COMMON RUN MODES
- # Full suite (unit + integration; integration may skip)
- # Unit/spec only (exclude integration)
- # Integration only

**Code refs:**
- `engine/tests/__init__.py`

**Sections:**
- # Engine Test Suite — Behaviors: Coverage Layers
- ## CHAIN
- ## OBSERVABLE BEHAVIOR
- ## INPUTS AND OUTPUTS

**Code refs:**
- `engine/tests/__init__.py`
- `test_behaviors.py`
- `test_implementation.py`
- `test_integration_scenarios.py`
- `test_spec_consistency.py`

**Sections:**
- # Engine Test Suite — Implementation: File Layout
- ## CHAIN
- ## DIRECTORY STRUCTURE
- ## ENTRY POINTS

**Code refs:**
- `engine/tests/__init__.py`

**Sections:**
- # Engine Test Suite — Patterns: Spec-Linked Layered Tests
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/tests/__init__.py`
- `test_implementation.py`

**Doc refs:**
- `docs/engine/SCHEMA.md`
- `docs/engine/tests/ALGORITHM_Test_Run_Flow.md`
- `docs/engine/tests/BEHAVIORS_Test_Coverage_Layers.md`
- `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md`
- `docs/engine/tests/PATTERNS_Spec_Linked_Test_Suite.md`
- `docs/engine/tests/SYNC_Engine_Test_Suite.md`
- `docs/engine/tests/TEST_Test_Suite_Coverage.md`
- `docs/engine/tests/VALIDATION_Test_Suite_Invariants.md`
- `docs/schema/SCHEMA.md`

**Sections:**
- # Engine Test Suite — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `engine/tests/__init__.py`
- `test_behaviors.py`
- `test_history.py`
- `test_implementation.py`
- `test_narrator_integration.py`
- `test_spec_consistency.py`

**Sections:**
- # Engine Test Suite — Test Coverage
- ## CHAIN
- ## COVERAGE SUMMARY
- ## HOW TO RUN
- # Full suite (integration tests may skip)
- # Unit/spec only
- # Integration only (requires FalkorDB)

**Code refs:**
- `engine/tests/__init__.py`

**Sections:**
- # Engine Test Suite — Validation: Test Invariants
- ## CHAIN
- ## INVARIANTS
- ## VALIDATION STEPS
- # Ensure unit/spec tests pass without DB
- # Verify integration tests fail fast or skip when DB is missing

**Code refs:**
- `frontend/components/map/MapClient.ts`

**Sections:**
- # Map View — Patterns: Interactive Travel Map
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/components/map/MapClient.ts`

**Sections:**
- # Map View — Patterns: Parchment Map With Fog Of War
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/map/page.tsx`
- `frontend/components/map/MapClient.ts`
- `frontend/components/map/MapClient.tsx`
- `frontend/lib/map/index.ts`
- `frontend/lib/map/projection.ts`
- `frontend/lib/map/random.ts`

**Doc refs:**
- `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`
- `docs/frontend/map/SYNC_Map_View.md`

**Sections:**
- # Map View — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Code refs:**
- `frontend/components/minimap/Minimap.ts`

**Sections:**
- # Minimap — Patterns: Discovered Location Snapshot
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/components/minimap/Minimap.ts`
- `frontend/components/minimap/Minimap.tsx`

**Doc refs:**
- `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`
- `docs/frontend/minimap/SYNC_Minimap.md`

**Sections:**
- # Minimap — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Code refs:**
- `frontend/components/panel/ChronicleTab.tsx`
- `frontend/components/panel/ConversationsTab.tsx`
- `frontend/components/panel/LedgerTab.tsx`
- `frontend/components/panel/RightPanel.ts`

**Sections:**
- # Right Panel — Patterns: Tabbed Sidebar For Chronicle And Ledger
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/components/panel/RightPanel.ts`
- `frontend/components/panel/RightPanel.tsx`

**Sections:**
- # Right Panel — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Code refs:**
- `frontend/app/scenarios/page.ts`

**Sections:**
- # Scenario Selection - Patterns: Curated Starting Point Picker
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/scenarios/page.ts`
- `frontend/app/scenarios/page.tsx`

**Doc refs:**
- `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`
- `docs/frontend/scenarios/SYNC_Scenario_Selection.md`

**Sections:**
- # Scenario Selection - Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Sections:**
- # Scene View — Algorithm
- ## CHAIN

**Sections:**
- # Scene View — Behaviors
- ## CHAIN

**Doc refs:**
- `data/init/BLOOD_LEDGER_DESIGN_DOCUMENT.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Vision.md`

**Sections:**
- # Scene View — Patterns: Design Philosophy
- ## Purpose
- ## The Core Question
- ## Design Principles for Scene
- ## What We Don't Know Yet
- ## What We're Testing
- ## Reference: Scene Structure (from Design Doc)
- ## My Current Thinking
- ## Links

**Code refs:**
- `Atmosphere.tsx`
- `CenterStage.tsx`
- `CharacterRow.tsx`
- `Hotspot.tsx`
- `HotspotRow.tsx`
- `ObjectRow.tsx`
- `SceneActions.tsx`
- `SceneBanner.tsx`
- `SceneHeader.tsx`
- `SceneImage.tsx`
- `SceneView.tsx`
- `SettingStrip.tsx`
- `frontend/components/moment/index.ts`
- `frontend/components/scene/SceneView.tsx`
- `frontend/hooks/useMoments.ts`
- `frontend/types/game.ts`

**Doc refs:**
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/scene/PATTERNS_Scene.md`
- `docs/physics/API_Physics.md`

**Sections:**
- # Scene View — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## DESIGN QUESTIONS (from PATTERNS)
- ## INTEGRATION
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## RECENT CHANGES
- ## POINTERS

**Sections:**
- # Scene View — Tests
- ## CHAIN
- ## Planned Suites
- ## Coverage Gaps

**Sections:**
- # Scene View — Validation
- ## CHAIN
- ## Invariants
- ## Checks

**Code refs:**
- `engine/infrastructure/api/moments.py`
- `frontend/components/scene/CenterStage.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/lib/api.ts`

**Doc refs:**
- `docs/frontend/BEHAVIORS_Frontend_State_And_Interaction.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- `docs/frontend/PATTERNS_Frontend.md`
- `docs/frontend/SYNC_Frontend.md`

**Sections:**
- # Frontend Data Flow — Algorithm
- ## Overview
- ## Two Paths
- ## Moment Updates: Current vs Desired
- ## SSE Event Types
- ## Implementation Checklist
- ## Migration Path
- ## Files
- ## Chain

**Code refs:**
- `frontend/app/page.ts`

**Sections:**
- # Frontend — Behaviors: State Management and User Interaction
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/components/moment/ClickableText.tsx`
- `frontend/components/moment/MomentDebugPanel.tsx`
- `frontend/components/moment/MomentDisplay.tsx`
- `frontend/components/moment/MomentStream.tsx`
- `frontend/components/scene/Atmosphere.tsx`
- `frontend/components/scene/CenterStage.tsx`
- `frontend/components/scene/CharacterRow.tsx`
- `frontend/components/scene/Hotspot.tsx`
- `frontend/components/scene/HotspotRow.tsx`
- `frontend/components/scene/ObjectRow.tsx`
- `frontend/components/scene/SceneActions.tsx`
- `frontend/components/scene/SceneBanner.tsx`
- `frontend/components/scene/SceneHeader.tsx`
- `frontend/components/scene/SceneImage.tsx`
- `frontend/components/scene/SceneView.tsx`
- `frontend/components/scene/SettingStrip.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/hooks/useMoments.ts`
- `frontend/lib/api.ts`
- `frontend/types/game.ts`
- `frontend/types/map.ts`
- `frontend/types/moment.ts`

**Doc refs:**
- `docs/frontend/PATTERNS_Presentation_Layer.md`

**Sections:**
- # Frontend — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/api/moments.py`
- `frontend/app/page.ts`

**Sections:**
- # Frontend — Patterns: Presentation Layer for The Blood Ledger
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/layout.tsx`
- `frontend/app/map/page.tsx`
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/components/SpeedControl.tsx`
- `frontend/components/chronicle/ChroniclePanel.tsx`
- `frontend/components/ui/Toast.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/hooks/useMoments.ts`
- `frontend/hooks/useTempo.ts`
- `frontend/lib/api.ts`
- `frontend/types/game.ts`
- `frontend/types/map.ts`
- `frontend/types/moment.ts`

**Doc refs:**
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- `docs/physics/API_Physics.md`

**Sections:**
- # Frontend — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## ARCHIVE

**Code refs:**
- `frontend/components/chronicle/ChroniclePanel.tsx`
- `frontend/components/debug/DebugPanel.tsx`
- `frontend/components/scene/CenterStage.tsx`
- `frontend/components/voices/Voices.tsx`
- `frontend/hooks/useGameState.ts`

**Doc refs:**
- `docs/frontend/ALGORITHM_Frontend_Data_Flow.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`

**Sections:**
- # Archived: SYNC_Frontend.md
- ## MATURITY
- ## RECENT CHANGES

**Code refs:**
- `hooks/useGameState.ts`
- `hooks/useMoments.ts`
- `lib/api.ts`

**Sections:**
- # Frontend — Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## E2E TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Currently no test suite configured
- # Future commands:
- # Run all tests
- # Run with coverage
- # Run E2E tests
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## RECOMMENDED IMPLEMENTATION ORDER
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/hooks/useGameState.ts`

**Sections:**
- # Frontend — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # Build (type checking)
- # Lint
- # No dedicated test suite yet (see TEST doc)
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/init_db.py`
- `engine/physics/graph/graph_ops.py`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/hooks/useGameState.ts`

**Sections:**
- # API — Algorithm
- ## Graph Helpers
- ## Health Check
- ## Debug Mutation Stream
- ## Playthrough Creation
- ## CHAIN

**Sections:**
- # API — Behaviors
- ## Health Check
- ## Debug Mutation Stream
- ## CHAIN

**Sections:**
- # API — Implementation
- ## Graph Access Helpers
- ## Health Check
- ## Debug Mutation Stream
- ## Action Endpoint
- ## Playthrough Creation
- ## CHAIN

**Sections:**
- # API — Patterns
- ## App Factory First
- ## Lightweight Health Checks
- ## SSE Debug Streams
- ## CHAIN

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/playthroughs.py`

**Doc refs:**
- `docs/infrastructure/api/ALGORITHM_Api.md`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
- `docs/infrastructure/api/BEHAVIORS_Api.md`
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`

**Sections:**
- # API — Sync: Current State
- ## CURRENT STATE
- ## RECENT CHANGES
- ## AGENT OBSERVATIONS
- ## CHAIN

**Sections:**
- # API — Test
- ## Health Check
- ## Debug Mutation Stream
- ## CHAIN

**Sections:**
- # API — Validation
- ## Invariants
- ## Failure Modes
- ## CHAIN

**Code refs:**
- `engine/scripts/check_injection.py`

**Sections:**
- # Async Architecture — Algorithm
- ## CHAIN
- ## Runner Protocol
- # May need to re-spawn Runner for remaining journey
- ## Hook Injection
- # Take first injection
- # Rewrite file with remaining injections
- # Return to Claude Code
- # No injection
- # In Narrator's context
- # Insert dialogue, then continue
- # Generate stop scene at current position
- ## Graph SSE
- # Write to graph
- # Emit SSE
- # Update graph
- # Emit SSE
- ## Waypoint Creation
- # Write to graph (triggers SSE + image generation)
- ## Fog of War
- # Update position
- # Reveal place
- # SSE broadcast handled by graph
- ## Image Generation
- # Generate image (async)
- # Save to disk
- # Update graph
- # SSE broadcast happens automatically from graph
- # Broadcast place_created (no image yet)
- # Queue image generation
- ## Discussion Trees
- # Delete the explored branch
- # Save updated tree
- # Check if regeneration needed

**Sections:**
- # Travel Experience — Behaviors
- ## CHAIN
- ## Core Behavior
- ## What the Player Sees
- ## Player Input During Travel
- ## Duration
- ## Anti-Patterns
- ## Success Metrics

**Code refs:**
- `check_injection.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/injection_queue.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/scripts/check_injection.py`
- `engine/scripts/inject_to_narrator.py`
- `inject_to_narrator.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `agents/world_runner/CLAUDE.md`

**Sections:**
- # Async Architecture - Implementation: Injection Hooks and Queue Integration
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Async Architecture — Design Patterns
- ## CHAIN
- ## Core Principle
- ## The Architecture in One Sentence
- ## CHAIN
- ## Component Responsibilities
- ## Data Flow Diagram
- ## Key Design Decisions
- ## File Paths
- ## What Goes Where
- ## Clarifications
- ## Related Documents

**Code refs:**
- `check_injection.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/scripts/check_injection.py`
- `engine/scripts/inject_to_narrator.py`
- `generate_images_for_existing.py`
- `graph_ops.py`
- `graph_queries.py`
- `narrator.py`
- `physics/tick.py`
- `world_runner.py`

**Doc refs:**
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/async/SYNC_Async_Architecture.md`

**Sections:**
- # Async Architecture — State & Implementation Plan
- ## Overview
- ## CHAIN
- ## Current State vs Target State
- ## Key Decisions Made
- ## Open Questions
- ## Next Action
- ## Recent Changes
- ## CONFLICTS
- ## ARCHIVE

**Code refs:**
- `tests/async/test_hook_injection.py`
- `tests/async/test_runner_protocol.py`
- `tests/async/test_sse_queue.py`

**Sections:**
- # Async Architecture — Tests
- ## CHAIN
- ## Planned Coverage
- ## Manual Verification
- ## Gaps

**Sections:**
- # Async Architecture — Validation
- ## CHAIN
- ## Invariants
- ## Verification Steps

**Doc refs:**
- `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/canon/SYNC_Canon.md`
- `docs/infrastructure/canon/VALIDATION_Canon.md`

**Sections:**
- # Canon Holder — Algorithm
- ## Overview
- ## Constants
- ## Q1: Detect Ready Moments (possible → active)
- ## Q2: Check Presence Requirements
- ## Q3: Get Player Location
- ## Q4: Flip Moment to Active
- ## Q5: Determine Speaker
- ## Q6: Record Moment to Canon (active → spoken)
- ## Q7: Get Last Spoken Moment
- ## Q8: Flip to Dormant (player leaves)
- ## Q9: Reactivate Dormant (player returns)
- ## Q10: Decay Check
- ## Process Flow
- # Find ready moments
- # Check presence
- # Check speaker for dialogue
- # Flip to active
- # Determine speaker
- # Record to canon
- # Broadcast
- ## SSE Events
- ## Integration Points
- ## Chain

**Sections:**
- # Canon Holder — Behaviors
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## SSE EVENTS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/canon/__init__.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/canon/speaker.py`

**Doc refs:**
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`

**Sections:**
- # Canon Holder — Implementation: Code Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md`
- `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- `docs/infrastructure/canon/SYNC_Canon.md`
- `docs/infrastructure/canon/VALIDATION_Canon.md`

**Sections:**
- # Canon Holder — Patterns
- ## Overview
- ## Core Design Principle: Single Gatekeeper
- ## Why This Shape
- ## Integration Pattern: Option A (Integrated)
- # In orchestrator.py
- ## Why Speaker Resolution is Part of Recording
- ## Invariants This Design Enforces
- ## What Canon Holder Does NOT Do
- ## Chain

**Code refs:**
- `__init__.py`
- `canon_holder.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/canon/__init__.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/canon/speaker.py`
- `orchestrator.py`
- `playthroughs.py`
- `speaker.py`
- `strength.py`
- `tests/infrastructure/canon/__init__.py`
- `tests/infrastructure/canon/test_canon_holder.py`
- `time.py`

**Doc refs:**
- `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md`
- `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/canon/TEST_Canon.md`
- `docs/infrastructure/canon/VALIDATION_Canon.md`

**Sections:**
- # Canon Holder — Sync
- ## Current State
- ## Resolved Issues
- # Creates ATTACHED_TO link to location with presence_required=false
- ## Implementation Summary
- ## Remaining Work
- ## Test Results
- ## Recent Changes
- ## Chain

**Code refs:**
- `tests/infrastructure/canon/test_canon_holder.py`

**Sections:**
- # Canon Holder — Test
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## BEHAVIOR TESTS
- ## EDGE CASE TESTS
- ## INTEGRATION TESTS
- ## TEST FIXTURES
- # ... extended fixture with 5 moments, CAN_LEAD_TO links
- ## HOW TO RUN
- # Run all canon tests
- # Run specific behavior
- # Run with coverage
- # Run integration only
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Canon Holder — Validation
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `generate_image.py`
- `stream_dialogue.py`
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Sections:**
- # CLI Tools — Algorithm: Stream Events and Image Requests
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: Stream Dialogue/Narration
- ## ALGORITHM: Stream Scene/Mutation/Time
- ## ALGORITHM: Generate Image
- ## KEY DECISIONS
- ## DATA FLOW
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Sections:**
- # CLI Tools — Behaviors: Streaming Dialogue and Image Output
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `generate_image.py`
- `stream_dialogue.py`
- `tools/image_generation/generate_image.py`
- `tools/stream_clickables.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `tools/image_generation/README.md`

**Sections:**
- # CLI Tools — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/db/graph_ops.py`
- `engine/db/graph_queries.py`
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Sections:**
- # CLI Agent Utilities — Patterns: Agent-Invocable Command Line Tools
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## THE TOOLS
- # Dialogue with clickable
- # Narration with tone
- # Complete the stream
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `generate_image.py`
- `stream_dialogue.py`
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `tools/image_generation/README.md`

**Sections:**
- # CLI Tools — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## POINTERS

**Code refs:**
- `engine/tests/test_narrator_integration.py`

**Sections:**
- # CLI Tools — Tests: Coverage and Gaps
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS

**Code refs:**
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Sections:**
- # CLI Tools — Validation: Streaming and Image Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Algorithm: Indexing and Search Procedures
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- # Source reference
- # For links: what nodes it connects
- # For conversations (not in graph)
- # Link-specific
- # Conversation-specific
- ## ALGORITHM: index_node()
- # Prefer detail, fallback to name
- # Update in graph:
- # MATCH (n {id: $id}) SET n.embedding = $vector
- ## ALGORITHM: index_link()
- # Update in graph:
- # MATCH ()-[r {id: $id}]->() SET r.embedding = $vector
- ## ALGORITHM: search()
- # Search all embeddings (FalkorDB vector index)
- # Keep best match per source
- ## ALGORITHM: index_world()
- # Index all nodes
- # Index all links
- ## ALGORITHM: on_scene_end()
- # Index new/updated nodes
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## VECTOR STORAGE IN FALKORDB
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Behaviors: Observable Indexing and Search Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- # For links
- # For conversations
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## QUERY EXAMPLES
- # Expected matches:
- # - character/char_aldric: "Watched his brother die at Stamford..."
- # - link/BELIEVES: "Aldric told me by the fire, voice breaking..."
- # - conversation: "I was fifty yards away. Couldn't reach him."
- # Expected matches:
- # - link/CARRIES: "Pulled from father's hand as he died..."
- # - narrative/narr_father_death: "Father died in the burning..."
- # Expected matches:
- # - place/place_moors: "Wind howls. Men disappear here..."
- # - place/place_humber: "Norman patrols check travelers..."
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`
- `service.py`

**Sections:**
- # Embeddings - Implementation: Embedding Service Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Embeddings — Patterns: Per-Field String Embedding
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## SCALE ESTIMATES
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/__init__.py`
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Sync: Current State
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## ARCHIVE

**Sections:**
- # Archived: SYNC_Embeddings.md
- ## MATURITY
- ## RECENT CHANGES
- ## IMPLEMENTATION PLAN

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST FIXTURES
- # Deterministic fake embedding based on text hash
- # detail > 20: uses detail for embedding
- # Expected: embedding from detail
- # detail < 20, name > 20: falls back to name
- # Expected: embedding from name
- # Both < 20: no embedding
- # Expected: None
- # detail > 20: uses detail
- # Expected: embedding from detail
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all embedding tests
- # Run with real model (slow)
- # Run only unit tests (fast, mocked)
- # Run with coverage
- # Run specific test
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## PERFORMANCE TESTS
- # ... index some content first ...
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # Run embedding tests
- # Run with coverage
- # Check index integrity
- ## INTEGRATION TESTS
- ## PERFORMANCE BENCHMARKS
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # History — Algorithm: Retrieval and Recording Procedures
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- # Conversations with {Character}
- ## Day 4, Night — The Camp
- ## Day 7, Morning — The Road
- ## ALGORITHM: query_history()
- ## ALGORITHM: record_player_history()
- ## ALGORITHM: record_world_history()
- # Characters at origin place learn immediately
- # Characters in connected places learn over time
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## COMMON QUERIES
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # History — Behaviors: Observable Memory Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `conversations.py`
- `engine/infrastructure/history/__init__.py`
- `engine/infrastructure/history/conversations.py`
- `engine/infrastructure/history/queries.py`
- `engine/infrastructure/history/recording.py`
- `engine/infrastructure/history/service.py`
- `service.py`

**Doc refs:**
- `engine/infrastructure/history/README.md`

**Sections:**
- # History — Implementation: Service and Conversation Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # History — Patterns: Distributed Memory Through Narratives
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/history/conversations.py`
- `engine/infrastructure/history/service.py`

**Doc refs:**
- `docs/infrastructure/history/SYNC_History.md`
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # History — Sync: Current State
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## CONFLICTS
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## CHAIN
- ## Agent Observations
- ## ARCHIVE
- ## ARCHIVE
- ## ARCHIVE

**Code refs:**
- `engine/infrastructure/history/conversations.py`

**Doc refs:**
- `docs/infrastructure/history/SYNC_History.md`

**Sections:**
- # Archived: SYNC_History.md
- ## MATURITY
- ## RECENT CHANGES
- # Archived: SYNC_History.md
- ## MATURITY
- ## RECENT CHANGES
- # Archived: SYNC_History.md
- ## RECENT CHANGES

**Sections:**
- # History — Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST FIXTURES
- # Player, Edmund, Aldric, Mildred
- # The Betrayal vs The Salvation narratives
- # Conflicting beliefs
- ## Day 4, Night — The Camp
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all history tests
- # Run specific test category
- # Run with coverage
- # Run integration tests only
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## EXPERIENCE TESTS (MANUAL)
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # History — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # Run history module tests
- # Run with coverage
- # Run invariant checks
- ## INTEGRATION TESTS
- ## SYNC STATUS
- ## EXPERIENCE VALIDATION
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `tools/image_generation/generate_image.py`

**Sections:**
- # Image Generation — Algorithm
- ## CHAIN

**Sections:**
- # Image Generation — Behaviors
- ## CHAIN

**Code refs:**
- `tools/image_generation/generate_image.py`

**Doc refs:**
- `tools/image_generation/README.md`

**Sections:**
- # Image Generation — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `tools/image_generation/generate_image.py`

**Sections:**
- # Blood Ledger Image Prompting Guide
- ## CHAIN
- ## Core Principles
- ## Scene Banner Philosophy
- ## The 8-Part Prompt Structure
- ## Assembling the Parts
- ## Lighting & Atmosphere Options
- ## Technical Enhancers Options
- ## Blood Ledger Specific Rules
- ## Checklist Before Generating
- ## API Configuration
- ## References

**Code refs:**
- `tools/image_generation/generate_image.py`

**Doc refs:**
- `tools/image_generation/README.md`

**Sections:**
- # SYNC: Image Generation
- ## Status
- ## CHAIN
- ## What's Canonical (v2)
- ## What's Working
- ## Approach
- ## Prompt Specifics
- ## Files
- ## Open Questions
- ## Next Steps
- ## Recent Changes
- ## Last Updated

**Code refs:**
- `tests/tools/test_generate_image.py`
- `tests/tools/test_graphops_images.py`
- `tests/tools/test_retry_policy.py`

**Sections:**
- # Image Generation — Tests
- ## CHAIN
- ## Planned Suites

**Sections:**
- # Image Generation — Validation
- ## CHAIN
- ## Invariants

**Sections:**
- # Ops Scripts — Algorithm: Seeding And Backfill Flows
- ## CHAIN
- ## SEED MOMENT SAMPLE
- ## GENERATE IMAGES FOR EXISTING

**Code refs:**
- `generate_images_for_existing.py`
- `seed_moment_sample.py`

**Sections:**
- # Ops Scripts — Behaviors: Operational Script Runbooks
- ## CHAIN
- ## EXPECTED BEHAVIOR
- ## INPUTS
- ## OUTPUTS

**Code refs:**
- `engine/physics/graph/graph_ops.py`
- `engine/scripts/check_injection.py`
- `engine/scripts/generate_images_for_existing.py`
- `engine/scripts/inject_to_narrator.py`
- `engine/scripts/seed_moment_sample.py`

**Sections:**
- # Ops Scripts — Implementation: Engine Scripts Layout
- ## CHAIN
- ## FILES
- ## ENTRY POINTS
- ## DEPENDENCIES

**Code refs:**
- `engine/physics/graph/graph_ops.py`
- `engine/scripts/seed_moment_sample.py`

**Sections:**
- # Ops Scripts — Patterns: Operational Seeding And Backfill Scripts
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/scripts/generate_images_for_existing.py`
- `engine/scripts/seed_moment_sample.py`

**Sections:**
- # Ops Scripts — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO

**Sections:**
- # Ops Scripts — Tests: Operational Scripts
- ## CHAIN
- ## AUTOMATED COVERAGE
- ## MANUAL CHECKS
- ## GAPS

**Sections:**
- # Ops Scripts — Validation: Operational Script Safety
- ## CHAIN
- ## INVARIANTS
- ## SAFETY CHECKS
- ## FAILURE MODES

**Sections:**
- # Scene Memory System — Algorithm
- ## CHAIN
- ## OVERVIEW
- ## NAME EXPANSION
- # Build prefix from scene context
- # Parse "Day 5, dusk" → "d5", "dusk"
- # → "crossing_d5_dusk"
- # Track used names for collision detection
- # Collision: append incrementing suffix
- # Expand narration element names
- # Expand clickable hint names
- # Expand player input names
- ## SCENE PROCESSING
- # 1. Store scene node
- # 2. Create Moment nodes for each narration element
- # Link scene to moment
- # Link moment to place
- # Link dialogue to speaker
- # Link to previous moment (sequence)
- # Create moments for clickable hints
- # 3. Process mutations - create narratives with FROM links
- # Link scene to narrative
- # Create FROM links to source moments
- # Auto-create beliefs for all present
- # → "scene_d5_dusk_crossing"
- # Link to place
- # Link to present characters
- # Embed if sufficient text
- ## PLAYER INPUT PROCESSING
- # Determine moment type from input type
- # Build moment text
- # Link to place
- # Link to player character
- ## NARRATIVE CREATION
- # Add detail and embedding if provided
- # Create ABOUT links if specified (for key things)
- # Note: FROM links to moments are created in process_narrator_output()
- ## BELIEF CREATION
- ## EMBEDDING
- ## QUERIES
- ## THE FULL CHAIN
- ## NEXT IN CHAIN

**Sections:**
- # Scene Memory System — Behavior
- ## CHAIN
- ## OVERVIEW
- ## ACTORS
- ## INPUT: NARRATOR OUTPUT
- ## INPUT: PLAYER ACTIONS
- ## OUTPUT: MOMENT NODES
- ## OUTPUT: STORED SCENE
- ## OUTPUT: STORED NARRATIVES
- ## OUTPUT: AUTOMATIC BELIEFS
- ## OUTPUT: EMBEDDINGS
- ## QUERYABLE BEHAVIORS
- ## INVARIANTS
- ## EDGE CASES
- ## NEXT IN CHAIN

**Code refs:**
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_ids.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/infrastructure/memory/transcript_store.py`
- `moment_processor.py`

**Sections:**
- # Scene Memory System — Implementation: Moment Processing Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Scene Memory System — Pattern
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## CORE PRINCIPLES
- ## WHY THIS SHAPE
- ## WHAT THIS ENABLES
- ## RELATIONSHIP TO OTHER SYSTEMS
- ## GAPS / IDEAS / QUESTIONS
- ## NEXT IN CHAIN

**Code refs:**
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_queries_moments.py`

**Sections:**
- # Scene Memory System — Sync
- ## DOCUMENT CHAIN
- ## ARCHITECTURE EVOLUTION
- ## IMPLEMENTATION STATUS
- ## LINK TYPES (IMPLEMENTED)
- ## INTEGRATION POINTS
- ## DECISIONS MADE (HISTORICAL)
- ## OPEN QUESTIONS
- ## CONFLICTS
- ## Agent Observations
- ## RECENT CHANGES
- ## ARCHIVE

**Code refs:**
- `engine/infrastructure/memory/moment_processor.py`
- `engine/models/nodes.py`
- `moment_processor.py`

**Sections:**
- # Archived: SYNC_Scene_Memory.md
- ## MOMENT NODE TYPE
- # Moment Graph fields
- # Tick tracking
- # Transcript reference
- ## MOMENT PROCESSOR API
- # Immediate moments (added to transcript)
- # Potential moments (graph only)
- # Links
- ## CHANGELOG

**Code refs:**
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_moment.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moments_api.py`

**Sections:**
- # Scene Memory System — Test: Moment Processing Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run MomentProcessor unit tests
- # Run full moment-related suite
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Scene Memory System — Validation
- ## CHAIN
- ## OVERVIEW
- ## INVARIANTS
- # Expected: crossing_d5_dusk_test, crossing_d5_dusk_test_2, crossing_d5_dusk_test_3
- # Check moments
- # Check narratives
- ## UNIT TESTS
- # Both characters should have beliefs
- # ... setup ...
- ## INTEGRATION TESTS
- # 1. Narrator outputs scene
- # 2. Verify narrative sources are expanded
- # 3. Verify beliefs created
- # 4. Verify scene stored with embedding
- # 5. Player clicks blade
- # 6. Verify traceability query works
- # Scene 1: Morning
- # Scene 2: Dusk - narrative references both scenes
- # Verify cross-scene sources
- ## QUERY TESTS
- # Setup: create narrative with known source
- # ...
- # Setup: create narrative with known sources
- # ...
- # Setup: create scene with present characters
- # ...
- # Setup: create scene about sword
- # ...
- ## PERFORMANCE TESTS
- # Assume graph has been populated
- ## MANUAL VERIFICATION
- ## RED FLAGS
- ## SYNC STATUS

**Sections:**
- # Tempo Controller — Algorithm
- ## Overview
- ## Speed Modes
- ## Pause Mode (⏸)
- ## 1x Mode (🗣️)
- ## 2x Mode (🚶)
- ## 3x Mode (⏩)
- ## Interrupt Conditions
- ## The Snap (3x → 1x)
- ## Main Loop
- # Components
- # Create player moment
- # Tick once, surface one response
- # Player input interrupts 3x
- # Run physics
- # Detect and surface ready moments
- # Process only first (highest salience)
- # SSE broadcast happens inside record_to_canon
- # Run physics
- # Detect ready moments
- # Record to canon
- # Check interrupt
- # At 2x/3x, SSE still fires but frontend filters display
- # Backpressure at 1x
- # Salience threshold check
- # Filter by presence requirements
- # Additional interrupt detection
- # (Could check for combat, arrivals, etc.)
- ## SSE Events
- ## API Endpoints
- ## Startup / Shutdown
- # On playthrough start
- # On playthrough end / disconnect
- ## Integration Points
- ## Chain
- ## Gaps / Questions
- ## Future UI: Minimap + Sun Arc

**Code refs:**
- `__init__.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `tempo_controller.py`

**Sections:**
- # Tempo Controller — Implementation: Code Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `GameClient.tsx`
- `SpeedControl.tsx`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/tempo/__init__.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `frontend/components/GameClient.tsx`
- `frontend/components/SpeedControl.tsx`
- `tempo.py`
- `tempo_controller.py`

**Doc refs:**
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/BEHAVIORS_Tempo.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/infrastructure/tempo/TEST_Tempo.md`
- `docs/infrastructure/tempo/VALIDATION_Tempo.md`

**Sections:**
- # Tempo Controller — Sync
- ## Current State
- ## Implementation Summary
- ## Architecture Clarification
- ## Remaining Work
- ## Files Changed This Session
- ## Chain
- ## Agent Observations

**Sections:**
- # World Builder — Algorithm
- ## Overview
- ## Core Insight: Attention IS Energy
- ## Core Flow
- ## Every Query Is A Moment
- # 1. Record query as moment (this IS the energy source)
- # 2. Execute query (embeddings use 'detail' or 'name' field)
- # 3. Link moment to results (weight=similarity, physics will flow energy)
- # 4. Check sparsity
- # Apply and link back to query moment
- # Re-query
- # Link new results
- ## Sparsity Detection
- # 1. Proximity - are results semantically close to query?
- # 2. Cluster size - how many results?
- # 3. Diversity - are results varied or all the same?
- # 4. Connectedness - do results link to other things?
- # Sparse if any dimension is weak
- ## World Builder Enrichment
- ## Apply Enrichment
- # Characters
- # Places
- # Things
- # Narratives
- # Links
- # Link ALL created nodes back to query moment
- # Moments - always type "thought"
- # Link to speaker
- # Link to place
- # Link enriched moment back to query moment
- ## Integration
- # Record
- # Execute
- # Link results
- # Enrich if sparse
- # Re-query
- ## Caching / Rate Limiting
- # Skip if recently enriched
- # Prevent recursion
- ## Chain
- ## Summary
- ## Gaps / Questions

**Code refs:**
- `engine/infrastructure/orchestration/agent_cli.py`
- `enrichment.py`
- `query.py`
- `query_moment.py`
- `sparsity.py`
- `world_builder.py`

**Sections:**
- # World Builder — Implementation
- ## CHAIN
- ## CORE INSIGHT
- ## CODE STRUCTURE
- ## SCHEMA
- ## KEY FUNCTIONS
- # engine/infrastructure/world_builder/query.py
- # 1. Record query as thought moment (this IS the energy source)
- # 2. Execute semantic search (embeddings use 'detail' or 'name')
- # 3. Link moment to results (weight=similarity, physics flows energy)
- # 4. Check sparsity
- # 5. Enrich
- # 6. Apply enrichment (links back to query moment)
- # 7. Re-query
- # Link new results
- # engine/infrastructure/world_builder/query_moment.py
- # Create moment node
- # Link to character (they can voice this thought)
- # Link to place
- # engine/infrastructure/world_builder/sparsity.py
- # Get query embedding
- # Get result embeddings (uses 'detail' or 'name' - already implemented)
- # Fallback: compute embeddings
- # Proximity: best match to query
- # Cluster size
- # Diversity: average pairwise distance
- # Connectedness: average outgoing links per result
- # Determine sparsity
- # engine/infrastructure/world_builder/world_builder.py
- # Skip if recently enriched
- # Prevent recursion
- # Parse YAML from response
- # engine/infrastructure/world_builder/enrichment.py
- # Characters
- # Places
- # Things
- # Narratives
- # Links (just weight, physics handles energy)
- # Link ALL created nodes back to query moment
- # Moments - always type "thought"
- # Link to speaker
- # Link to place
- # Link back to query moment
- # engine/infrastructure/world_builder/enrichment.py
- ## DATA FLOW
- ## MODULE DEPENDENCIES
- ## CONFIGURATION
- ## INTEGRATION
- # Old - bypasses recording and enrichment
- # New - recorded as thought, enriched if sparse, energy flows via physics
- ## TESTS
- # Should have created new content
- # Should include enriched nodes
- ## GAPS / TODO

**Code refs:**
- `__init__.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/world_builder/world_builder.py`
- `enrichment.py`
- `query.py`
- `query_moment.py`
- `sparsity.py`
- `tests/infrastructure/world_builder/test_world_builder.py`
- `world_builder.py`

**Sections:**
- # World Builder — SYNC
- ## Current State
- ## Recent Changes
- ## Integration Points
- ## Usage Example
- # Async with enrichment (creates content if sparse)
- # Sync without enrichment (just search + record)
- ## Configuration
- ## Next Steps
- ## Known Issues
- ## Handoff Notes
- ## Chain
- ## Agent Observations

**Code refs:**
- `enrichment.py`
- `query.py`
- `query_moment.py`
- `sparsity.py`
- `tests/infrastructure/test_world_builder.py`
- `world_builder.py`

**Sections:**
- # World Builder — Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all world builder tests
- # Run with coverage
- # Run specific test category
- # Run integration tests only (requires FalkorDB)
- ## TEST FIXTURES
- # Cleanup test data
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Builder — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # Run world builder tests
- # Run with coverage
- # Run sparsity tests only
- ## INTEGRATION TESTS
- ## PERFORMANCE BENCHMARKS
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Graph — Algorithm: Energy Flow
- ## Per-Tick Processing
- ## Step 1: Compute Character Energies
- # Relationship intensity: how much player cares
- # Geographical proximity
- ## Step 2: Flow Energy Into Narratives
- ## Step 3: Propagate Between Narratives
- # Link type factors — each type has its own propagation strength
- # Collect all transfers first (avoid order dependency)
- # Bidirectional: contradiction heats both sides
- # Reverse direction handled when processing from target
- # Bidirectional: allies rise together
- # Unidirectional: general → specific
- # Unidirectional: specific → general
- # Draining: old loses, new gains
- # Apply transfers
- # Apply drains (supersession)
- ## Step 4: Decay Energy
- # Dynamic — adjusted by criticality feedback
- # Apply decay
- # Floor at minimum
- # Skip recently active
- # Core narratives decay slower
- # Focused narratives decay slower
- # System too cold — let it heat
- # System too hot — dampen
- # Clamp to sane range
- # NEVER DYNAMICALLY ADJUST:
- # - breaking_point (changes story meaning)
- # - belief_flow_rate (changes character importance)
- # - link propagation factors (changes story structure)
- ## Step 5: Recompute Weights
- # Clamp and apply focus evolution
- # Direct: player believes it
- # Indirect: about someone player knows
- # Distant: no direct connection
- # Bonus is limited by weaker of the two
- ## Step 6: Tick Pressures
- # Check for flip
- # Tick gradual component
- # Find scheduled floor
- # Use higher of ticked or floor
- ## Step 7: Detect Flips
- ## Full Tick
- # 1. Character energies (relationship × proximity)
- # 2. Flow into narratives (characters pump)
- # 3. Propagate between narratives (link-type dependent)
- # 4. Decay
- # 5. Check conservation (soft global constraint)
- # 6. Adjust criticality (dynamic decay_rate)
- # 7. Weight recomputation
- # 8. Pressure ticks
- # 9. Detect flips
- ## Automatic Tension from Approach
- # Edmund's energy as player approaches York
- # Day 1 (one day travel):
- # Edmund: intensity=4.0, proximity=0.2 → energy=0.8
- # Day 2 (same region):
- # Edmund: intensity=4.0, proximity=0.7 → energy=2.8
- # No one decided this. Physics decided this.
- # Confrontation tension rises because Edmund's narratives heat up.
- ## Parameters Summary
- ## Link Type Factors
- ## Conservation Parameters
- ## Never Adjust Dynamically
- ## CHAIN

**Sections:**
- # Graph — Behaviors: What Should Happen
- ## Overview
- ## Behavior: Companions Matter More
- ## Behavior: Contradictions Intensify Together
- ## Behavior: Support Clusters Rise and Fall Together
- ## Behavior: Old Truths Fade When Replaced
- ## Behavior: Core Oaths Persist
- ## Behavior: Tensions Build Toward Breaking
- ## Behavior: Cascades Ripple Through
- ## Behavior: System Stays Near Criticality
- ## Behavior: Agents Update Links, Not Energy
- ## Summary: What To Expect

**Sections:**
- # Graph — Patterns: Why This Shape
- ## The Core Insight
- ## Energy As Attention
- ## Computed, Not Declared
- ## Pressure Requires Release
- ## The Graph Breathes
- ## Criticality
- ## What Agents Never Do

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/tick.py`
- `graph_ops.py`
- `graph_ops_events.py`
- `orchestrator.py`
- `tick.py`

**Doc refs:**
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`

**Sections:**
- # Graph — Current State
- ## What Exists ✓
- ## What's Missing: ONE ENDPOINT
- # TODO: SSE streaming version
- ## Two Paths (Both Valid)
- ## Known False Positives
- ## Recent Changes

**Code refs:**
- `engine/graph/health/check_health.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`

**Doc refs:**
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`
- `docs/physics/graph/SYNC_Graph.md`

**Sections:**
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- ## Agent Observations
- # Archived: SYNC_Graph.md
- ## Key Design Decisions
- ## The Full Energy Cycle
- ## Next Steps
- ## CONFLICTS
- ## Agent Observations

**Sections:**
- # THE BLOOD LEDGER — Validation Specification
- # Version: 1.0
- # =============================================================================
- # PURPOSE
- # =============================================================================
- # =============================================================================
- # GRAPH INTEGRITY RULES
- # =============================================================================
- # No links — char_wulfric would be orphaned
- # result.persisted = ["char_aldric", "narr_oath", "link_belief_1"]
- # result.rejected = [
- # {"item": "char_wulfric", "error": "orphaned_node", "fix": "Add link..."}
- # ]
- # =============================================================================
- # VISION MAPPING
- # =============================================================================
- # --- COVERED BY ENERGY SYSTEM ---
- # --- REQUIRES NARRATOR/CONTENT ---
- # =============================================================================
- # EXPECTED BEHAVIORS
- # =============================================================================
- # ---------------------------------------------------------------------------
- # PRESENCE & PROXIMITY
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # LIVING WORLD
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # NARRATIVE TENSION
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # COMPANION DEPTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # SYSTEM HEALTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # TIME & PRESSURE
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # ENGAGEMENT
- # ---------------------------------------------------------------------------
- # =============================================================================
- # ANTI-PATTERNS
- # =============================================================================
- # =============================================================================
- # TEST SUITE
- # =============================================================================
- # ---------------------------------------------------------------------------
- # PRESENCE & PROXIMITY
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # LIVING WORLD
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # NARRATIVE TENSION
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # COMPANION DEPTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # SYSTEM HEALTH
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # TIME & PRESSURE
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # ENGAGEMENT
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # CRITICALITY
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # CASCADE
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # ANTI-PATTERNS
- # ---------------------------------------------------------------------------
- # =============================================================================
- # SUMMARY
- # =============================================================================

**Code refs:**
- `engine/physics/energy.py`

**Sections:**
- # Physics — Algorithm: System Overview
- ## CHAIN
- ## Consolidation Note
- ## Energy Mechanics
- ## NODE TYPES
- ## LINK TYPES
- ## NARRATIVE TYPES
- ## LINK STRENGTH
- ## STRENGTH MECHANICS (Six Categories)
- # Speaking is stronger than thinking
- # Direct address is strongest
- # Speaker's belief activated
- # ABOUT links activated
- # Check what this evidence supports
- # Check what this evidence contradicts
- # Create new association if co-occurrence is strong enough
- # Recent narratives in same conversation
- # Co-occurring narratives associate
- # How much does receiver trust source?
- # Average trust from relationship narratives
- # Direct witness vs secondhand
- # Higher cost = stronger commitment
- # What beliefs motivated this action?
- # Tension pressure
- # Danger
- # Emotional weight of moment
- # All strength changes multiplied by intensity
- ## ENERGY SOURCES
- # Baseline regeneration
- # State modifier
- # Pump budget
- # Distribute by belief strength only
- # Things don't hold energy — redirect to related narratives
- # Character arrives — they bring their energy with them
- # News creates/energizes a narrative
- # Discovery energizes existing narrative
- # Draw energy from involved characters
- # Inject into related narratives
- ## ENERGY SINKS
- # Core types resist decay
- # Draw from speakers
- # Draw from attached narratives
- ## ENERGY TRANSFER (Links)
- # A pulls from B
- # B pulls from A
- # Energy flows toward equilibrium
- # Additional drain: old loses extra (world moved on)
- # Things don't hold energy — skip
- # Forward flow
- # Reverse flow only if bidirectional
- # Only if character is awake and present
- # Only nodes with energy
- # Reverse flow: target → moment
- # Partial drain — recent speech still has presence
- # Status change
- # Remaining energy decays normally from here
- ## MOMENT ENERGY & WEIGHT
- ## FULL TICK CYCLE
- # 1. Characters pump into narratives
- # 2. Narrative-to-narrative transfer
- # 3. ABOUT links (focal point pulls)
- # 4. Moment energy flow
- # 5. Tension injection (structural pressure)
- # 6. Decay (energy leaves system)
- # 7. Detect breaks
- # Energy decay (fast)
- # Check for status transition
- # Weight decay (slow, only without reinforcement)
- ## PHYSICAL GATING
- ## PARAMETERS
- ## EMERGENT BEHAVIORS
- ## M11: FLIP DETECTION
- # Check still valid (state may have changed)
- # Flip to active
- # Handler needed?
- # Async - handler will call record_to_canon when done
- # Direct record
- # ... process ...
- ## M12: CANON HOLDER
- # 1. Status change
- # 2. Energy cost (actualization)
- # 3. THEN link (history chain)
- # 4. Time passage
- # 5. Strength mechanics
- # 6. Actions
- # 7. Notify frontend
- # ABOUT links activated
- # Confirming evidence
- # Contradicting evidence
- # Recent narratives in same conversation
- # Adjust by text length
- # Check for time-based events
- # Decay check (large time jumps)
- # Apply Commitment mechanic (M5)
- # Winner proceeds to canon
- # Loser returns to possible, decayed
- ## M13: AGENT DISPATCH
- # Detect and process breaks
- # Scheduled events
- ## WHAT WE DON'T DO
- ## Physics Tick
- # 1. PUMP — Characters inject energy into narratives
- # 2. TRANSFER — Energy flows through narrative links
- # 3. TENSION — Structural tensions concentrate energy
- # 4. DECAY — Energy leaves the system
- # 5. WEIGHT — Recompute moment weights from sources
- # 6. DETECT — Find moments that crossed threshold
- # 7. EMIT — Send flipped moments to Canon Holder
- # 8. BREAKS — Return any structural breaks for handling
- # Baseline regeneration
- # State modifier (dead/unconscious = 0, sleeping = 0.2, awake = 1.0)
- # Distribute by belief strength only - no proximity filter
- # Narrative links
- # ABOUT links (focal point pulls)
- # Draw from participants
- # Inject into related narratives
- # Narrative decay
- # Character decay
- # From characters who can speak it
- # From attached narratives
- # From attached present characters
- # Actualization cost
- # Record to canon
- # Trigger handlers for attached characters
- ## Canon Holder
- # 1. Status change
- # 2. Energy cost (actualization)
- # 3. THEN link (history chain)
- # 4. Time passage
- # 5. Strength mechanics
- # 6. Actions
- # 7. Notify frontend
- # Check still valid (state may have changed)
- # Flip to active
- # Handler needed?
- # Async - handler will call record_to_canon when done
- # Direct record
- # ... process ...
- # ABOUT links activated
- # Confirming evidence
- # Contradicting evidence
- # Recent narratives in same conversation
- # Change AT link
- # Change CARRIES link
- # Change CARRIES link
- # Complex — may trigger combat
- # Thing-specific effects
- # Apply Commitment mechanic (M5)
- # Adjust by text length
- # Check for time-based events
- # Decay check (large time jumps)
- # Winner proceeds to canon
- # Loser returns to possible, decayed
- ## Character Handlers
- # Note: NO weight field. Physics assigns weight.
- # Build prompt based on character type and speed
- # LLM call
- # Parse structured output
- # Inject into graph (physics assigns weights)
- # Speed-aware framing
- # Calculate link strength (how much character energy flows to this moment)
- # Create moment (weight will be computed by physics tick)
- # Create CAN_SPEAK link (character energy → moment weight)
- # Create ATTACHED_TO link
- # Process additional links
- # Queue questions for async answering
- # "You there, guard on the left!"
- # individual now has own node, inherits group properties
- ## In handler output
- # Parallel execution
- # Each handler only writes its own character
- # No conflicts because of isolation
- # Create a synthetic "arrival" moment
- # Trigger handler with arrival as trigger
- # By the time player engages, potentials exist
- ## Action Processing
- # 1. VALIDATE — Is action still possible?
- # 2. EXECUTE — Modify graph state
- # 3. CONSEQUENCES — Generate consequence moments
- # 4. INJECT — Consequences enter graph with energy
- # Can actor travel to destination?
- # Is thing still present and unowned?
- # Is target still present and alive?
- # Does actor have the thing? Is recipient present?
- # Remove old AT link
- # Create new AT link
- # Handle moment dormancy (see ALGORITHM_Lifecycle.md)
- # Remove thing's AT link
- # Create CARRIES link
- # Calculate damage (simplified)
- # Update target health
- # Check for death
- # Update relationship
- # Remove actor's CARRIES link
- # Create recipient's CARRIES link
- # Departure noticed
- # Arrival noticed
- # Witness reactions will be generated by their handlers
- # Create moment with initial energy
- # Create links
- # Physics takes over — consequence may flip, trigger handlers
- # First action already processed (it's first in queue)
- # Second action validation will fail
- # Generate "blocked" consequence
- # Blocked consequence triggers actor_b's handler
- # Handler can generate reaction: frustration, new plan, etc.
- ## Player Input Processing
- # Character names
- # Also check nicknames, titles
- # Place names
- # Thing names
- # ATTACHED_TO player (they said it)
- # ATTACHED_TO current location
- # ATTACHED_TO all present characters (they heard it)
- # REFERENCES for recognized names/things (strong energy transfer)
- # CAN_SPEAK link (player spoke this)
- # Direct references get full energy
- # Boost all moments attached to this character
- # All present characters get partial energy (they heard)
- ## "Aldric, what do you think?"
- ## Aldric directly referenced → full energy boost
- ## "What does everyone think?"
- ## No direct reference → distributed partial energy
- # 1. Parse
- # 2. Create moment
- # 3. Create links
- # 4. Inject energy
- # 5. Emit player moment to display (immediate)
- # 6. Trigger physics tick (may be immediate based on settings)
- # After physics tick, check if anything flipped
- # No response from NPCs
- # Energy flows back to player character
- # Player character's handler will produce observation
- # "The silence stretches. No one meets your eye."
- # Or: pause until submit
- ## Question Answering
- ## In character handler
- # Handler needs to know about father
- # Queue question for answering
- # Handler continues with what it knows
- # Does NOT block waiting for answer
- # 1. GATHER — Get relevant existing facts
- # 2. GENERATE — Invent answer via LLM
- # 3. VALIDATE — Check consistency
- # 4. INJECT — Create nodes in graph
- # Character's existing family
- # Character's origin place
- # Character's existing beliefs/narratives
- # Historical events character witnessed
- # Check family conflicts
- # Check place conflicts
- # Check temporal conflicts
- # Create new character nodes
- # Create relationship link
- # Create new place nodes
- # Create relationship link
- # Create potential memory moments
- # Create ANSWERED_BY link for traceability
- ## After injection, physics handles integration:
- ## New father character exists
- ## Memory moments attached to asker exist
- ## These have initial weight (e.g., 0.4)
- ## Next tick:
- ## - Energy propagates through FAMILY links
- ## - Memory moments may get boosted if relevant
- ## - If weight crosses threshold, memory surfaces
- ## No special "integrate answer" logic
- ## Just physics
- ## Speed Controller
- # Player character directly addressed
- # Combat initiated
- # Major character arrival
- # Tension threshold crossed
- # Decision point (player choices available)
- # Discovery (new significant narrative)
- # Danger to player or companions
- # Phase 1: Running (player sees this already)
- # - Motion blur effect
- # - Muted colors
- # - Text small, streaming upward
- # Phase 2: The Beat (300-500ms)
- # Phase 3: Arrival
- # - Crystal clear, full color
- # - Large, centered, deliberate
- # Player can resume after input processed
- ## At 3x, low-weight moments:
- ## - Actualize in graph ✓
- ## - Create THEN links ✓
- ## - Become history ✓
- ## - Display to player ✗ (filtered)
- ## Player can review history later

**Code refs:**
- `engine/api/app.py`

**Sections:**
- # Physics — API Reference
- ## CHAIN
- ## Endpoints
- ## Removed Endpoints
- ## Frontend Types
- ## SSE Callbacks
- ## Narrator Output Format
- ## Graph Operations
- # Creation
- # Links
- # Status changes
- # Queries
- # Lifecycle

**Sections:**
- # Physics — Behaviors: What Should Happen
- ## CHAIN
- ## Overview
- ## B1: Instant Display, Eventual Depth
- ## B2: Conversations Are Multi-Participant
- ## B3: Characters Think Unprompted
- ## B4: Silence Is An Answer
- ## B5: Names Have Power
- ## B6: History Is Traversable
- ## B7: Actions Have Consequences
- ## B8: Cascades Create Drama
- ## B9: Characters Have Opinions About Each Other
- ## B10: The World Continues Elsewhere
- ## B11: The Snap
- ## B12: Journey Conversations
- ## Summary: What To Expect

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/physics/constants.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_apply.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_image.py`
- `engine/physics/graph/graph_ops_links.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`
- `engine/physics/graph/graph_query_utils.py`
- `engine/physics/tick.py`

**Sections:**
- # Physics — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## IMPLEMENTATION PRIORITIES
- ## GAPS / IDEAS / QUESTIONS
- # RUNTIME PATTERNS
- ## SCENE AS QUERY
- ## TIME PASSAGE
- # Conversation takes time
- # Tick the world
- # Check for scheduled events
- # Check for time-of-day transitions
- # Update character states (tiredness, hunger if tracked)
- ## CHARACTER MOVEMENT
- # This moment IS an action
- # Update location state
- # Find arrival moments for this character
- ## CHARACTER INTRODUCTION PATTERNS
- ## QUERY MOMENTS (Backstory Generation)
- # Create the narrative
- # Create memory moments, linked to the wondering
- # What has Aldric wondered about?
- # Full trace: wondering → answer → narrative
- ## FLASHBACK PATTERN
- ## FORWARD-ONLY CITIZENS
- ## IMPLEMENTATION CHECKLIST (Runtime Patterns)

**Sections:**
- # Physics — Patterns: Why This Shape
- ## CHAIN
- ## Core Principle
- ## P1: Potential vs Actual
- ## P2: The Graph Is Alive
- ## P3: Everything Is Moments
- ## P4: Moments Are Specific, Narratives Emerge
- ## P5: Energy Must Land
- ## P6: Sequential Actions, Parallel Potentials
- ## P7: The World Moves Without You
- ## P8: Time Is Elastic
- ## P9: Physics Is The Scheduler
- ## P10: Simultaneous Actions Are Drama
- ## What This Pattern Does NOT Solve
- ## The Philosophy

**Code refs:**
- `engine/moment_graph/queries.py`
- `engine/physics/tick.py`

**Sections:**
- # Physics — Current State
- ## GAPS
- ## Recent Changes
- ## CHAIN
- ## Architecture Summary
- ## Open Questions
- ## Next Steps
- ## Handoff Notes
- ## ARCHIVE

**Code refs:**
- `engine/handlers/base.py`
- `engine/infrastructure/api/moments.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/traversal.py`
- `engine/physics/tick.py`
- `graph_ops.py`
- `graph_ops_apply.py`
- `graph_ops_events.py`
- `graph_ops_image.py`
- `graph_ops_types.py`
- `graph_queries.py`
- `graph_queries_search.py`

**Doc refs:**
- `docs/physics/ALGORITHM_Physics.md`

**Sections:**
- # Archived: SYNC_Physics.md
- ## Recent Changes
- ## Agent Observations

**Code refs:**
- `engine/tests/test_moment_graph.py`

**Sections:**
- # Physics — Tests: Trace Scenarios
- ## CHAIN
- ## Trace Scenarios
- ## Trace 1: Simple Exchange
- ## Trace 2: Silence
- # This is about blacksmiths, not about philosophy
- # Player character always has a handler
- # Handler runs with context: "silence"
- ## Trace 3: Multi-Party
- ## Trace 4: Cascade
- # Links to confession via energy propagation
- ## Trace 5: Action Conflict
- ## Trace 6: The Snap (3x to 1x)
- # action: attack → combat initiated
- ## Trace 7: Journey Conversation (2x)
- ## Test Coverage Summary
- ## Implementation Test Files

**Code refs:**
- `engine/tests/test_moment_graph.py`

**Sections:**
- # Physics — Validation: How To Verify
- ## CHAIN
- ## Core Invariants
- # No state stored outside graph
- # (This is architectural, not queryable)
- # Verify: handlers don't cache state
- # Verify: no files store moment state
- # Verify: display queue reads from graph
- # Physics tick runs continuously
- # (Verify via tick counter)
- # THEN links only from spoken moments
- # THEN links must have tick
- # No THEN links deleted in test run
- # (Track count before/after)
- # All moments created by handler X are ATTACHED_TO character X
- # (This requires tracking handler outputs)
- # Verify in handler code:
- # - No writes to other character's moments
- # - No direct graph modifications outside ATTACHED_TO scope
- # Spoken moments cannot revert to possible
- # THEN links are permanent
- # (No DELETE on THEN links in codebase)
- # Run same scenario at 1x and 3x
- # Compare THEN link chains
- # Should be identical (display differs, canon same)
- # Sum of all weights before tick
- # Tick
- # Sum after = before - decay + injection
- # Handlers only triggered by flip
- # (Verify handler trigger conditions in code)
- # No cooldown logic in handler system
- # No artificial caps on handler runs per tick
- ## Graph State Invariants
- # Status must be valid enum
- # Spoken moments must have tick_spoken
- # Decayed moments must have tick_decayed
- # Weight must be 0-1
- # CAN_SPEAK weight must be 0-1
- # CAN_SPEAK must originate from Character
- # ATTACHED_TO targets must be valid types
- # THEN links connect Moments only
- ## Physics Invariants
- # At 3x speed, total decay over 10 seconds real-time
- # should equal decay at 1x over 10 seconds real-time
- # Same state → same flips
- # After player input, something responds (eventually)
- # Run physics until stable or max ticks
- # Either NPC responded or player character observed silence
- ## Handler Invariants
- # Handler must produce valid moment drafts
- # Handler does NOT set weight
- # Handler output only attaches to its character
- # When injected, should only attach to Aldric
- ## Canon Invariants
- # Two characters grabbing same item should BOTH canonize
- # Both should flip (high weight)
- # Both should be canon
- # Action processing handles the conflict, not canon holder
- # Same character, incompatible actions → mutex
- # Only one should canonize (higher weight)
- ## Speed Invariants
- # At 3x, low-weight moments still create THEN links
- # Not displayed (below threshold)
- # But is canon
- # At 3x, interrupt moments always display
- # Must display (combat is interrupt)
- # Speed should drop to 1x
- ## Action Invariants
- # Actions process one at a time
- # First succeeds
- # Second gets blocked consequence
- # Stale action fails validation
- # Sword already taken by someone else
- # Action should fail validation
- ## Question Answering Invariants
- # Handler doesn't wait for QA
- # Should complete in LLM time, not LLM time × 2 (waiting for QA)
- # QA cannot contradict existing facts
- # Aldric already has a father defined
- # QA for "who is my father" must return existing, not invent new
- # Should reference existing father, not create new one
- ## Performance Benchmarks
- # Setup: 1000 moments, 50 characters, 20 places
- # Setup: 10000 moments
- # 4 characters flip simultaneously
- # Should be ~1 LLM call time, not 4
- ## Verification Checklist

**Code refs:**
- `check_health.py`
- `engine/graph/health/check_health.py`
- `test_schema.py`

**Sections:**
- # Graph Health — Patterns: Schema-Driven Validation And Query Artifacts
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `check_health.py`
- `engine/graph/health/check_health.py`
- `engine/graph/health/lint_terminology.py`
- `engine/graph/health/test_schema.py`
- `test_schema.py`

**Sections:**
- # Graph Health — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## POINTERS
- ## Agent Observations

**Code refs:**
- `__init__.py`
- `base.py`
- `engine/models/__init__.py`
- `engine/tests/test_models.py`
- `links.py`
- `nodes.py`
- `tensions.py`

**Doc refs:**
- `docs/schema/SCHEMA.md`

**Sections:**
- # Schema Models — Patterns: Pydantic Graph Schema Models
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/tests/test_models.py`

**Doc refs:**
- `docs/schema/SCHEMA.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`

**Sections:**
- # Schema Models — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## Agent Observations

**Sections:**
- # THE BLOOD LEDGER — Complete Schema
- # Version: 5.1
- # =============================================================================
- # PHILOSOPHY
- # =============================================================================
- # The Core Insight
- # ----------------
- # The game is a web of narratives under tension, not a simulation of characters.
- # We simulate STORIES — narratives that exist, connect, contradict, and break.
- # Characters are how stories express themselves.
- # This matters because:
- # - Relationships become real: Not "trust: 0.65" but "the oath he swore,
- # the doubt seeded when he heard Edmund's version, the loyalty tested."
- # - Memory becomes structural: The graph remembers. That promise in hour one
- # is a narrative with weight — it will speak when relevant, break when pressured.
- # - Consequences become inevitable: Tension accumulates. What cannot hold, breaks.
- # =============================================================================
- # NODES (4 Types)
- # =============================================================================
- # ---------------------------------------------------------------------------
- # CHARACTER
- # ---------------------------------------------------------------------------
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # Characters are how the player experiences relationships.
- # The goal: "I know them" — the player can predict what Aldric would do.
- # Characters feel real because they ARE real — consistent beliefs, voice, history.
- # Key moments characters create:
- # - "They remembered" — character references something from sessions ago
- # - "I can rely on them" — Player sends companion on mission, confident they'll succeed
- # - "They became real" — Character reveals depth beyond their role
- # Characters are NOT stat blocks. They are people with:
- # - Beliefs (narratives they hold)
- # - Voice (how they speak)
- # - History (backstory that informs behavior)
- # - Agency (they act based on their beliefs, not player commands)
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - Characters BELIEVE narratives → beliefs drive behavior
- # - Characters SPREAD narratives → news travels through people
- # - Characters MOVE through places → proximity affects tension pressure
- # - Characters ACT when tensions break → World Runner determines what they do
- # - Companions are NEEDED → player can't do everything alone
- # ---------------------------------------------------------------------------
- # PLACE
- # ---------------------------------------------------------------------------
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # Places ground the player in the world.
- # The goal: "I know this place" — some locations become THEIRS.
- # Key moments places create:
- # - "I know this place well" — Familiarity creates ownership, home
- # - "The world moved" — Player arrives and learns events happened here without them
- # - Atmosphere shapes mood — the same place feels different at night, in rain, after battle
- # Places are NOT just containers. They have:
- # - Atmosphere (mood, weather, sensory details)
- # - Geography (connections to other places, travel time)
- # - Memory (events that happened here become narratives)
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - Places CONTAIN characters → proximity enables interaction
- # - Travel TIME matters → distance creates urgency, cost
- # - Atmosphere SHIFTS → same place, different feel
- # - Events HAPPEN at places → location becomes part of the story
- # - Geography determines what's possible → blocked paths, dangerous roads
- # ---------------------------------------------------------------------------
- # THING
- # ---------------------------------------------------------------------------
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # Things create ownership and stakes.
- # The goal: Objects become meaningful through their history and contested nature.
- # Key moments things create:
- # - "This was his" — An object carries emotional weight from its history
- # - "They want it" — Contested ownership creates tension
- # - "I gave my word" — A token represents an oath or bond
- # Things are NOT inventory items. They are:
- # - Story anchors (the sword that killed the father)
- # - Relationship tokens (the ring she gave you)
- # - Stakes (the land Edmund took)
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - Possession is GROUND TRUTH → they have it or they don't
- # - Ownership is NARRATIVE → who SHOULD have it is a story
- # - Things can be CONTESTED → creates tension
- # - Things carry SIGNIFICANCE → mundane vs legendary affects weight
- # - Transfer creates STORY → giving, stealing, finding all spawn narratives
- # ---------------------------------------------------------------------------
- # NARRATIVE
- # ---------------------------------------------------------------------------
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # NARRATIVES ARE THE GAME.
- # Everything — relationships, reputation, memory, knowledge — is narrative.
- # Key moments narratives create:
- # - "They remembered" — A narrative from sessions ago surfaces
- # - "My past speaks" — Player's oaths and debts pull in different directions
- # - "I was wrong" — Player discovers their foundational belief was mistaken
- # - "Everything led here" — Accumulated narratives converge in climactic moment
- # What narratives ARE:
- # - "Aldric is loyal" is a narrative, not a stat
- # - "Edmund betrayed me" is a narrative, not a flag
- # - "We are brothers" is a narrative, not a relationship type
- # Characters don't have relationships — they have stories they tell themselves
- # about relationships. The player's beliefs may be WRONG. Truth is director-only.
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - Narratives have WEIGHT → high-weight narratives speak louder, appear more
- # - Narratives can CONTRADICT → contradiction under pressure creates tension
- # - Narratives SPREAD → characters tell each other stories
- # - Narratives become VOICES → they speak to the player in scenes
- # - Narratives have TRUTH (director-only) → player beliefs can be mistaken
- # - Narratives CLUSTER into tensions → when tension breaks, story advances
- # - Old narratives can be SUPERSEDED → the world evolves
- # About events
- # About characters
- # About relationships
- # About things
- # About places
- # Meta
- # System fields
- # Director only
- # =============================================================================
- # DEFINITIONS
- # =============================================================================
- # character
- # place
- # thing
- # =============================================================================
- # LINKS (6 Types)
- # =============================================================================
- # ---------------------------------------------------------------------------
- # CHARACTER → NARRATIVE (Belief)
- # ---------------------------------------------------------------------------
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # Beliefs create DRAMA. Characters don't know facts — they believe stories.
- # Key moments beliefs create:
- # - "They don't know" — Character acts on incomplete information
- # - "They believe a lie" — Character's actions based on false narrative
- # - "Secrets emerge" — Hidden beliefs surface under pressure
- # - "News travels" — Belief spreads from character to character
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - heard + believes = character acts as if true
- # - heard + denies = character actively rejects (creates conflict)
- # - heard + doubts = character is uncertain (can be swayed)
- # - hides = knows but won't share (secret keeping)
- # - spreads = actively telling others (news propagation)
- # - High doubt + high belief = CONFLICTED (internal tension)
- # Belief propagation:
- # - Characters in same place can share narratives
- # - Trust affects whether beliefs are accepted
- # - Contradicting beliefs create tension
- # Knowledge (0-1) — how much do they know/believe?
- # Action (0-1) — what are they doing with this knowledge?
- # Origin
- # Metadata — how did they learn?
- # ---------------------------------------------------------------------------
- # NARRATIVE → NARRATIVE (Story Relationships)
- # ---------------------------------------------------------------------------
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # Story relationships create STRUCTURE and CONFLICT.
- # Key moments narrative relationships create:
- # - "They can't both be true" — Contradicting narratives force resolution
- # - "It all connects" — Supporting narratives create coherent worldview
- # - "Things have changed" — Superseding narrative replaces old understanding
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - CONTRADICTS → These narratives cannot both be true. Creates tension.
- # When believers of both are in proximity, pressure builds.
- # - SUPPORTS → These narratives reinforce each other. Creates clusters.
- # Believing one makes you more likely to believe the other.
- # - SUPERSEDES → New information replaces old. The world evolves.
- # "Edmund is dead" supersedes "Edmund is my enemy"
- # - ELABORATES → Adds detail without conflict.
- # - SUBSUMES → Specific case of broader pattern.
- # ---------------------------------------------------------------------------
- # CHARACTER → PLACE (Physical Presence)
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # CHARACTER → THING (Physical Possession)
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # THING → PLACE (Physical Location)
- # ---------------------------------------------------------------------------
- # ---------------------------------------------------------------------------
- # PLACE → PLACE (Geography)
- # ---------------------------------------------------------------------------
- # Two link types: CONTAINS (hierarchy) and ROUTE (travel)
- # -------------------------------------------------------------------------
- # HIERARCHY EXAMPLE
- # -------------------------------------------------------------------------
- # place_york (settlement)
- # ├── CONTAINS → place_york_market (district)
- # │                 └── CONTAINS → place_merchants_hall (building)
- # │                                    └── CONTAINS → place_back_room (room)
- # └── CONTAINS → place_york_minster (building)
- # -------------------------------------------------------------------------
- # ROUTE IS FOR INTER-SETTLEMENT TRAVEL ONLY
- # -------------------------------------------------------------------------
- # place_york ──[ROUTE]──> place_durham
- # place_york ──[ROUTE]──> place_scarborough
- # NOT for:
- # place_york_market ──[ROUTE]──> place_york_minster  # NO! Same settlement
- # Computed at link creation from waypoints + road_type
- # =============================================================================
- # TENSIONS
- # =============================================================================
- # ===========================================================================
- # ROLE IN THE EXPERIENCE
- # ===========================================================================
- # Tensions are HOW THE WORLD MOVES.
- # They create the feeling: "The world moved without me."
- # Key moments tensions create:
- # - "The world moved" — Player arrives and learns a tension broke while they were away
- # - "I could have prevented this" — If player had been faster, things would differ
- # - "Something is happening elsewhere" — Player senses tensions building beyond their view
- # - "This happened because of that" — Every break traces to accumulated pressure
- # Tensions are NOT scripted events. They are:
- # - Pressure that accumulates over TIME
- # - Contradictions that MUST eventually resolve
- # - Emergent drama, not authored triggers
- # ===========================================================================
- # DYNAMICS
- # ===========================================================================
- # THE TENSION LOOP:
- # 1. Time passes → pressure accumulates (mechanical, no LLM)
- # 2. Pressure exceeds breaking_point → FLIP detected
- # 3. World Runner called → determines WHAT specifically happened
- # 4. New narratives created → graph updated
- # 5. Cascades checked → did this destabilize other tensions?
- # PRESSURE SOURCES:
- # - Time (gradual accumulation via base_rate)
- # - Proximity (believers of contradicting narratives in same place)
- # - Events (direct pressure from player actions or other breaks)
- # - Deadlines (scheduled pressure floors)
- # WHY THIS MATTERS:
- # The player is NOT the center. While they talk to Aldric for 30 minutes,
- # Edmund gets 30 minutes closer to York. Tensions tick. The world moves.
- # For gradual
- # For scheduled/hybrid
- # =============================================================================
- # MOMENT
- # =============================================================================
- # -------------------------------------------------------------------------
- # ROLE IN THE EXPERIENCE
- # -------------------------------------------------------------------------
- # Moments enable:
- # - Semantic search across all game content ("when did Aldric mention his sister?")
- # - Temporal queries ("what happened yesterday?")
- # - Source attribution for narratives
- # - Full transcript preservation
- # -------------------------------------------------------------------------
- # DYNAMICS
- # -------------------------------------------------------------------------
- # - Every dialogue line → Moment
- # - Every narration line → Moment
- # - Every player action → Moment
- # - Every hint/voice → Moment
- # - Moments link to Place (where), Character (who said), Narrative (source for)
- # NOTE: Speaker is NOT an attribute. Use SAID link: Character -[SAID]-> Moment
- # =============================================================================
- # NARRATOR NOTES
- # =============================================================================

**Code refs:**
- `engine/db/graph_ops.py`

**Sections:**
- # Moments — Schema Reference
- ## CHAIN
- ## How This Document Works
- # NODES
- ## CHARACTER
- # For type: group
- # Identity (optional, enriches handler context)
- ## PLACE
- ## THING
- ## NARRATIVE
- # Tension detection fields (tension is computed, not stored)
- ## MOMENT
- # Target is expressed via TARGETS link
- # LINKS
- ## Character Links
- # Energy mechanics
- # Knowledge state (how much they know/believe)
- # Action state (what they do with it)
- # Provenance
- ## Place Links
- # No attributes — relationship is binary
- ## Thing Links
- ## Narrative Links
- # No attributes — just the connection
- # No attributes — traces source
- ## Moment Links
- # 0.5 = mention ("...like Aldric said")
- # No attributes — the link itself indicates target
- # No attributes
- # EXAMPLE: Creating a Scene

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Algorithm: Rendering, Places, Routes
- ## CHAIN
- ## Canvas Layers
- ## Projection
- ## Layer 0: Parchment Background
- ## Layer 1: Coastline + Water
- ## Layer 2: Routes
- ## Layer 3: Fog of War
- ## Layer 4: Place Icons + Labels
- ## Layer 5: Dynamic Markers
- ## Layer 6: UI Overlay
- ## Seeded Random
- ## Hit Detection
- ## Performance Optimization
- ## Place Schema
- ## Scale Levels
- # region can contain settlement
- # settlement can contain district
- # district can contain building
- # building can contain room
- # room contains nothing
- ## Place Types
- ## CONTAINS Link (Hierarchy)
- ## Creating Places
- # Required fields
- # ID format
- # Coordinates
- # Scale
- ## Example Places
- ## Coordinate System
- ## Scale-Based Defaults
- ## Embedding Detail
- # Get all places with embeddings
- # Compute similarities
- # Return top-k
- ## Data File
- # Regions
- # Settlements
- # Districts
- ## ROUTE Link Schema
- # Stored (traced input)
- # Computed at creation
- # Optional
- ## Route Types
- ## Distance Computation
- ## Travel Time Computation
- ## Creating Routes
- # Result:
- # {
- # "from": "place_york",
- # "to": "place_durham",
- # "waypoints": [...],
- # "road_type": "roman",
- # "distance_km": 96.5,
- # "travel_minutes": 1158,  # ~19.3 hours
- # "difficulty": "easy",
- # "detail": "The old Roman road north..."
- # }
- ## Graph Storage
- # Forward
- # Reverse (swap endpoints, reverse waypoints)
- # Downstream (fast)
- # Upstream (slower - 3 km/h instead of 8)
- ## Movement Rules
- # Same place
- # Get parents
- # Same parent → use scale-based default
- # Different parents → check for route at settlement level
- # Same settlement, different districts
- # Different settlements → need route
- # No direct route
- ## Route Queries
- ## Position Along Route
- # Interpolate within segment
- # At end
- ## Data File
- # York to Durham (Roman road)
- # York to Scarborough (track)
- # York to Whitby (path through moors)
- ## Route Tracing Tool
- ## Places
- ## Place Schema
- ## Scale Levels
- # region can contain settlement
- # settlement can contain district
- # district can contain building
- # building can contain room
- # room contains nothing
- ## Place Types
- ## CONTAINS Link (Hierarchy)
- ## Creating Places
- # Required fields
- # ID format
- # Coordinates
- # Scale
- ## Example Places
- ## Coordinate System
- ## Scale-Based Defaults
- ## Embedding Detail
- # Get all places with embeddings
- # Compute similarities
- # Return top-k
- ## Data File
- # Regions
- # Settlements
- # Districts
- ## Routes
- ## ROUTE Link Schema
- # Stored (traced input)
- # Computed at creation
- # Optional
- ## Route Types
- ## Distance Computation
- ## Travel Time Computation
- ## Creating Routes
- # Result:
- # {
- # "from": "place_york",
- # "to": "place_durham",
- # "waypoints": [...],
- # "road_type": "roman",
- # "distance_km": 96.5,
- # "travel_minutes": 1158,  # ~19.3 hours
- # "difficulty": "easy",
- # "detail": "The old Roman road north..."
- # }
- ## Graph Storage
- # Forward
- # Reverse (swap endpoints, reverse waypoints)
- # Downstream (fast)
- # Upstream (slower - 3 km/h instead of 8)
- ## Movement Rules
- # Same place
- # Get parents
- # Same parent → use scale-based default
- # Different parents → check for route at settlement level
- # Same settlement, different districts
- # Different settlements → need route
- # No direct route
- ## Route Queries
- ## Position Along Route
- # Interpolate within segment
- # At end
- ## Data File
- # York to Durham (Roman road)
- # York to Scarborough (track)
- # York to Whitby (path through moors)
- ## Route Tracing Tool

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Behaviors: Visibility & Interaction
- ## CHAIN
- ## Visibility System
- ## PlayerVisibility Schema
- # playthroughs/{id}/visibility.yaml
- ## Visibility Update Rules
- # Visiting makes it familiar
- # Passing through while traveling → at least known
- # Hearing about it → rumored if unknown
- # Seeing on a physical map → rumored
- # Detailed description from someone who's been there → known
- ## Route Visibility
- # Both ends must be known
- # Route-specific visibility
- # If route itself is known, show it
- # If both ends are at least rumored, show as rumored
- ## What Shows at Each Level
- ## Position Uncertainty
- # Add random offset (consistent per place)
- # Convert to degrees (~111 km per degree lat, ~70 km per degree lng at this latitude)
- ## Interaction Behaviors
- ## Map Component Props
- ## Visibility Changes During Play
- # "I've heard of a monastery to the north..."
- # "Whitby is two days north along the coast..."
- # Destination becomes familiar
- # Route becomes familiar
- # Places passed through become known
- ## Map Interaction Flow
- ## Discovery Moments
- ## Integration with Narrator
- # In Narrator's graph_mutations

**Code refs:**
- `engine/world/map/__init__.py`
- `engine/world/map/semantic.py`

**Doc refs:**
- `docs/world/map/PATTERNS_Map.md`

**Sections:**
- # Map System — Implementation: Semantic Search Code Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Patterns: Why This Design
- ## CHAIN
- ## The Core Insight
- ## What the Map Does
- ## Design Principles
- ## Why These Choices
- ## Connection to Other Systems
- ## What the Map Is NOT
- ## Player Experience

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Sync: Current State
- ## CHAIN
- ## Current State
- ## What's Implemented
- ## What's NOT Implemented
- ## Documentation Status
- ## Dependencies for Visual Map
- ## ARCHIVE

**Code refs:**
- `tests/world/test_map_semantic.py`

**Sections:**
- # Map System — Test: Semantic Search Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # No tests exist yet.
- # Suggested:
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Validation: Semantic Search Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # No automated tests yet for world map semantic search.
- # Suggested location: tests/world/test_map_semantic.py
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Scraping Pipeline — Algorithm
- ## CHAIN
- ## Overview
- ## Phases
- ## Phase 1: Geography
- # scripts/scrape/phase1_geography.py
- # 1. Get Domesday settlements
- # 2. Enrich with coordinates (OSM)
- # 3. Add Roman roads
- # 4. Compute travel times
- # 5. Output places.yaml + routes.yaml
- ## Phase 2: Political Structure
- # scripts/scrape/phase2_political.py
- # 1. Get Norman lords from Domesday
- # 2. Pull holdings for each lord
- # 3. Get dispossessed Saxons (1066 holders)
- # 4. Cross-reference with Chronicle for 1067 state
- # 5. Output characters.yaml + holdings.yaml
- ## Phase 3: Historical Events
- # scripts/scrape/phase3_events.py
- # Mostly manual curation from Chronicle
- # Script validates and links to places/characters
- ## Phase 4: Narratives & Beliefs
- ## Phase 5: Tensions
- ## Output Files (Summary)

**Sections:**
- # World Scraping — Behaviors
- ## CHAIN

**Code refs:**
- `data/scripts/inject_world.py`
- `data/scripts/scrape/narrative_rules.py`
- `data/scripts/scrape/osm_utils.py`
- `data/scripts/scrape/phase1_geography.py`
- `data/scripts/scrape/phase2_political.py`
- `data/scripts/scrape/phase3_events.py`
- `data/scripts/scrape/phase4_narratives.py`
- `data/scripts/scrape/phase5_tensions.py`
- `engine/db/graph_ops.py`
- `inject_world.py`

**Sections:**
- # World Scraping — Implementation (Pipeline Architecture)
- ## CHAIN
- ## CODE STRUCTURE
- ## FILE RESPONSIBILITIES
- ## ENTRY POINTS
- ## DATA FLOW
- ## DESIGN PATTERNS
- ## EXTERNAL DEPENDENCIES
- ## GAPS

**Code refs:**
- `data/scripts/scrape/phase1_geography.py`

**Sections:**
- # World Scraping — Design Patterns
- ## CHAIN
- ## Core Principle
- ## Pattern: Authentic England 1067
- ## Behaviors: What The Player Experiences
- ## Target Density
- ## Related Documents

**Doc refs:**
- `docs/world/scraping/ALGORITHM_Pipeline.md`
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`
- `docs/world/scraping/PATTERNS_World_Scraping.md`

**Sections:**
- # World Scraping — State & Progress
- ## CHAIN
- ## Phase Status
- ## Current Counts (YAML)
- ## New Content: Characters
- ## New Content: Tensions
- ## Narrative Breakdown (Updated)
- ## Data Sources
- ## Recent Changes
- ## Blockers Resolved
- ## Optional Expansion
- ## Updates
- ## ARCHIVE

**Code refs:**
- `tests/world/test_narratives.py`
- `tests/world/test_pipeline.py`
- `tests/world/test_positions.py`
- `tests/world/test_routes.py`

**Sections:**
- # World Scraping — Tests
- ## CHAIN

**Sections:**
- # World Scraping — Validation
- ## CHAIN
- ## How We Know It Works
- ## Geography Tests
- # Sample routes, compare to Google Maps walking
- ## Political Tests
- ## Narrative Tests
- ## Tension Tests
- ## Density Tests
- ## Playtest Checklist

**Code refs:**
- `Atmosphere.tsx`
- `CenterStage.tsx`
- `CharacterRow.tsx`
- `ClickableText.tsx`
- `GameClient.tsx`
- `Hotspot.tsx`
- `HotspotRow.tsx`
- `MomentDebugPanel.tsx`
- `MomentDisplay.tsx`
- `MomentStream.tsx`
- `ObjectRow.tsx`
- `SceneActions.tsx`
- `SceneBanner.tsx`
- `SceneHeader.tsx`
- `SceneImage.tsx`
- `SceneView.tsx`
- `SettingStrip.tsx`
- `SpeedControl.tsx`
- `__init__.py`
- `api/app.py`
- `api/moments.py`
- `app/page.tsx`
- `base.py`
- `canon/holder.py`
- `canon_holder.py`
- `check_health.py`
- `check_injection.py`
- `companion.py`
- `components/GameClient.tsx`
- `components/GameLayout.tsx`
- `components/moment/ClickableText.tsx`
- `components/moment/MomentDebugPanel.tsx`
- `components/moment/MomentDisplay.tsx`
- `components/moment/MomentStream.tsx`
- `components/scene/Atmosphere.tsx`
- `components/scene/CenterStage.tsx`
- `components/scene/CenterStageContent.tsx`
- `components/scene/CharacterRow.tsx`
- `components/scene/Hotspot.tsx`
- `components/scene/HotspotRow.tsx`
- `components/scene/ObjectRow.tsx`
- `components/scene/SceneActions.tsx`
- `components/scene/SceneBanner.tsx`
- `components/scene/SceneHeader.tsx`
- `components/scene/SceneImage.tsx`
- `components/scene/SceneView.tsx`
- `components/scene/SettingStrip.tsx`
- `conversations.py`
- `data/scripts/inject_world.py`
- `data/scripts/scrape/narrative_rules.py`
- `data/scripts/scrape/osm_utils.py`
- `data/scripts/scrape/phase1_geography.py`
- `data/scripts/scrape/phase2_political.py`
- `data/scripts/scrape/phase3_events.py`
- `data/scripts/scrape/phase4_narratives.py`
- `data/scripts/scrape/phase5_tensions.py`
- `engine/api/app.py`
- `engine/api/moments.py`
- `engine/canon/holder.py`
- `engine/db/__init__.py`
- `engine/db/graph_ops.py`
- `engine/db/graph_queries.py`
- `engine/embeddings/service.py`
- `engine/graph/health/check_health.py`
- `engine/graph/health/lint_terminology.py`
- `engine/graph/health/test_schema.py`
- `engine/handlers/__init__.py`
- `engine/handlers/base.py`
- `engine/history/conversations.py`
- `engine/history/service.py`
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/injection_queue.py`
- `engine/infrastructure/api/moments.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/canon/__init__.py`
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/canon/speaker.py`
- `engine/infrastructure/embeddings/__init__.py`
- `engine/infrastructure/embeddings/service.py`
- `engine/infrastructure/history/__init__.py`
- `engine/infrastructure/history/conversations.py`
- `engine/infrastructure/history/queries.py`
- `engine/infrastructure/history/recording.py`
- `engine/infrastructure/history/service.py`
- `engine/infrastructure/memory/__init__.py`
- `engine/infrastructure/memory/moment_ids.py`
- `engine/infrastructure/memory/moment_processor.py`
- `engine/infrastructure/memory/transcript_store.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/narrator_prompt.py`
- `engine/infrastructure/orchestration/opening.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/speed.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/infrastructure/tempo/__init__.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/infrastructure/world_builder/world_builder.py`
- `engine/init_db.py`
- `engine/memory/moment_processor.py`
- `engine/models/__init__.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/models/tensions.py`
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/api_models.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/moments/__init__.py`
- `engine/orchestration/narrator.py`
- `engine/orchestration/opening.py`
- `engine/orchestration/orchestrator.py`
- `engine/orchestration/speed.py`
- `engine/orchestration/world_runner.py`
- `engine/physics/constants.py`
- `engine/physics/energy.py`
- `engine/physics/graph/graph_ops.py`
- `engine/physics/graph/graph_ops_apply.py`
- `engine/physics/graph/graph_ops_events.py`
- `engine/physics/graph/graph_ops_image.py`
- `engine/physics/graph/graph_ops_links.py`
- `engine/physics/graph/graph_ops_moments.py`
- `engine/physics/graph/graph_ops_types.py`
- `engine/physics/graph/graph_queries.py`
- `engine/physics/graph/graph_queries_moments.py`
- `engine/physics/graph/graph_queries_search.py`
- `engine/physics/graph/graph_query_utils.py`
- `engine/physics/graph_tick.py`
- `engine/physics/tick.py`
- `engine/queries/semantic.py`
- `engine/run.py`
- `engine/scripts/check_injection.py`
- `engine/scripts/generate_images_for_existing.py`
- `engine/scripts/inject_to_narrator.py`
- `engine/scripts/seed_moment_sample.py`
- `engine/tests/__init__.py`
- `engine/tests/test_behaviors.py`
- `engine/tests/test_e2e_moment_graph.py`
- `engine/tests/test_history.py`
- `engine/tests/test_implementation.py`
- `engine/tests/test_integration_scenarios.py`
- `engine/tests/test_models.py`
- `engine/tests/test_moment.py`
- `engine/tests/test_moment_graph.py`
- `engine/tests/test_moment_lifecycle.py`
- `engine/tests/test_moment_standalone.py`
- `engine/tests/test_moments_api.py`
- `engine/tests/test_narrator_integration.py`
- `engine/tests/test_spec_consistency.py`
- `engine/world/map/__init__.py`
- `engine/world/map/semantic.py`
- `enrichment.py`
- `frontend/app/layout.tsx`
- `frontend/app/map/page.tsx`
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/app/scenarios/page.ts`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/components/Providers.tsx`
- `frontend/components/SpeedControl.tsx`
- `frontend/components/chronicle/ChroniclePanel.tsx`
- `frontend/components/debug/DebugPanel.tsx`
- `frontend/components/map/FogOfWar.tsx`
- `frontend/components/map/MapCanvas.tsx`
- `frontend/components/map/MapClient.ts`
- `frontend/components/map/MapClient.tsx`
- `frontend/components/map/MapView.tsx`
- `frontend/components/map/PlayerToken.tsx`
- `frontend/components/minimap/Minimap.ts`
- `frontend/components/minimap/Minimap.tsx`
- `frontend/components/moment/ClickableText.tsx`
- `frontend/components/moment/MomentDebugPanel.tsx`
- `frontend/components/moment/MomentDisplay.tsx`
- `frontend/components/moment/MomentStream.tsx`
- `frontend/components/moment/index.ts`
- `frontend/components/panel/ChronicleTab.tsx`
- `frontend/components/panel/ConversationsTab.tsx`
- `frontend/components/panel/LedgerTab.tsx`
- `frontend/components/panel/RightPanel.ts`
- `frontend/components/panel/RightPanel.tsx`
- `frontend/components/scene/Atmosphere.tsx`
- `frontend/components/scene/CenterStage.tsx`
- `frontend/components/scene/CharacterRow.tsx`
- `frontend/components/scene/Hotspot.tsx`
- `frontend/components/scene/HotspotRow.tsx`
- `frontend/components/scene/ObjectRow.tsx`
- `frontend/components/scene/SceneActions.tsx`
- `frontend/components/scene/SceneBanner.tsx`
- `frontend/components/scene/SceneHeader.tsx`
- `frontend/components/scene/SceneImage.tsx`
- `frontend/components/scene/SceneView.tsx`
- `frontend/components/scene/SettingStrip.tsx`
- `frontend/components/ui/Toast.tsx`
- `frontend/components/voices/Voices.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/hooks/useMoments.ts`
- `frontend/hooks/useTempo.ts`
- `frontend/lib/api.ts`
- `frontend/lib/map/index.ts`
- `frontend/lib/map/projection.ts`
- `frontend/lib/map/random.ts`
- `frontend/types/game.ts`
- `frontend/types/map.ts`
- `frontend/types/moment.ts`
- `generate_image.py`
- `generate_images_for_existing.py`
- `graph_ops.py`
- `graph_ops_apply.py`
- `graph_ops_events.py`
- `graph_ops_image.py`
- `graph_ops_types.py`
- `graph_queries.py`
- `graph_queries_search.py`
- `handlers/__init__.py`
- `handlers/base.py`
- `handlers/companion.py`
- `hooks/transformers.ts`
- `hooks/useGameState.ts`
- `hooks/useMoments.ts`
- `inject_to_narrator.py`
- `inject_world.py`
- `lib/api.ts`
- `lib/api/moments.ts`
- `links.py`
- `lint_terminology.py`
- `moment_graph/queries.py`
- `moment_graph/traversal.py`
- `moment_processor.py`
- `narrator.py`
- `narrator_prompt.py`
- `nodes.py`
- `orchestration/narrator.py`
- `orchestration/orchestrator.py`
- `orchestration/speed.py`
- `orchestrator.py`
- `physics/__init__.py`
- `physics/constants.py`
- `physics/graph/health/check_health.py`
- `physics/graph/health/lint_terminology.py`
- `physics/graph/health/test_schema.py`
- `physics/tick.py`
- `playthroughs.py`
- `query.py`
- `query_moment.py`
- `run.py`
- `scripts/check_chain.py`
- `seed_moment_sample.py`
- `service.py`
- `sparsity.py`
- `speaker.py`
- `stream_dialogue.py`
- `strength.py`
- `tempo.py`
- `tempo_controller.py`
- `tensions.py`
- `test_behaviors.py`
- `test_history.py`
- `test_implementation.py`
- `test_integration_scenarios.py`
- `test_models.py`
- `test_moment.py`
- `test_narrator_integration.py`
- `test_schema.py`
- `test_spec_consistency.py`
- `tests/api/test_health.py`
- `tests/async/test_hook_injection.py`
- `tests/async/test_runner_protocol.py`
- `tests/async/test_sse_queue.py`
- `tests/infrastructure/canon/__init__.py`
- `tests/infrastructure/canon/test_canon_holder.py`
- `tests/infrastructure/test_world_builder.py`
- `tests/infrastructure/world_builder/test_world_builder.py`
- `tests/tools/test_generate_image.py`
- `tests/tools/test_graphops_images.py`
- `tests/tools/test_retry_policy.py`
- `tests/world/test_map_semantic.py`
- `tests/world/test_narratives.py`
- `tests/world/test_pipeline.py`
- `tests/world/test_positions.py`
- `tests/world/test_routes.py`
- `tick.py`
- `time.py`
- `tools/image_generation/generate_image.py`
- `tools/stream_clickables.py`
- `tools/stream_dialogue.py`
- `types/game.ts`
- `types/map.ts`
- `types/moment.ts`
- `world_builder.py`
- `world_runner.py`

**Doc refs:**
- `agents/developer/CLAUDE.md`
- `agents/narrator/CLAUDE.md`
- `agents/world_runner/CLAUDE.md`
- `agents/world_runner/CLAUDE_PROMPT.md`
- `data/init/BLOOD_LEDGER_DESIGN_DOCUMENT.md`
- `docs/agents/narrator/ALGORITHM_Prompt_Structure.md`
- `docs/agents/narrator/ALGORITHM_Rolling_Window.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/ALGORITHM_Thread.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
- `docs/agents/narrator/INPUT_REFERENCE.md`
- `docs/agents/narrator/PATTERNS_Narrator.md`
- `docs/agents/narrator/PATTERNS_World_Building.md`
- `docs/agents/narrator/SYNC_Narrator.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/agents/narrator/TEMPLATE_Player_Notes.md`
- `docs/agents/narrator/TEMPLATE_Story_Notes.md`
- `docs/agents/narrator/TEST_Narrator.md`
- `docs/agents/narrator/TOOL_REFERENCE.md`
- `docs/agents/narrator/VALIDATION_Narrator.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Drives_And_Metrics.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
- `docs/design/opening/ALGORITHM_Opening.md`
- `docs/design/opening/BEHAVIORS_Opening.md`
- `docs/design/opening/CLAUDE.md`
- `docs/design/opening/CLAUDE_Core_Loop.md`
- `docs/design/opening/CLAUDE_Tool_Reference.md`
- `docs/design/opening/CONTENT.md`
- `docs/design/opening/GUIDE.md`
- `docs/design/opening/PATTERNS_Opening.md`
- `docs/design/opening/SYNC_Opening.md`
- `docs/design/opening/TEST_Opening.md`
- `docs/design/opening/VALIDATION_Opening.md`
- `docs/design/scenarios/README.md`
- `docs/documentation_system/ALGORITHM_Documentation_System.md`
- `docs/documentation_system/BEHAVIORS_Documentation_System.md`
- `docs/documentation_system/PATTERNS_Documentation_System.md`
- `docs/documentation_system/SYNC_Documentation_System.md`
- `docs/documentation_system/TEST_Documentation_System.md`
- `docs/documentation_system/VALIDATION_Documentation_System.md`
- `docs/engine/ALGORITHM_Engine.md`
- `docs/engine/ANALYSIS_Moment_Graph_Architecture.md`
- `docs/engine/ARCHITECTURE_REVIEW_Moment_Graph.md`
- `docs/engine/BEHAVIORS_Engine.md`
- `docs/engine/GRAPH_OPERATIONS_GUIDE.md`
- `docs/engine/IMPL_PHASE_1_Moment_Graph.md`
- `docs/engine/MAP_Moment_Graph.md`
- `docs/engine/PATTERNS_Engine.md`
- `docs/engine/SCHEMA.md`
- `docs/engine/SCHEMA_DELTA_Moment_Graph.md`
- `docs/engine/SYNC_Engine.md`
- `docs/engine/TEST_Complete_Spec.md`
- `docs/engine/TEST_Engine.md`
- `docs/engine/UI_API_CHANGES_Moment_Graph.md`
- `docs/engine/VALIDATION_Complete_Spec.md`
- `docs/engine/WORLD_RUNNER_INTEGRATION_Moment_Graph.md`
- `docs/engine/moments/PATTERNS_Moments.md`
- `docs/engine/moments/SCHEMA_Moments.md`
- `docs/engine/moments/SYNC_Moments.md`
- `docs/engine/scene_memory/ALGORITHM_Scene_Memory.md`
- `docs/engine/scene_memory/BEHAVIORS_Scene_Memory.md`
- `docs/engine/scene_memory/PATTERNS_Scene_Memory.md`
- `docs/engine/scene_memory/SYNC_Scene_Memory.md`
- `docs/engine/scene_memory/VALIDATION_Scene_Memory.md`
- `docs/engine/tests/ALGORITHM_Test_Run_Flow.md`
- `docs/engine/tests/BEHAVIORS_Test_Coverage_Layers.md`
- `docs/engine/tests/IMPLEMENTATION_Test_File_Layout.md`
- `docs/engine/tests/PATTERNS_Spec_Linked_Test_Suite.md`
- `docs/engine/tests/SYNC_Engine_Test_Suite.md`
- `docs/engine/tests/TEST_Test_Suite_Coverage.md`
- `docs/engine/tests/VALIDATION_Test_Suite_Invariants.md`
- `docs/frontend/ALGORITHM_Frontend_Data_Flow.md`
- `docs/frontend/BEHAVIORS_Frontend_State_And_Interaction.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- `docs/frontend/PATTERNS_Frontend.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`
- `docs/frontend/map/SYNC_Map_View.md`
- `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`
- `docs/frontend/minimap/SYNC_Minimap.md`
- `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`
- `docs/frontend/scenarios/SYNC_Scenario_Selection.md`
- `docs/frontend/scene/ALGORITHM_Scene.md`
- `docs/frontend/scene/BEHAVIORS_Scene.md`
- `docs/frontend/scene/PATTERNS_Scene.md`
- `docs/frontend/scene/SYNC_Scene.md`
- `docs/frontend/scene/TEST_Scene.md`
- `docs/frontend/scene/VALIDATION_Scene.md`
- `docs/history/PATTERNS_History.md`
- `docs/infrastructure/api/ALGORITHM_Api.md`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md`
- `docs/infrastructure/api/BEHAVIORS_Api.md`
- `docs/infrastructure/api/IMPLEMENTATION_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/async/ALGORITHM_Discussion_Trees.md`
- `docs/infrastructure/async/ALGORITHM_Fog_Of_War.md`
- `docs/infrastructure/async/ALGORITHM_Graph_SSE.md`
- `docs/infrastructure/async/ALGORITHM_Hook_Injection.md`
- `docs/infrastructure/async/ALGORITHM_Image_Generation.md`
- `docs/infrastructure/async/ALGORITHM_Runner_Protocol.md`
- `docs/infrastructure/async/ALGORITHM_Waypoint_Creation.md`
- `docs/infrastructure/async/BEHAVIORS_Travel_Experience.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/async/PATTERNS_Async_Architecture.md`
- `docs/infrastructure/async/SYNC_Async_Architecture.md`
- `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md`
- `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/canon/SYNC_Canon.md`
- `docs/infrastructure/canon/TEST_Canon.md`
- `docs/infrastructure/canon/VALIDATION_Canon.md`
- `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- `docs/infrastructure/embeddings/BEHAVIORS_Embeddings.md`
- `docs/infrastructure/embeddings/PATTERNS_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- `docs/infrastructure/embeddings/TEST_Embeddings.md`
- `docs/infrastructure/embeddings/VALIDATION_Embeddings.md`
- `docs/infrastructure/history/ALGORITHM_History.md`
- `docs/infrastructure/history/BEHAVIORS_History.md`
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`
- `docs/infrastructure/history/PATTERNS_History.md`
- `docs/infrastructure/history/SYNC_History.md`
- `docs/infrastructure/history/TEST_History.md`
- `docs/infrastructure/history/VALIDATION_History.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/BEHAVIORS_Tempo.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/infrastructure/tempo/TEST_Tempo.md`
- `docs/infrastructure/tempo/VALIDATION_Tempo.md`
- `docs/physics/ALGORITHM_Actions.md`
- `docs/physics/ALGORITHM_Canon.md`
- `docs/physics/ALGORITHM_Energy.md`
- `docs/physics/ALGORITHM_Handlers.md`
- `docs/physics/ALGORITHM_Input.md`
- `docs/physics/ALGORITHM_Physics.md`
- `docs/physics/ALGORITHM_Questions.md`
- `docs/physics/ALGORITHM_Speed.md`
- `docs/physics/API_Physics.md`
- `docs/physics/BEHAVIORS_Moments.md`
- `docs/physics/BEHAVIORS_Physics.md`
- `docs/physics/IMPLEMENTATION_Moments.md`
- `docs/physics/IMPLEMENTATION_Physics.md`
- `docs/physics/PATTERNS_Moments.md`
- `docs/physics/PATTERNS_Physics.md`
- `docs/physics/SCHEMA_Moments.md`
- `docs/physics/SYNC_Physics.md`
- `docs/physics/TEST_Moments.md`
- `docs/physics/TEST_Physics.md`
- `docs/physics/VALIDATION_Moments.md`
- `docs/physics/VALIDATION_Physics.md`
- `docs/physics/graph/ALGORITHM_Energy_Flow.md`
- `docs/physics/graph/ALGORITHM_Weight.md`
- `docs/physics/graph/ALGORITHM_Weight_Computation.md`
- `docs/physics/graph/BEHAVIORS_Graph.md`
- `docs/physics/graph/PATTERNS_Graph.md`
- `docs/physics/graph/SYNC_Graph.md`
- `docs/physics/graph/VALIDATION.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`
- `docs/scenarios/README.md`
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA_Moments.md`
- `docs/schema/VALIDATION_Graph.md`
- `docs/schema/VALIDATION_Living_Graph.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`
- `docs/world/map/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM_Rendering.md`
- `docs/world/map/ALGORITHM_Routes.md`
- `docs/world/map/BEHAVIORS_Map.md`
- `docs/world/map/PATTERNS_Map.md`
- `docs/world/map/SYNC_Map.md`
- `docs/world/map/SYNC_Map_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/map/SYNC_Map_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12_archive_2025-12.md`
- `docs/world/scraping/ALGORITHM_Events.md`
- `docs/world/scraping/ALGORITHM_Geography.md`
- `docs/world/scraping/ALGORITHM_Narratives.md`
- `docs/world/scraping/ALGORITHM_Pipeline.md`
- `docs/world/scraping/ALGORITHM_Political.md`
- `docs/world/scraping/ALGORITHM_Tensions.md`
- `docs/world/scraping/BEHAVIORS_World_Scraping.md`
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`
- `docs/world/scraping/PATTERNS_World_Scraping.md`
- `docs/world/scraping/SYNC_World_Scraping.md`
- `docs/world/scraping/VALIDATION_World_Scraping.md`
- `engine/history/README.md`
- `engine/infrastructure/history/README.md`
- `graph/VALIDATION.md`
- `physics/graph/health/README.md`
- `playthroughs/kl/PROFILE_NOTES.md`
- `tools/image_generation/README.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`
- `views/VIEW_Test_Write_Tests_And_Verify.md`

**Sections:**
- # Repository Map: the-blood-ledger

**Code refs:**
- `check_health.py`
- `lint_terminology.py`
- `test_schema.py`

**Sections:**
- # Graph Health & Queries
- ## Files
- ## Query Quality Ratings
- ## Top Queries by Category
- ## Running Health Checks
- # Basic health check
- # Full schema test suite (22 tests)
- # With pytest for CI integration
- # Terminology linter
- ## Schema Tests
- ## Using Queries
- # Run a query

**Docs:** `docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md`

**Definitions:**
- `class Issue`
- `class HealthReport`
- `def add_issue()`
- `def error_count()`
- `def warning_count()`
- `def is_healthy()`
- `def to_dict()`
- `def print_summary()`
- `def load_schema()`
- `def validate_node()`
- `def validate_link()`
- `def check_graph_health()`
- `def get_nodes_missing_field()`
- `def get_detailed_missing_report()`
- `def main()`

**Definitions:**
- `def get_player_name_from_graph()`
- `def get_player_name_from_yaml()`
- `class LintIssue`
- `class LintResult`
- `class TerminologyLinter`
- `def __init__()`
- `def should_skip()`
- `def get_files()`
- `def is_ok_context()`
- `def check_npc_usage()`
- `def check_player_as_name()`
- `def lint_file()`
- `def fix_file()`
- `def run()`
- `def report()`
- `def main()`

**Sections:**
- # Query Expected Outputs
- ## CHARACTER QUERIES
- ## KNOWLEDGE & BELIEFS
- ## PLACE & GEOGRAPHY
- ## THINGS & POSSESSIONS
- ## NARRATIVES & TENSIONS
- ## COMPLEX RELATIONSHIP QUERIES
- ## GAMEPLAY QUERIES
- ## ATMOSPHERIC QUERIES
- ## DEBUGGING & HEALTH CHECKS

**Sections:**
- # Query Results - Actual Data
- ## DATABASE STATS
- ## CHARACTER QUERIES
- ## KNOWLEDGE & BELIEFS
- ## SECRETS
- ## RUMORS
- ## OATHS & BLOOD
- ## PLACES
- ## TENSIONS
- ## COMPLEX QUERIES
- ## THINGS
- ## NARRATIVE TYPES

**Definitions:**
- `class SchemaViolation`
- `class TestResult`
- `class SchemaValidator`
- `def __init__()`
- `def _load_schema()`
- `def _query()`
- `def test_character_required_fields()`
- `def test_character_type_enum()`
- `def test_character_flaw_enum()`
- `def test_place_required_fields()`
- `def test_place_type_enum()`
- `def test_thing_required_fields()`
- `def test_thing_significance_enum()`
- `def test_narrative_required_fields()`
- `def test_narrative_type_enum()`
- `def test_tension_required_fields()`
- `def test_tension_pressure_range()`
- `def test_believes_link_structure()`
- `def test_believes_value_ranges()`
- `def test_at_link_structure()`
- `def test_carries_link_structure()`
- `def test_located_at_link_structure()`
- `def test_connects_link_structure()`
- `def test_orphan_characters()`
- `def test_characters_have_location()`
- `def test_things_have_location_or_carrier()`
- `def test_narratives_have_believers()`
- `def test_player_exists()`
- `def run_all_tests()`
- `def print_report()`
- `def validator()`
- `def test_character_required_fields()`
- `def test_character_type_enum()`
- `def test_place_required_fields()`
- `def test_place_type_enum()`
- `def test_thing_required_fields()`
- `def test_narrative_required_fields()`
- `def test_narrative_type_enum()`
- `def test_tension_pressure_range()`
- `def test_believes_link_structure()`
- `def test_at_link_structure()`
- `def test_player_exists()`
- `def main()`

**Docs:** `docs/infrastructure/api/`

**Definitions:**
- `class ActionRequest`
- `class SceneResponse`
- `class DialogueChunk`
- `class NewPlaythroughRequest`
- `class ScenarioPlaythroughRequest`
- `class QueryRequest`
- `def create_app()`
- `def _mutation_event_handler()`
- `def get_orchestrator()`
- `def get_graph_queries()`
- `def get_playthrough_queries()`
- `def get_graph_ops()`
- `async def health_check()`
- `async def create_playthrough()`
- `async def create_scenario_playthrough()`
- `async def player_action()`
- `async def get_playthrough()`
- `class MomentClickRequest`
- `class MomentClickResponse`
- `async def moment_click()`
- `async def get_moment_view()`
- `async def get_current_view()`
- `async def get_moment_view_as_scene_tree()`
- `async def update_moment_weight()`
- `async def debug_stream()`
- `async def event_generator()`
- `async def get_map()`
- `async def get_ledger()`
- `async def get_faces()`
- `async def get_chronicle()`
- `async def semantic_query_post()`
- `async def semantic_query_get()`
- `async def inject_event()`

**Definitions:**
- `def _resolve_graph_name()`
- `def _get_queries()`
- `def _get_traversal()`
- `def _get_surface()`
- `def _get_graph_queries()`
- `class MomentResponse`
- `class TransitionResponse`
- `class CurrentMomentsResponse`
- `class ClickRequest`
- `class ClickResponse`
- `class SurfaceRequest`
- `def create_moments_router()`
- `async def get_current_moments()`
- `async def click_word()`
- `async def get_moment_stats()`
- `async def get_moment()`
- `async def surface_moment()`
- `async def moment_stream()`
- `async def event_generator()`
- `def get_moments_router()`

**Definitions:**
- `class PlaythroughCreateRequest`
- `class MomentRequest`
- `def _opening_to_scene_tree()`
- `def build_beat_narration()`
- `def _count_branches()`
- `def count_clickables()`
- `def _delete_branch()`
- `def create_playthroughs_router()`
- `def _get_playthrough_queries()`
- `async def create_playthrough()`
- `async def send_moment()`
- `def dummy_embed()`
- `async def get_discussion_topics()`
- `async def get_discussion_topic()`
- `async def use_discussion_branch()`

**Definitions:**
- `def get_sse_clients()`
- `def register_sse_client()`
- `def unregister_sse_client()`
- `def broadcast_moment_event()`

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `class SetSpeedRequest`
- `class PlayerInputRequest`
- `class TempoStateResponse`
- `class QueueSizeUpdate`
- `def create_tempo_router()`
- `async def set_speed()`
- `async def get_tempo_state()`
- `async def player_input()`
- `async def update_queue_size()`
- `async def start_tempo()`
- `async def stop_tempo()`
- `def _get_or_create_controller()`
- `def get_tempo_controller()`

**Docs:** `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`

**Docs:** `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`

**Definitions:**
- `class CanonHolder`
- `def __init__()`
- `def record_to_canon()`
- `def process_ready_moments()`
- `def _get_moment()`
- `def _create_said_link()`
- `def _create_then_link()`
- `def _get_last_spoken_moment_id()`
- `def record_to_canon()`

**Docs:** `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`

**Definitions:**
- `def determine_speaker()`
- `def get_moment_type()`

**Docs:** `docs/infrastructure/embeddings/`

**Docs:** `docs/infrastructure/embeddings/`

**Definitions:**
- `class EmbeddingService`
- `def __init__()`
- `def _load_model()`
- `def embed()`
- `def embed_batch()`
- `def embed_node()`
- `def _node_to_text()`
- `def similarity()`
- `def get_embedding_service()`

**Doc refs:**
- `docs/history/PATTERNS_History.md`

**Sections:**
- # History Module
- ## Core Principle
- ## Two Sources of History
- ## Usage
- # What does the player know about Aldric?
- # What does the player know happened at York?
- # What happened between Day 5 and Day 10?
- # Search by topic
- # Who knows about the guard's death?
- # What history do player and Aldric share?
- ## Conversation Files
- # Conversations with Aldric
- ## Day 4, Night — The Camp
- ## Day 7, Morning — The Road
- # Read a specific section
- # List all sections
- # Search for sections containing a keyword
- ## Timestamps
- # Parse
- # Create
- # Compare
- # String
- ## API Reference
- ## Data Model
- # When did this happen?
- # Where did this happen? (OCCURRED_AT link to Place, not attribute)
- # (Narrative)-[:OCCURRED_AT]->(Place)
- # Content source (ONE of these)
- ## Design Rationale
- ## Testing
- # Run history tests
- # Run with coverage
- ## Files

**Definitions:**
- `class ConversationSection`
- `class ConversationThread`
- `def __init__()`
- `def _get_file_path()`
- `def _get_relative_path()`
- `def append_section()`
- `def read_section()`
- `def list_sections()`
- `def get_full_thread()`
- `def search_sections()`

**Docs:** `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`

**Definitions:**
- `class HistoryService`
- `def __init__()`
- `def query_history()`
- `def get_shared_history()`
- `def who_knows()`
- `def record_player_history()`
- `def record_world_history()`
- `def _parse_timestamp()`
- `def _timestamp_gte()`
- `def _timestamp_lte()`
- `def _create_narrative_node()`
- `def _create_belief_edge()`
- `def _propagate_beliefs()`

**Docs:** `docs/infrastructure/scene-memory/`

**Definitions:**
- `class MomentProcessor`
- `def __init__()`
- `def _load_transcript_line_count()`
- `def _write_transcript()`
- `def _append_to_transcript()`
- `def set_context()`
- `def process_dialogue()`
- `def process_narration()`
- `def process_player_action()`
- `def process_hint()`
- `def create_possible_moment()`
- `def link_moments()`
- `def link_narrative_to_moments()`
- `def _generate_id()`
- `def _tick_to_time_of_day()`
- `def last_moment_id()`
- `def transcript_line_count()`
- `def get_moment_processor()`

**Definitions:**
- `class AgentCliResult`
- `def get_agent_model()`
- `def _load_dotenv_if_needed()`
- `def build_agent_command()`
- `def run_agent()`
- `def parse_claude_json_output()`
- `def extract_claude_text()`
- `def _strip_code_fence()`
- `def parse_codex_stream_output()`

**Definitions:**
- `class NarratorService`
- `def __init__()`
- `def generate()`
- `def _build_prompt()`
- `def _call_claude()`
- `def _fallback_response()`
- `def reset_session()`

**Definitions:**
- `class Orchestrator`
- `def __init__()`
- `def process_action()`
- `def process_action_streaming()`
- `def _build_scene_context()`
- `def _get_player_location()`
- `def _get_time_of_day()`
- `def _get_game_day()`
- `def _get_player_goal()`
- `def _get_recent_action()`
- `def _apply_mutations()`
- `def _parse_time()`
- `def _process_flips()`
- `def _build_graph_context()`
- `def _get_character_location_by_id()`
- `def _apply_wr_mutations()`
- `def new_game()`
- `def _world_injection_path()`
- `def _get_world_tick()`
- `def _load_world_injection()`
- `def _save_world_injection()`
- `def _clear_world_injection()`

**Docs:** `docs/agents/world-runner/PATTERNS_World_Runner.md`

**Definitions:**
- `class WorldRunnerService`
- `def __init__()`
- `def process_flips()`
- `def _build_prompt()`
- `def _call_claude()`
- `def _fallback_response()`

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `class TempoController`
- `def __init__()`
- `async def run()`
- `def stop()`
- `def set_speed()`
- `async def on_player_input()`
- `def update_display_queue_size()`
- `async def _wait_for_input()`
- `async def _tick_once()`
- `async def _tick_continuous()`
- `def _tick_interval()`
- `def _detect_ready_moments()`
- `def _check_presence()`
- `def _get_player_location()`
- `def _check_interrupt()`
- `def _create_player_moment()`
- `def _broadcast_speed_change()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md`

**Definitions:**
- `def build_enrichment_prompt()`
- `def apply_enrichment()`
- `def _format_results()`
- `def _create_character()`
- `def _create_place()`
- `def _create_thing()`
- `def _create_narrative()`
- `def _create_link()`
- `def _create_moment()`
- `def _link_moment_to_speaker()`
- `def _link_moment_to_place()`
- `def _link_to_query_moment()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md`

**Definitions:**
- `async def query()`
- `def query_sync()`
- `def _get_default_semantic_search()`
- `def _create_count_links_fn()`
- `def count_links()`
- `def _build_enrichment_context()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md`

**Definitions:**
- `def record_query_moment()`
- `def link_results_to_moment()`
- `def _link_to_character()`
- `def _link_to_place()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md`

**Definitions:**
- `class SparsityResult`
- `def cosine_similarity()`
- `def node_to_text()`
- `def is_sparse()`
- `def _default_embed()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION_World_Builder.md`

**Definitions:**
- `class WorldBuilder`
- `def __init__()`
- `async def enrich()`
- `async def _call_llm()`
- `async def _call_agent_cli()`
- `def _parse_response()`
- `def _hash_query()`
- `def clear_cache()`
- `def get_default_world_builder()`

**Docs:** `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`

**Definitions:**
- `class CharacterType`
- `class Face`
- `class SkillLevel`
- `class VoiceTone`
- `class VoiceStyle`
- `class Approach`
- `class Value`
- `class Flaw`
- `class PlaceType`
- `class Weather`
- `class Mood`
- `class ThingType`
- `class Significance`
- `class NarrativeType`
- `class NarrativeTone`
- `class NarrativeVoiceStyle`
- `class BeliefSource`
- `class PathDifficulty`
- `class PressureType`
- `class MomentType`
- `class MomentStatus`
- `class MomentTrigger`
- `class ModifierType`
- `class ModifierSeverity`
- `class Modifier`
- `class Skills`
- `class CharacterVoice`
- `class Personality`
- `class Backstory`
- `class Atmosphere`
- `class NarrativeAbout`
- `class NarrativeVoice`
- `class TensionProgression`
- `class TimeOfDay`
- `class NarrativeSource`
- `class GameTimestamp`
- `def __str__()`
- `def parse()`
- `def __lt__()`
- `def __le__()`
- `def __gt__()`
- `def __ge__()`

**Definitions:**
- `class CharacterNarrative`
- `def belief_intensity()`
- `class NarrativeNarrative`
- `def link_type()`
- `class CharacterPlace`
- `def is_present()`
- `class CharacterThing`
- `def has_item()`
- `class ThingPlace`
- `def is_here()`
- `class PlacePlace`
- `def travel_days()`

**Docs:** `docs/schema/`

**Definitions:**
- `class Character`
- `def embeddable_text()`
- `class Place`
- `def embeddable_text()`
- `class Thing`
- `def embeddable_text()`
- `class Narrative`
- `def embeddable_text()`
- `def is_core_type()`
- `class Moment`
- `def tick()`
- `def embeddable_text()`
- `def should_embed()`
- `def is_active()`
- `def is_spoken()`
- `def can_surface()`
- `class Config`

**Definitions:**
- `class Tension`
- `def has_flipped()`
- `def tick_gradual()`
- `def tick_scheduled()`
- `def add_event_pressure()`
- `def reset()`

**Docs:** `docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md`

**Definitions:**
- `class MomentQueries`
- `def __init__()`
- `def get_current_view()`
- `def _get_transitions()`
- `def get_moment_by_id()`
- `def find_click_targets()`
- `def get_speaker_for_moment()`
- `def get_dormant_moments()`
- `def get_wait_triggers()`
- `def get_moments_attached_to_tension()`

**Definitions:**
- `class MomentSurface`
- `def __init__()`
- `def check_for_flips()`
- `def apply_decay()`
- `def tension_to_moments()`
- `def handle_scene_change()`
- `def boost_moment()`
- `def set_moment_weight()`
- `def get_surface_stats()`

**Definitions:**
- `class MomentTraversal`
- `def __init__()`
- `def handle_click()`
- `def activate_moment()`
- `def speak_moment()`
- `def make_dormant()`
- `def decay_moment()`
- `def reactivate_dormant()`
- `def process_wait_triggers()`
- `def _update_status()`
- `def _set_weight()`
- `def _boost_weight()`
- `def _create_then_link()`

**Docs:** `docs/engine/moments/PATTERNS_Moments.md`

**Definitions:**
- `class Moment`
- `def not_implemented()`

**Docs:** `docs/physics/graph/PATTERNS_Graph.md`

**Definitions:**
- `class GraphOps`
- `def __init__()`
- `def _query()`
- `def _cosine_similarity()`
- `def _find_similar_nodes()`
- `def check_duplicate()`
- `def add_character()`
- `def add_place()`
- `def add_thing()`
- `def add_narrative()`
- `def add_tension()`
- `def add_moment()`
- `def apply_mutations()`
- `def get_graph()`

**Definitions:**
- `class ApplyOperationsMixin`
- `def apply()`
- `def _get_existing_node_ids()`
- `def _node_has_links()`
- `def _validate_link_targets()`
- `def _link_id()`
- `def _extract_character_args()`
- `def _extract_place_args()`
- `def _extract_thing_args()`
- `def _extract_narrative_args()`
- `def _extract_tension_args()`
- `def _extract_moment_args()`
- `def _extract_belief_args()`
- `def _extract_presence_args()`
- `def _extract_possession_args()`
- `def _extract_geography_args()`
- `def _extract_narrative_link_args()`
- `def _extract_thing_location_args()`
- `def _apply_node_update()`
- `def _apply_tension_update()`

**Definitions:**
- `def add_mutation_listener()`
- `def remove_mutation_listener()`
- `def emit_event()`

**Definitions:**
- `def get_image_path()`
- `def _generate_node_image_async()`
- `def generate_node_image()`

**Definitions:**
- `class LinkCreationMixin`
- `def add_said()`
- `def add_moment_at()`
- `def add_moment_then()`
- `def add_narrative_from_moment()`
- `def add_can_speak()`
- `def add_attached_to()`
- `def add_can_lead_to()`
- `def add_belief()`
- `def add_presence()`
- `def move_character()`
- `def add_possession()`
- `def add_narrative_link()`
- `def add_thing_location()`
- `def add_geography()`
- `def add_contains()`
- `def add_about()`

**Definitions:**
- `class MomentOperationsMixin`
- `def handle_click()`
- `def update_moment_weight()`
- `def propagate_embedding_energy()`
- `def _get_current_tick()`
- `def decay_moments()`
- `def on_player_leaves_location()`
- `def on_player_arrives_location()`
- `def garbage_collect_moments()`
- `def boost_moment_weight()`

**Definitions:**
- `class QueryError`
- `def __init__()`
- `class GraphQueries`
- `def __init__()`
- `def _connect()`
- `def _query()`
- `def query()`
- `def _parse_node()`
- `def get_character()`
- `def get_all_characters()`
- `def get_characters_at()`
- `def get_place()`
- `def get_path_between()`
- `def get_narrative()`
- `def get_character_beliefs()`
- `def get_narrative_believers()`
- `def get_narratives_by_type()`
- `def get_narratives_about()`
- `def get_high_weight_narratives()`
- `def get_contradicting_narratives()`
- `def get_tension()`
- `def get_all_tensions()`
- `def get_flipped_tensions()`
- `def build_scene_context()`
- `def get_player_location()`
- `def get_queries()`

**Docs:** `docs/physics/IMPLEMENTATION_Physics.md`

**Definitions:**
- `class MomentQueryMixin`
- `def get_moment()`
- `def get_moments_at_place()`
- `def get_moments_by_character()`
- `def get_moments_in_tick_range()`
- `def get_moment_sequence()`
- `def get_narrative_moments()`
- `def get_narratives_from_moment()`
- `def search_moments()`
- `def _find_similar_moments_by_embedding()`
- `def get_current_view()`
- `def get_live_moments()`
- `def resolve_speaker()`
- `def get_available_transitions()`
- `def get_clickable_words()`

**Docs:** `docs/physics/IMPLEMENTATION_Physics.md`

**Definitions:**
- `class SearchQueryMixin`
- `def search()`
- `def _to_markdown()`
- `def _cosine_similarity()`
- `def _find_similar_by_embedding()`
- `def _get_connected_cluster()`

**Docs:** `None yet (extracted during monolith split)`

**Definitions:**
- `def cosine_similarity()`
- `def extract_node_props()`
- `def extract_link_props()`
- `def to_markdown()`
- `def view_to_scene_tree()`

**Definitions:**
- `def distance_to_proximity()`

**Docs:** `docs/physics/PATTERNS_Physics.md`

**Definitions:**
- `class TickResult`
- `class GraphTick`
- `def __init__()`
- `def run()`
- `def _process_moment_tick()`
- `def _compute_character_energies()`
- `def _compute_relationship_intensity()`
- `def _compute_proximity()`
- `def _get_character_location()`
- `def _parse_distance()`
- `def _flow_energy_to_narratives()`
- `def _propagate_energy()`
- `def _get_narrative_links()`
- `def _decay_energy()`
- `def _update_narrative_weights()`
- `def _adjust_criticality()`
- `def _tick_pressures()`
- `def _detect_flips()`

**Docs:** `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`

**Definitions:**
- `def main()`

**Docs:** `docs/infrastructure/ops-scripts/PATTERNS_Operational_Seeding_And_Backfill_Scripts.md`

**Definitions:**
- `def create_character_prompt()`
- `def create_place_prompt()`
- `def main()`

**Docs:** `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`

**Definitions:**
- `def is_narrator_running()`
- `def inject_via_queue()`
- `def inject_via_direct_call()`
- `def inject()`
- `def main()`

**Docs:** `docs/infrastructure/ops-scripts/PATTERNS_Operational_Seeding_And_Backfill_Scripts.md`

**Definitions:**
- `def main()`

**Definitions:**
- `class TestTimeProgression`
- `def test_tick_interval_defined()`
- `def test_min_tick_minutes_defined()`
- `def test_tick_to_day_calculation()`
- `def tick_to_day()`
- `def test_tick_to_time_of_day()`
- `def tick_to_time()`
- `class TestEnergyFlow`
- `def test_belief_flow_rate_valid()`
- `def test_max_propagation_hops_positive()`
- `def test_link_factors_all_positive()`
- `def test_link_factors_expected_types()`
- `def test_supersedes_factor_significant()`
- `def test_contradicts_high_factor()`
- `def test_energy_flow_calculation()`
- `def test_supersession_drain()`
- `class TestWeightComputation`
- `def test_weight_range()`
- `def test_min_weight_floor()`
- `def test_focus_affects_weight()`
- `def test_weight_clamp_logic()`
- `def clamp_weight()`
- `class TestDecaySystem`
- `def test_decay_rate_valid()`
- `def test_decay_rate_bounds()`
- `def test_core_types_defined()`
- `def test_core_decay_multiplier()`
- `def test_core_types_are_narrative_types()`
- `def test_decay_reduces_weight()`
- `def test_decay_respects_min_weight()`
- `def test_core_types_decay_slower()`
- `def test_focus_affects_decay()`
- `class TestTensionAndFlips`
- `def test_default_breaking_point()`
- `def test_base_pressure_rate()`
- `def test_max_cascade_depth()`
- `def test_tension_flip_detection()`
- `def test_tension_gradual_pressure()`
- `def test_tension_scheduled_ignores_gradual()`
- `def test_tension_event_pressure()`
- `def test_tension_event_pressure_capped()`
- `def test_tension_reset()`
- `def test_tension_pressure_formula()`
- `class TestCriticality`
- `def test_criticality_targets()`
- `def test_criticality_hot_threshold()`
- `def test_criticality_adjustment_logic()`
- `class TestProximity`
- `def test_same_location_proximity()`
- `def test_nearby_proximity()`
- `def test_moderate_proximity()`
- `def test_distant_proximity()`
- `def test_proximity_formula()`
- `class TestExperienceStructure`
- `def test_narrative_has_about_fields()`
- `def test_narrative_has_voice()`
- `def test_narrative_has_truth()`
- `def test_tension_has_narratives()`

**Definitions:**
- `def graph_ops()`
- `def graph_queries()`
- `def setup_location()`
- `def setup_character()`
- `class TestE2EMomentCreation`
- `def test_create_moment_basic()`
- `def test_create_moment_with_clickables()`
- `class TestE2EViewQuery`
- `def test_get_current_view()`
- `class TestE2EClickHandling`
- `def test_click_triggers_weight_transfer()`
- `def test_click_no_match()`
- `class TestE2ELifecycle`
- `def test_decay_reduces_weight()`
- `def test_decay_to_decayed_status()`
- `def test_dormancy_on_leave()`
- `def test_reactivation_on_arrive()`
- `class TestE2EFullFlow`
- `def test_complete_conversation_flow()`

**Definitions:**
- `def temp_conversations_dir()`
- `def conversation_thread()`
- `def sample_conversation_file()`
- `class TestGameTimestamp`
- `def test_parse_basic()`
- `def test_parse_different_formats()`
- `def test_parse_case_insensitive()`
- `def test_parse_invalid_raises()`
- `def test_str_format()`
- `def test_comparison_same_day()`
- `def test_comparison_different_days()`
- `def test_comparison_equal()`
- `class TestConversationThread`
- `def test_append_section_creates_file()`
- `def test_append_multiple_sections()`
- `def test_read_section()`
- `def test_read_section_not_found()`
- `def test_read_section_file_not_found()`
- `def test_list_sections()`
- `def test_list_sections_empty_file()`
- `def test_get_full_thread()`
- `def test_search_sections()`
- `def test_search_sections_multiple_matches()`
- `class TestNarrativeSource`
- `def test_create_source()`
- `def test_source_from_dict()`
- `class MockGraphQueries`
- `def __init__()`
- `def _query()`
- `class MockGraphOps`
- `def __init__()`
- `def apply()`
- `class TestHistoryServiceUnit`
- `def test_query_history_builds_correct_cypher()`
- `def test_query_history_filters_by_place()`
- `class TestHistoryServiceIntegration`
- `def live_service()`
- `def test_record_and_query_player_history()`
- `def test_record_world_history()`

**Definitions:**
- `def db_connection()`
- `def graph_ops()`
- `def graph_queries()`
- `def graph_tick()`
- `def test_world()`
- `class TestGraphOpsImplementation`
- `def test_add_character_creates_node()`
- `def test_add_narrative_creates_node()`
- `def test_add_belief_creates_link()`
- `def test_add_narrative_link_creates_relationship()`
- `class TestGraphQueriesImplementation`
- `def test_get_character_beliefs()`
- `def test_get_narratives_about_character()`
- `def test_get_characters_at_place()`
- `def test_get_path_between_places()`
- `def test_get_tension_by_id()`
- `class TestEnergyFlowImplementation`
- `def test_characters_pump_energy_to_narratives()`
- `def test_proximity_affects_energy()`
- `def test_contradicting_narratives_both_heat_up()`
- `class TestDecayImplementation`
- `def test_narratives_decay_over_time()`
- `def test_core_types_decay_slower()`
- `def test_weight_never_below_min()`
- `class TestTensionImplementation`
- `def test_tension_pressure_increases()`
- `def test_tension_flip_detected()`
- `def test_flip_returns_narrative_ids()`
- `class TestWorldRunnerImplementation`
- `def test_world_runner_creates_narratives()`
- `def test_world_runner_updates_beliefs()`
- `class TestNarratorImplementation`
- `def test_narrator_receives_high_weight_narratives()`
- `def test_narrator_returns_time_elapsed()`
- `def test_narrator_returns_mutations()`
- `class TestFullGameplayLoop`
- `def test_scene_to_tick_to_flip_to_resolution()`
- `def test_player_discovers_world_moved()`
- `class TestSemanticSearchImplementation`
- `def test_embed_narrative()`
- `def test_semantic_query()`
- `class TestMomentImplementation`
- `def test_moment_created_for_dialogue()`
- `def test_moment_searchable_by_content()`

**Definitions:**
- `def build_test_character()`
- `def build_test_narrative()`
- `def build_belief_link()`
- `class TestIKnowThem`
- `def test_character_beliefs_are_links()`
- `def test_belief_link_captures_knowledge()`
- `def test_belief_source_is_tracked()`
- `def test_character_personality_predicts_behavior()`
- `def test_character_voice_is_consistent()`
- `class TestTheyRemembered`
- `def test_narrative_persists()`
- `def test_core_types_persist_longer()`
- `def test_narrative_has_voice_for_surfacing()`
- `def test_weight_affects_surfacing()`
- `class TestTheWorldMoved`
- `def test_tensions_accumulate_over_time()`
- `def test_tension_flips_when_pressure_high()`
- `def test_scheduled_tension_follows_timeline()`
- `def test_multiple_tensions_can_exist()`
- `class TestIWasWrong`
- `def test_narrative_can_be_false()`
- `def test_truth_is_not_visible_to_player()`
- `def test_character_can_believe_lie()`
- `def test_contradicting_narratives_create_tension()`
- `class TestAntiPatterns`
- `def test_no_quest_completion_field()`
- `def test_no_optimal_score()`
- `def test_characters_have_distinctive_voice()`
- `def test_characters_have_distinctive_flaw()`
- `class TestCompleteGameplayLoop`
- `def test_scene_produces_moment()`
- `def test_tension_accumulates_during_scene()`
- `def test_flip_produces_world_runner_event()`
- `def test_world_runner_creates_new_narratives()`
- `def test_new_narrative_propagates_beliefs()`

**Definitions:**
- `class TestCharacterModel`
- `def test_character_required_fields()`
- `def test_character_type_default()`
- `def test_character_type_enum_validation()`
- `def test_character_alive_default()`
- `def test_character_skills_default()`
- `def test_character_skills_validation()`
- `def test_character_personality_values()`
- `def test_character_embeddable_text()`
- `def test_character_embeddable_text_with_backstory()`
- `class TestPlaceModel`
- `def test_place_required_fields()`
- `def test_place_type_default()`
- `def test_place_type_enum_validation()`
- `def test_place_atmosphere()`
- `def test_place_embeddable_text()`
- `class TestThingModel`
- `def test_thing_required_fields()`
- `def test_thing_type_default()`
- `def test_thing_significance_default()`
- `def test_thing_quantity_default()`
- `def test_thing_portable_default()`
- `def test_thing_non_portable()`
- `class TestNarrativeModel`
- `def test_narrative_required_fields()`
- `def test_narrative_weight_range()`
- `def test_narrative_focus_range()`
- `def test_narrative_truth_range()`
- `def test_narrative_is_core_type()`
- `def test_narrative_type_enum_validation()`
- `class TestTensionModel`
- `def test_tension_required_fields()`
- `def test_tension_pressure_range()`
- `def test_tension_breaking_point_range()`
- `def test_tension_breaking_point_default()`
- `def test_tension_pressure_type_default()`
- `def test_tension_has_flipped()`
- `def test_tension_tick_gradual()`
- `def test_tension_tick_gradual_respects_type()`
- `def test_tension_add_event_pressure()`
- `def test_tension_reset()`
- `class TestMomentModel`
- `def test_moment_required_fields()`
- `def test_moment_type_default()`
- `def test_moment_tick_non_negative()`
- `def test_moment_should_embed()`
- `def test_moment_embeddable_text()`
- `class TestCharacterNarrativeLink`
- `def test_believes_required_fields()`
- `def test_believes_value_ranges()`
- `def test_believes_defaults()`
- `def test_believes_source_enum()`
- `def test_belief_intensity()`
- `class TestNarrativeNarrativeLink`
- `def test_narrative_link_required_fields()`
- `def test_narrative_link_value_ranges()`
- `def test_narrative_link_type_property()`
- `class TestCharacterPlaceLink`
- `def test_at_link_required_fields()`
- `def test_at_link_present_range()`
- `def test_at_link_visible_default()`
- `class TestCharacterThingLink`
- `def test_carries_link_required_fields()`
- `def test_carries_link_has_item()`
- `class TestThingPlaceLink`
- `def test_located_at_required_fields()`
- `def test_located_at_specific_location()`
- `class TestPlacePlaceLink`
- `def test_place_link_required_fields()`
- `def test_place_link_travel_days()`
- `class TestModifier`
- `def test_modifier_required_type()`
- `def test_modifier_severity_default()`
- `def test_modifier_character_types()`
- `def test_modifier_place_types()`
- `def test_modifier_thing_types()`
- `class TestGameTimestamp`
- `def test_timestamp_creation()`
- `def test_timestamp_str()`
- `def test_timestamp_parse()`
- `def test_timestamp_comparison()`

**Definitions:**
- `def mock_graph_ops()`
- `def tracking_query()`
- `def mock_graph_queries()`
- `class TestMomentCreation`
- `def test_add_moment_basic()`
- `def test_add_moment_with_status_and_weight()`
- `def test_add_moment_with_tone()`
- `def test_add_moment_with_tick_spoken()`
- `def test_add_moment_with_speaker_creates_said_link()`
- `def test_add_moment_with_place_creates_at_link()`
- `def test_add_moment_with_after_creates_then_link()`
- `class TestCanSpeakLink`
- `def test_add_can_speak_basic()`
- `def test_add_can_speak_with_weight()`
- `class TestAttachedToLink`
- `def test_add_attached_to_basic()`
- `def test_add_attached_to_with_presence_required()`
- `def test_add_attached_to_non_persistent()`
- `def test_add_attached_to_dies_with_target()`
- `class TestCanLeadToLink`
- `def test_add_can_lead_to_basic()`
- `def test_add_can_lead_to_with_trigger()`
- `def test_add_can_lead_to_with_require_words()`
- `def test_add_can_lead_to_with_weight_transfer()`
- `def test_add_can_lead_to_bidirectional()`
- `def test_add_can_lead_to_with_wait_ticks()`
- `def test_add_can_lead_to_consumes_origin_false()`
- `class TestGetCurrentView`
- `def test_get_current_view_returns_structure()`
- `def test_get_current_view_queries_present_characters()`
- `class TestGetLiveMoments`
- `def test_get_live_moments_builds_correct_query()`
- `class TestResolveSpeaker`
- `def test_resolve_speaker_returns_highest_weight()`
- `def test_resolve_speaker_none_when_no_speakers()`
- `class TestGetAvailableTransitions`
- `def test_get_available_transitions_from_active()`
- `def test_get_available_transitions_empty_for_no_active()`
- `class TestGetClickableWords`
- `def test_get_clickable_words_extracts_from_transitions()`
- `class TestHandleClick`
- `def test_handle_click_no_transitions_queues_narrator()`
- `def test_handle_click_word_not_in_require_words()`
- `def test_handle_click_applies_weight_transfer()`
- `def tracking_query()`
- `def test_handle_click_flip_threshold()`
- `def tracking_query()`
- `def test_handle_click_no_flip_below_threshold()`
- `def tracking_query()`
- `class TestUpdateMomentWeight`
- `def test_update_weight_clamps_to_bounds()`
- `def tracking_query()`
- `def test_update_weight_triggers_flip()`
- `def tracking_query()`
- `def test_update_weight_no_flip_already_active()`
- `def tracking_query()`
- `class TestViewToSceneTree`
- `def test_view_to_scene_tree_basic_structure()`
- `def test_view_to_scene_tree_with_clickables()`
- `class TestInvariants`
- `def test_weight_bounds_invariant()`
- `def test_status_consistency_invariant()`
- `class TestBehavioralVisibility`
- `def test_presence_required_filters_correctly()`
- `class TestBehavioralSpeakerResolution`
- `def test_speaker_resolution_by_weight()`
- `class TestIntegrationConversationFlow`
- `def test_moment_creation_and_linking_flow()`
- `def test_click_to_flip_flow()`
- `def flow_query()`
- `class TestExtractMomentArgs`
- `def test_extract_moment_args_basic()`

**Definitions:**
- `def mock_moment_queries()`
- `def mock_moment_traversal()`
- `def mock_moment_surface()`
- `def mock_graph_queries()`
- `def test_client()`
- `class TestGetCurrentMoments`
- `def test_get_current_moments_basic()`
- `def test_get_current_moments_with_clickable_words()`
- `def test_get_current_moments_auto_location()`
- `def test_get_current_moments_with_present_chars()`
- `class TestClickWord`
- `def test_click_word_success()`
- `def test_click_word_no_match()`
- `def test_click_word_error_handling()`
- `class TestGetMoment`
- `def test_get_moment_exists()`
- `def test_get_moment_not_found()`
- `class TestSurfaceMoment`
- `def test_surface_moment()`
- `class TestMomentStats`
- `def test_get_stats()`
- `class TestMomentStream`
- `def test_stream_connection()`
- `class TestRequestValidation`
- `def test_click_requires_playthrough_id()`
- `def test_click_requires_moment_id()`
- `def test_surface_requires_both_ids()`
- `class TestResponseModels`
- `def test_current_moments_response_shape()`
- `def test_click_response_shape()`

**Definitions:**
- `def mock_graph_ops()`
- `def tracking_add_moment()`
- `def tracking_add_can_lead_to()`
- `def tracking_add_can_speak()`
- `def tracking_add_attached_to()`
- `def mock_moment_processor()`
- `class TestClickableParsing`
- `def test_parse_single_clickable()`
- `def test_parse_multiple_clickables()`
- `def test_parse_no_clickables()`
- `def test_parse_clickable_with_special_chars()`
- `class TestMomentProcessorSchema`
- `def test_process_dialogue_with_tone()`
- `def test_process_dialogue_with_weight_and_status()`
- `def test_process_narration_with_tone()`
- `def test_process_hint_defaults()`
- `def test_spoken_status_sets_tick_spoken()`
- `def test_possible_status_no_tick_spoken()`
- `class TestPossibleMomentCreation`
- `def test_create_possible_moment_basic()`
- `def test_create_possible_moment_with_attachments()`
- `class TestMomentLinking`
- `def test_link_moments_basic()`
- `def test_link_moments_with_weight_transfer()`
- `class TestGraphModeIntegration`
- `def test_create_moment_with_single_clickable()`
- `def test_create_moment_with_multiple_clickables()`
- `def test_create_moment_with_tone()`
- `class TestWeightActivation`
- `def test_weight_below_threshold_stays_possible()`

**Definitions:**
- `def extract_yaml_from_markdown()`
- `def extract_enums_from_schema()`
- `def find_enums()`
- `def extract_constants_from_content()`
- `class TestSchemaSpecAlignment`
- `def test_node_types_exist()`
- `def test_character_type_enum()`
- `def test_narrative_type_enum()`
- `class TestEnumConsistency`
- `def test_character_types_complete()`
- `def test_place_scales_hierarchical()`
- `def test_narrative_types_cover_all_categories()`
- `def test_skill_levels_ordered()`
- `def test_pressure_types_complete()`
- `def test_moment_types_cover_all_sources()`
- `class TestConstantsConsistency`
- `def test_belief_flow_rate_valid()`
- `def test_max_propagation_hops_positive()`
- `def test_decay_rate_valid()`
- `def test_min_weight_small()`
- `def test_breaking_point_valid()`
- `def test_link_factors_sum_reasonable()`
- `def test_link_factors_all_positive()`
- `def test_supersedes_has_drain_effect()`
- `def test_contradicts_highest_factor()`
- `class TestSpecInternalConsistency`
- `def test_core_types_for_slow_decay()`
- `def test_character_flaws_distinct()`
- `def test_voice_styles_cover_emotional_range()`
- `def test_modifier_types_cover_all_node_types()`
- `def test_road_types_have_speed_ordering()`
- `class TestCrossReferences`
- `def test_tension_references_narratives()`
- `def test_belief_source_types_make_sense()`
- `def test_narrative_about_fields_valid()`

**Docs:** `docs/world/map/PATTERNS_Map.md`

**Definitions:**
- `class SemanticSearch`
- `def __init__()`
- `def find()`
- `def find_similar()`
- `def find_narratives_like()`
- `def find_characters_like()`
- `def answer_question()`
- `def _vector_search()`
- `def _fallback_search()`
- `def _get_node_with_embedding()`
- `def get_semantic_search()`

**Definitions:**
- `def create_indexes()`
- `def load_initial_state()`
- `def verify_data()`
- `def main()`

**Definitions:**
- `def main()`

**Docs:** `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`

**Definitions:**
- `handleBegin()`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `rollRandomName()`
- `handleBegin()`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `ChroniclePanel()`
- `handleSubmit()`
- `handleKeyDown()`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `DebugPanel()`
- `connectSSE()`
- `addEvent()`
- `clearEvents()`
- `getEventColor()`
- `handleQuery()`
- `getTypeColor()`
- `formatEventSummary()`

**Definitions:**
- `getPlaceVisibility()`
- `getRouteVisibility()`
- `wobblePoint()`
- `drawParchmentLayer()`
- `drawTerrainLayer()`
- `radiusPx()`
- `cpx()`
- `cpy()`
- `drawCoastlineLayer()`
- `midX()`
- `midY()`
- `drawRoutesLayer()`
- `drawFogLayer()`
- `drawPlacesLayer()`
- `drawMarkersLayer()`
- `drawUILayer()`
- `MapCanvas()`

**Docs:** `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`

**Definitions:**
- `MapClient()`
- `updateDimensions()`

**Docs:** `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`

**Definitions:**
- `Minimap()`

**Docs:** `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md (Future UI: Minimap + Sun Arc)`

**Definitions:**
- `SunArc()`
- `dayProgress()`
- `getPeriod()`

**Definitions:**
- `ClickableText()`

**Definitions:**
- `MomentDebugPanel()`
- `getTransitionsFrom()`
- `getTransitionsTo()`
- `StatusBadge()`
- `WeightBar()`

**Definitions:**
- `getCharacterImageUrl()`
- `MomentDisplay()`
- `getTypeStyles()`
- `getToneStyles()`
- `getAnimationClass()`
- `getStatusBadge()`
- `renderText()`

**Definitions:**
- `MomentStream()`
- `handleWordClick()`

**Definitions:**
- `ChronicleTab()`

**Definitions:**
- `ConversationsTab()`

**Definitions:**
- `LedgerTab()`
- `renderSection()`

**Docs:** `docs/frontend/right-panel/PATTERNS_Tabbed_Right_Panel.md`

**Definitions:**
- `RightPanel()`

**Definitions:**
- `calculateReadTime()`
- `AnimatedLine()`
- `TypingIndicator()`
- `ClickableWord()`
- `MomentText()`
- `MomentBlock()`
- `useRevealAnimation()`
- `CenterStage()`
- `handleWordClick()`
- `handleSubmit()`
- `getReadTime()`

**Definitions:**
- `CharacterRow()`

**Definitions:**
- `Hotspot()`
- `handleClick()`
- `handleAction()`

**Definitions:**
- `HotspotRow()`

**Definitions:**
- `ObjectRow()`

**Definitions:**
- `getFallbackStyle()`
- `SceneBanner()`

**Definitions:**
- `SceneHeader()`

**Definitions:**
- `SceneImage()`
- `handleBackgroundClick()`

**Docs:** `docs/frontend/scene/PATTERNS_Scene.md`

**Definitions:**
- `SceneView()`

**Definitions:**
- `SettingStrip()`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `showToast()`
- `useToast()`
- `ToastProvider()`
- `ToastItem()`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `Voices()`

**Definitions:**
- `GameClient()`
- `handleAction()`

**Definitions:**
- `GameLayout()`

**Definitions:**
- `SpeedControl()`
- `fetchSpeed()`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `useGameState()`
- `moments()`
- `mapPlaceType()`
- `transformScene()`
- `clickables()`
- `transformVoices()`
- `transformViewToScene()`
- `transformMomentsToVoices()`
- `createFallbackScene()`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `useMoments()`

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `useTempo()`
- `fetchState()`

**Docs:** `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`

**Definitions:**
- `project()`
- `x()`
- `y()`
- `unproject()`
- `lng()`
- `haversine()`
- `lat1()`
- `lon1()`
- `lat2()`
- `lon2()`
- `routeDistance()`
- `getPositionAtProgress()`
- `t()`

**Docs:** `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`

**Definitions:**
- `seededRandom()`
- `hashString()`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Definitions:**
- `handleApiError()`
- `createPlaythrough()`
- `sendMoment()`
- `getPlaythrough()`
- `getMap()`
- `getFaces()`
- `getLedger()`
- `getChronicle()`
- `semanticQuery()`
- `fetchCurrentMoments()`
- `clickMoment()`
- `getMomentStats()`
- `subscribeToMomentStream()`
- `getCurrentView()`
- `checkHealth()`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Docs:** `docs/frontend/PATTERNS_Presentation_Layer.md`

**Sections:**
- # Discussion Tree Generator
- ## Input
- ## Output
- ## Format
- ## Guidelines
- ## Topic Categories
- ## Example
- ## Invocation

**Docs:** `docs/infrastructure/canon/TEST_Canon.md`

**Definitions:**
- `def mock_graph_queries()`
- `def mock_canon_holder()`
- `def mock_broadcast()`
- `class TestDetermineSpeaker`
- `def test_q5_speaker_present_and_awake()`
- `def test_q5_no_speaker_returns_none()`
- `class TestRecordToCanon`
- `def test_q6_moment_not_found()`
- `def test_q6_already_spoken()`
- `def test_q6_dialogue_no_speaker()`
- `def mock_query()`
- `def test_q6_narration_succeeds()`
- `def mock_query()`
- `class TestGetLastSpokenMoment`
- `def test_q7_returns_latest()`
- `def test_q7_no_spoken_returns_none()`
- `class TestBehaviorB3EnergyConservation`
- `def test_energy_reduced_on_record()`
- `def mock_query()`
- `class TestBehaviorB4HighestSpeakerWins`
- `def test_highest_strength_selected()`
- `class TestBehaviorB9DialogueWithoutSpeakerWaits`
- `def test_dialogue_stays_active_without_speaker()`
- `def mock_query()`
- `class TestEdgeCaseE1FirstMoment`
- `def test_first_moment_no_then_link()`
- `def mock_query()`
- `class TestEdgeCaseE2NarrationMoment`
- `def test_narration_no_said_link()`
- `def mock_query()`
- `class TestEdgeCaseE4PlayerCaused`
- `def test_player_caused_flag_on_then_link()`
- `def mock_query()`
- `class TestSSEBroadcast`
- `def test_moment_spoken_event_sent()`
- `def mock_query()`
- `class TestInvariantV4EnergyConservation`
- `def test_energy_formula()`
- `def mock_query()`

**Docs:** `docs/infrastructure/world-builder/TEST_World_Builder.md`

**Definitions:**
- `def mock_graph()`
- `def mock_semantic_search()`
- `def mock_embed_fn()`
- `def embed()`
- `def mock_count_links_fn()`
- `def count_links()`
- `def sample_enrichment()`
- `def mock_llm_yaml_response()`
- `class TestSparsityDetection`
- `def test_empty_results_sparse()`
- `def test_single_result_sparse()`
- `def test_rich_results_not_sparse()`
- `def high_links()`
- `def test_sparsity_result_complete()`
- `def test_cosine_similarity()`
- `def test_cosine_similarity_none_input()`
- `def test_node_to_text_priority()`
- `def test_no_embeddings_fallback()`
- `class TestQueryMomentRecording`
- `def test_record_creates_moment()`
- `def test_moment_type_thought_with_char()`
- `def test_moment_type_query_without_char()`
- `def test_moment_links_to_character()`
- `def test_moment_links_to_place()`
- `def test_link_results_to_moment()`
- `def test_link_weight_from_similarity()`
- `class TestWorldBuilderClass`
- `def test_init_with_api_key()`
- `def test_init_from_env()`
- `def test_init_no_key_warning()`
- `def test_cache_key_generation()`
- `async def test_cache_prevents_reenrichment()`
- `async def test_no_api_key_returns_none()`
- `def test_parse_yaml_from_code_fence()`
- `def test_parse_plain_yaml()`
- `def test_parse_invalid_yaml()`
- `def test_clear_cache()`
- `async def test_recursion_prevention()`
- `class TestEnrichmentApplication`
- `def test_apply_creates_characters()`
- `def test_apply_creates_places()`
- `def test_apply_creates_things()`
- `def test_apply_creates_narratives()`
- `def test_apply_creates_links()`
- `def test_apply_creates_moments()`
- `def test_generated_flag_set()`
- `def test_link_to_query_moment()`
- `def test_moment_links_to_speaker()`
- `def test_build_enrichment_prompt()`
- `def _get_query_module()`
- `class TestQueryInterface`
- `async def test_query_records_moment()`
- `async def test_query_executes_search()`
- `async def test_query_returns_results()`
- `def test_query_sync_no_enrichment()`
- `async def test_query_enriches_sparse_results()`
- `class TestEdgeCases`
- `def test_empty_enrichment()`
- `def test_enrichment_missing_id()`
- `def test_moment_missing_text()`
- `async def test_search_failure_graceful()`
- `def test_graph_failure_graceful()`
- `class TestInvariants`
- `def test_v1_query_creates_moment()`
- `def test_v5_moments_always_thought()`
- `def test_v6_sparsity_thresholds()`

**Sections:**
- # Image Generation Tool
- # DOCS: docs/infrastructure/image-generation/PATTERNS_Image_Generation.md
- ## Setup
- ## Usage
- ## Image Types
- ## Examples
- ## Options
- ## Output
- ## Style

**Docs:** `docs/infrastructure/image-generation/PATTERNS_Image_Generation.md`

**Definitions:**
- `def generate_image()`
- `def main()`

**Docs:** `docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md`

**Definitions:**
- `def get_playthrough_graph_name()`
- `def get_graph_ops()`
- `def get_graph_queries()`
- `def get_current_tick()`
- `def get_current_place()`
- `def create_moment_with_clickables()`
- `def parse_inline_clickables()`
- `def replace_match()`
- `def stream_event()`
- `def main()`

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`
- `views/VIEW_Test_Write_Tests_And_Verify.md`

**Sections:**
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## How These Principles Integrate
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 5. Communication Principles

**Sections:**
- # Context Protocol
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- # ADD Framework
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- # ngram
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change

**Sections:**
- # The Blood Ledger
- ## Launch Protocol
- # Or if first time:
- # docker run -d --name falkordb -p 6379:6379 -p 3002:3000 falkordb/falkordb
- ## Moment Graph Sample Data
- ## Service Summary

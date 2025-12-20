# Repository Map: the-blood-ledger

*Generated: 2025-12-20 17:54*

- **Files:** 362
- **Directories:** 107
- **Total Size:** 2.2M
- **Doc Files:** 282
- **Code Files:** 76
- **Areas:** 10 (docs/ subfolders)
- **Modules:** 48 (subfolders in areas)
- **DOCS Links:** 40 (0.53 avg per code file)

- markdown: 282
- tsx: 33
- python: 31
- typescript: 9
- css: 1
- html: 1
- shell: 1

```
├── agents/ (51.8K)
│   ├── developer/ (6.4K)
│   │   └── CLAUDE.md (6.4K)
│   ├── narrator/ (32.9K)
│   │   └── CLAUDE_old.md (32.9K)
│   └── world-builder/ (12.6K)
│       └── CLAUDE.md (12.6K)
├── docs/ (1.3M)
│   ├── concepts/ (3.5K)
│   │   └── subjective-truth-and-rumor/ (3.5K)
│   │       ├── CONCEPT_Subjective_Truth_And_Rumor.md (1.7K)
│   │       └── TOUCHES_Subjective_Truth_And_Rumor.md (1.8K)
│   ├── design/ (185.7K)
│   │   ├── archive/ (905)
│   │   │   └── SYNC_archive_2024-12.md (905)
│   │   ├── opening/ (106.7K)
│   │   │   ├── ALGORITHM_Opening.md (3.8K)
│   │   │   ├── BEHAVIORS_Opening.md (8.7K)
│   │   │   ├── CLAUDE.md (25.9K)
│   │   │   ├── CONTENT.md (10.2K)
│   │   │   ├── GUIDE.md (9.5K)
│   │   │   ├── HEALTH_Opening.md (7.5K)
│   │   │   ├── IMPLEMENTATION_Opening.md (10.4K)
│   │   │   ├── PATTERNS_Opening.md (10.8K)
│   │   │   ├── SYNC_Opening.md (6.4K)
│   │   │   ├── VALIDATION_Opening.md (10.7K)
│   │   │   └── (..1 more files)
│   │   ├── scenarios/ (10.3K)
│   │   │   └── README.md (10.3K)
│   │   ├── ALGORITHM_Vision.md (13.4K)
│   │   ├── BEHAVIORS_Vision.md (10.1K)
│   │   ├── IMPLEMENTATION_Vision.md (8.3K)
│   │   ├── PATTERNS_Vision.md (11.9K)
│   │   ├── SYNC_Vision.md (7.5K)
│   │   ├── SYNC_Vision_archive_2025-12.md (3.5K)
│   │   ├── TEST_Vision.md (3.2K)
│   │   └── VALIDATION_Vision.md (10.0K)
│   ├── engine/ (20.5K)
│   │   └── tests/ (20.5K)
│   │       ├── ALGORITHM_Test_Run_Flow.md (1.7K)
│   │       ├── BEHAVIORS_Test_Coverage_Layers.md (2.1K)
│   │       ├── IMPLEMENTATION_Test_File_Layout.md (4.4K)
│   │       ├── PATTERNS_Spec_Linked_Test_Suite.md (3.8K)
│   │       ├── SYNC_Engine_Test_Suite.md (5.1K)
│   │       ├── TEST_Test_Suite_Coverage.md (1.8K)
│   │       └── VALIDATION_Test_Suite_Invariants.md (1.5K)
│   ├── frontend/ (100.4K)
│   │   ├── IMPLEMENTATION_Frontend_Code_Architecture/ (5.2K)
│   │   │   └── IMPLEMENTATION_Runtime_And_Config.md (5.2K)
│   │   ├── archive/ (1.6K)
│   │   │   └── SYNC_archive_2024-12.md (1.6K)
│   │   ├── map/ (3.5K)
│   │   │   ├── PATTERNS_Parchment_Map_View.md (2.9K)
│   │   │   └── SYNC_Map_View.md (609)
│   │   ├── minimap/ (6.2K)
│   │   │   ├── PATTERNS_Discovered_Location_Minimap.md (2.4K)
│   │   │   └── SYNC_Minimap.md (3.9K)
│   │   ├── right-panel/ (6.7K)
│   │   │   ├── PATTERNS_Tabbed_Right_Panel.md (2.8K)
│   │   │   └── SYNC_Right_Panel.md (4.0K)
│   │   ├── scenarios/ (7.5K)
│   │   │   ├── PATTERNS_Scenario_Selection.md (3.7K)
│   │   │   └── SYNC_Scenario_Selection.md (3.8K)
│   │   ├── scene/ (33.0K)
│   │   │   ├── ALGORITHM_Scene.md (4.6K)
│   │   │   ├── BEHAVIORS_Scene.md (3.4K)
│   │   │   ├── PATTERNS_Scene.md (7.4K)
│   │   │   ├── SYNC_Scene.md (5.3K)
│   │   │   ├── SYNC_Scene_archive_2025-12.md (5.5K)
│   │   │   ├── TEST_Scene.md (3.6K)
│   │   │   └── VALIDATION_Scene.md (3.2K)
│   │   ├── ALGORITHM_Frontend_Data_Flow.md (7.6K)
│   │   ├── BEHAVIORS_Frontend_State_And_Interaction.md (4.1K)
│   │   ├── IMPLEMENTATION_Frontend_Code_Architecture.md (1.7K)
│   │   ├── PATTERNS_Presentation_Layer.md (6.0K)
│   │   ├── SYNC_Frontend.md (7.9K)
│   │   ├── SYNC_Frontend_archive_2025-12.md (3.4K)
│   │   ├── TEST_Frontend_Coverage.md (1.7K)
│   │   └── VALIDATION_Frontend_Invariants.md (4.2K)
│   ├── infrastructure/ (421.8K)
│   │   ├── async/ (76.8K)
│   │   │   ├── ALGORITHM/ (20.4K)
│   │   │   │   ├── ALGORITHM_Discussion_Trees.md (1.3K)
│   │   │   │   ├── ALGORITHM_Graph_SSE.md (2.9K)
│   │   │   │   ├── ALGORITHM_Hook_Injection.md (4.0K)
│   │   │   │   ├── ALGORITHM_Image_Generation.md (2.8K)
│   │   │   │   ├── ALGORITHM_Overview.md (992)
│   │   │   │   ├── ALGORITHM_Runner_Protocol.md (3.9K)
│   │   │   │   └── ALGORITHM_Waypoints_And_Fog.md (4.5K)
│   │   │   ├── archive/ (8.2K)
│   │   │   │   └── SYNC_archive_2024-12.md (8.2K)
│   │   │   ├── ALGORITHM_Async_Architecture.md (4.0K)
│   │   │   ├── BEHAVIORS_Travel_Experience.md (5.1K)
│   │   │   ├── IMPLEMENTATION_Async_Architecture.md (8.3K)
│   │   │   ├── PATTERNS_Async_Architecture.md (9.0K)
│   │   │   ├── SYNC_Async_Architecture.md (12.3K)
│   │   │   ├── SYNC_Async_Architecture_archive_2025-12.md (4.4K)
│   │   │   ├── TEST_Async_Architecture.md (3.8K)
│   │   │   └── VALIDATION_Async_Architecture.md (1.2K)
│   │   ├── canon/ (33.4K)
│   │   │   ├── ALGORITHM_Canon_Holder.md (7.4K)
│   │   │   ├── BEHAVIORS_Canon.md (5.2K)
│   │   │   ├── IMPLEMENTATION_Canon.md (5.2K)
│   │   │   ├── PATTERNS_Canon.md (4.2K)
│   │   │   ├── SYNC_Canon.md (1.7K)
│   │   │   ├── TEST_Canon.md (3.5K)
│   │   │   └── VALIDATION_Canon.md (6.1K)
│   │   ├── cli-tools/ (35.1K)
│   │   │   ├── ALGORITHM_CLI_Tool_Flows.md (4.8K)
│   │   │   ├── BEHAVIORS_CLI_Streaming_And_Image_Output.md (4.9K)
│   │   │   ├── IMPLEMENTATION_CLI_Tools_Architecture.md (7.3K)
│   │   │   ├── PATTERNS_CLI_Agent_Utilities.md (5.5K)
│   │   │   ├── SYNC_CLI_Tools.md (5.7K)
│   │   │   ├── TEST_CLI_Tool_Coverage.md (2.9K)
│   │   │   └── VALIDATION_CLI_Tool_Invariants.md (3.9K)
│   │   ├── embeddings/ (60.5K)
│   │   │   ├── ALGORITHM/ (6.0K)
│   │   │   │   ├── ALGORITHM_Indexing.md (2.4K)
│   │   │   │   ├── ALGORITHM_Overview.md (1.8K)
│   │   │   │   └── ALGORITHM_Search.md (1.7K)
│   │   │   ├── TEST/ (4.9K)
│   │   │   │   ├── TEST_Cases.md (3.3K)
│   │   │   │   └── TEST_Overview.md (1.6K)
│   │   │   ├── archive/ (3.1K)
│   │   │   │   └── SYNC_archive_2024-12.md (3.1K)
│   │   │   ├── ALGORITHM_Embeddings.md (3.7K)
│   │   │   ├── BEHAVIORS_Embeddings.md (5.5K)
│   │   │   ├── IMPLEMENTATION_Embeddings.md (4.6K)
│   │   │   ├── PATTERNS_Embeddings.md (5.9K)
│   │   │   ├── SYNC_Embeddings.md (5.6K)
│   │   │   ├── SYNC_Embeddings_archive_2025-12.md (10.6K)
│   │   │   ├── TEST_Embeddings.md (3.6K)
│   │   │   └── VALIDATION_Embeddings.md (7.1K)
│   │   ├── history/ (62.4K)
│   │   │   ├── ALGORITHM/ (6.3K)
│   │   │   │   ├── ALGORITHM_Overview.md (1.2K)
│   │   │   │   ├── ALGORITHM_Propagation_and_Beliefs.md (1.5K)
│   │   │   │   └── ALGORITHM_Query_and_Record.md (3.6K)
│   │   │   ├── TEST/ (3.9K)
│   │   │   │   ├── TEST_Cases.md (2.8K)
│   │   │   │   └── TEST_Overview.md (1.1K)
│   │   │   ├── archive/ (8.9K)
│   │   │   │   ├── SYNC_History_archive_2025-12.md (7.7K)
│   │   │   │   └── SYNC_archive_2024-12.md (1.2K)
│   │   │   ├── ALGORITHM_History.md (3.5K)
│   │   │   ├── BEHAVIORS_History.md (7.1K)
│   │   │   ├── IMPLEMENTATION_History_Service_Architecture.md (11.3K)
│   │   │   ├── PATTERNS_History.md (6.0K)
│   │   │   ├── SYNC_History.md (7.2K)
│   │   │   ├── TEST_History.md (543)
│   │   │   └── VALIDATION_History.md (7.6K)
│   │   ├── image-generation/ (26.4K)
│   │   │   ├── ALGORITHM_Image_Generation.md (1.2K)
│   │   │   ├── BEHAVIORS_Image_Generation.md (1.2K)
│   │   │   ├── IMPLEMENTATION_Image_Generation.md (8.2K)
│   │   │   ├── PATTERNS_Image_Generation.md (10.2K)
│   │   │   ├── SYNC_Image_Generation.md (3.8K)
│   │   │   ├── TEST_Image_Generation.md (904)
│   │   │   └── VALIDATION_Image_Generation.md (856)
│   │   ├── ops-scripts/ (13.2K)
│   │   │   ├── ALGORITHM_Seeding_And_Backfill_Flows.md (1.4K)
│   │   │   ├── BEHAVIORS_Operational_Script_Runbooks.md (1.5K)
│   │   │   ├── IMPLEMENTATION_Engine_Scripts_Layout.md (1.6K)
│   │   │   ├── PATTERNS_Operational_Seeding_And_Backfill_Scripts.md (2.5K)
│   │   │   ├── SYNC_Ops_Scripts.md (4.0K)
│   │   │   ├── TEST_Operational_Scripts.md (908)
│   │   │   └── VALIDATION_Operational_Script_Safety.md (1.2K)
│   │   ├── storm-loader/ (18.4K)
│   │   │   ├── BEHAVIORS_Storm_Loader_Mutations.md (2.5K)
│   │   │   ├── IMPLEMENTATION_Storm_Loader.md (3.3K)
│   │   │   ├── MECHANISMS_Storm_Loader_Pipeline.md (2.6K)
│   │   │   ├── PATTERNS_Storm_Loader_As_Diff.md (3.1K)
│   │   │   ├── SYNC_Storm_Loader.md (2.5K)
│   │   │   ├── TEST_Storm_Loader.md (1.7K)
│   │   │   └── VALIDATION_Storm_Loader_Invariants.md (2.6K)
│   │   ├── storms/ (18.7K)
│   │   │   ├── BEHAVIORS_Storm_Overlay_Behavior.md (2.6K)
│   │   │   ├── IMPLEMENTATION_Storms.md (3.3K)
│   │   │   ├── MECHANISMS_Storm_Application.md (2.9K)
│   │   │   ├── PATTERNS_Storms_As_Crisis_Overlays.md (3.2K)
│   │   │   ├── SYNC_Storms.md (2.6K)
│   │   │   ├── TEST_Storms.md (1.6K)
│   │   │   └── VALIDATION_Storm_Invariants.md (2.6K)
│   │   ├── tempo/ (42.0K)
│   │   │   ├── ALGORITHM_Tempo_Controller.md (12.3K)
│   │   │   ├── BEHAVIORS_Tempo.md (3.3K)
│   │   │   ├── IMPLEMENTATION_Tempo.md (10.3K)
│   │   │   ├── PATTERNS_Tempo.md (3.9K)
│   │   │   ├── SYNC_Tempo.md (6.1K)
│   │   │   ├── TEST_Tempo.md (2.4K)
│   │   │   └── VALIDATION_Tempo.md (3.7K)
│   │   └── world-builder/ (34.8K)
│   │       ├── ALGORITHM/ (3.8K)
│   │       │   ├── ALGORITHM_Details.md (1.5K)
│   │       │   └── ALGORITHM_Overview.md (2.3K)
│   │       ├── IMPLEMENTATION/ (4.3K)
│   │       │   ├── IMPLEMENTATION_Flow.md (1.7K)
│   │       │   └── IMPLEMENTATION_Overview.md (2.6K)
│   │       ├── TEST/ (2.3K)
│   │       │   ├── TEST_Cases.md (985)
│   │       │   └── TEST_Overview.md (1.4K)
│   │       ├── VALIDATION/ (3.0K)
│   │       │   ├── VALIDATION_Checks.md (1.2K)
│   │       │   └── VALIDATION_Overview.md (1.9K)
│   │       ├── archive/ (1.3K)
│   │       │   └── SYNC_archive_2024-12.md (1.3K)
│   │       ├── ALGORITHM_World_Builder.md (672)
│   │       ├── BEHAVIORS_World_Builder.md (3.6K)
│   │       ├── IMPLEMENTATION_World_Builder.md (672)
│   │       ├── PATTERNS_World_Builder.md (4.2K)
│   │       ├── SYNC_World_Builder.md (4.5K)
│   │       ├── SYNC_World_Builder_archive_2025-12.md (5.2K)
│   │       ├── TEST_World_Builder.md (606)
│   │       └── VALIDATION_World_Builder.md (646)
│   ├── network/ (139.5K)
│   │   ├── bleed-through/ (26.3K)
│   │   │   ├── BEHAVIORS_Bleed_Reports.md (3.3K)
│   │   │   ├── BEHAVIORS_Ghosts_Rumors_Reports.md (3.0K)
│   │   │   ├── IMPLEMENTATION_Bleed_Through.md (3.3K)
│   │   │   ├── MECHANISMS_Bleed_Through_Pipeline.md (3.7K)
│   │   │   ├── PATTERNS_Scars_Cross_Worlds.md (3.5K)
│   │   │   ├── SYNC_Bleed_Through.md (4.9K)
│   │   │   ├── TEST_Bleed_Through.md (1.7K)
│   │   │   └── VALIDATION_Bleed_Through_Safety.md (2.9K)
│   │   ├── ghost-dialogue/ (18.6K)
│   │   │   ├── BEHAVIORS_Ghost_Dialogue_Replay.md (2.7K)
│   │   │   ├── IMPLEMENTATION_Ghost_Dialogue.md (3.4K)
│   │   │   ├── MECHANISMS_Dialogue_Index.md (2.8K)
│   │   │   ├── PATTERNS_Ghost_Dialogue_Index.md (3.0K)
│   │   │   ├── SYNC_Ghost_Dialogue.md (2.7K)
│   │   │   ├── TEST_Ghost_Dialogue.md (1.7K)
│   │   │   └── VALIDATION_Ghost_Dialogue_Safety.md (2.4K)
│   │   ├── shadow-feed/ (18.6K)
│   │   │   ├── BEHAVIORS_Rumor_Import.md (2.7K)
│   │   │   ├── IMPLEMENTATION_Shadow_Feed.md (3.3K)
│   │   │   ├── MECHANISMS_Shadow_Feed_Filtering.md (2.5K)
│   │   │   ├── PATTERNS_Shadow_Feed_Rumor_Cache.md (3.1K)
│   │   │   ├── SYNC_Shadow_Feed.md (2.6K)
│   │   │   ├── TEST_Shadow_Feed.md (1.6K)
│   │   │   └── VALIDATION_Shadow_Feed_Locks.md (2.7K)
│   │   ├── transposition/ (31.1K)
│   │   │   ├── ALGORITHM_Transposition_Pipeline.md (5.8K)
│   │   │   ├── BEHAVIORS_Conflict_Resolution_Cascade.md (3.0K)
│   │   │   ├── IMPLEMENTATION_Transposition.md (3.4K)
│   │   │   ├── MECHANISMS_Transposition_Pipeline.md (3.4K)
│   │   │   ├── PATTERNS_Local_Canon_Primary.md (2.8K)
│   │   │   ├── SYNC_Transposition.md (3.0K)
│   │   │   ├── SYNC_Transposition_Logic.md (5.2K)
│   │   │   ├── TEST_Transposition.md (1.7K)
│   │   │   └── VALIDATION_Transposition_Invariants.md (2.7K)
│   │   ├── voyager-system/ (25.3K)
│   │   │   ├── BEHAVIORS_Voyager_Import_Experience.md (4.0K)
│   │   │   ├── IMPLEMENTATION_Voyager_System.md (3.4K)
│   │   │   ├── MECHANISMS_Export_Import_Transposition.md (4.4K)
│   │   │   ├── PATTERNS_Trauma_Without_Memory.md (4.6K)
│   │   │   ├── SYNC_Voyager_System.md (3.7K)
│   │   │   ├── TEST_Voyager_System.md (1.7K)
│   │   │   └── VALIDATION_Voyager_Invariants.md (3.6K)
│   │   └── world-scavenger/ (19.5K)
│   │       ├── BEHAVIORS_Scavenger_Priority_Stack.md (2.7K)
│   │       ├── IMPLEMENTATION_World_Scavenger.md (3.3K)
│   │       ├── MECHANISMS_Scavenger_Caches.md (3.1K)
│   │       ├── PATTERNS_Scavenge_Before_Generate.md (3.2K)
│   │       ├── SYNC_World_Scavenger.md (2.8K)
│   │       ├── TEST_World_Scavenger.md (1.7K)
│   │       └── VALIDATION_Scavenger_Locks.md (2.7K)
│   ├── product/ (140.6K)
│   │   ├── billing/ (25.3K)
│   │   │   ├── BEHAVIORS_Metered_Billing_Experience.md (2.7K)
│   │   │   ├── IMPLEMENTATION_Billing.md (3.3K)
│   │   │   ├── IMPLEMENTATION_Billing_Technical_Stack.md (3.5K)
│   │   │   ├── MECHANISMS_Billing_Metered_Stripe.md (2.4K)
│   │   │   ├── PATTERNS_Pay_To_Preserve_History.md (2.2K)
│   │   │   ├── SYNC_Billing.md (2.5K)
│   │   │   ├── SYNC_Billing_System.md (4.5K)
│   │   │   ├── TEST_Billing.md (1.6K)
│   │   │   └── VALIDATION_Billing_Invariants.md (2.6K)
│   │   ├── business-model/ (45.9K)
│   │   │   ├── ALGORITHM_Hallucination_Defense.md (5.3K)
│   │   │   ├── ALGORITHM_Semantic_Cache.md (3.3K)
│   │   │   ├── ALGORITHM_World_Scavenger.md (3.5K)
│   │   │   ├── BEHAVIORS_Retention_Mechanisms.md (7.9K)
│   │   │   ├── IMPLEMENTATION_Business_Model.md (3.4K)
│   │   │   ├── MECHANISMS_Margin_Defense.md (2.4K)
│   │   │   ├── PATTERNS_Market_Comparison.md (5.5K)
│   │   │   ├── PATTERNS_Whale_Economics.md (4.0K)
│   │   │   ├── SYNC_Business_Model.md (5.4K)
│   │   │   ├── VALIDATION_Business_Model_Invariants.md (2.4K)
│   │   │   └── (..3 more files)
│   │   ├── chronicle-system/ (33.4K)
│   │   │   ├── BEHAVIORS_Chronicle_Types_And_Structure.md (5.8K)
│   │   │   ├── IMPLEMENTATION_Chronicle_System.md (9.8K)
│   │   │   ├── IMPLEMENTATION_Chronicle_Technical_Pipeline.md (502)
│   │   │   ├── MECHANISMS_Chronicle_Pipeline.md (2.7K)
│   │   │   ├── PATTERNS_Chronicle_Flywheel.md (3.8K)
│   │   │   ├── SYNC_Chronicle_System.md (4.8K)
│   │   │   ├── TEST_Chronicle_System.md (1.7K)
│   │   │   ├── VALIDATION_Chronicle_Invariants.md (3.4K)
│   │   │   └── (..3 more files)
│   │   ├── gtm-strategy/ (17.9K)
│   │   │   ├── BEHAVIORS_Acquisition_Flywheel.md (2.4K)
│   │   │   ├── IMPLEMENTATION_GTM_Strategy.md (3.3K)
│   │   │   ├── MECHANISMS_GTM_Programs.md (2.5K)
│   │   │   ├── PATTERNS_Direct_Whale_Acquisition.md (3.0K)
│   │   │   ├── SYNC_GTM_Strategy.md (2.6K)
│   │   │   ├── TEST_GTM_Strategy.md (1.6K)
│   │   │   └── VALIDATION_GTM_Invariants.md (2.4K)
│   │   └── ledger-lock/ (18.1K)
│   │       ├── BEHAVIORS_Ledger_Lock_Trigger.md (2.5K)
│   │       ├── IMPLEMENTATION_Ledger_Lock.md (3.3K)
│   │       ├── MECHANISMS_Ledger_Lock_Flow.md (2.7K)
│   │       ├── PATTERNS_Ledger_Lock_Crisis.md (3.0K)
│   │       ├── SYNC_Ledger_Lock.md (2.5K)
│   │       ├── TEST_Ledger_Lock.md (1.6K)
│   │       └── VALIDATION_Ledger_Lock_Invariants.md (2.6K)
│   ├── schema/ (504)
│   │   └── archive/ (504)
│   │       └── SYNC_archive_2024-12.md (504)
│   ├── world/ (80.5K)
│   │   ├── map/ (35.7K)
│   │   │   ├── ALGORITHM/ (2.3K)
│   │   │   │   ├── places/ (765)
│   │   │   │   │   └── ALGORITHM_Places.md (765)
│   │   │   │   ├── rendering/ (777)
│   │   │   │   │   └── ALGORITHM_Rendering_Pipeline.md (777)
│   │   │   │   └── routes/ (765)
│   │   │   │       └── ALGORITHM_Routes.md (765)
│   │   │   ├── archive/ (384)
│   │   │   │   └── (..1 more files)
│   │   │   ├── ALGORITHM_Map.md (5.2K)
│   │   │   ├── BEHAVIORS_Map.md (4.4K)
│   │   │   ├── IMPLEMENTATION_Map_Code_Architecture.md (4.4K)
│   │   │   ├── PATTERNS_Map.md (4.2K)
│   │   │   ├── SYNC_Map.md (5.8K)
│   │   │   ├── SYNC_Map_archive_2025-12.md (2.2K)
│   │   │   ├── TEST_Map_Test_Coverage.md (3.3K)
│   │   │   └── VALIDATION_Map_Invariants.md (3.6K)
│   │   └── scraping/ (44.8K)
│   │       ├── ALGORITHM_Pipeline.md (14.4K)
│   │       ├── BEHAVIORS_World_Scraping.md (3.1K)
│   │       ├── IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md (5.1K)
│   │       ├── PATTERNS_World_Scraping.md (4.8K)
│   │       ├── SYNC_World_Scraping.md (2.0K)
│   │       ├── SYNC_World_Scraping_archive_2025-12.md (6.1K)
│   │       ├── TEST_World_Scraping.md (3.4K)
│   │       └── VALIDATION_World_Scraping.md (5.8K)
│   └── map.md (208.2K)
├── engine/ (255.7K)
│   ├── infrastructure/ (105.4K)
│   │   ├── canon/ (14.5K)
│   │   │   ├── __init__.py (805) →
│   │   │   ├── canon_holder.py (10.2K) →
│   │   │   └── speaker.py (3.5K) →
│   │   ├── history/ (34.7K)
│   │   │   ├── README.md (6.7K)
│   │   │   ├── __init__.py (1.6K)
│   │   │   ├── conversations.py (6.7K)
│   │   │   └── service.py (19.8K) →
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
│   ├── physics/ (627)
│   │   └── embeddings.py (627)
│   ├── scripts/ (12.8K)
│   │   ├── check_injection.py (1.4K) →
│   │   └── generate_images_for_existing.py (11.4K) →
│   ├── tests/ (123.0K)
│   │   ├── test_behaviors.py (18.3K)
│   │   ├── test_history.py (15.6K)
│   │   ├── test_implementation.py (31.2K)
│   │   ├── test_integration_scenarios.py (19.9K)
│   │   ├── test_models.py (28.6K)
│   │   ├── test_moment_standalone.py (9.3K)
│   │   └── (..1 more files)
│   ├── world/ (9.8K)
│   │   ├── map/ (9.7K)
│   │   │   ├── semantic.py (9.3K) →
│   │   │   └── (..1 more files)
│   │   └── (..1 more files)
│   ├── .env.example (540)
│   ├── Dockerfile (664)
│   ├── __init__.py (711)
│   ├── run.py (1.8K)
│   └── (..1 more files)
├── frontend/ (209.9K)
│   ├── app/ (17.4K)
│   │   ├── map/ (182)
│   │   │   └── (..1 more files)
│   │   ├── scenarios/ (7.1K)
│   │   │   └── page.tsx (7.1K) →
│   │   ├── start/ (6.7K)
│   │   │   └── page.tsx (6.7K) →
│   │   ├── globals.css (1.6K)
│   │   ├── layout.tsx (916) →
│   │   └── page.tsx (885) →
│   ├── components/ (136.6K)
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
│   │   ├── scene/ (40.1K)
│   │   │   ├── CenterStage.tsx (15.7K)
│   │   │   ├── CharacterRow.tsx (2.4K)
│   │   │   ├── Hotspot.tsx (2.6K)
│   │   │   ├── HotspotRow.tsx (2.8K)
│   │   │   ├── ObjectRow.tsx (2.1K)
│   │   │   ├── SceneBanner.tsx (2.6K)
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
│   │   ├── SpeedControl.tsx (3.6K) →
│   │   └── (..1 more files)
│   ├── hooks/ (23.7K)
│   │   ├── useGameState.ts (15.3K) →
│   │   ├── useMoments.ts (5.7K) →
│   │   └── useTempo.ts (2.8K) →
│   ├── lib/ (15.1K)
│   │   ├── map/ (3.6K)
│   │   │   ├── projection.ts (2.7K) →
│   │   │   ├── random.ts (777) →
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
│       └── world_builder/ (33.3K)
│           ├── test_world_builder.py (33.2K) →
│           └── (..1 more files)
├── tools/ (32.9K)
│   ├── image_generation/ (11.4K)
│   │   ├── README.md (2.3K)
│   │   └── generate_image.py (9.2K) →
│   ├── graph_scope_links.py (6.3K)
│   └── graph_scope_manual_classify.py (15.2K)
├── .gitignore (690)
├── .ngramignore (839)
├── AGENTS.md (25.3K)
├── Isomorphic_Architecture.md (20.1K)
├── README.md (1.2K)
├── create_project_files_pack_from_maps_and_repo.py (14.4K)
├── map.md (208.2K)
├── map_frontend.md (9.1K)
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

**Doc refs:**
- `docs/engine/moments/SCHEMA_Moments.md`

**Sections:**
- # Narrator Agent
- ## Quick Reference
- # GraphOps/GraphQueries live in the ngram repo graph runtime.
- # See data/ARCHITECTURE — Cybernetic Studio.md for the authoritative import path.
- # Query with natural language
- # Persist mutations
- ## 1. Execution Interface
- # Dialogue with inline clickables (graph-native — default)
- # Narration with clickables and tone
- # Signal time elapsed (significant actions only)
- # Signal completion
- # LEGACY MODE (not recommended) — Use --legacy-mode to write to scene.json
- # GraphOps lives in the ngram repo graph runtime.
- # See data/ARCHITECTURE — Cybernetic Studio.md for the authoritative import path.
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
- # GraphQueries lives in the ngram repo graph runtime.
- # See data/ARCHITECTURE — Cybernetic Studio.md for the authoritative import path.
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
- # GraphOps lives in the ngram repo graph runtime.
- # See data/ARCHITECTURE — Cybernetic Studio.md for the authoritative import path.
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
- # CONCEPT: Subjective Truth & Rumor — Canon vs Belief
- ## WHAT IT IS
- ## WHY IT EXISTS
- ## KEY PROPERTIES
- ## RELATIONSHIPS TO OTHER CONCEPTS
- ## THE CORE INSIGHT
- ## COMMON MISUNDERSTANDINGS
- ## SEE ALSO

**Doc refs:**
- `docs/network/transposition/PATTERNS_Local_Canon_Primary.md`

**Sections:**
- # TOUCHES: Where Subjective Truth & Rumor Appears in the System
- ## MODULES THAT IMPLEMENT
- ## INTERFACES
- ## DEPENDENCIES
- ## INVARIANTS ACROSS MODULES
- ## CONFLICTS / TENSIONS
- ## SYNC
- ## WHEN TO UPDATE THIS FILE

**Sections:**
- # Vision Archive — 2024-12
- ## Archived: Market Validation (CK3)
- ## Archived: Octalysis Mapping
- ## Archived: Engagement Levers

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`

**Sections:**
- # The Opening — Algorithm
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: _opening_to_scene_tree
- ## Primary Flow
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # The Opening — Behaviors: Player Experience
- ## CHAIN
- ## BEHAVIORS
- ## WHAT THE PLAYER EXPERIENCES
- ## INPUTS / OUTPUTS
- ## OBSERVABLE BEHAVIORS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `tools/stream_dialogue.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `docs/design/opening/GUIDE.md`

**Sections:**
- # Narrator Agent
- ## Quick Reference
- ## 1. Execution Interface
- # Dialogue with inline clickables
- # Narration with clickables
- # Scene with pre-baked responses
- # Signal time elapsed (significant actions only)
- # Signal completion
- # GraphOps apply examples now live in the ngram repo; this repo no longer
- # includes the graph runtime.
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

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/tests/test_opening_health.py`

**Sections:**
- # The Opening — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: opening_integrity
- ## INDICATOR: seed_graph_initialized
- ## INDICATOR: scenario_injection
- ## HOW TO RUN
- # Run opening health checks
- ## KNOWN GAPS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/opening/generator.py`
- `frontend/hooks/useGameState.ts`
- `playthroughs.py`

**Sections:**
- # The Opening — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # The Opening — Pattern
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## THE INSIGHT
- ## THE DESIGN PHILOSOPHY
- ## WHY THIS WORKS
- ## WHAT THIS PATTERN DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/orchestration/opening.py`
- `engine/orchestration/opening.py`

**Doc refs:**
- `docs/design/opening/CONTENT.md`

**Sections:**
- # The Opening — Sync
- ## Chain Reference
- ## MATURITY
- ## CURRENT STATE
- ## Code Locations
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Upcoming Work
- ## Notes
- ## Agent Observations

**Code refs:**
- `engine/infrastructure/api/playthroughs.py`

**Doc refs:**
- `docs/design/opening/TEST_Opening.md`

**Sections:**
- # The Opening — Validation
- ## CHAIN
- ## SUCCESS CRITERIA
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## METRICS (if we instrument)
- ## TEST SCENARIOS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## POST-OPENING VERIFICATION
- ## SYNC STATUS
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

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`

**Sections:**
- # Vision — Algorithm: Systems That Create Engagement
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: map_vision_systems
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## Purpose
- ## Architecture: Two Layers
- ## Engine Systems (Preliminary)
- ## Presentation Systems (Preliminary)
- ## What's Missing (Summary)
- ## Systems → Drives (Preliminary Mapping)
- ## Implementation Thinking (Summary)
- ## My Current Uncertainties
- ## Evolution Notes
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/design/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Vision — Behaviors: The Player Experience
- ## CHAIN
- ## BEHAVIORS
- ## What the Player Does
- ## The Arc of a Playthrough
- ## Observable Behaviors by View
- ## Key Experience Moments
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## Core Drives (Archived Summary)
- ## ANTI-BEHAVIORS
- ## Grounding (Summary)
- ## Engagement Levers (Archived Summary)
- ## Metrics (Archived Summary)
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
- `docs/design/archive/SYNC_archive_2024-12.md`
- `docs/design/opening/ALGORITHM_Opening.md`
- `docs/design/opening/BEHAVIORS_Opening.md`
- `docs/design/opening/CLAUDE.md`
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
- ## SCHEMA
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
- `docs/design/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Vision — Patterns: Why This Design
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS
- ## The Core Insight
- ## The One-Sentence Pitch
- ## The Player Fantasy
- ## Reference Points
- ## Market Validation (Archived Summary)
- ## Design Principles
- ## The Technical Bet
- ## The Central Risk
- ## What Success Looks Like
- ## Answered Questions
- ## Open Questions

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Vision — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## What's Been Established
- ## Answered Questions
- ## Clarified Success Metric
- ## Remaining Open Questions
- ## Decisions Needed
- ## Next Steps
- ## Handoff Notes
- ## Agent Observations
- ## ARCHIVE

**Doc refs:**
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Archived: SYNC_Vision.md
- ## RECENT CHANGES
- ## Agent Observations

**Doc refs:**
- `docs/design/opening/CONTENT.md`

**Sections:**
- # Vision — Tests / Validation Signals
- ## CHAIN
- ## Experience Metrics
- ## Build Verification
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`

**Sections:**
- # Vision — Validation: How We Know It's Working
- ## CHAIN
- ## The Core Question
- ## Validation by Layer
- ## Proof of Concept Milestones
- ## Red Flags to Watch
- ## The Ultimate Test
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

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

**Sections:**
- # Engine Test Suite — Implementation: File Layout
- ## CHAIN
- ## DIRECTORY STRUCTURE
- ## FILE RESPONSIBILITIES
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
- `MomentDisplay.tsx`
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/components/moment/MomentDebugPanel.tsx`
- `frontend/components/scene/CenterStage.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/hooks/useMoments.ts`
- `frontend/lib/api.ts`
- `frontend/types/game.ts`

**Doc refs:**
- `docs/frontend/ALGORITHM_Frontend_Data_Flow.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`

**Sections:**
- # Frontend — Implementation: Runtime and Configuration
- ## CHAIN
- ## ENTRY POINTS
- ## CODE STRUCTURE
- ## MODULE DEPENDENCIES (INTERNAL)
- ## EXTERNAL DEPENDENCIES
- ## DATA FLOW (SUMMARY)
- ## STATE MANAGEMENT
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Archived: SYNC_Frontend.md (Condensed)
- ## MATURITY
- ## RECENT CHANGES (ARCHIVED SUMMARY)
- ## NOTES

**Code refs:**
- `frontend/components/map/MapClient.ts`

**Sections:**
- # Map View — Patterns: Parchment Map With Fog Of War
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## SCOPE
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `world/map/SYNC_Map.md`

**Sections:**
- # Map View — Sync Redirect
- ## CHAIN
- ## Updates

**Code refs:**
- `frontend/components/minimap/Minimap.ts`

**Sections:**
- # Minimap — Patterns: Discovered Location Snapshot
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## SCOPE
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
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
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## AGENT OBSERVATIONS
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

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
- ## SCOPE
- ## INSPIRATIONS
- ## PRINCIPLES
- ## DEPENDENCIES
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/components/panel/RightPanel.ts`
- `frontend/components/panel/RightPanel.tsx`

**Doc refs:**
- `docs/frontend/SYNC_Frontend.md`

**Sections:**
- # Right Panel — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## AGENT OBSERVATIONS

**Code refs:**
- `frontend/app/scenarios/page.ts`

**Sections:**
- # Scenario Selection - Patterns: Curated Starting Point Picker
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## SCOPE
- ## INSPIRATIONS
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
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
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## Agent Observations

**Code refs:**
- `frontend/lib/api.ts`

**Sections:**
- # Scene View — Algorithm
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: RenderSceneView
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Scene View — Behaviors
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/components/scene/CenterStage.tsx`
- `frontend/components/scene/SceneBanner.tsx`
- `frontend/components/scene/SceneView.ts`
- `frontend/hooks/useMoments.ts`

**Doc refs:**
- `data/init/BLOOD_LEDGER_DESIGN_DOCUMENT.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Vision.md`

**Sections:**
- # Scene View — Patterns: Design Philosophy
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## Purpose
- ## The Core Question
- ## PRINCIPLES
- ## SCOPE
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## What We Don't Know Yet
- ## GAPS / IDEAS / QUESTIONS
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
- `frontend/hooks/useMoments.ts`
- `frontend/types/game.ts`

**Doc refs:**
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/scene/PATTERNS_Scene.md`
- `docs/physics/API_Physics.md`

**Sections:**
- # Scene View — Sync: Current State
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## TODO
- ## DESIGN QUESTIONS (from PATTERNS)
- ## INTEGRATION
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## POINTERS
- ## Agent Observations
- ## CONSCIOUSNESS TRACE
- ## ARCHIVE

**Code refs:**
- `SceneView.tsx`
- `frontend/components/moment/index.ts`
- `frontend/components/scene/SceneView.tsx`

**Doc refs:**
- `docs/frontend/scene/ALGORITHM_Scene.md`
- `docs/frontend/scene/BEHAVIORS_Scene.md`
- `docs/frontend/scene/PATTERNS_Scene.md`
- `docs/frontend/scene/SYNC_Scene.md`
- `docs/frontend/scene/TEST_Scene.md`
- `docs/frontend/scene/VALIDATION_Scene.md`

**Sections:**
- # Archived: SYNC_Scene.md
- ## MATURITY
- ## RECENT CHANGES
- ## RECENT CHANGES

**Code refs:**
- `CenterStage.tsx`
- `SceneActions.tsx`
- `SceneBanner.tsx`
- `SceneView.tsx`

**Sections:**
- # Scene View — Tests
- ## CHAIN
- ## PLANNED SUITES
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # No automated tests are wired yet for the scene module.
- # Expected commands once suites exist:
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Scene View — Validation
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/api/moments.py`
- `frontend/components/scene/CenterStage.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/lib/api.ts`

**Sections:**
- # Frontend Data Flow — Algorithm
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: ProcessFrontendDataFlow
- ## KEY DECISIONS
- ## DATA FLOW
- ## Moment Updates: Current vs Desired
- ## SSE Event Types
- ## Implementation Checklist
- ## Migration Path
- ## Files
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/page.ts`

**Sections:**
- # Frontend — Behaviors: State Management and User Interaction
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES (SUMMARY)
- ## ANTI-BEHAVIORS (SUMMARY)
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/hooks/useGameState.ts`

**Sections:**
- # Frontend — Implementation: Code Architecture (Overview)
- ## CHAIN
- ## SUMMARY
- ## CONTENTS
- ## LOGIC CHAINS
- ## CONCURRENCY MODEL

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
- ## SCOPE
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `api.ts`
- `frontend/app/map/page.tsx`
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/hooks/useMoments.ts`
- `frontend/lib/api.ts`
- `frontend/types/game.ts`
- `useGameState.ts`

**Doc refs:**
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/archive/SYNC_archive_2024-12.md`
- `docs/frontend/scenarios/SYNC_Scenario_Selection.md`
- `docs/physics/API_Physics.md`

**Sections:**
- # Frontend — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## MATURITY
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## CONSCIOUSNESS TRACE
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## Agent Observations
- ## GAPS
- ## ARCHIVE
- ## ARCHIVE

**Doc refs:**
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/SYNC_Frontend_archive_2025-12.md`
- `docs/frontend/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Frontend — Sync Archive: 2025-12
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- # Archived: SYNC_Frontend.md
- ## RECENT CHANGES

**Sections:**
- # Frontend — Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## PLANNED COVERAGE
- ## RUNNING TESTS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `frontend/hooks/useGameState.ts`

**Sections:**
- # Frontend — Validation: Invariants and Verification
- ## CHAIN
- ## INVARIANTS
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Async Architecture - Algorithm: Discussion Trees
- ## CHAIN
- ## Principle
- ## Lifecycle Summary
- ## Detailed Reference

**Sections:**
- # Async Architecture - Algorithm: Graph SSE
- ## CHAIN
- ## Graph SSE
- # Write to graph
- # Emit SSE
- # Update graph
- # Emit SSE

**Code refs:**
- `engine/scripts/check_injection.py`

**Sections:**
- # Async Architecture - Algorithm: Hook Injection
- ## CHAIN
- ## Principle
- ## Injection File
- ## Writers
- ## Hook Script
- # Take first injection
- # Rewrite file with remaining injections
- # Return to Claude Code
- # No injection
- ## Narrator Receives
- # In Narrator's context
- # Insert dialogue, then continue
- # Generate stop scene at current position
- ## Injection Types
- ## When Character Activation Triggers Hook
- ## Key Clarifications

**Sections:**
- # Async Architecture - Algorithm: Image Generation
- ## CHAIN
- ## Image Generation
- # Generate image (async)
- # Save to disk
- # Update graph
- # SSE broadcast happens automatically from graph
- # Broadcast place_created (no image yet)
- # Queue image generation

**Sections:**
- # Async Architecture - Algorithm Overview
- ## CHAIN
- ## Parts

**Sections:**
- # Async Architecture - Algorithm: Runner Protocol
- ## CHAIN
- ## Runner Protocol
- # May need to re-spawn Runner for remaining journey

**Sections:**
- # Async Architecture - Algorithm: Waypoints and Fog
- ## CHAIN
- ## Waypoint Creation
- # Write to graph (triggers SSE + image generation)
- ## Fog of War
- # Update position
- # Reveal place
- # SSE broadcast handled by graph

**Sections:**
- # Async Architecture - Archive (2024-12)
- ## Discussion Trees (Archived Detail)
- # Delete the explored branch
- # Save updated tree
- # Check if regeneration needed
- ## Data Flow Diagram (Archived Detail)

**Doc refs:**
- `docs/infrastructure/async/ALGORITHM/ALGORITHM_Overview.md`

**Sections:**
- # Async Architecture - Algorithm
- ## CHAIN
- ## Index
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: Coordinate_Async_Travel
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Travel Experience — Behaviors
- ## CHAIN
- ## BEHAVIORS
- ## What the Player Sees
- ## Player Input During Travel
- ## Duration
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## Success Metrics
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/api/app.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/scripts/check_injection.py`
- `engine/scripts/inject_to_narrator.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `agents/world_runner/CLAUDE.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`

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

**Doc refs:**
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Async Architecture — Design Patterns
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS
- ## Core Principle
- ## The Architecture in One Sentence
- ## Component Responsibilities
- ## Data Flow Diagram
- ## Key Design Decisions
- ## File Paths
- ## What Goes Where
- ## Clarifications
- ## Related Documents

**Code refs:**
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
- `docs/infrastructure/async/ALGORITHM_Async_Architecture.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/async/SYNC_Async_Architecture.md`
- `docs/infrastructure/async/SYNC_Async_Architecture_archive_2025-12.md`
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Async Architecture — State & Implementation Plan
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## Overview
- ## Maturity
- ## CHAIN
- ## CURRENT STATE
- ## IN PROGRESS
- ## Current State vs Target State
- ## Key Decisions Made
- ## Open Questions
- ## Next Action
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## CONSCIOUSNESS TRACE
- ## Known Issues
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## CONFLICTS
- ## ARCHIVE
- ## Agent Observations
- ## ARCHIVE

**Code refs:**
- `engine/scripts/check_injection.py`
- `engine/scripts/inject_to_narrator.py`

**Doc refs:**
- `docs/infrastructure/async/ALGORITHM_Async_Architecture.md`
- `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`
- `docs/infrastructure/async/PATTERNS_Async_Architecture.md`
- `docs/infrastructure/async/SYNC_Async_Architecture.md`
- `docs/infrastructure/async/TEST_Async_Architecture.md`
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Archived: SYNC_Async_Architecture.md
- ## RECENT CHANGES
- ## TODO
- ## POINTERS

**Code refs:**
- `tests/async/test_hook_injection.py`
- `tests/async/test_runner_protocol.py`
- `tests/async/test_sse_queue.py`

**Sections:**
- # Async Architecture — Tests
- ## CHAIN
- ## Planned Coverage
- ## Test Strategy
- ## Unit Tests
- ## Integration Tests
- ## Edge Cases
- ## Test Coverage
- ## How To Run
- ## Manual Verification
- ## Known Test Gaps
- ## Flaky Tests
- ## Gaps
- ## Gaps / Ideas / Questions

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
- `engine/infrastructure/canon/canon_holder.py`
- `engine/infrastructure/canon/speaker.py`

**Sections:**
- # Canon Holder — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL

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
- `engine/infrastructure/canon/canon_holder.py`
- `speaker.py`

**Doc refs:**
- `docs/infrastructure/canon/PATTERNS_Canon.md`

**Sections:**
- # Canon Holder — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## POINTERS
- ## CHAIN

**Code refs:**
- `engine/infrastructure/canon/canon_holder.py`

**Sections:**
- # Canon Holder — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: history_continuity
- ## HOW TO RUN
- # Run canon unit and integration checks
- ## KNOWN GAPS

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
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`
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
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

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
- # Embeddings — Algorithm: Indexing
- ## CHAIN
- ## ALGORITHM: index_node()
- ## ALGORITHM: index_link()
- ## ALGORITHM: index_world()
- ## ALGORITHM: on_scene_end()
- ## KEY DECISIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`

**Sections:**
- # Embeddings — Algorithm Overview
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## DOCUMENT SPLIT

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Algorithm: Search
- ## CHAIN
- ## ALGORITHM: search()
- ## KEY DECISIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Test Cases
- ## CHAIN
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## KNOWN TEST GAPS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`

**Sections:**
- # Embeddings — Test Overview
- ## CHAIN
- ## TEST STRATEGY
- ## CORE UNIT TESTS (Planned)
- ## INTEGRATION TESTS (Planned)
- ## HOW TO RUN
- ## ARCHIVED DETAILS

**Sections:**
- # Embeddings — Archive (2024-12)
- ## ALGORITHM: STORAGE AND QUERY DETAILS (ARCHIVED)
- ## BEHAVIORS: QUERY EXAMPLES (ARCHIVED)
- # Expected matches include character, link, and conversation sources.
- # Expected matches include link and narrative sources.
- # Expected matches include place sources.
- ## PATTERNS: SCALE ESTIMATES (ARCHIVED)
- ## TESTS: FIXTURES AND PERFORMANCE EXAMPLES (ARCHIVED)

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Algorithm (Entry Point)
- ## CHAIN
- ## ENTRY
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: Embeddings Documentation Entry
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
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
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`
- `service.py`

**Sections:**
- # Embeddings — Implementation: Embedding Service Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # Embeddings — Patterns: Per-Field String Embedding
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # Embeddings — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## ARCHIVE
- ## Agent Observations
- ## ARCHIVE

**Code refs:**
- `engine/infrastructure/embeddings/__init__.py`
- `engine/infrastructure/embeddings/service.py`

**Doc refs:**
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Indexing.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Overview.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Search.md`
- `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md`
- `docs/infrastructure/embeddings/PATTERNS_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings_archive_2025-12.md`
- `docs/infrastructure/embeddings/TEST/TEST_Cases.md`
- `docs/infrastructure/embeddings/TEST/TEST_Overview.md`
- `docs/infrastructure/embeddings/TEST_Embeddings.md`
- `docs/infrastructure/embeddings/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Archived: SYNC_Embeddings.md
- ## MATURITY
- ## RECENT CHANGES
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## IMPLEMENTATION PLAN
- # Archived: SYNC_Embeddings.md
- ## RECENT CHANGES

**Code refs:**
- `engine/infrastructure/embeddings/service.py`

**Sections:**
- # Embeddings — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: vector_validity
- ## HOW TO RUN
- # Run embeddings unit tests
- ## KNOWN GAPS

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
- # History — Algorithm Overview
- ## CHAIN
- ## OVERVIEW
- ## WHERE TO LOOK NEXT
- ## ARCHIVED DETAIL

**Sections:**
- # History — Algorithm: Propagation and Beliefs
- ## CHAIN
- ## PROPAGATION OVERVIEW
- ## CONFIDENCE GUIDELINES
- ## DATA FLOW
- ## ARCHIVED DETAIL

**Sections:**
- # History — Algorithm: Query and Record
- ## CHAIN
- ## DATA STRUCTURES
- # Conversations with {Character}
- ## Day 4, Night — The Camp
- ## ALGORITHM: query_history()
- ## ALGORITHM: record_player_history()
- ## ALGORITHM: record_world_history()
- ## KEY DECISIONS

**Sections:**
- # History — Test Cases
- ## CHAIN
- ## UNIT TESTS
- ## INTEGRATION TESTS (SUMMARY)
- ## TEST COVERAGE
- ## KNOWN TEST GAPS

**Sections:**
- # History — Test Overview
- ## CHAIN
- ## TEST STRATEGY
- ## HOW TO RUN
- ## ARCHIVED DETAIL

**Code refs:**
- `engine/infrastructure/history/conversations.py`

**Doc refs:**
- `docs/infrastructure/history/SYNC_History.md`

**Sections:**
- # Archived: SYNC_History.md
- ## MATURITY
- ## RECENT CHANGES
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- # Archived: SYNC_History.md
- ## RECENT CHANGES
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Sections:**
- # History — Archive (2024-12)
- ## ARCHIVED ALGORITHM DETAILS (CONDENSED)
- ## ARCHIVED TEST DETAILS (CONDENSED)
- ## NOTE

**Sections:**
- # History — Algorithm (Entry Point)
- ## CHAIN
- ## ENTRY
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: History Documentation Entry
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
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
- `engine/infrastructure/history/__init__.py`
- `engine/infrastructure/history/conversations.py`
- `engine/infrastructure/history/service.py`

**Doc refs:**
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`
- `engine/infrastructure/history/README.md`

**Sections:**
- # History — Implementation: Service and Conversation Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## ENTRY POINTS
- ## DATA FLOW
- ## SCHEMA
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # History — Patterns: Distributed Memory Through Narratives
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/history/conversations.py`

**Doc refs:**
- `archive/SYNC_History_archive_2025-12.md`
- `archive/SYNC_archive_2024-12.md`
- `docs/infrastructure/history/ALGORITHM_History.md`
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`
- `docs/infrastructure/history/PATTERNS_History.md`
- `docs/infrastructure/history/SYNC_History.md`
- `docs/infrastructure/history/archive/SYNC_History_archive_2025-12.md`

**Sections:**
- # History — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## CONFLICTS
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## CHAIN
- ## Agent Observations
- ## CONSCIOUSNESS TRACE
- ## ARCHIVE

**Sections:**
- # History — Tests (Entry Point)
- ## CHAIN

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
- `engine/scripts/check_injection.py`
- `engine/scripts/generate_images_for_existing.py`
- `engine/scripts/inject_to_narrator.py`
- `engine/scripts/seed_moment_sample.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # Ops Scripts — Implementation: Engine Scripts Layout
- ## CHAIN
- ## FILES
- ## ENTRY POINTS
- ## DEPENDENCIES

**Code refs:**
- `engine/scripts/seed_moment_sample.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

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

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # Ops Scripts — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## Review Observations

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
- # Storm Loader — Behaviors: Mutation Application
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storm Loader - Implementation: Code Architecture and Structure
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
- # Storm Loader — Mechanisms: Application Pipeline
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Load and Apply
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storm Loader — Patterns: Declarative Diff Application
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md`

**Sections:**
- # Storm Loader — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/infrastructure/test_storm_loader.py`

**Sections:**
- # Storm Loader - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storm Loader — Validation: Loader Guarantees
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storms — Behaviors: Overlay Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storms - Implementation: Code Architecture and Structure
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
- # Storms — Mechanisms: Crisis Injection
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Apply Storm
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storms — Patterns: Crisis Overlays
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md`

**Sections:**
- # Storms — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/infrastructure/test_storms.py`

**Sections:**
- # Storms - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Storms — Validation: Overlay Integrity
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

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
- `engine/infrastructure/tempo/tempo_controller.py`

**Sections:**
- # Tempo Controller — Behaviors: Speed-Driven Surfacing
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/tempo/__init__.py`
- `engine/infrastructure/tempo/tempo_controller.py`

**Doc refs:**
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

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
- `engine/infrastructure/tempo/tempo_controller.py`
- `frontend/components/SpeedControl.tsx`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # Tempo Controller — Patterns: Speed-As-State-Machine
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
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
- ## Recent Changes
- ## Chain
- ## Agent Observations

**Code refs:**
- `engine/tests/test_tempo.py`

**Sections:**
- # Tempo Controller — Test: Coverage Plan
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # No automated tests yet for tempo.
- # Planned:
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/infrastructure/tempo/tempo_controller.py`

**Sections:**
- # Tempo Controller — Validation: Pacing Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # No automated tests yet for tempo.
- # Planned: pytest engine/tests/test_tempo.py
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Builder — Algorithm Details
- ## CHAIN
- ## Sparsity Result Shape
- ## Enrichment Output Shape (Summary)
- ## Linking Rules
- ## Archive Note

**Sections:**
- # World Builder — Algorithm Overview
- ## CHAIN
- ## Overview
- ## Core Flow
- ## Query Moment Rules
- ## Sparsity Decision (Thresholds)
- ## Enrichment Application
- ## Caching / Guardrails
- ## Archive Note

**Code refs:**
- `enrichment.py`
- `query.py`
- `query_moment.py`
- `sparsity.py`
- `world_builder.py`

**Sections:**
- # World Builder — Implementation Flow
- ## CHAIN
- ## Query Flow (Module Boundaries)
- ## Enrichment Application Notes
- ## Error Handling Summary
- ## Archive Note

**Code refs:**
- `__init__.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/world/map/semantic.py`
- `enrichment.py`
- `query.py`
- `query_moment.py`
- `sparsity.py`
- `world_builder.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # World Builder — Implementation Overview
- ## CHAIN
- ## Code Structure
- ## Dependencies
- ## Configuration (Key Settings)
- ## Archive Note

**Code refs:**
- `tests/infrastructure/world_builder/test_world_builder.py`

**Sections:**
- # World Builder — Test Cases (Summary)
- ## CHAIN
- ## Representative Cases
- ## Notes

**Code refs:**
- `tests/infrastructure/world_builder/test_world_builder.py`

**Sections:**
- # World Builder — Test Overview
- ## CHAIN
- ## Test Strategy
- ## Suites (High-Level)
- ## How To Run
- ## Known Gaps
- ## Archive Note

**Sections:**
- # World Builder — Validation Checks
- ## CHAIN
- ## Manual Checklist
- ## Automated Verification
- ## Archive Note

**Sections:**
- # World Builder — Validation Overview
- ## CHAIN
- ## Invariants
- ## Properties
- ## Error Conditions
- ## Archive Note

**Sections:**
- # World Builder — Archive Summary (2024-12)
- ## Archived Sections (Condensed)
- ## Notes

**Sections:**
- # World Builder — Algorithm (Split)
- ## CHAIN
- ## Entry Point

**Code refs:**
- `engine/infrastructure/world_builder/query.py`

**Sections:**
- # World Builder — Behaviors: Query Moments, Sparse Enrichment, and Cache Guards
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Builder — Implementation (Split)
- ## CHAIN
- ## Entry Point

**Code refs:**
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/world_builder/query.py`
- `engine/world/map/semantic.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # World Builder — Patterns: Query Moments and Sparse Enrichment
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `__init__.py`
- `enrichment.py`
- `query.py`
- `query_moment.py`
- `sparsity.py`
- `world_builder.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`

**Sections:**
- # World Builder — SYNC
- ## Current State
- ## Documentation Updates
- ## Configuration
- ## Next Steps
- ## Known Issues
- ## Handoff Notes
- ## Chain
- ## Agent Observations
- ## ARCHIVE

**Code refs:**
- `__init__.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/world_builder/world_builder.py`
- `engine/world/map/semantic.py`
- `tests/infrastructure/world_builder/__init__.py`
- `tests/infrastructure/world_builder/test_world_builder.py`

**Sections:**
- # Archived: SYNC_World_Builder.md
- ## Recent Changes
- ## Integration Points
- ## Usage Example
- # Async with enrichment (creates content if sparse)
- # Sync without enrichment (just search + record)

**Sections:**
- # World Builder — Test (Split)
- ## CHAIN
- ## Entry Point

**Sections:**
- # World Builder — Validation (Split)
- ## CHAIN
- ## Entry Point

**Sections:**
- # BEHAVIORS: Bleed Reports
- ## Observable Effects
- ## Bleed Reports — Your Character's Legacy
- ## Why This Is Retention Gold
- ## The Whale Hook: Digital Immortality
- ## Steam Page Copy / Marketing Language
- ## Maturity
- ## CHAIN

**Sections:**
- # Bleed-Through — Behaviors: Ghosts, Rumors, Reports
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Bleed-Through - Implementation: Code Architecture and Structure
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
- # Bleed-Through — Mechanisms: Ghosts, Rumors, Reports
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Ghost Injection
- ## MECHANISM: Rumor Bleed
- ## MECHANISM: Bleed Reports
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # PATTERNS: Scars Cross Worlds
- ## Why This Design Exists
- ## Core Insight: AI as Actor, Not Author
- ## Strategic Position and Rationale
- ## Public Features of Bleed-Through
- ## Marketing and Vocabulary
- ## Maturity
- ## CHAIN

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md`
- `docs/network/transposition/ALGORITHM_Transposition_Pipeline.md`

**Sections:**
- # SYNC: Bleed-Through System
- ## Maturity
- ## Current State
- ## Recent Changes
- ## Handoffs
- ## Agent's Analysis (Gemini, 2025-12-19)
- ## CHAIN

**Code refs:**
- `tests/network/test_bleed_through.py`

**Sections:**
- # Bleed-Through - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Bleed-Through — Validation: Canon Safety and Messaging
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ghost Dialogue — Behaviors: Replay of Lived Lines
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ghost Dialogue - Implementation: Code Architecture and Structure
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
- # Ghost Dialogue — Mechanisms: Dialogue Index and Retrieval
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Indexing
- ## MECHANISM: Retrieval
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ghost Dialogue — Patterns: Real Lines Beat Prompts
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md`

**Sections:**
- # Ghost Dialogue — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/network/test_ghost_dialogue.py`

**Sections:**
- # Ghost Dialogue - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ghost Dialogue — Validation: Quality and Safety
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Shadow Feed — Behaviors: Rumor Imports and Fog of War
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Shadow Feed - Implementation: Code Architecture and Structure
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
- # Shadow Feed — Mechanisms: Safe Import Filtering
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Import Filter
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Shadow Feed — Patterns: Rumor Cache for Distant Events
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md`

**Sections:**
- # Shadow Feed — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/network/test_shadow_feed.py`

**Sections:**
- # Shadow Feed - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Shadow Feed — Validation: Causality and Canon Locks
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # ALGORITHM: Transposition Pipeline
- ## Procedures
- ## 2. The Transposition Pipeline: An Overview
- ## 3. Algorithm: Conflict Detection
- ## 4. Algorithm: Conflict Resolution Strategies
- ## Maturity
- ## CHAIN

**Sections:**
- # Transposition — Behaviors: Conflict Resolution Cascade
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Transposition - Implementation: Code Architecture and Structure
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
- # Transposition — Mechanisms: Conflict Detection & Resolution
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Conflict Detection
- ## MECHANISM: Conflict Resolution Cascade
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # PATTERNS: Local Canon Primary
- ## Why This Design Exists
- ## Core Principle: The Primacy of Local Canon
- ## The Bleed-Through Mandate
- ## Foundational Terms
- ## Maturity
- ## CHAIN

**Doc refs:**
- `data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md`

**Sections:**
- # Transposition — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md`

**Sections:**
- # SYNC: Transposition Logic
- ## Maturity
- ## Current State
- ## Recent Changes
- ## Handoffs
- ## Agent's Analysis (Gemini, 2025-12-19)
- ## CHAIN

**Code refs:**
- `tests/network/test_transposition.py`

**Sections:**
- # Transposition - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # VALIDATION: Transposition Invariants
- ## Invariants
- ## 5. Algorithm: Safety Locks on Ground Truth
- ## Overall Purpose
- ## Maturity
- ## CHAIN

**Sections:**
- # Voyager System — Behaviors: Importing Trauma Without Breaking Canon
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Voyager System - Implementation: Code Architecture and Structure
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
- # Voyager System — Mechanisms: Export/Import Transposition
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Export Capsule
- ## MECHANISM: Import Capsule
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Voyager System — Patterns: Trauma Without Memory
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Character Import.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md`

**Sections:**
- # Voyager System — Sync: Current State
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
- `tests/network/test_voyager_system.py`

**Sections:**
- # Voyager System - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Voyager System — Validation: Canon-Safe Imports
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- # Placeholder tests (not implemented yet)
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Scavenger — Behaviors: Priority Stack Reuse
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Scavenger - Implementation: Code Architecture and Structure
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
- # World Scavenger — Mechanisms: Cache and Ghost Reuse
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Priority Stack
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Scavenger — Patterns: Scavenge Before Generate
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md`

**Sections:**
- # World Scavenger — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/network/test_world_scavenger.py`

**Sections:**
- # World Scavenger - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # World Scavenger — Validation: Reuse Safety Locks
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Billing — Behaviors: Metered Experience
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Billing - Implementation: Code Architecture and Structure
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
- `tick.py`

**Sections:**
- # IMPLEMENTATION: Billing Technical Stack
- ## Code Architecture
- ## Stack
- ## Components
- ## Maturity
- ## CHAIN

**Sections:**
- # Billing — Mechanisms: Metered Stripe Flow
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Usage Tracking
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # PATTERNS: Pay To Preserve History
- ## Why This Design Exists
- ## Executive Summary
- ## Why This Model Fits Blood Ledger
- ## Maturity
- ## CHAIN

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md`

**Sections:**
- # Billing — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md`

**Sections:**
- # SYNC: Billing System
- ## Maturity
- ## Current State
- ## Recent Changes
- ## Handoffs
- ## Agent's Analysis (Gemini, 2025-12-19)
- ## CHAIN

**Code refs:**
- `tests/product/test_billing.py`

**Sections:**
- # Billing - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Billing — Validation: Metered Integrity
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `tick.py`

**Sections:**
- # ALGORITHM: Hallucination Defense
- ## Procedures
- ## The Problem with AI Narrative
- ## Our Architecture: Generation vs Canonization
- ## Algorithm Steps
- ## The Cost and Value
- ## The AI as Actor Model
- ## Maturity
- ## CHAIN

**Sections:**
- # ALGORITHM: Semantic Cache
- ## Procedures
- ## The Problem
- ## The Solution
- ## Algorithm Steps
- # BEFORE: Temporal cache (60 seconds)
- # AFTER: Semantic cache
- # 1. Extract the THEME of the request
- # 2. Query the graph for EVERYTHING related
- # 3. If content exists, respect it
- # 4. If new, generate AND tag for future
- ## Metadata Tagging
- ## Result
- ## Maturity
- ## CHAIN

**Sections:**
- # ALGORITHM: World Scavenger
- ## Procedures
- ## Paradigm Shift: Scavenge Before Generate
- ## The Scavenger Priority Stack
- ## Three Scavenging Systems
- ## Inverse Cost Curve
- ## Advantages of Scavenging
- ## Maturity
- ## CHAIN

**Sections:**
- # BEHAVIORS: Business Model Behaviors (Retention, Conversion, Unit Economics)
- ## Observable Effects
- ## Retention Mechanisms
- ## Churn Prevention Triggers
- ## Conversion Funnel and Ledger Lock
- ## Unit Economics Signals
- ## Maturity
- ## CHAIN

**Sections:**
- # Business Model - Implementation: Code Architecture and Structure
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
- # Business Model — Mechanisms: Margin Defense
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Margin Calculation
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # PATTERNS: Market Comparison
- ## Why This Design Exists
- ## Not a Game, a Service
- ## Strategic Market Comparisons
- ## Whale Economics (Canonical)
- ## Lifetime Value (LTV) Comparison
- ## Blue Ocean Market Position
- ## Maturity
- ## CHAIN

**Code refs:**
- `tick.py`

**Sections:**
- # PATTERNS: Whale Economics
- ## Why This Design Exists
- ## The Core Insight: Simulation Is Free
- ## Cost Per Moment Type
- ## The "Grandmother Query" Economics
- ## The "Nothing Happening" Subsidy
- ## Margin Defense Table
- ## Worst-Case Stress Test
- ## Maturity
- ## CHAIN

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md`

**Sections:**
- # SYNC: Business Model
- ## Maturity
- ## Current State
- ## Recent Changes
- ## Handoffs
- ## Agent's Analysis (Gemini, 2025-12-19)
- ## CHAIN

**Sections:**
- # Business Model — Validation: Margin Viability
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # BEHAVIORS: Chronicle Types and Structure
- ## Observable Effects
- ## Chronicle Types
- ## Behavior Contracts
- ## Inputs / Outputs
- ## Sharing & Distribution Behaviors
- ## Maturity
- ## CHAIN
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # IMPLEMENTATION: Chronicle System
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW
- ## TECHNICAL PIPELINE (DESIGN)
- ## COLD_OPEN
- ## THE_WEIGHT
- ## THE_MOMENT
- ## THE_SHADOW
- ## END_CARD
- # Voice mapping
- # ... character-specific voices
- # Cold open
- # The Weight — Ledger pages
- # ... continue for each section
- # Render
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # IMPLEMENTATION: Chronicle Technical Pipeline (Pointer)
- ## CHAIN

**Sections:**
- # Chronicle System — Mechanisms: Generation Pipeline
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Generate Chronicle
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/network/transposition/ALGORITHM_Transposition_Pipeline.md`
- `docs/product/billing/PATTERNS_Pay_To_Preserve_History.md`

**Sections:**
- # PATTERNS: Chronicle Flywheel
- ## Why This Design Exists
- ## The Flywheel Concept
- ## Key Design Decisions & Rationale
- ## Go-To-Market Integration
- ## What's In Scope
- ## What's Out of Scope (and Where it Lives Instead)
- ## Maturity
- ## CHAIN

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Chronicle System.md`

**Sections:**
- # SYNC: Chronicle System
- ## Maturity
- ## Current State
- ## Recent Changes
- ## Handoffs
- ## Agent's Analysis (Gemini, 2025-12-19)
- ## CHAIN

**Code refs:**
- `tests/product/test_chronicle_system.py`

**Sections:**
- # Chronicle System - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Chronicle System — Validation: Output Quality
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## METRICS AND SUCCESS CRITERIA
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # GTM Strategy — Behaviors: Acquisition Flywheel
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # GTM Strategy - Implementation: Code Architecture and Structure
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
- # GTM Strategy — Mechanisms: Programs and Channels
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Chronicle Flywheel
- ## MECHANISM: Weekly Storm Program
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # GTM Strategy — Patterns: Direct Whale Acquisition
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/Blood Ledger — Go-To-Market Strategy.md`

**Sections:**
- # GTM Strategy — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/product/test_gtm_strategy.py`

**Sections:**
- # GTM Strategy - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # GTM Strategy — Validation: Program Health
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ledger Lock — Behaviors: Conversion Trigger
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ledger Lock - Implementation: Code Architecture and Structure
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
- # Ledger Lock — Mechanisms: Trigger and Payment Flow
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## MECHANISM: Trigger
- ## MECHANISM: Payment Flow
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ledger Lock — Patterns: Crisis of Memory
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md`

**Sections:**
- # Ledger Lock — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `tests/product/test_ledger_lock.py`

**Sections:**
- # Ledger Lock - Test: Test Cases and Coverage
- ## CHAIN
- ## TEST STRATEGY
- ## UNIT TESTS
- ## INTEGRATION TESTS
- ## EDGE CASES
- ## TEST COVERAGE
- ## HOW TO RUN
- # Run all tests for this module
- ## KNOWN TEST GAPS
- ## FLAKY TESTS
- ## GAPS / IDEAS / QUESTIONS

**Sections:**
- # Ledger Lock — Validation: Conversion Integrity
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## TEST COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Doc refs:**
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA_Moments.md`

**Sections:**
- # Schema Archive Notes (2024-12)
- ## Summary
- ## Rationale

**Code refs:**
- `engine/world/map/semantic.py`

**Doc refs:**
- `docs/world/map/ALGORITHM_Map.md`

**Sections:**
- # Map System — Algorithm: Places
- ## CHAIN
- ## Canonical Location

**Code refs:**
- `engine/world/map/semantic.py`

**Doc refs:**
- `docs/world/map/ALGORITHM_Map.md`

**Sections:**
- # Map System — Algorithm: Rendering Pipeline
- ## CHAIN
- ## Canonical Location

**Code refs:**
- `engine/world/map/semantic.py`

**Doc refs:**
- `docs/world/map/ALGORITHM_Map.md`

**Sections:**
- # Map System — Algorithm: Routes
- ## CHAIN
- ## Canonical Location

**Code refs:**
- `engine/world/map/semantic.py`

**Doc refs:**
- `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`

**Sections:**
- # Map System — Algorithm: Overview
- ## CHAIN
- ## Purpose
- ## Rendering Summary
- ## Rendering Pipeline
- ## Places
- ## Routes
- ## Inputs and Outputs
- ## Constraints

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Behaviors: Visibility & Interaction
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS
- ## Visibility System
- ## PlayerVisibility Schema
- ## Visibility Update Rules
- ## Route Visibility
- ## Display Rules
- ## Interaction Behaviors
- ## Map Component Props (UI Contract)
- ## Narrator Integration

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Implementation: Semantic Search Code Architecture
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT

**Code refs:**
- `engine/world/map/semantic.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # Map System — Patterns: Why This Design
- ## CHAIN
- ## Core Insight
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## What the Map Is Not
- ## System Boundaries
- ## Summary
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `engine/world/map/semantic.py`
- `frontend/components/map/MapClient.tsx`

**Doc refs:**
- `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM_Map.md`
- `docs/world/map/ALGORITHM_Rendering.md`
- `docs/world/map/PATTERNS_Map.md`
- `docs/world/map/archive/SYNC_archive_2024-12.md`

**Sections:**
- # Map System — Sync: Current State
- ## CHAIN
- ## MATURITY
- ## CURRENT STATE
- ## Documentation Status
- ## RECENT CHANGES
- ## IN PROGRESS
- ## Agent Observations
- ## GAPS
- ## ARCHIVE
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS
- ## ARCHIVE

**Doc refs:**
- `docs/world/map/ALGORITHM/places/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM/routes/ALGORITHM_Routes.md`
- `docs/world/map/ALGORITHM_Map.md`
- `docs/world/map/ALGORITHM_Rendering.md`
- `docs/world/map/BEHAVIORS_Map.md`
- `docs/world/map/PATTERNS_Map.md`
- `docs/world/map/SYNC_Map.md`
- `docs/world/map/TEST_Map_Test_Coverage.md`

**Sections:**
- # Archived: SYNC_Map.md
- ## RECENT CHANGES

**Code refs:**
- `engine/world/map/semantic.py`

**Sections:**
- # Map System — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: search_relevance
- ## KNOWN GAPS

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

**Code refs:**
- `data/scripts/inject_world.py`
- `data/scripts/scrape/phase1_geography.py`
- `data/scripts/scrape/phase2_political.py`
- `data/scripts/scrape/phase3_events.py`
- `data/scripts/scrape/phase4_narratives.py`
- `data/scripts/scrape/phase5_tensions.py`

**Sections:**
- # Scraping Pipeline — Algorithm
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: run_scraping_pipeline
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS
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
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `data/scripts/inject_world.py`
- `data/scripts/scrape/phase1_geography.py`
- `data/scripts/scrape/phase2_political.py`

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # World Scraping — Implementation: Pipeline Architecture and Data Flow
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## CONCURRENCY MODEL

**Code refs:**
- `data/scripts/inject_world.py`
- `data/scripts/scrape/phase1_geography.py`

**Sections:**
- # World Scraping — Design Patterns
- ## CHAIN
- ## Core Principle
- ## The Problem
- ## The Pattern
- ## Principles
- ## Dependencies
- ## Inspirations
- ## Scope
- ## Gaps / Ideas / Questions
- ## Pattern: Authentic England 1067
- ## Behaviors: What The Player Experiences
- ## Target Density
- ## Related Documents

**Code refs:**
- `data/scripts/inject_world.py`

**Doc refs:**
- `docs/world/scraping/ALGORITHM_Pipeline.md`

**Sections:**
- # World Scraping — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## POINTERS
- ## CHAIN

**Code refs:**
- `data/scripts/inject_world.py`

**Doc refs:**
- `docs/world/scraping/ALGORITHM_Pipeline.md`
- `docs/world/scraping/BEHAVIORS_World_Scraping.md`
- `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`
- `docs/world/scraping/PATTERNS_World_Scraping.md`
- `docs/world/scraping/SYNC_World_Scraping.md`
- `docs/world/scraping/TEST_World_Scraping.md`
- `docs/world/scraping/VALIDATION_World_Scraping.md`

**Sections:**
- # Archived: SYNC_World_Scraping.md
- ## Recent Changes
- ## Agent Observations

**Code refs:**
- `data/scripts/scrape/phase1_geography.py`

**Sections:**
- # World Scraping — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## CHECKER INDEX
- ## INDICATOR: route_traversability
- ## HOW TO RUN
- # Run data validation scripts
- ## KNOWN GAPS

**Doc refs:**
- `docs/world/scraping/SYNC_World_Scraping.md`

**Sections:**
- # World Scraping — Validation
- ## CHAIN
- ## How We Know It Works
- ## Invariants
- ## Properties
- ## Error Conditions
- ## Test Coverage
- ## Verification Procedure
- ## Geography Tests
- # Sample routes, compare to Google Maps walking
- ## Political Tests
- ## Narrative Tests
- ## Tension Tests
- ## Density Tests
- ## Playtest Checklist
- ## Sync Status
- ## Gaps / Ideas / Questions

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
- `agent_cli.py`
- `api.ts`
- `api/app.py`
- `api/moments.py`
- `app.py`
- `app/layout.tsx`
- `app/page.tsx`
- `app/scenarios/page.tsx`
- `app/start/page.tsx`
- `base.py`
- `canon/holder.py`
- `canon_holder.py`
- `check_health.py`
- `check_injection.py`
- `companion.py`
- `components/GameClient.tsx`
- `components/GameLayout.tsx`
- `components/SpeedControl.tsx`
- `components/chronicle/ChroniclePanel.tsx`
- `components/debug/DebugPanel.tsx`
- `components/map/MapCanvas.tsx`
- `components/map/MapClient.tsx`
- `components/minimap/Minimap.tsx`
- `components/minimap/SunArc.tsx`
- `components/moment/ClickableText.tsx`
- `components/moment/MomentDebugPanel.tsx`
- `components/moment/MomentDisplay.tsx`
- `components/moment/MomentStream.tsx`
- `components/panel/ChronicleTab.tsx`
- `components/panel/ConversationsTab.tsx`
- `components/panel/LedgerTab.tsx`
- `components/panel/RightPanel.tsx`
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
- `components/ui/Toast.tsx`
- `components/voices/Voices.tsx`
- `conversations.py`
- `data/scripts/inject_world.py`
- `data/scripts/scrape/narrative_rules.py`
- `data/scripts/scrape/osm_utils.py`
- `data/scripts/scrape/phase1_geography.py`
- `data/scripts/scrape/phase2_political.py`
- `data/scripts/scrape/phase3_events.py`
- `data/scripts/scrape/phase4_narratives.py`
- `data/scripts/scrape/phase5_tensions.py`
- `doctor_cli_parser_and_run_checker.py`
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
- `engine/infrastructure/api/moments_sse.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/api/playthroughs_opening.py`
- `engine/infrastructure/api/sse_broadcast.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/api/views.py`
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
- `engine/infrastructure/memory/transcript.py`
- `engine/infrastructure/memory/transcript_store.py`
- `engine/infrastructure/opening/generator.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/narrator_prompt.py`
- `engine/infrastructure/orchestration/opening.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/speed.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/infrastructure/tempo/__init__.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/infrastructure/world_builder/__init__.py`
- `engine/infrastructure/world_builder/enrichment.py`
- `engine/infrastructure/world_builder/query.py`
- `engine/infrastructure/world_builder/query_moment.py`
- `engine/infrastructure/world_builder/sparsity.py`
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
- `engine/tests/test_opening_health.py`
- `engine/tests/test_spec_consistency.py`
- `engine/tests/test_tempo.py`
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
- `frontend/components/scene/SceneView.ts`
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
- `graph_queries_narratives.py`
- `graph_queries_search.py`
- `handlers/__init__.py`
- `handlers/base.py`
- `handlers/companion.py`
- `hooks/transformers.ts`
- `hooks/useGameState.ts`
- `hooks/useMoments.ts`
- `hooks/useTempo.ts`
- `inject_to_narrator.py`
- `inject_world.py`
- `lib/api.ts`
- `lib/api/moments.ts`
- `lib/map/projection.ts`
- `lib/map/random.ts`
- `links.py`
- `lint_terminology.py`
- `moment_graph/queries.py`
- `moment_graph/traversal.py`
- `moment_processor.py`
- `moments.py`
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
- `semantic_proximity_based_character_node_selector.py`
- `service.py`
- `snake_case.py`
- `sparsity.py`
- `speaker.py`
- `sse_broadcast.py`
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
- `tests/infrastructure/test_storm_loader.py`
- `tests/infrastructure/test_storms.py`
- `tests/infrastructure/test_world_builder.py`
- `tests/infrastructure/world_builder/__init__.py`
- `tests/infrastructure/world_builder/test_world_builder.py`
- `tests/network/test_bleed_through.py`
- `tests/network/test_ghost_dialogue.py`
- `tests/network/test_shadow_feed.py`
- `tests/network/test_transposition.py`
- `tests/network/test_voyager_system.py`
- `tests/network/test_world_scavenger.py`
- `tests/product/test_billing.py`
- `tests/product/test_chronicle_system.py`
- `tests/product/test_gtm_strategy.py`
- `tests/product/test_ledger_lock.py`
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
- `useGameState.ts`
- `views.py`
- `world_builder.py`
- `world_runner.py`

**Doc refs:**
- `agents/developer/CLAUDE.md`
- `agents/narrator/CLAUDE.md`
- `agents/narrator/CLAUDE_old.md`
- `agents/world_runner/CLAUDE.md`
- `agents/world_runner/CLAUDE_PROMPT.md`
- `archive/SYNC_History_archive_2025-12.md`
- `archive/SYNC_archive_2024-12.md`
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md`
- `data/Distributed-Content-Generation-Network/Blood Chronicle System.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Character Import.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Go-To-Market Strategy.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md`
- `data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md`
- `data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md`
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
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Drives_And_Metrics.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
- `docs/design/archive/SYNC_archive_2024-12.md`
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
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/VALIDATION_Models.md`
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
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Overview.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md`
- `docs/frontend/PATTERNS_Frontend.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/SYNC_Frontend_archive_2025-12.md`
- `docs/frontend/archive/SYNC_archive_2024-12.md`
- `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`
- `docs/frontend/map/PATTERNS_Parchment_Map_View.md`
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
- `docs/infrastructure/api/PATTERNS_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/api/TEST_Api.md`
- `docs/infrastructure/api/VALIDATION_Api.md`
- `docs/infrastructure/async/ALGORITHM/ALGORITHM_Overview.md`
- `docs/infrastructure/async/ALGORITHM_Async_Architecture.md`
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
- `docs/infrastructure/async/SYNC_Async_Architecture_archive_2025-12.md`
- `docs/infrastructure/async/TEST_Async_Architecture.md`
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`
- `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md`
- `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/canon/SYNC_Canon.md`
- `docs/infrastructure/canon/TEST_Canon.md`
- `docs/infrastructure/canon/VALIDATION_Canon.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Indexing.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Overview.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Search.md`
- `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- `docs/infrastructure/embeddings/BEHAVIORS_Embeddings.md`
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md`
- `docs/infrastructure/embeddings/PATTERNS_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings_archive_2025-12.md`
- `docs/infrastructure/embeddings/TEST/TEST_Cases.md`
- `docs/infrastructure/embeddings/TEST/TEST_Overview.md`
- `docs/infrastructure/embeddings/TEST_Embeddings.md`
- `docs/infrastructure/embeddings/VALIDATION_Embeddings.md`
- `docs/infrastructure/embeddings/archive/SYNC_archive_2024-12.md`
- `docs/infrastructure/history/ALGORITHM_History.md`
- `docs/infrastructure/history/BEHAVIORS_History.md`
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`
- `docs/infrastructure/history/PATTERNS_History.md`
- `docs/infrastructure/history/SYNC_History.md`
- `docs/infrastructure/history/TEST_History.md`
- `docs/infrastructure/history/VALIDATION_History.md`
- `docs/infrastructure/history/archive/SYNC_History_archive_2025-12.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/BEHAVIORS_Tempo.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/infrastructure/tempo/TEST_Tempo.md`
- `docs/infrastructure/tempo/VALIDATION_Tempo.md`
- `docs/network/transposition/ALGORITHM_Transposition_Pipeline.md`
- `docs/network/transposition/PATTERNS_Local_Canon_Primary.md`
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
- `docs/physics/SYNC_Physics_archive_2025-12.md`
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
- `docs/physics/graph/SYNC_Graph_archive_2025-12.md`
- `docs/physics/graph/VALIDATION.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`
- `docs/product/billing/PATTERNS_Pay_To_Preserve_History.md`
- `docs/scenarios/README.md`
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`
- `docs/schema/SCHEMA_Moments.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`
- `docs/schema/VALIDATION_Graph.md`
- `docs/schema/VALIDATION_Living_Graph.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Routes.md`
- `docs/world/map/ALGORITHM/places/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM/routes/ALGORITHM_Routes.md`
- `docs/world/map/ALGORITHM_Map.md`
- `docs/world/map/ALGORITHM_Rendering.md`
- `docs/world/map/BEHAVIORS_Map.md`
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md`
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
- `docs/world/map/TEST_Map_Test_Coverage.md`
- `docs/world/map/archive/SYNC_archive_2024-12.md`
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
- `docs/world/scraping/TEST_World_Scraping.md`
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
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`
- `views/VIEW_Test_Write_Tests_And_Verify.md`
- `world/map/SYNC_Map.md`

**Sections:**
- # Repository Map: the-blood-ledger

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

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

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

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

**Definitions:**
- `async def query()`
- `def query_sync()`
- `def _get_default_semantic_search()`
- `def _create_count_links_fn()`
- `def count_links()`
- `def _build_enrichment_context()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

**Definitions:**
- `def record_query_moment()`
- `def link_results_to_moment()`
- `def _link_to_character()`
- `def _link_to_place()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

**Definitions:**
- `class SparsityResult`
- `def cosine_similarity()`
- `def node_to_text()`
- `def is_sparse()`
- `def _default_embed()`

**Docs:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Overview.md`

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

**Definitions:**
- `def get_embedding()`
- `def get_embedding_batch()`

**Docs:** `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`

**Definitions:**
- `def main()`

**Docs:** `docs/infrastructure/ops-scripts/PATTERNS_Operational_Seeding_And_Backfill_Scripts.md`

**Definitions:**
- `def create_character_prompt()`
- `def create_place_prompt()`
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
- `def test_world_runner_processes_flip_output()`
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
- `def test_moment_creation()`
- `def test_embeddable_text()`
- `def test_should_embed()`
- `def test_extract_moment_args()`
- `def test_moment_processor_id_generation()`
- `def test_moment_processor_time_conversion()`
- `def test_moment_processor_dialogue()`
- `def test_moment_processor_sequence()`
- `def test_moment_processor_narrative_linking()`
- `def run_all_tests()`

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

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

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

**Docs:** `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Definitions:**
- `SpeedControl()`
- `fetchSpeed()`

**Docs:** `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`

**Definitions:**
- `useGameState()`
- `view()`
- `mapPlaceType()`
- `transformScene()`
- `clickables()`
- `placeId()`
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

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

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

**Docs:** `docs/frontend/map/PATTERNS_Parchment_Map_View.md`

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

**Docs:** `docs/infrastructure/world-builder/TEST/TEST_Overview.md`

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

**Definitions:**
- `def load_classification()`
- `def module_name_for_path()`
- `def build_module_index()`
- `def normalize_doc_path()`
- `def parse_doc_impl_links()`
- `def parse_code_docs_links()`
- `def parse_imports()`
- `def build_edges()`
- `def add_edge()`
- `def build_adjacency()`
- `def write_outputs()`
- `def main()`

**Definitions:**
- `def _entries()`
- `def main()`

**Code refs:**
- `doctor_cli_parser_and_run_checker.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
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
- ## NAMING ENGINEERING PRINCIPLES
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 6. Operational Proactivity
- ## 5. Communication Principles

**Doc refs:**
- `data/ARCHITECTURE — Cybernetic Studio.md`

**Sections:**
- # The Blood Ledger
- ## Launch Protocol
- # Or if first time:
- # docker run -d --name falkordb -p 6379:6379 -p 3002:3000 falkordb/falkordb
- ## Moment Graph Sample Data
- ## Service Summary

**Definitions:**
- `def _now_iso()`
- `def read_text()`
- `def write_text()`
- `def safe_glob()`
- `def detect_repo_kind()`
- `def parse_map_tree_paths()`
- `def append_source()`
- `def include_globs()`
- `def build_pack()`
- `def r()`
- `def header()`
- `def main()`

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
- `agent_cli.py`
- `api.ts`
- `api/app.py`
- `api/moments.py`
- `app.py`
- `app/layout.tsx`
- `app/page.tsx`
- `app/scenarios/page.tsx`
- `app/start/page.tsx`
- `base.py`
- `canon/holder.py`
- `canon_holder.py`
- `check_health.py`
- `check_injection.py`
- `companion.py`
- `components/GameClient.tsx`
- `components/GameLayout.tsx`
- `components/SpeedControl.tsx`
- `components/chronicle/ChroniclePanel.tsx`
- `components/debug/DebugPanel.tsx`
- `components/map/MapCanvas.tsx`
- `components/map/MapClient.tsx`
- `components/minimap/Minimap.tsx`
- `components/minimap/SunArc.tsx`
- `components/moment/ClickableText.tsx`
- `components/moment/MomentDebugPanel.tsx`
- `components/moment/MomentDisplay.tsx`
- `components/moment/MomentStream.tsx`
- `components/panel/ChronicleTab.tsx`
- `components/panel/ConversationsTab.tsx`
- `components/panel/LedgerTab.tsx`
- `components/panel/RightPanel.tsx`
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
- `components/ui/Toast.tsx`
- `components/voices/Voices.tsx`
- `conversations.py`
- `data/scripts/inject_world.py`
- `data/scripts/scrape/narrative_rules.py`
- `data/scripts/scrape/osm_utils.py`
- `data/scripts/scrape/phase1_geography.py`
- `data/scripts/scrape/phase2_political.py`
- `data/scripts/scrape/phase3_events.py`
- `data/scripts/scrape/phase4_narratives.py`
- `data/scripts/scrape/phase5_tensions.py`
- `doctor_cli_parser_and_run_checker.py`
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
- `engine/infrastructure/api/moments_sse.py`
- `engine/infrastructure/api/playthroughs.py`
- `engine/infrastructure/api/playthroughs_opening.py`
- `engine/infrastructure/api/sse_broadcast.py`
- `engine/infrastructure/api/tempo.py`
- `engine/infrastructure/api/views.py`
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
- `engine/infrastructure/memory/transcript.py`
- `engine/infrastructure/memory/transcript_store.py`
- `engine/infrastructure/opening/generator.py`
- `engine/infrastructure/orchestration/agent_cli.py`
- `engine/infrastructure/orchestration/narrator.py`
- `engine/infrastructure/orchestration/narrator_prompt.py`
- `engine/infrastructure/orchestration/opening.py`
- `engine/infrastructure/orchestration/orchestrator.py`
- `engine/infrastructure/orchestration/speed.py`
- `engine/infrastructure/orchestration/world_runner.py`
- `engine/infrastructure/tempo/__init__.py`
- `engine/infrastructure/tempo/tempo_controller.py`
- `engine/infrastructure/world_builder/__init__.py`
- `engine/infrastructure/world_builder/enrichment.py`
- `engine/infrastructure/world_builder/query.py`
- `engine/infrastructure/world_builder/query_moment.py`
- `engine/infrastructure/world_builder/sparsity.py`
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
- `engine/tests/test_opening_health.py`
- `engine/tests/test_spec_consistency.py`
- `engine/tests/test_tempo.py`
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
- `frontend/components/scene/SceneView.ts`
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
- `graph_queries_narratives.py`
- `graph_queries_search.py`
- `handlers/__init__.py`
- `handlers/base.py`
- `handlers/companion.py`
- `hooks/transformers.ts`
- `hooks/useGameState.ts`
- `hooks/useMoments.ts`
- `hooks/useTempo.ts`
- `inject_to_narrator.py`
- `inject_world.py`
- `lib/api.ts`
- `lib/api/moments.ts`
- `lib/map/projection.ts`
- `lib/map/random.ts`
- `links.py`
- `lint_terminology.py`
- `moment_graph/queries.py`
- `moment_graph/traversal.py`
- `moment_processor.py`
- `moments.py`
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
- `semantic_proximity_based_character_node_selector.py`
- `service.py`
- `snake_case.py`
- `sparsity.py`
- `speaker.py`
- `sse_broadcast.py`
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
- `tests/infrastructure/test_storm_loader.py`
- `tests/infrastructure/test_storms.py`
- `tests/infrastructure/test_world_builder.py`
- `tests/infrastructure/world_builder/__init__.py`
- `tests/infrastructure/world_builder/test_world_builder.py`
- `tests/network/test_bleed_through.py`
- `tests/network/test_ghost_dialogue.py`
- `tests/network/test_shadow_feed.py`
- `tests/network/test_transposition.py`
- `tests/network/test_voyager_system.py`
- `tests/network/test_world_scavenger.py`
- `tests/product/test_billing.py`
- `tests/product/test_chronicle_system.py`
- `tests/product/test_gtm_strategy.py`
- `tests/product/test_ledger_lock.py`
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
- `useGameState.ts`
- `views.py`
- `world_builder.py`
- `world_runner.py`

**Doc refs:**
- `agents/developer/CLAUDE.md`
- `agents/narrator/CLAUDE.md`
- `agents/narrator/CLAUDE_old.md`
- `agents/world_runner/CLAUDE.md`
- `agents/world_runner/CLAUDE_PROMPT.md`
- `archive/SYNC_History_archive_2025-12.md`
- `archive/SYNC_archive_2024-12.md`
- `data/ARCHITECTURE — Cybernetic Studio.md`
- `data/Distributed-Content-Generation-Network/ALGORITHM Character & Narrative Transposition Logic.md`
- `data/Distributed-Content-Generation-Network/Blood Chronicle System.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Business Model Stress Test.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Character Import.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Go-To-Market Strategy.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Refugee System.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md`
- `data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md`
- `data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md`
- `data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md`
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
- `docs/agents/narrator/archive/SYNC_archive_2024-12.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Drives_And_Metrics.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/IMPLEMENTATION_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
- `docs/design/archive/SYNC_archive_2024-12.md`
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
- `docs/engine/models/PATTERNS_Models.md`
- `docs/engine/models/VALIDATION_Models.md`
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
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Overview.md`
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md`
- `docs/frontend/PATTERNS_Frontend.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/SYNC_Frontend_archive_2025-12.md`
- `docs/frontend/archive/SYNC_archive_2024-12.md`
- `docs/frontend/map/PATTERNS_Interactive_Travel_Map.md`
- `docs/frontend/map/PATTERNS_Parchment_Map_View.md`
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
- `docs/infrastructure/api/PATTERNS_Api.md`
- `docs/infrastructure/api/SYNC_Api.md`
- `docs/infrastructure/api/TEST_Api.md`
- `docs/infrastructure/api/VALIDATION_Api.md`
- `docs/infrastructure/async/ALGORITHM/ALGORITHM_Overview.md`
- `docs/infrastructure/async/ALGORITHM_Async_Architecture.md`
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
- `docs/infrastructure/async/SYNC_Async_Architecture_archive_2025-12.md`
- `docs/infrastructure/async/TEST_Async_Architecture.md`
- `docs/infrastructure/async/archive/SYNC_archive_2024-12.md`
- `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md`
- `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`
- `docs/infrastructure/canon/SYNC_Canon.md`
- `docs/infrastructure/canon/TEST_Canon.md`
- `docs/infrastructure/canon/VALIDATION_Canon.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Indexing.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Overview.md`
- `docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Search.md`
- `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- `docs/infrastructure/embeddings/BEHAVIORS_Embeddings.md`
- `docs/infrastructure/embeddings/IMPLEMENTATION_Embeddings.md`
- `docs/infrastructure/embeddings/PATTERNS_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings_archive_2025-12.md`
- `docs/infrastructure/embeddings/TEST/TEST_Cases.md`
- `docs/infrastructure/embeddings/TEST/TEST_Overview.md`
- `docs/infrastructure/embeddings/TEST_Embeddings.md`
- `docs/infrastructure/embeddings/VALIDATION_Embeddings.md`
- `docs/infrastructure/embeddings/archive/SYNC_archive_2024-12.md`
- `docs/infrastructure/history/ALGORITHM_History.md`
- `docs/infrastructure/history/BEHAVIORS_History.md`
- `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md`
- `docs/infrastructure/history/PATTERNS_History.md`
- `docs/infrastructure/history/SYNC_History.md`
- `docs/infrastructure/history/TEST_History.md`
- `docs/infrastructure/history/VALIDATION_History.md`
- `docs/infrastructure/history/archive/SYNC_History_archive_2025-12.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/BEHAVIORS_Tempo.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/infrastructure/tempo/TEST_Tempo.md`
- `docs/infrastructure/tempo/VALIDATION_Tempo.md`
- `docs/network/transposition/ALGORITHM_Transposition_Pipeline.md`
- `docs/network/transposition/PATTERNS_Local_Canon_Primary.md`
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
- `docs/physics/SYNC_Physics_archive_2025-12.md`
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
- `docs/physics/graph/SYNC_Graph_archive_2025-12.md`
- `docs/physics/graph/VALIDATION.md`
- `docs/physics/graph/VALIDATION_Living_Graph.md`
- `docs/product/billing/PATTERNS_Pay_To_Preserve_History.md`
- `docs/scenarios/README.md`
- `docs/schema/SCHEMA.md`
- `docs/schema/SCHEMA/SCHEMA_Links.md`
- `docs/schema/SCHEMA/SCHEMA_Nodes.md`
- `docs/schema/SCHEMA_Moments.md`
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`
- `docs/schema/VALIDATION_Graph.md`
- `docs/schema/VALIDATION_Living_Graph.md`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `docs/schema/models/SYNC_Schema_Models.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM/ALGORITHM_Routes.md`
- `docs/world/map/ALGORITHM/places/ALGORITHM_Places.md`
- `docs/world/map/ALGORITHM/rendering/ALGORITHM_Rendering_Pipeline.md`
- `docs/world/map/ALGORITHM/routes/ALGORITHM_Routes.md`
- `docs/world/map/ALGORITHM_Map.md`
- `docs/world/map/ALGORITHM_Rendering.md`
- `docs/world/map/BEHAVIORS_Map.md`
- `docs/world/map/IMPLEMENTATION_Map_Code_Architecture.md`
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
- `docs/world/map/TEST_Map_Test_Coverage.md`
- `docs/world/map/archive/SYNC_archive_2024-12.md`
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
- `docs/world/scraping/TEST_World_Scraping.md`
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
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`
- `views/VIEW_Test_Write_Tests_And_Verify.md`
- `world/map/SYNC_Map.md`

**Sections:**
- # Repository Map: the-blood-ledger

**Code refs:**
- `app/layout.tsx`
- `app/page.tsx`
- `app/scenarios/page.tsx`
- `app/start/page.tsx`
- `components/GameClient.tsx`
- `components/GameLayout.tsx`
- `components/SpeedControl.tsx`
- `components/chronicle/ChroniclePanel.tsx`
- `components/debug/DebugPanel.tsx`
- `components/map/MapCanvas.tsx`
- `components/map/MapClient.tsx`
- `components/minimap/Minimap.tsx`
- `components/minimap/SunArc.tsx`
- `components/moment/ClickableText.tsx`
- `components/moment/MomentDebugPanel.tsx`
- `components/moment/MomentDisplay.tsx`
- `components/moment/MomentStream.tsx`
- `components/panel/ChronicleTab.tsx`
- `components/panel/ConversationsTab.tsx`
- `components/panel/LedgerTab.tsx`
- `components/panel/RightPanel.tsx`
- `components/scene/CenterStage.tsx`
- `components/scene/CharacterRow.tsx`
- `components/scene/Hotspot.tsx`
- `components/scene/HotspotRow.tsx`
- `components/scene/ObjectRow.tsx`
- `components/scene/SceneBanner.tsx`
- `components/scene/SceneHeader.tsx`
- `components/scene/SceneImage.tsx`
- `components/scene/SceneView.tsx`
- `components/scene/SettingStrip.tsx`
- `components/ui/Toast.tsx`
- `components/voices/Voices.tsx`
- `hooks/useGameState.ts`
- `hooks/useMoments.ts`
- `hooks/useTempo.ts`
- `lib/api.ts`
- `lib/map/projection.ts`
- `lib/map/random.ts`
- `types/game.ts`
- `types/map.ts`
- `types/moment.ts`

**Doc refs:**
- `docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/map/PATTERNS_Parchment_Map_View.md`
- `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`
- `docs/frontend/scenarios/PATTERNS_Scenario_Selection.md`
- `docs/frontend/scene/PATTERNS_Scene.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`

**Sections:**
- # Repository Map: the-blood-ledger/frontend
- ## Statistics
- ## File Tree
- ## File Details

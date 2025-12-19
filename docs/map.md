# Repository Map: the-blood-ledger

*Generated: 2025-12-19 01:59*

- **Files:** 219
- **Directories:** 64
- **Total Size:** 2.2M
- **Doc Files:** 122
- **Code Files:** 92
- **Areas:** 7 (docs/ subfolders)
- **Modules:** 13 (subfolders in areas)
- **DOCS Links:** 1 (0.01 avg per code file)

- markdown: 122
- python: 51
- tsx: 30
- typescript: 8
- css: 1
- html: 1
- shell: 1

```
├── agents/ (63.7K)
│   ├── developer/ (6.4K)
│   │   └── CLAUDE.md (6.4K)
│   ├── narrator/ (33.5K)
│   │   └── CLAUDE.md (33.5K)
│   └── world_runner/ (23.9K)
│       └── CLAUDE.md (23.9K)
├── docs/ (1.1M)
│   ├── agents/ (150.6K)
│   │   ├── narrator/ (83.0K)
│   │   │   ├── ALGORITHM_Prompt_Structure.md (9.6K)
│   │   │   ├── ALGORITHM_Rolling_Window.md (7.4K)
│   │   │   ├── ALGORITHM_Scene_Generation.md (9.5K)
│   │   │   ├── ALGORITHM_Thread.md (4.7K)
│   │   │   ├── BEHAVIORS_Narrator.md (9.1K)
│   │   │   ├── HANDOFF_Rolling_Window_Architecture.md (6.8K)
│   │   │   ├── INPUT_REFERENCE.md (6.8K)
│   │   │   ├── PATTERNS_Narrator.md (6.4K)
│   │   │   ├── PATTERNS_World_Building.md (6.0K)
│   │   │   ├── TOOL_REFERENCE.md (12.6K)
│   │   │   └── (..3 more files)
│   │   └── world-runner/ (67.6K)
│   │       ├── ALGORITHM_Graph_Ticks.md (4.7K)
│   │       ├── ALGORITHM_World_Runner.md (17.1K)
│   │       ├── BEHAVIORS_World_Runner.md (13.6K)
│   │       ├── INPUT_REFERENCE.md (6.2K)
│   │       ├── PATTERNS_World_Runner.md (8.1K)
│   │       ├── SYNC_World_Runner.md (1.3K)
│   │       └── TOOL_REFERENCE.md (16.6K)
│   ├── design/ (134.4K)
│   │   ├── opening/ (69.4K)
│   │   │   ├── ALGORITHM_Opening.md (915)
│   │   │   ├── BEHAVIORS_Opening.md (6.8K)
│   │   │   ├── CLAUDE.md (26.2K)
│   │   │   ├── CONTENT.md (10.2K)
│   │   │   ├── GUIDE.md (9.5K)
│   │   │   ├── PATTERNS_Opening.md (6.9K)
│   │   │   ├── SYNC_Opening.md (1.1K)
│   │   │   ├── TEST_Opening.md (627)
│   │   │   └── VALIDATION_Opening.md (7.2K)
│   │   ├── scenarios/ (10.3K)
│   │   │   └── README.md (10.3K)
│   │   ├── ALGORITHM_Vision.md (12.5K)
│   │   ├── BEHAVIORS_Vision.md (17.2K)
│   │   ├── PATTERNS_Vision.md (13.9K)
│   │   ├── SYNC_Vision.md (3.8K)
│   │   ├── TEST_Vision.md (996)
│   │   └── VALIDATION_Vision.md (6.2K)
│   ├── frontend/ (20.7K)
│   │   ├── scene/ (11.9K)
│   │   │   ├── ALGORITHM_Scene.md (1.3K)
│   │   │   ├── BEHAVIORS_Scene.md (1.3K)
│   │   │   ├── PATTERNS_Scene.md (5.7K)
│   │   │   ├── SYNC_Scene.md (1.8K)
│   │   │   ├── TEST_Scene.md (839)
│   │   │   └── VALIDATION_Scene.md (1.0K)
│   │   ├── PATTERNS_Presentation_Layer.md (4.5K)
│   │   └── SYNC_Frontend.md (4.3K)
│   ├── infrastructure/ (213.5K)
│   │   ├── async/ (44.7K)
│   │   │   ├── ALGORITHM_Discussion_Trees.md (4.6K)
│   │   │   ├── ALGORITHM_Fog_Of_War.md (2.8K)
│   │   │   ├── ALGORITHM_Graph_SSE.md (3.4K)
│   │   │   ├── ALGORITHM_Hook_Injection.md (4.5K)
│   │   │   ├── ALGORITHM_Image_Generation.md (2.8K)
│   │   │   ├── ALGORITHM_Runner_Protocol.md (3.8K)
│   │   │   ├── ALGORITHM_Waypoint_Creation.md (2.3K)
│   │   │   ├── BEHAVIORS_Travel_Experience.md (2.9K)
│   │   │   ├── PATTERNS_Async_Architecture.md (10.8K)
│   │   │   ├── SYNC_Async_Architecture.md (4.7K)
│   │   │   └── (..2 more files)
│   │   ├── embeddings/ (42.5K)
│   │   │   ├── ALGORITHM_Embeddings.md (8.2K)
│   │   │   ├── BEHAVIORS_Embeddings.md (6.5K)
│   │   │   ├── PATTERNS_Embeddings.md (6.1K)
│   │   │   ├── SYNC_Embeddings.md (6.0K)
│   │   │   ├── TEST_Embeddings.md (8.7K)
│   │   │   └── VALIDATION_Embeddings.md (7.1K)
│   │   ├── history/ (46.2K)
│   │   │   ├── ALGORITHM_History.md (10.6K)
│   │   │   ├── BEHAVIORS_History.md (7.0K)
│   │   │   ├── PATTERNS_History.md (5.5K)
│   │   │   ├── SYNC_History.md (6.0K)
│   │   │   ├── TEST_History.md (9.5K)
│   │   │   └── VALIDATION_History.md (7.6K)
│   │   ├── image-generation/ (16.3K)
│   │   │   ├── ALGORITHM_Image_Generation.md (1.1K)
│   │   │   ├── BEHAVIORS_Image_Generation.md (1.1K)
│   │   │   ├── PATTERNS_Image_Generation.md (9.9K)
│   │   │   ├── SYNC_Image_Generation.md (2.6K)
│   │   │   ├── TEST_Image_Generation.md (824)
│   │   │   └── VALIDATION_Image_Generation.md (803)
│   │   └── scene-memory/ (63.8K)
│   │       ├── ALGORITHM_Scene_Memory.md (18.8K)
│   │       ├── BEHAVIORS_Scene_Memory.md (12.4K)
│   │       ├── PATTERNS_Scene_Memory.md (6.6K)
│   │       ├── SYNC_Scene_Memory.md (5.3K)
│   │       └── VALIDATION_Scene_Memory.md (20.6K)
│   ├── physics/ (267.4K)
│   │   ├── graph/ (29.9K)
│   │   │   ├── ALGORITHM_Energy_Flow.md (11.2K)
│   │   │   ├── ALGORITHM_Weight.md (4.5K)
│   │   │   ├── BEHAVIORS_Graph.md (6.6K)
│   │   │   ├── PATTERNS_Graph.md (2.3K)
│   │   │   └── SYNC_Graph.md (5.1K)
│   │   ├── ALGORITHM_Actions.md (11.8K)
│   │   ├── ALGORITHM_Canon.md (15.0K)
│   │   ├── ALGORITHM_Energy.md (64.1K)
│   │   ├── ALGORITHM_Handlers.md (11.6K)
│   │   ├── ALGORITHM_Physics.md (12.4K)
│   │   ├── ALGORITHM_Questions.md (10.6K)
│   │   ├── BEHAVIORS_Physics.md (11.7K)
│   │   ├── IMPLEMENTATION_Physics.md (31.9K)
│   │   ├── TEST_Physics.md (16.7K)
│   │   ├── VALIDATION_Physics.md (13.9K)
│   │   └── (..5 more files)
│   ├── schema/ (109.9K)
│   │   ├── SCHEMA.md (48.2K)
│   │   ├── SCHEMA_Moments.md (21.5K)
│   │   ├── VALIDATION_Graph.md (2.3K)
│   │   └── VALIDATION_Living_Graph.md (37.9K)
│   ├── world/ (89.3K)
│   │   ├── map/ (60.7K)
│   │   │   ├── ALGORITHM_Places.md (9.3K)
│   │   │   ├── ALGORITHM_Rendering.md (17.0K)
│   │   │   ├── ALGORITHM_Routes.md (12.2K)
│   │   │   ├── BEHAVIORS_Map.md (14.0K)
│   │   │   ├── PATTERNS_Map.md (6.5K)
│   │   │   └── SYNC_Map.md (1.7K)
│   │   └── scraping/ (28.6K)
│   │       ├── ALGORITHM_Events.md (3.0K)
│   │       ├── ALGORITHM_Geography.md (2.7K)
│   │       ├── ALGORITHM_Narratives.md (3.5K)
│   │       ├── ALGORITHM_Pipeline.md (2.3K)
│   │       ├── ALGORITHM_Political.md (3.2K)
│   │       ├── ALGORITHM_Tensions.md (2.8K)
│   │       ├── BEHAVIORS_World_Scraping.md (1.1K)
│   │       ├── PATTERNS_World_Scraping.md (2.6K)
│   │       ├── SYNC_World_Scraping.md (3.7K)
│   │       ├── VALIDATION_World_Scraping.md (2.8K)
│   │       └── (..1 more files)
│   └── map.md (147.3K)
├── engine/ (859.6K)
│   ├── api/ (87.3K)
│   │   ├── app.py (48.2K)
│   │   ├── moments.py (16.9K)
│   │   ├── playthroughs.py (22.1K)
│   │   └── (..1 more files)
│   ├── db/ (187.7K)
│   │   ├── __init__.py (1.8K)
│   │   ├── graph_ops.py (98.7K)
│   │   ├── graph_ops_moments.py (20.0K)
│   │   ├── graph_queries.py (58.5K)
│   │   └── graph_query_utils.py (8.7K) →
│   ├── embeddings/ (6.0K)
│   │   ├── service.py (5.6K)
│   │   └── (..1 more files)
│   ├── graph/ (119.2K)
│   │   └── health/ (119.2K)
│   │       ├── README.md (3.4K)
│   │       ├── check_health.py (14.0K)
│   │       ├── example_queries.cypher (18.1K)
│   │       ├── lint_terminology.py (14.9K)
│   │       ├── query_outputs.md (23.3K)
│   │       ├── query_results.md (16.2K)
│   │       └── test_schema.py (29.3K)
│   ├── history/ (34.6K)
│   │   ├── README.md (6.7K)
│   │   ├── __init__.py (1.5K)
│   │   ├── conversations.py (6.7K)
│   │   └── service.py (19.7K)
│   ├── memory/ (19.5K)
│   │   ├── moment_processor.py (19.3K)
│   │   └── (..1 more files)
│   ├── models/ (37.5K)
│   │   ├── __init__.py (2.3K)
│   │   ├── base.py (12.8K)
│   │   ├── links.py (7.2K)
│   │   ├── nodes.py (10.6K)
│   │   └── tensions.py (4.6K)
│   ├── moment_graph/ (30.9K)
│   │   ├── queries.py (13.8K)
│   │   ├── surface.py (9.0K)
│   │   ├── traversal.py (7.7K)
│   │   └── (..1 more files)
│   ├── moments/ (1.1K)
│   │   └── __init__.py (1.1K)
│   ├── orchestration/ (30.9K)
│   │   ├── __init__.py (507)
│   │   ├── narrator.py (7.9K)
│   │   ├── orchestrator.py (17.6K)
│   │   └── world_runner.py (5.0K)
│   ├── physics/ (21.9K)
│   │   ├── constants.py (3.7K)
│   │   ├── tick.py (17.7K)
│   │   └── (..1 more files)
│   ├── queries/ (9.7K)
│   │   ├── semantic.py (9.2K)
│   │   └── (..1 more files)
│   ├── scripts/ (18.0K)
│   │   ├── check_injection.py (1.4K)
│   │   ├── generate_images_for_existing.py (11.3K)
│   │   ├── inject_to_narrator.py (3.6K)
│   │   └── seed_moment_sample.py (1.8K)
│   ├── tests/ (242.5K)
│   │   ├── test_behaviors.py (18.3K)
│   │   ├── test_e2e_moment_graph.py (16.7K)
│   │   ├── test_history.py (15.0K)
│   │   ├── test_implementation.py (28.8K)
│   │   ├── test_integration_scenarios.py (19.9K)
│   │   ├── test_models.py (28.6K)
│   │   ├── test_moment_graph.py (33.2K)
│   │   ├── test_moments_api.py (15.5K)
│   │   ├── test_narrator_integration.py (16.4K)
│   │   ├── test_spec_consistency.py (18.7K)
│   │   └── (..4 more files)
│   ├── .env.example (540)
│   ├── Dockerfile (664)
│   ├── __init__.py (696)
│   ├── init_db.py (8.7K)
│   ├── run.py (1.8K)
│   └── (..1 more files)
├── frontend/ (191.8K)
│   ├── app/ (16.5K)
│   │   ├── map/ (124)
│   │   │   └── (..1 more files)
│   │   ├── scenarios/ (7.0K)
│   │   │   └── page.tsx (7.0K)
│   │   ├── start/ (6.6K)
│   │   │   └── page.tsx (6.6K)
│   │   ├── globals.css (1.6K)
│   │   ├── layout.tsx (861)
│   │   └── (..1 more files)
│   ├── components/ (124.8K)
│   │   ├── chronicle/ (3.9K)
│   │   │   └── ChroniclePanel.tsx (3.9K)
│   │   ├── debug/ (13.0K)
│   │   │   └── DebugPanel.tsx (13.0K)
│   │   ├── map/ (27.4K)
│   │   │   ├── MapCanvas.tsx (22.7K)
│   │   │   ├── MapClient.tsx (4.6K)
│   │   │   └── (..1 more files)
│   │   ├── minimap/ (2.8K)
│   │   │   └── Minimap.tsx (2.8K)
│   │   ├── moment/ (19.3K)
│   │   │   ├── ClickableText.tsx (3.6K)
│   │   │   ├── MomentDebugPanel.tsx (6.6K)
│   │   │   ├── MomentDisplay.tsx (5.4K)
│   │   │   ├── MomentStream.tsx (3.4K)
│   │   │   └── (..1 more files)
│   │   ├── panel/ (9.3K)
│   │   │   ├── ChronicleTab.tsx (1.6K)
│   │   │   ├── ConversationsTab.tsx (3.1K)
│   │   │   ├── LedgerTab.tsx (2.3K)
│   │   │   └── RightPanel.tsx (2.3K)
│   │   ├── scene/ (38.7K)
│   │   │   ├── CenterStage.tsx (14.4K)
│   │   │   ├── CharacterRow.tsx (2.4K)
│   │   │   ├── Hotspot.tsx (2.6K)
│   │   │   ├── HotspotRow.tsx (2.8K)
│   │   │   ├── ObjectRow.tsx (2.1K)
│   │   │   ├── SceneBanner.tsx (2.5K)
│   │   │   ├── SceneHeader.tsx (1.1K)
│   │   │   ├── SceneImage.tsx (3.2K)
│   │   │   ├── SceneView.tsx (4.0K)
│   │   │   ├── SettingStrip.tsx (2.1K)
│   │   │   └── (..2 more files)
│   │   ├── ui/ (3.1K)
│   │   │   └── Toast.tsx (3.1K)
│   │   ├── voices/ (1.6K)
│   │   │   └── Voices.tsx (1.6K)
│   │   ├── GameClient.tsx (3.6K)
│   │   ├── GameLayout.tsx (2.0K)
│   │   └── (..1 more files)
│   ├── hooks/ (18.7K)
│   │   ├── useGameState.ts (13.2K)
│   │   └── useMoments.ts (5.5K)
│   ├── lib/ (14.9K)
│   │   ├── map/ (3.4K)
│   │   │   ├── projection.ts (2.7K)
│   │   │   ├── random.ts (722)
│   │   │   └── (..1 more files)
│   │   └── api.ts (11.5K)
│   ├── types/ (15.8K)
│   │   ├── game.ts (9.9K)
│   │   ├── map.ts (4.0K)
│   │   └── moment.ts (1.8K)
│   └── (..4 more files)
├── prompts/ (4.4K)
│   └── discussion_generator.md (4.4K)
├── tools/ (24.8K)
│   ├── image_generation/ (11.1K)
│   │   ├── README.md (2.2K)
│   │   └── generate_image.py (9.0K)
│   └── stream_dialogue.py (13.6K)
├── .gitignore (617)
├── .ngramignore (806)
├── AGENTS.md (2.9K)
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
- # Narrator — Algorithm: Prompt Structure
- ## The Orchestration
- ## File Locations
- ## Prompt Structure
- ## World Injection Block
- ## Scene Context Block
- ## Generation Instructions
- ## Required Output Schema
- ## Time Elapsed Guidelines
- ## Handling Different Injection Types
- ## The --continue Flag
- # First scene of playthrough
- # All subsequent scenes
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

**Sections:**
- # Narrator — Algorithm: Rolling Window Generation
- ## The Model
- ## The Window
- ## On Scene Load
- ## On Click
- ## Generation Priority
- ## Handling Slow Generation
- ## Scene Transitions
- ## Caching Strategy
- ## Background Worker
- ## Metrics to Track
- ## Example Flow
- ## Free Input Handling

**Sections:**
- # Narrator — Algorithm: Scene Generation
- ## Purpose
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
- ## Quality Control

**Sections:**
- # Narrator — Algorithm: The Thread
- ## The Thread
- ## Why Continuity Matters
- ## The Implementation
- # First scene
- # Subsequent scenes (same conversation)
- # Continue indefinitely
- ## Thread State
- ## When to Start Fresh
- ## Thread Management
- ## Generation Flow
- ## The Narrator's Memory
- ## Thread vs Graph
- ## Error Handling

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

**Sections:**
- # Narrator Input Reference
- ## Script Locations
- ## Prompt Structure
- ## Scene Context (Always Provided)
- ## World Injection (If Flips Occurred)
- ## Complete Example Input
- ## Handling World Injection
- ## Query Patterns

**Sections:**
- # Narrator — Patterns: Why This Design
- ## The Core Insight
- ## The Five Principles
- ## The Authorial Model
- ## Pre-Baked Scene Trees
- ## Generation Strategy
- ## The Schema
- ## What the Narrator Controls
- ## Free Input: The Exception
- ## The Narrator's Workflow
- ## Why This Matters
- ## Connection to Graph

**Sections:**
- # Narrator — Patterns: World Building Through Pre-Generation
- ## The Core Insight
- ## What This Creates
- ## The World Thickens
- ## The Player Feels This
- ## Graph Enrichment Protocol
- ## The Accumulation Effect
- ## What Gets Written Back
- ## The Narrator as Archeologist
- ## Why This Matters for Engagement
- ## Implementation Note

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
- # World Runner — Algorithm: Graph Ticks vs Narrative Flips
- ## Two Different Things
- ## Graph Ticks (Mechanical)
- ## Narrative Flips (World Runner)
- ## The Flow
- ## Why This Split
- ## Tick Frequency
- ## Cascade Handling

**Sections:**
- # World Runner — Algorithm: How It Works
- ## Core Principle: Runner Owns the Tick Loop
- # Run one graph tick (5 min)
- # Check for flips
- # Interrupt — something happened TO THE PLAYER
- # Process non-player flips (world keeps moving)
- # Completed without interruption
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

**Sections:**
- # World Runner Input Reference
- ## Script Location
- ## Prompt Structure
- ## Flip Context (Why You're Called)
- ## Graph Context (What You Need to Know)
- ## Player Context (Where Player Is)
- ## Complete Example Input
- ## Processing Guidance

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

**Sections:**
- # World Runner — Sync: Current State
- ## Current State
- ## Documentation Status
- ## Next Steps
- ## ARCHIVE

**Sections:**
- # World Runner Tool Reference
- ## Complete Output Schema
- ## Graph Mutations
- ## World Injection
- ## Complete Example
- ## Validation Rules
- ## Processing Order
- ## JSON Schema (for programmatic validation)

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
- `engine/orchestration/opening.py`

**Sections:**
- # The Opening — Sync
- ## Chain Reference
- ## Current Notes
- ## Upcoming Work

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

**Doc refs:**
- `docs/physics/API_Physics.md`

**Sections:**
- # Scene View — Sync: Current State
- ## Snapshot
- ## Open Questions
- ## Next Deliverables
- ## Dependencies
- ## Handoff Notes

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
- `frontend/app/map/page.tsx`
- `frontend/app/page.tsx`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/hooks/useGameState.ts`
- `frontend/hooks/useMoments.ts`
- `frontend/lib/api.ts`
- `frontend/types/game.ts`

**Doc refs:**
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/physics/API_Physics.md`

**Sections:**
- # Frontend — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS

**Sections:**
- # Discussion Trees — Algorithm
- ## Principle
- ## Lifecycle
- ## Tree Structure
- ## Player Triggered
- ## Idle Triggered
- ## Generation Prompt
- ## File Format
- ## Deletion on Use
- # Delete the explored branch
- # Save updated tree
- # Check if regeneration needed

**Sections:**
- # Fog of War — Algorithm
- ## Principle
- ## Visibility States
- ## Reveal Triggers
- ## Graph Storage
- ## SSE Event
- ## Frontend Rendering
- ## Travel Revelation
- # Update position
- # Reveal place
- # SSE broadcast handled by graph

**Sections:**
- # Graph SSE — Algorithm
- ## Principle
- ## Connection
- ## Event Types
- ## Backend Implementation
- # Write to graph
- # Emit SSE
- # Update graph
- # Emit SSE
- ## Frontend Handling
- ## Connection Management
- ## Performance Considerations

**Code refs:**
- `engine/scripts/check_injection.py`

**Sections:**
- # Hook Injection — Algorithm
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
- # Image Generation — Algorithm
- ## Principle
- ## Trigger
- ## Process
- ## Prompt Construction
- ## Output
- ## Implementation
- # Generate image (async)
- # Save to disk
- # Update graph
- # SSE broadcast happens automatically from graph
- ## Graph Hook
- # Broadcast place_created (no image yet)
- # Queue image generation

**Sections:**
- # Runner Protocol — Algorithm
- ## Invocation
- ## Reading Output
- ## During Processing
- ## Completion Payload
- ## Narrator Handling
- # May need to re-spawn Runner for remaining journey
- ## Key Clarifications

**Sections:**
- # Waypoint Creation — Algorithm
- ## Principle
- ## Creation Flow
- ## Place Node Schema
- ## Naming Patterns
- ## Persistence
- ## Graph Write
- # Write to graph (triggers SSE + image generation)

**Sections:**
- # Travel Experience — Behaviors
- ## Core Behavior
- ## What the Player Sees
- ## Player Input During Travel
- ## Duration
- ## Anti-Patterns
- ## Success Metrics

**Sections:**
- # Async Architecture — Design Patterns
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
- `check_injection.py`
- `generate_images_for_existing.py`
- `graph_ops.py`
- `graph_queries.py`
- `narrator.py`
- `physics/tick.py`
- `world_runner.py`

**Sections:**
- # Async Architecture — State & Implementation Plan
- ## Overview
- ## Current State vs Target State
- ## Key Decisions Made
- ## Open Questions
- ## Next Action
- ## ARCHIVE

**Code refs:**
- `engine/embeddings/service.py`

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
- `engine/embeddings/service.py`

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
- `engine/embeddings/service.py`

**Sections:**
- # Embeddings — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## IMPLEMENTATION PLAN
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS

**Code refs:**
- `engine/embeddings/service.py`

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
- `engine/embeddings/service.py`

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

**Sections:**
- # History — Sync: Current State
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

**Sections:**
- # Blood Ledger Image Prompting Guide
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
- ## What's Canonical (v2)
- ## What's Working
- ## Approach
- ## Prompt Specifics
- ## Files
- ## Open Questions
- ## Next Steps
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

**Sections:**
- # Scene Memory System — Sync
- ## DOCUMENT CHAIN
- ## IMPLEMENTATION STATUS
- ## INTEGRATION POINTS
- ## SCHEMA DEPENDENCIES
- ## OPEN QUESTIONS
- ## DECISIONS MADE
- ## NEXT STEPS
- ## CHANGELOG

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
- ## Step 5: Tick Pressures
- # Check for flip
- # Tick gradual component
- # Find scheduled floor
- # Use higher of ticked or floor
- ## Step 6: Detect Flips
- ## Full Tick
- # 1. Character energies (relationship × proximity)
- # 2. Flow into narratives (characters pump)
- # 3. Propagate between narratives (link-type dependent)
- # 4. Decay
- # 5. Check conservation (soft global constraint)
- # 6. Adjust criticality (dynamic decay_rate)
- # 7. Pressure ticks
- # 8. Detect flips
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

**Sections:**
- # Graph — Algorithm: Weight Computation
- ## What Weight Means
- ## Weight Formula
- # Clamp and apply focus evolution
- ## Component: Belief Intensity
- ## Component: Player Connection
- # Direct: player believes it
- # Indirect: about someone player knows
- # Distant: no direct connection
- ## Component: Contradiction Bonus
- # Bonus is limited by weaker of the two
- ## Component: Recency Factor
- ## Focus Evolution
- ## When Weight Is Recomputed
- ## Weight Thresholds
- ## Example Computation

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

**Sections:**
- # Graph — Current State
- ## What Exists
- ## What's Missing
- ## Key Design Decisions
- ## Parameters
- ## Criticality Targets
- ## The Full Energy Cycle
- ## Open Questions
- ## Next Steps

**Code refs:**
- `engine/orchestration/orchestrator.py`

**Sections:**
- # Physics — Algorithm: Action Processing
- ## CHAIN
- ## Core Principle
- ## Why Actions Are Special
- ## Action Queue
- ## Action Processing Steps
- # 1. VALIDATE — Is action still possible?
- # 2. EXECUTE — Modify graph state
- # 3. CONSEQUENCES — Generate consequence moments
- # 4. INJECT — Consequences enter graph with energy
- ## Step 1: Validate
- # Can actor travel to destination?
- # Is thing still present and unowned?
- # Is target still present and alive?
- # Does actor have the thing? Is recipient present?
- ## Step 2: Execute
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
- ## Step 3: Generate Consequences
- # Departure noticed
- # Arrival noticed
- # Witness reactions will be generated by their handlers
- ## Step 4: Inject Consequences
- # Create moment with initial energy
- # Create links
- # Physics takes over — consequence may flip, trigger handlers
- ## Mutex Handling
- # First action already processed (it's first in queue)
- # Second action validation will fail
- # Generate "blocked" consequence
- # Blocked consequence triggers actor_b's handler
- # Handler can generate reaction: frustration, new plan, etc.
- ## Action Types Reference
- ## Sequential Processing
- ## What Action Processing Does NOT Do
- ## Invariants

**Code refs:**
- `engine/canon/holder.py`

**Sections:**
- # Physics — Algorithm: Canon Holder
- ## CHAIN
- ## Core Principle
- ## The Flow
- ## Canon Holder Responsibilities
- ## The Code Shape
- # 1. Status change
- # 2. Energy cost (actualization)
- # 3. THEN link (history chain)
- # 4. Time passage
- # 5. Strength mechanics
- # 6. Actions
- # 7. Notify frontend
- ## Flip Detection
- # Check still valid (state may have changed)
- # Flip to active
- # Handler needed?
- # Async - handler will call record_to_canon when done
- # Direct record
- ## Status Progression
- ## Who Speaks?
- ## Rate Limiting
- # ... process ...
- ## Actualization Cost
- ## Strength Mechanics Applied
- # ABOUT links activated
- # Confirming evidence
- # Contradicting evidence
- # Recent narratives in same conversation
- ## Action Processing
- # Change AT link
- # Change CARRIES link
- # Change CARRIES link
- # Complex — may trigger combat
- # Thing-specific effects
- # Apply Commitment mechanic (M5)
- ## Time Passage
- # Adjust by text length
- # Check for time-based events
- # Decay check (large time jumps)
- ## THEN Links
- ## Frontend Notification
- ## Simultaneous Actions Are Drama
- ## True Mutex (Rare)
- # Winner proceeds to canon
- # Loser returns to possible, decayed
- ## History Is Queryable
- ## Parameters
- ## Invariants
- ## What Canon Holder Does NOT Do

**Code refs:**
- `engine/physics/energy.py`

**Sections:**
- # Graph — Algorithm: Energy Mechanics
- ## CHAIN
- ## Core Principles
- # NODE TYPES
- ## Weight vs Energy
- ## Why Both Matter
- ## Surfacing / Relevance
- ## Character Attributes
- ## Narrative Attributes
- ## Moment Attributes
- # LINK TYPES
- ## Character Links
- ## Narrative Links
- ## Moment Links
- ## Link Properties
- # NARRATIVE TYPES
- # LINK STRENGTH
- ## Principle
- ## Timescales (No Circularity)
- ## Default Initial Strength
- ## Base Functions
- # STRENGTH MECHANICS (Six Categories)
- ## Principle
- ## M1: ACTIVATION
- # Speaking is stronger than thinking
- # Direct address is strongest
- # Speaker's belief activated
- # ABOUT links activated
- ## M2: EVIDENCE
- # Check what this evidence supports
- # Check what this evidence contradicts
- ## M3: ASSOCIATION
- # Create new association if co-occurrence is strong enough
- # Recent narratives in same conversation
- # Co-occurring narratives associate
- ## M4: SOURCE
- # How much does receiver trust source?
- # Average trust from relationship narratives
- # Direct witness vs secondhand
- ## M5: COMMITMENT
- # Higher cost = stronger commitment
- # What beliefs motivated this action?
- ## M6: INTENSITY
- # Tension pressure
- # Danger
- # Emotional weight of moment
- # All strength changes multiplied by intensity
- ## Summary
- ## Agents That Modify Strength
- ## Emergent Scenarios
- ## Why Conservation
- ## The Energy Equation
- # ENERGY SOURCES
- ## S1: Character Pumping
- # Baseline regeneration
- # State modifier
- # Pump budget
- # Distribute by belief strength only
- ## S2: Player Focus Injection
- # Things don't hold energy — redirect to related narratives
- ## S3: World Events
- # Character arrives — they bring their energy with them
- # News creates/energizes a narrative
- # Discovery energizes existing narrative
- ## S4: Tension Pressure (Structural)
- # Draw energy from involved characters
- # Inject into related narratives
- # ENERGY SINKS
- ## K1: Decay
- # Core types resist decay
- ## K2: Actualization
- # Draw from speakers
- # Draw from attached narratives
- # ENERGY TRANSFER (Links)
- ## Principle
- ## T1: CONTRADICTS (Bidirectional)
- # A pulls from B
- # B pulls from A
- ## T2: SUPPORTS (Bidirectional)
- # Energy flows toward equilibrium
- ## T3: ELABORATES (Unidirectional, Parent → Child)
- ## T4: SUBSUMES (Unidirectional, Specific → General)
- ## T5: SUPERSEDES (Draining)
- # Additional drain: old loses extra (world moved on)
- ## T6: ABOUT (Focal Point Pulls)
- # Things don't hold energy — skip
- ## T7: CAN_LEAD_TO (Moment to Moment)
- # Forward flow
- # Reverse flow only if bidirectional
- ## T8: CAN_SPEAK (Character to Moment)
- # Only if character is awake and present
- ## T9: ATTACHED_TO (Moment from Sources)
- # Only nodes with energy
- # Reverse flow: target → moment
- ## Actualization (Energy Spent)
- # Partial drain — recent speech still has presence
- # Status change
- # Remaining energy decays normally from here
- ## Moment Decay by Status
- # MOMENT ENERGY & WEIGHT
- ## Surfacing Logic
- ## Energy Flow Into Moments
- ## Weight Evolution
- ## Example
- # FULL TICK CYCLE
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
- # PHYSICAL GATING
- ## How It Works
- ## Gating Queries
- ## What This Replaces
- ## Example
- # PARAMETERS
- ## Transfer Factors
- ## Moment Decay Rates
- ## Actualization
- ## Source Rates
- ## Sink Rates
- ## Weight Parameters
- ## Floors & Ceilings
- # EMERGENT BEHAVIORS
- ## "Arguments Heat Both Sides"
- ## "Approach Creates Tension"
- ## "Forgotten Things Bite Back"
- ## "The World Feels Alive"
- ## "Thinking About Someone Far Away"
- # M11: FLIP DETECTION
- ## Status Progression
- ## Detection Query
- ## Processing Multiple Ready Moments
- # Check still valid (state may have changed)
- # Flip to active
- # Handler needed?
- # Async - handler will call record_to_canon when done
- # Direct record
- ## Rate Limiting
- # ... process ...
- ## Speaker Resolution
- # M12: CANON HOLDER
- ## The Flow
- ## Canon Holder Responsibilities
- ## Recording Function
- # 1. Status change
- # 2. Energy cost (actualization)
- # 3. THEN link (history chain)
- # 4. Time passage
- # 5. Strength mechanics
- # 6. Actions
- # 7. Notify frontend
- ## Strength Mechanics on Record
- # ABOUT links activated
- # Confirming evidence
- # Contradicting evidence
- # Recent narratives in same conversation
- ## Time Passage
- # Adjust by text length
- # Check for time-based events
- # Decay check (large time jumps)
- ## Action Processing
- # Apply Commitment mechanic (M5)
- ## THEN Links
- ## Frontend Notification
- ## Simultaneous Actions Are Drama
- ## True Mutex (Rare)
- # Winner proceeds to canon
- # Loser returns to possible, decayed
- ## What Canon Holder Does NOT Do
- # M13: AGENT DISPATCH
- ## The Agents
- ## Runner (World)
- # Detect and process breaks
- # Scheduled events
- ## Narrator (Scene)
- ## Citizen (Character)
- ## Main Loop
- # WHAT WE DON'T DO

**Sections:**
- # Physics — Algorithm: Character Handlers
- ## CHAIN
- ## Core Principle
- ## When Handlers Run
- ## What Handler Receives
- ## What Handler Produces
- # Note: NO weight field. Physics assigns weight.
- ## Handler Implementation
- # Build prompt based on character type and speed
- # LLM call
- # Parse structured output
- # Inject into graph (physics assigns weights)
- # Speed-aware framing
- ## Moment Injection (Physics Side)
- # Calculate link strength (how much character energy flows to this moment)
- # Create moment (weight will be computed by physics tick)
- # Create CAN_SPEAK link (character energy → moment weight)
- # Create ATTACHED_TO link
- # Process additional links
- # Queue questions for async answering
- ## Handler Scaling
- # "You there, guard on the left!"
- # individual now has own node, inherits group properties
- # In handler output
- ## Parallel Execution
- # Parallel execution
- # Each handler only writes its own character
- # No conflicts because of isolation
- ## Reaction Scope
- ## Pre-Generation Strategy
- # Create a synthetic "arrival" moment
- # Trigger handler with arrival as trigger
- # By the time player engages, potentials exist
- ## What Handler Does NOT Do
- ## Invariants

**Code refs:**
- `engine/physics/tick.py`

**Sections:**
- # Physics — Algorithm: Physics Tick
- ## CHAIN
- ## Core Principle
- ## What Triggers a Tick
- ## Tick Steps (Sequential)
- # 1. PUMP — Characters inject energy into narratives
- # 2. TRANSFER — Energy flows through narrative links
- # 3. TENSION — Structural tensions concentrate energy
- # 4. DECAY — Energy leaves the system
- # 5. WEIGHT — Recompute moment weights from sources
- # 6. DETECT — Find moments that crossed threshold
- # 7. EMIT — Send flipped moments to Canon Holder
- # 8. BREAKS — Return any structural breaks for handling
- ## Step 1: Character Pumping
- # Baseline regeneration
- # State modifier (dead/unconscious = 0, sleeping = 0.2, awake = 1.0)
- # Distribute by belief strength only - no proximity filter
- ## Step 2: Energy Transfer
- # Narrative links
- # ABOUT links (focal point pulls)
- ## Step 3: Tension Injection
- # Draw from participants
- # Inject into related narratives
- ## Step 4: Decay
- # Narrative decay
- # Character decay
- ## Step 5: Moment Weight Computation
- # From characters who can speak it
- # From attached narratives
- # From attached present characters
- ## Step 6: Flip Detection
- ## Step 7: Emit to Canon Holder
- # Actualization cost
- # Record to canon
- # Trigger handlers for attached characters
- ## Parameters
- ## Graph States
- ## Tick Rate by Speed
- ## What Physics Does NOT Do
- ## Invariants
- ## Relationship to ALGORITHM_Energy.md

**Sections:**
- # Physics — Algorithm: Question Answering
- ## CHAIN
- ## Core Principle
- ## When Questions Arise
- # In character handler
- # Handler needs to know about father
- # Queue question for answering
- # Handler continues with what it knows
- # Does NOT block waiting for answer
- ## Not Async in "Fire and Forget" Sense
- ## Question Answerer Flow
- # 1. GATHER — Get relevant existing facts
- # 2. GENERATE — Invent answer via LLM
- # 3. VALIDATE — Check consistency
- # 4. INJECT — Create nodes in graph
- ## Step 1: Gather Existing Facts
- # Character's existing family
- # Character's origin place
- # Character's existing beliefs/narratives
- # Historical events character witnessed
- ## Step 2: Generate Answer
- ## Step 3: Validate Consistency
- # Check family conflicts
- # Check place conflicts
- # Check temporal conflicts
- ## Step 4: Inject Answer
- # Create new character nodes
- # Create relationship link
- # Create new place nodes
- # Create relationship link
- # Create potential memory moments
- # Create ANSWERED_BY link for traceability
- ## No Special Mechanism for Integration
- # After injection, physics handles integration:
- # New father character exists
- # Memory moments attached to asker exist
- # These have initial weight (e.g., 0.4)
- # Next tick:
- # - Energy propagates through FAMILY links
- # - Memory moments may get boosted if relevant
- # - If weight crosses threshold, memory surfaces
- # No special "integrate answer" logic
- # Just physics
- ## Constraints
- ## Example: "Who is my father?"
- ## What Question Answerer Does NOT Do
- ## Invariants

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
- `__init__.py`
- `api/app.py`
- `api/moments.py`
- `base.py`
- `canon/holder.py`
- `companion.py`
- `handlers/__init__.py`
- `handlers/base.py`
- `handlers/companion.py`
- `moment_graph/queries.py`
- `moment_graph/traversal.py`
- `orchestration/narrator.py`
- `orchestration/orchestrator.py`
- `orchestration/speed.py`
- `orchestrator.py`
- `physics/constants.py`
- `physics/tick.py`

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

**Sections:**
- # Graph Validation
- ## Rules
- ## Valid Mutation
- ## Invalid Mutation
- # No links — char_wulfric would be orphaned
- ## Error Handling
- ## Error Types
- ## Partial Persistence
- # result.persisted = ["char_aldric", "narr_oath", "link_belief_1"]
- # result.rejected = [
- # {"item": "char_wulfric", "error": "orphaned_node", "fix": "Add link..."}
- # ]

**Sections:**
- # THE BLOOD LEDGER — Validation Specification
- # Version: 1.0
- # =============================================================================
- # PURPOSE
- # =============================================================================
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

**Sections:**
- # Map System — Algorithm: Places
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

**Sections:**
- # Map System — Algorithm: Rendering
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

**Sections:**
- # Map System — Algorithm: Routes
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

**Sections:**
- # Map System — Behaviors: Visibility & Interaction
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

**Sections:**
- # Map System — Patterns: Why This Design
- ## The Core Insight
- ## What the Map Does
- ## Design Principles
- ## Why These Choices
- ## Connection to Other Systems
- ## What the Map Is NOT
- ## Player Experience

**Sections:**
- # Map System — Sync: Current State
- ## Current State
- ## Documentation Status
- ## Summary Table
- ## ARCHIVE

**Sections:**
- # Phase 3: Historical Events — Algorithm
- ## Sources
- ## Output
- ## Key Events Timeline
- ## Script
- # scripts/scrape/phase3_events.py
- # Mostly manual curation from Chronicle
- # Script validates and links to places/characters
- # Link to our place IDs
- # Link to our character IDs
- # Validate dates
- ## The Harrying (Critical Context)
- ## Event Categories
- ## Verification

**Sections:**
- # Phase 1: Geography — Algorithm
- ## Sources
- ## Output
- ## Script
- # scripts/scrape/phase1_geography.py
- # 1. Get Domesday settlements
- # 2. Enrich with coordinates
- # 3. Add Roman roads
- # 4. Compute travel times
- # 5. Output
- ## Travel Time Calculation
- ## Verification

**Sections:**
- # Phase 4: Narratives & Beliefs — Algorithm
- ## Sources
- ## Output
- ## Narrative Templates
- ## Belief Distribution Rules
- ## Narrative Types
- ## Verification

**Sections:**
- # Scraping Pipeline — Algorithm
- ## Overview
- ## Phases
- ## Data Sources
- ## Phase Dependencies
- ## Output Files

**Sections:**
- # Phase 2: Political Structure — Algorithm
- ## Sources
- ## Output
- ## Script
- # scripts/scrape/phase2_political.py
- # 1. Get Norman lords from Domesday
- # 2. Get their holdings
- # Map to our place IDs
- # 3. Get dispossessed Saxons (1066 holders)
- # 4. Cross-reference with Chronicle for 1067 state
- # (Manual curation needed - see phase2_manual.md)
- # 5. Output
- ## Key Historical Figures
- ## Faction Relationships
- ## Verification

**Sections:**
- # Phase 5: Tensions — Algorithm
- ## Sources
- ## Output
- ## Tension Templates
- ## Pressure Types
- ## Breaking Points
- ## Initial Pressure Distribution
- ## Verification

**Sections:**
- # World Scraping — Behaviors
- ## CHAIN

**Sections:**
- # World Scraping — Design Patterns
- ## Core Principle
- ## Pattern: Authentic England 1067
- ## Behaviors: What The Player Experiences
- ## Target Density
- ## Related Documents

**Sections:**
- # World Scraping — State & Progress
- ## Phase Status
- ## Current Counts (YAML)
- ## New Content: Characters
- ## New Content: Tensions
- ## Narrative Breakdown (Updated)
- ## Data Sources
- ## Blockers Resolved
- ## Optional Expansion
- ## ARCHIVE

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
- `ClickableText.tsx`
- `MomentDebugPanel.tsx`
- `MomentDisplay.tsx`
- `MomentStream.tsx`
- `__init__.py`
- `api/app.py`
- `api/moments.py`
- `base.py`
- `canon/holder.py`
- `check_health.py`
- `check_injection.py`
- `companion.py`
- `engine/api/app.py`
- `engine/api/moments.py`
- `engine/canon/holder.py`
- `engine/db/__init__.py`
- `engine/db/graph_ops.py`
- `engine/db/graph_queries.py`
- `engine/embeddings/service.py`
- `engine/history/conversations.py`
- `engine/history/service.py`
- `engine/init_db.py`
- `engine/memory/moment_processor.py`
- `engine/models/base.py`
- `engine/models/links.py`
- `engine/models/nodes.py`
- `engine/models/tensions.py`
- `engine/moment_graph/__init__.py`
- `engine/moment_graph/api_models.py`
- `engine/moment_graph/queries.py`
- `engine/moment_graph/surface.py`
- `engine/moment_graph/traversal.py`
- `engine/orchestration/narrator.py`
- `engine/orchestration/opening.py`
- `engine/orchestration/orchestrator.py`
- `engine/orchestration/speed.py`
- `engine/orchestration/world_runner.py`
- `engine/physics/constants.py`
- `engine/physics/energy.py`
- `engine/physics/graph_tick.py`
- `engine/physics/tick.py`
- `engine/queries/semantic.py`
- `engine/run.py`
- `engine/scripts/check_injection.py`
- `engine/scripts/generate_images_for_existing.py`
- `engine/scripts/inject_to_narrator.py`
- `engine/scripts/seed_moment_sample.py`
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
- `frontend/app/map/page.tsx`
- `frontend/app/page.ts`
- `frontend/app/page.tsx`
- `frontend/app/scenarios/page.tsx`
- `frontend/app/start/page.tsx`
- `frontend/components/GameClient.tsx`
- `frontend/components/GameLayout.tsx`
- `frontend/components/Providers.tsx`
- `frontend/components/chronicle/ChroniclePanel.tsx`
- `frontend/components/debug/DebugPanel.tsx`
- `frontend/components/map/FogOfWar.tsx`
- `frontend/components/map/MapCanvas.tsx`
- `frontend/components/map/MapClient.tsx`
- `frontend/components/map/MapView.tsx`
- `frontend/components/map/PlayerToken.tsx`
- `frontend/components/minimap/Minimap.tsx`
- `frontend/components/moment/ClickableText.tsx`
- `frontend/components/moment/MomentDebugPanel.tsx`
- `frontend/components/moment/MomentDisplay.tsx`
- `frontend/components/moment/MomentStream.tsx`
- `frontend/components/panel/ChronicleTab.tsx`
- `frontend/components/panel/ConversationsTab.tsx`
- `frontend/components/panel/LedgerTab.tsx`
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
- `frontend/lib/api.ts`
- `frontend/lib/map/projection.ts`
- `frontend/lib/map/random.ts`
- `frontend/types/game.ts`
- `frontend/types/moment.ts`
- `generate_images_for_existing.py`
- `graph_ops.py`
- `graph_queries.py`
- `handlers/__init__.py`
- `handlers/base.py`
- `handlers/companion.py`
- `lint_terminology.py`
- `moment_graph/queries.py`
- `moment_graph/traversal.py`
- `narrator.py`
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
- `run.py`
- `scripts/check_chain.py`
- `stream_dialogue.py`
- `test_behaviors.py`
- `test_history.py`
- `test_implementation.py`
- `test_integration_scenarios.py`
- `test_models.py`
- `test_moment.py`
- `test_schema.py`
- `test_spec_consistency.py`
- `tests/api/test_health.py`
- `tests/async/test_hook_injection.py`
- `tests/async/test_runner_protocol.py`
- `tests/async/test_sse_queue.py`
- `tests/tools/test_generate_image.py`
- `tests/tools/test_graphops_images.py`
- `tests/tools/test_retry_policy.py`
- `tests/world/test_narratives.py`
- `tests/world/test_pipeline.py`
- `tests/world/test_positions.py`
- `tests/world/test_routes.py`
- `tools/image_generation/generate_image.py`
- `tools/stream_dialogue.py`
- `world_runner.py`

**Doc refs:**
- `agents/developer/CLAUDE.md`
- `agents/narrator/CLAUDE.md`
- `agents/world_runner/CLAUDE.md`
- `data/init/BLOOD_LEDGER_DESIGN_DOCUMENT.md`
- `docs/agents/narrator/ALGORITHM_Prompt_Structure.md`
- `docs/agents/narrator/ALGORITHM_Rolling_Window.md`
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md`
- `docs/agents/narrator/ALGORITHM_Thread.md`
- `docs/agents/narrator/BEHAVIORS_Narrator.md`
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md`
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
- `docs/agents/narrator/TOOL_REFERENCE.md`
- `docs/design/ALGORITHM_Vision.md`
- `docs/design/BEHAVIORS_Vision.md`
- `docs/design/PATTERNS_Vision.md`
- `docs/design/SYNC_Vision.md`
- `docs/design/TEST_Vision.md`
- `docs/design/VALIDATION_Vision.md`
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
- `docs/engine/moments/SCHEMA_Moments.md`
- `docs/engine/scene_memory/ALGORITHM_Scene_Memory.md`
- `docs/engine/scene_memory/BEHAVIORS_Scene_Memory.md`
- `docs/engine/scene_memory/PATTERNS_Scene_Memory.md`
- `docs/engine/scene_memory/SYNC_Scene_Memory.md`
- `docs/engine/scene_memory/VALIDATION_Scene_Memory.md`
- `docs/frontend/PATTERNS_Presentation_Layer.md`
- `docs/frontend/SYNC_Frontend.md`
- `docs/frontend/scene/ALGORITHM_Scene.md`
- `docs/frontend/scene/BEHAVIORS_Scene.md`
- `docs/frontend/scene/PATTERNS_Scene.md`
- `docs/frontend/scene/SYNC_Scene.md`
- `docs/frontend/scene/TEST_Scene.md`
- `docs/frontend/scene/VALIDATION_Scene.md`
- `docs/history/PATTERNS_History.md`
- `docs/infrastructure/async/ALGORITHM_Discussion_Trees.md`
- `docs/infrastructure/async/ALGORITHM_Fog_Of_War.md`
- `docs/infrastructure/async/ALGORITHM_Graph_SSE.md`
- `docs/infrastructure/async/ALGORITHM_Hook_Injection.md`
- `docs/infrastructure/async/ALGORITHM_Image_Generation.md`
- `docs/infrastructure/async/ALGORITHM_Runner_Protocol.md`
- `docs/infrastructure/async/ALGORITHM_Waypoint_Creation.md`
- `docs/infrastructure/async/BEHAVIORS_Travel_Experience.md`
- `docs/infrastructure/async/PATTERNS_Async_Architecture.md`
- `docs/infrastructure/async/SYNC_Async_Architecture.md`
- `docs/infrastructure/embeddings/ALGORITHM_Embeddings.md`
- `docs/infrastructure/embeddings/BEHAVIORS_Embeddings.md`
- `docs/infrastructure/embeddings/PATTERNS_Embeddings.md`
- `docs/infrastructure/embeddings/SYNC_Embeddings.md`
- `docs/infrastructure/embeddings/TEST_Embeddings.md`
- `docs/infrastructure/embeddings/VALIDATION_Embeddings.md`
- `docs/infrastructure/history/ALGORITHM_History.md`
- `docs/infrastructure/history/BEHAVIORS_History.md`
- `docs/infrastructure/history/PATTERNS_History.md`
- `docs/infrastructure/history/SYNC_History.md`
- `docs/infrastructure/history/TEST_History.md`
- `docs/infrastructure/history/VALIDATION_History.md`
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
- `docs/world/scraping/PATTERNS_World_Scraping.md`
- `docs/world/scraping/SYNC_World_Scraping.md`
- `docs/world/scraping/VALIDATION_World_Scraping.md`
- `engine/history/README.md`
- `graph/VALIDATION.md`
- `physics/graph/health/README.md`
- `tools/image_generation/README.md`

**Sections:**
- # Repository Map: the-blood-ledger

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
- `class PlaythroughCreateRequest`
- `def _opening_to_scene_tree()`
- `def build_beat_narration()`
- `async def create_playthrough()`
- `class MomentRequest`
- `async def send_moment()`
- `async def get_discussion_topics()`
- `async def get_discussion_topic()`
- `async def use_discussion_branch()`
- `def _count_branches()`
- `def count_clickables()`
- `def _delete_branch()`

**Definitions:**
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
- `def broadcast_moment_event()`
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
- `async def get_discussion_topics()`
- `async def get_discussion_topic()`
- `async def use_discussion_branch()`

**Definitions:**
- `def get_playthrough_graph_name()`

**Definitions:**
- `def _get_image_path()`
- `def _generate_node_image_async()`
- `def _generate_node_image()`
- `def add_mutation_listener()`
- `def remove_mutation_listener()`
- `def _emit_event()`
- `class WriteError`
- `def __init__()`
- `class SimilarNode`
- `def __str__()`
- `class ApplyResult`
- `def success()`
- `def has_duplicates()`
- `class GraphOps`
- `def __init__()`
- `def _query()`
- `def _cosine_similarity()`
- `def _find_similar_nodes()`
- `def check_duplicate()`
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
- `def add_character()`
- `def add_place()`
- `def add_thing()`
- `def add_narrative()`
- `def add_tension()`
- `def add_moment()`
- `def add_said()`
- `def add_moment_at()`
- `def add_moment_then()`
- `def add_narrative_from_moment()`
- `def add_can_speak()`
- `def add_attached_to()`
- `def add_can_lead_to()`
- `def handle_click()`
- `def update_moment_weight()`
- `def propagate_embedding_energy()`
- `def _get_current_tick()`
- `def decay_moments()`
- `def on_player_leaves_location()`
- `def on_player_arrives_location()`
- `def garbage_collect_moments()`
- `def boost_moment_weight()`
- `def add_belief()`
- `def add_narrative_link()`
- `def add_presence()`
- `def move_character()`
- `def add_possession()`
- `def add_thing_location()`
- `def add_geography()`
- `def apply_mutations()`
- `def get_graph()`

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
- `def search()`
- `def _to_markdown()`
- `def _cosine_similarity()`
- `def _find_similar_by_embedding()`
- `def _get_connected_cluster()`
- `def _extract_node_props()`
- `def _extract_link_props()`
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
- `def get_moment()`
- `def get_moments_at_place()`
- `def get_moments_by_character()`
- `def get_moments_in_tick_range()`
- `def get_moment_sequence()`
- `def get_narrative_moments()`
- `def get_narratives_from_moment()`
- `def search_moments()`
- `def _find_similar_by_embedding()`
- `def build_scene_context()`
- `def get_player_location()`
- `def get_current_view()`
- `def get_live_moments()`
- `def resolve_speaker()`
- `def get_available_transitions()`
- `def get_clickable_words()`
- `def view_to_scene_tree()`
- `def get_queries()`

**Docs:** `None yet (extracted during monolith split)`

**Definitions:**
- `def cosine_similarity()`
- `def extract_node_props()`
- `def extract_link_props()`
- `def to_markdown()`
- `def view_to_scene_tree()`

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

**Definitions:**
- `class Tension`
- `def has_flipped()`
- `def tick_gradual()`
- `def tick_scheduled()`
- `def add_event_pressure()`
- `def reset()`

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

**Definitions:**
- `class Moment`
- `def not_implemented()`

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
- `def _load_world_injection()`
- `def _save_world_injection()`
- `def _clear_world_injection()`

**Definitions:**
- `class WorldRunnerService`
- `def __init__()`
- `def process_flips()`
- `def _build_prompt()`
- `def _call_claude()`
- `def _fallback_response()`

**Definitions:**
- `def distance_to_proximity()`

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

**Definitions:**
- `def create_character_prompt()`
- `def create_place_prompt()`
- `def main()`

**Definitions:**
- `def is_narrator_running()`
- `def inject_via_queue()`
- `def inject_via_direct_call()`
- `def inject()`
- `def main()`

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

**Definitions:**
- `def create_indexes()`
- `def load_initial_state()`
- `def verify_data()`
- `def main()`

**Definitions:**
- `def main()`

**Definitions:**
- `handleBegin()`

**Definitions:**
- `rollRandomName()`
- `handleBegin()`

**Definitions:**
- `ChroniclePanel()`
- `handleSubmit()`
- `handleKeyDown()`

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

**Definitions:**
- `MapClient()`
- `updateDimensions()`

**Definitions:**
- `Minimap()`

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

**Definitions:**
- `SceneView()`

**Definitions:**
- `SettingStrip()`

**Definitions:**
- `showToast()`
- `useToast()`
- `ToastProvider()`
- `ToastItem()`

**Definitions:**
- `Voices()`

**Definitions:**
- `GameClient()`
- `handleAction()`

**Definitions:**
- `GameLayout()`

**Definitions:**
- `useGameState()`
- `mapPlaceType()`
- `transformScene()`
- `clickables()`
- `transformVoices()`
- `transformViewToScene()`
- `transformMomentsToVoices()`
- `createFallbackScene()`

**Definitions:**
- `useMoments()`

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

**Definitions:**
- `seededRandom()`
- `hashString()`

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

**Sections:**
- # Discussion Tree Generator
- ## Input
- ## Output
- ## Format
- ## Guidelines
- ## Topic Categories
- ## Example
- ## Invocation

**Sections:**
- # Image Generation Tool
- ## Setup
- ## Usage
- ## Image Types
- ## Examples
- ## Options
- ## Output
- ## Style

**Definitions:**
- `def generate_image()`
- `def main()`

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

**Code refs:**
- `run.py`
- `test_history.py`

**Sections:**
- # Repository Guidelines
- ## Project Structure & Module Organization
- ## Build, Test, and Development Commands
- ## Coding Style & Naming Conventions
- ## Testing Guidelines
- ## Commit & Pull Request Guidelines

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

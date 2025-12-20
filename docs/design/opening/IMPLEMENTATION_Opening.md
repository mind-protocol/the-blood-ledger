# The Opening — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Opening.md
BEHAVIORS:      ./BEHAVIORS_Opening.md
ALGORITHM:      ./ALGORITHM_Opening.md
VALIDATION:     ./VALIDATION_Opening.md
THIS:           IMPLEMENTATION_Opening.md (you are here)
HEALTH:         ./HEALTH_Opening.md
SYNC:           ./SYNC_Opening.md

IMPL:           engine/infrastructure/api/playthroughs.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/api/
├── playthroughs.py          # Exports create_playthrough endpoint
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/api/playthroughs.py` | Playthrough creation and opening handling | `create_playthrough`, `_opening_to_scene_tree` | ~450 | WATCH |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

> When a file reaches WATCH status, identify extraction candidates in the GAPS section below.
> When a file reaches SPLIT status, splitting becomes the next task before any feature work.

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Pipeline / Template Method

**Why this pattern:** The opening sequence is a deterministic transformation of a static template (`opening.json`) combined with dynamic scenario data. It follows a strict sequence: Load -> Transform -> Persist.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Template Method | `_opening_to_scene_tree` | Defines the skeleton of the scene tree generation, letting the `opening.json` provide the specific steps. |
| Recursion | `build_beat_narration` | Handles the nested structure of beats and questions (chains of "then"). |

### Anti-Patterns to Avoid

- **Hardcoded Strings**: Avoid embedding narration text in Python code. Use `opening.json` or `CONTENT.md`.
- **Dynamic Question Generation**: Do not generate questions at runtime via LLM for the opening. The sequence must be deterministic to establish the companion's voice correctly.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Opening Module | Template processing, SceneTree generation | Graph state, Player input | `create_playthrough`, `scene.json` |

---

## SCHEMA

### Opening Template (`opening.json`)

```yaml
OpeningTemplate:
  required:
    - setting: {location, time, characters}
    - beats: List[Beat]
```

### Beat

```yaml
Beat:
  required:
    - narration: List[str]
    - questions: List[Question]
```

### Question

```yaml
Question:
  required:
    - text: str
    - type: str (question|statement)
  optional:
    - speaker: str
    - transition: str
```

### SceneTree (Output)

```yaml
SceneTree:
  required:
    - id: str
    - location: {place, name, region, time}
    - narration: List[NarrationNode]
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `create_playthrough` | `engine/infrastructure/api/playthroughs.py:192` | `POST /api/playthrough/create` or `/api/playthrough/scenario` |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Flow 1: Playthrough Initialization & Opening Generation

Creates the playthrough context and generates the initial scene state.

```yaml
flow:
  name: initialization_and_opening
  purpose: Bootstrap a new playthrough with graph state and initial UI payload.
  scope: User Request -> Filesystem & Graph -> API Response
  steps:
    - id: step_1
      description: Generate playthrough ID and filesystem structure.
      file: engine/infrastructure/api/playthroughs.py
      function: create_playthrough
      input: PlaythroughCreateRequest
      output: Playthrough ID & Dir
      trigger: API Call
      side_effects: creates directories, writes player.yaml, initializes queue files
    - id: step_2
      description: Seed a new graph for the playthrough with base world data.
      file: engine/infrastructure/api/playthroughs.py
      function: create_playthrough (calls engine.init_db.load_initial_state)
      input: Seed data from data/world/ and engine/data/init/initial_state.yaml
      output: Base graph in FalkorDB (graph name == playthrough_id)
      trigger: step_1
      side_effects: writes nodes/links to FalkorDB
    - id: step_3
      description: Load and inject scenario into the graph.
      file: engine/infrastructure/api/playthroughs.py
      function: create_playthrough (calls GraphOps.apply)
      input: Scenario YAML (nodes + links)
      output: Graph Mutation Result
      trigger: step_2
      side_effects: writes nodes/links to FalkorDB
    - id: step_4
      description: Create opening moments in the graph and attach to location.
      file: engine/infrastructure/api/playthroughs.py
      function: create_playthrough (calls GraphOps.add_moment)
      input: Scenario Opening Narration
      output: Moment IDs
      trigger: step_3
      side_effects: writes moments + THEN/ATTACHED_TO links to FalkorDB
    - id: step_5
      description: Generate SceneTree from opening template and write scene.json.
      file: engine/infrastructure/api/playthroughs.py
      function: _opening_to_scene_tree
      input: opening.json, Scenario Data
      output: SceneTree Dict
      trigger: step_4
      side_effects: writes scene.json
    - id: step_6
      description: Return playthrough payload to the client.
      file: engine/infrastructure/api/playthroughs.py
      function: create_playthrough
      input: SceneTree Dict
      output: HTTP response {status, playthrough_id, scenario, scene}
      trigger: step_5
      side_effects: none
  docking_points:
    guidance:
      include_when: significant, risky, complex, transformative
      omit_when: trivial pass-through, redundant, low-impact
      selection_notes: select points where state is persisted or transformed significantly.
    available:
      - id: seed_graph
        type: graph_ops
        direction: output
        file: engine/infrastructure/api/playthroughs.py
        function: create_playthrough
        trigger: step_2
        payload: Base world seed data
        async_hook: not_applicable
        needs: none
        notes: Establishes baseline world state before scenario injection.
      - id: scenario_injection
        type: graph_ops
        direction: output
        file: engine/infrastructure/api/playthroughs.py
        function: create_playthrough
        trigger: step_2
        payload: Scenario Data
        async_hook: not_applicable
        needs: none
        notes: Critical for world state.
      - id: scene_generation
        type: file
        direction: output
        file: engine/infrastructure/api/playthroughs.py
        function: create_playthrough
        trigger: step_4
        payload: SceneTree
        async_hook: not_applicable
        needs: none
        notes: Determines initial user experience.
    health_recommended:
      - dock_id: seed_graph
        reason: Ensures the playthrough graph is created with base world data.
      - dock_id: scenario_injection
        reason: Verifies the graph is seeded correctly.
      - dock_id: scene_generation
        reason: Verifies the frontend has a valid starting state.
```

---

## LOGIC CHAINS

### LC1: Opening Scene Construction

**Purpose:** Transform static template into dynamic SceneTree.

```
{opening.json, scenario_data}
  → _opening_to_scene_tree()
    → build_beat_narration(0)
      → build_beat_narration(1) ... (Recursion)
    → {SceneTree}
```

**Data transformation:**
- Input: `Template Dict`, `Scenario Dict` — Raw configuration.
- Process: Merges companion ID, iterates beats, chains questions via `then` property.
- Output: `SceneTree Dict` — Recursive structure ready for frontend/narrator.

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/api/playthroughs.py
    └── imports → engine/physics/graph/graph_ops.py
    └── imports → engine/physics/graph/graph_queries.py
    └── imports → engine/init_db.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `yaml` | Parsing scenario/player files | `playthroughs.py` |
| `pydantic` | Request validation | `playthroughs.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Playthrough Config | `playthroughs/{id}/player.yaml` | File | Created at start, immutable |
| Current Scene | `playthroughs/{id}/scene.json` | File | Mutable, updates per action |
| Graph State | FalkorDB | Database | Persistent, mutable |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| API Endpoints | Async | Handled by FastAPI/Uvicorn |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `DEFAULT_PLAYTHROUGH` | `frontend/hooks/useGameState.ts` | 'beorn' | Dev default playthrough (`playthroughs/beorn`) that keeps SSE active for the demo. |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/api/playthroughs.py` | 1 | `# DOCS: docs/design/opening/IMPLEMENTATION_Opening.md` (Needs update) |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM Primary Flow | `create_playthrough` |
| ALGORITHM _opening_to_scene_tree | `_opening_to_scene_tree` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `engine/infrastructure/api/playthroughs.py` | ~450L | <400L | `engine/infrastructure/opening/generator.py` | Opening generation logic (`_opening_to_scene_tree`, `build_beat_narration`) |

### Missing Implementation

- [ ] `CONTENT.md` alignment check.
- [ ] Explicit error handling for malformed `opening.json`.

### Questions

- QUESTION: Should `opening.json` be localized per scenario, or is one template truly sufficient?

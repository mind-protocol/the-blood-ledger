# Physics — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2024-12-18
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
ALGORITHM:      ./ALGORITHM_Physics.md
VALIDATION:     ./VALIDATION_Physics.md
THIS:           IMPLEMENTATION_Physics.md
HEALTH:         ./HEALTH_Physics.md
SYNC:           ./SYNC_Physics.md

IMPL:           engine/physics/tick.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/
├── physics/
│   ├── __init__.py          # Exports GraphTick, TickResult
│   ├── tick.py              # Physics tick loop (Energy, Flips)
│   ├── constants.py         # Energy/decay constants
│   └── graph/               # Graph database operations
│       ├── __init__.py
│       ├── graph_queries.py # Read operations
│       ├── graph_ops.py     # Write operations (Facade)
│       └── ...              # Mixins (links, moments, types)
├── moment_graph/
│   ├── __init__.py          # Exports MomentGraph facade
│   ├── queries.py           # Fast graph queries (<50ms)
│   └── traversal.py         # Click/wait traversal
└── models/
    ├── base.py              # Base model class
    ├── nodes.py             # Moment, Narrative, etc.
    └── links.py             # Link types
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/physics/tick.py` | Living world simulation | `GraphTick.run`, `_detect_flips` | ~450 | WATCH |
| `engine/physics/graph/graph_queries.py` | Graph read operations | `GraphQueries` | ~892 | SPLIT |
| `engine/physics/graph/graph_ops.py` | Graph write operations | `GraphOps` | ~792 | SPLIT |
| `engine/moment_graph/traversal.py` | Interaction traversal | `handle_click` | ~300 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Graph-first orchestration with a thin coordinator layer.

**Why this pattern:** Physics logic stays in the graph and tick loop while the orchestrator only sequences calls and never owns narrative state. This keeps storage authoritative and prevents split-brain behavior between runtime services and the graph.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Facade | `engine/physics/graph/graph_ops.py` | Provide a single, stable write entry point to graph mutations. |
| Mixins | `engine/physics/graph/graph_ops_*.py` | Keep domain-specific mutations isolated while composing them into GraphOps. |
| Observer | `engine/physics/graph/graph_ops_events.py` | Emit mutation events for downstream listeners. |
| Query/Command split | `engine/physics/graph/graph_queries.py` vs `graph_ops.py` | Separate read paths from write paths. |

### Anti-Patterns to Avoid

- **Stateful orchestration**: Avoid caching graph state in orchestrator memory -> always query the graph.
- **Hidden writes in queries**: Keep writes in graph_ops so effects stay explicit.

---

## SCHEMA

### Moment (Node)

```yaml
Moment:
  required:
    - id: str                    # {place}_{day}_{time}_{type}_{timestamp}
    - text: str                  # The actual content
    - type: MomentType           # narration | dialogue | action | thought | description
    - status: MomentStatus       # possible | active | spoken | dormant | decayed
    - weight: float              # 0.0-1.0
    - energy: float              # Current activation (0.0-5.0)
```

### Links

```yaml
BELIEVES:
  from: Character
  to: Narrative
  properties:
    - strength: float (0.0-1.0)
ATTACHED_TO:
  from: Moment
  to: Character | Narrative | Place | Thing
  properties:
    - presence_required: bool
    - strength: float (0.0-1.0)
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Physics tick | `engine/physics/tick.py:68` | Orchestrator / Scheduler |
| Click traversal | `engine/moment_graph/traversal.py:50` | Frontend interaction |
| Player input | `engine/infrastructure/api/moments.py:30` | User text entry |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Physics Tick Flow: Living World Metabolism

The core metabolism of the world. Energy flows from characters to narratives to moments, eventually triggering "flips" that become observable events.

```yaml
flow:
  name: physics_tick
  purpose: Propagate energy and detect narrative flips.
  scope: Character energy -> Narrative energy -> Moment weight -> Flip detection
  steps:
    - id: step_1_inject
      description: Characters pump energy into narratives they believe in.
      file: engine/physics/tick.py
      function: _flow_energy_to_narratives
      input: char_energies (Dict)
      output: narrative_energies (Dict)
      trigger: GraphTick.run
      side_effects: none
    - id: step_2_propagate
      description: Energy flows between narratives via RELATES_TO links.
      file: engine/physics/tick.py
      function: _propagate_energy
      input: narrative_energies (Dict)
      output: narrative_energies (Dict)
      trigger: GraphTick.run
      side_effects: none
    - id: step_3_detect
      description: Check if any tension/moment crosses breaking threshold.
      file: engine/physics/tick.py
      function: _detect_flips
      input: tensions (List)
      output: flips (List)
      trigger: GraphTick.run
      side_effects: none
  docking_points:
    guidance:
      include_when: energy crosses a boundary or flips are detected
    available:
      - id: tick_input
        type: custom
        direction: input
        file: engine/physics/tick.py
        function: run
        trigger: Orchestrator.tick
        payload: elapsed_minutes
        async_hook: not_applicable
        needs: none
        notes: Entry point for the physics metabolism
      - id: flip_output
        type: event
        direction: output
        file: engine/physics/tick.py
        function: run
        trigger: return flips
        payload: List[FlipResult]
        async_hook: required
        needs: none
        notes: Critical for narrator/handler triggering
    health_recommended:
      - dock_id: flip_output
        reason: Verification of narrative momentum and event generation.
```

---

## LOGIC CHAINS

### LC1: Flip Detection

**Purpose:** Determine when a moment should trigger a handler.

```
moment.weight (via narrative.energy)
  → engine/physics/tick.py:_detect_flips()    # Check against breaking_point
    → TickResult.flips                        # Surface to orchestrator
      → Orchestrator.dispatch()                # Trigger character handlers
```

**Data transformation:**
- Input: `float` (pressure/weight) — Current system state
- Threshold check: `pressure >= breaking_point`
- Output: `List[Dict]` — Metadata for event generation

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/orchestration/orchestrator.py
    └── imports → engine/physics/tick.py
    └── imports → engine/moment_graph/queries.py

engine/physics/tick.py
    └── imports → engine/physics/graph/graph_queries.py
    └── imports → engine/physics/graph/graph_ops.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `falkordb` | Graph database | `engine/physics/graph/graph_queries.py` |
| `pydantic` | Model validation | `engine/models/base.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Graph State | FalkorDB | Global | Persistent |
| Active Tensions | `Tension` Nodes | Graph | Transient to Persistent |
| Energy Levels | `energy` properties | Graph | Decays over time |

---

## RUNTIME BEHAVIOR

### Initialization

1. Connect to FalkorDB.
2. Load physics constants from `engine/physics/constants.py`.
3. Initialize `GraphTick` runner.

### Main Loop

1. `Orchestrator` receives elapsed time.
2. `GraphTick.run()` computes energy flow.
3. `_detect_flips()` identifies triggered events.
4. `Orchestrator` dispatches handlers for each flip.

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Physics Tick | Sync | Linear math operations on graph snapshots. |
| Handlers | Async | LLM calls run in parallel. |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `DECAY_RATE` | `engine/physics/constants.py` | 0.02 | Base energy decay per tick |
| `BELIEF_FLOW_RATE` | `engine/physics/constants.py` | 0.1 | Speed of character-to-narrative flow |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/physics/tick.py` | 1 | `# DOCS: docs/physics/PATTERNS_Physics.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM Step 1 (Pump) | `engine/physics/tick.py:_flow_energy_to_narratives` |
| ALGORITHM Step 2 (Decay) | `engine/physics/tick.py:_decay_energy` |
| BEHAVIOR B11 (The Snap) | `engine/infrastructure/orchestration/speed.py` (Planned) |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `engine/physics/graph/graph_queries.py` | ~892L | <400L | `graph_queries_narratives.py` | Narrative-specific queries |

### Missing Implementation

- [ ] Handler runtime integration for real-time response generation.
- [ ] Speed controller "The Snap" transition logic.

---

## RUNTIME PATTERNS (Infrastructure)

### Scene as Query
There is no scene object. "Scene" is a query result of `Character AT Place`.

### Time Passage
Conversations have opportunity cost. `advance_time(minutes)` is called on every spoken moment, triggering physics ticks.

### Character Movement
Travel is a `Moment` with an `action: travel` field. Processing this updates the `AT` link in the graph.
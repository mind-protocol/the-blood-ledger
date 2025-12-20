# World Runner — Implementation: Service Architecture and Boundaries

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_World_Runner.md
BEHAVIORS:      ./BEHAVIORS_World_Runner.md
ALGORITHM:      ./ALGORITHM_World_Runner.md
VALIDATION:     ./VALIDATION_World_Runner_Invariants.md
THIS:           IMPLEMENTATION_World_Runner_Service_Architecture.md
HEALTH:         ./HEALTH_World_Runner.md
SYNC:           ./SYNC_World_Runner.md

IMPL:           engine/infrastructure/orchestration/world_runner.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
agents/
└── world_runner/
    └── CLAUDE.md                       # World Runner agent prompt/instructions

engine/
└── infrastructure/
    └── orchestration/
        ├── __init__.py                 # Exports WorldRunnerService
        └── world_runner.py             # CLI adapter for World Runner agent
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `agents/world_runner/CLAUDE.md` | Agent instructions and output contract | — | ~650 | WATCH |
| `engine/infrastructure/orchestration/world_runner.py` | Build prompt, call agent CLI, parse JSON | `WorldRunnerService` | ~156 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Adapter + Service Wrapper.

**Why this pattern:** Isolates agent CLI interaction behind a stable interface, allowing the LLM boundary to be replaced or mocked without impacting the orchestrator.

---

## SCHEMA

### WorldRunnerOutput (JSON)

```yaml
WorldRunnerOutput:
  required:
    - thinking: string          # Agent's chain-of-thought
    - graph_mutations: object   # Updates for FalkorDB
    - world_injection: object   # Narrative events for the Narrator
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| process_flips | `world_runner.py:34` | Orchestrator._process_flips |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### World Evolution: Ticks → Flips → Agent Resolution

This flow handles the transition from detected tension flips in the graph to structured world changes and narrative injections.

```yaml
flow:
  name: world_evolution
  purpose: Resolve off-screen tension flips into concrete world changes.
  scope: Tick Result -> World Runner Agent -> Mutations & Injections
  steps:
    - id: step_1_prompt
      description: Assemble prompt from flips and graph context.
      file: engine/infrastructure/orchestration/world_runner.py
      function: _build_prompt
      input: flips (List), graph_context (Dict)
      output: prompt_string
      trigger: process_flips call
      side_effects: none
    - id: step_2_call
      description: Invoke agent CLI and capture stdout.
      file: engine/infrastructure/orchestration/world_runner.py
      function: _call_claude
      input: prompt_string
      output: json_response_string
      trigger: process_flips workflow
      side_effects: none
    - id: step_3_resolve
      description: Return structured output to Orchestrator.
      file: engine/infrastructure/orchestration/world_runner.py
      function: process_flips
      input: json_response_string
      output: WorldRunnerOutput (Dict)
      trigger: return value
      side_effects: none
  docking_points:
    guidance:
      include_when: world state is being transformed or agents are triggered
    available:
      - id: runner_input
        type: custom
        direction: input
        file: engine/infrastructure/orchestration/world_runner.py
        function: process_flips
        trigger: Orchestrator
        payload: PromptContext
        async_hook: optional
        needs: none
        notes: Context for world-state resolution
      - id: runner_output
        type: event
        direction: output
        file: engine/infrastructure/orchestration/world_runner.py
        function: _call_claude
        trigger: json.loads
        payload: WorldRunnerOutput
        async_hook: required
        needs: none
        notes: Results applied to graph and narrator queue
    health_recommended:
      - dock_id: runner_output
        reason: Verification of background story consistency and schema.
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/orchestration/orchestrator.py
    └── imports → WorldRunnerService
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| CLI Config | `WorldRunnerService` | instance | persistent for service life |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Agent Call | Sync/Subprocess | Blocks worker until agent returns or times out |
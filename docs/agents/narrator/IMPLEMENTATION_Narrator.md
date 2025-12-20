# Narrator — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2024-12-19
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
THIS:            IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            engine/infrastructure/orchestration/narrator.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
agents/narrator/
├── CLAUDE.md             # Core agent instructions (System Prompt)
├── .claude/              # Agent CLI state
└── ...
engine/infrastructure/orchestration/
├── narrator.py           # Python entry point and prompt builder
└── agent_cli.py          # CLI wrapper for agent invocation
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `agents/narrator/CLAUDE.md` | Authorial intelligence rules | N/A | ~400 | OK |
| `engine/infrastructure/orchestration/narrator.py` | Prompt construction and IO | `run_narrator` | ~300 | OK |
| `engine/infrastructure/orchestration/agent_cli.py` | Subprocess management | `run_agent` | ~200 | OK |

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Agent-as-a-Service with CLI integration.

**Why this pattern:** Decouples the authorial logic (prompt-driven) from the game engine (Python-driven). The CLI interface allows for thread persistence and easy testing.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Prompt Builder | `narrator.py` | Dynamically assembles context for the LLM. |
| Streaming | `stream_dialogue.py` | Delivers incremental output to the frontend via SSE. |

---

## SCHEMA

### Narrator Output (JSON)

```yaml
NarratorOutput:
  required:
    - scene: object            # New scene tree or updates
    - time_elapsed: int        # Game minutes passed
  optional:
    - mutations: list          # Graph updates to apply
    - voice_lines: list        # Audio assets to trigger
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Narrator Call | `narrator.py:50` | Orchestrator.process_action |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Scene Generation: Action → Narrator → Graph

This flow handles the transition from a player action to a newly authored scene, including any world-state changes (mutations).

```yaml
flow:
  name: scene_generation
  purpose: Author new story beats based on current graph state.
  scope: Action -> LLM -> Graph Mutations -> Scene Response
  steps:
    - id: step_1_context
      description: Orchestrator gathers graph context and world state.
      file: engine/infrastructure/orchestration/narrator.py
      function: build_prompt
      input: playthrough_id, player_action
      output: full_prompt_string
      trigger: run_narrator call
      side_effects: none
    - id: step_2_author
      description: Agent authors response using CLAUDE.md rules.
      file: agents/narrator/CLAUDE.md
      function: N/A (Agent Intelligence)
      input: prompt
      output: JSON payload
      trigger: subprocess call
      side_effects: none
    - id: step_3_apply
      description: Extract and apply graph mutations from output.
      file: engine/physics/graph/graph_ops.py
      function: apply_mutation
      input: mutation_list
      output: success_boolean
      trigger: narrator.py parsing
      side_effects: graph state changed
  docking_points:
    guidance:
      include_when: narrative intent becomes concrete data
    available:
      - id: narrator_input
        type: custom
        direction: input
        file: engine/infrastructure/orchestration/narrator.py
        function: run_narrator
        trigger: Orchestrator
        payload: PromptContext
        async_hook: optional
        needs: none
        notes: Context fed to the authorial intelligence
      - id: narrator_output
        type: custom
        direction: output
        file: engine/infrastructure/orchestration/narrator.py
        function: run_narrator
        trigger: return response
        payload: NarratorOutput
        async_hook: required
        needs: none
        notes: Raw output before filtering
    health_recommended:
      - dock_id: narrator_output
        reason: Verification of authorial coherence and schema adherence.
```

---

## LOGIC CHAINS

### LC1: Invention to Canon

**Purpose:** Ensure LLM inventions are persisted correctly.

```
Agent authored "fact"
  → narrator.py extracts mutations
    → graph_ops.py applies to FalkorDB
      → fact is now queryable by physics/other agents
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/orchestration/narrator.py
    ├── imports → engine/physics/graph
    └── imports → engine/moment_graph
```

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Thread History | `.claude/` | thread | per-playthrough session |

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Narrator CLI | Sync/Subprocess | Blocks worker thread during generation |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `AGENTS_MODEL` | env | `claude` | Model provider for narrator |
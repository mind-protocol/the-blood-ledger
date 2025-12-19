# World Runner — Implementation: Service Architecture and Boundaries

```
STATUS: STABLE
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_World_Runner.md
BEHAVIORS:      ./BEHAVIORS_World_Runner.md
ALGORITHM:      ./ALGORITHM_World_Runner.md
VALIDATION:     ./VALIDATION_World_Runner_Invariants.md
THIS:           IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:           ./TEST_World_Runner_Coverage.md
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
| `engine/infrastructure/orchestration/world_runner.py` | Build prompt, call Claude CLI, parse JSON | `WorldRunnerService` | ~156 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Adapter + Service Wrapper (within layered orchestration)

**Why this pattern:** The module isolates Claude CLI interaction behind a small service interface (`process_flips`), so orchestrator logic stays decoupled from prompt formatting, subprocess handling, and JSON parsing while keeping the LLM boundary replaceable.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Builder | `engine/infrastructure/orchestration/world_runner.py:_build_prompt` | Assemble structured prompt text from YAML fragments |
| Adapter | `engine/infrastructure/orchestration/world_runner.py:WorldRunnerService` | Wraps the external Claude CLI into a stable Python interface |
| Fail-safe fallback (Null Object) | `engine/infrastructure/orchestration/world_runner.py:_fallback_response` | Guarantees output shape even on failures |

### Anti-Patterns to Avoid

- **Prompt Sprawl**: Avoid embedding orchestration logic into `_build_prompt()`.
- **Prompt Duplication**: Keep the schema/prompt contract centralized in `agents/world_runner/CLAUDE.md`.
- **Hidden Exceptions**: Do not add silent failures without logging.
- **God Object**: Keep WorldRunnerService focused on I/O, not graph logic.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| World Runner Service | prompt build, CLI call, JSON parsing, fallback | graph tick detection, mutation application, injection storage | WorldRunnerService process_flips |
| Agent Contract | structure and guidance in `agents/world_runner/CLAUDE.md` | orchestration flow and graph data fetching | `WORLD RUNNER INSTRUCTION` sections |

---

## SCHEMA

### WorldRunnerOutput (Summary)

```yaml
WorldRunnerOutput:
  required:
    - thinking: string
    - graph_mutations: object
    - world_injection: object
  constraints:
    - JSON parseable
    - schema defined in docs/agents/world-runner/TOOL_REFERENCE.md
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| WorldRunnerService constructor | `engine/infrastructure/orchestration/world_runner.py:22` | Orchestrator startup |
| WorldRunnerService process_flips | `engine/infrastructure/orchestration/world_runner.py:32` | Orchestrator `_process_flips` |

---

## DATA FLOW

### Flip Resolution: Orchestrator to World Runner

```
┌─────────────────────────┐
│ Orchestrator._process_flips │
└──────────────┬──────────┘
               │ flips, graph_context, player_context
               ▼
┌─────────────────────────┐
│ WorldRunnerService process_flips │
│ world_runner.py          │
└──────────────┬──────────┘
               │ builds prompt
               ▼
┌─────────────────────────┐
│ WorldRunnerService._call_claude │
│ subprocess Claude CLI    │
└──────────────┬──────────┘
               │ JSON response
               ▼
┌─────────────────────────┐
│ Orchestrator             │
│ apply mutations + store injection │
└─────────────────────────┘
```

---

## LOGIC CHAINS

### LC1: Prompt Build → CLI Call → Parse

**Purpose:** Resolve flips through Claude CLI and return structured output.

```
flips/context
  → WorldRunnerService._build_prompt()
    → WorldRunnerService._call_claude()
      → json.loads(response)
        → WorldRunnerOutput dict
```

**Data transformation:**
- Input: `flips`, `graph_context`, `player_context`, `time_span`
- After step 1: `prompt` string
- After step 2: CLI `stdout`
- Output: parsed dict matching WorldRunnerOutput

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/orchestration/orchestrator.py
    └── imports → WorldRunnerService
agents/world_runner/CLAUDE.md
    └── prompt contract referenced by → engine/infrastructure/orchestration/world_runner.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `subprocess` | Calling Claude CLI | `engine/infrastructure/orchestration/world_runner.py` |
| `json` | Parse CLI output | `engine/infrastructure/orchestration/world_runner.py` |
| `yaml` | Serialize prompt sections | `engine/infrastructure/orchestration/world_runner.py` |
| `logging` | Service logging | `engine/infrastructure/orchestration/world_runner.py` |
| `pathlib` | Default working directory | `engine/infrastructure/orchestration/world_runner.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| `working_dir` | `WorldRunnerService` | instance | set on init, used per call |
| `timeout` | `WorldRunnerService` | instance | set on init, used per call |

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Orchestrator instantiates WorldRunnerService
2. working_dir and timeout stored
3. Logger emits initialization message
4. service ready to process flips
```

### Main Request Cycle

```
1. Orchestrator detects flips
2. process_flips() builds prompt
3. Claude CLI runs and returns JSON
4. JSON parsed or fallback returned
5. Orchestrator applies mutations + stores injection
```

### Shutdown

No explicit shutdown; subprocess calls are bounded by timeout.

---

## CONCURRENCY MODEL

Synchronous subprocess call with a timeout. Orchestrator call blocks until CLI returns or times out.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `working_dir` | WorldRunnerService constructor | `Path.cwd()` | Working directory for CLI invocation |
| `timeout` | WorldRunnerService constructor | `600` | CLI timeout in seconds |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/orchestration/world_runner.py` | 8 | `docs/agents/world-runner/PATTERNS_World_Runner.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| Prompt build | `engine/infrastructure/orchestration/world_runner.py:_build_prompt` |
| CLI call + fallback | `engine/infrastructure/orchestration/world_runner.py:_call_claude` |
| Output parsing | `engine/infrastructure/orchestration/world_runner.py:_call_claude` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `agents/world_runner/CLAUDE.md` | ~650L | <400L | Split prompt body into a new file (proposed) | Prompt body vs reference sections |

### Missing Implementation

- [ ] Dedicated unit tests for `WorldRunnerService` fallback behaviors.

### Questions

- QUESTION: Should the service stream output or remain batch-only?

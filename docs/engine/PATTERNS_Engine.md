# Engine — Patterns: Why This Architecture

```
STATUS: DRAFT
CREATED: 2024-12-17
```

---

## CHAIN

```
THIS:        PATTERNS_Engine.md (you are here)
BEHAVIORS:   ./BEHAVIORS_Engine.md
ALGORITHM:   ./ALGORITHM_Engine.md
TEST:        ./TEST_Engine.md
SYNC:        ./SYNC_Engine.md
IMPLEMENTATION: ../engine/
```

---

## The Problem

The Blood Ledger engine must coordinate FalkorDB graph access, narrative generation, world runners, and multiple UI services without duplicating state. Earlier scene-tree prototypes stored narrative state in JSON files, forcing manual synchronization, blocking streaming, and making history impossible to query.

---

## The Pattern

1. **Graph-First State** — Everything that matters (characters, tensions, "moments", history) lives in FalkorDB; files are treated as cached views.
2. **Orchestrator Agents** — FastAPI hosts a thin API surface that triggers orchestration pipelines (narrator, world runner, director). Each pipeline writes mutations through `engine/db/graph_ops.py` and reads via `engine/db/graph_queries.py`.
3. **Documentation Chains** — Every subsystem (moments, runner, map, etc.) keeps PATTERNS→BEHAVIORS→ALGORITHMS→VALIDATION docs inside `docs/engine/*`.
4. **Moment Graph Roadmap** — Phase documents inside `docs/engine/moments/` describe the staged migration away from scene.json toward query-driven moments.

---

## Principles

- **Single Source of Truth** — Graph schema updates happen once and propagate via docs + CLI tools.
- **LLM at the Edges** — The runtime avoids hot-path LLM calls; AI agents write mutations offline.
- **Stateful Documentation** — SYNC files capture open questions + blocked work before diving into implementation.
- **Testable Contracts** — API + orchestration logic cite their doc counterparts for verification.
```

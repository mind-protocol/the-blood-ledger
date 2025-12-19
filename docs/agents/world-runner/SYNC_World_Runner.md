# World Runner — Sync: Current State

```
LAST_UPDATED: 2025-12-19
STATUS: CANONICAL — fully implemented and documented
```

---

## Current State

**Module is complete.** The World Runner is an AI agent that processes tension flips (when narrative tension exceeds breaking point) and determines what happened in the world.

**Components:**
- `agents/world_runner/CLAUDE.md` — AI agent instructions (650 lines, comprehensive)
- `engine/infrastructure/orchestration/world_runner.py` — Python service that invokes the agent via Claude CLI
- Full documentation suite in `docs/agents/world-runner/`

**Design Summary:**
- Runner owns time, Narrator owns story
- Runner runs tick loop until interrupt or completion
- Returns Injection (structured data) for Narrator to weave into narrative
- Stateless — each call independent, graph IS the memory

---

## Documentation Status

| Doc | Purpose | Status |
|-----|---------|--------|
| `PATTERNS_World_Runner.md` | Why this shape | Current |
| `BEHAVIORS_World_Runner.md` | What it produces (Injection) | Current |
| `ALGORITHM_World_Runner.md` | How the tick loop works | Current |
| `VALIDATION_World_Runner_Invariants.md` | Invariants + failure behavior | Current |
| `IMPLEMENTATION_World_Runner_Service_Architecture.md` | Code architecture | Current |
| `TEST_World_Runner_Coverage.md` | Test coverage + gaps | Current |
| `TOOL_REFERENCE.md` | JSON schemas for LLM output | Current |
| `INPUT_REFERENCE.md` | What Runner receives | Current |
| `SYNC_World_Runner.md` | Current state | This file |

---

## Integration

**Called by:** Orchestrator (via WorldRunnerService) when tick detects flips
**Outputs to:** Graph mutations (YAML) + injection_queue.json (for Narrator)
**Depends on:** GraphQueries for context, GraphOps for applying mutations

---

## Notes

The INPUT_REFERENCE.md references `engine/orchestration/world_runner.py` but the correct path after restructure is `engine/infrastructure/orchestration/world_runner.py`. This is a minor doc drift but doesn't affect functionality.

## Updates

- Consolidated the graph tick vs narrative flip description into `docs/agents/world-runner/ALGORITHM_World_Runner.md`.
- Removed deprecated `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md` after consolidating its content into the canonical algorithm doc.
- Added VALIDATION, IMPLEMENTATION, and TEST docs to complete the documentation chain.
- Consolidated duplicate IMPLEMENTATION docs into `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` and removed `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service.md`.
- Noted the initialization logging step in the canonical implementation doc to match current service behavior.
- Updated the implementation doc to remove non-existent file references and point to the actual PATTERNS doc path.

---

*"The Runner runs the world. The Narrator tells the story. They meet at Injections."*

---

## CHAIN

PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
INPUTS:          ./INPUT_REFERENCE.md
TOOLS:           ./TOOL_REFERENCE.md
SYNC:            ./SYNC_World_Runner.md

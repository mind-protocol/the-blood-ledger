# World Runner — Sync: Current State

```
LAST_UPDATED: 2025-12-19
STATUS: CANONICAL — fully implemented and documented
```

---

## Current State

**Module is complete.** The World Runner is an AI agent that processes tension flips (when narrative tension exceeds breaking point) and determines what happened in the world.

**Components:**
- `agents/world_runner/CLAUDE.md` — AI agent instructions (651 lines, comprehensive)
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
| `ALGORITHM_Graph_Ticks.md` | Redirects to canonical algorithm doc | Deprecated |
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
- Replaced `docs/agents/world-runner/ALGORITHM_Graph_Ticks.md` with a reference to the canonical algorithm doc to remove duplication.

---

*"The Runner runs the world. The Narrator tells the story. They meet at Injections."*

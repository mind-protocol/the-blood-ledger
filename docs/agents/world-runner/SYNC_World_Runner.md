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
- `engine/infrastructure/orchestration/world_runner.py` — Python service that invokes the agent via the agent CLI (`AGENTS_MODEL`)
- Documentation suite in `docs/agents/world-runner/`

**Design Summary:**
- Runner owns time, Narrator owns story
- Runner runs tick loop until interrupt or completion
- Returns Injection (structured data) for Narrator to weave into narrative
- Stateless — each call independent, graph IS the memory

---

## Documentation Status

| Doc | Purpose | Status |
|-----|---------|--------|
| `PATTERNS_World_Runner.md` | Why this shape | Current (condensed) |
| `BEHAVIORS_World_Runner.md` | What it produces (Injection) | Current (condensed) |
| `ALGORITHM_World_Runner.md` | How the tick loop works | Current (condensed) |
| `VALIDATION_World_Runner_Invariants.md` | Invariants + failure behavior | Current |
| `IMPLEMENTATION_World_Runner_Service_Architecture.md` | Code architecture | Current |
| `TEST_World_Runner_Coverage.md` | Test coverage + gaps | Current |
| `TOOL_REFERENCE.md` | Output schema summary | Current (examples archived) |
| `INPUT_REFERENCE.md` | What Runner receives | Current (example archived) |
| `archive/SYNC_archive_2024-12.md` | Archived examples + JSON schema | Current |
| `SYNC_World_Runner.md` | Current state | This file |

---

## Integration

**Called by:** Orchestrator (via WorldRunnerService) when tick detects flips
**Outputs to:** Graph mutations (YAML) + injection_queue.json (for Narrator)
**Depends on:** GraphQueries for context, GraphOps for applying mutations

---

## Notes

- The INPUT_REFERENCE.md references `engine/infrastructure/orchestration/world_runner.py` (correct after restructure).
- Verbose examples and the full JSON schema are archived in `docs/agents/world-runner/archive/SYNC_archive_2024-12.md` to keep module docs under size limits.

---

## Updates

- Condensed PATTERNS/BEHAVIORS/ALGORITHM to remove duplicated interface examples.
- Moved verbose examples and JSON schema into `archive/SYNC_archive_2024-12.md`.
- Simplified TOOL_REFERENCE and INPUT_REFERENCE to keep current, high-signal content.

---

## Agent Observations

### Remarks
- The doc chain repeated large schema/examples across multiple files; consolidating references reduced redundancy.

### Suggestions
- [ ] Consider adding a short link in `agents/world_runner/CLAUDE.md` pointing to the archived full JSON schema if prompt usage needs it.

### Propositions
- Document a single canonical schema location (file or generated artifact) to avoid future duplication.

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

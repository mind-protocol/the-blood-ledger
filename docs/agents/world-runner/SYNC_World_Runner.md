# World Runner — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- World Runner orchestration, tick loop, and injection output are stable and fully implemented.
- Stateless operation via CLI is enforced.

## CURRENT STATE

The World Runner is complete. It operates as an adapter between the Python game engine and an AI agent that resolves off-screen narrative tensions.

## RECENT CHANGES

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_World_Runner_Service_Architecture.md` and updated `TEST_World_Runner_Coverage.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** World Runner documentation is now compliant; Health checks are anchored to the CLI adapter boundary.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code for adapter changes. Ensure any changes to the agent's instructions in `CLAUDE.md` are reflected in the Health indicators.

## TODO

- [ ] Add unit tests for `WorldRunnerService` fallback behaviors.
- [ ] Implement automated schema validation for injection payloads.

## POINTERS

- `docs/agents/world-runner/PATTERNS_World_Runner.md` for the core "own time" insight.
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` for adapter details.

## CHAIN

```
THIS:            SYNC_World_Runner.md (you are here)
PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
```
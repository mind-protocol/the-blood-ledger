# World Runner — Patterns: Why This Shape

```
CREATED: 2024-12-16
UPDATED: 2025-12-19
STATUS: Canonical
```

---

## The Core Insight

**The Runner owns time. The Narrator owns story.**

When the player takes a time-consuming action, the Narrator hands control to the Runner to advance the world. The Runner simulates time and detects player-affecting flips, then returns an Injection for the Narrator to write the moment or the summary.

---

## The Problem

Long actions need consistent world evolution without forcing the narrator to
simulate physics, travel, and tension decay. If the narrator handles both, it
either stalls on simulation detail or drifts from the canon graph.

---

## The Pattern

Delegate time advancement to a stateless runner that reads the graph, ticks
tensions until a player-facing flip or completion, and emits a structured
Injection for the narrator to render.

---

## Design Principles

1. **Time is a control flow boundary**
   - Runner owns elapsed time and tick cadence; narrator only reacts.

2. **Graph state is the source of truth**
   - Runner never invents state outside graph reads and validated mutations.

3. **Interrupts are explicit**
   - Player-facing flips must become an Injection, not a silent mutation.

4. **Stateless runs stay composable**
   - Each call is independent so retries and resumes are deterministic.

---

## Principles

- Prefer deterministic tick loops over ad-hoc narration-side time jumps.
- Keep runner output structured so narration is faithful and inspectable.
- Avoid simulating everything; only advance tensions that can flip meaning.

---

## Interrupt/Resume Pattern

```
NARRATOR                              RUNNER
   │                                     │
   │ long action                           │
   │─────────────────────────────────────► │
   │                                     │ runs tick loop
   │                                     │ flip affects player
   │         Injection (interrupted)     │
   │ ◄────────────────────────────────────
   │ writes scene + resolves             │
   │                                     │
   │ resume with remaining time          │
   │─────────────────────────────────────►│
   │                                     │ runs to completion
   │         Injection (completed)       │
   │ ◄────────────────────────────────────
```

**Key rule:** Runner runs until interrupted OR completed. Narrator handles the interrupt, then resumes.

---

## Stateless Runner

The Runner does not keep memory between calls. The graph is the memory.

- Inputs: action, duration, player context, graph context
- Output: Injection + graph mutations already applied
- Next call reads updated graph and continues

---

## What the Runner Is Not

- **Not a full simulation:** It ticks only what matters for narratives under tension.
- **Not random events:** Events come from narrative tension, not dice rolls.
- **Not a time system:** Time is a trigger, not a physics engine.
- **Not the Narrator's boss:** Injection is information, not instruction.

---

## Player Impact Threshold

**Only flips that affect the player interrupt.** Everything else becomes world changes or news.

See `docs/agents/world-runner/ALGORITHM_World_Runner.md` for the `affects_player()` logic.

---

## Why Separation Matters

- **Focus:** Narrator writes scenes; Runner handles world evolution.
- **Continuity:** Offscreen changes happen consistently.
- **Clean interrupts:** Player-facing events become explicit moments.

---

## Dependencies

- `engine/infrastructure/orchestration/world_runner.py` for orchestration,
  injection assembly, and tick loop ownership.
- `engine/physics/graph/graph_ops.py` and `engine/physics/graph/graph_queries.py`
  for reading tensions and applying mutations.
- `agents/world_runner/CLAUDE.md` for runner instructions and output contract.

---

## Inspirations

- Narrative simulation systems that separate world ticks from authored prose,
  keeping chronology stable while narration stays expressive.
- GM-style adjudication loops where time advances offscreen until a trigger
  demands a player-facing interruption.

---

## Scope

In scope: tick orchestration, flip detection, mutation emission, and structured
Injection output. Out of scope: narrator prose, frontend rendering, and
non-tension simulation (combat physics, economy, etc.).

---

## Gaps / Ideas / Questions

- Should the runner expose a trace summary for debugging long actions?
- How should partial ticks be represented when resuming mid-action?
- What is the minimum Injection payload that still feels narratively grounded?

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

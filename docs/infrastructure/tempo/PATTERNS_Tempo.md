# Tempo Controller — Patterns: Speed-As-State-Machine

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against local tree
```

---

## CHAIN

```
THIS:            PATTERNS_Tempo.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Tempo.md
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
VALIDATION:      ./VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
HEALTH:          ./HEALTH_Tempo_Controller.md
TEST:            ./TEST_Tempo.md
SYNC:            ./SYNC_Tempo.md

IMPL:            engine/infrastructure/tempo/tempo_controller.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Tempo.md: "Docs updated, implementation needs: {what}"
3. Run tests: `pytest engine/tests/test_tempo.py` (once created)

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Tempo.md: "Implementation changed, docs need: {what}"
3. Run tests: `pytest engine/tests/test_tempo.py` (once created)

---

## THE PROBLEM

The game needs pacing without a "Next" button. Moments should surface at
different speeds (pause, real-time, fast travel, skip) without overwhelming the
frontend or bypassing physics + canon. Without a dedicated tempo layer:

- Physics ticks would be either too slow (boring) or too fast (spam).
- Surfacing would ignore player intent (pause vs fast-forward).
- Frontend would drown in updates without backpressure.
- Narrator output would be confused with surfacing logic.

---

## THE PATTERN

**A per-playthrough TempoController runs an async loop and acts as a speed state
machine.** It drives physics ticks, detects ready moments, and records them to
canon, while broadcasting speed changes to the frontend.

Key insight: **tempo is not content generation.** It is the pacing and surfacing
layer between physics and canon display.

---

## PRINCIPLES

### Principle 1: Speed Is A State Machine

Pause/1x/2x/3x are explicit states with consistent tick intervals and rules.
This keeps transitions deterministic and testable.

### Principle 2: Surfacing Is Decoupled From Generation

Narrator creates possible moments; tempo decides when they surface. This avoids
short-circuiting physics or canon rules.

### Principle 3: Backpressure Protects the Frontend

The controller slows in 1x when the display queue grows, so SSE streams do not
overwhelm the UI.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Physics runtime (ngram repo) | Runs `GraphTick` to advance simulation (see `data/ARCHITECTURE — Cybernetic Studio.md`) |
| GraphQueries (ngram repo) | Detect ready moments (see `data/ARCHITECTURE — Cybernetic Studio.md`) |
| `engine/infrastructure/canon/` | Records moments to canon + SSE |
| `engine/infrastructure/api/` | SSE broadcast + tempo endpoints |
| `frontend/components/SpeedControl.tsx` | User speed input + state display |

---

## INSPIRATIONS

- Real-time narrative games with speed controls (pause, fast travel).
- State-machine driven game loops with explicit pacing phases.

---

## SCOPE

### In Scope

- Speed state machine (pause/1x/2x/3x)
- Tick scheduling and backpressure
- Ready-moment detection and canon recording
- Speed change broadcast events
- Player input handling for pause/interrupt

### Out of Scope

- Content generation (narrator logic) → see `docs/agents/narrator/`
- Physics rules (energy flow, decay) → see `docs/physics/`
- UI display filtering + animations → frontend scene/chronicle modules
- Persistence of tempo state across sessions

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define a canonical spec for frontend display filtering at 2x/3x.
- [ ] Decide if tempo state should persist across reconnects.
- IDEA: Add optional metrics for tick latency and queue pressure.

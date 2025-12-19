# Physics — Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-19
```

## GAPS

- None.

## Recent Changes

### 2025-12-19: Completed physics behaviors template sections

- **What:** Filled BEHAVIORS, INPUTS/OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and
  GAPS/IDEAS/QUESTIONS sections in `docs/physics/BEHAVIORS_Physics.md`.
- **Why:** Resolve doc-template drift for the physics behaviors spec.
- **Files:** `docs/physics/BEHAVIORS_Physics.md`

### 2025-12-19: Completed physics tick energy flow for repair 13

- **What:** Normalized belief-based injection and enforced zero-sum propagation with supersedes drain, clamping to `MIN_WEIGHT`.
- **Why:** Close the incomplete-impl gap for physics tick energy flow and align with the documented algorithm.
- **Files:** `engine/physics/tick.py:300`, `engine/physics/tick.py:342`, `docs/physics/IMPLEMENTATION_Physics.md`

### 2025-12-19: Documented physics module mapping

- **What:** Added `modules.yaml` entry for `engine/physics/**` and linked `engine/physics/tick.py` to the physics doc chain.
- **Why:** Close the undocumented module gap and make `ngram context` resolve physics docs.
- **Files:** `modules.yaml`, `engine/physics/tick.py`

## CHAIN

```
THIS:            SYNC_Physics.md (you are here)
PATTERNS:        ./PATTERNS_Physics.md
BEHAVIORS:       ./BEHAVIORS_Physics.md
ALGORITHMS:      ./ALGORITHM_Physics.md (consolidated: energy, tick, canon, handlers, input, actions, QA, speed)
SCHEMA:         ../schema/SCHEMA_Moments.md
API:             ./API_Physics.md
VALIDATION:      ./VALIDATION_Physics.md
IMPLEMENTATION:  ./IMPLEMENTATION_Physics.md (+ Runtime Patterns from INFRASTRUCTURE.md)
TEST:            ./TEST_Physics.md, ../../engine/tests/test_moment_graph.py
IMPL (existing): ../../engine/physics/tick.py, ../../engine/physics/graph/
IMPL (planned):  ../../engine/handlers/, ../../engine/canon/, ../../engine/infrastructure/orchestration/speed.py
```

---

## Architecture Summary

**The graph is the only truth.**

| Component | Purpose | Status |
|-----------|---------|--------|
| Energy System | Characters pump, links route, decay drains | ALGORITHM_Physics.md (Energy Mechanics section) ✓ |
| Physics Tick | Pump, transfer, decay, detect flips | ALGORITHM_Physics.md (Physics Tick section) ✓ |
| Character Handlers | One handler per character, triggered on flip | ALGORITHM_Physics.md (Character Handlers section) ✓ |
| Flip Detection (M11) | Status progression, salience threshold | ALGORITHM_Physics.md (Energy Mechanics section) ✓ |
| Canon Holder (M12) | Record what becomes real, THEN links | ALGORITHM_Physics.md (Canon Holder section) ✓ |
| Agent Dispatch (M13) | Runner/Narrator/Citizen/Canon coordination | ALGORITHM_Physics.md (Energy Mechanics section) ✓ |
| Speed Controller | 1x/2x/3x display modes | ALGORITHM_Physics.md (Speed Controller section) ✓ |

---

## Open Questions

1. **LLM latency at 1x** — If handler takes 3-5s, is that acceptable? Pre-generation helps but may not cover all cases.

2. **Grouped character splitting** — When to split automatically vs. on direct address?

3. **Montage moment generation** — Same handlers or dedicated montage handler?

4. **Energy constants** — What values for PUMP_RATE, transfer factors, etc.? Need playtesting. See ALGORITHM_Physics.md (Energy Mechanics section).

5. **Question answerer priority** — When multiple questions queued, which first?

---

## Next Steps

1. ~~**Document Speed Controller section** — Speed controller with The Snap~~ ✓ DONE
2. ~~**Update VALIDATION_Physics.md** — Align with v2 invariants~~ ✓ DONE
3. ~~**Deprecate legacy files**~~ ✓ DONE
4. ~~**Update SCHEMA_Moments.md** — Add energy/weight fields~~ ✓ DONE
5. ~~**Consolidate algorithm docs into ALGORITHM_Physics.md** — Energy mechanics, conservation, link transfers~~ ✓ DONE
6. ~~**Remove TENSION node** — Tension is now computed, not stored~~ ✓ DONE
7. **Begin implementation** — Create handlers/, canon/, physics/energy.py

---

## Handoff Notes

For next session:

- v2 architecture is fully documented in ALGORITHM files
- **ALGORITHM_Physics.md** is the master document, containing:
  - **M1-M6**: Strength Mechanics (Activation, Evidence, Association, Source, Commitment, Intensity)
  - **M11**: Flip Detection — status progression, salience threshold, detection queries
  - **M12**: Canon Holder — record, link, time, trigger, strength, notify
  - **M13**: Agent Dispatch — Runner (world), Narrator (scene), Citizen (character), Canon Holder (record)
  - **Weight vs Energy**: All nodes have both weight (importance over time, slow) and energy (current activation, fast)
  - **Salience = weight × energy** — determines surfacing (threshold = 0.3)
  - Characters are batteries, narratives are circuits, moments spend energy on actualization
  - Links route energy (zero-sum), don't create it
  - Tension is computed from structure, not stored
  - **Energy IS proximity** — no separate proximity calculation
  - **Physical gating is link attributes** (presence_required, AT), not functions
  - Transfer types: T1-T6 (narrative links), T7 (CAN_LEAD_TO), T8 (CAN_SPEAK), T9 (ATTACHED_TO)

---

## Agent Observations

### Remarks
- `pytest engine/tests/test_behaviors.py -q` failed: missing `pytest_xprocess` (anchorpy plugin import).
- `ngram validate` still reports pre-existing doc gaps and broken CHAIN links (schema/tempo/world-builder).

### Suggestions
- [ ] Install `pytest_xprocess` (or disable the anchorpy pytest plugin) to run the physics behavior tests.

### Propositions
- None.

---


---

## ARCHIVE

Older content archived to: `SYNC_Physics_archive_2025-12.md`

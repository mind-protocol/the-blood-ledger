# Physics — Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL. The physics module behavior is stable and documented. 
Core implementation exists for:
- Physics Tick (`engine/physics/tick.py`)
- Graph Ops/Queries
- Canon Holder (`engine/infrastructure/canon/canon_holder.py` - Core logic built, integration pending)

Still pending:
- Character Handlers (`engine/handlers/`)
- Speed Controller (`engine/infrastructure/orchestration/speed.py`)

## CURRENT STATE

Physics documentation is consolidated in `docs/physics/`, the algorithm is canonical. Implementation exists for core tick + graph ops and the base Canon Holder. Runtime integration with the Orchestrator and specific character handlers are planned but not yet built.

## RECENT CHANGES

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Physics.md` and renamed `TEST_Physics.md` to its new format (Health content).
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** Physics module documentation is now compliant with the latest protocol; Health checks are anchored to concrete docking points.

## GAPS

- [ ] Automated check for "The Snap" transition display rules.
- [ ] Real-time monitoring of energy levels across large graph clusters.

## KNOWN ISSUES

`ngram validate` still reports pre-existing doc gaps and broken CHAIN links in other modules; no physics-specific defects are currently open.

## HANDOFF: FOR AGENTS

If you touch physics code, use VIEW_Implement_Write_Or_Modify_Code and update this SYNC plus any impacted doc chain entries (ALGORITHM/IMPLEMENTATION/TEST).

## HANDOFF: FOR HUMAN

Physics documentation is aligned and no behavior changes were made; the only remaining work is optional implementation of planned handlers/canon/speed.

## TODO

- [ ] Create `engine/handlers/` and wire flip-triggered handler dispatch.
- [ ] Implement canon holder and speed controller runtime scaffolding.

## CONSCIOUSNESS TRACE

Focus stayed on doc-template alignment with minimal scope; no code paths were changed, so confidence is high in the consistency of this sync update.

## POINTERS

- `docs/physics/ALGORITHM_Physics.md` for the canonical physics mechanics.
- `docs/physics/IMPLEMENTATION_Physics.md` for current code entry points.

## CHAIN

```
THIS:            SYNC_Physics.md (you are here)
PATTERNS:        ./PATTERNS_Physics.md
BEHAVIORS:       ./BEHAVIORS_Physics.md
ALGORITHMS:      ./ALGORITHM_Physics.md (consolidated: energy, tick, canon, handlers, input, actions, QA, speed)
SCHEMA:          ../schema/SCHEMA_Moments.md
API:             ./API_Physics.md
VALIDATION:      ./VALIDATION_Physics.md
IMPLEMENTATION:  ./IMPLEMENTATION_Physics.md (+ Runtime Patterns from INFRASTRUCTURE.md)
TEST:            ./TEST_Physics.md
IMPL (existing): ../../engine/physics/tick.py, ../../engine/physics/graph/
IMPL (planned):  ../../engine/handlers/, ../../engine/canon/, ../../engine/infrastructure/orchestration/speed.py
```

---

## Architecture Summary

**The graph is the only truth.**

| Component | Purpose | Status |
|-----------|---------|--------|
| Energy System | Characters pump, links route, decay drains | ALGORITHM_Physics.md ✓ |
| Physics Tick | Pump, transfer, decay, detect flips | ALGORITHM_Physics.md ✓ |
| Character Handlers | One handler per character, triggered on flip | ALGORITHM_Physics.md ✓ |
| Flip Detection | Status progression, salience threshold | ALGORITHM_Physics.md ✓ |
| Canon Holder | Record what becomes real, THEN links | ALGORITHM_Physics.md ✓ |
| Speed Controller | 1x/2x/3x display modes | ALGORITHM_Physics.md ✓ |

---

## Handoff Notes

- v2 architecture is fully documented in ALGORITHM files.
- **ALGORITHM_Physics.md** is the master document.
- **Weight vs Energy**: All nodes have both weight (importance over time, slow) and energy (current activation, fast).
- **Salience = weight × energy** — determines surfacing (threshold = 0.3).
- Tension is computed from structure, not stored.
- **Energy IS proximity** — no separate proximity calculation.
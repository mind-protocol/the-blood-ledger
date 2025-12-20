# Canon Holder — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- Canon recording logic (`record_to_canon`), speaker resolution, and history chaining are implemented and tested.
- Integration with the Orchestrator and SSE broadcast is live.

## CURRENT STATE

The Canon Holder is fully functional. It serves as the primary gatekeeper for the game's history, ensuring all spoken moments are correctly linked and broadcast.

## RECENT CHANGES

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Canon.md` and updated `TEST_Canon.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** Canon module documentation is now compliant; Health checks are anchored to the recording and broadcast flow.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code for recording logic changes. Ensure any new moment types are reflected in `speaker.py` and the Health indicators.

## TODO

- [ ] Implement `detect_and_surface()` for automated tick-based surfacing.
- [ ] Add property-based tests for THEN chain acyclicity.

## POINTERS

- `docs/infrastructure/canon/PATTERNS_Canon.md` for the "gatekeeper" philosophy.
- `engine/infrastructure/canon/canon_holder.py` for the core implementation.

## CHAIN

```
THIS:            SYNC_Canon.md (you are here)
PATTERNS:        ./PATTERNS_Canon.md
BEHAVIORS:       ./BEHAVIORS_Canon.md
ALGORITHM:       ./ALGORITHM_Canon_Holder.md
VALIDATION:      ./VALIDATION_Canon.md
IMPLEMENTATION:  ./IMPLEMENTATION_Canon.md
TEST:            ./TEST_Canon.md
```
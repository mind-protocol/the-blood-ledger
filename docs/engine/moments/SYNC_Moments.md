# Moments — Current State

```
STATUS: CANONICAL
UPDATED: 2024-12-18
```

---

## CHAIN

```
THIS:            SYNC_Moments.md (you are here)
PATTERNS:        ./PATTERNS_Moments.md
BEHAVIORS:       ./BEHAVIORS_Moments.md
ALGORITHMS:      ./ALGORITHM_Physics.md, ./ALGORITHM_Handlers.md, ./ALGORITHM_Canon.md
SCHEMA:          ./SCHEMA_Moments.md
API:             ./API_Moments.md
VALIDATION:      ./VALIDATION_Moments.md
TEST:            ./TEST_Moments.md, ../../engine/tests/test_moment_graph.py
IMPL:            ../../engine/physics/tick.py, ../../engine/handlers/, ../../engine/canon/
```

---

## Architecture Summary

**The graph is the only truth.**

| Component | Purpose | Status |
|-----------|---------|--------|
| Physics Tick | Inject, decay, propagate, detect flips | ALGORITHM_Physics.md ✓ |
| Character Handlers | One handler per character, triggered on flip | ALGORITHM_Handlers.md ✓ |
| Canon Holder | Record what becomes real, THEN links | ALGORITHM_Canon.md ✓ |
| Speed Controller | 1x/2x/3x display modes | ALGORITHM_Speed.md (planned) |

---

## Open Questions

1. **LLM latency at 1x** — If handler takes 3-5s, is that acceptable? Pre-generation helps but may not cover all cases.

2. **Grouped character splitting** — When to split automatically vs. on direct address?

3. **Montage moment generation** — Same handlers or dedicated montage handler?

4. **Energy injection constants** — What values for INJECTION_MULTIPLIER, etc.? Need playtesting.

5. **Question answerer priority** — When multiple questions queued, which first?

---

## Next Steps

1. **Create ALGORITHM_Speed.md** — Speed controller with The Snap
2. **Update VALIDATION_Moments.md** — Align with v2 invariants
3. **Update SCHEMA_Moments.md** — Add energy/weight fields
4. **Begin implementation** — Start with physics tick loop
5. **Deprecate legacy files** — ALGORITHM_View_Query.md, ALGORITHM_Transitions.md, ALGORITHM_Lifecycle.md

---

## Handoff Notes

For next session:

- v2 architecture is fully documented in ALGORITHM files
- PATTERNS and BEHAVIORS rewritten for energy-based physics
- TEST_Moments.md has trace scenarios ready for implementation
- Legacy files need review/merge
- Implementation is next phase

---

## Legacy Files (To Review)

| File | Status | Notes |
|------|--------|-------|
| ALGORITHM_View_Query.md | Review | May merge into Physics |
| ALGORITHM_Transitions.md | Review | May merge into Canon |
| ALGORITHM_Lifecycle.md | Review | May merge into Physics |
| ARCHITECTURE_Overview.md | Deprecated | Replaced by PATTERNS |
| PHASE_*.md | Deprecated | Historical reference only |

---

*"There is no scene. There is only the graph."*

---

## ARCHIVE

Older content archived to: `SYNC_Moments_archive_2025-12.md`

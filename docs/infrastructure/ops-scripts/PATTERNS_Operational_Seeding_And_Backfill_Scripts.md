# Ops Scripts — Patterns: Operational Seeding And Backfill Scripts

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:            PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
BEHAVIORS:       ./BEHAVIORS_Operational_Script_Runbooks.md
ALGORITHM:       ./ALGORITHM_Seeding_And_Backfill_Flows.md
VALIDATION:      ./VALIDATION_Operational_Script_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
TEST:            ./TEST_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md
IMPL:            engine/scripts/seed_moment_sample.py
```

---

## THE PROBLEM

The project needs repeatable, lightweight ways to seed sample data and backfill
missing assets without running the full game loop or building new admin
interfaces. These tasks are occasional but critical for validating pipelines
and keeping playthrough data coherent.

---

## THE PATTERN

Maintain a small set of standalone CLI scripts under `engine/scripts/` that call
into existing GraphOps and image-generation utilities. Each script is focused
on a single operational task and is safe to run in isolation, with explicit
CLI arguments for target graph, host, or playthrough scope.

---

## PRINCIPLES

### Principle 1: Script Entry Points Stay Thin

Scripts should be thin wrappers around existing engine utilities, so logic
lives in shared modules instead of being duplicated in ad-hoc entry points.

### Principle 2: Explicit Targeting

Every script accepts CLI arguments for graph/host/playthrough inputs to avoid
accidentally mutating the wrong data set.

### Principle 3: Safe Defaults And Visibility

Scripts surface dry-run or summary output where possible so operators can
confirm what changed without digging into the database.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `engine/physics/graph/graph_ops.py` | GraphOps entry point for applying YAML samples. |
| `tools/image_generation` | Image generator used by the backfill script. |
| `docs/infrastructure/async` | Injection scripts live in the same folder but are documented there. |

---

## WHAT THIS DOES NOT SOLVE

- Automated scheduling or orchestration for these scripts.
- Rollback or transaction safety beyond what GraphOps provides.
- Runtime safeguards beyond explicit CLI arguments.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide whether image backfill should always default to dry-run.
- [ ] Add a standard logging format for operational scripts.

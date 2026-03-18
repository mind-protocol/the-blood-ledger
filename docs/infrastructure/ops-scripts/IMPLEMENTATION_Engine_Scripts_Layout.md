# Ops Scripts — Implementation: Engine Scripts Layout

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
BEHAVIORS:       ./BEHAVIORS_Operational_Script_Runbooks.md
ALGORITHM:       ./ALGORITHM_Seeding_And_Backfill_Flows.md
VALIDATION:      ./VALIDATION_Operational_Script_Safety.md
THIS:            IMPLEMENTATION_Engine_Scripts_Layout.md
TEST:            ./TEST_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md
```

---

## FILES

| File | Role | Entry Point | Notes |
|------|------|-------------|-------|
| `engine/scripts/generate_images_for_existing.py` | Backfill missing node images | `main()` | Moved to ngram repo with graph runtime. |
| `engine/scripts/check_injection.py` | Injection queue hook reader | `main()` | Documented under `docs/infrastructure/async/`. |

---

## ENTRY POINTS

- `engine/scripts/generate_images_for_existing.py` (moved to ngram repo)
- `engine/scripts/check_injection.py`

## EXTERNAL SCRIPTS (NGAM REPO)

- seed_moment_sample (moved to ngram repo with graph runtime)
- inject_to_narrator (moved to ngram repo with graph runtime)

---

## DEPENDENCIES

- GraphOps runtime in ngram repo (see `data/ARCHITECTURE — Cybernetic Studio.md`).
- `tools/image_generation` for image generation helpers.
- FalkorDB connection settings for graph access.

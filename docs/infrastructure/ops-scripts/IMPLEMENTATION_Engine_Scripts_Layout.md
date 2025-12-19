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
| `engine/scripts/seed_moment_sample.py` | Seed sample moment YAML into FalkorDB | `main()` | Uses `engine/physics/graph/graph_ops.py` (`GraphOps`). |
| `engine/scripts/generate_images_for_existing.py` | Backfill missing node images | `main()` | Uses `engine/physics/graph/graph_ops.py` (`GraphOps`) + `engine/physics/graph/graph_ops_image.py`. |
| `engine/scripts/check_injection.py` | Injection queue hook reader | `main()` | Documented under `docs/infrastructure/async/`. |
| `engine/scripts/inject_to_narrator.py` | Manual injection CLI | `main()` | Documented under `docs/infrastructure/async/`. |

---

## ENTRY POINTS

- `engine/scripts/seed_moment_sample.py`
- `engine/scripts/generate_images_for_existing.py`

---

## DEPENDENCIES

- `engine/physics/graph/graph_ops.py` for GraphOps apply behavior.
- `tools/image_generation` for image generation helpers.
- FalkorDB connection settings for graph access.

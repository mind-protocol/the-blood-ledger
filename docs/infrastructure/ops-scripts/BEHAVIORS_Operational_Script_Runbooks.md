# Ops Scripts — Behaviors: Operational Script Runbooks

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
THIS:            BEHAVIORS_Operational_Script_Runbooks.md
ALGORITHM:       ./ALGORITHM_Seeding_And_Backfill_Flows.md
VALIDATION:      ./VALIDATION_Operational_Script_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
TEST:            ./TEST_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md
```

---

## EXPECTED BEHAVIOR

- `seed_moment_sample.py` loads a YAML sample and applies it to a target
  FalkorDB graph, printing a summary of persisted, duplicate, and error counts.
- `generate_images_for_existing.py` scans for Character/Place/Thing nodes
  missing `image_path`, composes prompts, and optionally generates images.
- Both scripts expose CLI arguments for host, port, and playthrough scope to
  avoid accidental writes to the wrong dataset.
- Injection-related scripts in the same folder are documented under
  `docs/infrastructure/async/` and should remain compatible with the async
  architecture runbooks.

---

## INPUTS

- YAML sample files for seeding (`data/samples/moment_sample.yaml` by default).
- FalkorDB host/port and graph name.
- Playthrough folder name for image output paths.

---

## OUTPUTS

- Console summaries of operations performed.
- Updated graph nodes (moments or image fields) when not running dry-run.
- Image files written by the image generation tooling.

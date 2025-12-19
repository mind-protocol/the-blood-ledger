# Ops Scripts — Algorithm: Seeding And Backfill Flows

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
BEHAVIORS:       ./BEHAVIORS_Operational_Script_Runbooks.md
THIS:            ALGORITHM_Seeding_And_Backfill_Flows.md
VALIDATION:      ./VALIDATION_Operational_Script_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
TEST:            ./TEST_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md
```

---

## SEED MOMENT SAMPLE

1. Parse CLI arguments (graph name, host, port, sample path, playthrough).
2. Resolve the sample file path relative to project root.
3. Fail fast if the sample file is missing.
4. Initialize GraphOps with the target graph connection.
5. Apply the YAML sample via GraphOps.
6. Print persisted, duplicate, and error counts.

---

## GENERATE IMAGES FOR EXISTING

1. Parse CLI arguments (playthrough, host, port, dry-run).
2. Connect to FalkorDB via GraphOps.
3. Query for Character nodes missing `image_path`.
4. Build prompts from node attributes and log a preview.
5. If not dry-run, write `image_prompt`, generate image, and persist `image_path`.
6. Repeat for Place nodes missing `image_path`.
7. Repeat for Thing nodes missing `image_path`.
8. Log completion summary.

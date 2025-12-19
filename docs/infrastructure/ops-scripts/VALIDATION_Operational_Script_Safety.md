# Ops Scripts — Validation: Operational Script Safety

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
THIS:            VALIDATION_Operational_Script_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
TEST:            ./TEST_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md
```

---

## INVARIANTS

- Seed script must exit if the sample YAML file does not exist.
- Seeding must target the graph name provided by CLI arguments.
- Image backfill must only update nodes missing `image_path`.
- Image backfill must respect the dry-run flag and avoid writes when enabled.

---

## SAFETY CHECKS

- Verify host/port defaults before running against production data.
- Confirm playthrough name matches the intended asset output directory.
- Review console summaries for errors or duplicates after each run.

---

## FAILURE MODES

- Missing or invalid YAML sample file.
- Graph connection failures (host/port mismatch).
- Image generation failures that leave `image_prompt` set but no image path.

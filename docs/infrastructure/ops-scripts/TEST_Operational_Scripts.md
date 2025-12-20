# Ops Scripts — Tests: Operational Scripts

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
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
THIS:            TEST_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md
```

---

## AUTOMATED COVERAGE

No automated tests exist for these scripts.

---

## MANUAL CHECKS

```bash
python engine/scripts/seed_moment_sample.py --help
python engine/scripts/generate_images_for_existing.py --help
```

---

## GAPS

- No integration test to validate GraphOps seeding against a local FalkorDB (ngram repo runtime).
- No test harness for image backfill dry-run versus write modes.

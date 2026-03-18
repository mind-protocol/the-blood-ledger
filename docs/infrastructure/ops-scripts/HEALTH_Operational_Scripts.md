# Ops Scripts — Health: Seeding and Backfill Checks

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers operational scripts used for seeding and backfill. It
exists to catch failures where scripts run but do not mutate the graph as
expected. It does not verify data correctness beyond basic success signals.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
BEHAVIORS:       ./BEHAVIORS_Operational_Script_Runbooks.md
ALGORITHM:       ./ALGORITHM_Seeding_And_Backfill_Flows.md
VALIDATION:      ./VALIDATION_Operational_Script_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
THIS:            HEALTH_Operational_Scripts.md
SYNC:            ./SYNC_Ops_Scripts.md

IMPL:            tools/health/check_ops_scripts.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented ops scripts health checker
Implement `tools/health/check_ops_scripts.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for ops scripts
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: ops_script_applies
    flow_id: seed_moment_sample
    priority: high
    rationale: Script runs must result in graph mutations.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: ops_script_applies
```

---

## HOW TO RUN

```bash
# Manual: run a seed script and confirm no errors
python3 engine/scripts/seed_moment_sample.py --playthrough default
```

---

## KNOWN GAPS

- [ ] No automated validation of resulting graph mutations.

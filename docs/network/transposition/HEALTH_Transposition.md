# Transposition — Health: Conflict Resolution Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks transposition conflict resolution outcomes. It exists
to detect failures where imported content violates local canon. It does not
verify narrative quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Local_Canon_Primary.md
BEHAVIORS:       ./BEHAVIORS_Conflict_Resolution_Cascade.md
ALGORITHM:       ./ALGORITHM_Transposition_Pipeline.md
VALIDATION:      ./VALIDATION_Transposition_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Transposition.md
THIS:            HEALTH_Transposition.md
SYNC:            ./SYNC_Transposition.md

IMPL:            tools/health/check_transposition.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented transposition health checker
Implement `tools/health/check_transposition.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for conflict resolution
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: transposition_conflict_resolution
```

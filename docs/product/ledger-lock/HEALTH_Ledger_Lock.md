# Ledger Lock — Health: Lock State Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks ledger lock state changes. It exists to detect missing
lock/unlock transitions that would leave data in an inconsistent state. It
does not verify payment processor behavior.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ledger_Lock_Crisis.md
BEHAVIORS:       ./BEHAVIORS_Ledger_Lock_Trigger.md
ALGORITHM:       ./ALGORITHM_Ledger_Lock_Flow.md
VALIDATION:      ./VALIDATION_Ledger_Lock_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ledger_Lock.md
THIS:            HEALTH_Ledger_Lock.md
SYNC:            ./SYNC_Ledger_Lock.md

IMPL:            tools/health/check_ledger_lock.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented ledger lock health checker
Implement `tools/health/check_ledger_lock.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for lock transitions
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: ledger_lock_transitions
    flow_id: ledger_lock
    priority: high
    rationale: Lock/unlock must be observable and consistent.
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
    source: ledger_lock_transitions
```

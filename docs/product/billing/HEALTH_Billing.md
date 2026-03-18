# Billing — Health: Metered Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks billing signals (usage tally, alert delivery). It
exists to detect missing usage events that would underbill or surprise users.
It does not verify payment processor availability.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Pay_To_Preserve_History.md
BEHAVIORS:       ./BEHAVIORS_Metered_Billing_Experience.md
ALGORITHM:       ./ALGORITHM_Billing_Metering.md
VALIDATION:      ./VALIDATION_Billing_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Billing.md
THIS:            HEALTH_Billing.md
SYNC:            ./SYNC_Billing.md

IMPL:            tools/health/check_billing.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented billing health checker
Implement `tools/health/check_billing.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for billing metering
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: billing_usage_tracked
    flow_id: billing_metering
    priority: high
    rationale: Metered usage must reflect actual player activity.
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
    source: billing_usage_tracked
```

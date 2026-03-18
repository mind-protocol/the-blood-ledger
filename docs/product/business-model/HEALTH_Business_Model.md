# Business Model — Health: Monetization Signals

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file tracks business-model health signals (conversion, retention,
cost control). It exists to keep monetization assumptions observable. It does
not verify gameplay quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Whale_Economics.md
BEHAVIORS:       ./BEHAVIORS_Unit_Economics.md
ALGORITHM:       ./ALGORITHM_Semantic_Cache.md
VALIDATION:      ./VALIDATION_Business_Model_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Business_Model.md
THIS:            HEALTH_Business_Model.md
SYNC:            ./SYNC_Business_Model.md

IMPL:            tools/health/check_business_model.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented business model health checker
Implement `tools/health/check_business_model.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for margin guardrails
- Updates `status.result.value` in this file
- Runs throttled (max 1/day in production)
- Integrates with `ngram doctor` for aggregated reporting

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: margin_guardrails
    flow_id: monetization
    priority: high
    rationale: Cost overruns break the business model.
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
    source: margin_guardrails
```

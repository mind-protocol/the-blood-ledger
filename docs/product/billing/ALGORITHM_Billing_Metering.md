# Billing — Algorithm: Metered Usage Flow

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Pay_To_Preserve_History.md
BEHAVIORS:       ./BEHAVIORS_Metered_Billing_Experience.md
THIS:            ALGORITHM_Billing_Metering.md
VALIDATION:      ./VALIDATION_Billing_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Billing.md
HEALTH:          ./HEALTH_Billing.md
SYNC:            ./SYNC_Billing.md
```

---

## ALGORITHM

```
1. Track billable events (moments saved, storage deltas).
2. Aggregate usage by account and billing period.
3. Compute charges and notify the player before crossing thresholds.
4. Generate invoice metadata and deliver via billing provider.
5. Apply ledger lock when payment is overdue (per policy).
```

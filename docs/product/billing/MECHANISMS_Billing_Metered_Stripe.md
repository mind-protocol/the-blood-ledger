# Billing — Mechanisms: Metered Stripe Flow

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Pay_To_Preserve_History.md
BEHAVIORS:       ./BEHAVIORS_Metered_Billing_Experience.md
THIS:            MECHANISMS_Billing_Metered_Stripe.md (you are here)
VERIFICATION:    ./VALIDATION_Billing_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Billing.md
TEST:            ./TEST_Billing.md
SYNC:            ./SYNC_Billing.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Billing uses Stripe metered subscriptions. The game logs interactions locally, batches usage to Stripe, and issues monthly invoices formatted as stories.

---

## DATA STRUCTURES

### UsageRecord

```
player_id: string
interaction_type: string
cost_cents: int
created_at: timestamp
synced_to_stripe: bool
```

---

## MECHANISM: Usage Tracking

### Step 1: Log interaction

Write interaction data to local usage store.

### Step 2: Batch sync

Every N minutes, increment Stripe usage records.

### Step 3: Invoice generation

Stripe invoices monthly; the system sends a narrative summary.

---

## KEY DECISIONS

### D1: Aggregation cadence

```
IF time_since_last_sync >= 5 minutes:
    sync usage batch
```

### D2: Spending alerts

```
IF spend >= player_threshold:
    send notification
```

---

## DATA FLOW

```
Interaction
    ↓
Local usage log
    ↓
Stripe usage record
    ↓
Monthly invoice
```

---

## COMPLEXITY

**Time:** O(n) per batch of interactions.

**Space:** O(n) for usage log.

**Bottlenecks:**
- Stripe API rate limits

---

## HELPER FUNCTIONS

### `sync_usage_batch()`

**Purpose:** Report usage increments to Stripe.

**Logic:** Aggregate unsynced usage records and create usage entries.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/product/ledger-lock | billing_entry | Player payment setup |
| docs/product/chronicle-system | invoice_format | Story-formatted invoice

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define retry logic for Stripe API failures
- [ ] Define alert thresholds defaults
- IDEA: Add monthly usage projections

# Billing — Behaviors: Metered Experience

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Pay_To_Preserve_History.md
THIS:            BEHAVIORS_Metered_Billing_Experience.md (you are here)
MECHANISMS:      ./MECHANISMS_Billing_Metered_Stripe.md
VERIFICATION:    ./VALIDATION_Billing_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Billing.md
TEST:            ./TEST_Billing.md
SYNC:            ./SYNC_Billing.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Billing runs without interrupting play

```
GIVEN:  a player with a payment method on file
WHEN:   they play
THEN:   interactions are metered silently
```

### B2: Invoice reads like a Chronicle

```
GIVEN:  a monthly invoice is generated
WHEN:   the player receives it
THEN:   it is formatted as a story summary
```

### B3: Spending alerts are player-controlled

```
GIVEN:  the player sets alert thresholds
WHEN:   thresholds are crossed
THEN:   the player is notified without breaking immersion
```

---

## INPUTS / OUTPUTS

### Primary Function: `record_usage()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| player_id | string | Player identifier |
| moment_type | string | Dialogue/action/worldbuild |
| token_count | int | Token usage |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| usage_record | object | Stored usage entry |

**Side Effects:**

- Writes to local usage log
- Periodically syncs to Stripe

---

## EDGE CASES

### E1: Payment failure

```
GIVEN:  a failed invoice
THEN:   player enters grace period or read-only mode
```

### E2: Player opts out of alerts

```
GIVEN:  alerts disabled
THEN:   no in-game interruptions occur
```

---

## ANTI-BEHAVIORS

### A1: Pay-to-win behavior

```
GIVEN:   two players with different spend
WHEN:    content is generated
MUST NOT: alter simulation or outcomes based on spend
INSTEAD: only alter depth of history saved
```

### A2: Surprise charges without notice

```
GIVEN:   billing event occurs
WHEN:    invoice is sent
MUST NOT: conceal usage summaries
INSTEAD: include narrative breakdown
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define alert delivery channels (email, in-game, both)
- [ ] Define billing retries and dunning communication
- IDEA: Provide a pre-commit cost preview for high-cost queries

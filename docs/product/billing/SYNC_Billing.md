# Billing — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: Codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Metered billing via Stripe
- Narrative invoice framing
- Configurable spending alerts

**What's still being designed:**
- Dunning / payment failure flows
- Tax/VAT compliance

**What's proposed (v2+):**
- Pre-paid credits for high-risk accounts
- Usage projection dashboard

---

## CURRENT STATE

Billing is defined in the architecture spec and now captured in a module chain. No implementation exists in code yet.

---

## RECENT CHANGES

- 2025-12-21: Normalized implementation doc references and notes to match current repo state.
- 2025-12-21: Added HEALTH COVERAGE to `VALIDATION_Billing_Invariants.md`.

### 2025-12-19: Billing docs created

- **What:** Added PATTERNS/BEHAVIORS/MECHANISMS/VALIDATION/SYNC.
- **Why:** Establish pay-to-preserve billing model.
- **Files:** docs/product/billing/*

### 2025-12-20: Added algorithm and health docs

- **What:** Added `ALGORITHM_Billing_Metering.md` and `HEALTH_Billing.md`.
- **Why:** Close the doc chain gap flagged by `ngram validate`.
- **Files:** docs/product/billing/*

---

## KNOWN ISSUES

### Regulatory undefined

- **Severity:** medium
- **Symptom:** No tax/VAT handling guidance
- **Suspected cause:** Early design stage
- **Attempted:** None

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Document_Create_Module_Documentation

**Where I stopped:** Documentation only.

**What you need to understand:**
Billing must never leak into simulation logic; it's a preservation layer only.

**Watch out for:**
Alert settings that interrupt play.

**Open questions I had:**
How to handle failed payments without deleting worlds.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Billing docs are in place; implementation and compliance steps are pending.

**Decisions made:**
Metered post-paid billing is canonical; alerts are player-controlled.

**Needs your input:**
Confirm tax/VAT strategy and dunning policy.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Build usage tracker and Stripe sync

### Tests to Run

```bash
pytest tests/product/test_billing.py
```

### Immediate

- [ ] Define billing portal UX
- [ ] Define tax/VAT handling

### Later

- [ ] Add pre-paid credit option
- IDEA: Add usage projection UI

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Measured; billing needs legal clarity before implementation.

**Threads I was holding:**
Compliance, dunning, and invoice narrative formatting.

**Intuitions:**
Story-format invoices are core to retention and perception.

**What I wish I'd known at the start:**
Whether we want a subscription fallback for risk mitigation.

---

## POINTERS

| What | Where |
|------|-------|
| Billing architecture source | `data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md` |

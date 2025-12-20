# Ledger Lock — Patterns: Crisis of Memory

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md
```

---

## CHAIN

```
THIS:            PATTERNS_Ledger_Lock_Crisis.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Ledger_Lock_Trigger.md
MECHANISMS:      ./MECHANISMS_Ledger_Lock_Flow.md
VERIFICATION:    ./VALIDATION_Ledger_Lock_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ledger_Lock.md
TEST:            ./TEST_Ledger_Lock.md
SYNC:            ./SYNC_Ledger_Lock.md

IMPL:            data/Distributed-Content-Generation-Network/UX Design The Ledger Lock.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Ledger_Lock.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Ledger_Lock.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

A standard paywall destroys immersion. The Ledger Lock must convert deeply invested players by framing billing as a narrative crisis rather than a transaction.

---

## THE PATTERN

**Crisis of Memory.** Trigger conversion at the moment the player attempts to save/exit after building meaningful history. Present the choice as preserving or losing the Chronicle.

Current source content embedded here:
- Trigger heuristics: time, meaningful choices, ledger depth, tensions, grandmother query.
- Modal copy with personalized ledger lines.
- QR code + magic link flows.

---

## PRINCIPLES

### Principle 1: Weight, not a paywall
The moment must feel like a story consequence.

### Principle 2: Personalization is leverage
The modal uses the player’s own ledger entries to create urgency.

### Principle 3: Friction is a filter
The flow is designed to identify whales, not maximize mass conversion.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/product/billing | Payment setup and usage tracking |
| docs/product/chronicle-system | Chronicle framing and summaries |

---

## INSPIRATIONS

- Ledger Lock UX design doc
- Octalysis drives (ownership + loss aversion)

---

## SCOPE

### In Scope

- Trigger heuristics
- Modal copy and dynamic data insertion
- QR + magic link payment flow

### Out of Scope

- Billing implementation (Billing)
- Acquisition funnel (GTM Strategy)
- Chronicle video generation (Chronicle System)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define fallback flows for Steam overlay limitations
- [ ] Define localization for modal copy
- IDEA: Add "save grace" for disconnected users
- QUESTION: How to handle players who dismiss the modal repeatedly?

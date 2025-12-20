# Storms — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Storms as diff overlays
- Energy floods/drains
- Weekly/legacy/mystery storm types

**What's still being designed:**
- Authoring tools and validation
- Overlap/stacking rules

**What's proposed (v2+):**
- Storm marketplace
- Community storm editor

---

## CURRENT STATE

Storms are documented as lightweight crisis overlays built on top of Scavenger and Bleed-Through layers. No code implementation exists in the repository yet.

---

## RECENT CHANGES

### 2025-12-19: Storm docs created

- **What:** Added PATTERNS/BEHAVIORS/MECHANISMS/VALIDATION/SYNC.
- **Why:** Establish a canonical storm overlay model.
- **Files:** docs/infrastructure/storms/*

---

## KNOWN ISSUES

### No schema enforcement

- **Severity:** medium
- **Symptom:** Storm files could reference invalid nodes without checks
- **Suspected cause:** No validation tooling yet
- **Attempted:** None

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Document_Create_Module_Documentation

**Where I stopped:** Documentation only.

**What you need to understand:**
Storms are diffs; topology must stay in Scavenger.

**Watch out for:**
Stacking multiple storms without explicit precedence rules.

**Open questions I had:**
Whether to allow partial overlays for community submissions.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Storms docs are in place; implementation and tooling are pending.

**Decisions made:**
Energy floods/drains are the canonical mechanism for presence.

**Needs your input:**
Confirm storm authoring workflow and validation requirements.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Implement storm schema + apply pipeline

### Tests to Run

```bash
pytest tests/infrastructure/test_storms.py
```

### Immediate

- [ ] Define storm schema validator
- [ ] Decide storm stacking precedence

### Later

- [ ] Build storm authoring tool
- IDEA: Add storm lint CLI

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Energized; storms are clear but the tooling gap is big.

**Threads I was holding:**
Schema validation, stacking order, community submission safety.

**Intuitions:**
Storms will become the fastest path to content creation, so validation is critical.

**What I wish I'd known at the start:**
Whether we want storms as JSON or YAML for tooling.

---

## POINTERS

| What | Where |
|------|-------|
| Storms source | `data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md` |

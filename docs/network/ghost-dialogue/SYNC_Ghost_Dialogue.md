# Ghost Dialogue — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Dialogue index + vector search
- Reaction-based quality boosting
- Transposition before replay

**What's still being designed:**
- Safety and moderation pipeline
- Consent defaults and opt-out UX

**What's proposed (v2+):**
- Multilingual ghost dialogue
- Curated “legendary lines” library

---

## CURRENT STATE

Ghost Dialogue is defined in the feedback integration doc and now captured as a dedicated module. Implementation is not present yet.

---

## RECENT CHANGES

### 2025-12-19: Ghost Dialogue docs created

- **What:** Added PATTERNS/BEHAVIORS/MECHANISMS/VALIDATION/SYNC.
- **Why:** Establish shared dialogue reuse and safety constraints.
- **Files:** docs/network/ghost-dialogue/*

---

## KNOWN ISSUES

### Safety and consent undefined

- **Severity:** high
- **Symptom:** Potential misuse of player-generated dialogue
- **Suspected cause:** No policy or filters defined
- **Attempted:** None

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Document_Create_Module_Documentation

**Where I stopped:** Documentation only.

**What you need to understand:**
Ghost Dialogue requires a safety filter and consent model before any deployment.

**Watch out for:**
Privacy exposure if dialogue includes identifying information.

**Open questions I had:**
Should we default to opt-in or opt-out for indexing?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Ghost Dialogue docs are in place; policy and implementation are missing.

**Decisions made:**
Use real dialogue lines as top-tier content; transposition required.

**Needs your input:**
Define consent model and moderation requirements.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Build dialogue index and retrieval pipeline

### Tests to Run

```bash
pytest tests/network/test_ghost_dialogue.py
```

### Immediate

- [ ] Define consent and opt-out policy
- [ ] Define safety filters and escalation path

### Later

- [ ] Add quality scoring rubric
- IDEA: Create "legendary line" curation flow

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Cautious; safety and consent feel like launch blockers.

**Threads I was holding:**
Consent defaults, safety filters, and privacy law compliance.

**Intuitions:**
Opt-in is safer; opt-out risks backlash.

**What I wish I'd known at the start:**
Whether we have legal guidance on reusing player-generated dialogue.

---

## POINTERS

| What | Where |
|------|-------|
| Feedback integration source | `data/Distributed-Content-Generation-Network/Blood Ledger — Feedback Integration.md` |

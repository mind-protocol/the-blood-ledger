# Shadow Feed — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Rumor-only caching model
- Causality/proximity/canon locks
- Distant events imported as low-truth rumors

**What's still being designed:**
- Feed storage, retention, and pruning
- Rumor surfacing frequency

**What's proposed (v2+):**
- Rumor investigation UI
- Cross-world rumor analytics

---

## CURRENT STATE

Shadow Feed is defined as a rumor cache for distant events. The module is documentation-only and depends on canon truth checks and transposition for conflict handling.

---

## RECENT CHANGES

### 2025-12-19: Shadow Feed docs created

- **What:** Added PATTERNS/BEHAVIORS/MECHANISMS/VALIDATION/SYNC.
- **Why:** Clarify safe reuse constraints for distant events.
- **Files:** docs/network/shadow-feed/*

### 2025-12-20: Added algorithm and health docs

- **What:** Added `ALGORITHM_Shadow_Feed_Import.md` and `HEALTH_Shadow_Feed.md`.
- **Why:** Close the doc chain gap flagged by `ngram validate`.
- **Files:** docs/network/shadow-feed/*

---

## KNOWN ISSUES

### Storage undefined

- **Severity:** medium
- **Symptom:** No defined backend or retention policy
- **Suspected cause:** Early design stage
- **Attempted:** None

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Document_Create_Module_Documentation

**Where I stopped:** Docs only; no implementation details.

**What you need to understand:**
Shadow Feed is rumor-only; any drift toward fact breaks canon safety.

**Watch out for:**
Local events accidentally entering the feed.

**Open questions I had:**
How to surface rumors without overwhelming the player.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Shadow Feed docs are complete; implementation is pending.

**Decisions made:**
Causality, proximity, and canon locks are required.

**Needs your input:**
Confirm desired rumor persistence/expiry windows.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Implement feed storage + filtering rules

### Tests to Run

```bash
pytest tests/network/test_shadow_feed.py
```

### Immediate

- [ ] Define feed storage backend
- [ ] Define rumor surfacing cadence

### Later

- [ ] Build rumor investigation UX
- IDEA: Add feed health dashboards

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Calm; constraints are clear, but storage decisions are open.

**Threads I was holding:**
Rumor cadence and player tolerance for misinformation.

**Intuitions:**
Rumors should be rare and high-impact to avoid noise.

**What I wish I'd known at the start:**
Whether we want rumors to appear in the Ledger or Chronicle by default.

---

## POINTERS

| What | Where |
|------|-------|
| Cluster State Cache source | `data/Distributed-Content-Generation-Network/Blood Ledger — Cluster State Cache.md` |

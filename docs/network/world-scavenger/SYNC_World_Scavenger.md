# World Scavenger — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Priority stack (cache → ghost → rumor → synthesize → generate)
- Topology/state split
- Safety locks (causality, proximity, canon)

**What's still being designed:**
- Cache storage and retrieval infrastructure
- Dialogue index quality scoring
- Retention/pruning policies

**What's proposed (v2+):**
- Region-specific cache pools
- User-facing opt-out for scavenged content

---

## CURRENT STATE

World Scavenger is defined as a design system with pseudocode and economic rationale. Documentation now captures the priority stack and safety rules; no runtime implementation exists yet.

---

## RECENT CHANGES

### 2025-12-19: World Scavenger docs created

- **What:** Added PATTERNS/BEHAVIORS/MECHANISMS/VALIDATION/SYNC.
- **Why:** Make reuse strategy canonical and auditable.
- **Files:** docs/network/world-scavenger/*

---

## KNOWN ISSUES

### Cache storage undefined

- **Severity:** high
- **Symptom:** No clear storage backend or pruning strategy
- **Suspected cause:** Early design phase
- **Attempted:** None

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Document_Create_Module_Documentation

**Where I stopped:** Documentation only.

**What you need to understand:**
Safety locks are core; reuse without them breaks causality.

**Watch out for:**
Homogenization risk if caches dominate content generation.

**Open questions I had:**
How to evaluate quality of imported content at scale.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
World Scavenger docs are in place; implementation and storage details remain open.

**Decisions made:**
Priority stack and topology/state split are canonical.

**Needs your input:**
Confirm storage architecture for global caches and indices.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Build cache/ghost index services

### Tests to Run

```bash
pytest tests/network/test_world_scavenger.py
```

### Immediate

- [ ] Decide cache storage + indexing backend
- [ ] Define pruning and retention policy

### Later

- [ ] Design quality scoring rubric
- IDEA: Add cache diagnostics dashboard

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Concerned about scale and homogenization, but the economics are strong.

**Threads I was holding:**
Cache storage, quality gating, retention policy.

**Intuitions:**
Quality scoring is essential; otherwise reuse will degrade story texture.

**What I wish I'd known at the start:**
Whether reuse should be visible to players as a toggle.

---

## POINTERS

| What | Where |
|------|-------|
| World Scavenger source | `data/Distributed-Content-Generation-Network/Blood Ledger — World Scavenger.md` |

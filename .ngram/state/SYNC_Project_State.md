# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
```

---

## CURRENT STATE

Graph scope files listed in `data/graph_scope_classification.yaml` were deleted from this repo.
ngram scaffolding has been reinitialized and the repository map regenerated.

---

## ACTIVE WORK

### Graph Scope Cleanup

- **Area:** repo-wide
- **Status:** completed
- **Owner:** agent
- **Context:** Removed curated graph scope files; reinitialized ngram and rebuilt map.

---

## RECENT CHANGES

### 2025-12-20: Delete curated graph scope files

- **What:** Removed all existing files listed in `data/graph_scope_classification.yaml`.
- **Why:** Graph-related files were transferred to the ngram repo per request.
- **Impact:** 202 files deleted; 4 referenced paths already missing.

### 2025-12-20: Reinitialize ngram and regenerate map

- **What:** Ran `ngram init` and `ngram overview`.
- **Why:** Restore protocol scaffolding and regenerate `map.md`.
- **Impact:** Fresh `.ngram/` structure and updated repo map.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| Doc references to missing paths | medium | repo-wide | Missing: `engine/models/tensions.py`, `engine/db/graph_ops.py`, `engine/api/app.py`, `engine/infrastructure/memory/transcript.py`. |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Analyze_Structural_Analysis.md`

**Current focus:** Verify repo state after graph scope removal and update any remaining documentation references.

**Key context:**
Graph scope files were deleted on purpose. ngram scaffolding was reinitialized afterward.

**Watch out for:**
Docs still reference deleted paths; decide whether to clean or leave as historical references.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Curated graph scope files were deleted and the ngram framework was reinitialized.
The repository map has been regenerated.

**Decisions made recently:**
Delete all graph scope files listed in `data/graph_scope_classification.yaml` per request.

**Needs your input:**
Whether to clean up remaining doc references to deleted files or leave them as historical references.

**Concerns:**
Any downstream tooling expecting those files will fail until references are updated or restored.

---

## TODO

### High Priority

- [ ] Confirm whether to remove or preserve doc references to deleted graph scope files.

### Backlog

- [ ] Rebuild or replace missing modules if the ngram repo transfer needs verification.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Work is progressing with major deletions completed; next steps depend on verification and cleanup decisions.

**Architectural concerns:**
Deleting graph scope files may leave dangling dependencies in other modules.

**Opportunities noticed:**
If the ngram repo is authoritative now, consider adding a pointer document that explains the split.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| repo-wide | updated | `docs/**/SYNC_*.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| N/A | N/A | N/A | N/A |

**Unmapped code:** (run `ngram validate` to check)
- Not assessed after deletions.

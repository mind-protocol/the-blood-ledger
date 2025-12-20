# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
```

---

## CURRENT STATE

Graph scope files listed in `data/graph_scope_classification.yaml` were removed
from this repo. ngram was reinitialized and repo maps regenerated. Vision,
opening, and README references were updated to point to the ngram repo for
graph runtime documentation.

---

## ACTIVE WORK

### Graph Reference Cleanup

- **Area:** docs/design + README
- **Status:** in progress
- **Owner:** agent
- **Context:** Remove or replace references to graph runtime paths that no longer exist here.

---

## RECENT CHANGES

### 2025-12-20: Delete curated graph scope files

- **What:** Removed all existing files listed in `data/graph_scope_classification.yaml`.
- **Why:** Graph-related files were transferred to the ngram repo per request.
- **Impact:** 202 files deleted; 4 referenced paths already missing.

### 2025-12-20: Reinitialize ngram and regenerate maps

- **What:** Ran `ngram init` and `ngram overview` (twice) to restore scaffolding and map.
- **Why:** Rebuild protocol files after the curated deletion and doc updates.
- **Impact:** `.ngram/` refreshed and `map.md` regenerated.

### 2025-12-20: Update vision/opening docs after graph move

- **What:** Updated `README.md`, `docs/design/ALGORITHM_Vision.md`,
  `docs/design/SYNC_Vision.md`, `docs/design/opening/CLAUDE.md`,
  and `docs/design/opening/IMPLEMENTATION_Opening.md`.
- **Why:** Remove references to graph runtime paths that no longer live here.
- **Impact:** Docs now point to `data/ARCHITECTURE — Cybernetic Studio.md`.

### 2025-12-20: Clean remaining graph path references

- **What:** Updated infrastructure/world docs to replace deleted graph runtime paths with ngram repo pointers.
- **Why:** Remove stale references to `engine/physics/graph`, `engine/db/graph_*`, and `docs/physics/graph`.
- **Impact:** Dependencies and ops-script docs now point to `data/ARCHITECTURE — Cybernetic Studio.md`.

### 2025-12-20: Update agent instructions and module docs

- **What:** Updated async/history/image-generation/map/scraping docs and agent instructions to note the ngram repo graph runtime.
- **Why:** Ensure examples and invariants match the runtime split.
- **Impact:** GraphOps/GraphQueries references now avoid pointing to removed local paths.

### 2025-12-20: Health checks and validation run

- **What:** Ran `ngram doctor` and `ngram validate`.
- **Why:** Verify protocol health after doc updates.
- **Impact:** Existing repo-wide issues remain (missing VIEW, missing HEALTH docs, broken CHAIN links). See `.ngram/state/SYNC_Project_Health.md` and validation output for details.

### 2025-12-20: Add missing VIEW and HEALTH docs

- **What:** Added `VIEW_Collaborate_Pair_Program_With_Human.md` and HEALTH docs for map, scraping, embeddings, and canon modules.
- **Why:** Address missing VIEW and broken CHAIN links reported by `ngram validate`.
- **Impact:** Validation should clear missing VIEW and chain link errors for those modules.

### 2025-12-20: Re-run validation and health checks

- **What:** Re-ran `ngram validate` and `ngram doctor`.
- **Why:** Confirm doc chain fixes and update health state.
- **Impact:** Missing VIEW and CHAIN link issues resolved; remaining gaps are missing HEALTH docs and undocumented modules.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| Remaining graph references in other docs | medium | `docs/` | Need scan beyond vision/opening/README. |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Analyze_Structural_Analysis.md`

**Current focus:** Finish cleaning graph references after the graph runtime move.

**Key context:**
Graph scope files were deleted; use ngram repo for graph runtime docs.

**Watch out for:**
Stale `engine/physics/graph`/`engine.db.graph_*` references outside design docs.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Graph scope files were removed from this repo and documentation was updated to
point to the ngram repo. ngram scaffolding and maps were regenerated.

**Decisions made recently:**
Graph runtime documentation now lives in the ngram repo; this repo is cleaned
to reflect that split.

**Needs your input:**
Whether to purge all remaining graph references in non-design docs or keep them
as historical context.

**Concerns:**
Docs outside design/opening may still refer to deleted graph paths.

---

## Agent Observations

### Remarks
- `map.md` still lists `engine/physics/graph/**` and `docs/physics/graph/**` because those directories still exist in this repo.

### Suggestions
- [ ] Decide whether the remaining graph directories should be deleted or intentionally retained; align docs and map accordingly.

### Propositions
- If graph runtime must stay external, add a single canonical pointer doc that lists the ngram repo locations and import guidance.

---

## TODO

### High Priority

- [ ] Decide scope of graph reference cleanup beyond design/opening/README.

### Backlog

- [ ] Re-run a full doc scan once cleanup scope is defined.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Cleanup is progressing; remaining work is mostly documentation alignment.

**Architectural concerns:**
Decoupling docs across repos risks drift if references are not consolidated.

**Opportunities noticed:**
Add a single pointer doc that enumerates where graph/runtime docs now live.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `docs/design/` | updating | `docs/design/SYNC_Vision.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| N/A | N/A | N/A | N/A |

**Unmapped code:** (run `ngram validate` to check)
- Not assessed after deletions.

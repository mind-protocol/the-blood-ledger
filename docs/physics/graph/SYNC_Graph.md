# SYNC: Graph Module

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: gemini
STATUS: DESIGNING
MATURITY: PROPOSED
```

---

## CURRENT STATE

The module is currently in the **DESIGNING** phase for the migration to `~/ngram`.
The existing `GraphQueries` implementation (direct FalkorDB) is deprecated and will be replaced by `NgramGraphClient`.

**Analysis Complete:**
- Integration points identified: Canon, Speaker, World Builder, Semantic Search.
- Design pattern selected: Adapter (`NgramGraphClient`).
- Risk identified: Vector search compatibility.

---

## ACTIVE WORK

### Ngram Integration
- **Owner:** Agent
- **Status:** Planning
- **Goal:** Replace direct FalkorDB connection with `~/ngram` service calls.

**Next Steps:**
1.  Implement `NgramGraphClient` in `engine/physics/graph/`.
2.  Update `engine/infrastructure/canon/` to use the new client.
3.  Refactor `engine/world/map/semantic.py` for vector search compatibility.

---

## KNOWN ISSUES

| Issue | Severity | Notes |
|-------|----------|-------|
| Vector Search | High | FalkorDB specific syntax in `semantic.py` may not work with `ngram`. |
| Missing `__init__.py` | Medium | `engine/physics/graph/__init__.py` was missing in recent scans, needs restoration. |

---

## HANDOFF

**For the next agent:**
The design docs (`PATTERNS_Ngram_Integration.md`, `IMPLEMENTATION_Ngram_Client.md`) are ready.
Start by creating the `NgramGraphClient` class. Verify the `ngram` API capabilities regarding vector search before refactoring `semantic.py`.

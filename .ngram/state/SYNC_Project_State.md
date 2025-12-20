# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
```

---

## CURRENT STATE

Opening flow documentation is now aligned to the current playthrough bootstrap
implementation, including seed graph initialization, scenario injection, and
opening moment creation. Local dev startup uses the correct FastAPI entrypoint.
Escalation marker wording in principles and agent guidance now avoids
false-positive escalation detection.

---

## ACTIVE WORK

### Documentation Alignment

- **Area:** `docs/design/opening/`
- **Status:** in progress
- **Owner:** agent
- **Context:** Ensure opening data flow and health checks match current code paths.

---

## RECENT CHANGES

### 2025-12-20: Opening Flow Docs + Dev Startup Fix

- **What:** Updated opening implementation/health docs to include seed graph init and clarified steps; fixed backend entrypoint in `run.sh`.
- **Why:** Close doc/code drift and resolve missing SSE route in local dev.
- **Impact:** Clearer opening data flow; local SSE endpoint mounts correctly when using `run.sh`.

### 2025-12-20: Principles Escalation Marker Wording

- **What:** Reworded the escalation marker reference in `.ngram/PRINCIPLES.md` to avoid being parsed as an active escalation marker.
- **Why:** Prevent false-positive escalation detection in the principles doc.
- **Impact:** Escalation scan no longer flags the principles reference as unresolved.

### 2025-12-20: Escalation View Marker Escaped

- **What:** Escaped the escalation marker example in `.ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md`.
- **Why:** Prevent the example from being parsed as a live escalation marker.
- **Impact:** Escalation scans no longer flag the view's example block as unresolved.

### 2025-12-20: Agents Escalation Marker Wording

- **What:** Reworded the escalation marker reference in `AGENTS.md` to avoid being parsed as an active escalation marker.
- **Why:** Prevent false-positive escalation detection in the agent guidance doc.
- **Impact:** Escalation scan no longer flags the agent guidance reference as unresolved.

### 2025-12-20: GEMINI Escalation Review

- **What:** Reviewed `.ngram/GEMINI.md` for escalation markers tied to issue #16; no conflicts or escalation markers were present to resolve.
- **Why:** Ensure the escalation repair task is assessed even when the target file has no actionable conflicts.
- **Impact:** No changes required to `.ngram/GEMINI.md`; issue handled as a no-op with verification recorded here.

### 2025-12-20: CLAUDE Escalation Review

- **What:** Reviewed `.ngram/CLAUDE.md` for escalation markers tied to issue #16; no conflicts or escalation markers were present to resolve.
- **Why:** Ensure the escalation repair task is assessed even when the target file has no actionable conflicts.
- **Impact:** No changes required to `.ngram/CLAUDE.md`; issue handled as a no-op with verification recorded here.

### 2025-12-20: Escalation View Marker Encoding

- **What:** Encoded the proposition marker examples in the escalation view to avoid false-positive marker detection.
- **Why:** Prevent the escalation/proposition examples from being flagged as unresolved markers during health scans.
- **Impact:** The escalation view remains instructional without triggering the escalation scanner.
- **Repair run:** Confirmed during repair `03-ESCALATION-CLAUDE`; no further action needed.

### 2025-12-20: Graph Health Check Helpers Verified

- **What:** Verified `engine/graph/health/check_health.py` already implements health report helper methods tied to issue #16; no code edits required.
- **Why:** The incomplete-implementation repair targeted helper functions that were already filled in.
- **Impact:** Documentation sync updated to record the no-op repair.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| SSE stream 404 when backend is started with the old module path | high | `run.sh` | Use `engine.infrastructure.api.app:app` so `/api/moments/stream/{id}` is mounted |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Implement_Write_Or_Modify_Code.md

**Current focus:** Keep opening/playthrough bootstrap docs aligned with code, verify SSE endpoint behavior.

**Key context:**
Playthrough creation seeds a fresh graph via `engine/init_db.py`, then applies scenario YAML, creates opening moments, and returns `scene.json`.

**Watch out for:**
Local dev scripts may point at outdated FastAPI module paths; SSE 404 is a symptom.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Opening docs now describe the real bootstrap flow, including seed graph init and opening moment creation.
Local dev `run.sh` now targets the correct API entrypoint so the moment SSE route is available.

**Decisions made recently:**
Documented seed graph init as a first-class step in the opening flow and added a health indicator for it.

**Needs your input:**
Confirm whether playthrough bootstrap should hard-fail when seed graph loading fails (currently logs and continues).

**Concerns:**
If deployment uses a different entrypoint than `engine.infrastructure.api.app:app`, the SSE route may still be missing.

---

## TODO

### High Priority

- [ ] Decide if seed-load failures should abort playthrough creation.

### Backlog

- [ ] Add automated opening health checks (`engine/tests/test_opening_health.py`).
- IDEA: Add a lightweight smoke test that hits `/api/moments/stream/{id}` after playthrough creation.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Stable; small documentation alignment and dev startup fixes.

**Architectural concerns:**
Seed graph init is best-effort today; drift risk if scenarios assume missing seed nodes.

**Opportunities noticed:**
Automate opening health checks to validate graph + scene outputs together.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `design/opening/` | active | `docs/design/opening/SYNC_Opening.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| opening | `engine/infrastructure/api/playthroughs.py` | `docs/design/opening/` | CANONICAL |

**Unmapped code:** (run `ngram validate` to check)
- {List any code directories without module mappings}

**Coverage notes:**
Module manifest needs to include docs for opening if you want full mapping coverage.

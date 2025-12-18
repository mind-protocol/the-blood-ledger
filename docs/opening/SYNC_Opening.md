# The Opening — Sync

```
LAST_UPDATED: 2024-12-17
UPDATED_BY: Codex agent
STATUS: Scripted transcript active
```

---

## Chain Reference

| Doc | Purpose |
|-----|---------|
| PATTERNS_Opening.md | Philosophy
| BEHAVIORS_Opening.md | Experience description
| ALGORITHM_Opening.md | Implementation outline
| CONTENT.md | Actual script + prompts
| VALIDATION_Opening.md | Success metrics
| TEST_Opening.md | Planned coverage
| SYNC_Opening.md | This file

---

## Current Notes

- Transcript in `CONTENT.md` continues to drive best engagement; keep static for now.
- Need to automate extraction of answers → ledger entries.
- Playthrough bootstrap writes `player.yaml` but not moment graph yet.

---

## Upcoming Work

1. **Moment Migration** — Convert opening script into moment graph nodes so `/api/view` can serve the first scene without scene.json.
2. **Answer Storage** — Map each question to ledger/tension updates automatically (write helper in `engine/orchestration/opening.py`).
3. **Prototype Test Plan** — Capture actual player transcripts + validation metrics (see TEST_Opening.md).

Add owners/ETAs next update.

# The Opening — Sync

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: ngram repair agent
STATUS: Scripted transcript active
MATURITY: CANONICAL
```

---

## Chain Reference

| Doc | Purpose |
|-----|---------|
| PATTERNS_Opening.md | Philosophy — why static questions work |
| BEHAVIORS_Opening.md | Experience description — what player feels |
| ALGORITHM_Opening.md | Implementation outline — bootstrap steps |
| CONTENT.md | Actual script + prompts (17 questions, 10 beats) |
| VALIDATION_Opening.md | Success metrics |
| TEST_Opening.md | Planned coverage (STATUS: TODO) |
| SYNC_Opening.md | This file |

---

## Current State

**What's working:**
- `opening.json` provides structured question flow (10 beats, 17 questions)
- `playthroughs.py::_opening_to_scene_tree()` converts opening.json → SceneTree format
- Playthrough bootstrap writes `player.yaml` AND moment graph (fixed since 2024-12-17)
- Opening moments created from scenario narration in graph via `add_moment()`
- `PROFILE_NOTES.md` created per playthrough for tracking player answers

**What's not yet implemented:**
- Automated extraction of answers → ledger entries (still manual via PROFILE_NOTES)
- Answer-to-tension mapping helper (originally planned for `engine/orchestration/opening.py`)
- Tests (TEST_Opening.md still shows STATUS: TODO)

---

## Code Locations

Since 2025-12 restructure:
- `engine/infrastructure/api/playthroughs.py` — opening scene generation, moment creation
- `docs/design/opening/opening.json` — structured question template
- Orchestration now at `engine/infrastructure/orchestration/` (not `engine/orchestration/`)

---

## Upcoming Work

1. **Answer Storage** — Map each question's player response to ledger/tension updates automatically. Create helper in `engine/infrastructure/orchestration/opening.py`.
2. **Test Coverage** — Implement scripted session replay, sentiment analysis, persistence checks per TEST_Opening.md.

---

## Notes

- Static questions in CONTENT.md remain the most engaging approach per design philosophy
- LLM's role: present questions with life/timing, listen, build player profile, reflect back authentically
- Companion reflection template in CONTENT.md guides post-question synthesis

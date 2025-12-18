# The Opening — Algorithm

```
STATUS: DRAFT
CREATED: 2024-12-17
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Opening.md
BEHAVIORS:   ./BEHAVIORS_Opening.md
THIS:        ALGORITHM_Opening.md (you are here)
CONTENT:     ./CONTENT.md
VALIDATION:  ./VALIDATION_Opening.md
TEST:        ./TEST_Opening.md
SYNC:        ./SYNC_Opening.md
```

---

1. **Bootstrap** — Load `opening.json` and apply narrator instructions from `CONTENT.md`.
2. **Companion Profiling** — Evaluate player input to tag drives (BLOOD/OATH/SHADOW) and tone.
3. **Question Loop**
   - Ask question
   - Await player free text (LLM-friendly, multi-line)
   - Summarize answer, store to `player.yaml`
   - Mirror back with companion reflection
4. **Ledger Hooks** — Convert answers into ledger entries or vows when applicable.
5. **Transition** — After final reveal, write `scene.json` + `scene_memory` nodes for downstream systems.
```

# Vision — Tests / Validation Signals

```
CREATED: 2024-12-17
STATUS: CANONICAL_METRICS
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Vision.md
BEHAVIORS:   ./BEHAVIORS_Vision.md
ALGORITHM:   ./ALGORITHM_Vision.md
VALIDATION:  ./VALIDATION_Vision.md
THIS:        TEST_Vision.md (you are here)
SYNC:        ./SYNC_Vision.md
```

---

## Experience Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Companion familiarity | Player can describe 2 companions after 1 hour | Post-session interview |
| Memory surprise | Player recalls at least 1 "they remembered" moment | Diary study |
| Agency clarity | Player can state next action without hints | Think-aloud observation |

---

## Build Verification

- Playthrough smoke (UI) — follow Launch Protocol in README, record issues.
- Backend uptime — `curl /health` every minute, alert on >2 failures.
- Narrative probes — Use prompts in `docs/design/opening/CONTENT.md` to ensure responses remain grounded.
```

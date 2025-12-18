# World Scraping — Tests

```
CREATED: 2024-12-17
STATUS: TODO
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_World_Scraping.md
BEHAVIORS:   ./BEHAVIORS_World_Scraping.md
ALGORITHMS:  ./ALGORITHM_*.md
VALIDATION:  ./VALIDATION_World_Scraping.md
THIS:        TEST_World_Scraping.md (you are here)
SYNC:        ./SYNC_World_Scraping.md
```

---

| Test | Path | Purpose |
|------|------|---------|
| Geography routes | `tests/world/test_routes.py` | Travel time + river crossing assertions |
| Political placement | `tests/world/test_positions.py` | Historical NPC alignment |
| Narrative integrity | `tests/world/test_narratives.py` | Conflicting accounts flagged |
| Pipeline smoke | `tests/world/test_pipeline.py` | Ensures ETL stages run sequentially |

Gaps: tests currently conceptual; need to implement once world data scaffolding exists.
```

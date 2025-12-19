# World Scraping — Behaviors

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_World_Scraping.md
THIS:        BEHAVIORS_World_Scraping.md (you are here)
ALGORITHM:   ./ALGORITHM_Pipeline.md
VALIDATION:  ./VALIDATION_World_Scraping.md
TEST:        ./TEST_World_Scraping.md
SYNC:        ./SYNC_World_Scraping.md
```

---

### B1: Source Traceability
```
GIVEN:  Data is ingested from chronicles/maps
WHEN:   Nodes/edges created
THEN:   Each carries `source` metadata pointing to the reference (book/page/url)
```

### B2: Narrative Cohesion
```
GIVEN:  Scraped facts include conflicting accounts
WHEN:   They enter the graph
THEN:   Contradictions are represented as separate narratives with uncertainty weights
```

### B3: Incremental Refresh
```
GIVEN:  New sources arrive
WHEN:   Pipeline runs again
THEN:   Only changed nodes are updated (MERGE), keeping manual annotations intact
```

### B4: Exportable Bundles
```
GIVEN:  Designer wants to inspect dataset
WHEN:   `python scripts/export_world.py` executes
THEN:   Structured JSON/YAML export is generated with identical shape each time
```
```

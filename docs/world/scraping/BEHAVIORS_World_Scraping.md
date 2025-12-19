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
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
TEST:        ./TEST_World_Scraping.md
SYNC:        ./SYNC_World_Scraping.md
```

---

## BEHAVIORS

### B1: Source Traceability
```
GIVEN:  Data is ingested from chronicles/maps
WHEN:   Nodes/edges created
THEN:   Each carries `source` metadata pointing to the reference (book/page/url)
```
Notes: Source metadata must stay attached across phases so later merges can
audit where every fact came from without guessing provenance.

### B2: Narrative Cohesion
```
GIVEN:  Scraped facts include conflicting accounts
WHEN:   They enter the graph
THEN:   Contradictions are represented as separate narratives with uncertainty weights
```
Notes: Conflicting claims are preserved as parallel narratives instead of
overwriting prior records, keeping ambiguity explicit for the graph.

### B3: Incremental Refresh
```
GIVEN:  New sources arrive
WHEN:   Pipeline runs again
THEN:   Only changed nodes are updated (MERGE), keeping manual annotations intact
```
Notes: Re-runs should be idempotent for unchanged content while respecting
curated fields like tags, labels, or hand-written notes.

### B4: Exportable Bundles
```
GIVEN:  Designer wants to inspect dataset
WHEN:   `python scripts/export_world.py` executes
THEN:   Structured JSON/YAML export is generated with identical shape each time
```
Notes: Exports must remain stable across runs so downstream validation and
diff tooling can compare bundles without format drift.

## INPUTS / OUTPUTS

Inputs include phase-specific source lists, cached scraping outputs, and manual
historical references stored alongside the pipeline scripts and YAML fixtures.
Outputs include normalized YAML bundles for places, routes, characters, events,
narratives, beliefs, tensions, and things, plus optional JSON exports.

## EDGE CASES

- Source endpoints are offline or rate-limited, so cached or manual data is used.
- Duplicate names across regions require disambiguation to avoid conflating nodes.
- Partial sources yield missing fields that must be filled or flagged explicitly.
- Re-ingesting data with manual edits must preserve curated annotations.

## ANTI-BEHAVIORS

- Do not overwrite curated fields with empty scraped values on reruns.
- Do not collapse conflicting accounts into a single narrative without weights.
- Do not emit unstable export schemas that break downstream tooling.
- Do not inject nodes without a traceable source or explicit manual override.

## GAPS / IDEAS / QUESTIONS

- Decide how to store multiple source citations per node when facts overlap.
- Define the minimum confidence threshold for adding rumors vs. events.
- Clarify whether export bundles should include provenance diffs per phase.
- Identify the best place to track manual overrides for audit and rollback.

# World Builder — Algorithm Overview

```
STATUS: CANONICAL
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_World_Builder.md
BEHAVIORS:       ../BEHAVIORS_World_Builder.md
THIS:            ALGORITHM_Overview.md (you are here)
DETAILS:         ./ALGORITHM_Details.md
VALIDATION:      ../VALIDATION/VALIDATION_Overview.md
IMPLEMENTATION:  ../IMPLEMENTATION/IMPLEMENTATION_Overview.md
TEST:            ../TEST/TEST_Overview.md
SYNC:            ../SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/
```

---

## Overview

World Builder records every query as a thought moment, links it to results, and enriches the graph only when results are sparse.
Attention becomes energy via the physics system; no explicit energy injection is required in query logic.

---

## Core Flow

1. Record query as a thought moment (energy=0.3, status=possible).
2. Run semantic search against the graph.
3. Link the moment to top results via ABOUT (weight=similarity).
4. Measure sparsity across proximity, cluster size, diversity, and connectedness.
5. If sparse and enrichment enabled: call `WorldBuilder.enrich()`.
6. Apply enrichment, linking all created content back to the query moment.
7. Re-run semantic search and link new results.

---

## Query Moment Rules

- Always `type="thought"`, `status="possible"`, `energy=0.3`.
- Links:
  - `ATTACHED_TO` + `CAN_SPEAK` when `char_id` provided.
  - `OCCURRED_AT` when `place_id` provided.
  - `ABOUT` for each result (weight=similarity).

---

## Sparsity Decision (Thresholds)

A query is sparse if ANY of these are true:

- proximity < 0.6
- cluster_size < 2
- diversity < 0.3
- connectedness < 1.5

---

## Enrichment Application

- World Builder produces characters, places, things, narratives, links, and moments.
- All created nodes are marked `generated: true` and linked back to the query moment via ABOUT.
- Enriched moments are always `type="thought"` and connected to the speaker/place if available.

---

## Caching / Guardrails

- Recent enrichments are cached to prevent repeated calls within 60s.
- A recursion guard prevents the same query from enriching concurrently.

---

## Archive Note

Long-form prompt templates and examples are summarized in `../archive/SYNC_archive_2024-12.md`.

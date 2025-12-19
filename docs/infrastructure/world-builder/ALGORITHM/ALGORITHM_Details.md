# World Builder — Algorithm Details

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
OVERVIEW:        ./ALGORITHM_Overview.md
THIS:            ALGORITHM_Details.md (you are here)
VALIDATION:      ../VALIDATION/VALIDATION_Overview.md
IMPLEMENTATION:  ../IMPLEMENTATION/IMPLEMENTATION_Overview.md
TEST:            ../TEST/TEST_Overview.md
SYNC:            ../SYNC_World_Builder.md
```

---

## Sparsity Result Shape

```
SparsityResult:
  sparse: bool
  proximity: float      # 0-1
  cluster_size: int
  diversity: float      # 0-1
  connectedness: float
```

`is_sparse()` computes these values from embeddings and graph link counts.

---

## Enrichment Output Shape (Summary)

```
EnrichmentOutput:
  characters: List[Character]
  places: List[Place]
  things: List[Thing]
  narratives: List[Narrative]
  links: List[Link]
  moments: List[Moment]
```

All moments emitted by enrichment are treated as `type="thought"` and linked to the query moment via ABOUT.

---

## Linking Rules

- Each created node receives an ABOUT link from the query moment.
- Enriched moments link to their speaker via ATTACHED_TO and CAN_SPEAK when a speaker is known.
- Enriched moments link to place context when provided.

---

## Archive Note

The previous full prompt template and YAML examples are condensed in `../archive/SYNC_archive_2024-12.md`.

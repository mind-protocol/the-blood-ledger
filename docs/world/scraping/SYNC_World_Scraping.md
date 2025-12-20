# World Scraping — Sync: Current State

```
STATUS: DESIGNING
UPDATED: 2025-12-20
```

## MATURITY

STATUS: DESIGNING

The scraping pipeline and YAML outputs are stable, but ongoing documentation consolidation means the module remains in DESIGNING until the pipeline is fully verified end-to-end.

## CURRENT STATE

Pipeline phases 1–6 are complete, YAML outputs are present in `data/world/`, and the `seed` database is populated.

## RECENT CHANGES

### 2025-12-20: Graph runtime location noted

- **What:** Updated GraphOps references to call out the ngram repo graph runtime.
- **Why:** The graph runtime was moved out of this repo.
- **Impact:** Scraping docs now point to the authoritative runtime location.

### 2025-12-20: Add HEALTH doc for seeding checks

- **What:** Added `HEALTH_World_Scraping.md` for injection verification.
- **Why:** Close the doc chain gap flagged by `ngram validate`.
- **Impact:** Scraping module now has a HEALTH doc placeholder with manual checks.

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md` and updated `TEST_World_Scraping.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** Scraping module documentation is now compliant; Health checks are anchored to YAML output and injection.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code. Focus on keeping the scraping doc chain aligned with `data/scripts/scrape/**` and the YAML outputs.

## TODO

- [ ] Reconfirm OpenDomesday availability or identify an alternate API.
- [ ] Add an automated diff report between pipeline runs to spot regressions.

## POINTERS

- `docs/world/scraping/ALGORITHM_Pipeline.md` for the five-phase flow.
- `data/scripts/inject_world.py` for the database loading logic.

## CHAIN

```
THIS:            SYNC_World_Scraping.md (you are here)
PATTERNS:        ./PATTERNS_World_Scraping.md
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
TEST:            ./TEST_World_Scraping.md
```

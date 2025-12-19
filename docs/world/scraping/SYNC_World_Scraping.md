# World Scraping — State & Progress

**Last Updated:** 2025-12-19
**Status:** COMPLETE (Enriched)
**Database:** `seed` (FalkorDB)

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Scraping.md
BEHAVIORS:       ./BEHAVIORS_World_Scraping.md
ALGORITHM:       ./ALGORITHM_Pipeline.md
VALIDATION:      ./VALIDATION_World_Scraping.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md
TEST:            ./TEST_World_Scraping.md
THIS:            SYNC_World_Scraping.md (you are here)
```

---

## Maturity

STATUS: DESIGNING

The scraping pipeline and YAML outputs are stable enough for repeatable
seed-world imports, but ongoing documentation consolidation means the module
remains in DESIGNING until the pipeline is fully verified end-to-end.

---

## Current State

Pipeline phases 1–6 are complete, YAML outputs are present in `data/world/`,
and the `seed` database is populated via `data/scripts/inject_world.py`. The
documentation chain is now consolidated under `ALGORITHM_Pipeline.md`.

---

## In Progress

No new scrape phases are active. Current work is documentation hygiene only,
including ensuring template sections remain complete and aligning SYNC notes
with the canonical algorithm and implementation docs.

---

## Phase Status

| Phase | Name | Status | Output |
|-------|------|--------|--------|
| 1 | Geography | **COMPLETE** | `places.yaml`, `places_minor.yaml`, `routes.yaml` |
| 2 | Political | **COMPLETE** | `characters.yaml`, `holdings.yaml` |
| 3 | Events | **COMPLETE** | `events.yaml` |
| 4 | Narratives | **COMPLETE** | `narratives.yaml`, `beliefs.yaml` |
| 5 | Tensions | **COMPLETE** | `tensions.yaml` |
| 6 | Things | **COMPLETE** | `things.yaml`, `thing_locations.yaml`, `thing_ownership.yaml` |

---

## Current Counts (YAML)

| Data Type | Previous | Current | Added |
|-----------|----------|---------|-------|
| Places (main) | 62 | 62 | — |
| Places (minor) | 0 | 26 | +26 |
| Routes | 113 | 113 | — |
| Characters | 39 | 49 | +10 |
| Holdings | 56 | 56 | — |
| Things | 0 | 28 | +28 |
| Thing Locations | 0 | 24 | +24 |
| Thing Ownership | 0 | 11 | +11 |
| Events | 22 | 22 | — |
| Narratives | 77 | 141 | +64 |
| Beliefs | 1,520 | ~2,040 | +520 |
| Tensions | 17 | 22 | +5 |

---

## New Content: Characters

### Historical Figures (Outside Yorkshire)

| Character | Role | Location |
|-----------|------|----------|
| Eadric the Wild | Resistance leader | Welsh marches (rumored) |
| Gytha | Harold's mother | Exeter (funding resistance) |
| Godwine Haroldson | Harold's eldest son | Ireland (gathering ships) |
| Edmund Haroldson | Harold's son | Ireland |
| Magnus Haroldson | Harold's son | Ireland |
| Aldgyth | Harold's widow, Edwin/Morcar's sister | Hiding |

---

## New Content: Tensions

| Tension | Pressure | Type | Description |
|---------|----------|------|-------------|
| Harold's sons return | 0.6 | scheduled (1068-06) | Ships gathering in Dublin |
| Galtres Wolves | 0.35 | gradual | Wulfric grows bolder |
| Siward Barn rising | 0.3 | event | Waiting for the Danes |
| Gytha at Exeter | 0.5 | scheduled (1068-01) | William will march west |
| Aldgyth prize | 0.25 | gradual | Someone will find her |

---

## Narrative Breakdown (Updated)

| Type | Count |
|------|-------|
| control | 37 |
| memory | 35 |
| rumour | 25 |
| belief | 15 |
| claim | 8 |
| secret | 7 |
| reputation | 6 |
| debt | 3 |

---

## Data Sources

| Source | URL | Status | Notes |
|--------|-----|--------|-------|
| OpenDomesday | opendomesday.org/api/ | **DOWN (404)** | API not responding |
| OSM/Nominatim | nominatim.openstreetmap.org | **USED** | Geocoding |
| Manual Historical | - | **USED** | Domesday records, Anglo-Saxon Chronicle |
| Claude Knowledge | - | **USED** | Historical figures, things, outlaw bands |

---

## Recent Changes

Recent documentation updates focused on consolidation and alignment rather
than new scraping features or additional YAML outputs.

### 2025-12-19: Completed patterns template sections

- **What:** Added THE PROBLEM, THE PATTERN, PRINCIPLES, DEPENDENCIES,
  INSPIRATIONS, SCOPE, and GAPS / IDEAS / QUESTIONS to the world scraping
  patterns doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the patterns document without
  changing the pipeline behavior or YAML outputs.
- **Files:** `docs/world/scraping/PATTERNS_World_Scraping.md`

### 2025-12-19: Expanded SYNC template coverage

- **What:** Filled missing SYNC sections (maturity, current state, in progress,
  known issues, handoffs, todo, consciousness trace, pointers).
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the scraping SYNC without changing
  behavior or data outputs.
- **Files:** `docs/world/scraping/SYNC_World_Scraping.md`

### 2025-12-19: Filled behaviors template sections

- **What:** Added BEHAVIORS, INPUTS/OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and
  GAPS/IDEAS/QUESTIONS sections with expanded notes for the scraping pipeline.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the world scraping behaviors doc.
- **Files:** `docs/world/scraping/BEHAVIORS_World_Scraping.md`

### 2025-12-19: Expanded validation template coverage

- **What:** Added invariants, properties, error conditions, test coverage, and
  verification procedure guidance to the validation doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT and keep validation expectations explicit.
- **Files:** `docs/world/scraping/VALIDATION_World_Scraping.md`

### 2025-12-19: Filled implementation template sections

- **What:** Added the missing implementation template sections (schema, logic
  chains, module dependencies, state management, runtime behavior, concurrency
  model, configuration, bidirectional links, and gaps framing) to the world
  scraping implementation architecture doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the implementation doc without
  changing code or pipeline behavior.
- **Files:** `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`

### 2025-12-19: Verified implementation doc file list

- **What:** Confirmed the implementation doc already lists all scrape scripts and current `data/world/` YAML outputs (including things and minor places).
- **Why:** Close the stale implementation warning without changing code.
- **Files:** `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`

### 2025-12-19: Consolidated scraping algorithm docs

- **What:** Merged phase algorithm docs into `ALGORITHM_Pipeline.md` and removed duplicates.
- **Why:** Keep one canonical ALGORITHM doc for the scraping module.
- **Files:** `docs/world/scraping/ALGORITHM_Pipeline.md`, `docs/world/scraping/PATTERNS_World_Scraping.md`

### 2025-12-19: Filled algorithm template sections

- **What:** Added the missing algorithm template sections (overview, data
  structures, primary algorithm steps, decisions, data flow, complexity,
  helpers, interactions, gaps) to the scraping pipeline doc.
- **Why:** Resolve DOC_TEMPLATE_DRIFT and keep the pipeline algorithm
  documentation template-complete.
- **Files:** `docs/world/scraping/ALGORITHM_Pipeline.md`

### 2025-12-19: Verified implementation architecture doc

- **What:** Verified the implementation doc exists and the chain points to it; recorded refactoring targets for oversized scripts.
- **Why:** Confirmed the documentation chain is complete for the module.
- **Files:** `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`, `docs/world/scraping/PATTERNS_World_Scraping.md`

### 2025-12-19: Repaired implementation file references

- **What:** Updated the scraping implementation doc to use concrete paths for world YAML outputs and GraphOps, and removed non-existent file targets from extraction notes.
- **Why:** Fix broken link checks for the pipeline implementation doc.
- **Files:** `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`

### 2025-12-19: Normalized remaining implementation paths

- **What:** Replaced remaining glob-style YAML references in the scraping implementation doc with concrete directory paths.
- **Why:** Ensure all implementation references resolve to existing paths.
- **Files:** `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`

### 2025-12-19: Documented thing and minor-place YAML inputs

- **What:** Added missing world data YAML files (minor places, things, thing links) to the implementation architecture doc, along with injection notes.
- **Why:** Keep the implementation doc aligned with the YAML inputs actually loaded by `data/scripts/inject_world.py`.
- **Files:** `docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`

### 2025-12-19: Expanded test coverage template

- **What:** Filled the missing TEST sections (strategy, unit/integration,
  edge cases, coverage, run steps, gaps, flaky tracking, questions) and
  expanded short entries to meet the template guidance.
- **Why:** Resolve DOC_TEMPLATE_DRIFT for the scraping test doc without
  changing pipeline behavior or YAML outputs.
- **Files:** `docs/world/scraping/TEST_World_Scraping.md`

---

## Blockers Resolved

- [x] ~~Verify OpenDomesday API~~ → Down, used manual data
- [x] ~~Find reliable coordinate source~~ → OSM Nominatim
- [x] ~~Need human review for character selection~~ → Core 49 selected
- [x] ~~Schema compliance~~ → All fields populated
- [x] ~~Database injection~~ → `seed` database ready
- [x] ~~Add Things/Items~~ → 28 things with locations and ownership
- [x] ~~Add minor locations~~ → 26 locations (crossings, ruins, camps)
- [x] ~~Add outlaw bands~~ → 4 bands with leaders and territories
- [x] ~~Add historical figures~~ → 6 characters outside Yorkshire

---

## Optional Expansion

| Task | Priority |
|------|----------|
| Add scops/bards (traveling storytellers) | Medium |
| Add songs and tales (as narratives) | Medium |
| Add marriage alliances (narrative links) | Medium |
| Add garrison strengths (narratives) | Low |
| Add more female characters | Medium |
| Add patrol routes (narratives) | Low |


---

## Known Issues

OpenDomesday remains unavailable (404), so historical verification depends on
manual sources and Claude knowledge. Data/scripts remain gitignored, which
prevents DOCS references unless the ignore rules are adjusted.

---

## Handoff: For Agents

Use VIEW_Implement_Write_Or_Modify_Code. Focus on keeping the scraping doc
chain aligned with `data/scripts/scrape/**` and the YAML outputs listed here,
especially if new phases or new data sources are added.

---

## Handoff: For Human

World scraping data is stable and injected into the `seed` database. No code
changes were required for this repair; only SYNC coverage was expanded to
match the template and keep documentation consistent.

---

## TODO

- [ ] Reconfirm OpenDomesday availability or identify a durable alternate API.
- [ ] Decide whether to whitelist `data/scripts/` for DOCS references.

---

## Consciousness Trace

This update is strictly a documentation template alignment pass. The main
uncertainty is whether the pipeline is considered canonical despite the
external API outage; staying in DESIGNING preserves that caution.

---

## Pointers

See `docs/world/scraping/ALGORITHM_Pipeline.md` for the phase flow, and
`docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md`
for script entry points and YAML outputs.

---

## Updates

- Consolidated phase-level ALGORITHM docs into the canonical `docs/world/scraping/ALGORITHM_Pipeline.md` and left per-phase stubs as redirects.
- Verified the IMPLEMENTATION doc is present and linked across scraping docs.
- DOCS references are still absent in `data/scripts/` because the directory is gitignored; add an exception if code-doc linking is required.

## Agent Observations

### Remarks
- Behaviors doc now spells out pipeline expectations, but source citation
  handling still needs a clear multi-citation standard.
- Patterns doc now captures the missing template sections to align with the
  scrape pipeline scope and dependencies.
- Template sections were filled in this SYNC to resolve doc drift without
  altering scraping behavior or data outputs.
- Algorithm doc now captures data structures and decisions for future audits.

### Suggestions
- [ ] Add a short provenance policy to `VALIDATION_World_Scraping.md` so
  multi-source attribution is consistently enforced.

### Propositions
- Consider a follow-up doc pass to align export format expectations with
  downstream validation tooling and diff workflows.

---

## Agent Observations

### Remarks
- Validation now captures the required invariants and verification steps for the pipeline.
- Implementation doc now documents injection CLI flags and the sequential
  runtime/concurrency expectations for the pipeline scripts.

### Suggestions
- [ ] Add an automated diff report between pipeline runs to spot regressions.
- [ ] Add `DOCS:` references to the scrape phase scripts if ignore rules allow it.

### Propositions
- Consider a lightweight validation script that checks minor place and thing linkage integrity.

## ARCHIVE

Older content archived to: `SYNC_World_Scraping_archive_2025-12.md`

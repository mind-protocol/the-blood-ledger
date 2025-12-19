# World Builder — Test Overview

```
STATUS: DRAFT
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_World_Builder.md
BEHAVIORS:       ../BEHAVIORS_World_Builder.md
ALGORITHM:       ../ALGORITHM/ALGORITHM_Overview.md
VALIDATION:      ../VALIDATION/VALIDATION_Overview.md
IMPLEMENTATION:  ../IMPLEMENTATION/IMPLEMENTATION_Overview.md
THIS:            TEST_Overview.md (you are here)
DETAILS:         ./TEST_Cases.md
SYNC:            ../SYNC_World_Builder.md

IMPL:            tests/infrastructure/world_builder/test_world_builder.py
```

---

## Test Strategy

- Unit tests isolate graph, embeddings, and LLM calls with mocks.
- Integration tests (future) cover real FalkorDB and physics flow.
- Focus areas: query moments, sparsity detection, enrichment application, error handling.

---

## Suites (High-Level)

- Sparsity detection
- Query moment recording
- WorldBuilder enrichment and caching
- Enrichment application
- Query interface
- Edge cases and invariants

---

## How To Run

```bash
pytest tests/infrastructure/world_builder/test_world_builder.py -v
```

---

## Known Gaps

- Integration coverage with real FalkorDB
- Performance/regression benchmarks
- LLM quality validation

---

## Archive Note

Detailed test matrices and fixture examples were trimmed; see `../archive/SYNC_archive_2024-12.md`.

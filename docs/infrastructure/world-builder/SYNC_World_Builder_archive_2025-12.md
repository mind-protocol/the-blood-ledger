# Archived: SYNC_World_Builder.md

Archived on: 2025-12-19
Original file: SYNC_World_Builder.md

---

## Recent Changes

### 2025-12-19 — Normalize world-builder implementation file references

- Added the `__init__.py` entry to the implementation doc and replaced bare dependency references with full `engine/infrastructure/world_builder/**` paths.

### 2025-12-19 — Repair 34 BROKEN_IMPL_LINK verification

- Verified the world-builder implementation doc references are normalized to full paths and no broken links remain.

### 2025-12-19 — Fix world-builder implementation doc file links

- Normalized world-builder IMPLEMENTATION file references to full `engine/infrastructure/world_builder/**` paths.
- Updated semantic search reference to `engine/world/map/semantic.py` and removed backticks from numeric defaults to avoid broken link checks.

### 2025-12-19 — Documentation mapping verification (repair 23)

- Confirmed `engine/infrastructure/world_builder/**` is mapped in `modules.yaml`.
- Confirmed all world-builder source files already contain DOCS references.
- No code or doc chain changes required for the undocumented mapping report.

### 2025-12-19 — Linked world-builder tests to docs

- Added a DOCS reference in `tests/infrastructure/world_builder/__init__.py`.
- Corrected the TEST doc IMPL path to `tests/infrastructure/world_builder/test_world_builder.py`.

### 2025-12-19 — Documentation chain completion

- Added `PATTERNS_World_Builder.md` and `BEHAVIORS_World_Builder.md` to complete the world-builder doc chain and align CHAIN links.
- Added the world-builder module mapping in `modules.yaml` for discovery and validation.

### 2025-12-19 — Repair verification (world_builder.py, repair 03-INCOMPLETE_IMPL)

- Confirmed `_hash_query` and `clear_cache` are already implemented in `engine/infrastructure/world_builder/world_builder.py`; no code changes required for this repair run.

### 2025-12-19 — Repair revalidation (world_builder.py, repair 03-INCOMPLETE_IMPL)

- Confirmed `_hash_query` and `clear_cache` are already implemented in `engine/infrastructure/world_builder/world_builder.py`; no code changes required for this repair run.

### 2025-12-19 — Repair revalidation (world_builder.py)

- Rechecked `_hash_query` and `clear_cache` in `engine/infrastructure/world_builder/world_builder.py`; both are already implemented, so no code changes were needed for this repair run.

### 2025-12-19 — Repair verification (world_builder.py, repair 04-INCOMPLETE_IMPL)

- Confirmed `_hash_query` and `clear_cache` are already implemented in `engine/infrastructure/world_builder/world_builder.py`; no code changes required for this repair run.

### 2025-12-19 — Repair verification (world_builder.py)

- Verified `_hash_query` and `clear_cache` implementations in `engine/infrastructure/world_builder/world_builder.py`; repair task was stale and required no code changes.

### 2025-12-19 — Added agent CLI wrapper path for enrichment

- Added a shared agent CLI wrapper (`engine/infrastructure/orchestration/agent_cli.py`) and wired World Builder to use it exclusively (no SDK path).
- Updated implementation docs to reflect the CLI-only dependency.

### 2025-12-19 — Tests Implemented

- Created `tests/infrastructure/world_builder/test_world_builder.py`
- 49 unit tests passing covering all modules
- Test categories: sparsity, query moment, world builder, enrichment, query interface, edge cases, invariants

### 2025-12-19 — Documentation Complete

- Created VALIDATION_World_Builder.md with 8 invariants, 5 properties, 6 error conditions
- Created TEST_World_Builder.md with comprehensive test plan
- All docs in chain now exist

### 2025-12-19 — Initial Implementation

- Created complete module structure
- Implemented semantic sparsity detection with 4 metrics
- Implemented query moment recording (queries as thoughts)
- Implemented LLM enrichment with YAML parsing
- Implemented universal `query()` and `query_sync()` functions
- All created content marked with `generated: true`
- Enriched content links back to query moment via ABOUT

---


## Integration Points

### Consumes

| Service | How | For |
|---------|-----|-----|
| `SemanticSearch` | `engine.world.map.semantic` | Vector search |
| `GraphQueries` | `engine.physics.graph` | Graph operations |
| `Embeddings` | `engine.infrastructure.embeddings` | Sparsity check |
| `Claude/Codex CLI` | `engine/infrastructure/orchestration/agent_cli.py` | LLM enrichment (CLI only) |

### Provides

| Export | Purpose |
|--------|---------|
| `query()` | Async universal query with enrichment |
| `query_sync()` | Sync query without enrichment |
| `WorldBuilder` | Enrichment service class |
| `is_sparse()` | Sparsity detection |
| `SparsityResult` | Sparsity metrics dataclass |

---


## Usage Example

```python
from engine.infrastructure.world_builder import query, query_sync

# Async with enrichment (creates content if sparse)
results = await query(
    "What do I know about Edmund?",
    graph,
    char_id="char_aldric",
    place_id="place_camp"
)

# Sync without enrichment (just search + record)
results = query_sync(
    "memories of home",
    graph,
    char_id="char_player"
)
```

---


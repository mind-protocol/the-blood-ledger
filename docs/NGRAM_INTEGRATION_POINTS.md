# Ngram Integration Points

## Overview

This document describes how the blood-ledger engine integrates with the `~/ngram` service for all graph database interactions. The integration uses a **proxy module pattern** where `engine/physics/graph/` re-exports the `GraphQueries` class from the ngram repository.

**Status:** ✅ **Integration Complete**

## Architecture

### Proxy Module Pattern

The integration uses a proxy approach rather than duplicating code:

```
engine/physics/graph/__init__.py
    └── imports from: ~/ngram/ngram/db/graph_queries.py
         └── GraphQueries class (FalkorDB client)
```

**Key files:**
- `engine/physics/graph/__init__.py` - Proxy that re-exports `GraphQueries` from ngram
- `~/ngram/ngram/db/graph_queries.py` - Actual implementation (FalkorDB client)

### GraphQueries Interface

The `GraphQueries` class from ngram provides:

- `query(cypher_query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]` - Execute raw Cypher
- `get_character(char_id: str) -> Dict[str, Any]` - Fetch character node
- `get_place(place_id: str) -> Dict[str, Any]` - Fetch place node

## Integration Points

All integration points now use `GraphQueries` via `from engine.physics.graph import GraphQueries`, which proxies to ngram.

### 1. Canon & Narrative State (`engine/infrastructure/canon/`) ✅

* **File:** `engine/infrastructure/canon/canon_holder.py`
  * **Class:** `CanonHolder`
  * **Usage:** Instantiates `GraphQueries` in `__init__`.
  * **Operations:**
    * `record_to_canon`: Executes Cypher to update moment status to 'spoken', set tick, and apply energy costs.
  * **Status:** ✅ Uses ngram `GraphQueries` via proxy.

* **File:** `engine/infrastructure/canon/speaker.py`
  * **Function:** `determine_speaker`
  * **Usage:** Accepts a graph instance.
  * **Operations:** Complex queries to resolve who speaks a moment based on location and status.
  * **Status:** ✅ Works with ngram `GraphQueries`.

### 2. World Builder (`engine/infrastructure/world_builder/`) ✅

* **File:** `engine/infrastructure/world_builder/query.py`
  * **Function:** `query` and `query_sync`
  * **Usage:** Accepts `graph` argument (expected to be `GraphQueries`).
  * **Operations:**
    * `record_query_moment`: Creates new moment nodes.
    * `_create_count_links_fn`: Executes raw Cypher to count edges.
    * `_build_enrichment_context`: Calls `graph.get_character` and `graph.get_place`.
  * **Status:** ✅ Compatible with ngram `GraphQueries` interface.

* **File:** `engine/infrastructure/world_builder/enrichment.py`
  * **Function:** `apply_enrichment`
  * **Usage:** Accepts `graph` argument.
  * **Operations:** Extensive `MERGE` and `CREATE` Cypher queries to generate:
    * Characters, Places, Things, Narratives, Links, Moments.
  * **Status:** ✅ ngram `GraphQueries.query()` supports all write operations.

* **File:** `engine/infrastructure/world_builder/sparsity.py`
  * **Function:** `is_sparse`
  * **Usage:** Uses `count_links_fn` (which wraps a DB query).
  * **Status:** ✅ Works via the graph callback.

### 3. Semantic Search (`engine/world/map/`) ✅

* **File:** `engine/world/map/semantic.py`
  * **Class:** `SemanticSearch`
  * **Usage:** Instantiates `GraphQueries`.
  * **Operations:**
    * `_vector_search`: Executes `CALL db.idx.vector.queryNodes` (FalkorDB vector procedure).
    * `_get_node_with_embedding`: Retrieves node data.
    * `_fallback_search`: Brute-force node scan (backup).
  * **Status:** ✅ ngram `GraphQueries.query()` supports FalkorDB vector procedures.
  * **Note:** Results returned as `List[Dict]` with `r.get('similarity', 0)` access pattern.

### 4. Configuration (`engine/run.py`) ✅

* **File:** `engine/run.py`
  * **Usage:** Sets environment variables `GRAPH_NAME`, `FALKORDB_HOST`, `FALKORDB_PORT`.
  * **Status:** ✅ ngram `GraphQueries` reads these same environment variables.

## Agent Integration ✅

The high-level agents (Narrator, World Runner, World Builder) defined in `agents/` are markdown-based prompts that are executed via `agent_cli.py`. They interact with the system by invoking the *implementation code* listed above.

* **Narrator:** Relies on `CanonHolder` and `Speaker` logic. ✅
* **World Builder:** Relies on `world_builder/query.py` and `enrichment.py`. ✅

Since all engine infrastructure uses the ngram `GraphQueries` via the proxy, agents are automatically integrated.

## Implementation Summary

The integration was completed using a **proxy pattern**:

1. ✅ **Proxy Module:** `engine/physics/graph/__init__.py` re-exports `GraphQueries` from `~/ngram/ngram/db/graph_queries.py`
2. ✅ **No Code Changes:** Existing imports (`from engine.physics.graph import GraphQueries`) work unchanged
3. ✅ **Interface Compatibility:** ngram's `GraphQueries.query()` returns `List[Dict[str, Any]]`, matching expected usage
4. ✅ **Vector Search:** FalkorDB vector procedures work via `query()` method
5. ✅ **Environment Config:** ngram reads the same `FALKORDB_HOST`, `FALKORDB_PORT`, `GRAPH_NAME` env vars

## Maintenance Notes

- The proxy lives at `engine/physics/graph/__init__.py`
- The actual implementation is in the ngram repository at `~/ngram/ngram/db/graph_queries.py`
- Changes to the ngram `GraphQueries` API will automatically propagate to blood-ledger
- Ensure ngram is available in the Python path (typically via shared parent or symlink)

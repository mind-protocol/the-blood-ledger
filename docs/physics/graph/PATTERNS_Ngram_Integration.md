# PATTERNS: Ngram Integration

**Module:** `engine.physics.graph`
**Context:** Migrating database persistence from direct FalkorDB connections to the `~/ngram` service.

---

## 1. The Core Problem

The current engine accesses the graph database (FalkorDB) directly via the `GraphQueries` class.
To support the distributed agent architecture, we must route all persistence and graph operations through the `~/ngram` service (likely via a local socket or API) instead of managing direct database connections.

### Constraints
1.  **Interface Compatibility:** The rest of the engine (Canon, World Builder) expects a specific method signature from `GraphQueries`.
2.  **Vector Search:** The `SemanticSearch` module relies on specific FalkorDB vector procedures (`db.idx.vector.queryNodes`) which may not be directly exposed or supported by `ngram` in the same way.
3.  **Performance:** `ngram` integration must not introduce significant latency for high-frequency operations (like `canon.record_to_canon`).

---

## 2. Solution Pattern: The Adapter Strategy

We will replace the existing `GraphQueries` implementation with a **Client Adapter** pattern.

### The `NgramGraphClient`

Instead of rewriting every call site, we implement `NgramGraphClient` which adheres to the existing `GraphQueries` interface but delegates actual execution to `ngram`.

```python
class NgramGraphClient:
    def __init__(self, connection_string: str):
        self.client = NgramClient(connection_string)

    def query(self, cypher: str, params: Dict) -> List[Dict]:
        # Adapt Cypher if necessary
        # Send to ngram
        # Transform response to expected List[Dict] format
        pass
```

### Integration Points Strategy

| Component | Strategy |
|-----------|----------|
| **CanonHolder** | **Direct Replacement.** Inject `NgramGraphClient` instead of `GraphQueries`. The strict schema and simple queries here make this low-risk. |
| **World Builder** | **Direct Replacement.** The `query()` interface is generic enough. Entity creation (characters, places) logic remains in Python but writes via `ngram`. |
| **Semantic Search** | **Refactor Required.** The `SemanticSearch` class currently builds raw FalkorDB vector queries. We must update `SemanticSearch` to use `ngram`'s native search capabilities if available, or expose a `vector_query` method in the client. |

---

## 3. Data Flow

**Current:**
`Engine -> GraphQueries -> [TCP/IP] -> FalkorDB`

**New:**
`Engine -> NgramGraphClient -> [Socket/HTTP] -> ~/ngram -> [Unknown] -> Persistence`

---

## 4. Vector Search Approach

The most critical technical risk is `engine/world/map/semantic.py`.

**Plan A (Preferred): Ngram Native Search**
If `ngram` exposes a semantic search API (e.g., `client.search(text)`), we rewrite `SemanticSearch.find()` to use it, bypassing the embedding generation and vector query construction in our code.

**Plan B (Fallback): Passthrough**
If `ngram` allows raw Cypher execution including procedure calls, we keep the existing logic and just tunnel the query string.

---

## 5. Principles

*   **Transparency:** The rest of the engine should not know it's talking to `ngram`.
*   **Resilience:** Handle `ngram` service unavailability gracefully (retries/errors).
*   **Traceability:** All queries sent to `ngram` should carry context (agent ID, tick) if supported.

# IMPLEMENTATION: Ngram Client Adapter

**Module:** `engine.physics.graph`
**Implements:** `PATTERNS_Ngram_Integration.md`

---

## 1. Class Structure

We need to create `engine/physics/graph/client.py` (or modify `__init__.py` if that's where `GraphQueries` lived/was mocked).

### `NgramGraphClient`

```python
class NgramGraphClient:
    """
    Adapter for the ~/ngram service.
    Implements the interface expected by CanonHolder and WorldBuilder.
    """
    
    def __init__(self, socket_path: str = None, host: str = None, port: int = None):
        # Initialize connection to ngram
        pass

    def query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Executes a Cypher query via ngram.
        Returns a list of dictionaries (nodes/relationships/maps).
        """
        pass

    def get_character(self, char_id: str) -> Optional[Dict]:
        """Convenience method used by WorldBuilder."""
        # Cypher: MATCH (c:Character {id: $id}) RETURN c
        pass

    def get_place(self, place_id: str) -> Optional[Dict]:
        """Convenience method used by WorldBuilder."""
        # Cypher: MATCH (p:Place {id: $id}) RETURN p
        pass
```

## 2. Refactoring Targets

### `engine/infrastructure/canon/canon_holder.py`

**Change:**
```python
# Old
self._queries = GraphQueries(graph_name=..., host=..., port=...)

# New
from engine.physics.graph import NgramGraphClient
self._queries = NgramGraphClient(socket_path=os.getenv("NGRAM_SOCKET"))
```

### `engine/world/map/semantic.py`

**Change:**
The method `_vector_search` constructs a specific FalkorDB procedure call:
`CALL db.idx.vector.queryNodes('Node', 'embedding', ...)`

We need to verify if `ngram` supports this. If not, `SemanticSearch` needs to call:
`self.client.vector_search(embedding, limit, node_types)`

## 3. Configuration

Update `engine/run.py` to accept `ngram` connection args:

```python
# run.py
parser.add_argument('--ngram-socket', help='Path to ngram socket')
# ...
os.environ['NGRAM_SOCKET'] = args.ngram_socket
```

## 4. Migration Steps

1.  **Draft the Client:** Create `engine/physics/graph/client.py`.
2.  **Mock/Stub:** Initially, this client can just log queries or connect to FalkorDB directly (temporary) to prove the interface works.
3.  **Connect:** Switch the internal implementation to talk to `~/ngram`.
4.  **Cutover:** Update `CanonHolder` and `WorldBuilder` to instantiate the new client.

# Embeddings — Algorithm: Indexing and Search Procedures

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Embeddings.md
BEHAVIORS:   ./BEHAVIORS_Embeddings.md
THIS:        ALGORITHM_Embeddings.md (you are here)
VALIDATION:  ./VALIDATION_Embeddings.md
IMPLEMENTATION: ./IMPLEMENTATION_Embeddings.md
TEST:        ./TEST_Embeddings.md
SYNC:        ./SYNC_Embeddings.md
IMPL:        ../../../engine/infrastructure/embeddings/service.py
```

---

## OVERVIEW

The embedding system has two primary operations:

1. **Indexing** — Convert detail text to vectors and store with source references
2. **Searching** — Find similar content via vector similarity

All operations use local sentence-transformers models for fast, cheap embedding generation.

---

## DATA STRUCTURES

### Embedding Record

```yaml
Embedding:
  id: string              # emb_{source_type}_{source_id}_{field}
  text: string            # The actual text (for debugging/display)
  vector: float[]         # The embedding vector (384 or 768 dims)

  # Source reference
  source_type: string     # narrative | character | place | tension | link | conversation
  source_id: string       # narr_oath | char_aldric | link_uuid | null
  source_field: string    # detail | convo

  # For links: what nodes it connects
  link_from: string       # char_player
  link_to: string         # narr_oath
  link_type: string       # BELIEVES | PRESENT | CARRIES

  # For conversations (not in graph)
  source_file: string     # "conversations/char_aldric.md"
  source_section: string  # "Day 4, Night — The Camp"

  created_at: string      # ISO timestamp
```

### Search Result

```python
@dataclass
class SearchResult:
    source_type: str
    source_id: str
    source_field: str
    text: str
    score: float

    # Link-specific
    link_from: Optional[str] = None
    link_to: Optional[str] = None
    link_type: Optional[str] = None

    # Conversation-specific
    source_file: Optional[str] = None
    source_section: Optional[str] = None
```

---

## ALGORITHM: index_node()

Embed a node's `detail` field, falling back to `name`. Stores embedding as node attribute.

### Step 1: Select Text to Embed

```python
def index_node(node: dict) -> Optional[List[float]]:
    detail = node.get('detail', '')
    name = node.get('name', '')

    # Prefer detail, fallback to name
    if detail and len(detail) > 20:
        text = detail
    elif name and len(name) > 20:
        text = name
    else:
        return None  # Nothing to embed
```

### Step 2: Generate Embedding

```python
    vector = embed(text)  # sentence-transformers, 768 dims
```

### Step 3: Store as Node Attribute

```python
    node['embedding'] = vector
    # Update in graph:
    # MATCH (n {id: $id}) SET n.embedding = $vector
    return vector
```

---

## ALGORITHM: index_link()

Embed a link's `detail` field if > 20 chars. Stores embedding as link attribute.

### Step 1: Check Detail

```python
def index_link(link: dict) -> Optional[List[float]]:
    detail = link.get('detail', '')

    if not detail or len(detail) <= 20:
        return None  # Links don't have name fallback
```

### Step 2: Generate Embedding

```python
    vector = embed(detail)  # sentence-transformers, 768 dims
```

### Step 3: Store as Link Attribute

```python
    link['embedding'] = vector
    # Update in graph:
    # MATCH ()-[r {id: $id}]->() SET r.embedding = $vector
    return vector
```

---

## ALGORITHM: search()

Search embeddings by vector similarity.

### Step 1: Embed Query

```python
def search(query: str, limit: int = 10) -> List[SearchResult]:
    query_vector = embed(query)
```

### Step 2: Vector Similarity Search

```python
    # Search all embeddings (FalkorDB vector index)
    raw_results = vector_search(query_vector, limit=limit * 2)
```

### Step 3: Group by Source (Deduplicate)

```python
    # Keep best match per source
    grouped = {}
    for emb in raw_results:
        key = (emb.source_type, emb.source_id)
        if key not in grouped or emb.score > grouped[key].score:
            grouped[key] = emb
```

### Step 4: Convert to SearchResult

```python
    results = []
    for emb in sorted(grouped.values(), key=lambda x: x.score, reverse=True)[:limit]:
        results.append(SearchResult(
            source_type=emb.source_type,
            source_id=emb.source_id,
            source_field=emb.source_field,
            text=emb.text,
            score=emb.score,
            link_from=emb.link_from,
            link_to=emb.link_to,
            link_type=emb.link_type,
            source_file=emb.source_file,
            source_section=emb.source_section
        ))
    return results
```

---

## ALGORITHM: index_world()

Batch index all existing content on game start.

```python
def index_world():
    # Index all nodes
    for node in graph.get_all_nodes():
        index_node(node)

    # Index all links
    for link in graph.get_all_links():
        index_link(link)
```

---

## ALGORITHM: on_scene_end()

Incremental indexing after each scene.

```python
def on_scene_end(mutations: List[dict]):
    # Index new/updated nodes
    for mutation in mutations:
        if mutation['type'] in ['new_narrative', 'new_character', 'update_node']:
            index_node(mutation['payload'])

        elif mutation['type'] in ['new_belief', 'update_link']:
            index_link(mutation['payload'])
```

---

## KEY DECISIONS

### D1: Embed or Skip

```
IF detail exists AND len(detail) > 20:
    embed(detail)
ELSE:
    skip (return None)
```

### D2: ID Generation Strategy

```
Nodes:         emb_{type}_{id}_detail
Links:         emb_link_{link_type}_{link_id}_detail
Conversations: emb_convo_{char_id}_{slugified_section}
```

Deterministic IDs allow upsert without checking existence.

### D3: Deduplication in Search

```
IF multiple embeddings from same source match:
    keep highest score only
```

Prevents one detailed node from dominating results.

---

## DATA FLOW

```
Node/Link Created
    ↓
Check detail > 20 chars
    ↓ Yes              ↓ No
Generate vector       Skip
    ↓
Store embedding
    ↓
Vector index updated
```

```
Search Query
    ↓
Embed query
    ↓
Vector similarity search
    ↓
Group by source
    ↓
Return top N results
```

---

## COMPLEXITY

**index_node() / index_link():**
- Time: O(T) where T = text length (embedding model)
- Space: O(D) where D = embedding dimension (768)

**search():**
- Time: O(N * D) for brute force, O(log N * D) with index
- Space: O(limit * D)

**index_world():**
- Time: O(N * T) where N = total nodes/links/sections
- Space: O(N * D) for all embeddings

**Bottlenecks:**
- Initial world indexing (~1000 embeddings) takes ~30 seconds
- Individual embedding ~50ms per text

---

## VECTOR STORAGE IN FALKORDB

### Create Vector Index (Per Node Label)

```cypher
CREATE VECTOR INDEX narrative_emb_idx
FOR (n:Narrative) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}

CREATE VECTOR INDEX character_emb_idx
FOR (n:Character) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}

-- Repeat for Place, Tension, etc.
```

### Search Query

```cypher
CALL db.idx.vector.queryNodes('narrative_emb_idx', $limit, $query_vector)
YIELD node, score
RETURN node.id, node.name, node.detail, score
ORDER BY score DESC
```

### Set Embedding on Node

```cypher
MATCH (n:Narrative {id: $id})
SET n.embedding = $vector
```

### Set Embedding on Link

```cypher
MATCH ()-[r:BELIEVES {id: $id}]->()
SET r.embedding = $vector
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| sentence-transformers | model.encode(text) | Vector [768 floats] |
| FalkorDB | vector index query | Similar embeddings |
| GraphQueries | get_all_nodes() | Nodes to index |
| ConversationThread | read_sections() | Conversation text |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Optimal chunk size for long detail fields?
- [ ] Should we store embeddings in separate DB for performance?
- [ ] Index invalidation when source deleted?
- IDEA: Use approximate nearest neighbor for faster search
- IDEA: Hybrid search (vector + keyword)
- QUESTION: FalkorDB vector index performance at 10K+ embeddings?

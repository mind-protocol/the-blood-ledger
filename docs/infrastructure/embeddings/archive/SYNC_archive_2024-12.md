# Embeddings — Archive (2024-12)

```
ARCHIVED_ON: 2025-12-19
SOURCE_MODULE: docs/infrastructure/embeddings
REASON: Reduce main doc size; retain historical detail and examples.
```

---

## ALGORITHM: STORAGE AND QUERY DETAILS (ARCHIVED)

### Vector Storage in FalkorDB

```cypher
CREATE VECTOR INDEX narrative_emb_idx
FOR (n:Narrative) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}

CREATE VECTOR INDEX character_emb_idx
FOR (n:Character) ON n.embedding
OPTIONS {dimension: 768, similarityFunction: 'cosine'}
```

```cypher
CALL db.idx.vector.queryNodes('narrative_emb_idx', $limit, $query_vector)
YIELD node, score
RETURN node.id, node.name, node.detail, score
ORDER BY score DESC
```

```cypher
MATCH (n:Narrative {id: $id})
SET n.embedding = $vector
```

```cypher
MATCH ()-[r:BELIEVES {id: $id}]->()
SET r.embedding = $vector
```

### External Interactions

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| sentence-transformers | model.encode(text) | Vector [768 floats] |
| FalkorDB | vector index query | Similar embeddings |
| GraphQueries | get_all_nodes() | Nodes to index |
| ConversationThread | read_sections() | Conversation text |

---

## BEHAVIORS: QUERY EXAMPLES (ARCHIVED)

### "What do I know about guilt?"

```python
results = search("guilt regret couldn't save")
# Expected matches include character, link, and conversation sources.
```

### "How did I get this ring?"

```python
results = search("ring father inheritance")
# Expected matches include link and narrative sources.
```

### "Dangerous places"

```python
results = search("dangerous threat wolves bandits")
# Expected matches include place sources.
```

---

## PATTERNS: SCALE ESTIMATES (ARCHIVED)

| Type | Count | Embeddable | Embeddings |
|------|-------|------------|------------|
| Narrative | ~250 | ~80% | ~200 |
| Character | ~120 | ~80% | ~100 |
| Place | ~215 | ~70% | ~150 |
| Tension | ~50 | 100% | ~50 |
| BELIEVES links | ~1500 | ~20% | ~300 |
| PRESENT links | ~50 | ~60% | ~30 |
| CARRIES links | ~50 | ~40% | ~20 |
| Conversation chunks | ~200 | — | ~200 |
| **Total** | | | **~1,050** |

---

## TESTS: FIXTURES AND PERFORMANCE EXAMPLES (ARCHIVED)

### Mock Embedding Service

```python
class MockEmbeddingService:
    def embed(self, text: str) -> List[float]:
        import hashlib
        h = hashlib.md5(text.encode()).hexdigest()
        return [int(h[i:i+2], 16) / 255.0 for i in range(0, 32, 2)] * 48

    def similarity(self, v1, v2) -> float:
        return sum(a * b for a, b in zip(v1, v2)) / len(v1)
```

### Sample Fixtures

```python
@pytest.fixture
def sample_narrative_with_detail():
    return {
        "id": "narr_test",
        "type": "narrative",
        "name": "The Oath",
        "detail": "The rebellion began at dawn. Robert Cumin died in flames."
    }
```

### Performance Tests (Examples)

```python
def test_embed_latency():
    service = EmbeddingService()
    text = "Test text for embedding latency measurement."
    start = time.time()
    service.embed(text)
    elapsed = time.time() - start
    assert elapsed < 0.1
```

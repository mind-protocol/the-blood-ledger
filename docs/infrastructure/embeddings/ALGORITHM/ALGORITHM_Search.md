# Embeddings — Algorithm: Search

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Embeddings.md
BEHAVIORS:      ../BEHAVIORS_Embeddings.md
OVERVIEW:       ./ALGORITHM_Overview.md
INDEXING:       ./ALGORITHM_Indexing.md
THIS:           ALGORITHM/ALGORITHM_Search.md
VALIDATION:     ../VALIDATION_Embeddings.md
IMPLEMENTATION: ../IMPLEMENTATION_Embeddings.md
TEST:           ../TEST/TEST_Overview.md
SYNC:           ../SYNC_Embeddings.md
IMPL:           ../../../../engine/infrastructure/embeddings/service.py
```

---

## ALGORITHM: search()

Search embeddings by vector similarity.

```python
def search(query: str, limit: int = 10) -> List[SearchResult]:
    query_vector = embed(query)
    raw_results = vector_search(query_vector, limit=limit * 2)

    grouped = {}
    for emb in raw_results:
        key = (emb.source_type, emb.source_id)
        if key not in grouped or emb.score > grouped[key].score:
            grouped[key] = emb

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
            source_section=emb.source_section,
        ))
    return results
```

---

## KEY DECISIONS

### D3: Deduplication in Search

```
IF multiple embeddings from same source match:
    keep highest score only
```

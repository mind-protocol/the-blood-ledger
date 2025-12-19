# Embeddings — Algorithm Overview

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
THIS:           ALGORITHM/ALGORITHM_Overview.md
INDEXING:       ./ALGORITHM_Indexing.md
SEARCH:         ./ALGORITHM_Search.md
VALIDATION:     ../VALIDATION_Embeddings.md
IMPLEMENTATION: ../IMPLEMENTATION_Embeddings.md
TEST:           ../TEST/TEST_Overview.md
SYNC:           ../SYNC_Embeddings.md
IMPL:           ../../../../engine/infrastructure/embeddings/service.py
```

---

## OVERVIEW

The embedding system supports two primary operations:

1. **Indexing** — convert text fields into vectors and store on the source entity
2. **Search** — embed a query and return the closest sources by similarity

This algorithm layer describes the intended procedures. The current implementation
only covers embedding generation (see SYNC for spec gaps).

---

## DATA STRUCTURES

### Embedding Record (Logical)

```yaml
Embedding:
  id: string
  text: string
  vector: float[]

  source_type: string
  source_id: string
  source_field: string

  link_from: string
  link_to: string
  link_type: string

  source_file: string
  source_section: string
  created_at: string
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

    link_from: Optional[str] = None
    link_to: Optional[str] = None
    link_type: Optional[str] = None

    source_file: Optional[str] = None
    source_section: Optional[str] = None
```

---

## DOCUMENT SPLIT

- Indexing procedures: `ALGORITHM/ALGORITHM_Indexing.md`
- Search procedures: `ALGORITHM/ALGORITHM_Search.md`
- Storage/index details and examples archived (see `archive/SYNC_archive_2024-12.md`)

# Embeddings — Behaviors: Observable Indexing and Search Effects

```
STATUS: DRAFT
CREATED: 2024-12-16
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Embeddings.md
THIS:        BEHAVIORS_Embeddings.md (you are here)
ALGORITHM:   ./ALGORITHM_Embeddings.md
VALIDATION:  ./VALIDATION_Embeddings.md
TEST:        ./TEST_Embeddings.md
SYNC:        ./SYNC_Embeddings.md
IMPL:        ../../engine/embeddings/service.py (existing, needs update)
```

---

## BEHAVIORS

### B1: Index Node on Create/Update

```
GIVEN:  Node created or updated
WHEN:   Indexing triggered
THEN:   IF detail > 20 chars: embed(detail) → node.embedding
        ELSE IF name > 20 chars: embed(name) → node.embedding
        ELSE: no embedding
AND:    Old embedding replaced if update
```

### B2: Index Link on Create/Update

```
GIVEN:  Link created or updated
AND:    Link has detail > 20 characters
WHEN:   Indexing triggered
THEN:   embed(detail) → link.embedding
AND:    Old embedding replaced if update
```

### B3: Skip When No Qualifying Text

```
GIVEN:  Node with detail <= 20 chars AND name <= 20 chars
WHEN:   Indexing runs
THEN:   No embedding created
AND:    No error raised
```

### B5: Search Returns Ranked Results

```
GIVEN:  Query text
WHEN:   search(query, limit=N) called
THEN:   Returns up to N results
AND:    Results ordered by similarity score (descending)
AND:    Each result includes source reference
AND:    Each result includes matched text
```

### B6: Search Spans All Source Types

```
GIVEN:  Query text matching content in narrative, character, and conversation
WHEN:   search(query) called
THEN:   Results include matches from all source types
AND:    Each result tagged with source_type
```

---

## INPUTS / OUTPUTS

### Function: `index_node(node)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| node | dict | Node with id, type, name, and optional detail |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| vector | List[float] or None | 768-dim embedding, or None if nothing to embed |

**Side Effects:**

- Sets `node.embedding` attribute in graph
- Logs indexing action

### Function: `index_link(link)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| link | dict | Link with id, type, from_id, to_id, and optional detail |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| vector | List[float] or None | 768-dim embedding, or None if detail <= 20 chars |

**Side Effects:**

- Sets `link.embedding` attribute in graph

### Function: `search(query, limit=10)`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| query | str | Natural language query |
| limit | int | Maximum results to return |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| results | List[SearchResult] | Ranked list of matches |

**SearchResult structure:**

```python
@dataclass
class SearchResult:
    source_type: str      # "narrative" | "character" | "place" | "link" | "conversation"
    source_id: str        # Node/link ID
    source_field: str     # "detail"
    text: str             # Matched text
    score: float          # Similarity score (0-1)

    # For links
    link_from: str        # Source node ID
    link_to: str          # Target node ID
    link_type: str        # "BELIEVES" | "PRESENT" | "CARRIES"

    # For conversations
    source_file: str      # "conversations/aldric.md"
    source_section: str   # "Day 4, Night — The Camp"
```

---

## EDGE CASES

### E1: No Qualifying Text

```
GIVEN:  Node with detail <= 20 AND name <= 20
THEN:   No embedding created
AND:    Returns None
AND:    No error raised
```

### E2: Very Long Detail

```
GIVEN:  Detail field > 512 tokens
THEN:   Text truncated to model's max length
AND:    Embedding created from truncated text
```

### E3: Duplicate Indexing

```
GIVEN:  Same node indexed twice
THEN:   Second call updates existing embedding
AND:    Only one embedding exists per source
```

### E4: Missing Source on Search

```
GIVEN:  Search result references deleted node
THEN:   Result includes source reference
AND:    get_full_context() returns None for that result
AND:    No error raised
```

### E5: Unicode/Special Characters

```
GIVEN:  Detail contains unicode, emojis, or special chars
THEN:   Embedding created normally
AND:    Text stored correctly
```

---

## ANTI-BEHAVIORS

### A1: No Embedding for Metadata Fields

```
GIVEN:   Node with only id, type fields
WHEN:    index_node() called
MUST NOT: Create embedding from id or type
INSTEAD:  Check detail, then name, else skip
```

### A2: No Graph Links for Embeddings

```
GIVEN:   Embedding created
WHEN:    Stored
MUST NOT: Create HAS_EMBEDDING edge in graph
INSTEAD:  Store source reference in embedding record
```

### A3: No Embedding Short Text

```
GIVEN:   String field with <= 20 characters
WHEN:    index_node() called
MUST NOT: Create embedding for that field
INSTEAD:  Skip that field (too short for meaningful embedding)
```

### A4: No Duplicate Embeddings

```
GIVEN:   Node updated, indexed twice
WHEN:    Second index_node() called
MUST NOT: Create second embedding
INSTEAD:  Overwrite node.embedding attribute
```

---

## QUERY EXAMPLES

### "What do I know about guilt?"

```python
results = search("guilt regret couldn't save")

# Expected matches:
# - character/char_aldric: "Watched his brother die at Stamford..."
# - link/BELIEVES: "Aldric told me by the fire, voice breaking..."
# - conversation: "I was fifty yards away. Couldn't reach him."
```

### "How did I get this ring?"

```python
results = search("ring father inheritance")

# Expected matches:
# - link/CARRIES: "Pulled from father's hand as he died..."
# - narrative/narr_father_death: "Father died in the burning..."
```

### "Dangerous places"

```python
results = search("dangerous threat wolves bandits")

# Expected matches:
# - place/place_moors: "Wind howls. Men disappear here..."
# - place/place_humber: "Norman patrols check travelers..."
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should search support filtering by source_type?
- [ ] Should search support minimum score threshold?
- [ ] How to handle queries that match many results equally?
- IDEA: Boost recent embeddings in search ranking
- IDEA: Allow negative queries ("not about York")
- QUESTION: What's the practical limit on results before quality degrades?

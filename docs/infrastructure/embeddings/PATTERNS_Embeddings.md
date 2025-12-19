# Embeddings — Patterns: Per-Field String Embedding

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2024-12-16
```

---

## CHAIN

```
THIS:        PATTERNS_Embeddings.md (you are here)
BEHAVIORS:   ./BEHAVIORS_Embeddings.md
ALGORITHM:   ./ALGORITHM_Embeddings.md
VALIDATION:  ./VALIDATION_Embeddings.md
IMPLEMENTATION: ./IMPLEMENTATION_Embeddings.md
TEST:        ./TEST_Embeddings.md
SYNC:        ./SYNC_Embeddings.md
IMPL:        ../../../engine/infrastructure/embeddings/
```

---

## THE PROBLEM

The Blood Ledger stores rich textual content across many types:
- Narrative details ("The rebellion began at dawn...")
- Character backstories ("Watched his brother die at Stamford...")
- Place atmospheres ("Wind howls across empty moors...")
- Link context ("Aldric told me by the fire, voice breaking...")
- Conversation threads (full dialogue scenes)

Players and the Narrator need to find relevant content through natural language queries:
- "What do I know about guilt?"
- "How did I get this ring?"
- "Dangerous places"

Keyword search fails because:
- "guilt" doesn't appear in "watched his brother die"
- Semantic relationships matter more than exact matches
- Context is distributed across many node types

---

## THE PATTERN

**One Embedding Per Node: `detail` with `name` Fallback**

Each node/link gets ONE embedding, stored as an attribute. Prefer `detail`, fall back to `name`.

```
IF detail exists AND len(detail) > 20:
    node.embedding = embed(detail)
ELSE IF name exists AND len(name) > 20:
    node.embedding = embed(name)
ELSE:
    no embedding
```

### Why This Works

**Semantic search on rich content.** `detail` contains the evocative text — "Voice breaking, he told me by the fire..." — where semantic search adds value.

**Fallback for named-only nodes.** Some nodes have meaningful names but no detail yet. "The Rebellion at Durham Cathedral" is searchable.

**One embedding per node.** Simple. One vector attribute, one index, no separate Embedding nodes.

**Local embeddings are cheap.** With models like `all-mpnet-base-v2`, embedding thousands of texts takes seconds. No API cost, no rate limits.

### What Gets Embedded

| Type | Primary | Fallback |
|------|---------|----------|
| Narrative | detail | name |
| Character | detail | name |
| Place | detail | name |
| Tension | detail | name |
| Links | detail | — |

Conversations stay in markdown files — no graph embedding.

---

## PRINCIPLES

### Principle 1: One Embedding Per Node

Each node gets at most one embedding, stored as a `node.embedding` attribute.

Why this matters:
- Simple mental model: node = one vector
- One vector index covers everything
- No separate Embedding nodes cluttering the graph

### Principle 2: Prefer `detail`, Fallback to `name`

`detail` has the rich semantic content. `name` is the backup.

Why this matters:
- "What do I know about guilt?" → finds detail text
- Nodes without detail can still be found by descriptive name
- Clear priority: detail > name > nothing

### Principle 3: Embeddings Are Node Attributes

```cypher
(n:Narrative {
  id: "narr_oath",
  name: "The Oath at Durham",
  detail: "Aldric told me by the fire...",
  embedding: [0.1, 0.2, ...]  # 768 floats
})
```

Why this matters:
- No HAS_EMBEDDING edges
- Simpler queries
- Vector index directly on nodes

### Principle 4: Links Are First-Class

Links with `detail` > 20 chars get embeddings too.

Why this matters:
- Link context often contains the most evocative content
- "Aldric told me by the fire, voice breaking..." is searchable
- Queries like "how did I get this ring?" find CARRIES link details

### Principle 5: Conversations Are Not Embedded

Conversation files are markdown, stored outside the graph. No embeddings.

Why this matters:
- Conversations are retrieved by character, not by semantic search
- Graph stays focused on world state, not dialogue history
- Simpler system

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| engine/db/graph_queries | Read nodes and links for indexing |
| engine/history/conversations | Read conversation sections |
| FalkorDB vector index | Store and search embeddings |

---

## INSPIRATIONS

**RAG (Retrieval-Augmented Generation)**
Embed chunks, search by similarity, retrieve for context. We apply this to game state rather than documents.

**Universal Schema**
GraphQL's idea of uniform field access. Every type has `detail`, so embedding logic is type-agnostic.

**Cheap Local Models**
The economics of local embedding models (sentence-transformers) make "embed everything" viable in ways that API-based embeddings don't.

---

## WHAT THIS DOES NOT SOLVE

**Ranking by importance.** Embeddings find similar content, not important content. Weight/focus filtering happens at query time, not embedding time.

**Structured queries.** "Show me all oaths" is a graph query, not an embedding search. Embeddings handle semantic similarity, not categorical filtering.

**Multi-hop reasoning.** "What does Aldric know that I don't?" requires graph traversal + comparison. Embeddings surface individual pieces, not relationships between pieces.

---

## SCALE ESTIMATES

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

Growth: ~5-10 embeddings per scene (new narratives, link details, conversation chunks).

At 384 dimensions, total storage: ~1.5 MB for vectors. Trivial.

---

## GAPS / IDEAS / QUESTIONS

- [ ] How to handle very long fields? Chunk or truncate?
- [ ] Should embedding IDs be deterministic (from source) or UUIDs?
- [ ] Deduplication in search results (multiple fields from same source)?
- IDEA: Pre-compute common query embeddings for faster search
- IDEA: Field-specific boosting in search ranking
- QUESTION: What's the right similarity threshold for "relevant"?

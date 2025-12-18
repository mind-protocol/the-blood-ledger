# Graph Operations Guide

API patterns for the Blood Ledger graph.

- Field definitions: `SCHEMA.md`
- Validation: `graph/VALIDATION.md`

**Scripts:**
- `engine/db/graph_ops.py` — Write operations
- `engine/db/graph_queries.py` — Read operations

---

## Setup

```python
from engine.db.graph_ops import GraphOps
from engine.db.graph_queries import GraphQueries

write = GraphOps(graph_name="blood_ledger")
read = GraphQueries(graph_name="blood_ledger")
```

---

## Writing

```python
result = write.apply(path="mutations/scene_001.yaml")
```

---

## Querying

### Cypher

```python
# Everything at a place: characters, narratives they believe, tensions
read.query("""
  MATCH (p:Place {id: 'place_york'})
  OPTIONAL MATCH (c:Character)-[:AT]->(p)
  OPTIONAL MATCH (c)-[b:BELIEVES]->(n:Narrative)
  OPTIONAL MATCH (t:Tension)-[:INVOLVES]->(n)
  RETURN p, collect(DISTINCT c), collect(DISTINCT {narrative: n, belief: b}), collect(DISTINCT t)
""")

# Scene context: place + present characters + their beliefs + active tensions
read.query("""
  MATCH (p:Place {id: 'place_camp'})
  OPTIONAL MATCH (c:Character)-[:AT {present: 1}]->(p)
  OPTIONAL MATCH (c)-[b:BELIEVES]->(n:Narrative) WHERE b.heard > 0.5
  OPTIONAL MATCH (t:Tension) WHERE t.pressure > 0.3
  RETURN p, collect(DISTINCT c), collect(DISTINCT n), collect(DISTINCT t)
""")

# Everything about a narrative: who believes it, what it contradicts, related tensions
# Note: t.narratives is stored as JSON string, use CONTAINS for filtering
read.query("""
  MATCH (n:Narrative {id: 'narr_betrayal'})
  OPTIONAL MATCH (c:Character)-[b:BELIEVES]->(n)
  OPTIONAL MATCH (n)-[r:RELATES_TO]-(n2:Narrative)
  OPTIONAL MATCH (t:Tension) WHERE t.narratives CONTAINS n.id
  RETURN n, collect({char: c, belief: b}), collect({related: n2, link: r}), collect(t)
""")

# Flipped tensions with involved narratives and believers
# Note: t.narratives is stored as JSON string, use CONTAINS for filtering
read.query("""
  MATCH (t:Tension) WHERE t.pressure > t.breaking_point
  OPTIONAL MATCH (n:Narrative) WHERE t.narratives CONTAINS n.id
  OPTIONAL MATCH (c:Character)-[:BELIEVES]->(n)
  RETURN t, collect(DISTINCT n), collect(DISTINCT c)
""")
```

### Natural Language

```python
# Returns markdown (default) — all fields, ready for LLM
context = read.search(query="Who betrayed Edmund?", embed_fn=get_embedding)

# JSON format — for programmatic use
results = read.search(query="Who betrayed Edmund?", embed_fn=get_embedding, format='json')
```

**IMPORTANT:** NEVER filter output fields. LLM needs complete context.

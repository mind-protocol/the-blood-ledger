# Graph Health & Queries

Tools for validating and querying the Blood Ledger graph database.

## Files

| File | Purpose |
|------|---------|
| `schema.yaml` | Node/link schema definition for validation |
| `check_health.py` | Validates graph data against schema |
| `test_schema.py` | Comprehensive test suite for schema validation |
| `lint_terminology.py` | Linter for NPC→character terminology |
| `example_queries.cypher` | 70+ example queries with quality ratings |
| `query_results.md` | Actual query outputs from the database |
| `query_outputs.md` | Expected output descriptions for each query |

## Query Quality Ratings

Each query in `example_queries.cypher` has a quality rating (1-10):

| Rating | Meaning |
|--------|---------|
| **10/10** | Essential - core gameplay, run frequently |
| **9/10** | Very useful - important for narrative/strategy |
| **8/10** | Useful - good for specific situations |
| **7/10** | Helpful - atmosphere, planning |
| **6/10** | Occasional - logistics, reference |
| **5/10** | Debugging - data quality checks |
| **4/10** | Technical - schema validation only |

## Top Queries by Category

### Scene Setup (run at every scene)
```cypher
// Who is here and what do they know? (10/10)
MATCH (c:Character)-[at:AT]->(p:Place {name: $location})
WHERE at.present > 0.5
OPTIONAL MATCH (c)-[b:BELIEVES]->(n:Narrative)
WHERE b.heard > 0.5
RETURN c.name, c.type, at.visible, collect(n.name) AS knows
```

### Tension Tracking (10/10)
```cypher
// What's about to explode?
MATCH (t:Tension)
WHERE t.pressure > 0.7
RETURN t.description, t.pressure, t.narrator_notes
```

### Knowledge Network (10/10)
```cypher
// False beliefs - dramatic irony gold
MATCH (c:Character)-[b:BELIEVES]->(n:Narrative)
WHERE b.believes > 0.7 AND n.truth < 0.3
RETURN c.name AS believer, n.name AS false_belief
```

### Secrets (10/10)
```cypher
// What are characters hiding?
MATCH (c:Character)-[b:BELIEVES]->(n:Narrative)
WHERE b.hides > 0.5
RETURN c.name AS keeper, n.name AS secret, n.content
```

## Running Health Checks

```bash
# Basic health check
python engine/graph/health/check_health.py

# Full schema test suite (22 tests)
python engine/graph/health/test_schema.py

# With pytest for CI integration
pytest engine/graph/health/test_schema.py -v

# Terminology linter
python engine/graph/health/lint_terminology.py --fix
```

## Schema Tests

The `test_schema.py` suite validates:

**Node Tests:**
- Required fields (id, name, content)
- Enum values (type, flaw, significance, tone)
- Value ranges (pressure 0-1, weight 0-1)

**Link Tests:**
- Structure: Character→Narrative (BELIEVES), Character→Place (AT), etc.
- Value ranges on link properties (heard, believes, doubts all 0-1)

**Data Quality:**
- Orphan nodes (no relationships)
- Characters without locations
- Things without location or carrier
- Narratives without believers
- Player character exists

## Using Queries

Copy queries into FalkorDB browser or use programmatically:

```python
from falkordb import FalkorDB

db = FalkorDB()
graph = db.select_graph("blood_ledger")

# Run a query
result = graph.query("""
    MATCH (c:Character {type: 'companion', alive: true})
    RETURN c.name, c.flaw
""")

for row in result.result_set:
    print(row)
```

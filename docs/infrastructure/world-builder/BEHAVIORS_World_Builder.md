# World Builder — Behaviors: Query Moments, Sparse Enrichment, and Cache Guards

```
STATUS: CANONICAL
CREATED: 2025-12-19
VERIFIED: Not yet verified
```

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_World_Builder.md
PATTERNS:        ./PATTERNS_World_Builder.md
THIS:            BEHAVIORS_World_Builder.md (you are here)
ALGORITHM:       ./ALGORITHM_World_Builder.md
VALIDATION:      ./VALIDATION_World_Builder.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Builder.md
TEST:            ./TEST_World_Builder.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/query.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Query Creates a Thought Moment and ABOUT Links

```
GIVEN:  a natural-language query with optional char_id/place_id
WHEN:   query() is called
THEN:   a Moment node is created with type=thought, status=possible, energy=0.3
AND:    ABOUT links are created from the moment to top results with weight=similarity
```

### B2: Sparse Results Trigger Enrichment and Re-Query

```
GIVEN:  semantic search results that are sparse by threshold rules
WHEN:   query() is called with enrich=True
THEN:   WorldBuilder.enrich() is invoked with context
AND:    enrichment content is applied and linked back to the query moment
AND:    semantic search is run again to return enriched results
```

### B3: Cache and Recursion Guards Block Repeat Enrichment

```
GIVEN:  an identical query recently enriched or currently in progress
WHEN:   WorldBuilder.enrich() is called again
THEN:   enrichment is skipped and an empty response is returned
```

---

## INPUTS / OUTPUTS

### Primary Function: `query()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query_text` | `str` | Natural-language query text |
| `char_id` | `str \| None` | Optional character context |
| `place_id` | `str \| None` | Optional place context |
| `enrich` | `bool` | Whether to enrich when sparse |
| `graph` | `GraphQueries \| None` | Graph interface (ngram repo runtime) |
| `world_builder` | `WorldBuilder \| None` | Enrichment service (defaults to shared instance) |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| `results` | `List[Dict]` | Semantic search results (post-enrichment if applied) |

**Side Effects:**

- Creates a thought moment node in the graph
- Creates ABOUT links to results (and to enriched nodes)
- May create new nodes/links/moments during enrichment

---

## EDGE CASES

### E1: Empty Results

```
GIVEN:  semantic search returns no results
THEN:   is_sparse() reports sparse and enrichment may run (if enabled)
```

### E2: LLM Failure or Missing Key

```
GIVEN:  WorldBuilder cannot call the LLM successfully
THEN:   enrichment returns empty and query() returns original results
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Enrichment Loops

```
GIVEN:   the same query is already enriching
WHEN:    WorldBuilder.enrich() is called again
MUST NOT: trigger a second enrichment or recurse
INSTEAD:  return empty and exit early
```

### A2: Non-Thought Moments

```
GIVEN:   any World Builder query
WHEN:    a moment is created
MUST NOT: create moments with type other than "thought"
INSTEAD:  always set type="thought"
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Clarify behavior when semantic search raises exceptions (return empty list vs partial results)
- [ ] Specify whether query moments should be eligible to surface by default
- IDEA: Track and expose enrichment acceptance rate for debugging

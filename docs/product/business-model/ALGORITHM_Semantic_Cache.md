# ALGORITHM: Semantic Cache

## Procedures

The Semantic Cache is a critical component for maintaining narrative consistency over long playtimes (100+ hours). Unlike traditional temporal caches, it stores and retrieves content based on meaning and theme, rather than just recent access time. This ensures that the system provides consistent responses to recurring narrative themes or character backstories.

## The Problem

A simple temporal cache (e.g., 60 seconds) is insufficient for complex narrative games. Players asking about the same NPC's family history at different times could receive contradictory answers, breaking immersion.

## The Solution

Cache by MEANING (theme) rather than by time.

## Algorithm Steps

### 1. Extract Theme
The system first analyzes the player's query to extract its core thematic content.

```python
# BEFORE: Temporal cache (60 seconds)
def get_cached(query):
    if cache.age(query) < 60:
        return cache.get(query)
    return generate_new(query)
```

```python
# AFTER: Semantic cache
def get_cached_semantic(query, character):
    # 1. Extract the THEME of the request
    theme = extract_theme(query)  # "family", "past", "loyalty"
```

### 2. Query Graph for Related Content
The extracted theme and character context are used to query the game's knowledge graph for all related canonical information.

```python
    # 2. Query the graph for EVERYTHING related
    related = graph.query(f"""
        MATCH (c:Character {{name: '{character}'}})-[*1..3]-(n)
        WHERE n.theme IN {theme} OR n.origin = 'worldbuilder'
        RETURN n
    """)
```

### 3. Generate Consistent Content
If existing content related to the theme is found in the graph, the system uses it to generate a new response that is consistent with the established canon. This might involve re-phrasing or contextualizing existing facts.

```python
    # 3. If content exists, respect it
    if related:
        return generate_consistent_with(query, related)
```

### 4. Generate and Tag New Content (if not found)
If no existing content is found, the system generates new narrative content. This new content is then meticulously tagged with metadata (origin, theme, timestamp, constraints) and added to the graph, making it available for future semantic queries.

```python
    # 4. If new, generate AND tag for future
    content = generate_new(query)
    content.metadata = {
        'origin': 'worldbuilder',
        'theme': theme,
        'timestamp': now()
    }
    graph.add(content)
    return content
```

## Metadata Tagging

Every generation process includes tagging the new canonical nodes with semantic breadcrumbs.

```yaml
node: narr_aldric_orphan
origin: worldbuilder
theme: [family, loss, solitude]
generated_at: 2025-01-15T14:23:00Z
constraints_applied:
  - "no living relatives (established)"
  - "tragic backstory (character trait)"
```

## Result

The Semantic Cache enables the system to learn and consistently reference themes and facts over extended periods, ensuring narrative integrity and preventing contradictions across 100+ hours of gameplay.

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Whale_Economics.md
THIS:            ./ALGORITHM_Semantic_Cache.md
SYNC:            ./SYNC_Business_Model.md

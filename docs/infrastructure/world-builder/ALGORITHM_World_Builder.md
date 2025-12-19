# World Builder — Algorithm

```
CREATED: 2025-12-19
UPDATED: 2025-12-19
STATUS: SPEC (not implemented)
```

---

## Overview

World Builder is the JIT compiler for narrative content. Graph is sparse by default. Content materializes on demand when queries return unsatisfying results.

**Two key principles:**

1. **Every query is a moment.** Queries leave traces in the graph — thoughts, questions, explorations. The graph remembers what was asked.

2. **Sparse triggers enrichment.** When results are thin, World Builder invents content — characters, places, narratives, AND moments (thoughts, memories).

---

## Core Insight: Attention IS Energy

**Query moments inject energy via physics.**

The act of asking creates a moment. That moment links to results via ABOUT. Physics flows energy through those links. What you think about becomes more salient naturally.

```
Aldric thinks: "What do I know about Edmund?"
         ↓
    Query creates moment (energy=0.3)
         ↓
    ABOUT links to: narr_edmund_betrayal, char_edmund
         ↓
    Physics tick: energy flows through ABOUT links
         ↓
    Edmund-related nodes gain energy
         ↓
    Edmund-related moments more likely to surface
```

No special injection logic. The moment IS the energy source. Physics handles distribution.

---

## Core Flow

```
Any component calls graph query (natural language)
         ↓
    Record query as moment (type=thought, energy=0.3)
         ↓
    Execute query (embeddings use 'detail' or 'name' field)
         ↓
    Create ABOUT links from moment to results (weight=similarity)
         ↓
    Measure sparsity (embedding proximity, cluster size, diversity, connectedness)
         ↓
    Sparse? → await WorldBuilder.enrich(query, context)
         ↓
    WorldBuilder creates:
      - Nodes (characters, places, things, narratives)
      - Links (all links have weight + energy)
      - Moments (type=thought, status=possible)
      - All linked back to query moment via ABOUT
         ↓
    Re-query → return enriched results
         ↓
    Physics tick later → energy flows from query moment to results
```

---

## Every Query Is A Moment

**Principle:** The graph is self-documenting. Every query leaves a trace.

```python
async def query_graph(
    query: str,
    char_id: str = None,
    place_id: str = None
) -> QueryResult:
    """
    Query graph. Record the query as a moment. Enrich if sparse.
    Energy flows via physics - no explicit injection needed.
    """
    # 1. Record query as moment (this IS the energy source)
    moment_id = create_query_moment(query, char_id, place_id)
    
    # 2. Execute query (embeddings use 'detail' or 'name' field)
    results = await execute_semantic_query(query)
    
    # 3. Link moment to results (weight=similarity, physics will flow energy)
    for result in results[:5]:
        create_link(moment_id, 'ABOUT', result['id'], {
            'weight': result['similarity']
        })
    
    # 4. Check sparsity
    if is_sparse(query, results):
        enrichment = await world_builder.enrich(query, {
            'char_id': char_id,
            'place_id': place_id,
            'existing_results': results
        })
        # Apply and link back to query moment
        apply_enrichment(enrichment, moment_id, char_id, place_id)
        
        # Re-query
        results = await execute_semantic_query(query)
        
        # Link new results
        for result in results[5:10]:
            create_link(moment_id, 'ABOUT', result['id'], {
                'weight': result['similarity']
            })
    
    return results
```

### Query Moment Schema

```yaml
Moment:
  id: mom_{uuid}
  text: "{the query}"
  type: query | thought | memory  # thought if char-centered
  status: possible
  weight: 0.2  # Low - may not surface unless relevant
  energy: 0.3
  
Links created:
  - ATTACHED_TO → Character (if char_id provided)
  - CAN_SPEAK → from Character (they could voice this)
  - OCCURRED_AT → Place (if place_id provided)
  - ABOUT → each result node
```

**Example:**

```
Aldric queries: "What do I know about Edmund's betrayal?"
         ↓
Moment created:
  text: "What do I know about Edmund's betrayal?"
  type: thought
  
Links:
  (moment)-[:ATTACHED_TO]->(char_aldric)
  (char_aldric)-[:CAN_SPEAK]->(moment)
  (moment)-[:OCCURRED_AT]->(place_camp)
  (moment)-[:ABOUT]->(narr_edmund_betrayal)
  (moment)-[:ABOUT]->(char_edmund)
```

If this thought surfaces (salience crosses threshold), Aldric might say: "I've been thinking about Edmund's betrayal..."

---

## Sparsity Detection

**No query_type enum.** Queries are natural language. Use semantic measures.

```python
def is_sparse(query: str, results: List[Dict]) -> SparsityResult:
    """
    Measure result quality across multiple dimensions.
    """
    if not results:
        return SparsityResult(sparse=True, reason='no_results')
    
    query_embedding = embed(query)
    result_embeddings = [embed(node_to_text(r)) for r in results]
    
    # 1. Proximity - are results semantically close to query?
    proximity = max([
        cosine_similarity(query_embedding, re) 
        for re in result_embeddings
    ])
    
    # 2. Cluster size - how many results?
    cluster_size = len(results)
    
    # 3. Diversity - are results varied or all the same?
    if len(result_embeddings) > 1:
        diversity = avg_pairwise_distance(result_embeddings)
    else:
        diversity = 0.0
    
    # 4. Connectedness - do results link to other things?
    connectedness = avg([
        count_links(r['id']) for r in results
    ])
    
    # Sparse if any dimension is weak
    sparse = (
        proximity < 0.6 or      # Results don't match query
        cluster_size < 2 or     # Too few results
        diversity < 0.3 or      # Results too similar
        connectedness < 1.5     # Results are isolated nodes
    )
    
    return SparsityResult(
        sparse=sparse,
        proximity=proximity,
        cluster_size=cluster_size,
        diversity=diversity,
        connectedness=connectedness
    )
```

---

## World Builder Enrichment

**World Builder creates everything** — nodes, links, AND moments.

### Enrichment Prompt

```python
def build_enrichment_prompt(query: str, context: Dict) -> str:
    char_context = ""
    if context.get('char_id'):
        char = get_character(context['char_id'])
        char_context = f"""
FROM PERSPECTIVE OF: {char['name']}
  Backstory: {char.get('backstory', 'Unknown')}
  Location: {char.get('location', 'Unknown')}
  Voice: {char.get('voice', 'Unknown')}
"""
    
    place_context = ""
    if context.get('place_id'):
        place = get_place(context['place_id'])
        place_context = f"""
LOCATION: {place['name']} ({place.get('type', 'place')})
  Region: {place.get('region', 'Unknown')}
"""
    
    existing = ""
    if context.get('existing_results'):
        existing = f"""
EXISTING (sparse, needs enrichment):
{format_results(context['existing_results'])}
"""
    
    return f"""
You are the World Builder for a story set in 1087 England, after the Norman Conquest.

QUERY: "{query}"

{char_context}
{place_context}
{existing}

Generate content to answer this query richly. You may create:

1. CHARACTERS - New people with names, backstories, relationships
2. PLACES - Locations with atmosphere, details
3. THINGS - Objects with significance
4. NARRATIVES - Events, memories, rumors, beliefs
5. LINKS - Relationships between any nodes
6. MOMENTS - Thoughts as potential dialogue (status=possible)

For moments, these are things the querying character might think or say.
They should feel personal, emotional, connected to the query.
Type is always "thought".

Output as YAML:

```yaml
characters:
  - id: char_{{slug}}
    name: string
    character_type: minor | significant
    backstory: string
    voice: {{tone, patterns}}

places:
  - id: place_{{slug}}
    name: string
    type: string
    atmosphere: {{sights, sounds, smells}}
    description: string

things:
  - id: thing_{{slug}}
    name: string
    type: string
    description: string
    significance: string

narratives:
  - id: narr_{{slug}}
    name: string
    content: string
    type: memory | rumor | event | legend
    truth: float

links:
  - from: node_id
    to: node_id
    type: LINK_TYPE
    properties: {{}}

moments:
  - text: string
    type: thought  # Always "thought"
    weight: float  # 0.3-0.7
    energy: float  # 0.3-0.6
    speaker_id: char_id  # Who would say/think this
```

Be specific. Use concrete details. Create 2-5 items per category (not all categories needed).
Moments should be emotional, personal — things the character might actually think or say.
"""
```

### Enrichment Examples

**Query:** "Who are my relatives?" (char_id=char_player)

```yaml
characters:
  - id: char_niece_anna
    name: "Anna"
    character_type: minor
    backstory: "Your sister's daughter. Seven years old. Lives in York with her mother."
    voice: {tone: innocent, patterns: [asks questions, trusts easily]}

  - id: char_uncle_godric
    name: "Godric"
    character_type: significant
    backstory: "Your father's brother. A merchant in Durham. Never forgave your father for inheriting the land."
    voice: {tone: bitter, patterns: [speaks in proverbs, avoids eye contact]}

narratives:
  - id: narr_uncle_grudge
    name: "Godric's Grudge"
    content: "Godric believes your father cheated him of his inheritance. He's nursed this wound for twenty years."
    type: memory
    truth: 0.5

links:
  - from: char_player
    to: char_niece_anna
    type: RELATED_TO
    properties: {relation: uncle/aunt, closeness: 0.7}
  
  - from: char_player
    to: char_uncle_godric
    type: RELATED_TO
    properties: {relation: nephew/niece, closeness: 0.2}
  
  - from: char_uncle_godric
    to: narr_uncle_grudge
    type: BELIEVES
    properties: {strength: 0.9, originated: 1.0}

moments:
  - text: "Anna. I haven't seen her since before... all this."
    type: thought
    weight: 0.5
    speaker_id: char_player

  - text: "Godric would sooner see me dead than help. Blood means nothing to him."
    type: thought
    weight: 0.4
    speaker_id: char_player

  - text: "I should find Anna. Make sure she's safe."
    type: thought
    weight: 0.6
    speaker_id: char_player
```

---

## Apply Enrichment

```python
def apply_enrichment(enrichment: Dict, query_moment_id: str, char_id: str, place_id: str):
    """
    Create all nodes, links, and moments from enrichment.
    Links ALL created content back to the query moment.
    Physics handles energy flow - just set weights.
    """
    created_ids = []
    
    # Characters
    for char in enrichment.get('characters', []):
        create_node('Character', char)
        created_ids.append(char['id'])
    
    # Places
    for place in enrichment.get('places', []):
        create_node('Place', place)
        created_ids.append(place['id'])
    
    # Things
    for thing in enrichment.get('things', []):
        create_node('Thing', thing)
        created_ids.append(thing['id'])
    
    # Narratives
    for narr in enrichment.get('narratives', []):
        create_node('Narrative', narr)
        created_ids.append(narr['id'])
    
    # Links
    for link in enrichment.get('links', []):
        props = link.get('properties', {})
        props.setdefault('weight', 0.5)
        create_link(
            link['from'], 
            link['type'], 
            link['to'], 
            props
        )
    
    # Link ALL created nodes back to query moment
    for node_id in created_ids:
        create_link(query_moment_id, 'ABOUT', node_id, {'weight': 0.5})
    
    # Moments - always type "thought"
    for moment in enrichment.get('moments', []):
        moment_id = f"mom_{uuid4().hex[:8]}"
        create_node('Moment', {
            'id': moment_id,
            'text': moment['text'],
            'type': 'thought',  # Always thought
            'status': 'possible',
            'weight': moment.get('weight', 0.4),
            'energy': moment.get('energy', 0.5)
        })
        
        # Link to speaker
        speaker_id = moment.get('speaker_id', char_id)
        if speaker_id:
            create_link(moment_id, 'ATTACHED_TO', speaker_id, {'weight': 0.8})
            create_link(speaker_id, 'CAN_SPEAK', moment_id, {'strength': 0.8})
        
        # Link to place
        if place_id:
            create_link(moment_id, 'ATTACHED_TO', place_id, {'weight': 0.5})
        
        # Link enriched moment back to query moment
        create_link(query_moment_id, 'ABOUT', moment_id, {'weight': 0.6})
```

---

## Integration

### Where Queries Happen

| Component | Query Example | char_id | place_id |
|-----------|---------------|---------|----------|
| Narrator (flip) | "What does Aldric feel about this?" | char_aldric | current place |
| Frontend view | "What's in this room?" | char_player | current place |
| Click handler | "Tell me about this sword" | char_player | current place |
| Relationship check | "How do I know Edmund?" | char_player | - |
| Knowledge check | "What do I know about York?" | char_player | - |

### Query Wrapper (Unified)

```python
async def query(
    query: str,
    char_id: str = None,
    place_id: str = None,
    enrich: bool = True
) -> List[Dict]:
    """
    The universal graph query function.
    
    - Records query as moment
    - Enriches if sparse
    - Returns results
    """
    # Record
    moment_id = record_query_moment(query, char_id, place_id)
    
    # Execute
    results = semantic_search(query)
    
    # Link results
    link_results_to_moment(moment_id, results)
    
    # Enrich if sparse
    if enrich and is_sparse(query, results):
        enrichment = await world_builder.enrich(query, {
            'char_id': char_id,
            'place_id': place_id,
            'existing': results
        })
        apply_enrichment(enrichment, {'char_id': char_id, 'place_id': place_id})
        
        # Re-query
        results = semantic_search(query)
        link_results_to_moment(moment_id, results)
    
    return results
```

---

## Caching / Rate Limiting

```python
class WorldBuilder:
    def __init__(self):
        self._cache: Dict[str, datetime] = {}  # query_hash → last_enriched
        self._enriching: Set[str] = set()  # Prevent recursion
        self.MIN_INTERVAL = 60  # seconds
    
    async def enrich(self, query: str, context: Dict) -> Dict:
        query_hash = hash(query + str(context.get('char_id')))
        
        # Skip if recently enriched
        if query_hash in self._cache:
            if (now() - self._cache[query_hash]).seconds < self.MIN_INTERVAL:
                return {}
        
        # Prevent recursion
        if query_hash in self._enriching:
            return {}
        
        self._enriching.add(query_hash)
        try:
            prompt = build_enrichment_prompt(query, context)
            result = await llm(prompt, structured=True)
            self._cache[query_hash] = now()
            return result
        finally:
            self._enriching.remove(query_hash)
```

---

## Chain

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
THIS:            ALGORITHM_World_Builder.md
VALIDATION:      ./VALIDATION_World_Builder.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Builder.md
TEST:            ./TEST_World_Builder.md
SYNC:            ./SYNC_World_Builder.md
```

---

## Summary

| Principle | Implementation |
|-----------|----------------|
| Every query is a moment | `record_query_moment()` creates thought/query moment |
| Sparsity is semantic | Embedding proximity, cluster size, diversity, connectedness |
| World Builder creates everything | Characters, places, things, narratives, links, AND moments |
| Moments from enrichment | Thoughts, memories, realizations (status=possible) |
| Query traces in graph | ABOUT links from query moment to result nodes |

---

## Gaps / Questions

- QUESTION: How to handle conflicting enrichments? (Two queries generate contradictory content)
- QUESTION: Should query moments ever surface? Or always stay hidden?
- QUESTION: Depth limit for enrichment? (Enriching A creates B, query about B triggers more enrichment...)
- IDEA: "Examine" action forces enrichment even if not sparse
- IDEA: Mark generated content so humans can review/edit

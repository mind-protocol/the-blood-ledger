# World Builder — Implementation

```
STATUS: CANONICAL
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Builder.md
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM_World_Builder.md
VALIDATION:      ./VALIDATION_World_Builder.md
THIS:            IMPLEMENTATION_World_Builder.md
TEST:            ./TEST_World_Builder.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CORE INSIGHT

**Query moments inject energy via physics.**

No explicit energy injection in query code. The query creates a moment with energy. Physics flows that energy through ABOUT links to results. Attention IS energy, but physics handles it.

```
query("What about Edmund?")
  → create moment (energy=0.3)
  → ABOUT links to results (weight=similarity)
  → physics tick later
  → energy flows through links
  → Edmund-related nodes gain salience
```

---

## CODE STRUCTURE

```
engine/infrastructure/world_builder/
├── engine/infrastructure/world_builder/__init__.py        # Exports query(), WorldBuilder
├── engine/infrastructure/world_builder/world_builder.py   # Main WorldBuilder class, LLM calls
├── engine/infrastructure/world_builder/sparsity.py        # Semantic sparsity detection
├── engine/infrastructure/world_builder/query_moment.py    # Record queries as moments
├── engine/infrastructure/world_builder/enrichment.py      # Build prompts, apply enrichment
└── engine/infrastructure/world_builder/query.py           # Universal query() function
```

### File Responsibilities

| File | Purpose | Key Functions | Lines | Status |
|------|---------|---------------|-------|--------|
| `engine/infrastructure/world_builder/__init__.py` | Package exports | `query`, `WorldBuilder` | ~10 | IMPL |
| `engine/infrastructure/world_builder/query.py` | Universal query interface | `query()`, `query_sync()` | ~200 | IMPL |
| `engine/infrastructure/world_builder/query_moment.py` | Record queries as thought moments | `record_query_moment()`, `link_results_to_moment()` | ~186 | IMPL |
| `engine/infrastructure/world_builder/sparsity.py` | Semantic sparsity detection | `is_sparse()`, `SparsityResult` | ~207 | IMPL |
| `engine/infrastructure/world_builder/world_builder.py` | Enrichment service | `WorldBuilder.enrich()` | ~189 | IMPL |
| `engine/infrastructure/world_builder/enrichment.py` | Prompts and mutations | `build_enrichment_prompt()`, `apply_enrichment()` | ~478 | IMPL |

---

## SCHEMA

### QueryMoment

```yaml
Moment:
  id: mom_{uuid}
  text: "{query text}"
  type: thought           # Always "thought" - no other types
  status: possible
  weight: 0.2
  energy: 0.3             # This IS the energy source
  tick_created: int

Links created:
  - (moment)-[:ATTACHED_TO]->(Character)     # if char_id
  - (Character)-[:CAN_SPEAK]->(moment)       # if char_id  
  - (moment)-[:OCCURRED_AT]->(Place)         # if place_id
  - (moment)-[:ABOUT {weight}]->(result)     # for each result
```

### SparsityResult

```yaml
SparsityResult:
  sparse: bool
  proximity: float      # 0-1, how close results match query
  cluster_size: int     # Number of results
  diversity: float      # 0-1, how varied results are
  connectedness: float  # Avg links per result node
```

### EnrichmentOutput

```yaml
EnrichmentOutput:
  characters: List[Character]
  places: List[Place]
  things: List[Thing]
  narratives: List[Narrative]
  links: List[Link]
  moments: List[Moment]    # type=thought, status=possible
```

---

## KEY FUNCTIONS

### query()

```python
# engine/infrastructure/world_builder/query.py

async def query(
    query_text: str,
    char_id: str = None,
    place_id: str = None,
    enrich: bool = True,
    graph: GraphQueries = None,
    world_builder: WorldBuilder = None
) -> List[Dict]:
    """
    Universal graph query. Records as moment. Enriches if sparse.
    
    Energy flows via physics - no explicit injection here.
    The moment IS the energy source. ABOUT links carry weight.
    Physics will flow energy through those links.
    """
    graph = graph or get_default_graph()
    world_builder = world_builder or get_default_world_builder()
    
    # 1. Record query as thought moment (this IS the energy source)
    moment_id = create_query_moment(query_text, char_id, place_id, graph)
    
    # 2. Execute semantic search (embeddings use 'detail' or 'name')
    results = graph.semantic_search(query_text)
    
    # 3. Link moment to results (weight=similarity, physics flows energy)
    for result in results[:5]:
        graph.create_link(moment_id, 'ABOUT', result['id'], {
            'weight': result['similarity']
        })
    
    # 4. Check sparsity
    if enrich:
        sparsity = is_sparse(query_text, results)
        
        if sparsity.sparse:
            # 5. Enrich
            enrichment = await world_builder.enrich(
                query_text,
                context={
                    'char_id': char_id,
                    'place_id': place_id,
                    'existing': results,
                    'sparsity': sparsity
                }
            )
            
            if enrichment:
                # 6. Apply enrichment (links back to query moment)
                apply_enrichment(enrichment, moment_id, char_id, place_id, graph)
                
                # 7. Re-query
                results = graph.semantic_search(query_text)
                
                # Link new results
                for result in results[5:10]:
                    graph.create_link(moment_id, 'ABOUT', result['id'], {
                        'weight': result['similarity']
                    })
    
    return results
```

### create_query_moment()

```python
# engine/infrastructure/world_builder/query_moment.py

def create_query_moment(
    query_text: str,
    char_id: str,
    place_id: str,
    graph: GraphQueries
) -> str:
    """
    Create a thought moment representing this query.
    
    Type is always "thought" - queries are thoughts.
    The moment's energy (0.3) will flow to results via physics.
    """
    moment_id = f"mom_{uuid4().hex[:8]}"
    
    # Create moment node
    graph.create_node('Moment', {
        'id': moment_id,
        'text': query_text,
        'type': 'thought',      # Always thought
        'status': 'possible',
        'weight': 0.2,
        'energy': 0.3,          # Energy source for physics
        'tick_created': get_current_tick()
    })
    
    # Link to character (they can voice this thought)
    if char_id:
        graph.create_link(moment_id, 'ATTACHED_TO', char_id, {'weight': 0.5})
        graph.create_link(char_id, 'CAN_SPEAK', moment_id, {'strength': 0.5})
    
    # Link to place
    if place_id:
        graph.create_link(moment_id, 'OCCURRED_AT', place_id, {'weight': 0.3})
    
    return moment_id
```

### is_sparse()

```python
# engine/infrastructure/world_builder/sparsity.py

from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class SparsityResult:
    sparse: bool
    proximity: float
    cluster_size: int
    diversity: float
    connectedness: float

def is_sparse(query_text: str, results: List[Dict]) -> SparsityResult:
    """
    Semantic sparsity detection. No type-based rules.
    Uses embedding proximity, cluster size, diversity, connectedness.
    """
    if not results:
        return SparsityResult(
            sparse=True,
            proximity=0.0,
            cluster_size=0,
            diversity=0.0,
            connectedness=0.0
        )
    
    # Get query embedding
    query_emb = get_embedding(query_text)
    
    # Get result embeddings (uses 'detail' or 'name' - already implemented)
    result_embs = [r['embedding'] for r in results if 'embedding' in r]
    
    if not result_embs:
        # Fallback: compute embeddings
        result_embs = [get_embedding(node_to_text(r)) for r in results]
    
    # Proximity: best match to query
    similarities = [cosine_similarity(query_emb, re) for re in result_embs]
    proximity = max(similarities) if similarities else 0.0
    
    # Cluster size
    cluster_size = len(results)
    
    # Diversity: average pairwise distance
    if len(result_embs) > 1:
        distances = []
        for i, e1 in enumerate(result_embs):
            for e2 in result_embs[i+1:]:
                distances.append(1 - cosine_similarity(e1, e2))
        diversity = np.mean(distances)
    else:
        diversity = 0.0
    
    # Connectedness: average outgoing links per result
    link_counts = [r.get('link_count', count_links(r['id'])) for r in results]
    connectedness = np.mean(link_counts) if link_counts else 0.0
    
    # Determine sparsity
    sparse = (
        proximity < 0.6 or
        cluster_size < 2 or
        diversity < 0.3 or
        connectedness < 1.5
    )
    
    return SparsityResult(
        sparse=sparse,
        proximity=proximity,
        cluster_size=cluster_size,
        diversity=diversity,
        connectedness=connectedness
    )

def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def node_to_text(node: Dict) -> str:
    """Convert node to text for embedding. Uses 'detail' or 'name'."""
    return node.get('detail') or node.get('name') or str(node.get('id', ''))
```

### WorldBuilder.enrich()

```python
# engine/infrastructure/world_builder/world_builder.py

from datetime import datetime
from typing import Dict, Set

from engine.infrastructure.orchestration.agent_cli import extract_claude_text, run_agent

class WorldBuilder:
    def __init__(self, playthrough_id: str):
        self.playthrough_id = playthrough_id
        self._cache: Dict[str, datetime] = {}
        self._enriching: Set[str] = set()
        self.MIN_INTERVAL = 60  # seconds
    
    async def enrich(self, query: str, context: Dict) -> Dict:
        """
        Generate enrichment for sparse query results.
        
        Returns dict with characters, places, things, narratives, links, moments.
        All moments are type="thought".
        """
        cache_key = f"{hash(query)}:{context.get('char_id')}"
        
        # Skip if recently enriched
        if cache_key in self._cache:
            elapsed = (datetime.now() - self._cache[cache_key]).seconds
            if elapsed < self.MIN_INTERVAL:
                return {}
        
        # Prevent recursion
        if cache_key in self._enriching:
            return {}
        
        self._enriching.add(cache_key)
        try:
            prompt = build_enrichment_prompt(query, context)
            
            result = run_agent(
                prompt,
                working_dir=self.working_dir,
                timeout=self.timeout,
                output_format="json",
                add_dir="../..",
            )
            if result.returncode != 0:
                return {}

            # Parse YAML from response
            result = parse_enrichment_yaml(extract_claude_text(result.stdout))
            
            self._cache[cache_key] = datetime.now()
            return result
            
        finally:
            self._enriching.remove(cache_key)
```

### apply_enrichment()

```python
# engine/infrastructure/world_builder/enrichment.py

def apply_enrichment(
    enrichment: Dict,
    query_moment_id: str,
    char_id: str,
    place_id: str,
    graph: GraphQueries
):
    """
    Create all nodes, links, and moments from enrichment.
    Links ALL created content back to the query moment.
    
    Physics handles energy flow - just set weights on links.
    """
    created_ids = []
    
    # Characters
    for char in enrichment.get('characters', []):
        graph.create_node('Character', char)
        created_ids.append(char['id'])
    
    # Places
    for place in enrichment.get('places', []):
        graph.create_node('Place', place)
        created_ids.append(place['id'])
    
    # Things
    for thing in enrichment.get('things', []):
        graph.create_node('Thing', thing)
        created_ids.append(thing['id'])
    
    # Narratives
    for narr in enrichment.get('narratives', []):
        graph.create_node('Narrative', narr)
        created_ids.append(narr['id'])
    
    # Links (just weight, physics handles energy)
    for link in enrichment.get('links', []):
        props = link.get('properties', {})
        props.setdefault('weight', 0.5)
        graph.create_link(link['from'], link['type'], link['to'], props)
    
    # Link ALL created nodes back to query moment
    for node_id in created_ids:
        graph.create_link(query_moment_id, 'ABOUT', node_id, {'weight': 0.5})
    
    # Moments - always type "thought"
    for moment in enrichment.get('moments', []):
        moment_id = f"mom_{uuid4().hex[:8]}"
        
        graph.create_node('Moment', {
            'id': moment_id,
            'text': moment['text'],
            'type': 'thought',          # Always thought
            'status': 'possible',
            'weight': moment.get('weight', 0.4),
            'energy': moment.get('energy', 0.5)
        })
        
        # Link to speaker
        speaker_id = moment.get('speaker_id', char_id)
        if speaker_id:
            graph.create_link(moment_id, 'ATTACHED_TO', speaker_id, {'weight': 0.8})
            graph.create_link(speaker_id, 'CAN_SPEAK', moment_id, {'strength': 0.8})
        
        # Link to place
        if place_id:
            graph.create_link(moment_id, 'ATTACHED_TO', place_id, {'weight': 0.5})
        
        # Link back to query moment
        graph.create_link(query_moment_id, 'ABOUT', moment_id, {'weight': 0.6})
```

### build_enrichment_prompt()

```python
# engine/infrastructure/world_builder/enrichment.py

def build_enrichment_prompt(query: str, context: Dict) -> str:
    """Build LLM prompt for enrichment."""
    
    char_section = ""
    if context.get('char_id'):
        char = get_character(context['char_id'])
        if char:
            char_section = f"""
FROM PERSPECTIVE OF: {char.get('name', context['char_id'])}
  Backstory: {char.get('backstory', 'Unknown')}
  Location: {char.get('location', 'Unknown')}
"""
    
    place_section = ""
    if context.get('place_id'):
        place = get_place(context['place_id'])
        if place:
            place_section = f"""
LOCATION: {place.get('name', context['place_id'])}
  Type: {place.get('type', 'place')}
"""
    
    existing_section = ""
    if context.get('existing'):
        existing_section = f"""
EXISTING (sparse, needs enrichment):
{format_nodes(context['existing'][:3])}
"""
    
    return f"""You are the World Builder for a story set in 1087 England.

QUERY: "{query}"
{char_section}{place_section}{existing_section}

Generate content to answer this query richly. You may create:
- CHARACTERS with id, name, backstory, voice
- PLACES with id, name, type, atmosphere  
- THINGS with id, name, description, significance
- NARRATIVES with id, name, content, type (memory/rumor/event/legend)
- LINKS between nodes (from, to, type, properties)
- MOMENTS as thoughts the character might have (always type="thought")

For moments: personal, emotional, connected to the query.

Output as YAML:

```yaml
characters:
  - id: char_{{slug}}
    name: string
    backstory: string

places:
  - id: place_{{slug}}
    name: string
    type: string

things:
  - id: thing_{{slug}}
    name: string
    description: string

narratives:
  - id: narr_{{slug}}
    name: string
    content: string
    type: memory | rumor | event | legend

links:
  - from: node_id
    to: node_id
    type: LINK_TYPE
    properties: {{weight: 0.5}}

moments:
  - text: string
    type: thought
    weight: 0.4
    energy: 0.5
    speaker_id: char_id
```

Create 2-5 items per relevant category. Be specific and concrete.
"""
```

---

## DATA FLOW

```
┌─────────────────┐
│  Any Component  │
└────────┬────────┘
         │ query("What about Edmund?", char_id="char_aldric")
         ▼
┌─────────────────┐
│  query()        │
│  (module)       │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌────────────┐
│ create │  │ semantic   │
│ query  │  │ search()   │
│ moment │  └─────┬──────┘
└────┬───┘        │ results
     │            ▼
     │   ┌─────────────────┐
     │   │ create ABOUT    │
     │   │ links (weight)  │
     │   └────────┬────────┘
     │            │
     │            ▼
     │   ┌─────────────────┐
     │   │ is_sparse()?    │
     │   └────────┬────────┘
     │            │ sparse=True
     │            ▼
     │   ┌─────────────────┐
     │   │ WorldBuilder    │
     │   │ .enrich()       │
     │   └────────┬────────┘
     │            │ enrichment
     │            ▼
     │   ┌─────────────────┐
     │   │ apply_          │
     │   │ enrichment()    │
     │   │ (links to query │
     │   │  moment)        │
     │   └────────┬────────┘
     │            │
     │            ▼
     │   ┌─────────────────┐
     │   │ re-query +      │
     │   │ more ABOUT      │
     │   │ links           │
     │   └────────┬────────┘
     │            │
     └──────┬─────┘
            ▼
┌─────────────────┐
│  Return results │
└────────┬────────┘
         │
         ▼
    (later: physics tick)
         │
         ▼
┌─────────────────┐
│ Energy flows    │
│ from query      │
│ moment through  │
│ ABOUT links     │
└─────────────────┘
```

---

## MODULE DEPENDENCIES

### Internal

```
engine/infrastructure/world_builder/query.py
  └── engine/infrastructure/world_builder/query_moment.py
  └── engine/infrastructure/world_builder/sparsity.py
  └── engine/infrastructure/world_builder/world_builder.py
        └── engine/infrastructure/world_builder/enrichment.py
        └── engine/infrastructure/orchestration/agent_cli.py
```

### External

| Package | Used For | File |
|---------|----------|------|
| `claude` (CLI) | LLM calls (CLI only) | `engine/infrastructure/orchestration/agent_cli.py` |
| `numpy` | Cosine similarity | `engine/infrastructure/world_builder/sparsity.py` |
| `pyyaml` | Parse LLM output | `engine/infrastructure/world_builder/enrichment.py` |

### Existing Code

| Dependency | Used For | Notes |
|------------|----------|-------|
| `GraphQueries.semantic_search()` | Query by embedding | Already implemented |
| `GraphQueries.create_node()` | Create nodes | Already implemented |
| `GraphQueries.create_link()` | Create links | Already implemented |
| Embeddings | Node/link embeddings | Uses 'detail' or 'name' field |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `AGENTS_MODEL` | env | `claude` | CLI provider (`claude` or `codex`, loaded from `.env` if present) |
| `SPARSITY_PROXIMITY_THRESHOLD` | `engine/infrastructure/world_builder/sparsity.py` | 0.6 | Min embedding similarity |
| `SPARSITY_MIN_CLUSTER` | `engine/infrastructure/world_builder/sparsity.py` | 2 | Min results |
| `SPARSITY_MIN_DIVERSITY` | `engine/infrastructure/world_builder/sparsity.py` | 0.3 | Min result variety |
| `SPARSITY_MIN_CONNECTEDNESS` | `engine/infrastructure/world_builder/sparsity.py` | 1.5 | Min avg links |
| `QUERY_MOMENT_WEIGHT` | `engine/infrastructure/world_builder/query_moment.py` | 0.2 | Weight for query moments |
| `QUERY_MOMENT_ENERGY` | `engine/infrastructure/world_builder/query_moment.py` | 0.3 | Energy for query moments |
| `ENRICHMENT_CACHE_SECONDS` | `engine/infrastructure/world_builder/world_builder.py` | 60 | Cache duration |
| `LLM_MODEL` | `engine/infrastructure/world_builder/world_builder.py` | claude-sonnet-4-20250514 | Model |

---

## INTEGRATION

### Before (direct graph access)

```python
# Old - bypasses recording and enrichment
results = graph.query("MATCH (c:Character) WHERE c.name CONTAINS 'Edmund' RETURN c")
```

### After (through query())

```python
# New - recorded as thought, enriched if sparse, energy flows via physics
results = await query("What do I know about Edmund?", char_id="char_aldric")
```

### Usage by Components

| Component | Example | char_id | place_id |
|-----------|---------|---------|----------|
| Narrator | "What does Aldric feel?" | char_aldric | current |
| Frontend | "What's here?" | char_player | current |
| Click | "Tell me about sword" | char_player | current |
| Relationship | "How do I know him?" | char_player | - |

---

## TESTS

### Unit Tests

```python
def test_query_creates_moment():
    """Query should create a thought moment."""
    results = await query("test query", char_id="char_test")
    
    moment = graph.get_latest_moment()
    assert moment['type'] == 'thought'
    assert moment['text'] == "test query"
    assert moment['energy'] == 0.3

def test_query_links_results():
    """Query moment should link to results via ABOUT."""
    results = await query("known topic", char_id="char_test")
    
    moment = graph.get_latest_moment()
    about_links = graph.get_links(moment['id'], 'ABOUT')
    assert len(about_links) > 0

def test_sparse_triggers_enrichment():
    """Sparse results should trigger WorldBuilder."""
    results = await query("unknown obscure topic", char_id="char_test")
    
    # Should have created new content
    assert len(results) >= 2

def test_enrichment_links_to_query_moment():
    """All enriched content should link back to query moment."""
    results = await query("my relatives", char_id="char_test")
    
    moment = graph.get_latest_moment()
    about_links = graph.get_links(moment['id'], 'ABOUT')
    
    # Should include enriched nodes
    assert any(link['to'].startswith('char_') for link in about_links)

def test_moments_always_thought_type():
    """All created moments should be type=thought."""
    results = await query("memories of home", char_id="char_test")
    
    moments = graph.get_nodes_by_type('Moment')
    for m in moments:
        assert m['type'] == 'thought'
```

---

## GAPS / TODO

- [x] Implement all files in `engine/infrastructure/world_builder/`
- [x] YAML parsing with error handling (in `engine/infrastructure/world_builder/world_builder.py`)
- [ ] Integration tests with real FalkorDB
- [ ] Unit tests for sparsity detection
- [ ] End-to-end test with LLM enrichment

### Implementation Notes

- LLM failures: Returns `None`, caller decides what to do
- Generated content: Marked with `generated: true` property on nodes
- Query moments: Low weight (0.2), can surface but unlikely unless boosted
- Uses `SemanticSearch` from `engine/world/map/semantic.py` for vector search
- LLM transport: Agent CLI only (set `AGENTS_MODEL=claude` or `AGENTS_MODEL=codex`)

### Questions (Resolved)

- How to handle LLM failures? → Return None, log warning
- Should query moments ever surface as dialogue? → Yes, if energy high enough
- Mark generated vs authored content? → Yes, `generated: true` property

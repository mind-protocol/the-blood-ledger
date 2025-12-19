# Embeddings — Algorithm: Indexing

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
THIS:           ALGORITHM/ALGORITHM_Indexing.md
SEARCH:         ./ALGORITHM_Search.md
VALIDATION:     ../VALIDATION_Embeddings.md
IMPLEMENTATION: ../IMPLEMENTATION_Embeddings.md
TEST:           ../TEST/TEST_Overview.md
SYNC:           ../SYNC_Embeddings.md
IMPL:           ../../../../engine/infrastructure/embeddings/service.py
```

---

## ALGORITHM: index_node()

Embed a node's `detail` field, falling back to `name`. Store embedding as node attribute.

```python
def index_node(node: dict) -> Optional[List[float]]:
    detail = node.get('detail', '')
    name = node.get('name', '')

    if detail and len(detail) > 20:
        text = detail
    elif name and len(name) > 20:
        text = name
    else:
        return None

    vector = embed(text)
    node['embedding'] = vector
    return vector
```

---

## ALGORITHM: index_link()

Embed a link's `detail` field if > 20 chars. Store embedding as link attribute.

```python
def index_link(link: dict) -> Optional[List[float]]:
    detail = link.get('detail', '')

    if not detail or len(detail) <= 20:
        return None

    vector = embed(detail)
    link['embedding'] = vector
    return vector
```

---

## ALGORITHM: index_world()

Batch index existing content on world load.

```python
def index_world():
    for node in graph.get_all_nodes():
        index_node(node)

    for link in graph.get_all_links():
        index_link(link)
```

---

## ALGORITHM: on_scene_end()

Incremental indexing after each scene.

```python
def on_scene_end(mutations: List[dict]):
    for mutation in mutations:
        if mutation['type'] in ['new_narrative', 'new_character', 'update_node']:
            index_node(mutation['payload'])
        elif mutation['type'] in ['new_belief', 'update_link']:
            index_link(mutation['payload'])
```

---

## KEY DECISIONS

### D1: Embed or Skip

```
IF detail exists AND len(detail) > 20:
    embed(detail)
ELSE IF name exists AND len(name) > 20:
    embed(name)
ELSE:
    skip
```

### D2: ID Generation Strategy

```
Nodes:         emb_{type}_{id}_detail
Links:         emb_link_{link_type}_{link_id}_detail
Conversations: emb_convo_{char_id}_{slugified_section}
```

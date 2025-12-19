# Map System — Sync: Current State

```
LAST_UPDATED: 2025-12-19
STATUS: Partial implementation - semantic search complete, visual map pending
```

---

## CHAIN

PATTERNS:        ./PATTERNS_Map.md
BEHAVIORS:       ./BEHAVIORS_Map.md
ALGORITHM:       ./ALGORITHM_Rendering.md
VALIDATION:      ./VALIDATION_Map_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Map_Code_Architecture.md
TEST:            ./TEST_Map_Test_Coverage.md
THIS:            ./SYNC_Map.md

IMPL:            engine/world/map/semantic.py
---

## Current State

**Documentation complete.** Map system fully specified, with places/routes consolidated into a single algorithm doc. Consolidation verified during repair 17:
- Place schema and hierarchy
- Route computation and movement rules
- Canvas rendering with 7 layers
- Visibility system with 4 levels
- Interaction behaviors
Documentation repair 65: fixed implementation doc references to point at `engine/world/map/semantic.py` methods and removed the broken `DOCS:` path label.

Documentation chain completed for validation, implementation, and test coverage.

**Partial implementation:**

| Component | Status | Notes |
|-----------|--------|-------|
| Semantic Search | **Implemented** | `engine/world/map/semantic.py` |
| FalkorDB Integration | **Available** | Used via GraphQueries |
| Visual Map Rendering | Not started | Canvas layers, fog of war |
| Place/Route Display | Not started | Requires frontend setup |
| Visibility System | Not started | Player knowledge tracking |

---

## What's Implemented

### SemanticSearch (`engine/world/map/semantic.py`)

Natural language query layer for finding world content:

- `find(query, node_types, limit)` — Search by natural language
- `find_similar(node_id)` — Find nodes similar to given node
- `find_narratives_like(text)` — Find matching narratives
- `find_characters_like(description)` — Find matching characters
- `answer_question(question)` — Find nodes that answer a question

Uses FalkorDB vector search with fallback to brute-force similarity computation.

**Integration:**
- Uses `engine.infrastructure.embeddings` for embedding generation
- Uses `engine.physics.graph.GraphQueries` for database access

---

## What's NOT Implemented

### Visual Map System

The documented map features remain unimplemented:
- Canvas-based rendering with 7 layers
- Parchment aesthetic with hand-drawn feel
- Fog of war using multiply blend
- Place icons and labels
- Route visualization with waypoints
- Player position tracking
- Click-to-travel interaction

### Visibility/Knowledge System

Player-specific knowledge tracking:
- Unknown/Rumored/Known/Familiar states
- Fog of war reveal
- Discovery mechanics

---

## Documentation Status

| Doc | Purpose | Status |
|-----|---------|--------|
| `PATTERNS_Map.md` | Why this design | Complete |
| `BEHAVIORS_Map.md` | Visibility, interaction | Complete |
| `ALGORITHM_Rendering.md` | Rendering, places, routes, movement | Complete |
| `VALIDATION_Map_Invariants.md` | Semantic search invariants | Complete |
| `IMPLEMENTATION_Map_Code_Architecture.md` | Code architecture | Complete |
| `TEST_Map_Test_Coverage.md` | Test coverage | Complete (no tests yet) |
| `SYNC_Map.md` | Current state | This file |

---

## Dependencies for Visual Map

To implement the visual map system:
1. **Frontend canvas component** — React component with layered Canvas2D
2. **Place/Route data loading** — Query places from graph
3. **Visibility state storage** — Per-playthrough player knowledge
4. **Travel event handling** — Integration with Narrator

---

*"Semantic search is ready. The visual map awaits."*


---

## ARCHIVE

Older content archived to: `SYNC_Map_archive_2025-12.md`

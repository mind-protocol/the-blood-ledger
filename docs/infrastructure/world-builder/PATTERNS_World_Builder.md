# World Builder — Patterns: Query Moments and Sparse Enrichment

```
STATUS: CANONICAL
CREATED: 2025-12-19
VERIFIED: Not yet verified
```

---

## CHAIN

```
THIS:            PATTERNS_World_Builder.md (you are here)
BEHAVIORS:       ./BEHAVIORS_World_Builder.md
ALGORITHM:       ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:      ./VALIDATION/VALIDATION_Overview.md
IMPLEMENTATION:  ./IMPLEMENTATION/IMPLEMENTATION_Overview.md
HEALTH:          ./HEALTH_World_Builder.md
TEST:            ./TEST/TEST_Overview.md
SYNC:            ./SYNC_World_Builder.md

IMPL:            engine/infrastructure/world_builder/query.py
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in `docs/infrastructure/world-builder/SYNC_World_Builder.md`
3. Run tests: `pytest tests/infrastructure/world_builder/test_world_builder.py -v`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in `docs/infrastructure/world-builder/SYNC_World_Builder.md`
3. Run tests: `pytest tests/infrastructure/world_builder/test_world_builder.py -v`

---

## THE PROBLEM

The graph starts sparse; narrative queries often return thin or irrelevant results.
If we do nothing, the world feels empty and the system forgets the questions that
revealed the gaps. We need a mechanism that (1) records what was asked and
(2) enriches the graph when the answer is weak.

---

## THE PATTERN

**Query-as-Moment with Sparse-Triggered Enrichment.** Every natural-language
query creates a "thought" moment that links to its results. That moment becomes
the energy source for physics. When results are sparse, World Builder uses an
LLM to synthesize new nodes and links, then re-queries so the newly created
content participates in normal retrieval.

The key insight: **attention is energy** and does not require explicit injection.
Creating the moment and linking it via ABOUT is enough; physics handles salience.

---

## PRINCIPLES

### Principle 1: Every Query Leaves a Trace

Queries are recorded as thought moments, with ABOUT links to results. This makes
the graph self-documenting and ensures future surfacing is tied to actual player
attention, not hidden heuristics.

### Principle 2: Enrich Only When Sparse

LLM enrichment is expensive and should only fire when semantic sparsity rules
detect thin results. This keeps generation targeted and avoids flooding the graph.

### Principle 3: Generated Content Is Explicit

Enriched nodes and moments are marked as generated and linked back to the query
moment. This preserves provenance and keeps the enrichment surface auditable.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Graph runtime (ngram repo) | GraphQueries for node/link creation and semantic search (see `data/ARCHITECTURE — Cybernetic Studio.md`) |
| `engine/world/map/semantic.py` | Semantic search over embeddings |
| `engine/infrastructure/embeddings/**` | Embedding helpers for sparsity detection |
| `engine/infrastructure/orchestration/agent_cli.py` | LLM calls via agent CLI |

---

## INSPIRATIONS

- Event sourcing: queries become recorded events (moments) that shape future state.
- Sparse retrieval enrichment: fill missing knowledge only when needed.
- "Attention is energy" framing from the physics system to align with salience flow.

---

## SCOPE

### In Scope

- Recording queries as thought moments
- Linking query moments to search results via ABOUT
- Detecting semantic sparsity and triggering enrichment
- Applying LLM-generated nodes, links, and moments

### Out of Scope

- Physics tick and energy propagation → see `docs/physics/`
- Frontend or narrator UI interactions → see `docs/frontend/`, `docs/agents/`
- Canon and story validation rules → see `docs/infrastructure/canon/`

---

## GAPS / IDEAS / QUESTIONS

- [ ] Decide how to reconcile conflicting enrichments across repeated queries
- [ ] Define a review workflow for generated content
- IDEA: Add an explicit "force enrich" action for author tooling
- QUESTION: Should query moments ever surface as dialogue by default?

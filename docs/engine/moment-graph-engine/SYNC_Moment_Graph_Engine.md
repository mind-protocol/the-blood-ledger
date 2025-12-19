# Moment Graph Engine — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Instant_Traversal_Moment_Graph.md
BEHAVIORS:       ./BEHAVIORS_Traversal_And_Surfacing.md
ALGORITHM:       ./ALGORITHM_Click_Wait_Surfacing.md
VALIDATION:      ./VALIDATION_Moment_Traversal_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Moment_Graph_Runtime_Layout.md
TEST:            ./TEST_Moment_Graph_Runtime_Coverage.md
THIS:            SYNC_Moment_Graph_Engine.md (you are here)
IMPL:            engine/moment_graph/__init__.py
```

---

## MATURITY

**What's canonical (v1):**
- Traversal, query, and surfacing helpers implemented in `engine/moment_graph/`.
- Hot-path goal of sub-50ms graph operations with no LLM calls.

**What's still being designed:**
- Formal validation invariants for traversal/surfacing.
- Integration performance benchmarks and thresholds.

**What's proposed (v2+):**
- Expanded surface heuristics and richer transition strategies.

---

## CURRENT STATE

Moment graph traversal, query, and surfacing logic lives in `engine/moment_graph/`
with explicit click/wait transitions, weight updates, and surfacing thresholds.
The module relies on physics graph ops/queries and is treated as a hot path.

---

## RECENT CHANGES

### 2025-12-19: Documented moment graph engine module

- **What:** Added docs and mapped the module in `modules.yaml`.
- **Why:** Close the undocumented engine/moment_graph module gap.
- **Files:** `docs/engine/moment-graph-engine/`, `modules.yaml`,
  `engine/moment_graph/__init__.py`
- **Struggles/Insights:** Keeping this distinct from the schema-first
  `docs/engine/moments/` module avoids doc duplication.

### 2025-12-19: Clarified implementation references

- **What:** Removed class/method references that were misread as file paths.
- **Why:** Avoid false broken-link reports from health checks.
- **Files:** `docs/engine/moment-graph-engine/IMPLEMENTATION_Moment_Graph_Runtime_Layout.md`

### 2025-12-19: Verified moment graph query helpers

- **What:** Reviewed `get_dormant_moments`, `get_wait_triggers`, and
  `get_moments_attached_to_tension` in `engine/moment_graph/queries.py`.
- **Why:** Repair task flagged incomplete implementations.
- **Files:** `engine/moment_graph/queries.py`
- **Result:** Implementations already present; no code changes required.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documentation only; no code changes beyond DOCS reference.

**What you need to understand:** This module is the runtime traversal/surfacing
engine; schema and contract docs live in `docs/engine/moments/`.

**Watch out for:** Performance expectations ("<50ms") in docstrings are
assumptions; validate against real graph benchmarks before tightening.

---

## TODO

### Doc/Impl Drift

- [ ] Document additional invariants if traversal logic changes.

### Tests to Run

```bash
pytest engine/tests/test_moment_graph.py -v
pytest engine/tests/test_e2e_moment_graph.py -v -s
```

## Agent Observations

### Remarks
- Repair task identified incomplete functions, but the current
  `engine/moment_graph/queries.py` implementations are already in place.

### Suggestions
- None.

### Propositions
- None.

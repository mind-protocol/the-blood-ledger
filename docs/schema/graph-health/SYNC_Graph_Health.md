# Graph Health — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Graph_Health_Validation.md
THIS:            SYNC_Graph_Health.md
```

---

## MATURITY

**What's canonical (v1):**
- Schema-driven health check CLI (`check_health.py`).
- Schema validation test suite (`test_schema.py`).
- Curated query set with quality ratings (`example_queries.cypher`).

**What's still being designed:**
- How health checks integrate into CI or automated workflows.
- Whether link property validation needs deeper coverage.

**What's proposed (v2+):**
- Exportable reports (CSV/markdown) for audit trails.
- Automated repair suggestions or optional fix mode.

---

## CURRENT STATE

The graph health module provides a YAML-backed schema (`schema.yaml`), a CLI
health check that reports missing required fields and invalid enums, a pytest
suite for schema invariants, and a terminology linter for NPC/character naming.
Query artifacts include a rated Cypher library plus expected/actual outputs to
make inspection repeatable.

---

## RECENT CHANGES

### 2025-12-19: Documented graph health module

- **What:** Added PATTERNS + SYNC docs and mapped the module in `modules.yaml`.
- **Why:** The health tooling was undocumented; repairs require a doc chain.
- **Files:** `docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md`,
  `docs/schema/graph-health/SYNC_Graph_Health.md`, `modules.yaml`,
  `engine/graph/health/check_health.py`
- **Struggles/Insights:** Kept docs minimal to avoid duplicating schema docs.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documented the graph health module and added a DOCS link.

**What you need to understand:**
Schema validation is centered on `schema.yaml`, with both CLI and pytest entry
points. The query library is a static asset meant for human use.

**Watch out for:**
Doc chain is minimal; add BEHAVIORS/ALGORITHM/VALIDATION/IMPLEMENTATION/TEST if
this module becomes a frequent touchpoint.

---

## TODO

### Tests to Run

```bash
python engine/graph/health/check_health.py --graph seed
pytest engine/graph/health/test_schema.py -v
python engine/graph/health/lint_terminology.py --graph seed
```

### Immediate

- [ ] Decide whether to add full doc chain (BEHAVIORS/ALGORITHM/etc.).

---

## POINTERS

| What | Where |
|------|-------|
| Health check CLI | `engine/graph/health/check_health.py` |
| Schema tests | `engine/graph/health/test_schema.py` |
| Terminology linter | `engine/graph/health/lint_terminology.py` |
| Schema definition | `engine/graph/health/schema.yaml` |
| Query library | `engine/graph/health/example_queries.cypher` |

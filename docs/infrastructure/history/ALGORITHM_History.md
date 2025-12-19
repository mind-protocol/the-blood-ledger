# History — Algorithm (Entry Point)

```
STATUS: DRAFT
CREATED: 2024-12-16
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_History.md
BEHAVIORS:   ./BEHAVIORS_History.md
THIS:        ALGORITHM_History.md
OVERVIEW:    ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:  ./VALIDATION_History.md
IMPLEMENTATION: ./IMPLEMENTATION_History_Service_Architecture.md
TEST:        ./TEST/TEST_Overview.md
SYNC:        ./SYNC_History.md
```

---

## ENTRY

Primary algorithm documentation now lives under `docs/infrastructure/history/ALGORITHM/`.
Start with `ALGORITHM/ALGORITHM_Overview.md` to understand the narrative and
belief recording flow before following any sub-doc paths.

---

## OVERVIEW

This entry point exists to route readers to the authoritative algorithm
documents without duplicating procedures. Use it to confirm where each
history workflow is documented (overview and conversations) before diving in.

---

## DATA STRUCTURES

### Algorithm Map

```
Entry point that enumerates the history algorithm sub-docs and clarifies
which file owns the narrative/belief flow versus conversation storage details.
```

---

## ALGORITHM: History Documentation Entry

### Step 1: Read the overview

Start with `ALGORITHM/ALGORITHM_Overview.md` to review the core HistoryService
flow, including narrative creation, belief propagation, and query framing.

### Step 2: Follow the conversation path

Use `ALGORITHM/ALGORITHM_Query_and_Record.md` for the narrative recording
flow, query shapes, and the conversation thread integration points.

### Step 3: Follow the belief propagation path

Use `ALGORITHM/ALGORITHM_Propagation_and_Beliefs.md` for how beliefs spread,
what edges are created, and how proximity affects memory diffusion.

---

## KEY DECISIONS

### D1: Keep this file as routing only

```
IF a detailed algorithm changes:
    update the sub-doc and keep this file as navigation
ELSE:
    avoid duplicating logic that belongs in the sub-docs
```

---

## DATA FLOW

```
Reader intent
    ↓
ALGORITHM_History.md (entry and routing)
    ↓
ALGORITHM_Overview / ALGORITHM_Query_and_Record / ALGORITHM_Propagation_and_Beliefs
```

---

## COMPLEXITY

**Time:** O(1) — this file is static documentation routing.

**Space:** O(1) — no data storage or computation is performed here.

**Bottlenecks:**
- Routing drift if sub-doc names change without updating this entry point.
- Missing coverage if new algorithm docs are added without being linked here.

---

## HELPER FUNCTIONS

### `open_overview_doc()`

**Purpose:** Direct readers to the core HistoryService algorithm summary.

**Logic:** Reference `ALGORITHM/ALGORITHM_Overview.md` and keep it canonical.

### `open_query_record_doc()`

**Purpose:** Route history query and recording questions to the detail doc.

**Logic:** Use `ALGORITHM/ALGORITHM_Query_and_Record.md` as the source of truth.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/infrastructure/history/ALGORITHM/ALGORITHM_Overview.md | Read | Primary flow description |
| docs/infrastructure/history/ALGORITHM/ALGORITHM_Query_and_Record.md | Read | Query/record steps |
| docs/infrastructure/history/ALGORITHM/ALGORITHM_Propagation_and_Beliefs.md | Read | Belief propagation details |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm the query/record algorithm file name stays stable as a link target.
- IDEA: Add an additional routing bullet if new history sub-docs are added.

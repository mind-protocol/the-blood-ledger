# Archived: SYNC_Async_Architecture.md

Archived on: 2025-12-20
Original file: SYNC_Async_Architecture.md

---

## RECENT CHANGES

### 2025-12-19: Restore missing SYNC template sections

- **What:** Added MATURITY, CURRENT STATE, IN PROGRESS, handoffs, TODO,
  CONSCIOUSNESS TRACE, and POINTERS sections with narrative context.
- **Why:** The DOC_TEMPLATE_DRIFT check requires all SYNC sections so
  the async module can be handed off without ambiguity.
- **Files:** `docs/infrastructure/async/SYNC_Async_Architecture.md`
- **Struggles/Insights:** Keeping the detailed capability tables while
  inserting template sections required careful ordering to avoid duplication.

### 2025-12-19: Async docs template alignment

- **What:** Expanded async docs (algorithm, test, implementation references)
  and recorded the injection queue format decision.
- **Why:** Resolve the template drift warning and clarify the async stack.
- **Files:** `docs/infrastructure/async/ALGORITHM_Async_Architecture.md`,
  `docs/infrastructure/async/TEST_Async_Architecture.md`,
  `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md`,
  `docs/infrastructure/async/SYNC_Async_Architecture.md`
- **Struggles/Insights:** Multiple queue formats exist; documenting the split
  prevents silent drift while follow-up work is planned.

---


## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Ensure hook consumer and API endpoints converge on JSONL
  queue semantics before implementing travel interrupts.

### Tests to Run

```bash
ngram validate
```

### Immediate

- [ ] Decide on a single injection queue format (JSONL vs JSON array) and
  update docs + scripts accordingly.

### Later

- [ ] Define SSE event payload schemas for map, image, and travel updates.
- IDEA: Capture a short ADR for queue format decisions if ambiguity persists.

---


## POINTERS

| What | Where |
|------|-------|
| Async patterns and design | `docs/infrastructure/async/PATTERNS_Async_Architecture.md` |
| Async algorithm entry point | `docs/infrastructure/async/ALGORITHM_Async_Architecture.md` |
| Async implementation notes | `docs/infrastructure/async/IMPLEMENTATION_Async_Architecture.md` |
| Async test plan | `docs/infrastructure/async/TEST_Async_Architecture.md` |
| Async archive notes | `docs/infrastructure/async/archive/SYNC_archive_2024-12.md` |

---


- Filled missing sections in `PATTERNS_Async_Architecture.md` (problem, pattern,
  principles, dependencies, inspirations, scope, gaps) to resolve the remaining
  DOC_TEMPLATE_DRIFT requirement for repair #16.
- Expanded `TEST_Async_Architecture.md` with full test template sections
  (strategy, unit/integration coverage, edge cases, coverage, run guidance,
  known gaps, flaky tracking, and open questions) to resolve DOC_TEMPLATE_DRIFT
  for repair #16.
- Expanded the async algorithm entry point with full template sections (overview,
  data structures, primary algorithm steps, decisions, data flow, complexity,
  helpers, interactions, gaps) to resolve DOC_TEMPLATE_DRIFT for repair #16.
- Verified the async implementation doc already lists the `engine/scripts/inject_to_narrator.py` code-to-docs link and aligned the hook-script path in this SYNC table.
- Updated async implementation doc to replace runtime-only file references with configured script paths so all references point to tracked files.
- Refreshed the async implementation doc to match current queue file formats/paths (JSONL default queue, JSON array per playthrough) and updated entry point lines and config table; noted the playthrough initialization mismatch as a gap.
- Reverified `IMPLEMENTATION_Async_Architecture.md` after the broken-link report; no additional path corrections were needed.
- Split async algorithm docs into `docs/infrastructure/async/ALGORITHM/` with an overview and focused parts (Runner, Hook, Graph SSE, Waypoints/Fog, Image Generation, Discussion Trees), added `ALGORITHM_Async_Architecture.md` as the entry point, and updated CHAIN references.
- Added `IMPLEMENTATION_Async_Architecture.md`, linked CHAIN references, and added DOCS pointer in `engine/scripts/check_injection.py`.
- Added DOCS pointer in `engine/scripts/inject_to_narrator.py` so the manual injector resolves to the async implementation chain.
- Archived verbose discussion tree details and the data flow diagram to `docs/infrastructure/async/archive/SYNC_archive_2024-12.md` to keep module docs under size limits.

---


# Repair Task

**Issue Type:** LARGE_DOC_MODULE
**Severity:** warning
**Target:** docs/infrastructure/api

## Instructions
## Task: Reduce Documentation Size

**Target:** `docs/infrastructure/api`
**Problem:** Total 61K chars (threshold: 50K)
**File sizes:** [('SYNC_Api.md', '18K'), ('ALGORITHM_Api.md', '15K'), ('IMPLEMENTATION_Api.md', '12K'), ('ALGORITHM_Playthrough_Creation.md', '5K'), ('PATTERNS_Api.md', '2K')]

## Steps:

1. Read the docs in the module folder
2. Identify content that can be reduced:
   - Old/archived sections -> move to dated archive file
   - Duplicate information -> consolidate
   - Verbose explanations -> make concise
   - Implementation details that changed -> update or remove
3. For large individual files (~300+ lines), split into a folder:
   - Any doc type can become a folder when too large
   - Example: `ALGORITHM.md` -> `ALGORITHM/ALGORITHM_Overview.md`, `ALGORITHM_Details.md`
   - Keep an overview file as entry point
4. Update CHAIN sections after any splits
5. Update SYNC with what was reorganized

## Splitting pattern for any doc type:
```
DOC_TYPE.md (too large) -> DOC_TYPE/
├── DOC_TYPE_Overview.md      # Entry point, high-level
├── DOC_TYPE_Part1.md         # Focused section
├── DOC_TYPE_Part2.md         # Another section
```

## Archiving pattern:
- Create `docs/infrastructure/api/archive/SYNC_archive_2024-12.md` for old content
- Keep only current state in main docs

## Success Criteria:
- Total chars under 50K
- Individual files under ~300 lines
- Content is current and relevant
- No duplicate information
- CHAIN links still work

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Refactor_Improve_Code_Structure.md
- docs/infrastructure/api

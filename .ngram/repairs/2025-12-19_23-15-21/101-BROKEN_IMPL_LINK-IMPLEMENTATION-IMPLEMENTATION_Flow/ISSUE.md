# Repair Task

**Issue Type:** BROKEN_IMPL_LINK
**Severity:** critical
**Target:** docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Flow.md

## Instructions
## Task: Fix Broken Implementation Links

**Target:** `docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Flow.md`
**Problem:** References 6 non-existent file(s)
**Missing files:** ['query_moment.py', 'sparsity.py', 'world_builder.py', 'query.py', 'archive/SYNC_archive_2024-12.md', 'enrichment.py']

## Steps:

1. Read the IMPLEMENTATION doc
2. For each missing file reference:
   - Search the codebase for the actual file location
   - If file was moved: update the path in the doc
   - If file was renamed: update the reference
   - If file was deleted: remove the reference or note it's deprecated
3. Verify all remaining file references point to existing files
4. Update SYNC with what you fixed

## Success Criteria:
- All file references in IMPLEMENTATION doc point to existing files
- No broken links remain
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Document_Create_Module_Documentation.md
- docs/infrastructure/world-builder/IMPLEMENTATION/IMPLEMENTATION_Flow.md

# Repair Task

**Issue Type:** STALE_IMPL
**Severity:** warning
**Target:** docs/agents/narrator/IMPLEMENTATION_Narrator.md

## Instructions
## Task: Update Stale IMPLEMENTATION Doc

**Target:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`
**Problem:** 5 referenced files not found
**Missing files:** ['engine/infrastructure/orchestration/narrator_prompt.py', 'narrator_prompt.py', 'stream_dialogue.py', 'narrator.py', 'graph_ops.py']
**New files:** []

The IMPLEMENTATION doc doesn't match the actual files in the codebase.

## Steps:

1. Read the current IMPLEMENTATION doc
2. Compare against actual files in the module
3. For missing files (referenced but don't exist):
   - If renamed: update the path
   - If deleted: remove from doc
4. For new files (exist but not documented):
   - Add to CODE STRUCTURE section
   - Add to File Responsibilities table
5. Update data flow diagrams if needed
6. Update SYNC

## Success Criteria:
- All files in doc exist in codebase
- All files in codebase are in doc
- File descriptions are accurate

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Document_Create_Module_Documentation.md
- docs/agents/narrator/IMPLEMENTATION_Narrator.md

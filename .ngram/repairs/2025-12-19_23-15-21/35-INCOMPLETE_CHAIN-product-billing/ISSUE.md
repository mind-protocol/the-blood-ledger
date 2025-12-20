# Repair Task

**Issue Type:** INCOMPLETE_CHAIN
**Severity:** warning
**Target:** docs/product/billing

## Instructions
## Task: Complete Documentation Chain

**Target:** `docs/product/billing`
**Missing docs:** ['ALGORITHM']
**Existing docs:** ['PATTERNS', 'BEHAVIORS', 'ALGORITHM', 'VALIDATION', 'IMPLEMENTATION', 'TEST', 'SYNC']

## CRITICAL: Check for existing docs first

Before creating any missing doc type:
- Search `docs/` for existing docs of that type that might cover this module
- Check if the missing doc exists in a different location or with different name
- If found elsewhere, link to it instead of creating a duplicate

## IMPLEMENTATION doc guidance

One IMPLEMENTATION doc per module that documents ALL files in that module.

**File Responsibilities table MUST include:**
- Line count for each file (approximate)
- Status: OK (<400L), WATCH (400-700L), or SPLIT (>700L)
- Any WATCH/SPLIT files need extraction candidates in GAPS section

**DESIGN PATTERNS section MUST include:**
- Architecture pattern (MVC, Layered, Pipeline, etc.) and WHY
- Code patterns in use (Factory, Strategy, etc.) and WHERE
- Anti-patterns to avoid in this module
- Boundary definitions (what's inside vs outside)

**Structure:**
- List all files in CODE STRUCTURE section
- Document each file's purpose in File Responsibilities table
- Define design patterns and boundaries
- Show data flows between files

If the IMPLEMENTATION doc exceeds ~300 lines, split into folder:
```
IMPLEMENTATION/
├── IMPLEMENTATION_Overview.md      # Entry point, high-level structure
├── IMPLEMENTATION_DataFlow.md      # How data moves
├── IMPLEMENTATION_Components.md    # Individual file details
```

## Steps:

1. Read the VIEW doc and modules.yaml
2. Read existing docs in `docs/product/billing` to understand the module
3. For EACH missing doc type:
   a. Search for existing docs: `grep -r "PATTERN_TYPE" docs/`
   b. If found: update CHAIN to link to existing doc
   c. If not found: create using templates from `.ngram/templates/`
4. Ensure CHAIN sections link all docs together
5. Update SYNC with what you created/linked

## Success Criteria:
- Missing doc types are present (created or linked)
- NO duplicate documentation created
- CHAIN sections link correctly

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Document_Create_Module_Documentation.md
- modules.yaml

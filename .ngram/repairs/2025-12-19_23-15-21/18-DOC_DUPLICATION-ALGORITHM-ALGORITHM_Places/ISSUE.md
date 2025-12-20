# Repair Task

**Issue Type:** DOC_DUPLICATION
**Severity:** warning
**Target:** docs/world/map/ALGORITHM/ALGORITHM_Places.md

## Instructions
## Task: Consolidate Duplicate Documentation

**Target:** `docs/world/map/ALGORITHM/ALGORITHM_Places.md`
**Problem:** Multiple ALGORITHM docs in `ALGORITHM/`
**Details:** {'doc_type': 'ALGORITHM', 'folder': 'ALGORITHM', 'docs': ['docs/world/map/ALGORITHM/ALGORITHM_Places.md', 'docs/world/map/ALGORITHM/ALGORITHM_Rendering_Pipeline.md', 'docs/world/map/ALGORITHM/ALGORITHM_Routes.md', 'docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Overview.md', 'docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Search.md', 'docs/infrastructure/embeddings/ALGORITHM/ALGORITHM_Indexing.md', 'docs/infrastructure/history/ALGORITHM/ALGORITHM_Overview.md', 'docs/infrastructure/history/ALGORITHM/ALGORITHM_Query_and_Record.md', 'docs/infrastructure/history/ALGORITHM/ALGORITHM_Propagation_and_Beliefs.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Overview.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Hook_Injection.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Waypoints_And_Fog.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Runner_Protocol.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Discussion_Trees.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Image_Generation.md', 'docs/infrastructure/async/ALGORITHM/ALGORITHM_Graph_SSE.md', 'docs/infrastructure/world-builder/ALGORITHM/ALGORITHM_Overview.md', 'docs/infrastructure/world-builder/ALGORITHM/ALGORITHM_Details.md']}

Documentation duplication wastes context and creates inconsistency risk.

## Duplication Types

1. **Same file in multiple IMPLEMENTATION docs**
   - One file should be documented in exactly one IMPLEMENTATION doc
   - Remove references from all but the primary module's doc

2. **Multiple docs of same type in same folder**
   - Merge into single doc (e.g., two PATTERNS files -> one)
   - Or split into subfolders if genuinely different modules

3. **Similar content across docs**
   - If >60% similar, one is probably redundant
   - Consolidate into the canonical location
   - Remove or replace the duplicate with a reference

## Steps:

1. Read the flagged doc and its "similar" doc
2. Determine which is the canonical source:
   - More complete? More recently updated? In better location?
3. For file references: keep in the owning module's IMPLEMENTATION only
4. For content duplication:
   - Merge unique content into canonical doc
   - Replace duplicate with: `See [Doc Name](path/to/canonical.md)`
   - Or delete if truly redundant
5. Update CHAIN sections to reflect new structure
6. Update SYNC with consolidation done

## Success Criteria:
- No duplicate file references
- No redundant content
- Clear canonical location for each topic
- CHAIN links updated
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Document_Create_Module_Documentation.md
- docs/world/map/ALGORITHM/ALGORITHM_Places.md

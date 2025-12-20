# VIEW: Analyze — Structural Analysis and Recommendations

**You're analyzing the codebase structure to understand what exists, what's needed, and recommend improvements.**

---

## WHY THIS VIEW EXISTS

Before building or refactoring, you need the full picture. This view is for:
- Understanding the current shape of the codebase
- Identifying structural gaps, redundancies, or misalignments
- Recommending reorganization or new modules
- Aligning implementation with vision

This is analysis work, not implementation. The output is understanding and recommendations.

---

## CONTEXT TO LOAD

**FIRST: Generate and read the overview before any analysis.**

### Step 1: Generate Repository Map

```bash
ngram overview
```

This creates `map.md` with:
- File tree with character counts
- Bidirectional links (code↔docs)
- Function definitions and section headers
- Module dependencies
- Statistics

**Read `map.md` thoroughly.** This is your primary source of truth for what exists.

### Step 2: Read Vision and Architecture

```
.ngram/state/SYNC_Project_State.md     — current focus and recent changes
docs/concepts/                          — cross-cutting ideas (if exists)
```

Look for any vision, goals, or architecture documents:
```
docs/**/PATTERNS_*.md                   — design philosophy per module
docs/**/SPEC_*.md or VISION_*.md        — high-level specs (if exists)
README.md                               — project overview
```

### Step 3: Read Module Documentation

For each major area in `docs/`:
```
docs/{area}/SYNC_*.md                   — area status
docs/{area}/{module}/PATTERNS_*.md      — module design intent
docs/{area}/{module}/IMPLEMENTATION_*.md — code structure
```

---

## ANALYSIS CHECKLIST

### Structure Analysis

- [ ] **File organization**: Do files live where they belong? Are there orphans?
- [ ] **Module boundaries**: Are modules cohesive? Clear responsibilities?
- [ ] **Size distribution**: Any monoliths? Files that need splitting?
- [ ] **Naming conventions**: Consistent? Meaningful?
- [ ] **Dependency flow**: Clean hierarchy? Circular dependencies?

### Documentation Analysis

- [ ] **Coverage**: Do all significant modules have docs?
- [ ] **Freshness**: Do docs match current code?
- [ ] **Links**: Are code↔docs links bidirectional and valid?
- [ ] **SYNC status**: Are SYNC files current?

### Alignment Analysis

- [ ] **Vision alignment**: Does structure serve stated goals?
- [ ] **Pattern consistency**: Are similar things done similarly?
- [ ] **Gap identification**: What's missing that should exist?
- [ ] **Redundancy check**: Are there duplicates or near-duplicates?

---

## OUTPUT FORMAT

Your analysis should produce:

### 1. Current State Summary

```markdown
## Current Structure

**Stats:** X files, Y modules, Z areas
**Health:** [from ngram doctor if run]

### Strengths
- [What's well-organized]

### Concerns
- [Structural issues found]
```

### 2. Recommendations

```markdown
## Recommendations

### High Priority
- [ ] [Critical structural changes]

### Medium Priority
- [ ] [Important improvements]

### Low Priority / Future
- [ ] [Nice-to-have reorganizations]
```

### 3. Proposed Structure (if major changes)

```markdown
## Proposed Structure

```
src/
├── {proposed}/
│   └── {new_organization}/
```

### Rationale
[Why this structure is better]

### Migration Path
[How to get from current to proposed]
```

---

## AFTER ANALYSIS

### Update SYNC

Add your analysis to `.ngram/state/SYNC_Project_State.md`:

```markdown
## Structural Analysis — [DATE]

### Summary
[Key findings]

### Recommendations
- [ ] [Actionable items]

### Next Steps
[What should happen next]
```

---

## HANDOFF

**For implementation agent:** Clear list of what to change, in what order, with rationale.

**For human:** Executive summary of findings, prioritized recommendations, any decisions needed.

---

## VERIFICATION

- Overview generated and read
- Vision/architecture docs consulted
- All major modules examined
- Recommendations are specific and actionable
- SYNC updated with analysis results

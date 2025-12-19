# Vision - Implementation: Documentation Architecture

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Vision.md
BEHAVIORS:      ./BEHAVIORS_Vision.md
ALGORITHM:      ./ALGORITHM_Vision.md
VALIDATION:     ./VALIDATION_Vision.md
THIS:           IMPLEMENTATION_Vision.md
TEST:           ./TEST_Vision.md
SYNC:           ./SYNC_Vision.md

IMPL:           docs/design/PATTERNS_Vision.md
```

> Contract: Read docs before modifying. After changes: update this doc or add TODOs to SYNC. Run tests where applicable.

Note: This module is documentation-only; the IMPL reference points to the primary entry doc.

---

## CODE STRUCTURE

```
docs/design/PATTERNS_Vision.md
docs/design/BEHAVIORS_Vision.md
docs/design/ALGORITHM_Vision.md
docs/design/VALIDATION_Vision.md
docs/design/IMPLEMENTATION_Vision.md
docs/design/TEST_Vision.md
docs/design/SYNC_Vision.md
docs/design/opening/PATTERNS_Opening.md
docs/design/opening/BEHAVIORS_Opening.md
docs/design/opening/ALGORITHM_Opening.md
docs/design/opening/VALIDATION_Opening.md
docs/design/opening/TEST_Opening.md
docs/design/opening/SYNC_Opening.md
docs/design/opening/GUIDE.md
docs/design/opening/CONTENT.md
docs/design/opening/CLAUDE.md
docs/design/opening/opening.json
docs/design/scenarios/README.md
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|-----------------------|-------|--------|
| `docs/design/PATTERNS_Vision.md` | Vision rationale and design principles | N/A | 320 | OK |
| `docs/design/BEHAVIORS_Vision.md` | Player experience targets and behaviors | N/A | 409 | WATCH |
| `docs/design/ALGORITHM_Vision.md` | System mapping from vision to mechanics | N/A | 323 | OK |
| `docs/design/VALIDATION_Vision.md` | Validation plan and success criteria | N/A | 193 | OK |
| `docs/design/IMPLEMENTATION_Vision.md` | Documentation architecture and file map | N/A | 225 | OK |
| `docs/design/TEST_Vision.md` | Experience metrics and test signals | N/A | 38 | OK |
| `docs/design/SYNC_Vision.md` | Vision status and handoff notes | N/A | 102 | OK |
| `docs/design/opening/PATTERNS_Opening.md` | Opening-specific design rationale | N/A | 136 | OK |
| `docs/design/opening/BEHAVIORS_Opening.md` | Opening experience behaviors | N/A | 153 | OK |
| `docs/design/opening/ALGORITHM_Opening.md` | Opening flow outline | N/A | 33 | OK |
| `docs/design/opening/VALIDATION_Opening.md` | Opening validation criteria | N/A | 158 | OK |
| `docs/design/opening/TEST_Opening.md` | Opening test signals | N/A | 29 | OK |
| `docs/design/opening/SYNC_Opening.md` | Opening status and notes | N/A | 62 | OK |
| `docs/design/opening/GUIDE.md` | Opening guidance and process | N/A | 311 | OK |
| `docs/design/opening/CONTENT.md` | Opening script content | N/A | 327 | OK |
| `docs/design/opening/CLAUDE.md` | Narrator agent operating guide | N/A | 728 | SPLIT |
| `docs/design/opening/opening.json` | Opening data payload | N/A | 401 | WATCH |
| `docs/design/scenarios/README.md` | Scenario capture and usage notes | N/A | 329 | OK |

**Size Thresholds:**
- OK (<400 lines): Healthy size, easy to understand
- WATCH (400-700 lines): Getting large, consider extraction opportunities
- SPLIT (>700 lines): Too large, split before adding more content

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Layered documentation chain

**Why this pattern:** The vision docs define the core game intent, while the opening and scenarios folders provide applied detail. Keeping a layered chain prevents the opening content from drifting away from the core vision.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Documentation chain | `docs/design/TEST_Vision.md`, `docs/design/IMPLEMENTATION_Vision.md` | Explicitly links vision docs for navigation |
| Template-driven docs | `docs/design/`, `docs/design/opening/` | Keeps documentation structured and comparable |

### Anti-Patterns to Avoid

- **Duplicate vision docs**: Avoid parallel vision writeups in other areas; extend this module instead.
- **Unlinked submodules**: Opening/scenarios docs must point back to vision intent, not drift.
- **Overgrown guide files**: Split large doc guides (e.g., CLAUDE.md) before adding new sections.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Vision core | `docs/design/` | Engine/frontend modules | CHAIN references, shared terminology |
| Opening submodule | `docs/design/opening/` | Vision core docs | References in GUIDE/CONTENT |
| Scenarios | `docs/design/scenarios/` | Opening/vision docs | Scenario index links |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Vision rationale | `docs/design/PATTERNS_Vision.md:1` | Vision review or design decisions |
| Experience targets | `docs/design/BEHAVIORS_Vision.md:1` | UX/experience planning |
| System mapping | `docs/design/ALGORITHM_Vision.md:1` | System decomposition |
| Validation plan | `docs/design/VALIDATION_Vision.md:1` | Testing/acceptance planning |
| Metrics | `docs/design/TEST_Vision.md:1` | Test planning |
| Current state | `docs/design/SYNC_Vision.md:1` | Handoff or status check |

---

## DATA FLOW

### Vision to Opening: Vision intent informs the opening experience

```
PATTERNS/BEHAVIORS/ALGORITHM
        │
        ▼
Opening GUIDE/CONTENT
        │
        ▼
Opening payload (opening.json)
```

### Vision to Validation: Success criteria inform tests

```
VALIDATION_Vision.md
        │
        ▼
TEST_Vision.md
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
docs/design/TEST_Vision.md
    └── references -> docs/design/PATTERNS_Vision.md
docs/design/opening/
    └── depends on -> docs/design/
```

### External Dependencies

None. This module is documentation-only.

---

## STATE MANAGEMENT

Not applicable. This module is documentation-only.

---

## RUNTIME BEHAVIOR

Not applicable. This module is documentation-only.

---

## CONCURRENCY MODEL

Not applicable. This module is documentation-only.

---

## CONFIGURATION

Not applicable. This module is documentation-only.

---

## BIDIRECTIONAL LINKS

### Code -> Docs

None. This module does not have code files.

### Docs -> Code

None. This module does not map to implementation code.

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `docs/design/BEHAVIORS_Vision.md` | 409L | <400L | Proposed: split into a new drives/metrics behaviors doc (name TBD) | Octalysis framework + metrics section |
| `docs/design/opening/CLAUDE.md` | 728L | <400L | Proposed: split into core loop + tool reference docs (names TBD) | Tool call reference and operational checklists |
| `docs/design/opening/opening.json` | 401L | <400L | Proposed: split into per-scene JSON payloads (names TBD) | Split by scene/section payloads |

### Missing Implementation

- None identified for the documentation chain itself.

### Questions

- Should the vision docs add CHAIN blocks to all files for consistency?

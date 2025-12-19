# History — Sync: Current State

```
LAST_UPDATED: 2024-12-16
UPDATED_BY: Claude (documentation session)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Core pattern: distributed history through narratives + beliefs
- Two sources: player-experienced (conversation refs) vs world-generated (detail field)
- Timestamp format: "Day N, time_of_day"
- BELIEVES edge structure with confidence, source, when, where

**What's still being designed:**
- Actual query implementation in Cypher
- Conversation file structure and location
- Propagation algorithm specifics
- Integration with Chronicle view

**What's proposed (v2+):**
- Memory decay over time
- Confidence degradation with retellings
- Player journal entries as narratives
- "Actively trying to remember" mechanic

---

## CURRENT STATE

Documentation complete. Implementation not started.

The History module has a complete documentation chain:
- PATTERNS: Why distributed memory (philosophy)
- BEHAVIORS: Observable effects (what the system does)
- ALGORITHM: How queries and recording work (procedures)
- VALIDATION: Invariants and test criteria
- TEST: Test cases and coverage gaps

No code exists yet. This is design documentation for a system to be built.

---

## IN PROGRESS

### Documentation Creation

- **Started:** 2024-12-16
- **By:** Claude
- **Status:** Complete
- **Context:** Created full doc chain for History module based on design principles from CLAUDE.md system reminder

---

## RECENT CHANGES

### 2024-12-16: Initial Documentation

- **What:** Created docs/infrastructure/history/ with full PATTERN → TEST chain
- **Why:** History system is core to "they remembered" experience; needed documented before implementation
- **Files:**
  - docs/infrastructure/history/PATTERNS_History.md
  - docs/infrastructure/history/BEHAVIORS_History.md
  - docs/infrastructure/history/ALGORITHM_History.md
  - docs/infrastructure/history/VALIDATION_History.md
  - docs/infrastructure/history/TEST_History.md
  - docs/infrastructure/history/SYNC_History.md
- **Insights:** The pattern of "narratives as index, conversations as content" is elegant but needs careful file management

---

## KNOWN ISSUES

### No Implementation

- **Severity:** High (blocking)
- **Symptom:** Can't actually query or record history
- **Suspected cause:** Not built yet
- **Attempted:** N/A — this is expected state

### Conversation File Location Undecided

- **Severity:** Medium
- **Symptom:** Docs reference "conversations/char_aldric.md" but location not finalized
- **Suspected cause:** Need to decide project file structure
- **Attempted:** N/A

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Documentation complete. Ready for implementation.

**What you need to understand:**
- History is NOT a separate system — it's narratives + beliefs in the graph
- Two recording paths: player-experienced (append conversation, create narrative with source ref) vs world-generated (create narrative with detail field)
- All queries filter by character's BELIEVES edges

**Watch out for:**
- Don't create an event log — that defeats the pattern
- Conversation files need to be appendable and section-readable
- Timestamp comparison as strings might be tricky — may need parsing

**Open questions I had:**
- Where exactly should conversation files live?
- How to handle FalkorDB-specific Cypher syntax?
- Should conversation sections use specific markers for parsing?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created complete documentation for the History module — how the game stores and retrieves memories through distributed beliefs rather than a central log. Six files covering pattern, behaviors, algorithm, validation, and tests. Ready for implementation.

**Decisions made:**
- History is narratives + beliefs, not an event log (per design principles)
- Two paths: player-experienced uses conversation file references, world-generated uses detail field
- Timestamps as "Day N, time" strings

**Needs your input:**
- Confirm conversation file location (currently assuming conversations/{char_id}.md)
- Confirm this aligns with your vision for "they remembered" moments
- Any additional behaviors or edge cases to capture?

---

## TODO

### Immediate

- [ ] Implement query_history() with FalkorDB
- [ ] Implement record_player_history()
- [ ] Implement record_world_history()
- [ ] Create conversation file structure
- [ ] Write first tests against implementation

### Later

- [ ] Implement propagation algorithm
- [ ] Integrate with Chronicle view
- [ ] Performance testing with many narratives
- IDEA: Visual debug tool to see belief graph
- IDEA: "Memory inspector" dev tool

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident in the documentation. The pattern is clear and elegant — history as belief state rather than event log feels right for "they remembered" moments.

**Threads I was holding:**
- Connection to Chronicle view (needs its own docs)
- Connection to Narrator (needs to call query_history)
- Connection to Runner (needs to call record_world_history)
- Propagation could get complex — kept it simple for now

**Intuitions:**
- Conversation files might get large over long games — may need archiving
- The "heard" field on beliefs could enable interesting "telephone game" effects
- Chronicle could show confidence visually (faded text for rumors?)

**What I wish I'd known at the start:**
Nothing major — the system reminder provided good foundation. Would have been helpful to see existing conversation file examples.

---

## POINTERS

| What | Where |
|------|-------|
| Pattern philosophy | ./PATTERNS_History.md |
| Observable behaviors | ./BEHAVIORS_History.md |
| Query/record procedures | ./ALGORITHM_History.md |
| Test invariants | ./VALIDATION_History.md |
| Test cases | ./TEST_History.md |
| Vision docs | docs/design/ |
| Graph engine (planned) | docs/physics/graph/ |
| Chronicle view (planned) | docs/views/chronicle/ |

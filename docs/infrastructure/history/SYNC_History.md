# History — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Claude (repair agent)
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- Core pattern: distributed history through narratives + beliefs
- Two sources: player-experienced (conversation refs) vs world-generated (detail field)
- Timestamp format: "Day N, time_of_day"
- BELIEVES edge structure with confidence, source, when, where
- HistoryService class with query/record operations
- ConversationThread class for markdown conversation files
- Belief propagation to nearby characters

**What's still being designed:**
- Integration with Chronicle view
- Performance optimization for large narrative sets

**What's proposed (v2+):**
- Memory decay over time
- Confidence degradation with retellings
- Player journal entries as narratives
- "Actively trying to remember" mechanic

---

## CURRENT STATE

**Implementation complete.** The History module is fully functional.

### Code Structure

```
engine/infrastructure/history/
├── __init__.py          # Module exports, usage examples
├── service.py           # HistoryService class (~565 lines)
├── conversations.py     # ConversationThread class (~217 lines)
└── README.md            # Implementation documentation
```

### HistoryService (service.py)

**Query operations:**
- `query_history()` - Query what a character believes about the past
- `get_shared_history()` - Get narratives both characters believe
- `who_knows()` - Find all characters who know about an event

**Record operations:**
- `record_player_history()` - Record events from scenes (with conversation)
- `record_world_history()` - Record off-screen events (with detail field)
- `_propagate_beliefs()` - Spread news to nearby characters

**Helpers:**
- Timestamp parsing and comparison
- Narrative node creation with OCCURRED_AT links
- BELIEVES edge creation

### ConversationThread (conversations.py)

- `append_section()` - Add new conversation section to character's file
- `read_section()` - Read specific section by header
- `list_sections()` - List all sections in a file
- `get_full_thread()` - Get complete conversation history
- `search_sections()` - Search for keyword in sections

**File format:** Markdown with `## Day N, Time — Location` headers.

---

## IN PROGRESS

No active work.

---

## RECENT CHANGES

### 2025-12-19: ConversationThread Review

- **What:** Verified ConversationThread functions flagged by repair as incomplete already contain implementations
- **Why:** Repair task marked `__init__`, `_get_file_path`, `_get_relative_path` as empty, but code is implemented
- **Files:** `engine/infrastructure/history/conversations.py`

### 2025-12-19: Implementation Added

- **What:** Full HistoryService and ConversationThread implementation
- **Why:** Part of code restructure to match documentation areas
- **Commit:** `bd15ecf` - "refactor: Restructure code to match docs areas"
- **Files:**
  - engine/infrastructure/history/service.py
  - engine/infrastructure/history/conversations.py
  - engine/infrastructure/history/__init__.py
  - engine/infrastructure/history/README.md

### 2024-12-16: Initial Documentation

- **What:** Created docs/infrastructure/history/ with full PATTERN → TEST chain
- **Why:** History system is core to "they remembered" experience; needed documented before implementation
- **Files:** PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, TEST, SYNC docs

---

## KNOWN ISSUES

### No Tests Yet

- **Severity:** Medium
- **Symptom:** Implementation exists but no automated tests
- **Next step:** Write unit tests for HistoryService methods

### Integration Not Verified

- **Severity:** Medium
- **Symptom:** HistoryService not yet integrated with Narrator/World-Runner
- **Next step:** Connect to agent workflows

## CONFLICTS

### DECISION: ConversationThread Incomplete Impl
- Conflict: Repair task flagged `__init__`, `_get_file_path`, and `_get_relative_path` in `engine/infrastructure/history/conversations.py` as empty, but they already contain implementations.
- Resolution: Treat the issue as already resolved; no code changes made.
- Reasoning: The functions handle base directory creation and path formatting used by conversation operations.
- Updated: `docs/infrastructure/history/SYNC_History.md`

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Test_Write_Tests_And_Verify.md` or `VIEW_Extend_Add_Features_To_Existing.md`

**Where I stopped:** Implementation complete. Tests and integration pending.

**What you need to understand:**
- History is NOT a separate system — it's narratives + beliefs in the graph
- Two recording paths: player-experienced (append conversation, create narrative with source ref) vs world-generated (create narrative with detail field)
- All queries filter by character's BELIEVES edges

**Watch out for:**
- Conversation files need to be appendable and section-readable
- Timestamp comparison uses string parsing — validate edge cases

**Open questions:**
- How to integrate with Narrator (when to call record_player_history)?
- How to integrate with World-Runner (when to call record_world_history)?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
History module now has full implementation. HistoryService provides query_history, record_player_history, record_world_history. ConversationThread manages markdown files with conversation sections. Beliefs propagate to nearby characters.

**What's done:**
- All core query and record operations
- Conversation thread file management
- Belief propagation to nearby places

**What's needed:**
- Write tests
- Integrate with Narrator and World-Runner agents
- Test performance with many narratives

---

## TODO

### Immediate

- [ ] Write unit tests for HistoryService
- [ ] Write unit tests for ConversationThread
- [ ] Integrate with Narrator agent
- [ ] Integrate with World-Runner agent

### Later

- [ ] Performance testing with many narratives
- [ ] Integrate with Chronicle view
- IDEA: Visual debug tool to see belief graph
- IDEA: "Memory inspector" dev tool

---

## POINTERS

| What | Where |
|------|-------|
| Pattern philosophy | ./PATTERNS_History.md |
| Observable behaviors | ./BEHAVIORS_History.md |
| Query/record procedures | ./ALGORITHM_History.md |
| Test invariants | ./VALIDATION_History.md |
| Test cases | ./TEST_History.md |
| Implementation code | engine/infrastructure/history/ |
| Module registration | modules.yaml (history) |

## Agent Observations

### Remarks
- Repair task appears stale relative to `engine/infrastructure/history/conversations.py`.

### Suggestions
- None.

### Propositions
- None.

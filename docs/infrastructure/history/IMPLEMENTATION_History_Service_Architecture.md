# History — Implementation: Service and Conversation Architecture

```
STATUS: DRAFT
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_History.md
BEHAVIORS:      ./BEHAVIORS_History.md
ALGORITHM:      ./ALGORITHM_History.md
VALIDATION:     ./VALIDATION_History.md
THIS:           IMPLEMENTATION_History_Service_Architecture.md
TEST:           ./TEST_History.md
SYNC:           ./SYNC_History.md

IMPL:           engine/infrastructure/history/service.py
```

> Contract: Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/infrastructure/history/__init__.py           # Module exports and usage examples
engine/infrastructure/history/service.py            # HistoryService query/record workflows
engine/infrastructure/history/conversations.py      # ConversationThread file handling
engine/infrastructure/history/README.md             # Implementation overview and examples
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/infrastructure/history/service.py` | Query and record distributed history in the graph | `HistoryService`, `query_history`, `record_player_history`, `record_world_history` | ~563 | WATCH |
| `engine/infrastructure/history/conversations.py` | Append/read markdown conversation threads | `ConversationThread`, `append_section`, `read_section` | ~216 | OK |
| `engine/infrastructure/history/__init__.py` | Public exports and usage examples | module exports | ~44 | OK |
| `engine/infrastructure/history/README.md` | Narrative on module usage | docs | ~270 | OK |

Size thresholds:
- OK (<400 lines): healthy size
- WATCH (400-700 lines): consider extraction
- SPLIT (>700 lines): must split before adding more

---

## DESIGN PATTERNS

### Architecture Pattern

Pattern: Layered service + graph storage + file-backed conversations.

Why this pattern:
- Keeps behavior readable and centered in `HistoryService`.
- Delegates storage concerns to graph ops/queries and filesystem helper.
- Keeps conversation IO separate from graph logic.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Service object | `engine/infrastructure/history/service.py:HistoryService` | Single entry point for history workflows |
| Facade | `HistoryService` around graph ops/queries | Hides Cypher details from callers |
| Repository-style helper | `engine/infrastructure/history/conversations.py:ConversationThread` | Encapsulates file storage concerns |

### Anti-Patterns to Avoid

- God object: keep `HistoryService` focused on orchestration, not graph schema changes.
- Leaky storage details: callers should not depend on conversation file layout.
- Schema drift: narrative fields and BELIEVES attributes must stay consistent with docs.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| History service | Query/record logic, timestamp helpers | Graph persistence implementation | `HistoryService` public methods |
| Conversation storage | Markdown section IO | Narrative graph logic | `ConversationThread` methods |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `HistoryService method query_history` | `engine/infrastructure/history/service.py:54` | Narrator/history queries |
| `HistoryService method record_player_history` | `engine/infrastructure/history/service.py:208` | Scene completion |
| `HistoryService method record_world_history` | `engine/infrastructure/history/service.py:312` | World runner events |

---

## DATA FLOW

### Player-Experienced Recording

```
Scene outcome
  -> HistoryService record_player_history
    -> ConversationThread append_section
    -> HistoryService _create_narrative_node
    -> HistoryService _create_belief_edge for each witness
```

### World-Generated Recording

```
World event
  -> HistoryService record_world_history
    -> HistoryService _create_narrative_node
    -> HistoryService _create_belief_edge for witnesses
    -> HistoryService _propagate_beliefs (optional)
```

### Query Flow

```
Narrator query
  -> HistoryService query_history
    -> Graph query for BELIEVES + Narrative
    -> ConversationThread read_section when source reference exists
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/infrastructure/history/service.py
    -> engine/infrastructure/history/conversations.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `logging` | runtime logging | `engine/infrastructure/history/service.py`, `engine/infrastructure/history/conversations.py` |
| `uuid` | narrative id creation | `engine/infrastructure/history/service.py` |
| `datetime` | timestamp parsing support | `engine/infrastructure/history/service.py` |
| `pathlib` | file path management | `engine/infrastructure/history/conversations.py` |

---

## STATE MANAGEMENT

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Conversations base dir | `ConversationThread base_dir` | instance | set on init, reused |
| Narrative ids | `HistoryService record_* methods` | local | per call |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `conversations_dir` | `HistoryService init` | required | Base directory for conversation files |

---

## BIDIRECTIONAL LINKS

### Code -> Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/infrastructure/history/service.py` | 1 | `docs/infrastructure/history/IMPLEMENTATION_History_Service_Architecture.md` |

### Docs -> Code

| Doc Section | Implemented In |
|-------------|----------------|
| query flow | `engine/infrastructure/history/service.py:query_history` |
| player recording | `engine/infrastructure/history/service.py:record_player_history` |
| world recording | `engine/infrastructure/history/service.py:record_world_history` |
| conversation IO | `engine/infrastructure/history/conversations.py:ConversationThread` |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

| File | Current | Target | Extract To | What to Move |
|------|---------|--------|------------|--------------|
| `engine/infrastructure/history/service.py` | ~563L | <400L | history queries module (planned) | `query_history`, `get_shared_history`, `who_knows` |
| `engine/infrastructure/history/service.py` | ~563L | <400L | history recording module (planned) | `record_*` and `_propagate_beliefs` helpers |

### Missing Implementation

- None noted in current scope.

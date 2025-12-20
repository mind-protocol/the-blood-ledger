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
ALGORITHM:      ./ALGORITHM/ALGORITHM_Overview.md
VALIDATION:     ./VALIDATION_History.md
THIS:           IMPLEMENTATION_History_Service_Architecture.md
TEST:           ./TEST/TEST_Overview.md
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

## SCHEMA

### Narrative Node Fields (Graph)

| Field | Type | Owner | Notes |
|-------|------|-------|-------|
| `id` | `str` | Narrative | `narr_{uuid8}` identifier used for BELIEVES edges |
| `name` | `str` | Narrative | Short name from content prefix (`content[:50]`) |
| `content` | `str` | Narrative | Summary of the event or memory |
| `narrative_type` | `str` | Narrative | Defaults to `"memory"` unless overridden |
| `occurred_at` | `str` | Narrative | `"Day N, time"` string used for ordering |
| `occurred_where` | `str` | Narrative | Place ID used to link `OCCURRED_AT` |
| `source_file` | `str` | Narrative | Relative path like `conversations/aldric.md` |
| `source_section` | `str` | Narrative | Section header for conversation lookup |
| `detail` | `str` | Narrative | World-generated detail text (no convo) |
| `about_characters` | `list[str]` | Narrative | Character IDs referenced by the memory |
| `about_places` | `list[str]` | Narrative | Place IDs referenced by the memory |
| `weight` | `float` | Narrative | Initial salience for later surfacing |

### BELIEVES Edge Fields (Graph)

| Field | Type | Owner | Notes |
|-------|------|-------|-------|
| `believes` | `float` | BELIEVES | Confidence score (0.0-1.0) |
| `heard` | `float` | BELIEVES | Strength of hearing/awareness |
| `source` | `str` | BELIEVES | `participated`, `witnessed`, or `rumor` |
| `when` | `str` | BELIEVES | Timestamp string aligned to narrative |
| `where` | `str` | BELIEVES | Place ID where knowledge was gained |
| `from_whom` | `str` | BELIEVES | Optional, not yet populated in service |

### Conversation Thread Format (Filesystem)

Conversation files are Markdown with `#` title and `##` section headers:
`## Day N, Time — Location`. Narratives store `source_file` and
`source_section` to load the exact dialogue block later. These files are
per-playthrough artifacts and are not stored inside the graph.

---

## LOGIC CHAINS

### Query History

```
query_history(character_id, filters)
  -> build Cypher with BELIEVES constraints
  -> graph._query(...) returns narrative rows
  -> filter by timestamp helpers (if provided)
  -> if source_file/section present: read_section(...)
  -> return enriched narrative list
```

### Record Player History

```
record_player_history(content, conversation_text, ...)
  -> parse timestamp into day/time
  -> append_section(...) writes conversation file
  -> _create_narrative_node(...) with source_file/section
  -> _create_belief_edge(...) for each witness
  -> return narrative_id + belief ids
```

### Record World History

```
record_world_history(content, detail, ...)
  -> _create_narrative_node(...) with detail field
  -> _create_belief_edge(...) for direct witnesses
  -> optional _propagate_beliefs(...) for nearby chars
  -> return narrative_id + belief ids
```

These chains describe the current orchestration order; GraphOps (ngram repo graph runtime) is responsible
for transaction boundaries and persistence guarantees during writes.

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

## RUNTIME BEHAVIOR

### Initialization

```
1. HistoryService is constructed with graph_queries, graph_ops, conversations_dir
2. ConversationThread ensures base directory exists on init
3. Service is ready for query/record calls immediately
```

### Query Path

```
1. Cypher query executes against graph
2. Results filtered by optional time range
3. ConversationThread reads sections when source reference exists
4. Caller receives narratives with optional conversation text
```

### Record Path

```
1. Conversation section appended (player history only)
2. Narrative node created; OCCURRED_AT link added when place ID exists
3. BELIEVES edges created for witnesses (and propagated if enabled)
4. IDs returned to caller for downstream tracking
```

Logging occurs on missing conversation files or sections to aid debugging,
but queries still return narrative metadata when dialogue is unavailable.

---

## CONCURRENCY MODEL

The service does not implement explicit locking. Calls are expected to be
serialized by the caller or by the process model of the runtime. Conversation
sections are appended to Markdown files using standard file append semantics;
concurrent writes could interleave, so high-concurrency usage should add a
queue or per-thread file lock in the caller if needed. Graph writes execute
via the provided GraphOps/GraphQueries objects (ngram repo graph runtime) and assume the database
connection handles transaction isolation.
Reads can race with writes and may return partial sections if callers do not
serialize per-playthrough history recording.

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

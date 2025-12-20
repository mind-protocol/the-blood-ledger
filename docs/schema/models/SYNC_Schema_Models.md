# Schema Models — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Pydantic models for nodes, links, and tensions in `engine/models/`.
- Enum taxonomy for schema fields in `engine/models/base.py`.

**What's still being designed:**
- Cross-model validation rules beyond field-level checks.

**What's proposed (v2+):**
- Dedicated schema validation suite that enforces graph-level invariants.

---

## CURRENT STATE

The engine exposes a unified set of Pydantic models for graph nodes, links, and
tensions, along with shared enums and helper methods. The module is structured
by responsibility (base enums, nodes, links, tensions) and re-exported from
`engine/models/__init__.py` for stable imports. Tests live in
`engine/tests/test_models.py` with some integration coverage in scenario tests.
Updated the patterns doc to include the missing INSPIRATIONS and SCOPE
sections and expanded the non-goals to meet template length guidance.

---

## IN PROGRESS

Doc-template repair for this SYNC file, focused on filling missing sections so
schema-model documentation stays aligned while avoiding behavioral changes.
Once complete, keep the schema-model doc chain synced with future field edits.

---

## KNOWN ISSUES

The schema-models doc chain does not yet link `docs/schema/SCHEMA.md`, so schema
context is split across modules and can drift without explicit cross-links.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Added docs + mapping; no code changes beyond DOCS reference.

**What you need to understand:**
Schema models are the canonical Pydantic types for nodes/links/tensions. Keep
`engine/models/__init__.py` as the public entry point and update docs if fields
change.

**Watch out for:**
Some schema behavior is documented in `docs/schema/SCHEMA.md` but not yet linked
into a full doc chain for this module.

---

## HANDOFF: FOR HUMAN

This update only fills missing SYNC sections to satisfy the doc template; no
behavior changes were made to schema models or tests.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL->DOCS: If model fields change, update `docs/schema/models/`.

### Tests to Run

```bash
pytest engine/tests/test_models.py
```

## CONSCIOUSNESS TRACE

Attention stayed on template completeness rather than schema changes; the main
concern is avoiding doc drift while keeping updates minimal and traceable.

---

## POINTERS

- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md`
- `engine/models/__init__.py`
- `engine/tests/test_models.py`


---

## ARCHIVE

Older content archived to: `SYNC_Schema_Models_archive_2025-12.md`

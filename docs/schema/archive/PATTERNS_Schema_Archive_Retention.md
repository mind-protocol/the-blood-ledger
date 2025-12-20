# Schema Archive — Patterns: Retention and Scope

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## PURPOSE

The schema archive exists to retain historical schema decisions without
polluting the canonical schema references. It preserves prior content for
traceability while keeping the active schema concise and navigable.

---

## DESIGN DECISIONS

- **Archive, don't delete:** Preserve prior schema detail in an archive to
  avoid losing context during schema refactors.
- **Canonical stays small:** The canonical schema lives in
  `docs/schema/SCHEMA/` and `docs/schema/SCHEMA_Moments/`.
- **Narrative over duplication:** Archive notes explain what changed rather
  than duplicating full schema content.

---

## SCOPE

**In scope:**
- Notes describing what was removed from canonical schema docs.
- Pointers to canonical schema locations.

**Out of scope:**
- Active schema definitions (live in `docs/schema/SCHEMA/`).
- Runtime code or validation rules.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Schema_Archive_Retention.md
BEHAVIORS:       ./BEHAVIORS_Schema_Archive_Notes.md
ALGORITHM:       ./ALGORITHM_Schema_Archive_Process.md
VALIDATION:      ./VALIDATION_Schema_Archive_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Schema_Archive_Notes.md
HEALTH:          ./HEALTH_Schema_Archive_Verification.md
SYNC:            ./SYNC_archive_2024-12.md
```

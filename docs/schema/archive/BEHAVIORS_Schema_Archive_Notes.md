# Schema Archive — Behaviors: Archival Notes

```
STATUS: STABLE
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Schema_Archive_Retention.md
THIS:            BEHAVIORS_Schema_Archive_Notes.md
ALGORITHM:       ./ALGORITHM_Schema_Archive_Process.md
VALIDATION:      ./VALIDATION_Schema_Archive_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Schema_Archive_Notes.md
HEALTH:          ./HEALTH_Schema_Archive_Verification.md
SYNC:            ./SYNC_archive_2024-12.md
```

---

## BEHAVIORS

### B1: Archive Summary Preserved

```
GIVEN:  Schema refactor moves verbose content out of canonical docs
WHEN:   Archive note is updated
THEN:   Summary explains what moved and where the canonical schema lives
```

### B2: No Canonical Duplication

```
GIVEN:  Canonical schema changes
WHEN:   Archive note is updated
THEN:   Archive does not re-copy full node/link schemas
```

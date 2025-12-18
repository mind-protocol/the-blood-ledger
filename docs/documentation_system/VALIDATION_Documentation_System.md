# Documentation System — Validation: How We Verify

```
STATUS: STABLE
CREATED: 2024-12-17
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Documentation_System.md
BEHAVIORS:   ./BEHAVIORS_Documentation_System.md
ALGORITHM:   ./ALGORITHM_Documentation_System.md
THIS:        VALIDATION_Documentation_System.md (you are here)
```

---

## Invariants

1. **Presence** — Each module folder contains PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, TEST, SYNC (or an explicit note explaining why a layer is deferred).
2. **Naming** — Filenames follow `TYPE_Context.md` pattern with descriptive suffix.
3. **CHAIN Integrity** — Every CHAIN block references files that exist locally.
4. **Implementation Links** — Implementation/test paths listed in CHAIN resolve to real files.
5. **SYNC Updates** — After any change, SYNC timestamp + notes reflect the latest work.

---

## Validation Routines

### Scripted
- `context-protocol validate`
  - Checks presence + naming
  - Reports broken CHAIN links
  - Flags modules lacking PATTERNS/SYNC

### Manual Spot-Checks
- Pick a module at random, follow CHAIN completely — verify no dead ends.
- Confirm SYNC last-updated date matches most recent work session.
- Ensure templates include status headers and metadata blocks.

---

## Escalation

If invariants fail:
1. Record the issue in the module's SYNC file.
2. Prioritize remediation before new feature work.
3. If systemic (e.g., many modules missing docs), schedule a documentation sprint.

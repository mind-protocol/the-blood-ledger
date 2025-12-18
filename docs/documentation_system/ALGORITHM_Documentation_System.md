# Documentation System — Algorithm: Maintaining the Chain

```
STATUS: STABLE
CREATED: 2024-12-17
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Documentation_System.md
BEHAVIORS:   ./BEHAVIORS_Documentation_System.md
THIS:        ALGORITHM_Documentation_System.md (you are here)
VALIDATION:  ./VALIDATION_Documentation_System.md
```

---

## Procedure: Creating a Module Chain

1. **Identify module boundary**
   - Confirm code + docs live under a dedicated folder
   - Determine module owner + scope
2. **Instantiate docs**
   - Copy templates for PATTERNS/BEHAVIORS/ALGORITHM/VALIDATION/TEST/SYNC
   - Rename files using `PATTERNS_{Insight}.md` etc
3. **Link CHAIN**
   - In each file, update the CHAIN block with relative references
   - Include implementation + test entry points if known
4. **Document reasoning**
   - PATTERNS: describe philosophy and tradeoffs
   - BEHAVIORS: capture GIVEN/WHEN/THEN expectations
   - ALGORITHM: detail procedures, pseudocode, and data flows
   - VALIDATION: outline invariants + checks
   - TEST: list coverage + test files
5. **Update SYNC**
   - Record current status, open questions, and next steps
6. **Validate**
   - Run `context-protocol validate`
   - Fix reported issues before shipping work

---

## Procedure: Updating Docs After Code Changes

1. Read relevant PATTERNS + SYNC to refresh context
2. Make code changes
3. Update ALGORITHM/BEHAVIORS if the logic or observable behavior shifts
4. Capture new invariants/tests in VALIDATION + TEST docs
5. Write SYNC notes summarizing what changed and handoffs
6. Rerun validation

---

## Tooling Hooks

- `context-protocol new module --name <module>` can scaffold files (future work)
- `context-protocol validate` enforces naming + presence
- Editors can map shortcuts to open CHAIN sequences
```

# Storm Loader — Patterns: Declarative Diff Application

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md
```

---

## CHAIN

```
THIS:            PATTERNS_Storm_Loader_As_Diff.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Storm_Loader_Mutations.md
MECHANISMS:      ./MECHANISMS_Storm_Loader_Pipeline.md
VERIFICATION:    ./VALIDATION_Storm_Loader_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storm_Loader.md
TEST:            ./TEST_Storm_Loader.md
SYNC:            ./SYNC_Storm_Loader.md

IMPL:            data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md
```

### Bidirectional Contract

**Before modifying this doc or the system design:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_Storm_Loader.md: "Docs updated, implementation needs: {what}"
3. Run tests: `N/A (design-only)`

**After modifying the system design or implementation:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_Storm_Loader.md: "Implementation changed, docs need: {what}"
3. Run tests: `N/A (design-only)`

---

## THE PROBLEM

Storms are designed as lightweight overlays, but applying them requires a deterministic, validated mutation pipeline. Without a dedicated loader, overlays risk corruption, partial application, or silent failures.

---

## THE PATTERN

**Declarative overlay loader.** Apply storm directives sequentially as atomic graph mutations with validation and graceful failure. Treat the loader as a diff application engine that never owns topology.

Current source content embedded here:
- Four-layer world instantiation.
- Stepwise application: tensions → facts → secrets → energy.
- Validation rules for missing nodes and schema conformance.

---

## PRINCIPLES

### Principle 1: Idempotent application
Applying the same storm twice yields the same world state.

### Principle 2: Validation before mutation
Missing nodes must be detected before applying changes.

### Principle 3: Graceful failure
Invalid directives log warnings and do not halt the load.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| docs/infrastructure/storms | Defines the storm schema and semantics |
| docs/network/world-scavenger | Provides base world graph |
| docs/physics | Consumes energy floods during tick |

---

## INSPIRATIONS

- Storm Loader implementation spec
- Diff-based config application patterns

---

## SCOPE

### In Scope

- Storm schema validation
- Graph mutation sequence (facts/tensions/secrets/energy)
- Warning/logging on missing nodes

### Out of Scope

- Storm authoring tools (Storms)
- Energy propagation (Physics)
- Content generation (Scavenger)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define logging format and severity levels
- [ ] Define storm schema validator source of truth
- IDEA: Add dry-run mode to report applied mutations
- QUESTION: Should storm application be transactional or best-effort?

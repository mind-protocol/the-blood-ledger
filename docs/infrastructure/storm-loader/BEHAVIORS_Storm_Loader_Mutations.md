# Storm Loader — Behaviors: Mutation Application

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storm_Loader_As_Diff.md
THIS:            BEHAVIORS_Storm_Loader_Mutations.md (you are here)
MECHANISMS:      ./MECHANISMS_Storm_Loader_Pipeline.md
VERIFICATION:    ./VALIDATION_Storm_Loader_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storm_Loader.md
TEST:            ./TEST_Storm_Loader.md
SYNC:            ./SYNC_Storm_Loader.md

IMPL:            data/Distributed-Content-Generation-Network/IMPLEMENTATION_Storm_Loader.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Apply facts and tensions first

```
GIVEN:  a validated storm overlay
WHEN:   the loader runs
THEN:   facts and tensions are applied before secrets and energy
```

### B2: Missing nodes are skipped

```
GIVEN:  a storm directive references a missing node
WHEN:   applying the directive
THEN:   the loader logs a warning and continues
```

### B3: Energy floods modify potential energy

```
GIVEN:  a storm with energy floods/drains
WHEN:   applied
THEN:   target nodes receive potential_energy deltas
```

---

## INPUTS / OUTPUTS

### Primary Function: `load_storm()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| storm_file | object | Parsed storm YAML |
| world_graph | object | Base graph |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| world_graph | object | Mutated graph |

**Side Effects:**

- Logs warnings for invalid directives

---

## EDGE CASES

### E1: Schema missing overlay

```
GIVEN:  storm without overlay key
THEN:   loader rejects the storm
```

### E2: Duplicate directives

```
GIVEN:  multiple directives targeting same node
THEN:   last directive wins
```

---

## ANTI-BEHAVIORS

### A1: Loader creates topology

```
GIVEN:   storm application
WHEN:    loader runs
MUST NOT: create new map or NPC topology
INSTEAD: rely on Scavenger base
```

### A2: Loader halts on missing node

```
GIVEN:   missing node reference
WHEN:    applying directive
MUST NOT: abort entire storm
INSTEAD: log warning and continue
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define mutation ordering for secrets vs memories
- [ ] Define warning levels (info vs error)
- IDEA: Add per-storm checksum for debugging

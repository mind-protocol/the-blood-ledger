# Storms — Behaviors: Overlay Effects

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storms_As_Crisis_Overlays.md
THIS:            BEHAVIORS_Storm_Overlay_Behavior.md (you are here)
MECHANISMS:      ./MECHANISMS_Storm_Application.md
VERIFICATION:    ./VALIDATION_Storm_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storms.md
TEST:            ./TEST_Storms.md
SYNC:            ./SYNC_Storms.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Storm overlays mutate tensions and facts

```
GIVEN:  a base world from the Scavenger
WHEN:   a storm is applied
THEN:   tensions and facts are overwritten as specified
```

### B2: Energy floods make factions present

```
GIVEN:  a storm with energy floods
WHEN:   the storm applies
THEN:   targeted factions dominate narrative context
```

### B3: Weekly storms standardize challenge

```
GIVEN:  a weekly storm identifier
WHEN:   multiple players start the storm
THEN:   all receive the same crisis overlay
```

---

## INPUTS / OUTPUTS

### Primary Function: `apply_storm()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| storm | object | Storm overlay data |
| world_graph | object | Base world graph |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| world_graph | object | Mutated graph |

**Side Effects:**

- Sets tensions
- Mutates fact nodes
- Adds secrets and goals
- Injects energy floods/drains

---

## EDGE CASES

### E1: Storm references missing nodes

```
GIVEN:  storm references a node not in the base world
THEN:   mutation logs a warning and continues
```

### E2: Overlapping storms

```
GIVEN:  multiple storms applied sequentially
THEN:   last-applied storm wins for conflicting fields
```

---

## ANTI-BEHAVIORS

### A1: Storm carries topology

```
GIVEN:   storm data payload
WHEN:    applied
MUST NOT: contain full map/NPC topology
INSTEAD: only contain diffs (tensions, facts, secrets)
```

### A2: Energy floods bypass physics

```
GIVEN:   energy floods applied
WHEN:    simulation runs
MUST NOT: skip physics propagation
INSTEAD: allow tick.py to propagate normally
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define order-of-operations for multiple overlays
- [ ] Define storm conflict resolution policy
- IDEA: Allow "storm stacking" with explicit priorities

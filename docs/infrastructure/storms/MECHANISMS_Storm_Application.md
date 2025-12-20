# Storms — Mechanisms: Crisis Injection

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storms_As_Crisis_Overlays.md
BEHAVIORS:       ./BEHAVIORS_Storm_Overlay_Behavior.md
THIS:            MECHANISMS_Storm_Application.md (you are here)
VERIFICATION:    ./VALIDATION_Storm_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storms.md
TEST:            ./TEST_Storms.md
SYNC:            ./SYNC_Storms.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — Storms.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Storm application mutates a base world graph by setting tensions, facts, secrets, memories, and energy floods/drains. The storm is a declarative overlay applied after Scavenger and Bleed-Through layers.

---

## DATA STRUCTURES

### StormOverlay

```
tensions: list
facts: list
secrets: list
memories: list
energy_floods: list
energy_drains: list
goal: object
```

---

## MECHANISM: Apply Storm

### Step 1: Validate storm schema

Ensure required keys exist and referenced nodes can be resolved.

### Step 2: Set tensions

Overwrite tension values for listed tensions.

### Step 3: Apply facts and secrets

Mutate node states and attach hidden beliefs.

### Step 4: Inject energy floods/drains

Modify potential energy for targets; let physics propagate.

### Step 5: Set goal + chronicle hooks

Register success/failure conditions and hooks.

---

## KEY DECISIONS

### D1: Missing node handling

```
IF node is missing:
    log warning and continue
```

### D2: Energy propagation

```
Energy floods are applied as potential_energy deltas;
physics handles propagation and decay.
```

---

## DATA FLOW

```
Storm overlay
    ↓
Validation
    ↓
Graph mutations (tensions/facts/secrets)
    ↓
Energy floods/drains
    ↓
Tick simulation
```

---

## COMPLEXITY

**Time:** O(n) where n = number of storm directives.

**Space:** O(1) additional beyond graph mutations.

**Bottlenecks:**
- Node lookup per directive

---

## HELPER FUNCTIONS

### `apply_fact()`

**Purpose:** Mutate a node state per storm overlay.

**Logic:** Update state fields and attach death metadata if present.

### `apply_energy_flood()`

**Purpose:** Add energy to a target.

**Logic:** Increment potential_energy and allow tick to propagate.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/world-scavenger | get_default_world | Base topology |
| docs/physics | tick | Energy propagation |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define storm schema validation rules in code
- [ ] Define hook registration for chronicle hooks
- IDEA: Build pre-flight "storm lint" CLI

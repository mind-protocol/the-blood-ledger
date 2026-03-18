# {Module Name} — Validation: Invariants and Verification

```
@ngram:id: VALIDATION.{AREA}.{MODULE}
STATUS: DRAFT | DESIGNING | CANONICAL
CREATED: {DATE}
```

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_{name}.md
PATTERNS:        ./PATTERNS_*.md
BEHAVIORS:       ./BEHAVIORS_*.md
ALGORITHM:       ./ALGORITHM_*.md
THIS:            VALIDATION_*.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_{name}.md
HEALTH:          ./HEALTH_{name}.md
SYNC:            ./SYNC_{name}.md
```

---

## TESTS VS HEALTH

**Tests gate completion. Health monitors runtime.**

| Concern | Tests (CI) | Health (Runtime) |
|---------|------------|------------------|
| When | Build time | Production |
| Data | Fixtures | Real graph |
| Catches | Code bugs | Emergent drift |
| Blocks | Merge/deploy | Alerts/pages |

### Write Tests For

| Category | Why |
|----------|-----|
| Formula correctness | Deterministic input → output |
| State transitions | Finite, enumerable |
| Bounds checking | Known edge cases |
| Ordering invariants | Sequence matters |

### Use Health Only For

| Category | Why |
|----------|-----|
| Drift over time | Needs 1000+ real ticks |
| Ratio health | Emergent behavior |
| Graph-wide state | Needs real structure |

---

## INVARIANTS

### @ngram:id: V-{MODULE}-{NAME}
**{One-line description}**

```yaml
invariant: V-{MODULE}-{NAME}
priority: HIGH | MED | LOW
criteria: |
  {What must hold, formally or semi-formally}
verified_by:
  test: tests/{area}/test_{module}.py::test_{name}
  health: {area}/health/{module}.py::check_{name}
  confidence: high | partial | needs-health | untested
evidence:
  - {How violation would be detected}
failure_mode: |
  {What breaks if this invariant fails}
```

### @ngram:id: V-{MODULE}-{NAME-2}
**{One-line description}**

```yaml
invariant: V-{MODULE}-{NAME-2}
priority: HIGH | MED | LOW
criteria: |
  {What must hold}
verified_by:
  test: {test path if applicable}
  health: {health path if applicable}
  confidence: untested
evidence:
  - {Detection method}
failure_mode: |
  {Consequence of failure}
```

---

## CONFIDENCE LEVELS

| Level | Meaning | Action |
|-------|---------|--------|
| `high` | Test + health cover completely | None |
| `partial` | Test exists but edge cases remain | Track gaps |
| `needs-health` | Runtime behavior matters more than test | Write health check |
| `untested` | Gap, tracked for completion | Write test or justify needs-health |

---

## PRIORITY LEVELS

| Priority | Meaning | Requirement |
|----------|---------|-------------|
| `HIGH` | System breaks without this | MUST have verified_by.test or verified_by.health |
| `MED` | Degraded behavior | SHOULD have test |
| `LOW` | Nice to have | MAY defer |

---

## VALIDATION ID INDEX

| ID | Category | Priority | Confidence |
|----|----------|----------|------------|
| V-{MODULE}-{NAME} | {category} | HIGH | high |
| V-{MODULE}-{NAME-2} | {category} | MED | untested |

---

## MARKERS

<!-- @ngram:todo {Missing test for invariant V-*} -->
<!-- @ngram:escalation {Test blocked by infrastructure} -->
<!-- @ngram:proposition {Additional invariant to add} -->

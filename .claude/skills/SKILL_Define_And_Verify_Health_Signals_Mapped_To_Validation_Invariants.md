# Skill: `ngram.health_define_and_verify`
@ngram:id: SKILL.HEALTH.DEFINE_VERIFY.MAP_TO_VALIDATION

## Maps to VIEW
`.ngram/views/VIEW_Health_Define_Health_Checks_And_Verify.md`

## Purpose
Define/extend health signals and verify via the real-time health sublayer; map indicators to VALIDATION invariants and declared docking points.

## Inputs (YAML)
```yaml
module: "<area/module>"
invariants: ["<VALIDATION @ngram:id anchors>"]
```

## Outputs (YAML)
```yaml
health_signals:
  - id: "<signal>"
    maps_to_invariant: "<VALIDATION id>"
    docking_point: "<file:symbol>"
verification_results:
  - signal: "<signal>"
    status: "<pass|warn|fail>"
    evidence: "<health stream / command>"
```

## Gates (non-negotiable)
- Health indicators must map to VALIDATION (prefer `@ngram:id` anchors).
- Docking points must be declared in IMPLEMENTATION.
- Verification is required before marking the module “done”.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

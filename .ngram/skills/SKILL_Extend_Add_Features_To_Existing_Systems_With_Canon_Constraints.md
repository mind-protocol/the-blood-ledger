# Skill: `ngram.extend_add_features`
@ngram:id: SKILL.EXTEND.ADD_FEATURES.CANON_CONSTRAINTS

## Maps to VIEW
`.ngram/views/VIEW_Extend_Add_Features_To_Existing.md`

## Purpose
Extend existing systems with new features while enforcing canon constraints and avoiding default-repo regressions.

## Inputs (YAML)
```yaml
module: "<area/module>"
feature: "<feature description>"
```

## Outputs (YAML)
```yaml
code_changes: ["<files modified/added>"]
doc_updates: ["<docs updated>"]
markers:
  escalations: ["<@ngram:escalation>"]
  propositions: ["<@ngram:proposition>"]
```

## Gates (non-negotiable)
- Must align with PATTERNS scope and VALIDATION invariants.
- Must update HEALTH expectations when behavior surface changes.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

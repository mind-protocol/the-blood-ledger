# Skill: `ngram.onboard_understand_module_codebase`
@ngram:id: SKILL.ONBOARD.UNDERSTAND_EXISTING_CODEBASE.CONFIRM_CANON

## Maps to VIEW
`.ngram/views/VIEW_Onboard_Understand_Existing_Codebase.md`

## Purpose
Identify canonical paths/symbols/dataflow and confirm naming/comment/monitoring expectations for the module.

## Inputs (YAML)
```yaml
module: "<area/module>"
code_roots: ["<paths>"]
```

## Outputs (YAML)
```yaml
canonical_surfaces:
  - file: "<path>"
    symbols: ["<function/class>"]
dataflow_notes: ["<key flows>"]
naming_terms: ["<canon terms>"]
```

## Gates (non-negotiable)
- If canonical surface is unclear, log `@ngram:escalation` and proceed with other modules/tasks.
- Must update IMPLEMENTATION_* with discovered surfaces/docking points.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

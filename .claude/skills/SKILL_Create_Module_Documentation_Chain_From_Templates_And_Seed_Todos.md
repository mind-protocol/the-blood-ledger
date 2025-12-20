# Skill: `ngram.create_module_documentation`
@ngram:id: SKILL.DOCS.CREATE_CHAIN_FROM_TEMPLATES.SEED_TODOS

## Maps to VIEW
`.ngram/views/VIEW_Document_Create_Module_Documentation.md`

## Purpose
Create module doc directory and copy templates into the full chain; add TODO plans and establish doc↔code pointers.

## Inputs (YAML)
```yaml
module: "<area/module>"
templates_root: "<path to templates>"
```

## Outputs (YAML)
```yaml
created_files:
  - "docs/<area>/<module>/PATTERNS_*.md"
  - "docs/<area>/<module>/BEHAVIORS_*.md"
  - "docs/<area>/<module>/ALGORITHM_*.md"
  - "docs/<area>/<module>/VALIDATION_*.md"
  - "docs/<area>/<module>/IMPLEMENTATION_*.md"
  - "docs/<area>/<module>/HEALTH_*.md"
  - "docs/<area>/<module>/SYNC_*.md"
todos_added:
  - file: "<doc path>"
    todo: "<@ngram:TODO text>"
```

## Gates (non-negotiable)
- Must use templates verbatim as the base (no partial stubs).
- Must add at least one `@ngram:TODO` per module with a plan.
- Must establish bidirectional pointers (docs → code surfaces, code → doc chain path).

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

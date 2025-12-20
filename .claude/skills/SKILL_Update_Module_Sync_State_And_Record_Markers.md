# Skill: `ngram.sync_update_module_state`
@ngram:id: SKILL.SYNC.UPDATE_STATE.RECORD_MARKERS

## Maps to VIEW
`(SYNC always rule; called after each module/task)`

## Purpose
Update SYNC_*.md to record present state: what changed, what verified, what’s next, and all markers placed.

## Inputs (YAML)
```yaml
module: "<area/module>"
completed: ["<items>"]
verification: ["<health/test results>"]
markers:
  todos: ["<@ngram:TODO>"]
  escalations: ["<@ngram:escalation>"]
  propositions: ["<@ngram:proposition>"]
```

## Outputs (YAML)
```yaml
sync_updated: "docs/<area>/<module>/SYNC_*.md"
```

## Gates (non-negotiable)
- Must be called after each module/task.
- Must capture verification evidence and next actions deterministically.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

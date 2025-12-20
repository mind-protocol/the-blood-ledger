# Skill: `ngram.orchestrate_feature_integration`
@ngram:id: SKILL.ORCH.FEATURE_INTEGRATION.PIPELINE.ORCHESTRATOR

## Maps to VIEW
`(wrapper skill; calls the sequence below)`

## Purpose
Run the full pipeline: ingest → per-module loop → close-out, enforcing never-stop work conservation and deterministic routing.

## Inputs (YAML)
```yaml
objective: "<goal + acceptance criteria>"
data_sources:
  - "<path-or-url>"
scope_hints:
  areas: ["<optional>"]
  modules: ["<optional>"]
constraints:
  do_not_touch: ["<paths/surfaces>"]
  patterns: ["<canon patterns to respect>"]
```

## Outputs (YAML)
```yaml
task_graph:
  - module: "<area/module>"
    todos: ["<todo-id>"]
    chosen_view: "<implement|extend|debug>"
    verification_plan: ["<health-check>"]
progress_log:
  - module: "<area/module>"
    status: "<scaffolded|documented|implemented|verified>"
```

## Gates (non-negotiable)
- Must load PROTOCOL and required VIEWS referenced by downstream skills.
- Must create at least one `@ngram:TODO` per module/task discovered.
- Must enforce pipeline order and never-stop work conservation.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

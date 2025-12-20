# Skill: `ngram.ingest_raw_data_sources`
@ngram:id: SKILL.INGEST.RAW_DATA.ROUTE_TO_MODULES

## Maps to VIEW
`.ngram/views/VIEW_Ingest_Process_Raw_Data_Sources.md`

## Purpose
Parse and route raw inputs into areas/modules/tasks; produce deterministic mapping and seed TODOs.

## Inputs (YAML)
```yaml
data_sources:
  - "<path-or-url>"
scope_hints:
  areas: ["<optional>"]
  modules: ["<optional>"]
```

## Outputs (YAML)
```yaml
routing_table:
  - data_item: "<name>"
    target_area: "<area>"
    target_module: "<module>"
    doc_chain_targets: ["PATTERNS", "BEHAVIORS", "ALGORITHM", "VALIDATION", "IMPLEMENTATION", "HEALTH", "SYNC"]
    implementation_surfaces: ["<optional file:symbol>"]
seeded_todos:
  - module: "<area/module>"
    todo: "<@ngram:TODO text>"
```

## Gates (non-negotiable)
- No code/doc edits until a routing table exists.
- If routing is ambiguous, log `@ngram:escalation` and route everything else first.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

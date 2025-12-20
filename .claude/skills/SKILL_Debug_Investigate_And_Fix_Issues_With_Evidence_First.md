# Skill: `ngram.debug_investigate_fix_issues`
@ngram:id: SKILL.DEBUG.INVESTIGATE_FIX.EVIDENCE_FIRST

## Maps to VIEW
`.ngram/views/VIEW_Debug_Investigate_And_Fix_Issues.md`

## Purpose
Investigate and fix issues with evidence-first workflow; update docs and health signals to prevent recurrence.

## Inputs (YAML)
```yaml
module: "<area/module>"
symptom: "<error/log/behavior>"
```

## Outputs (YAML)
```yaml
diagnosis: ["<hypotheses + evidence refs>"]
fix: ["<files changed>"]
doc_updates: ["<docs updated>"]
verification: ["<health/test results>"]
```

## Gates (non-negotiable)
- Must cite evidence (health stream / logs / code) for each major claim.
- Must add regression prevention (tests/health) where canon expects.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

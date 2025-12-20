# Skill: `ngram.review_evaluate_changes`
@ngram:id: SKILL.REVIEW.EVALUATE.PRODUCE_AUDITABLE_REPORT

## Maps to VIEW
`.ngram/views/VIEW_Review_Evaluate_Changes.md`

## Purpose
Produce a review-ready report with stable references and explicit remaining gaps.

## Inputs (YAML)
```yaml
module: "<area/module>"
changes: ["<files changed>"]
```

## Outputs (YAML)
```yaml
report:
  evidence:
    docs: ["<@ngram:id + file + header path>"]
    code: ["<file + symbol>"]
  summary: ["<what changed>"]
  verification: ["<what was verified>"]
  remaining_gaps: ["<open TODOs/escalations>"]
```

## Gates (non-negotiable)
- Must include stable references for non-trivial claims.
- Must list remaining TODOs and escalations/propositions explicitly.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.

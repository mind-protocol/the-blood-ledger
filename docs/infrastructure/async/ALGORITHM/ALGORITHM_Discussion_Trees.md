# Async Architecture - Algorithm: Discussion Trees

**Purpose:** Summary of discussion tree lifecycle and usage rules.

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Async_Architecture.md
BEHAVIORS:      ../BEHAVIORS_Travel_Experience.md
VALIDATION:     ../VALIDATION_Async_Architecture.md
IMPLEMENTATION: ../IMPLEMENTATION_Async_Architecture.md
OVERVIEW:       ALGORITHM_Overview.md
THIS:           ALGORITHM_Discussion_Trees.md (you are here)
SYNC:           ../SYNC_Async_Architecture.md
```

---

## Principle

Each companion has discussion trees: pre-generated topics with branching prompts.
Trees are generated in the background, consumed on use, and regenerated when low.

## Lifecycle Summary

- **Generate:** On companion creation or when branches < 5; background subagent job.
- **Store:** `playthroughs/default/discussion_trees/{char_id}.json`.
- **Use:** Player selects a topic or companion initiates on idle; explored branches are deleted.
- **Regenerate:** Automatically when remaining branches drop below threshold.

## Detailed Reference

Full examples, JSON shapes, and prompt details are archived in
`docs/infrastructure/async/archive/SYNC_archive_2024-12.md`.

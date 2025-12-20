# Storm Loader — Algorithm: Mutation Intake

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Storm_Loader_As_Diff.md
BEHAVIORS:       ./BEHAVIORS_Storm_Loader_Mutations.md
THIS:            ALGORITHM_Storm_Loader_Pipeline.md
VALIDATION:      ./VALIDATION_Storm_Loader_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Storm_Loader.md
HEALTH:          ./HEALTH_Storm_Loader.md
SYNC:            ./SYNC_Storm_Loader.md
```

---

## ALGORITHM

```
1. Load storm mutation files from the intake queue.
2. Validate schema and guardrails.
3. Apply mutations to the graph.
4. Record applied storm metadata and failures.
```

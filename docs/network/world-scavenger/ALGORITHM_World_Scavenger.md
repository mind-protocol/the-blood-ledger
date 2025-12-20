# World Scavenger — Algorithm: Reuse Before Generate

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scavenge_Before_Generate.md
BEHAVIORS:       ./BEHAVIORS_Scavenger_Priority_Stack.md
THIS:            ALGORITHM_World_Scavenger.md
VALIDATION:      ./VALIDATION_Scavenger_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Scavenger.md
HEALTH:          ./HEALTH_World_Scavenger.md
SYNC:            ./SYNC_World_Scavenger.md
```

---

## ALGORITHM

```
1. Receive a generation request with context.
2. Query scavenger cache for reusable artifacts.
3. Rank candidates by similarity and freshness.
4. Return a cached artifact or fall back to generation.
5. Record reuse metrics for future prioritization.
```

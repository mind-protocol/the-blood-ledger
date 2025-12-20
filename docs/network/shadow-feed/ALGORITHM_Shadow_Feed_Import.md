# Shadow Feed — Algorithm: Rumor Import

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Shadow_Feed_Rumor_Cache.md
BEHAVIORS:       ./BEHAVIORS_Rumor_Import.md
THIS:            ALGORITHM_Shadow_Feed_Import.md
VALIDATION:      ./VALIDATION_Shadow_Feed_Locks.md
IMPLEMENTATION:  ./IMPLEMENTATION_Shadow_Feed.md
HEALTH:          ./HEALTH_Shadow_Feed.md
SYNC:            ./SYNC_Shadow_Feed.md
```

---

## ALGORITHM

```
1. Pull candidate rumors from external sources or caches.
2. Filter by safety locks and relevance.
3. Insert into local rumor cache with provenance.
4. Surface to narrative systems as low-truth narratives.
```

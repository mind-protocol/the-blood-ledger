# Ghost Dialogue — Algorithm: Replay and Injection

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Ghost_Dialogue_Index.md
BEHAVIORS:       ./BEHAVIORS_Ghost_Dialogue_Replay.md
THIS:            ALGORITHM_Ghost_Dialogue_Replay.md
VALIDATION:      ./VALIDATION_Ghost_Dialogue_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ghost_Dialogue.md
HEALTH:          ./HEALTH_Ghost_Dialogue.md
SYNC:            ./SYNC_Ghost_Dialogue.md
```

---

## ALGORITHM

```
1. Receive a dialogue request for a character or place.
2. Query the ghost dialogue index for candidate lines.
3. Filter by safety locks (canon, proximity, causality).
4. Select a compatible line and inject into response stream.
5. Record reuse metrics for curation.
```

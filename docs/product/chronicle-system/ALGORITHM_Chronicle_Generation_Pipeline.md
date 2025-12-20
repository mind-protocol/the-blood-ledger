# Chronicle System — Algorithm: Generation Pipeline

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
BEHAVIORS:       ./BEHAVIORS_Chronicle_Types_And_Structure.md
THIS:            ALGORITHM_Chronicle_Generation_Pipeline.md
VALIDATION:      ./VALIDATION_Chronicle_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Chronicle_System.md
HEALTH:          ./HEALTH_Chronicle_System.md
SYNC:            ./SYNC_Chronicle_System.md
```

---

## ALGORITHM

```
1. Collect session signals (moments, player choices, narrator highlights).
2. Select a chronicle type and outline (session recap, character focus, etc.).
3. Generate script beats with LLM and align to source moments.
4. Render TTS and visual assets (images/scene panels).
5. Compose final video + metadata package.
6. Publish or queue for player approval and upload.
```

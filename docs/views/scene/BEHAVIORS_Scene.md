# Scene View — Behaviors

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
THIS:        BEHAVIORS_Scene.md (you are here)
ALGORITHM:   ./ALGORITHM_Scene.md
VALIDATION:  ./VALIDATION_Scene.md
TEST:        ./TEST_Scene.md
SYNC:        ./SYNC_Scene.md
```

---

### B1: Framed Atmosphere
```
GIVEN:  Player enters a location
WHEN:   Scene view renders
THEN:   2-3 lines of sensory grounding appear before dialogue
```

### B2: Narrative Voices
```
GIVEN:  Narratives with high weight attach to present characters
WHEN:   Scene loads
THEN:   The player sees inner voices / ledger whispers inline with the main dialogue
```

### B3: Clickable Language
```
GIVEN:  CAN_LEAD_TO links specify require_words
WHEN:   Scene renders
THEN:   Clickable words are highlighted and trigger transitions instantly (<50ms)
```

### B4: Waiting Has Consequences
```
GIVEN:  Wait-triggered transitions exist
WHEN:   The player pauses for the configured ticks
THEN:   The scene advances (new moment, consequence narration) without input
```

### B5: Ledger Integration
```
GIVEN:  Ledger entries are affected by conversation
WHEN:   Critical obligations are referenced
THEN:   The corresponding ledger entries glow / link for immediate inspection
```
```

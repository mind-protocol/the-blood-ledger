# Chronicle System — Behaviors: Session, Weekly, Life

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Chronicle System.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
THIS:            BEHAVIORS_Chronicle_Types.md (you are here)
MECHANISMS:      ./MECHANISMS_Chronicle_Pipeline.md
VERIFICATION:    ./VALIDATION_Chronicle_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Chronicle_System.md
TEST:            ./TEST_Chronicle_System.md
SYNC:            ./SYNC_Chronicle_System.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Chronicle System.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Session chronicle generated after play

```
GIVEN:  a session ends
WHEN:   chronicle generation runs
THEN:   a 60–90 second session chronicle is produced
```

### B2: Weekly chronicle summarizes arc

```
GIVEN:  7 days or major arc completion
WHEN:   weekly generation runs
THEN:   a 3–5 minute chronicle is produced
```

### B3: Life chronicle on death

```
GIVEN:  player character dies
WHEN:   life chronicle generation runs
THEN:   an 8–15 minute chronicle is produced
```

---

## INPUTS / OUTPUTS

### Primary Function: `generate_chronicle()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| chronicle_buffer | object | Events and snapshots |
| chronicle_type | string | session/weekly/life |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| video_file | string | Rendered MP4 path |

**Side Effects:**

- Saves MP4, thumbnail, metadata
- Optional upload to YouTube

---

## EDGE CASES

### E1: No significant events

```
GIVEN:  low activity session
THEN:   chronicle focuses on "shadow" events or skips upload
```

### E2: Upload failure

```
GIVEN:  YouTube upload fails
THEN:   store MP4 locally and retry later
```

---

## ANTI-BEHAVIORS

### A1: Raw gameplay dump

```
GIVEN:   chronicle generation
WHEN:    output is produced
MUST NOT: output a raw log
INSTEAD: produce a cinematic narrative
```

### A2: Player forced to upload

```
GIVEN:   chronicle generated
WHEN:    upload choice appears
MUST NOT: auto-upload without consent
INSTEAD: require explicit opt-in
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define consent flow for auto-upload
- [ ] Define default sharing settings
- IDEA: Add chronicle preview and trim tools

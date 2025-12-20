# Tempo — Health: Tick and Query Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the tempo controller's tick loop and graph queries. It
exists to prevent silent failures that stall moment surfacing. It does not
verify narrative quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tempo.md
BEHAVIORS:       ./BEHAVIORS_Tempo.md
ALGORITHM:       ./ALGORITHM_Tempo_Controller.md
VALIDATION:      ./VALIDATION_Tempo.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tempo.md
THIS:            HEALTH_Tempo_Controller.md
SYNC:            ./SYNC_Tempo.md

IMPL:            engine/infrastructure/tempo/tempo_controller.py
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: tempo_tick_advances
    flow_id: tempo_tick
    priority: high
    rationale: If ticks fail, moments never surface to the player.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: tempo_tick_advances
```

---

## HOW TO RUN

```bash
# Manual: run the tempo controller and confirm ticks increment
python3 - <<'PY'
from engine.infrastructure.tempo.tempo_controller import TempoController
controller = TempoController(playthrough_id="default")
print(controller.tick_once())
PY
```

---

## KNOWN GAPS

- [ ] No automated tick health check exists.

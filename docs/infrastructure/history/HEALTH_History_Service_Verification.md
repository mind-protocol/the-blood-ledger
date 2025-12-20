# History — Health: Service Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the HistoryService record/query flows. It exists to
reduce the risk of silent failures in narrative persistence and retrieval. It
does not verify narrator orchestration or UI rendering.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_History.md
BEHAVIORS:       ./BEHAVIORS_History.md
ALGORITHM:       ./ALGORITHM_History.md
VALIDATION:      ./VALIDATION_History.md
IMPLEMENTATION:  ./IMPLEMENTATION_History_Service_Architecture.md
THIS:            HEALTH_History_Service_Verification.md
SYNC:            ./SYNC_History.md

IMPL:            engine/infrastructure/history/service.py
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: history_record_roundtrip
    flow_id: record_player_history
    priority: high
    rationale: History must persist and remain queryable by witnesses.
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
    source: history_record_roundtrip
```

---

## HOW TO RUN

```bash
# Manual smoke: record + query history
python3 - <<'PY'
from engine.infrastructure.history.service import HistoryService
service = HistoryService(playthrough_id="default")
result = service.record_world_history("Test event", detail="Health check")
print(result)
print(service.query_history("Test event"))
PY
```

---

## KNOWN GAPS

- [ ] No automated tests are wired to validate record/query round trips.

# Frontend — Health: UI Runtime Checks

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the frontend runtime boot and core UI routes. It
exists to detect failures where the UI fails to render or fetches break. It
does not verify narrative quality or backend correctness.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
THIS:            HEALTH_Frontend_Runtime.md
SYNC:            ./SYNC_Frontend.md
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: frontend_boots
    flow_id: frontend_boot
    priority: high
    rationale: If the UI fails to boot, the experience is blocked.
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
    source: frontend_boots
```

---

## HOW TO RUN

```bash
# Manual: start frontend and confirm /start loads
cd frontend && npm run dev
```

---

## KNOWN GAPS

- [ ] No automated UI health checks are configured.

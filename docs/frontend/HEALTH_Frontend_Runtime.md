# Frontend — Health: UI Runtime Checks

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-22
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the frontend runtime boot and core UI routes. It exists to:
- Detect failures where the UI fails to render
- Verify TypeScript compilation succeeds
- Ensure API connectivity works
- Catch SSE connection issues

It does not verify narrative quality or backend correctness.

---

## WHY THIS PATTERN

The frontend is the player's window into the game. Tests verify component logic, but HEALTH checks verify the full boot→render→connect pipeline works end-to-end. Dock-based checks ensure:
- Build succeeds without type errors
- Core routes render
- Backend connectivity works

---

## CHAIN

```
OBJECTIFS:       ./OBJECTIFS_Frontend_UI.md
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Frontend_Code_Architecture.md
THIS:            HEALTH_Frontend_Runtime.md
SYNC:            ./SYNC_Frontend.md

IMPL:            tools/health/check_frontend.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented frontend health checker
Implement `tools/health/check_frontend.py` checker script that:
- Executes dock-based verification against VALIDATION criteria V1-V5
- Updates `status.result.value` in this file
- Runs throttled (max 10/day in CI)
- Integrates with `ngram doctor` for aggregated reporting

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: frontend_boot
    purpose: Initialize React app and render core routes.
    triggers:
      - type: manual
        source: npm run dev
        notes: Starts Next.js dev server.
    frequency:
      expected_rate: 1-10/day (dev), continuous (prod)
      peak_rate: 100/day (active development)
      burst_behavior: Server restarts on code changes.
    risks:
      - V5 (TypeScript errors)
      - Build failures
    notes: Must complete in < 30 seconds.

  - flow_id: api_connectivity
    purpose: Verify backend API is reachable.
    triggers:
      - type: event
        source: useGameState hook
        notes: Health check on mount.
    frequency:
      expected_rate: 1/min (health polling)
      peak_rate: 10/min
      burst_behavior: Reconnect attempts on failure.
    risks:
      - E1 (backend unavailable)
      - E3 (SSE connection lost)
    notes: Updates isConnected state.

  - flow_id: sse_streaming
    purpose: Receive real-time updates from backend.
    triggers:
      - type: event
        source: useMoments hook
        notes: SSE subscription on mount.
    frequency:
      expected_rate: continuous
      peak_rate: 100 events/min
      burst_behavior: Events batched in UI.
    risks:
      - E3 (connection lost)
      - E4 (invalid response shape)
    notes: Reconnects automatically.
```

---

## HEALTH INDICATORS SELECTED

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Build succeeds | typescript_compiles | Type errors = broken build |
| UI renders | frontend_boots | No render = blocked experience |
| Backend connected | api_connectivity_ok | No connection = no game |

```yaml
health_indicators:
  - name: typescript_compiles
    flow_id: frontend_boot
    priority: high
    rationale: TypeScript errors block deployment (V5).

  - name: frontend_boots
    flow_id: frontend_boot
    priority: high
    rationale: If the UI fails to boot, the experience is blocked.

  - name: api_connectivity_ok
    flow_id: api_connectivity
    priority: high
    rationale: Backend connection is required for gameplay.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-22T00:00:00Z
    source: typescript_compiles
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: typescript_compiles
    purpose: Verify npm run build succeeds (V5).
    status: active
    priority: high

  - name: frontend_boots
    purpose: Verify core routes render.
    status: pending
    priority: high

  - name: api_connectivity_ok
    purpose: Verify backend health check succeeds.
    status: pending
    priority: high
```

---

## INDICATOR: typescript_compiles

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: typescript_compiles
  client_value: UI is deployable; no type errors.
  validation:
    - validation_id: V5
      criteria: All API responses are typed; no 'any' in production paths.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed: [binary, enum]
  selected: [enum]
  semantics:
    enum: OK (build succeeds), ERROR (build fails)
  aggregation:
    method: worst_of
    display: enum
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: npm_build
    method: npm run build
    location: frontend/package.json
  output:
    id: build_result
    method: exit code
    location: stdout
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Run npm run build, check exit code.
  steps:
    - cd frontend
    - Run npm run build
    - Check exit code (0 = success)
  data_required: Node.js, npm, frontend source.
  failure_mode: Non-zero exit code.
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual
  max_frequency: 10/day
  burst_limit: none
  backoff: none
```

### MANUAL RUN

```yaml
manual_run:
  command: cd frontend && npm run build
  notes: Requires Node.js and npm installed.
```

---

## INDICATOR: frontend_boots

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: frontend_boots
  client_value: Player can access the game UI.
  validation:
    - validation_id: V1
      criteria: Frontend state is derived from backend API responses.
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Start dev server, verify route renders.
  steps:
    - Start npm run dev
    - Wait for server ready
    - Fetch http://localhost:3000/start
    - Verify HTTP 200 and HTML content
  data_required: Node.js, npm, frontend source.
  failure_mode: Server fails to start or route returns error.
```

### MANUAL RUN

```yaml
manual_run:
  command: |
    cd frontend && npm run dev &
    sleep 10
    curl -s http://localhost:3000/start | head -20
  notes: Verify /start route renders HTML.
```

---

## HOW TO RUN

```bash
# Run TypeScript compilation check
cd frontend && npm run build

# Run dev server and verify boot
cd frontend && npm run dev
# Then open http://localhost:3000/start in browser

# Run all frontend health checks (manual)
echo "=== Frontend Health Checks ==="
cd frontend
npm run build && echo "typescript_compiles: OK" || echo "typescript_compiles: ERROR"
```

---

## KNOWN GAPS

- [ ] V1 (backend source of truth) automated verification not implemented.
- [ ] V2/V3/V4 (state invariants) automated verification not implemented.
- [ ] E1-E4 error condition checkers not implemented.
- [ ] No automated UI health checks are configured.
- [ ] No Playwright/E2E tests for route verification.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add Playwright for automated E2E tests.
- IDEA: Add health check route that verifies all hooks.
- QUESTION: Should CI run build check on every PR?

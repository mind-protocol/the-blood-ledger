# Scenario Selection - Patterns: Curated Starting Point Picker

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Scenario_Selection.md
SYNC:  ./SYNC_Scenario_Selection.md
IMPL:  frontend/app/scenarios/page.tsx
```

---

## THE PROBLEM

Players need to choose a starting scenario after naming their character. The
UI must present clear, atmospheric options that map to backend scenario IDs so
playthrough creation is deterministic.

---

## THE PATTERN

Maintain a static, curated scenario list in the selection page, render a
left-column chooser with a right-column preview, and hand the selected scenario
ID to the playthrough creation API.

---

## SCOPE

This pattern covers only the scenario selection page UX, the curated list
content, and the handoff of the selected scenario ID to create a playthrough.
It does not define scenario authoring, backend validation, or broader session
state beyond the immediate selection flow.

---

## INSPIRATIONS

The layout borrows from tabletop campaign pickers and visual novel episode
selectors: short atmospheric summaries, a focused preview panel, and a clear
commit action once the player knows what kind of story they are entering.

---

## PRINCIPLES

### Principle 1: Scenario IDs Are the Contract

Scenario IDs in the UI must match the backend YAML and API expectations so the
selected option creates the intended playthrough.

### Principle 2: Guard the Flow

If player identity data is missing, redirect back to the start screen rather
than creating an incomplete playthrough.

### Principle 3: Preview Before Commit

Selection shows the scenario tone, tagline, and starting items to help players
understand the promise before they begin.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/lib/api` | `createPlaythrough` call to seed the backend playthrough |
| `scenarios/*.yaml` | Scenario IDs and narrative intent reflected in the UI list |

---

## INSPIRATIONS

- **Narrative selection menus** — RPG prologue pickers that pair a strong visual with a succinct promise to anchor the player's choice.
- **Streaming adventure hubs** — Two-column layouts that keep the list visible while the detail pane updates, reducing selection anxiety.
- **Visual novel prologues** — Character-driven scenario intros that emphasize tone, stakes, and starting constraints up front.

---

## SCOPE

### In Scope

- Curate a small, readable scenario list with previews that reflect the current YAML catalog and keep IDs in sync.
- Enforce session-gated flow by redirecting to the start screen if player identity or setup data is missing.
- Provide enough preview detail (tone, tagline, starting items) to set expectations before the playthrough begins.

### Out of Scope

- Authoring, validating, or versioning the scenario YAML content; those workflows live outside the selection UI.
- Handling every playthrough creation edge case beyond retry and logging; deeper error recovery belongs to the API layer.
- Persisting player identity beyond session storage or adding account-level scenario unlock logic for v1.

---

## WHAT THIS DOES NOT SOLVE

- Authoring, validating, or versioning scenario YAML content lives in tooling and docs outside this UI surface.
- Persisting player state beyond session storage or offering account-level save migration in the selection flow.
- Handling playthrough creation failures beyond logging and retry; deeper recovery paths belong to the backend API.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Consider loading the scenario list from the backend once scenario metadata is exposed.
- [ ] Decide whether tone tags should be color-coded by category.

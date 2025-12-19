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

## WHAT THIS DOES NOT SOLVE

- Authoring or validating scenario YAML content.
- Persisting player state beyond session storage.
- Handling playthrough creation failures beyond logging and retry.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Consider loading the scenario list from the backend once scenario metadata is exposed.
- [ ] Decide whether tone tags should be color-coded by category.

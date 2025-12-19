# Frontend — Implementation: Code Architecture (Overview)

```
STATUS: STABLE
CREATED: 2025-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Presentation_Layer.md
BEHAVIORS:       ./BEHAVIORS_Frontend_State_And_Interaction.md
ALGORITHM:       ./ALGORITHM_Frontend_Data_Flow.md
VALIDATION:      ./VALIDATION_Frontend_Invariants.md
THIS:            IMPLEMENTATION_Frontend_Code_Architecture.md (you are here)
TEST:            ./TEST_Frontend_Coverage.md
SYNC:            ./SYNC_Frontend.md

IMPL:            frontend/app/page.tsx
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## SUMMARY

The frontend is a Next.js App Router UI that renders the game state provided by the backend. State logic lives in hooks, while components focus on presentation and interaction.

---

## CONTENTS

- `IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Code_Structure.md` — File layout, responsibilities, key dependencies
- `IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md` — Entry points, runtime flow, configuration, and doc links

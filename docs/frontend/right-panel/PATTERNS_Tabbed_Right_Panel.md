# Right Panel — Patterns: Tabbed Sidebar For Chronicle And Ledger

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Tabbed_Right_Panel.md
SYNC:  ./SYNC_Right_Panel.md
IMPL:  frontend/components/panel/RightPanel.tsx
```

---

## THE PROBLEM

The scene view needs a compact place for ongoing narrative context (chronicle),
conversation recall, and unresolved obligations (ledger). Showing all three at
once would crowd the main scene and force constant scrolling.

---

## THE PATTERN

Use a right-side panel with tabbed navigation so the player can switch between
chronicle, conversations, and ledger without leaving the scene. Keep the state
local to the panel and rely on data passed in from the main game client.

---

## SCOPE

This pattern covers the right-side panel layout, tab switching, and read-only
rendering of chronicle, conversations, and ledger content within the scene
view; it does not cover data creation, persistence, or backend sync logic.

---

## INSPIRATIONS

Sidebar tab patterns from collaborative tools (Slack/Notion), plus RPG journals
that separate lore, dialogue, and obligations into quick-access panes, guided
the decision to keep the panel compact and immediately switchable.

---

## PRINCIPLES

### Principle 1: Scene First

The panel should never compete with the scene for space; it exists to support
scene comprehension and recall, not replace the main flow.

### Principle 2: Fast Context Switching

Tabs are short, always visible, and switch immediately without round trips.

### Principle 3: Read-Only Display

The panel does not mutate game state; it renders snapshots passed from higher
state owners.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `frontend/components/panel/ChronicleTab.tsx` | Chronicle display for timeline context |
| `frontend/components/panel/ConversationsTab.tsx` | Conversation list and preview |
| `frontend/components/panel/LedgerTab.tsx` | Ledger summary by obligation type |
| `frontend/types/game` | Data shapes for entries and player state |

---

## WHAT THIS DOES NOT SOLVE

- Authoring or mutating chronicle, conversations, or ledger entries.
- Persisting UI state between sessions; the active tab resets on reload.
- Providing search or filtering within tabs.

---

## GAPS / IDEAS / QUESTIONS

Open questions focus on whether the panel should behave like a persistent
context shelf or an attention-capture surface, because that choice drives the
storage and indicator design.

- [ ] Decide if the active tab should persist in local storage or per-session.
- [ ] Consider unread indicators when new entries arrive within each tab.

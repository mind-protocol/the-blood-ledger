# Minimap — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:  ./PATTERNS_Discovered_Location_Minimap.md
THIS:      SYNC_Minimap.md (you are here)
IMPL:      frontend/components/minimap/Minimap.tsx
```

---

## MATURITY

**What's canonical (v1):**
- Read-only minimap renders discovered locations and current location.
- Clicking the minimap triggers the full map open action.

**What's still being designed:**
- Visual treatment for connections and region boundaries.
- Whether labels beyond the current location should appear.

**What's proposed (v2+):**
- Animated discovery pulses when new locations are revealed.

---

## CURRENT STATE

The minimap component renders a square button with plotted discovered
locations, connection lines, and a current-location label. It relies on
map data passed in from the parent game state and triggers a single callback
to open the full map.

---

## IN PROGRESS

No active minimap UI changes are underway. Any upcoming work should first
confirm how the minimap snapshot aligns with the full map view styling to
avoid diverging visual language.

---

## KNOWN ISSUES

None recorded for the minimap module right now, but verify that the current
location label stays legible once the map palette or typography shifts.

---

## RECENT CHANGES

### 2025-12-19: Completed missing SYNC template sections

- **What:** Added in-progress, known-issues, human handoff, consciousness
  trace, and pointers sections; expanded short entries to meet template size.
- **Why:** Repair task flagged template drift in the minimap SYNC doc.
- **Files:** `docs/frontend/minimap/SYNC_Minimap.md`

### 2025-12-19: Filled template sections in minimap patterns

- **What:** Added SCOPE and INSPIRATIONS sections and expanded template text.
- **Why:** Repair task flagged missing PATTERNS sections and short entries.
- **Files:** `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`

### 2025-12-19: Documented minimap module

- **What:** Added minimap module docs, mapping, and DOCS reference.
- **Why:** Repair task flagged minimap as undocumented.
- **Files:** `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md`, `docs/frontend/minimap/SYNC_Minimap.md`, `modules.yaml`, `frontend/components/minimap/Minimap.tsx`

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Documented the minimap module and linked the entrypoint.

**What you need to understand:**
The minimap is a read-only preview. Any state mutations or navigation should
happen in the parent map flow.

---

## HANDOFF: FOR HUMAN

No decisions require human input right now. If the minimap behavior changes,
please review the map UI alignment goals before approving a new interaction.

---

## AGENT OBSERVATIONS

### Remarks
- Filled missing SCOPE and INSPIRATIONS sections to match the template.

### Suggestions
No immediate suggestions beyond keeping the minimap strictly read-only and
consistent with the full map rendering rules to prevent UX drift.

### Propositions
Consider adding a lightweight hover tooltip only if it mirrors the map view
metadata and does not introduce additional navigation or interactions.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Update docs if minimap behavior changes beyond a preview,
  especially if interaction expands past the "open full map" action.

### Tests to Run

```bash
npm test
```

---

## CONSCIOUSNESS TRACE

Focused on closing template drift without altering the minimap behavior,
keeping edits scoped to documentation completeness and clarity.

---

## POINTERS

Review `docs/frontend/minimap/PATTERNS_Discovered_Location_Minimap.md` for
design intent and `frontend/components/minimap/Minimap.tsx` for the current
rendering implementation and props contract.

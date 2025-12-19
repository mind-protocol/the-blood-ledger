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

## RECENT CHANGES

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

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Update docs if minimap behavior changes beyond a preview.

### Tests to Run

```bash
npm test
```

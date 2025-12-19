# Archived: SYNC_Frontend.md (Condensed)

Archived on: 2025-12-19
Source: SYNC_Frontend_archive_2025-12.md

---

## MATURITY

**What's canonical (v1):**
- Next.js 16 app structure with App Router
- Scene display with atmospheric UI
- useGameState hook for backend connection
- useMoments hook for moment system
- Right panel with Chronicle/Ledger/Conversations tabs
- Map view with fog of war
- Moment display with clickable text
- SSE streaming integration

**What's still being designed:**
- Testing strategy (Playwright mentioned, not implemented)
- Component-level tests

**What's proposed (v2+):**
- Storybook for component development
- Better offline/fallback experience

---

## RECENT CHANGES (ARCHIVED SUMMARY)

### 2025-12-19: Frontend docs chain and mappings
- Created the full frontend documentation chain and updated the PATTERNS/CHAIN links.
- Mapped frontend modules in `modules.yaml` and added DOCS references across core files.

### 2025-12-19: SSE integration and polling removal
- Added SSE subscription to `useGameState` and removed the polling hack in CenterStage.
- Updated `ALGORITHM_Frontend_Data_Flow.md` to reflect SSE handling.

### 2025-12-19: Implementation doc path normalization
- Normalized implementation doc file paths to `frontend/**` and fixed `.env.local` reference.

### 2025-12-19: UI layout adjustments
- Moved speed controls into the Chronicle panel footer and aligned tempo API base usage.

---

## NOTES

This archive consolidates the previous SYNC archive content to reduce module doc size.
For detailed per-file change logs, consult git history around 2025-12-19.

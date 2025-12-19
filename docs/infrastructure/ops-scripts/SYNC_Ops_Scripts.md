# Ops Scripts — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Operational_Seeding_And_Backfill_Scripts.md
BEHAVIORS:       ./BEHAVIORS_Operational_Script_Runbooks.md
ALGORITHM:       ./ALGORITHM_Seeding_And_Backfill_Flows.md
VALIDATION:      ./VALIDATION_Operational_Script_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Engine_Scripts_Layout.md
TEST:            ./TEST_Operational_Scripts.md
THIS:            SYNC_Ops_Scripts.md (you are here)
IMPL:            engine/scripts/seed_moment_sample.py
```

---

## MATURITY

**What's canonical (v1):**
- CLI scripts exist for seeding sample moment data and backfilling missing
  images on graph nodes.
- Scripts run as standalone entry points with explicit host/graph/playthrough
  arguments.

**What's still being designed:**
- How image backfill should be invoked in production or tooling flows.

**What's proposed (v2+):**
- Unified operational CLI runner for all engine maintenance scripts.

---

## CURRENT STATE

`engine/scripts/seed_moment_sample.py` seeds a YAML sample into FalkorDB using
GraphOps. `engine/scripts/generate_images_for_existing.py` scans for nodes
missing `image_path` and uses the image-generation utilities to backfill
assets. Injection-related scripts in the same directory are documented under
`docs/infrastructure/async/` to avoid duplicating their behavior docs.

---

## RECENT CHANGES

### 2025-12-19: Fixed ops-scripts implementation links

- **What:** Updated ops-scripts implementation doc links to point at existing engine paths.
- **Why:** Repair task flagged broken file references in the implementation doc.
- **Files:** `docs/infrastructure/ops-scripts/IMPLEMENTATION_Engine_Scripts_Layout.md`

### 2025-12-19: Documented ops scripts module

- **What:** Added minimal docs and module mapping for engine operational scripts.
- **Why:** Repair task flagged `engine/scripts` as undocumented.
- **Files:** `docs/infrastructure/ops-scripts/PATTERNS_Operational_Seeding_And_Backfill_Scripts.md`, `docs/infrastructure/ops-scripts/SYNC_Ops_Scripts.md`, `modules.yaml`, `engine/scripts/seed_moment_sample.py`

### 2025-12-19: Verified ops-scripts mapping

- **What:** Confirmed the ops-scripts documentation chain and DOCS reference are in place.
- **Why:** Repair 51 revalidated `engine/scripts` documentation coverage.
- **Files:** No code changes.

### 2025-12-19: Linked backfill script to ops-scripts docs

- **What:** Added DOCS reference in `engine/scripts/generate_images_for_existing.py`.
- **Why:** Ensure `ngram context` resolves the ops-scripts documentation chain.
- **Files:** `engine/scripts/generate_images_for_existing.py`

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Added ops-scripts docs and mapping, linked the seed script.

**What you need to understand:**
Operational scripts are intentionally thin wrappers; keep logic in shared
modules and update docs if new scripts are added.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Update ops-scripts docs if new scripts are added to
  `engine/scripts/`.

### Tests to Run

```bash
python engine/scripts/seed_moment_sample.py --help
python engine/scripts/generate_images_for_existing.py --help
```

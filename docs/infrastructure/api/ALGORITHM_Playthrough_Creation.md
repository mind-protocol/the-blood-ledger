# API — Algorithm: Playthrough Creation (Legacy Alias)

```
STATUS: DEPRECATED (alias to ALGORITHM_Api.md)
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against engine/infrastructure/api/playthroughs.py (working tree)
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Api.md
BEHAVIORS:       ./BEHAVIORS_Api.md
THIS:            ALGORITHM_Playthrough_Creation.md (legacy alias)
VALIDATION:      ./VALIDATION_Api.md
IMPLEMENTATION:  ./IMPLEMENTATION_Api.md
TEST:            ./TEST_Api.md
SYNC:            ./SYNC_Api.md

IMPL:            engine/infrastructure/api/playthroughs.py
```

> **Contract:** This file is a legacy alias. The canonical algorithm reference
> for the API module is `docs/infrastructure/api/ALGORITHM_Api.md`.

---

## OVERVIEW

Playthrough creation turns a scenario selection into a live, isolated graph
instance plus a starter `scene.json` payload for the frontend. This alias
summarizes the flow so older references keep working while the canonical API
algorithm doc remains the source of truth.

---

## DATA STRUCTURES

### PlaythroughCreateRequest

```
player_name: string
player_gender: string
scenario_id: string
```

The request payload passed to `/api/playthrough/create` and its alias.

### PlaythroughFilesystemLayout

```
playthroughs/{id}/
  player.yaml
  scene.json
  message_queue.json
  injection_queue.json
  stream.jsonl
  PROFILE_NOTES.md
```

Directory layout that makes the playthrough discoverable by other endpoints.

### ScenarioPayload

```
nodes: list
links: list
opening: { narration, ... }
location: string
```

Scenario YAML entries used to seed graph nodes, relationships, and opening
narration moments for the new playthrough.

---

## ALGORITHM: create_playthrough

### Step 1: Generate an isolated playthrough id

Normalize the player name into a slug and append a numeric suffix if the
directory already exists. This prevents collisions while keeping IDs stable
for users who repeat their name.

### Step 2: Materialize the playthrough workspace

Create the playthrough folder structure, write `player.yaml`, and seed the
queue and log files. This step ensures downstream endpoints can immediately
read/write files even if graph initialization fails.

### Step 3: Initialize graph + scenario state

Load base seed data into a new FalkorDB graph and apply the scenario’s nodes
and links. Update the player node with the request’s name and gender before
calling `GraphOps.apply` so the graph reflects the current player identity.

### Step 4: Create opening narration moments

Parse the scenario opening narration, create Moment nodes with `status=possible`,
and attach them to the opening location. These moments are surfaced later by
the canon holder rather than pre-marking them as spoken.

### Step 5: Build the opening scene payload

Transform the opening template into a `scene.json` payload if the template
exists; otherwise write a minimal fallback scene. Persist the JSON so the
frontend can fetch the same scene on subsequent loads.

---

## KEY DECISIONS

### D1: Graph isolation vs. reuse

```
IF playthrough_id is new:
    create a new graph name and seed it
    keep the playthrough isolated per player
ELSE:
    reject or suffix the id to avoid cross-player state bleed
```

Isolation preserves per-player state at the cost of more graph instances.

### D2: Opening moments as possible vs. spoken

```
IF narration lines exist:
    create moments with status="possible" and weight=1.0
    let canon holder surface and record them
ELSE:
    skip moment creation and rely on the fallback scene
```

This keeps canon recording centralized while still bootstrapping the scene.

---

## DATA FLOW

```
PlaythroughCreateRequest
    ↓
playthrough_id + filesystem layout
    ↓
scenario YAML + seed graph data
    ↓
graph mutations + opening moments
    ↓
scene.json payload
    ↓
API response {playthrough_id, scenario, scene}
```

---

## COMPLEXITY

**Time:** O(S + M) — S for scenario nodes/links, M for opening narration lines.

**Space:** O(S + M) — persistent files and graph writes scale with scenario size.

**Bottlenecks:**
- Scenario injection cost grows with node/link count in the YAML.
- Graph initialization latency dominates if seed data is large.

---

## HELPER FUNCTIONS

### `_opening_to_scene_tree()`

**Purpose:** Convert opening template JSON plus scenario data into a scene tree.

**Logic:** Maps beats into narration/voice entries and injects scenario-specific
character and location names into the response payload.

### `_count_branches()`

**Purpose:** Count discussion branches when generating metadata for openings.

**Logic:** Walks nested discussion structures to compute clickables and branch
depths used by the scene tree.

### `_get_playthrough_queries()`

**Purpose:** Provide cached `GraphQueries` objects for a playthrough graph.

**Logic:** Lazily constructs the query helper on first access and reuses it for
subsequent API calls to avoid repeated connection setup.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| engine/init_db.py | `load_initial_state()` | Base world graph seed data |
| engine/physics/graph/graph_ops.py | `GraphOps.apply()` | Scenario nodes/links persisted |
| engine/physics/graph/graph_ops.py | `GraphOps.add_moment()` | Opening narration moments |
| scenarios/*.yaml | Scenario file load | Nodes, links, opening, location |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Confirm whether playthrough creation should fail on seed-data errors.
- [ ] Decide if scene template lookup should be scenario-specific.
- IDEA: Cache parsed scenario YAML to avoid re-reading on duplicate starts.
- IDEA: Emit a single audit event once playthrough creation completes.
- QUESTION: Should the API return validation warnings from graph injection?

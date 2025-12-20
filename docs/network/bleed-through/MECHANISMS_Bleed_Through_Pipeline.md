# Bleed-Through — Mechanisms: Ghosts, Rumors, Reports

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scars_Cross_Worlds.md
BEHAVIORS:       ./BEHAVIORS_Ghosts_Rumors_Reports.md
THIS:            MECHANISMS_Bleed_Through_Pipeline.md (you are here)
VERIFICATION:    ./VALIDATION_Bleed_Through_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Bleed_Through.md
TEST:            ./TEST_Bleed_Through.md
SYNC:            ./SYNC_Bleed_Through.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

Bleed-Through is a cross-world content layer that injects ghosts and rumors without violating local canon, and generates bleed reports that surface player legacy. It is narrative-first and hides the underlying reuse economics.

---

## DATA STRUCTURES

### GhostEntity

```
source_world: string
entity_id: string
type: character | rumor
traits: list[string]
scars: list[scar]
transposition_map: map
```

### BleedReport

```
subject: character
appearances: list[appearance]
stats: {died, betrayed, saved, legend_count}
```

---

## MECHANISM: Ghost Injection

### Step 1: Select ghost candidate

Pick a character from scavenger/ghost index that matches context.

### Step 2: Transpose conflicts

Apply renaming/relocation/fuzzing to prevent canon collision.

### Step 3: Inject into local graph

Create character node and attach scars/beliefs.

---

## MECHANISM: Rumor Bleed

### Step 1: Choose distant event

Select an event from shadow feed or bleed sources.

### Step 2: Downgrade to rumor

Set truth to low value; attach rumor provenance.

### Step 3: Place into local narrative

Insert as gossip from travelers or markets.

---

## MECHANISM: Bleed Reports

### Step 1: Aggregate appearances

Collect where the character appeared in other worlds.

### Step 2: Summarize outcomes

Count deaths, betrayals, saves, and legends.

### Step 3: Deliver report

Send via weekly email or in-game notification.

---

## KEY DECISIONS

### D1: Ghost vs. generated NPC

```
IF ghost candidate matches and passes canon checks:
    inject ghost
ELSE:
    generate new NPC
```

### D2: Rumor truth value

```
IF local canon contradicts event:
    truth = 0.0
ELSE:
    truth = 0.3
```

---

## DATA FLOW

```
External world data
    ↓
Transposition + canon checks
    ↓
Ghost/rumor injection
    ↓
Bleed report aggregation
```

---

## COMPLEXITY

**Time:** O(n) for report aggregation (appearances).

**Space:** O(n) for bleed report histories.

**Bottlenecks:**
- Ghost candidate search at scale
- Report aggregation if not indexed

---

## HELPER FUNCTIONS

### `transpose_ghost()`

**Purpose:** Resolve name/place conflicts.

**Logic:** Apply rename/relocate/fuzzing in order.

### `generate_bleed_report()`

**Purpose:** Summarize cross-world appearances.

**Logic:** Aggregate appearance records, compute stats.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| docs/network/world-scavenger | select_ghost | Candidate NPCs |
| docs/network/transposition | resolve_conflict | Canon-safe references |
| docs/network/shadow-feed | select_rumor | Distant event templates |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Define data store for bleed report histories
- [ ] Define content moderation for ghost imports
- IDEA: Provide opt-out for players who dislike bleed-through
- QUESTION: Should rumors ever be marked true in local canon?

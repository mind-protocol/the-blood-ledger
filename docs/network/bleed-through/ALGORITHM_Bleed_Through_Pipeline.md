# Bleed-Through — Algorithm: Ghosts, Rumors, Reports

```
STATUS: DESIGNING
CREATED: 2025-12-20
UPDATED: 2025-12-21
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Scars_Cross_Worlds.md
BEHAVIORS:       ./BEHAVIORS_Ghosts_Rumors_Reports.md
THIS:            ALGORITHM_Bleed_Through_Pipeline.md
VALIDATION:      ./VALIDATION_Bleed_Through_Safety.md
IMPLEMENTATION:  ./IMPLEMENTATION_Bleed_Through.md
HEALTH:          ./HEALTH_Bleed_Through.md
SYNC:            ./SYNC_Bleed_Through.md

IMPL:            data/Distributed-Content-Generation-Network/Blood Ledger — The Bleed-Through.md
```

---

## OVERVIEW

Bleed-Through injects cross-world ghosts, rumors, and reports into local canon without violating safety locks. The algorithm selects a candidate, transposes identifiers, and writes a low-truth narrative artifact with provenance so downstream systems can surface it without pretending it is canonical history.

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

## ALGORITHM: Generate_Bleed_Through

Primary function name: `Generate_Bleed_Through`

1. Identify eligible scars or rumors from the source world.
2. Transpose identifiers and strip direct memory.
3. Inject as low-truth narratives in the destination world.
4. Apply safety locks and provenance metadata.

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
    set truth_value = LOW
ELSE:
    set truth_value = MEDIUM
```

---

## DATA FLOW

Source world candidate -> transposition -> low-truth artifact -> local narrative surface -> report delivery.

---

## COMPLEXITY

Selection and transposition are `O(n)` over candidate lists. Injection and report write costs scale with the number of artifacts created per tick.

---

## HELPER FUNCTIONS

- `select_candidate(context)` — filters ghost/rumor candidates by relevance.
- `transpose_identity(entity)` — maps identifiers and traits to local-safe equivalents.
- `write_bleed_artifact(payload)` — persists low-truth narrative nodes/links.

---

## INTERACTIONS

- Scavenger indices provide candidate pools.
- Shadow feed contributes rumor events.
- Canon locks gate injection into local narratives.

---

## GAPS / IDEAS / QUESTIONS

- Gap: report delivery channel (email vs. in-game) is not finalized.
- Idea: add a bleed-through visibility threshold per region.
- Question: should ghosts decay over time or remain as permanent scars?

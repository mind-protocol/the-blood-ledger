# Canon Holder — Patterns

```
UPDATED: 2025-12-19
STATUS: CANONICAL
```

---

## Overview

Canon Holder is the **single point of truth** for what has happened in the game world. No moment reaches the player without passing through it.

This document explains WHY Canon Holder exists and the design philosophy behind it.

---

## Core Design Principle: Single Gatekeeper

**Problem:** Multiple systems create moments (Narrator, World Runner, click handler). Without coordination:
- Moments could be spoken out of order
- THEN links could be inconsistent
- SSE broadcasts could race
- Time could advance inconsistently

**Solution:** All paths converge to one function: `record_to_canon()`.

```
Narrator ──────┐
               │
World Runner ──┼──→ Canon Holder ──→ Player sees moment
               │
Click Handler ─┘
```

---

## Why This Shape

### 1. Separation of Creation vs Recording

**Moments are created** by:
- Narrator (generates response moments)
- World Runner (processes tension flips)
- Graph traversal (click activates linked moment)

**Moments are recorded** by:
- Canon Holder (only)

This separation means:
- Creators don't need to know about SSE, time, strength mechanics
- Recording logic lives in one place
- Easy to add new creators without touching recording

### 2. Graph-First, Not Queue-Based

Moments exist in the graph with `status='active'` before being spoken. Canon Holder doesn't maintain a separate queue—it queries the graph.

**Why:**
- Graph is source of truth
- No sync issues between queue and graph
- Can inspect pending moments via graph queries
- Recovery is simple: re-query active moments

### 3. Energy Cost at Recording

When a moment becomes spoken, it pays 60% energy cost (`energy *= 0.4`).

**Why at recording, not creation:**
- Created moments are *potential*—they haven't happened yet
- Energy cost represents the "actualization" of potential into reality
- Keeps weight (importance) separate from energy (activation)

### 4. THEN Links Form History

Each spoken moment links to the previous via `THEN` edge.

**Why:**
- Enables history traversal ("what led to this moment?")
- `player_caused` flag distinguishes player-driven vs auto-triggered
- Forms a chain that IS the story

---

## Integration Pattern: Option A (Integrated)

Canon Holder is a **function called by systems**, not a separate service.

```python
# In orchestrator.py
narrator_output = narrator.generate(...)
for moment in narrator_output.moments:
    canon_holder.record_to_canon(moment, speaker, previous)
```

**Why integrated over service:**
- Simpler mental model
- No inter-process coordination
- Easier to debug
- Service would add latency

**When to consider service:**
- If recording becomes a bottleneck
- If multiple processes need to record concurrently
- If decoupling is needed for scaling

---

## Why Speaker Resolution is Part of Recording

Speaker is determined at recording time, not creation time.

**Why:**
- Characters might move between creation and speaking
- Presence requirements must be checked at speak time
- Allows moments to be "waiting for speaker"

---

## Invariants This Design Enforces

1. **Total ordering:** THEN links form a chain, not a tree
2. **Causality:** Every spoken moment links to its predecessor
3. **Presence:** Dialogue moments require present speaker
4. **Energy conservation:** Speaking costs energy
5. **Notification:** Every recording triggers SSE

---

## What Canon Holder Does NOT Do

| Not Responsible For | Who Does It |
|--------------------|-------------|
| Creating moments | Narrator, World Runner |
| Deciding what to create | Narrator's prompt, flip logic |
| Weight propagation | Tick loop |
| Click handling | MomentTraversal |
| Moment activation | Salience check in tick loop |

Canon Holder is narrow: record what's ready, notify who's listening.

---

## Chain

- **PATTERNS: This file**
- BEHAVIORS: `docs/infrastructure/canon/BEHAVIORS_Canon.md`
- ALGORITHM: `docs/infrastructure/canon/ALGORITHM_Canon_Holder.md`
- VALIDATION: `docs/infrastructure/canon/VALIDATION_Canon.md`
- IMPLEMENTATION: `docs/infrastructure/canon/IMPLEMENTATION_Canon.md`
- SYNC: `docs/infrastructure/canon/SYNC_Canon.md`

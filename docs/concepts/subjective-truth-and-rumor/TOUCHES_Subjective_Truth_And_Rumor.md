# TOUCHES: Where Subjective Truth & Rumor Appears in the System

```
LAST_UPDATED: 2025-12-19
```

---

## MODULES THAT IMPLEMENT

| Module | What It Does With Subjective Truth |
|--------|------------------------------------|
| `network/transposition` | Downgrades conflicting beliefs into rumors |
| `network/shadow-feed` | Imports distant events as low-truth rumors |
| `network/bleed-through` | Frames cross-world content as scars and rumors |
| `network/world-scavenger` | Uses rumor layer for safe reuse |
| `infrastructure/canon` | Defines ground truth that subjective truth cannot override |

---

## INTERFACES

### network/transposition

**Functions:**
- `transpose_entity()` — resolves conflicts and fuzzes beliefs

**Relevant docs:**
- `docs/network/transposition/PATTERNS_Local_Canon_Primary.md`

### network/shadow-feed

**Functions:**
- `import_distant_event()` — converts events into rumors

**Relevant docs:**
- `docs/network/shadow-feed/PATTERNS_Shadow_Feed_Rumor_Cache.md`

---

## DEPENDENCIES

How the concept flows through modules:

```
canon (defines truth)
         ↓
transposition (fuzzes conflicts)
         ↓
shadow-feed (imports rumors)
         ↓
bleed-through (player-facing framing)
```

---

## INVARIANTS ACROSS MODULES

- **I1:** Canon is immutable; subjective truth cannot overwrite it.
- **I2:** Rumors default to low truth (<= 0.3) unless verified locally.

---

## CONFLICTS / TENSIONS

- Potential tension between "no multiverse" rule and cross-world rumor framing.

---

## SYNC

```
LAST_VERIFIED: 2025-12-19
ALL_MODULES_ALIGNED: PARTIAL
CONFLICTS: Multi-world framing vs single-reality narrative needs clear copy guardrails.
```

---

## WHEN TO UPDATE THIS FILE

Update TOUCHES when:
- New modules use subjective truth or rumor mechanics
- Canon/rumor rules change
- New interfaces are added

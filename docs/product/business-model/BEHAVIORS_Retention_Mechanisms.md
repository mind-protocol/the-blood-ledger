# BEHAVIORS: Business Model Behaviors (Retention, Conversion, Unit Economics)

## Observable Effects

This document captures the observable behaviors for the Blood Ledger business model:
retention drivers, the conversion funnel and Ledger Lock, and unit economics signals.

## Retention Mechanisms

### Retention Mechanism 1: The Growing Graph

*   **Behavior:** As a player invests time, their personal "Graph" of relationships, events, and lore expands significantly. This graph is treated as a unique, valuable asset built by the player.
*   **System Response:** The game displays the increasing complexity and detail of this graph (e.g., from 50 nodes to 3,000+ nodes, encompassing regional history, political factions, and multi-generational family trees).
*   **Player Psychology:** Leaving the game means abandoning this highly personalized and detailed world-state, akin to a sunk cost, making retention significantly higher.

### Retention Mechanism 2: The Chronicle Promise

*   **Behavior:** Every hour of gameplay contributes to the player's eventual "Life Chronicle" (a death/ending montage).
*   **System Response:** The game implicitly and explicitly links continued play to the richness and length of this ultimate narrative artifact.
*   **Player Psychology:** Players are motivated to continue playing to see what their full "Life Chronicle" will look like after many hours, or how their character will ultimately die, creating a goal they build towards from minute one.

### Retention Mechanism 3: The Multi-Life Model

*   **Behavior:** Upon character death or story completion, players can start a new life in the *same persistent world*, often as a descendant.
*   **System Response:** The world remembers previous lives. NPCs react based on the legacy of previous characters, and past actions (lies, debts) become starting conditions for the new playthrough.
*   **Player Psychology:** Each life offers a fresh perspective and new challenges within an evolving, familiar world, providing infinite replayability and continuous discovery.

### Retention Mechanism 4: The "Missed Events" Drive

*   **Behavior:** Chronicles (especially Life Chronicles) reveal significant off-screen events that occurred during the player's absence or in parallel.
*   **System Response:** The game uses these revelations to demonstrate the world's persistence and complexity.
*   **Player Psychology:** This generates curiosity and a desire to explore more, understand what else was missed, and engage more deeply with the world.

## Churn Prevention Triggers

The system monitors player behavior and intervenes with targeted nudges to prevent churn.

| Signal | Detection | Intervention |
|--------|-----------|--------------|
| Session frequency drops | <2 sessions in 7 days | Email: "The world moved while you were away. Wulfric made a decision." |
| Average session shortens | <20 mins for 3 sessions | In-game: Voice whispers something intriguing they haven't explored |
| Graph exploration slows | Same 5 NPCs for 10 sessions | Introduce mystery: "A stranger arrived asking about you by name." |
| Payment declines | CC failed | 7-day grace period, "read-only" mode, save their world |

## Conversion Funnel and Ledger Lock

### The Death Zone: Steam -> Stripe
*   **Behavior:** A player downloads the free game on Steam, plays for a period, and then encounters a paywall, requiring them to register payment information via an external Stripe link.
*   **Risk:** High drop-off (estimated 70-90%) at this stage.
*   **Intent:** This high friction is intentional and serves as a filter. The players who convert are those most invested and most likely to become high-value whales. The goal is whale identification, not mass conversion.

### The "Hook" Moment Design: The Ledger Lock

*   **Trigger:** After approximately 45 minutes of free play (during which the player has made meaningful choices, accumulated Ledger entries, developed relationships, and asked world-building questions), the Ledger Lock is triggered when the player attempts to SAVE or CLOSE the game.
*   **System Response:** A popup appears, framing payment not as a cost for access, but as a means to preserve the history and progress they have already created.
    ```
    "The Ledger remembers 12 moments you've lived.

    Aldric believes you saved his brother.
    Wulfric's debt grows heavier each day.
    The lie you told in Stamford still echoes.

    Without a Chronicle, these moments fade.
    The world forgets. You become no one.

    [Secure Your Chronicle]  [Let It Fade]"
    ```
*   **Psychology:** This leverages the sunk cost fallacy and emotional investment. Players are paying to keep what they've built, not for more game.

### The Bridge UX

*   **Option A: QR Code (Recommended for Steam)**
    *   Player clicks "Secure Your Chronicle."
    *   Game generates a unique session token and displays a QR code.
    *   Player scans the QR code with their phone, leading to Stripe Checkout (leveraging pre-saved payment methods like Apple Pay/Google Pay for a 2-tap process).
    *   Game detects payment via webhook and seamlessly continues play.
*   **Option B: Magic Link (For Desktop-only players)**
    *   Player enters email, receives a unique link.
    *   Clicking the link opens Stripe Checkout in a browser.
    *   Game polls for payment completion and notifies in-game.

### Funnel Metrics to Track

| Stage | Metric | Target | Red Flag |
|-------|--------|--------|----------|
| Download | Steam downloads | 1,000/month | <200 |
| Play | Start session | 70% of downloads | <50% |
| Hook | Reach Ledger Lock | 60% of sessions | <40% |
| Convert | Complete payment | 15% of hooks | <5% |
| Retain | Active Month 2 | 70% of converts | <50% |

## Unit Economics Signals

Status: DRAFT (needs verification against the source business model stress test data).

### B1: Average margin remains >75%

```
GIVEN:  a month of typical usage
WHEN:   costs are calculated
THEN:   gross margin remains above 75%
```

### B2: Grandmother queries remain profitable

```
GIVEN:  frequent worldbuilder queries
WHEN:   costs are aggregated
THEN:   the margin remains positive after caching
```

### B3: Hallucination defense prevents canon break

```
GIVEN:  AI proposes actions
WHEN:   physics rejects them
THEN:   output reflects rejection rather than hallucination
```

### Inputs / Outputs

#### Primary Function: `calculate_margin()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| interaction_mix | object | Distribution of moment types |
| pricing | object | Per-moment pricing |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| margin | float | Gross margin percentage |

**Side Effects:**

- None

### Edge Cases

#### E1: Whale spamming expensive queries

```
GIVEN:  high volume of worldbuilder calls
THEN:   margin remains > 60% after caching
```

### Anti-Behaviors

#### A1: Hidden cost spikes

```
GIVEN:   large context windows
WHEN:    usage increases
MUST NOT: exceed margin thresholds without alerts
INSTEAD: trigger cost monitoring
```

### Gaps / Ideas / Questions

- [ ] Define live margin dashboards
- [ ] Define automatic pricing adjustments
- IDEA: Add per-tier cost caps to protect margins

## Maturity

STATUS: CANONICAL
NOTE: Unit economics signals are draft content pending verification.

---

## CHAIN

PATTERNS:        ./PATTERNS_Whale_Economics.md
MECHANISMS:      ./MECHANISMS_Margin_Defense.md
ALGORITHM:       ./ALGORITHM_Semantic_Cache.md
ALGORITHM:       ./ALGORITHM_Hallucination_Defense.md
ALGORITHM:       ./ALGORITHM_World_Scavenger.md
VALIDATION:      ./VALIDATION_Business_Model_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Business_Model.md
TEST:            ./TEST_Business_Model.md
PATTERNS:        ./PATTERNS_Market_Comparison.md
THIS:            ./BEHAVIORS_Retention_Mechanisms.md
SYNC:            ./SYNC_Business_Model.md

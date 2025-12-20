# BEHAVIORS: Conversion Funnel and Ledger Lock

## Observable Effects

This document describes the intended player behaviors and system responses within the Blood Ledger's monetization conversion funnel, focusing on the critical "Ledger Lock" mechanism. The funnel is intentionally designed to filter for "whales" by introducing friction at a strategic moment.

## The Conversion Funnel

### The Death Zone: Steam → Stripe
*   **Behavior:** A player downloads the free game on Steam, plays for a period, and then encounters a paywall, requiring them to register payment information via an external Stripe link.
*   **Risk:** High drop-off (estimated 70-90%) at this stage.
*   **Intent:** This high friction is *intentional* and serves as a filter. The players who convert are those most invested and most likely to become high-value "whales." The goal is whale identification, not mass conversion.

### The "Hook" Moment Design: The Ledger Lock

*   **Trigger:** After approximately 45 minutes of free play (during which the player has made meaningful choices, accumulated Ledger entries, developed relationships, and asked world-building questions), the "Ledger Lock" is triggered when the player attempts to SAVE or CLOSE the game.
*   **System Response:** A popup appears, framing payment not as a cost for access, but as a means to "preserve" the history and progress they have already created.
    ```
    "The Ledger remembers 12 moments you've lived.        

    Aldric believes you saved his brother.                
    Wulfric's debt grows heavier each day.               
    The lie you told in Stamford still echoes.           

    Without a Chronicle, these moments fade.             
    The world forgets. You become no one.                

    [Secure Your Chronicle]  [Let It Fade]"              
    ```
*   **Psychology:** This leverages the sunk cost fallacy and emotional investment. Players are paying to KEEP what they've built, not for "more game." The threat of their story vanishing acts as a powerful motivator.

### The Bridge UX

Designed to minimize friction in the payment process for those who choose to convert.

*   **Option A: QR Code (Recommended for Steam)**
    *   Player clicks "Secure Your Chronicle."
    *   Game generates a unique session token and displays a QR code.
    *   Player scans the QR code with their phone, leading to Stripe Checkout (leveraging pre-saved payment methods like Apple Pay/Google Pay for a 2-tap process).
    *   Game detects payment via webhook and seamlessly continues play.
*   **Option B: Magic Link (For Desktop-only players)**
    *   Player enters email, receives a unique link.
    *   Clicking the link opens Stripe Checkout in a browser.
    *   Game polls for payment completion and notifies in-game.

## Funnel Metrics to Track

Key metrics for monitoring the funnel's performance, prioritizing ARPU over raw conversion rates.

| Stage | Metric | Target | Red Flag |
|-------|--------|--------|----------|
| Download | Steam downloads | 1,000/month | <200 |
| Play | Start session | 70% of downloads | <50% |
| Hook | Reach Ledger Lock | 60% of sessions | <40% |
| Convert | Complete payment | 15% of hooks | <5% |
| Retain | Active Month 2 | 70% of converts | <50% |

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Whale_Economics.md
ALGORITHM:       ./ALGORITHM_Semantic_Cache.md
ALGORITHM:       ./ALGORITHM_Hallucination_Defense.md
ALGORITHM:       ./ALGORITHM_World_Scavenger.md
BEHAVIORS:       ./BEHAVIORS_Retention_Mechanisms.md
PATTERNS:        ./PATTERNS_Market_Comparison.md
THIS:            ./BEHAVIORS_Conversion_Funnel_And_Ledger_Lock.md
SYNC:            ./SYNC_Business_Model.md

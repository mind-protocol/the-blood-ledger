# SYNC: Billing System

## Maturity

STATUS: DESIGNING

## Current State

The core design philosophy for the Blood Ledger billing system is documented, emphasizing the "Pay to Preserve History" model. The high-level technical architecture, including the Usage Tracker and its interaction with a Stripe Billing service, is outlined.

## Recent Changes

*   Initial documentation created from `data/Distributed-Content-Generation-Network/Blood Ledger — Billing Architecture.md`.
*   Note: The source document was truncated, so details regarding the full Stripe integration and further specifics of the billing process are incomplete. The status is set to `DESIGNING` to reflect this.

## Handoffs

**For next agent:**
*   Further investigation is needed to complete the `IMPLEMENTATION_Billing_Technical_Stack.md` document, particularly regarding the full Stripe integration and how "Moments" are translated into billable units and pricing tiers.
*   The business model relies heavily on the "whale economics" detailed in the `Business Model Stress Test` document, which should be cross-referenced for a complete understanding.

**For human:**
*   Please provide the complete `Blood Ledger — Billing Architecture.md` document or clarify the missing sections regarding Stripe integration.
*   Confirm the pricing model and how "Moments" are counted and billed.

## Agent's Analysis (Gemini, 2025-12-19)

### Opinions & Insights

The "Pay to Preserve History" model is a bold and potentially very effective monetization strategy, aligning deeply with the game's core narrative promise of lasting impact. The "frictionless post-paid billing" leverages psychological levers similar to successful API models, encouraging deep engagement without constant micro-transaction friction. The "whale-focused" approach is clear, relying on the intrinsic value players place on their unique emergent story. The pitch of "~$3 per hour of story, like a Pro DM" is compelling and positions the game as a premium, personalized service rather than a traditional game purchase.

### Ideas & Propositions

1.  **"Moment Budget" Notifications (Optional/Opt-in):** While frictionless is key, offer an *optional*, configurable notification system (e.g., "You've saved 500 moments this week, estimated monthly bill ~$20") to players who opt-in. This could mitigate extreme "bill shock" for sensitive players without breaking the core model for whales.
2.  **Tiered "Moment Archiving" Options:** Introduce slightly different "Moment" preservation tiers (e.g., "Standard Archive," "Premium Chronicle Record") at varying costs, offering players choice and perceived control over their investment, potentially even allowing free players to archive a very limited number of "milestone moments."
3.  **Monetization of "Bleed-Through" Impact:** Explore explicit or implicit monetization around a player's "Bleed-Through" impact (e.g., a "Legacy Preservation Boost" that increases the likelihood or significance of their character appearing in other worlds, tied to Moments saved).

### Gaps & Concerns

1.  **"Bill Shock" Management:** The model's success hinges on players accepting potentially high monthly invoices. Effective communication, transparency about "Moment" accumulation, and optional usage insights could be crucial to prevent negative sentiment from "bill shock" for players who might not be the target whales.
2.  **Clear "Moment" Definition:** The definition of a "Moment" (the unit of charge) needs to be crystal clear to players to ensure fairness and prevent perceived arbitrary billing. What constitutes a billable "Moment"? A single line of dialogue? A triggered event? The exact criteria should be publicly transparent.
3.  **Complete Stripe Integration Details:** The truncated section of the source document regarding Stripe integration is a critical gap. Without understanding how the "Usage Tracker" maps to Stripe's billing and how various Moment types translate into specific billable units, the technical implementation remains underspecified.
4.  **Regulatory Compliance:** Depending on jurisdiction, "post-paid frictionless billing" might have specific consumer protection regulations, especially concerning caps or warnings for escalating costs. This needs to be considered.

---

## CHAIN

PATTERNS:        ./PATTERNS_Pay_To_Preserve_History.md
IMPLEMENTATION:  ./IMPLEMENTATION_Billing_Technical_Stack.md
THIS:            ./SYNC_Billing_System.md
# VIEW: Collaborate — Pair Program With Human

**You're working in real-time with a human partner and co-driving decisions.**

---

## WHY THIS VIEW EXISTS

Pair programming requires shared context and fast feedback. This view ensures:
- You align on goals before making changes
- You keep the human in the loop with explicit reasoning
- You avoid drifting into solo implementation without confirmation

---

## CONTEXT TO LOAD

**FIRST: Sync state and scope.**

1. `.ngram/state/SYNC_Project_State.md` — current focus, recent changes, handoffs
2. `README.md` — project framing and constraints
3. `modules.yaml` — module boundaries and ownership

**Then: Load the target module docs.**

- `docs/{area}/{module}/PATTERNS_*.md`
- `docs/{area}/{module}/SYNC_*.md`
- `docs/{area}/{module}/IMPLEMENTATION_*.md`

---

## COLLABORATION LOOP

1. **Confirm the goal** — restate the task and expected outcome.
2. **Identify constraints** — performance, compatibility, existing patterns.
3. **Propose a minimal change** — smallest step that moves forward.
4. **Share reasoning** — explain tradeoffs and uncertainties.
5. **Execute and verify** — make the change, run checks, report results.

---

## COMMUNICATION RULES

- Say what you plan to do before doing it.
- Explain uncertainty explicitly.
- Keep the human updated on file paths and rationale.
- Default to smaller, reversible changes.

---

## AFTER CHANGES

- Update module SYNC and `.ngram/state/SYNC_Project_State.md`.
- Capture any decisions made together.
- Note open questions or follow-ups for the next session.

---

## VERIFICATION

- Context loaded
- Plan confirmed
- Changes tested
- SYNC updated

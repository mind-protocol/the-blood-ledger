# Vision — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
```

---

## Current State

Vision documentation complete (draft). Full protocol chain created:

| Document | Content | Status |
|----------|---------|--------|
| PATTERNS_Vision.md | Design philosophy, principles, market validation (CK3 insights) | Draft |
| BEHAVIORS_Vision.md | Player experience, arc, Octalysis drives, anti-patterns | Draft |
| ALGORITHM_Vision.md | Systems that create behaviors, dependencies, priority | Draft |
| VALIDATION_Vision.md | Testing approach, POC milestones, ultimate test | Draft |
| IMPLEMENTATION_Vision.md | Documentation architecture, file responsibilities, data flow | Draft |

All documents ready for validation.

### 2025-12-19 Update
- Fixed broken file references in `docs/design/IMPLEMENTATION_Vision.md` by listing concrete paths and removing placeholder target filenames so link validation resolves cleanly.
- Verified the remaining implementation doc references resolve to existing vision/opening/scenarios files for the BROKEN_IMPL_LINK repair.

---

## What's Been Established

### Confirmed
- **One-sentence pitch:** Real relationships that matter — people who remember and act accordingly
- **Player fantasy:** Start small → adventure → become lord (through people, not points)
- **Reference points:** Game of Thrones, Crusader Kings 3, The Expanse
- **Core risk:** Engagement in text-heavy medium

### Drafted (Needs Validation)
- Design principles (narratives over mechanics, emergence over scripting, etc.)
- The technical bet (LLM + Graph)
- Player experience arc (fire → road → web thickens → reckoning → lord/grave)
- Engagement levers (voices, brevity, stakes, rhythm, images)
- Validation approach (POC milestones, red flags, ultimate test)

---

## Answered Questions

1. **Failure states.** Yes, you can die. Death is final. Future: "restart from 10 days before" via DB snapshots.
2. **Session length.** Potentially infinite. No artificial boundaries.
3. **Replayability.** Yes. Full vision is "anyone, anywhere, anytime" — currently constrained to Norman England 1067.
4. **Scope control.** Ship V1 soon. Learn from reality.
5. **Multiplayer.** Not for V1.

## Clarified Success Metric

**The win condition:** You know companions/enemies well enough to *predict and rely on them*.

- "I'll send Aldric because [specific reasons from relationship]"
- You can ask about grandmother, upbringing, beliefs — and get real answers
- Deep relationships, not surface ones

## Remaining Open Questions

1. **Graph pruning.** How do distant narratives get archived?
2. **Character depth generation.** How do we create backstories rich enough for deep questioning?
3. **Consistency at scale.** How do we maintain character consistency over many sessions?
4. **Image generation scope.** How much? When? What style?

---

## Decisions Needed

| Question | Options | Impact |
|----------|---------|--------|
| Is death possible? | Yes (permadeath) / Yes (with recovery) / No | Affects tension, stakes |
| Single story or replayable? | Single epic / Meant for replay | Affects onboarding, content depth |
| Always text + occasional images / images frequent | Text-primary / Image-heavy | Affects performance, cost, design |

---

## Next Steps

1. **Nicolas validates vision docs** — correct, refine, approve
2. **Define documentation structure for engine** — areas and modules
3. **Create engine module docs** — starting with graph/
4. **Update SYNC_Project_State.md** — reflect actual project state

---

## Handoff Notes

### For Future Agents
- Vision docs are drafts — check if Nicolas has validated/modified
- The pitch is "real relationships that matter"
- The risk is engagement — keep this in mind for all design decisions
- Reference points are GoT, CK3, Expanse

### For Nicolas
- Please review PATTERNS and BEHAVIORS especially
- Note any disagreements with principles or experience goals
- Answer open questions when ready
- Flag anything that feels wrong or missing

---

*Status: Vision drafted, awaiting validation*

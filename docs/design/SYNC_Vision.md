# Vision — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (repair agent)
```

---

## MATURITY

STATUS: DESIGNING

What's canonical (v1):
- Vision doc chain exists and is coherent enough for review and iteration.
- Core pitch and experience framing are drafted for validation.

What's still being designed:
- Final wording and scope after Nicolas reviews open questions.
- Concrete validation steps and acceptance thresholds.

What's proposed (v2):
- Expanded market validation and research annexes in the archive.

---

## CURRENT STATE

Vision documentation complete (draft). Full protocol chain created:

| Document | Content | Status |
|----------|---------|--------|
| PATTERNS_Vision.md | Design philosophy, principles, market validation summary | Draft |
| BEHAVIORS_Vision.md | Player experience, arc, core drives summary, anti-patterns | Draft |
| ALGORITHM_Vision.md | Systems that create behaviors, dependencies, priority | Draft |
| VALIDATION_Vision.md | Testing approach, POC milestones, ultimate test | Draft |
| IMPLEMENTATION_Vision.md | Documentation architecture, file responsibilities, data flow | Draft |

All documents ready for validation, pending human review and decisions.

### 2025-12-19 Update
- Fixed broken file references in `docs/design/IMPLEMENTATION_Vision.md` by listing concrete paths and removing placeholder target filenames so link validation resolves cleanly.
- Verified the remaining implementation doc references resolve to existing vision/opening/scenarios files for the BROKEN_IMPL_LINK repair.

### 2025-12-19 Update (Doc Size Reduction)
- Condensed PATTERNS and BEHAVIORS content to keep core vision concise while preserving intent.
- Archived market validation, Octalysis mapping, and engagement lever details in `docs/design/archive/SYNC_archive_2024-12.md`.
- Updated `docs/design/IMPLEMENTATION_Vision.md` file map and line counts to reflect the reduced docs.
- Ran `ngram validate`; failures remain for pre-existing missing VIEW/doc-chain gaps (schema/product/network/storms/history).

---

## IN PROGRESS

No active drafting sessions at the moment; pending feedback from Nicolas on the
vision chain before further revisions or expansion.

---

## RECENT CHANGES

- 2025-12-19: Added missing BEHAVIORS template sections (CHAIN, behaviors summary, inputs/outputs, edge cases, anti-behaviors, gaps) in `docs/design/BEHAVIORS_Vision.md` for repair #16.
- 2025-12-19: Filled missing SYNC template sections and lengthened entries.
- 2025-12-19: Added missing PATTERNS template sections (chain/problem/pattern/principles/dependencies/inspirations/scope/gaps).
- 2025-12-19: Filled VALIDATION_Vision template sections (chain, invariants, properties, errors, verification) for repair #16.
- 2025-12-19: Expanded validation layer status lines to clarify pending implementation dependencies.
- 2025-12-19: Expanded TEST_Vision sections (strategy, coverage, gaps, run guidance) to resolve doc-template drift for repair #16.
- 2025-12-19: Fixed broken IMPLEMENTATION references and validated the chain.
- 2025-12-19: Condensed PATTERNS/BEHAVIORS content and archived long-form notes.
- 2025-12-19: Updated the file map/line counts in IMPLEMENTATION to match edits.
- 2025-12-19: Added SCHEMA and LOGIC CHAINS sections to the implementation doc and expanded bidirectional link notes.
- 2025-12-19: Verified SYNC template sections meet required headings and length guidance.
- 2025-12-19: Ran `ngram validate`; failures remain for missing VIEW and doc-chain gaps in schema/product/network/storms modules.
- 2025-12-19: Ran `ngram validate`; failures remain pre-existing (missing VIEW file and doc-chain gaps in schema/product/network/storms modules).

---

## KNOWN ISSUES

- Vision docs remain unvalidated by Nicolas; several open questions persist.
- Some repository-wide doc-chain gaps remain outside the design module.

---

## HANDOFF: FOR AGENTS

Likely VIEW: `VIEW_Implement_Write_Or_Modify_Code.md`

Focus: Keep vision docs stable until human review lands; avoid introducing new
sections without a validated need.

Watchouts: Align any edits with the archived notes to avoid reintroducing drift.

---

## HANDOFF: FOR HUMAN

Executive summary: Vision docs are drafted and trimmed; ready for review and
approval with open questions listed below.

Decisions needed: Confirm death/replayability/image scope and the validation
thresholds before implementation moves forward.

---

## TODO

- [ ] Confirm vision wording, scope, and the core win condition phrasing.
- [ ] Resolve open questions in this SYNC and update the archive if needed.
- [ ] Re-run `ngram validate` after any edits that change doc links.

---

## CONSCIOUSNESS TRACE

Awareness: The vision documentation feels coherent but still fragile without
human sign-off; restraint is important until feedback lands.

Uncertainty: The engagement risk and image scope remain the biggest unknowns,
and should be treated as validation priorities.

---

## POINTERS

- `docs/design/PATTERNS_Vision.md` for design intent and scope.
- `docs/design/BEHAVIORS_Vision.md` for player experience details.
- `docs/design/archive/SYNC_archive_2024-12.md` for pruned research notes.

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

---

## Agent Observations

### Remarks
- The BEHAVIORS doc now includes explicit template sections so drift checks can validate the structure without altering the underlying vision.
- The vision docs now fit the size threshold while keeping the core experience narrative intact.

### Suggestions
- [ ] Review the condensed Key Experience Moments list to ensure no critical moments were removed.
- [ ] Confirm the archive summary is sufficient for future reference before further pruning.

### Propositions
- Keep future additions to BEHAVIORS in short lists or tables to avoid re-growth past thresholds.

### 2025-12-19 Update (Docs size reduction)
- Condensed market validation and Octalysis content in vision docs to reduce size while preserving core intent.
- Added `docs/design/archive/SYNC_archive_2024-12.md` to retain removed detail.
- Trimmed ALGORITHM scope notes to high-level mapping and updated file responsibilities.
- Ran `ngram validate`; failures remain for missing VIEW/doc-chain gaps outside docs/design.

---

## Agent Observations

### Remarks
- The vision docs had overlapping rationale and validation detail; trimming helped reduce redundancy without changing intent.
- The implementation doc now captures schema expectations and logic flows for the vision documentation chain.
- Validation layer status lines now spell out which implementation pieces are required before testing.
- PATTERNS_Vision now includes the full template headings to prevent drift warnings.

### Suggestions
- [ ] Consider moving any future long-form research quotes directly into the archive to keep the vision docs concise.

### Propositions
- None.

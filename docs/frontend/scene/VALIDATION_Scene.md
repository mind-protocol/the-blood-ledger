# Scene View — Validation

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Scene.md
BEHAVIORS:   ./BEHAVIORS_Scene.md
ALGORITHM:   ./ALGORITHM_Scene.md
THIS:        VALIDATION_Scene.md (you are here)
TEST:        ./TEST_Scene.md
SYNC:        ./SYNC_Scene.md
```

---

## INVARIANTS

### V1: People Row Reflects Scene Hotspots
Only `scene.hotspots` with `type === 'person'` appear in the people row,
and the row is omitted entirely when no person hotspots exist.

### V2: Voices Are Sorted, Capped, and Weighted Visually
Voices are sorted by `weight`, capped at four entries, and rendered with
opacity scaled by `0.5 + weight * 0.5` to preserve ranking clarity.

### V3: Actions Always Include Travel and Write
The action bar always renders Travel and Write buttons, with one Talk
button per person hotspot; there is no state where actions disappear.

### V4: Banner Always Renders with a Fallback
If `scene.bannerImage` is missing, the banner still renders using a
type-based gradient, with a default ROAD gradient for unknown types.

---

## PROPERTIES

- P1: The banner image cache-buster updates on banner changes to avoid stale
  assets without requiring a full page refresh.
- P2: Portraits always render with a square frame; missing images fall back
  to the provided icon so the row still conveys identity.
- P3: Voices display is optional but visually separated by a label and
  spacing so the absence of voices does not collapse the layout.

---

## ERROR CONDITIONS

### E1: Missing Banner Image
```
WHEN:    scene.bannerImage is empty or undefined
THEN:    render gradient fallback and still show scene type label
SYMPTOM: No broken image icon; layout remains stable
```

### E2: Empty People List
```
WHEN:    scene.hotspots contains no person entries
THEN:    omit the people section entirely
SYMPTOM: Scene still renders header, banner, voices, and actions
```

### E3: Unknown Scene Type
```
WHEN:    scene.type does not match a defined gradient key
THEN:    use ROAD gradient fallback to avoid blank banner styling
SYMPTOM: Banner renders with neutral slate gradient
```

---

## TEST COVERAGE

- No automated tests exist for the scene components yet; coverage is manual.
- Planned Playwright and component tests are listed in `./TEST_Scene.md`.
- TypeScript compile checks apply but do not verify scene layout logic.

---

## VERIFICATION PROCEDURE

- `cd frontend && npm run dev` and load the main scene view.
- Use a scene with and without `bannerImage` to verify fallback gradients.
- Confirm voices are sorted by weight and capped at four entries.
- Confirm person hotspots create Talk buttons and portraits.

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_BY: ngram repair agent
RESULT: Documentation updated for template completeness; UI verification not run in this repair.
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add component tests for SceneView and SceneBanner fallback behavior.
- [ ] Add Playwright coverage for action button presence and voice ordering.
- IDEA: Document a scene fixture with missing fields to test resilient rendering.
- QUESTION: Should voice opacity be clamped to avoid overly faint text?

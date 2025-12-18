# Image Generation — Behaviors

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Image_Generation.md
THIS:        BEHAVIORS_Image_Generation.md (you are here)
ALGORITHM:   ./ALGORITHM_Image_Generation.md
VALIDATION:  ./VALIDATION_Image_Generation.md
TEST:        ./TEST_Image_Generation.md
SYNC:        ./SYNC_Image_Generation.md
```

---

### B1: Deterministic Prompts
```
GIVEN:  A node specifies `image_prompt`
WHEN:   Image generation runs
THEN:   The prompt template expands with canonical style tokens (resolution, film grain) for reproducibility
```

### B2: File Placement
```
GIVEN:  A character/place/thing image is generated
WHEN:   The job succeeds
THEN:   File lands under `frontend/public/playthroughs/{pt}/images/{type}/{id}.png`
```

### B3: Graph Attachment
```
GIVEN:  An image path exists
WHEN:   GraphOps finishes
THEN:   The node receives `image_path` + `image_generated_at` fields
```

### B4: Failure Logging
```
GIVEN:  External API errors or moderation blocks occur
WHEN:   Generation fails
THEN:   A warning is logged with guidance; pipeline continues without crashing
```
```

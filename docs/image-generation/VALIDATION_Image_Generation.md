# Image Generation — Validation

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Image_Generation.md
BEHAVIORS:   ./BEHAVIORS_Image_Generation.md
ALGORITHM:   ./ALGORITHM_Image_Generation.md
THIS:        VALIDATION_Image_Generation.md (you are here)
TEST:        ./TEST_Image_Generation.md
SYNC:        ./SYNC_Image_Generation.md
```

---

## Invariants

1. **File Exists** — Generated path exists and is non-empty.
2. **Graph Sync** — Node `image_path` matches filesystem path.
3. **Prompt Traceability** — Metadata records the final prompt string + seed.
4. **Retry Exhaustion** — Failures after retries raise descriptive exceptions.

Manual verification: run `python tools/image_generation/generate_image.py --test char_aldric` and inspect output.

# Image Generation — Health: Pipeline Verification

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers the image generation CLI pipeline. It exists to catch
failures where images are generated but not saved or surfaced. It does not
verify prompt quality.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Image_Generation.md
BEHAVIORS:       ./BEHAVIORS_Image_Generation.md
ALGORITHM:       ./ALGORITHM_Image_Generation.md
VALIDATION:      ./VALIDATION_Image_Generation.md
IMPLEMENTATION:  ./IMPLEMENTATION_Image_Generation.md
THIS:            HEALTH_Image_Generation.md
SYNC:            ./SYNC_Image_Generation.md

IMPL:            tools/image_generation/generate_image.py
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: image_generation_output
    flow_id: image_generation
    priority: high
    rationale: Generated assets must land in the expected output path.
```

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: manual
  result:
    representation: enum
    value: UNKNOWN
    updated_at: 2025-12-20T00:00:00Z
    source: image_generation_output
```

---

## HOW TO RUN

```bash
# Manual: dry-run to verify prompt expansion and output path
python3 tools/image_generation/generate_image.py --dry-run --type place --id place_example
```

---

## KNOWN GAPS

- [ ] No automated check validates image file persistence.

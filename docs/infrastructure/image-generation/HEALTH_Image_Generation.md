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

IMPL:            tools/health/check_image_generation.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC. Run HEALTH checks at throttled rates.

@ngram:done: Implemented image generation health checker
Implement `tools/health/check_image_generation.py` checker script that:
- Executes dock-based verification against VALIDATION criteria for image pipeline
- Updates `status.result.value` in this file
- Runs throttled (max 1/hour in production)
- Integrates with `ngram doctor` for aggregated reporting

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

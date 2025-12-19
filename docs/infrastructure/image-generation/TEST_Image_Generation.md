# Image Generation — Tests

```
CREATED: 2024-12-17
STATUS: TODO
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Image_Generation.md
BEHAVIORS:   ./BEHAVIORS_Image_Generation.md
ALGORITHM:   ./ALGORITHM_Image_Generation.md
VALIDATION:  ./VALIDATION_Image_Generation.md
THIS:        TEST_Image_Generation.md (you are here)
IMPLEMENTATION: ./IMPLEMENTATION_Image_Generation.md
SYNC:        ./SYNC_Image_Generation.md
```

---

## Planned Suites

| Test | Target | Description |
|------|--------|-------------|
| `tests/tools/test_generate_image.py` | CLI wrapper | Ensures prompts expand + files saved |
| `tests/tools/test_graphops_images.py` | GraphOps integration | Confirms image metadata persisted |
| `tests/tools/test_retry_policy.py` | Error handling | Simulates API failure + retry log |

---

Manual QA: run CLI with `--dry-run` to inspect prompt before hitting API.

# Image Generation — Algorithm

```
CREATED: 2024-12-17
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:    ./PATTERNS_Image_Generation.md
BEHAVIORS:   ./BEHAVIORS_Image_Generation.md
THIS:        ALGORITHM_Image_Generation.md (you are here)
VALIDATION:  ./VALIDATION_Image_Generation.md
IMPLEMENTATION: ./IMPLEMENTATION_Image_Generation.md
TEST:        ./TEST_Image_Generation.md
SYNC:        ./SYNC_Image_Generation.md
```

---

1. **Prompt Assembly**
   - Determine stable diffusion preset (character portrait, setting strip, object icon)
   - Merge node-provided `image_prompt` with style template
2. **Invocation**
   - Call `tools/image_generation/generate_image.py`
   - Provide `playthrough`, `name`, `image_type`
3. **Storage**
   - ensure directories exist under `frontend/public/playthroughs/{playthrough}/images/{subdir}`
   - Save PNG file + metadata JSON if needed
4. **Graph Update**
   - Write `image_path`, `image_prompt`, `image_generated_at` to node
   - Optionally attach `image_seed`
5. **Retry Policy**
   - Up to 2 retries for transient network issues, exponential backoff (1s, 3s)
6. **Cleanup**
   - Remove temporary files older than 7 days
```

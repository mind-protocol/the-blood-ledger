# SYNC: Image Generation

## Status

**STATUS: DESIGNING**

## CHAIN

```
PATTERNS:       ./PATTERNS_Image_Generation.md
BEHAVIORS:      ./BEHAVIORS_Image_Generation.md
ALGORITHM:      ./ALGORITHM_Image_Generation.md
VALIDATION:     ./VALIDATION_Image_Generation.md
IMPLEMENTATION: ./IMPLEMENTATION_Image_Generation.md
TEST:           ./TEST_Image_Generation.md
THIS:           SYNC_Image_Generation.md (you are here)
```

## Recent Changes

- 2025-12-21: Moved image generation defaults into `tools/image_generation/config.py` and added env overrides.

## What's Canonical (v2)

- Ideogram 3.0 API integration via `tools/image_generation/generate_image.py`
- Scene banners at 3:1 aspect ratio
- REALISTIC style type
- **Banners show ONLY locations** — no objects, no characters, no camp equipment
- Objects and characters shown separately in UI
- 8-part prompt structure (see PATTERNS doc)

## What's Working

- Pure location banners (forest clearing, road, hall interior)
- Specific vegetation, time, weather in prompts
- Cinematic quality with 35mm film aesthetic
- Cache-busting on frontend for immediate refresh
- No unwanted furniture/props when using location-only approach

## Approach

**Banner = Stage, not Scene**

The banner shows the empty location. The UI populates it with:
- Characters (CharacterRow component)
- Objects (ObjectRow component)
- Actions, atmosphere, voices

This solves:
- AI adding unwanted items
- Inconsistency with game state
- Narrative problems (2 travelers can't carry elaborate camps)

## Prompt Specifics

Must include:
- Vegetation type (oak, birch, bracken, heather)
- Time of day (dawn, morning, midday, dusk, night)
- Weather (clear, overcast, rain, fog, frost)
- Framing (wide establishing shot, low angle)
- Exclusions ("no fire, no structures, no objects")

## Files

| File | Purpose |
|------|---------|
| `tools/image_generation/generate_image.py` | CLI tool for generation |
| `tools/image_generation/README.md` | Usage documentation |
| `docs/infrastructure/image-generation/PATTERNS_Image_Generation.md` | Prompting guide |
| `frontend/public/playthrough/*/images/` | Generated images |
| `frontend/data/scenes.json` | Scene data |

## Open Questions

1. Auto-generate prompts from scene type + time + weather?
2. Character portrait generation (people allowed — different rules)
3. Regional vegetation mapping (North = oak/heather, South = beech/chalk)

---

## Next Steps

| Task | Owner | Notes |
|------|-------|-------|
| Automate prompt generation from place metadata | Tools | Use place YAML + weather to build the 8-part prompt |
| Hook GraphOps (ngram repo graph runtime) to trigger generation when new place appears | Backend | Tie into Async Architecture Phase 1 |
| Define portrait pipeline | Art | Decide on style + moderation rules for characters |
| Regional vegetation map | Narrative | Map place IDs → vegetation/time defaults |

Update this table when tasks complete or reprioritized.

---

## Recent Changes

- Added IMPLEMENTATION doc and linked CHAIN references for image-generation.
- Added DOCS references in `tools/image_generation/README.md` and prioritized the image-generation doc link in `tools/image_generation/generate_image.py`.
- Replaced the HTML DOCS comment in `tools/image_generation/README.md` with a `# DOCS:` line to standardize the marker; `ngram context` still does not resolve markdown files.
- Simplified the implementation doc code-to-docs reference entry to avoid false broken-link detection.
- Noted in the implementation doc that the code reference column omits the `# DOCS:` marker to prevent broken-link checks from misreading it.
- Updated GraphOps references to call out the ngram repo graph runtime.
- Added `HEALTH_Image_Generation.md` for runtime verification notes.

---

## Last Updated

2025-12-19 — Documented the path-only reference convention in the implementation doc to prevent broken-link checks from misreading `# DOCS:` markers.

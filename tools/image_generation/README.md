# Image Generation Tool

DOCS: docs/infrastructure/image-generation/PATTERNS_Image_Generation.md

Generate images for Blood Ledger using the Ideogram 3.0 API.

## Setup

Requires `IDEOGRAM_API_KEY` in `.env` at project root.

## Usage

```bash
python tools/image_generation/generate_image.py --type <type> --prompt "<description>"
```

## Image Types

| Type | Aspect | Description |
|------|--------|-------------|
| `scene_banner` | 16:9 | Atmospheric scene banners (no people) |
| `character_portrait` | 1:1 | Square character portraits |
| `character_portrait_tall` | 3:4 | Tall character portraits |
| `object_icon` | 1:1 | Item/object icons |
| `map_region` | 4:3 | Regional map illustrations |
| `full_map` | 1:1 | World map |

## Examples

### Scene Banner
```bash
python tools/image_generation/generate_image.py \
  --type scene_banner \
  --prompt "A military camp at night. Tents around a fire. Stars through bare branches." \
  --name "camp_night"
```

### Character Portrait
```bash
python tools/image_generation/generate_image.py \
  --type character_portrait \
  --prompt "A weathered Saxon warrior, graying beard, haunted eyes, scarred face" \
  --name "aldric"
```

### With Playthrough
```bash
python tools/image_generation/generate_image.py \
  --type scene_banner \
  --prompt "A stone hall with a long table, firelight, tapestries" \
  --playthrough "game1" \
  --name "hall_council"
```

## Options

| Flag | Description |
|------|-------------|
| `--type, -t` | Image type (default: scene_banner) |
| `--prompt, -p` | Image description (required) |
| `--playthrough` | Playthrough folder (default: "default") |
| `--name, -n` | Output filename (without extension) |
| `--seed, -s` | Random seed for reproducibility |
| `--speed` | FLASH, TURBO, DEFAULT, or QUALITY |
| `--no-save` | Don't save locally, just return URL |
| `--list-types` | Show available image types |

## Output

Images are saved to:
```
frontend/public/playthroughs/<playthrough>/images/<name>.png
```

## Style

All images include a base style prompt for the Blood Ledger aesthetic:
- Dark medieval England 1067
- Muted earth tones, amber firelight
- Painterly illustration style

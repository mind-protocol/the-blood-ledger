import os

API_URL = os.getenv("IDEOGRAM_API_URL", "https://api.ideogram.ai/v1/ideogram-v3/generate")

# Negative prompt to exclude unwanted elements (weak - use explicit exclusions in main prompt)
NEGATIVE_PROMPT = os.getenv(
    "IDEOGRAM_NEGATIVE_PROMPT",
    "people, persons, figures, silhouettes, humans, faces, crowds, soldiers, characters, bodies",
)

# Image type configurations
# Style types: AUTO, GENERAL, REALISTIC, DESIGN
IMAGE_TYPES = {
    "scene_banner": {
        "aspect_ratio": "3x1",
        "style_type": "REALISTIC",
        "description": "3:1 wide atmospheric scene banner (no people)",
    },
    "setting_strip": {
        "aspect_ratio": "1x3",
        "style_type": "REALISTIC",
        "description": "1:3 tall atmospheric setting strip (no people)",
    },
    "character_portrait": {
        "aspect_ratio": "1x1",
        "style_type": "REALISTIC",
        "description": "1:1 character portrait",
    },
    "character_portrait_tall": {
        "aspect_ratio": "3x4",
        "style_type": "REALISTIC",
        "description": "3:4 tall character portrait",
    },
    "object_icon": {
        "aspect_ratio": "1x1",
        "style_type": "DESIGN",
        "description": "1:1 object/item icon",
    },
    "map_region": {
        "aspect_ratio": "4x3",
        "style_type": "REALISTIC",
        "description": "4:3 map region illustration",
    },
    "full_map": {
        "aspect_ratio": "1x1",
        "style_type": "DESIGN",
        "description": "1:1 full world map",
    },
}

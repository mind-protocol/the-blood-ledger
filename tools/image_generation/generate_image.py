#!/usr/bin/env python3
# DOCS: docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md
# DOCS: docs/infrastructure/image-generation/PATTERNS_Image_Generation.md
"""
Image generation tool using Ideogram 3.0 API.

Usage:
    python generate_image.py --type scene_banner --prompt "A medieval camp at night..."
    python generate_image.py --type character_portrait --prompt "A weathered Saxon warrior..."
    python generate_image.py --type scene_banner --prompt "..." --playthrough "my_game" --name "camp_night"
"""

import argparse
import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("IDEOGRAM_API_KEY")
API_URL = "https://api.ideogram.ai/v1/ideogram-v3/generate"

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

# Negative prompt to exclude unwanted elements (weak - use explicit exclusions in main prompt)
NEGATIVE_PROMPT = "people, persons, figures, silhouettes, humans, faces, crowds, soldiers, characters, bodies"


def generate_image(
    prompt: str,
    image_type: str = "scene_banner",
    playthrough: str = "default",
    name: str | None = None,
    seed: int | None = None,
    rendering_speed: str = "DEFAULT",
    magic_prompt: str = "AUTO",
    save: bool = True,
) -> dict:
    """
    Generate an image using Ideogram 3.0 API.

    Args:
        prompt: The image description
        image_type: One of IMAGE_TYPES keys
        playthrough: Playthrough folder name
        name: Optional filename (without extension)
        seed: Optional seed for reproducibility
        rendering_speed: FLASH, TURBO, DEFAULT, or QUALITY
        magic_prompt: AUTO, ON, or OFF
        save: Whether to save the image locally

    Returns:
        dict with url, local_path, seed, and metadata
    """
    if not API_KEY:
        raise ValueError("IDEOGRAM_API_KEY not found in environment")

    if image_type not in IMAGE_TYPES:
        raise ValueError(f"Unknown image type: {image_type}. Valid types: {list(IMAGE_TYPES.keys())}")

    config = IMAGE_TYPES[image_type]

    # Prepare request data
    data = {
        "prompt": prompt,
        "aspect_ratio": config["aspect_ratio"],
        "style_type": config["style_type"],
        "rendering_speed": rendering_speed,
        "magic_prompt": magic_prompt,
        "negative_prompt": NEGATIVE_PROMPT,
    }

    if seed is not None:
        data["seed"] = seed

    headers = {
        "Api-Key": API_KEY,
    }

    print(f"Generating {image_type} image...")
    print(f"Aspect ratio: {config['aspect_ratio']}")
    print(f"Style: {config['style_type']}")

    # API requires multipart/form-data
    # Convert dict to list of tuples for multipart encoding
    files = [(key, (None, str(value))) for key, value in data.items()]

    response = requests.post(
        API_URL,
        headers=headers,
        files=files,
    )

    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")

    result = response.json()

    if not result.get("data"):
        raise Exception("No image data in response")

    image_data = result["data"][0]
    image_url = image_data.get("url")

    if not image_url:
        if not image_data.get("is_image_safe", True):
            raise Exception("Image failed safety check")
        raise Exception("No URL in response")

    output = {
        "url": image_url,
        "seed": image_data.get("seed"),
        "resolution": image_data.get("resolution"),
        "prompt_used": image_data.get("prompt"),
        "style_type": image_data.get("style_type"),
        "image_type": image_type,
    }

    if save:
        # Create output directory
        output_dir = PROJECT_ROOT / "frontend" / "public" / "playthroughs" / playthrough / "images"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        if name:
            filename = f"{name}.png"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{image_type}_{timestamp}.png"

        output_path = output_dir / filename

        # Ensure parent directory exists (for paths like "characters/char_rolf")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Download and save image
        print(f"Downloading image...")
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            print(f"Saved to: {output_path}")
            output["local_path"] = str(output_path)
        else:
            print(f"Warning: Failed to download image: {img_response.status_code}")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Generate images for Blood Ledger using Ideogram 3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Image Types:
  scene_banner          16:9 atmospheric scene (no people)
  character_portrait    1:1 character face
  character_portrait_tall  3:4 character portrait
  object_icon           1:1 item/object icon
  map_region            4:3 map region illustration
  full_map              1:1 world map

Examples:
  %(prog)s --type scene_banner --prompt "A medieval camp at night, tents around a fire"
  %(prog)s --type character_portrait --prompt "A weathered Saxon warrior, graying beard"
  %(prog)s --type scene_banner --prompt "..." --playthrough "game1" --name "camp_night"
        """
    )

    parser.add_argument(
        "--type", "-t",
        choices=list(IMAGE_TYPES.keys()),
        default="scene_banner",
        help="Image type (default: scene_banner)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required="--list-types" not in sys.argv,
        help="Image description"
    )
    parser.add_argument(
        "--playthrough",
        default="default",
        help="Playthrough folder name (default: default)"
    )
    parser.add_argument(
        "--name", "-n",
        help="Output filename (without extension)"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--speed",
        choices=["FLASH", "TURBO", "DEFAULT", "QUALITY"],
        default="DEFAULT",
        help="Rendering speed (default: DEFAULT)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save image locally, just return URL"
    )
    parser.add_argument(
        "--list-types",
        action="store_true",
        help="List available image types and exit"
    )

    args = parser.parse_args()

    if args.list_types:
        print("Available image types:")
        for type_name, config in IMAGE_TYPES.items():
            print(f"  {type_name:25} {config['description']}")
        return

    try:
        result = generate_image(
            prompt=args.prompt,
            image_type=args.type,
            playthrough=args.playthrough,
            name=args.name,
            seed=args.seed,
            rendering_speed=args.speed,
            save=not args.no_save,
        )

        print("\nGeneration complete!")
        print(f"URL: {result['url']}")
        print(f"Seed: {result['seed']}")
        print(f"Resolution: {result['resolution']}")
        if result.get("local_path"):
            print(f"Saved: {result['local_path']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

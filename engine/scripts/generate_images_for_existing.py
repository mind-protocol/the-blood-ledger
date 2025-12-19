#!/usr/bin/env python3
"""
Generate images for existing graph nodes that don't have them.

Creates appropriate image prompts based on node attributes and generates images.

DOCS: docs/infrastructure/ops-scripts/PATTERNS_Operational_Seeding_And_Backfill_Scripts.md

Usage:
    python generate_images_for_existing.py --playthrough default
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add parent directories to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "engine"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "image_generation"))

from db.graph_ops import GraphOps, _generate_node_image

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_character_prompt(char: dict) -> str:
    """Create an image prompt from character attributes."""
    name = char.get('name', 'Unknown')
    char_type = char.get('type', 'minor')
    face = char.get('face', 'weathered')
    flaw = char.get('flaw', '')
    backstory_wound = char.get('backstory_wound', '')
    voice_tone = char.get('voice_tone', '')

    # Parse values if JSON string
    values = char.get('values', [])
    if isinstance(values, str):
        try:
            values = json.loads(values)
        except:
            values = []

    # Build character description based on attributes
    age_map = {
        'player': 'late twenties',
        'companion': 'thirties',
        'major': 'forties',
        'minor': 'middle-aged',
        'background': 'indeterminate age'
    }
    age = age_map.get(char_type, 'middle-aged')

    face_desc = {
        'young': 'youthful face, unblemished',
        'scarred': 'angular face with visible scars, marks of battle',
        'weathered': 'weathered face, deep lines from hardship',
        'gaunt': 'gaunt, hollow-cheeked face',
        'hard': 'hard face, cold eyes',
        'noble': 'noble features, strong jaw'
    }.get(face, 'weathered face')

    # Determine mood/expression from flaw or tone
    expression = 'guarded expression'
    if flaw == 'doubt':
        expression = 'uncertain, searching eyes'
    elif flaw == 'wrath':
        expression = 'barely contained anger in the eyes'
    elif flaw == 'pride':
        expression = 'proud, defiant gaze'
    elif flaw == 'fear':
        expression = 'haunted, watchful eyes'
    elif voice_tone == 'bitter':
        expression = 'bitter, hard expression'
    elif voice_tone == 'quiet':
        expression = 'quiet intensity in the eyes'

    # Build the prompt following PATTERNS_Image_Generation.md
    prompt = f"""A cinematic portrait of a Saxon {'warrior' if char_type in ['player', 'companion'] else 'man'}, 10th century England. {age.capitalize()}, {face_desc}. Dark hair, {expression}. Worn wool and leather clothing, iron brooch at shoulder. Firelight from below casting warm orange glow, cold blue moonlight from above mixing on features. Background dark and indistinct. Shallow depth of field. 35mm film photography, naturalistic lighting, muted earth tones, highly detailed."""

    return prompt


def create_place_prompt(place: dict) -> str:
    """Create an image prompt from place attributes."""
    name = place.get('name', 'Unknown')
    place_type = place.get('type', 'village')
    mood = place.get('mood', 'watchful')

    # Parse weather if JSON string
    weather = place.get('weather', [])
    if isinstance(weather, str):
        try:
            weather = json.loads(weather)
        except:
            weather = []

    weather_desc = 'overcast sky'
    if 'clear' in weather:
        weather_desc = 'clear sky with stars visible'
    elif 'rain' in weather:
        weather_desc = 'light rain falling'
    elif 'fog' in weather:
        weather_desc = 'thick fog'
    elif 'cold' in weather:
        weather_desc = 'frost on the ground, cold clear air'

    mood_desc = {
        'welcoming': 'warm, inviting atmosphere',
        'hostile': 'threatening, unwelcoming atmosphere',
        'indifferent': 'neutral, still atmosphere',
        'fearful': 'tense, fearful atmosphere',
        'watchful': 'watchful, alert atmosphere',
        'desperate': 'desperate, grim atmosphere',
        'peaceful': 'peaceful, calm atmosphere',
        'tense': 'heavy tension in the air'
    }.get(mood, 'watchful atmosphere')

    type_desc = {
        'region': f'A cinematic wide shot of rolling northern English countryside, 10th century. Bare oak and birch trees, heather moorland stretching to distant hills.',
        'city': f'A cinematic wide shot of a walled Saxon city, 10th century England. Stone and timber walls, thatched roofs within, church spire visible.',
        'hold': f'A cinematic wide shot of a fortified Saxon hall on a hill, 10th century England. Timber palisade walls, central hall with smoke rising.',
        'village': f'A cinematic wide shot of a small Saxon village, 10th century England. Thatched cottages, muddy paths, bare trees surrounding.',
        'monastery': f'A cinematic wide shot of a stone monastery, 10th century England. Simple stone church, cloisters, gardens.',
        'camp': f'A cinematic wide shot of an empty forest clearing suitable for camping, 10th century England. Bare oak trees framing the scene, frost-covered grass.',
        'road': f'A cinematic wide shot of a muddy forest road, 10th century England. Rutted track through bare trees, puddles reflecting grey sky.',
        'room': f'A cinematic interior shot of a Saxon hall interior, 10th century England. Massive oak beams, rough stone walls, central hearth.',
        'wilderness': f'A cinematic wide shot of untamed northern moorland, 10th century England. Heather and bracken, scattered boulders, no paths.',
        'ruin': f'A cinematic wide shot of burned ruins, 10th century England. Charred timbers, collapsed walls, overgrown with weeds.'
    }.get(place_type, f'A cinematic wide shot of a {place_type}, 10th century England.')

    prompt = f"""{type_desc} {weather_desc.capitalize()}. {mood_desc.capitalize()}. No people visible, no modern elements. Wide establishing shot, slight low angle. Volumetric mist. 35mm film photography, desaturated colors, naturalistic lighting."""

    return prompt


def main():
    parser = argparse.ArgumentParser(description='Generate images for existing graph nodes')
    parser.add_argument('--playthrough', default='default', help='Playthrough folder name')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--dry-run', action='store_true', help='Show prompts without generating')
    args = parser.parse_args()

    logger.info(f"Connecting to FalkorDB at {args.host}:{args.port}")
    graph = GraphOps(host=args.host, port=args.port)

    # Get all characters without image_path
    logger.info("\n=== Processing Characters ===")
    result = graph.graph.query("""
        MATCH (n:Character)
        WHERE n.image_path IS NULL
        RETURN n
    """)

    for row in result.result_set or []:
        char = row[0].properties
        char_id = char.get('id')
        name = char.get('name')

        prompt = create_character_prompt(char)
        logger.info(f"\n{name} ({char_id}):")
        logger.info(f"  Prompt: {prompt[:100]}...")

        if args.dry_run:
            continue

        # Update node with prompt
        graph.graph.query(f"""
            MATCH (n:Character {{id: '{char_id}'}})
            SET n.image_prompt = $prompt
        """, {'prompt': prompt})

        # Generate image
        image_path = _generate_node_image('character', char_id, prompt, args.playthrough)
        if image_path:
            graph.graph.query(f"""
                MATCH (n:Character {{id: '{char_id}'}})
                SET n.image_path = $path
            """, {'path': image_path})
            logger.info(f"  Image saved: {image_path}")
        else:
            logger.warning(f"  Failed to generate image")

    # Get all places without image_path
    logger.info("\n=== Processing Places ===")
    result = graph.graph.query("""
        MATCH (n:Place)
        WHERE n.image_path IS NULL
        RETURN n
    """)

    for row in result.result_set or []:
        place = row[0].properties
        place_id = place.get('id')
        name = place.get('name')

        prompt = create_place_prompt(place)
        logger.info(f"\n{name} ({place_id}):")
        logger.info(f"  Prompt: {prompt[:100]}...")

        if args.dry_run:
            continue

        # Update node with prompt
        graph.graph.query(f"""
            MATCH (n:Place {{id: '{place_id}'}})
            SET n.image_prompt = $prompt
        """, {'prompt': prompt})

        # Generate image
        image_path = _generate_node_image('place', place_id, prompt, args.playthrough)
        if image_path:
            graph.graph.query(f"""
                MATCH (n:Place {{id: '{place_id}'}})
                SET n.image_path = $path
            """, {'path': image_path})
            logger.info(f"  Image saved: {image_path}")
        else:
            logger.warning(f"  Failed to generate image")

    # Get all things without image_path
    logger.info("\n=== Processing Things ===")
    result = graph.graph.query("""
        MATCH (n:Thing)
        WHERE n.image_path IS NULL
        RETURN n
    """)

    for row in result.result_set or []:
        thing = row[0].properties
        thing_id = thing.get('id')
        name = thing.get('name')
        thing_type = thing.get('type', 'tool')
        desc = thing.get('description', '')
        significance = thing.get('significance', 'mundane')

        # Create thing prompt
        sig_desc = {
            'mundane': 'common, well-used',
            'personal': 'carefully maintained, clearly treasured',
            'political': 'finely crafted, bearing marks of authority',
            'sacred': 'bearing religious symbols, reverently kept',
            'legendary': 'ancient, storied, radiating significance'
        }.get(significance, 'common')

        prompt = f"""A cinematic close-up of a {sig_desc} Saxon {thing_type}, 10th century England. {desc if desc else 'Well-crafted, showing signs of use.'}. Resting on rough wool cloth. Warm candlelight catching details, deep shadows. Shallow depth of field, dark background. 35mm film photography, rich warm tones, highly detailed."""

        logger.info(f"\n{name} ({thing_id}):")
        logger.info(f"  Prompt: {prompt[:100]}...")

        if args.dry_run:
            continue

        # Update node with prompt
        graph.graph.query(f"""
            MATCH (n:Thing {{id: '{thing_id}'}})
            SET n.image_prompt = $prompt
        """, {'prompt': prompt})

        # Generate image
        image_path = _generate_node_image('thing', thing_id, prompt, args.playthrough)
        if image_path:
            graph.graph.query(f"""
                MATCH (n:Thing {{id: '{thing_id}'}})
                SET n.image_path = $path
            """, {'path': image_path})
            logger.info(f"  Image saved: {image_path}")
        else:
            logger.warning(f"  Failed to generate image")

    logger.info("\n=== Complete ===")


if __name__ == "__main__":
    main()

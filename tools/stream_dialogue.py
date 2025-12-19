#!/usr/bin/env python3
# DOCS: docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md
"""
Stream dialogue and narration to the frontend via moments graph.

Usage from narrator (Claude Code):

    # Dialogue - creates moment in graph with speaker
    python3 tools/stream_dialogue.py -p default -t dialogue -s char_aldric \
        "But my niece — [Edda](Who's Edda?) — she's the finest archer."

    # Narration - creates moment in graph (no speaker)
    python3 tools/stream_dialogue.py -p default -t narration --tone tense \
        "He prods the [embers](The fire is dying.) with a stick."

    # Signal time elapsed (triggers world tick)
    python3 tools/stream_dialogue.py -p default -t time "4 hours"

    # Complete the stream
    python3 tools/stream_dialogue.py -p default -t complete

Flags:
    --tone          Emotional tone (curious, defiant, warm, cold, tense, etc.)
    -s, --speaker   Character ID for dialogue

Inline clickable syntax:
    [word](What player says when clicking)

    This creates a clickable that triggers streaming when clicked.
    The response is NOT pre-baked — narrator will generate it live.

Moment creation behavior:
    1. Main moment created as "active" with weight 1.0 (immediately visible)
    2. Each [word](speaks) creates:
       - A "possible" target moment (weight 0.5, empty text)
       - A CAN_LEAD_TO link from main → target with require_words=[word]
    3. When player clicks word:
       - handle_click() adds weight_transfer (0.4) to target
       - Target weight becomes 0.9 > 0.8 threshold → flips to "active"
       - Narrator generates response, fills target moment text

Deprecated (no longer used):
{
  "narration": [
    {
      "text": "Aldric looks up, his blade across his knees.",
      "speaker": "char_aldric",
      "clickable": {
        "blade": {
          "speaks": "That blade's seen some use.",
          "intent": "ask_about_past",
          "response": {
            "speaker": "char_aldric",
            "text": "Aye. It was my father's."
          }
        }
      }
    }
  ],
  "voices": [...]
}

The script appends to playthroughs/{playthrough}/stream.jsonl
The API endpoint tails this file and forwards as SSE events.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Tuple

PROJECT_ROOT = Path(__file__).parent.parent

# Add engine to path for graph imports
sys.path.insert(0, str(PROJECT_ROOT))


def get_playthrough_graph_name(playthrough: str) -> str:
    """Get the graph name for a playthrough from player.yaml."""
    import yaml
    player_file = PROJECT_ROOT / 'playthroughs' / playthrough / 'player.yaml'
    if player_file.exists():
        try:
            data = yaml.safe_load(player_file.read_text())
            return data.get('graph_name', playthrough)
        except Exception:
            pass
    # Fallback to playthrough id as graph name
    return playthrough


def get_graph_ops(playthrough: str = None):
    """Lazy import of GraphOps with playthrough-specific graph."""
    from engine.physics.graph.graph_ops import GraphOps
    graph_name = get_playthrough_graph_name(playthrough) if playthrough else "blood_ledger"
    return GraphOps(graph_name=graph_name)


def get_graph_queries(playthrough: str = None):
    """Lazy import of GraphQueries with playthrough-specific graph."""
    from engine.physics.graph.graph_queries import GraphQueries
    graph_name = get_playthrough_graph_name(playthrough) if playthrough else "blood_ledger"
    return GraphQueries(graph_name=graph_name)


def get_current_tick(playthrough: str) -> int:
    """Get current tick from graph world state or default to 0."""
    try:
        queries = get_graph_queries(playthrough)
        # Query for world tick from graph
        result = queries._query("""
            MATCH (w:World)
            RETURN w.tick
            LIMIT 1
        """)
        if result and result[0]:
            return result[0][0] or 0
    except Exception:
        pass
    return 0


def get_current_place(playthrough: str) -> Optional[str]:
    """Get player's current place ID from graph."""
    try:
        queries = get_graph_queries(playthrough)
        player_loc = queries.get_player_location("char_player")
        if player_loc:
            return player_loc.get("id")
    except Exception:
        pass
    return None


def create_moment_with_clickables(
    playthrough: str,
    text: str,
    moment_type: str,
    speaker: Optional[str] = None,
    tone: Optional[str] = None
) -> Tuple[str, Dict]:
    """
    Create a moment in the graph with CAN_LEAD_TO links for clickables.

    This is the graph-native alternative to scene.json. Each clickable word
    creates a "possible" target moment that can surface when clicked.

    Args:
        playthrough: Playthrough ID
        text: Text with inline clickables [word](speaks text)
        moment_type: "dialogue" or "narration"
        speaker: Character ID for dialogue
        tone: Emotional tone

    Returns:
        Tuple of (moment_id, clickables_dict)
    """
    ops = get_graph_ops(playthrough)
    tick = get_current_tick(playthrough)
    place_id = get_current_place(playthrough)

    # Parse clickables from text
    clean_text, clickables = parse_inline_clickables(text)

    # Generate moment ID
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%H%M%S%f")[:10]
    place_prefix = place_id.replace("place_", "") if place_id and place_id.startswith("place_") else "unknown"
    day = (tick // 1440) + 1
    moment_id = f"{place_prefix}_d{day}_{moment_type}_{timestamp}"

    # Create main moment (active, weight 1.0 = immediately visible)
    ops.add_moment(
        id=moment_id,
        text=clean_text,
        type=moment_type,
        tick=tick,
        speaker=speaker,
        place_id=place_id,
        status="active",
        weight=1.0,
        tone=tone,
        tick_spoken=tick
    )

    # For each clickable, create a target moment and CAN_LEAD_TO link
    for word, clickable_data in clickables.items():
        speaks = clickable_data.get('speaks', '')

        # Target moment ID
        target_id = f"{moment_id}_click_{word.lower().replace(' ', '_')}"

        # Create target moment as "possible" - waits for player click
        # The text is empty because narrator will generate the response
        ops.add_moment(
            id=target_id,
            text="",  # Empty - will be filled when narrator responds
            type="dialogue",
            tick=tick,
            place_id=place_id,
            status="possible",
            weight=0.5  # Below flip threshold
        )

        # Create CAN_LEAD_TO link with require_words
        ops.add_can_lead_to(
            from_moment_id=moment_id,
            to_moment_id=target_id,
            trigger="player",
            require_words=[word],
            weight_transfer=0.4,  # Clicking adds 0.4 weight (0.5 + 0.4 = 0.9 > 0.8 threshold)
            consumes_origin=False  # Main moment stays visible
        )

        # Store the target ID back in clickables for reference
        clickables[word]['target_moment_id'] = target_id
        clickables[word]['player_speaks'] = speaks

    print(f"[GRAPH] Created moment {moment_id} with {len(clickables)} clickables")
    return moment_id, clickables

# Regex for inline clickables: [word](speaks text)
CLICKABLE_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def parse_inline_clickables(text: str) -> tuple[str, dict]:
    """
    Parse inline clickable syntax from text.

    Input:  "My niece [Edda](Who's Edda?) is an archer."
    Output: ("My niece Edda is an archer.", {"Edda": {"speaks": "Who's Edda?", ...}})
    """
    clickables = {}

    def replace_match(match):
        word = match.group(1)
        speaks = match.group(2)
        clickables[word] = {
            "speaks": speaks,
            "intent": "ask",
            "waitingMessage": "..."  # Triggers streaming response
        }
        return word

    clean_text = CLICKABLE_PATTERN.sub(replace_match, text)
    return clean_text, clickables


def stream_event(playthrough: str, event_type: str, data: dict):
    """Write an event to the stream file."""
    event = {
        'type': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'data': data
    }

    stream_file = PROJECT_ROOT / 'playthroughs' / playthrough / 'stream.jsonl'
    stream_file.parent.mkdir(parents=True, exist_ok=True)

    with open(stream_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

    return event


def main():
    parser = argparse.ArgumentParser(description='Stream dialogue to frontend')
    parser.add_argument('-p', '--playthrough', required=True, help='Playthrough ID')
    parser.add_argument('-t', '--type', required=True,
                        choices=['dialogue', 'narration', 'mutation', 'scene', 'time', 'complete', 'error'],
                        help='Event type')
    parser.add_argument('-s', '--speaker', help='Character ID for dialogue')
    parser.add_argument('--file', help='JSON file path for scene/mutation')
    # Graph mode is now the only mode - moments are always created in graph
    parser.add_argument('--tone', help='Emotional tone for the moment (curious, defiant, warm, etc.)')
    parser.add_argument('text', nargs='?', help='Text content for dialogue/narration')

    args = parser.parse_args()

    if args.type == 'dialogue':
        if not args.text:
            print("Error: text required for dialogue", file=sys.stderr)
            sys.exit(1)

        # Create moment in graph
        moment_id, clickables = create_moment_with_clickables(
            playthrough=args.playthrough,
            text=args.text,
            moment_type="dialogue",
            speaker=args.speaker,
            tone=args.tone
        )
        # Parse for clean text to stream
        clean_text, _ = parse_inline_clickables(args.text)
        data = {
            'text': clean_text,
            'moment_id': moment_id
        }
        if args.speaker:
            data['speaker'] = args.speaker
        if clickables:
            data['clickable'] = clickables
        if args.tone:
            data['tone'] = args.tone

        event = stream_event(args.playthrough, 'dialogue', data)

    elif args.type == 'narration':
        if not args.text:
            print("Error: text required for narration", file=sys.stderr)
            sys.exit(1)

        # Create moment in graph
        moment_id, clickables = create_moment_with_clickables(
            playthrough=args.playthrough,
            text=args.text,
            moment_type="narration",
            speaker=None,  # Narration has no speaker
            tone=args.tone
        )
        # Parse for clean text to stream
        clean_text, _ = parse_inline_clickables(args.text)
        data = {
            'text': clean_text,
            'moment_id': moment_id
        }
        if clickables:
            data['clickable'] = clickables
        if args.tone:
            data['tone'] = args.tone

        event = stream_event(args.playthrough, 'narration', data)

    elif args.type == 'scene':
        if args.file:
            scene_path = Path(args.file)
            if not scene_path.is_absolute():
                scene_path = PROJECT_ROOT / 'playthroughs' / args.playthrough / args.file
            try:
                data = json.loads(scene_path.read_text())
            except Exception as e:
                print(f"Error reading scene file: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.text:
            try:
                data = json.loads(args.text)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Error: --file or JSON text required for scene", file=sys.stderr)
            sys.exit(1)

        # Persist scene to playthrough's scene.json
        persist_path = PROJECT_ROOT / 'playthroughs' / args.playthrough / 'scene.json'
        persist_path.parent.mkdir(parents=True, exist_ok=True)
        persist_path.write_text(json.dumps(data, indent=2))
        print(f"[PERSIST] Scene saved to {persist_path}")

        event = stream_event(args.playthrough, 'scene', data)

    elif args.type == 'mutation':
        if args.file:
            mut_path = Path(args.file)
            if not mut_path.is_absolute():
                mut_path = PROJECT_ROOT / 'playthroughs' / args.playthrough / args.file
            try:
                data = json.loads(mut_path.read_text())
            except Exception as e:
                print(f"Error reading mutation file: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.text:
            try:
                data = json.loads(args.text)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Error: --file or JSON text required for mutation", file=sys.stderr)
            sys.exit(1)
        event = stream_event(args.playthrough, 'mutation', data)

    elif args.type == 'time':
        event = stream_event(args.playthrough, 'time', {'time_elapsed': args.text or '5 minutes'})

    elif args.type == 'complete':
        event = stream_event(args.playthrough, 'complete', {'status': 'ok'})

    elif args.type == 'error':
        event = stream_event(args.playthrough, 'error', {'error': args.text or 'Unknown error'})

    # Print for feedback
    print(f"[STREAM] {event['type']}: {json.dumps(event['data'])[:100]}...")


if __name__ == '__main__':
    main()

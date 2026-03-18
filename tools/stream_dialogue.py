#!/usr/bin/env python3
# DOCS: docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md
"""
Stream dialogue and narration to the frontend via moments graph.

Usage:
    python3 tools/stream_dialogue.py -p default -t dialogue -s char_aldric \
        "But my niece - [Edda](Who's Edda?) - she's the finest archer."

    python3 tools/stream_dialogue.py -p default -t narration --tone tense \
        "He prods the [embers](The fire is dying.) with a stick."
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _ensure_ngram_engine_on_path() -> None:
    ngram_root = Path("/home/mind-protocol/ngram")
    if ngram_root.exists():
        sys.path.insert(0, str(ngram_root))


def _import_graph_ops():
    try:
        from engine.physics.graph.graph_ops import GraphOps
        return GraphOps
    except ModuleNotFoundError:
        _ensure_ngram_engine_on_path()
        from engine.physics.graph.graph_ops import GraphOps
        return GraphOps


def _import_graph_queries():
    try:
        from engine.physics.graph.graph_queries import GraphQueries
        return GraphQueries
    except ModuleNotFoundError:
        _ensure_ngram_engine_on_path()
        from engine.physics.graph.graph_queries import GraphQueries
        return GraphQueries


def get_playthrough_graph_name(playthrough: str) -> str:
    import yaml
    player_file = PROJECT_ROOT / "playthroughs" / playthrough / "player.yaml"
    if player_file.exists():
        try:
            data = yaml.safe_load(player_file.read_text())
            return data.get("graph_name", playthrough)
        except Exception:
            pass
    return playthrough


def get_graph_ops(playthrough: Optional[str]):
    GraphOps = _import_graph_ops()
    graph_name = get_playthrough_graph_name(playthrough) if playthrough else "blood_ledger"
    return GraphOps(graph_name=graph_name)


def get_graph_queries(playthrough: Optional[str]):
    GraphQueries = _import_graph_queries()
    graph_name = get_playthrough_graph_name(playthrough) if playthrough else "blood_ledger"
    return GraphQueries(graph_name=graph_name)


def get_current_tick(playthrough: str) -> int:
    try:
        queries = get_graph_queries(playthrough)
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
    try:
        queries = get_graph_queries(playthrough)
        player_loc = queries.get_player_location("char_player")
        if player_loc:
            return player_loc.get("id")
    except Exception:
        pass
    return None


CLICKABLE_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def parse_inline_clickables(text: str) -> Tuple[str, Dict]:
    clickables: Dict[str, Dict[str, str]] = {}

    def replace_match(match: re.Match) -> str:
        word = match.group(1)
        speaks = match.group(2)
        clickables[word] = {
            "speaks": speaks,
            "intent": "ask",
            "waitingMessage": "...",
        }
        return word

    clean_text = CLICKABLE_PATTERN.sub(replace_match, text)
    return clean_text, clickables


def create_moment_with_clickables(
    playthrough: str,
    text: str,
    moment_type: str,
    speaker: Optional[str] = None,
    tone: Optional[str] = None,
) -> Tuple[str, Dict]:
    clean_text, clickables = parse_inline_clickables(text)

    tick = get_current_tick(playthrough)
    place_id = get_current_place(playthrough)
    timestamp = datetime.utcnow().strftime("%H%M%S%f")[:10]
    place_prefix = (
        place_id.replace("place_", "")
        if place_id and place_id.startswith("place_")
        else "unknown"
    )
    day = (tick // 1440) + 1
    moment_id = f"{place_prefix}_d{day}_{moment_type}_{timestamp}"

    try:
        ops = get_graph_ops(playthrough)
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
            tick_spoken=tick,
        )

        for word, clickable_data in clickables.items():
            target_id = f"{moment_id}_click_{word.lower().replace(' ', '_')}"
            ops.add_moment(
                id=target_id,
                text="",
                type="dialogue",
                tick=tick,
                place_id=place_id,
                status="possible",
                weight=0.5,
            )
            ops.add_can_lead_to(
                from_moment_id=moment_id,
                to_moment_id=target_id,
                trigger="player",
                require_words=[word],
                weight_transfer=0.4,
                consumes_origin=False,
            )
            clickables[word]["target_moment_id"] = target_id
            clickables[word]["player_speaks"] = clickable_data.get("speaks", "")

        print(f"[GRAPH] Created moment {moment_id} with {len(clickables)} clickables")
    except Exception as exc:
        print(f"[WARN] GraphOps unavailable, skipping graph writes: {exc}", file=sys.stderr)

    return moment_id, clickables


def stream_event(playthrough: str, event_type: str, data: dict) -> dict:
    event = {
        "type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }
    stream_file = PROJECT_ROOT / "playthroughs" / playthrough / "stream.jsonl"
    stream_file.parent.mkdir(parents=True, exist_ok=True)
    with stream_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")
    return event


def _load_json_payload(playthrough: str, file_path: Optional[str], text: Optional[str], label: str) -> dict:
    if file_path:
        payload_path = Path(file_path)
        if not payload_path.is_absolute():
            payload_path = PROJECT_ROOT / "playthroughs" / playthrough / file_path
        try:
            return json.loads(payload_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise SystemExit(f"Error reading {label} file: {exc}") from exc
    if text:
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Error: Invalid JSON: {exc}") from exc
    raise SystemExit(f"Error: --file or JSON text required for {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream dialogue to frontend")
    parser.add_argument("-p", "--playthrough", required=True, help="Playthrough ID")
    parser.add_argument(
        "-t",
        "--type",
        required=True,
        choices=["dialogue", "narration", "mutation", "scene", "time", "complete", "error"],
        help="Event type",
    )
    parser.add_argument("-s", "--speaker", help="Character ID for dialogue")
    parser.add_argument("--file", help="JSON file path for scene/mutation")
    parser.add_argument("--tone", help="Emotional tone for the moment")
    parser.add_argument("text", nargs="?", help="Text content for dialogue/narration")
    args = parser.parse_args()

    if args.type == "dialogue":
        if not args.text:
            raise SystemExit("Error: text required for dialogue")
        moment_id, clickables = create_moment_with_clickables(
            playthrough=args.playthrough,
            text=args.text,
            moment_type="dialogue",
            speaker=args.speaker,
            tone=args.tone,
        )
        clean_text, _ = parse_inline_clickables(args.text)
        data = {"text": clean_text, "moment_id": moment_id}
        if args.speaker:
            data["speaker"] = args.speaker
        if clickables:
            data["clickable"] = clickables
        if args.tone:
            data["tone"] = args.tone
        event = stream_event(args.playthrough, "dialogue", data)

    elif args.type == "narration":
        if not args.text:
            raise SystemExit("Error: text required for narration")
        moment_id, clickables = create_moment_with_clickables(
            playthrough=args.playthrough,
            text=args.text,
            moment_type="narration",
            speaker=None,
            tone=args.tone,
        )
        clean_text, _ = parse_inline_clickables(args.text)
        data = {"text": clean_text, "moment_id": moment_id}
        if clickables:
            data["clickable"] = clickables
        if args.tone:
            data["tone"] = args.tone
        event = stream_event(args.playthrough, "narration", data)

    elif args.type == "scene":
        data = _load_json_payload(args.playthrough, args.file, args.text, "scene")
        persist_path = PROJECT_ROOT / "playthroughs" / args.playthrough / "scene.json"
        persist_path.parent.mkdir(parents=True, exist_ok=True)
        persist_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[PERSIST] Scene saved to {persist_path}")
        event = stream_event(args.playthrough, "scene", data)

    elif args.type == "mutation":
        data = _load_json_payload(args.playthrough, args.file, args.text, "mutation")
        event = stream_event(args.playthrough, "mutation", data)

    elif args.type == "time":
        event = stream_event(args.playthrough, "time", {"time_elapsed": args.text or "5 minutes"})

    elif args.type == "complete":
        event = stream_event(args.playthrough, "complete", {"status": "ok"})

    else:
        event = stream_event(args.playthrough, "error", {"error": args.text or "Unknown error"})

    print(f"[STREAM] {event['type']}: {json.dumps(event['data'])[:100]}...")


if __name__ == "__main__":
    main()

"""
Blood Ledger — Playthrough Management API Endpoints

Endpoints for creating and managing playthroughs, sending player moments,
and discussion tree navigation.

Extracted from app.py to reduce file size.

Docs:
- docs/physics/IMPLEMENTATION_Physics.md — code architecture
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from engine.physics.graph import GraphQueries, get_playthrough_graph_name

logger = logging.getLogger(__name__)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class PlaythroughCreateRequest(BaseModel):
    """Request to create a new playthrough."""
    scenario_id: str
    player_name: str
    player_gender: str = "male"


class MomentRequest(BaseModel):
    """Request to send a player moment."""
    playthrough_id: str
    text: str
    moment_type: str = "player_freeform"  # player_freeform, player_click, player_choice


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _opening_to_scene_tree(opening_template: dict, scenario: dict) -> dict:
    """
    Convert opening.json template to SceneTree format with nested freeform_acknowledgment.
    """
    setting = opening_template.get("setting", {})
    beats = opening_template.get("beats", [])
    companion_id = scenario.get("companion", {}).get("id", "char_aldric")

    # Build nested narration from beats
    def build_beat_narration(beat_index: int) -> list:
        """Recursively build narration for a beat with freeform_acknowledgment linking to next."""
        if beat_index >= len(beats):
            return []

        beat = beats[beat_index]
        narration_lines = beat.get("narration", [])
        questions = beat.get("questions", [])

        result = []

        # Add narration lines
        for line in narration_lines:
            # Check if it's dialogue (starts with quote)
            if line.startswith('"'):
                result.append({
                    "text": line,
                    "speaker": companion_id
                })
            else:
                result.append({"text": line})

        # Add questions with freeform_acknowledgment
        for i, question in enumerate(questions):
            is_last_question_of_beat = (i == len(questions) - 1)
            is_last_beat = (beat_index == len(beats) - 1)

            q_narration = {
                "text": question.get("text", ""),
                "speaker": question.get("speaker", companion_id)
            }

            # Add transition if present
            if question.get("transition"):
                result.append({"text": question["transition"]})

            # Build freeform_acknowledgment
            if question.get("type") == "statement":
                # Statements don't need acknowledgment text, just continue
                ack = {"text": ""}
            else:
                # Regular questions get acknowledgment
                ack = {"text": "He nods slowly."}

            # Link to next content
            if is_last_question_of_beat and not is_last_beat:
                # Link to next beat
                ack["then"] = build_beat_narration(beat_index + 1)
            elif not is_last_question_of_beat:
                # Link to next question in same beat (continue with remaining questions)
                remaining_questions = questions[i+1:]
                if remaining_questions:
                    next_q = remaining_questions[0]
                    ack["then"] = [{
                        "text": next_q.get("text", ""),
                        "speaker": next_q.get("speaker", companion_id),
                        "freeform_acknowledgment": {
                            "text": "He nods slowly.",
                            "then": build_beat_narration(beat_index + 1) if is_last_question_of_beat else []
                        }
                    }]

            q_narration["freeform_acknowledgment"] = ack
            result.append(q_narration)
            break  # Only add first question, rest are in nested then

        return result

    # Build the scene tree
    scene = {
        "id": "opening_fireside",
        "location": {
            "place": setting.get("location", "camp_roadside"),
            "name": "Roadside Camp",
            "region": "The North Road",
            "time": setting.get("time", "night")
        },
        "characters": setting.get("characters", ["char_aldric"]),
        "atmosphere": setting.get("atmosphere", []),
        "narration": build_beat_narration(0),
        "voices": []
    }

    return scene


def _count_branches(topics: list) -> int:
    """Count total unexplored branches across all topics."""
    count = 0

    def count_clickables(obj):
        nonlocal count
        if isinstance(obj, dict):
            clickable = obj.get("clickable", {})
            count += len(clickable)
            for v in clickable.values():
                if isinstance(v, dict) and "response" in v:
                    count_clickables(v["response"])

    for topic in topics:
        count_clickables(topic.get("opener", {}))

    return count


def _delete_branch(topic: dict, branch_path: list):
    """Delete a branch from a topic tree."""
    if not branch_path:
        return

    # Navigate to parent of branch to delete
    current = topic.get("opener", {})
    for word in branch_path[:-1]:
        clickable = current.get("clickable", {})
        if word in clickable:
            current = clickable[word].get("response", {})
        else:
            return  # Path not found

    # Delete the final branch
    clickable = current.get("clickable", {})
    if branch_path[-1] in clickable:
        del clickable[branch_path[-1]]


# =============================================================================
# ROUTER
# =============================================================================

def create_playthroughs_router(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379,
    playthroughs_dir: str = "playthroughs"
) -> APIRouter:
    """
    Create the playthroughs API router.

    This is mounted in app.py as /api.
    Handles playthrough creation, moment sending, and discussion trees.
    """
    router = APIRouter(tags=["playthroughs"])

    # Store config
    _host = host
    _port = port
    _graph_name = graph_name
    _playthroughs_dir = Path(playthroughs_dir)

    # Track running narrator processes per playthrough
    _narrator_processes: Dict[str, subprocess.Popen] = {}

    def _get_playthrough_queries(playthrough_id: str) -> GraphQueries:
        """Get graph queries instance for a specific playthrough."""
        pt_graph_name = get_playthrough_graph_name(playthrough_id)
        return GraphQueries(graph_name=pt_graph_name, host=_host, port=_port)

    # =========================================================================
    # PLAYTHROUGH CREATION
    # =========================================================================

    @router.post("/playthrough/create")
    async def create_playthrough(request: PlaythroughCreateRequest):
        """
        Create a new playthrough:
        1. Create playthrough directory
        2. Save player.yaml
        3. Inject scenario nodes/links into graph
        4. Generate scene.json from opening.json template
        5. Return scene for frontend to display
        """
        import re
        import yaml
        from engine.physics.graph.graph_ops import GraphOps

        # Generate playthrough ID from player name
        # Slugify: lowercase, replace spaces/special chars with underscore
        base_id = re.sub(r'[^a-z0-9]+', '_', request.player_name.lower()).strip('_')
        if not base_id:
            base_id = "player"

        # Find unique ID (add number suffix if duplicate exists)
        playthrough_id = base_id
        counter = 2
        while (_playthroughs_dir / playthrough_id).exists():
            playthrough_id = f"{base_id}_{counter}"
            counter += 1

        playthrough_dir = _playthroughs_dir / playthrough_id
        playthrough_dir.mkdir(parents=True, exist_ok=True)
        (playthrough_dir / "mutations").mkdir(exist_ok=True)
        (playthrough_dir / "conversations").mkdir(exist_ok=True)

        # 1. Save player.yaml (includes graph_name for other endpoints)
        player_data = {
            "name": request.player_name,
            "gender": request.player_gender,
            "scenario": request.scenario_id,
            "graph_name": playthrough_id,  # Graph name = playthrough_id for isolation
            "created_at": datetime.utcnow().isoformat()
        }
        (playthrough_dir / "player.yaml").write_text(yaml.dump(player_data))

        # 2. Load and inject scenario
        scenarios_dir = Path(__file__).parent.parent.parent / "scenarios"
        scenario_file = scenarios_dir / f"{request.scenario_id}.yaml"

        if not scenario_file.exists():
            raise HTTPException(status_code=404, detail=f"Scenario not found: {request.scenario_id}")

        scenario = yaml.safe_load(scenario_file.read_text())

        # Use playthrough_id as graph name for isolation
        playthrough_graph_name = playthrough_id

        # Initialize new graph with seed data
        try:
            from engine.init_db import load_initial_state
            logger.info(f"Initializing graph {playthrough_graph_name} with seed data...")
            load_initial_state(playthrough_graph_name, _host, _port)
            logger.info(f"Seed data loaded for {playthrough_graph_name}")
        except Exception as e:
            logger.error(f"Failed to load seed data: {e}")
            # Continue anyway - scenario may still work

        # Inject scenario nodes and links into graph
        try:
            graph = GraphOps(graph_name=playthrough_graph_name, host=_host, port=_port)

            # Build injection data from scenario
            inject_data = {
                "nodes": scenario.get("nodes", []),
                "links": scenario.get("links", [])
            }

            # Update player name/gender in player node if present
            for node in inject_data["nodes"]:
                if node.get("id") == "char_player":
                    node["name"] = request.player_name
                    node["gender"] = request.player_gender

            if inject_data["nodes"] or inject_data["links"]:
                result = graph.apply(data=inject_data, playthrough=playthrough_id)
                logger.info(f"Scenario injected: {len(result.persisted)} items, {len(result.errors)} errors")
                if result.errors:
                    for err in result.errors[:5]:
                        logger.warning(f"  Injection error: {err}")
        except Exception as e:
            logger.error(f"Failed to inject scenario: {e}")

        # 3. Create opening moments from scenario
        try:
            opening = scenario.get("opening", {})
            opening_narration = opening.get("narration", "")
            location_id = scenario.get("location", "place_camp")

            if opening_narration:
                # Split narration into lines and create moments
                lines = [line.strip() for line in opening_narration.strip().split("\n") if line.strip()]
                for i, line in enumerate(lines):
                    moment_id = f"opening_{playthrough_id[:8]}_{i}"
                    graph.add_moment(
                        id=moment_id,
                        text=line,
                        type="narration",
                        tick=0,
                        place_id=location_id,
                        status="active",
                        weight=1.0,
                        tick_spoken=0
                    )
                logger.info(f"Created {len(lines)} opening moments for {playthrough_id}")
        except Exception as e:
            logger.error(f"Failed to create opening moments: {e}")

        # 4. Load opening.json template and convert to scene
        opening_template_path = Path(__file__).parent.parent.parent / "docs" / "opening" / "opening.json"
        if opening_template_path.exists():
            opening_template = json.loads(opening_template_path.read_text())
            scene = _opening_to_scene_tree(opening_template, scenario)
        else:
            # Fallback minimal scene
            scene = {
                "id": f"scene_{request.scenario_id}_start",
                "location": {"place": "place_camp", "name": "Camp", "region": "The North", "time": "night"},
                "characters": ["char_aldric"],
                "atmosphere": ["The fire crackles."],
                "narration": [{"text": "Aldric looks at you.", "speaker": "char_aldric"}],
                "voices": []
            }

        # 4. Save scene.json
        (playthrough_dir / "scene.json").write_text(json.dumps(scene, indent=2))

        # 5. Initialize empty files
        (playthrough_dir / "message_queue.json").write_text("[]")
        (playthrough_dir / "injection_queue.json").write_text('{"injections": []}')
        (playthrough_dir / "stream.jsonl").write_text("")
        (playthrough_dir / "PROFILE_NOTES.md").write_text("# Player Profile (Opening)\n\n## Answers So Far\n\n## Emerging Pattern\n")

        logger.info(f"Created playthrough {playthrough_id} with scenario {request.scenario_id}")

        return {
            "status": "ok",
            "playthrough_id": playthrough_id,
            "scenario": request.scenario_id,
            "scene": scene
        }

    # =========================================================================
    # MOMENT ENDPOINT (Async)
    # =========================================================================

    @router.post("/moment")
    async def send_moment(request: MomentRequest):
        """
        Send a player moment (async).

        1. Append to message_queue.json
        2. If narrator not running: spawn it with scene.json + injection_queue.json
        3. Return immediately
        """
        playthrough_dir = _playthroughs_dir / request.playthrough_id
        if not playthrough_dir.exists():
            raise HTTPException(status_code=404, detail="Playthrough not found")

        # 1. Append to message queue
        queue_file = playthrough_dir / "message_queue.json"
        try:
            queue = json.loads(queue_file.read_text()) if queue_file.exists() else []
        except:
            queue = []

        moment = {
            "text": request.text,
            "type": request.moment_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        queue.append(moment)
        queue_file.write_text(json.dumps(queue, indent=2))

        # 2. Check if narrator is running
        narrator_running = False
        if request.playthrough_id in _narrator_processes:
            proc = _narrator_processes[request.playthrough_id]
            if proc.poll() is None:  # Still running
                narrator_running = True
            else:
                del _narrator_processes[request.playthrough_id]

        # 3. Spawn narrator if not running
        if not narrator_running:
            project_root = Path(__file__).parent.parent.parent
            narrator_dir = project_root / "agents" / "narrator"

            # Get context from graph
            try:
                queries = _get_playthrough_queries(request.playthrough_id)
                player_loc = queries.get_player_location("char_player")
                location_id = player_loc.get("id", "unknown") if player_loc else "unknown"
                location_name = player_loc.get("name", "Unknown") if player_loc else "Unknown"

                # Get characters at location
                characters = queries.get_characters_at(location_id) if location_id != "unknown" else []
                char_names = [c.get("name", c.get("id", "Unknown")) for c in characters if c.get("id") != "char_player"]
            except Exception as e:
                logger.warning(f"[moment] Failed to get graph context: {e}")
                location_id = "unknown"
                location_name = "Unknown"
                char_names = []

            characters_str = ", ".join(char_names) if char_names else "None"

            prompt = f"""Playthrough: {request.playthrough_id}
Player moment: {request.text}
Location: {location_name} ({location_id})
Characters present: {characters_str}

Respond using ../../tools/stream_dialogue.py -p {request.playthrough_id}. End with -t complete."""

            try:
                # Load PROFILE_NOTES.md for system prompt
                profile_notes_file = playthrough_dir / "PROFILE_NOTES.md"
                profile_notes = profile_notes_file.read_text() if profile_notes_file.exists() else ""

                cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions", "--continue"]
                if profile_notes:
                    cmd.extend(["--append-system-prompt", profile_notes])

                proc = subprocess.Popen(
                    cmd,
                    cwd=str(narrator_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                _narrator_processes[request.playthrough_id] = proc
                logger.info(f"[moment] Started narrator PID {proc.pid} for {request.playthrough_id}")
            except Exception as e:
                logger.error(f"[moment] Failed to start narrator: {e}")
                return {"status": "queued", "narrator_started": False, "error": str(e)}

        return {
            "status": "queued",
            "narrator_started": not narrator_running,
            "narrator_running": narrator_running or True
        }

    # =========================================================================
    # DISCUSSION TREE ENDPOINTS
    # =========================================================================

    @router.get("/{playthrough_id}/discussion/{char_id}/topics")
    async def get_discussion_topics(playthrough_id: str, char_id: str):
        """
        Get list of available discussion topics for a character.
        """
        tree_file = _playthroughs_dir / playthrough_id / "discussion_trees" / f"{char_id}.json"

        if not tree_file.exists():
            return {"topics": [], "branch_count": 0}

        try:
            data = json.loads(tree_file.read_text())
            topics = data.get("topics", [])
            branch_count = _count_branches(topics)

            return {
                "topics": [{"id": t["id"], "name": t["name"]} for t in topics],
                "branch_count": branch_count
            }
        except Exception as e:
            logger.error(f"Failed to get discussion topics: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{playthrough_id}/discussion/{char_id}/topic/{topic_id}")
    async def get_discussion_topic(playthrough_id: str, char_id: str, topic_id: str):
        """
        Get a specific discussion topic tree.
        """
        tree_file = _playthroughs_dir / playthrough_id / "discussion_trees" / f"{char_id}.json"

        if not tree_file.exists():
            raise HTTPException(status_code=404, detail="Discussion trees not found")

        try:
            data = json.loads(tree_file.read_text())
            topics = data.get("topics", [])

            for topic in topics:
                if topic["id"] == topic_id:
                    return {"topic": topic}

            raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get topic: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/{playthrough_id}/discussion/{char_id}/use-branch")
    async def use_discussion_branch(
        playthrough_id: str,
        char_id: str,
        request: Request
    ):
        """
        Mark a branch as used (delete it from the tree).
        Request body: {"topic_id": "...", "branch_path": ["word1", "word2"]}

        Returns remaining branch count. Triggers regeneration if < 5.
        """
        try:
            body = await request.json()
            topic_id = body.get("topic_id")
            branch_path = body.get("branch_path", [])

            tree_file = _playthroughs_dir / playthrough_id / "discussion_trees" / f"{char_id}.json"

            if not tree_file.exists():
                raise HTTPException(status_code=404, detail="Discussion trees not found")

            data = json.loads(tree_file.read_text())
            topics = data.get("topics", [])

            # Find and modify the topic
            modified = False
            for topic in topics:
                if topic["id"] == topic_id:
                    _delete_branch(topic, branch_path)
                    modified = True
                    break

            if not modified:
                raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found")

            # Save updated JSON
            tree_file.write_text(json.dumps({"topics": topics}, indent=2))

            # Count remaining branches
            branch_count = _count_branches(topics)

            # Trigger regeneration if needed
            regenerate_needed = branch_count < 5

            return {
                "status": "ok",
                "branch_count": branch_count,
                "regenerate_needed": regenerate_needed
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to use branch: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return router

"""
Blood Ledger — FastAPI Application

Main API application with endpoints for:
- Scene generation and clicks
- View data (map, ledger, faces, chronicle)
- SSE for rolling window updates

Docs:
- docs/engine/moments/PATTERNS_Moments.md — architecture + rationale
- docs/engine/moments/API_Moments.md — HTTP contract for the moment graph
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, AsyncGenerator
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from engine.orchestration import Orchestrator
from engine.db import GraphQueries, GraphOps, add_mutation_listener
from engine.api.moments import create_moments_router

# =============================================================================
# LOGGING SETUP
# =============================================================================

_project_root = Path(__file__).parent.parent.parent
_log_dir = _project_root / "data" / "logs"
_log_dir.mkdir(parents=True, exist_ok=True)

# Configure file logging
_file_handler = logging.FileHandler(_log_dir / "backend.log")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
logging.getLogger().addHandler(_file_handler)

# Also log uvicorn access/errors
logging.getLogger("uvicorn").addHandler(_file_handler)
logging.getLogger("uvicorn.access").addHandler(_file_handler)
logging.getLogger("uvicorn.error").addHandler(_file_handler)

logger = logging.getLogger(__name__)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ActionRequest(BaseModel):
    """Request for a player action."""
    playthrough_id: str
    action: str
    player_id: str = "char_player"
    location: Optional[str] = None
    stream: bool = False  # If true, returns SSE stream instead of JSON


class SceneResponse(BaseModel):
    """Response containing a scene."""
    scene: Dict[str, Any]
    time_elapsed: str


class DialogueChunk(BaseModel):
    """A single chunk of streamed dialogue."""
    speaker: Optional[str] = None  # Character ID if dialogue, None for narration
    text: str


class NewPlaythroughRequest(BaseModel):
    """Request to create a new playthrough."""
    drive: str  # BLOOD, OATH, or SHADOW
    companion: str = "char_aldric"
    initial_goal: Optional[str] = None


class ScenarioPlaythroughRequest(BaseModel):
    """Request to create a playthrough from a scenario."""
    scenario_id: str  # e.g. "thornwick_betrayed"
    player_name: str
    player_gender: str  # "male" or "female"


class QueryRequest(BaseModel):
    """Request for semantic query."""
    query: str


# =============================================================================
# APPLICATION FACTORY
# =============================================================================

def create_app(
    graph_name: str = "blood_ledger",
    host: str = "localhost",
    port: int = 6379,
    playthroughs_dir: str = "playthroughs"
) -> FastAPI:
    """
    Create the FastAPI application.

    Args:
        graph_name: FalkorDB graph name
        host: FalkorDB host
        port: FalkorDB port
        playthroughs_dir: Directory for playthrough data

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Blood Ledger API",
        description="API for The Blood Ledger narrative RPG",
        version="0.1.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Per-playthrough orchestrators
    _orchestrators: Dict[str, Orchestrator] = {}
    _debug_sse_clients: list = []  # list of queues for debug/mutation events
    _playthroughs_dir = Path(playthroughs_dir)

    # Register mutation listener to broadcast to debug SSE clients
    def _mutation_event_handler(event: Dict[str, Any]):
        """Handle mutation events and broadcast to debug SSE clients."""
        for queue in _debug_sse_clients:
            try:
                queue.put_nowait(event)
            except:
                pass  # Queue full or closed

    add_mutation_listener(_mutation_event_handler)

    def get_orchestrator(playthrough_id: str) -> Orchestrator:
        """Get or create orchestrator for a playthrough."""
        if playthrough_id not in _orchestrators:
            _orchestrators[playthrough_id] = Orchestrator(
                playthrough_id=playthrough_id,
                graph_name=graph_name,
                host=host,
                port=port,
                playthroughs_dir=playthroughs_dir
            )
        return _orchestrators[playthrough_id]

    def get_graph_queries() -> GraphQueries:
        """Get graph queries instance for default graph."""
        return GraphQueries(graph_name=graph_name, host=host, port=port)

    def get_playthrough_queries(playthrough_id: str) -> GraphQueries:
        """Get graph queries instance for a specific playthrough."""
        from engine.db import get_playthrough_graph_name
        pt_graph_name = get_playthrough_graph_name(playthrough_id)
        return GraphQueries(graph_name=pt_graph_name, host=host, port=port)

    def get_graph_ops() -> GraphOps:
        """Get graph ops instance."""
        return GraphOps(graph_name=graph_name, host=host, port=port)

    # =========================================================================
    # MOMENTS ROUTER (Moment Graph API)
    # =========================================================================

    # Mount the moments API router for moment graph operations
    # Endpoints: GET /api/moments/current, POST /api/moments/click, etc.
    moments_router = create_moments_router(
        host=host,
        port=port,
        playthroughs_dir=playthroughs_dir
    )
    app.include_router(moments_router, prefix="/api")

    # =========================================================================
    # HEALTH CHECK
    # =========================================================================

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

    # =========================================================================
    # PLAYTHROUGH ENDPOINTS
    # =========================================================================

    @app.post("/api/playthrough")
    async def create_playthrough(request: NewPlaythroughRequest):
        """
        Create a new playthrough.

        Sets up playthrough directory for mutations and world injections.
        Player psychology tracked in narrator's conversation context.
        Story notes live in the graph (narrative.narrator_notes, tension.narrator_notes).
        """
        import uuid
        playthrough_id = f"pt_{uuid.uuid4().hex[:8]}"
        playthrough_dir = _playthroughs_dir / playthrough_id
        playthrough_dir.mkdir(parents=True, exist_ok=True)

        # Create mutations directory
        (playthrough_dir / "mutations").mkdir(exist_ok=True)

        # Initialize orchestrator
        get_orchestrator(playthrough_id)

        return {
            "playthrough_id": playthrough_id,
            "drive": request.drive,
            "companion": request.companion,
            "status": "created"
        }

    @app.post("/api/playthrough/scenario")
    async def create_scenario_playthrough(request: ScenarioPlaythroughRequest):
        """
        Create a new playthrough from a scenario.

        1. Creates playthrough folder structure
        2. Loads scenario YAML
        3. Applies scenario nodes/links/tensions to graph
        4. Saves player.yaml with character info
        5. Creates initial scene.json from scenario opening
        """
        import uuid
        import yaml

        # Validate scenario exists
        scenarios_dir = Path(__file__).parent.parent.parent / "scenarios"
        scenario_file = scenarios_dir / f"{request.scenario_id}.yaml"

        if not scenario_file.exists():
            raise HTTPException(status_code=404, detail=f"Scenario not found: {request.scenario_id}")

        # Load scenario
        scenario = yaml.safe_load(scenario_file.read_text())

        # Generate playthrough ID
        playthrough_id = f"pt_{uuid.uuid4().hex[:8]}"
        playthrough_dir = _playthroughs_dir / playthrough_id
        playthrough_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (playthrough_dir / "mutations").mkdir(exist_ok=True)
        (playthrough_dir / "conversations").mkdir(exist_ok=True)

        # Save player.yaml
        player_data = {
            "name": request.player_name,
            "gender": request.player_gender,
            "scenario": request.scenario_id,
            "created": datetime.utcnow().isoformat()
        }
        (playthrough_dir / "player.yaml").write_text(yaml.dump(player_data))

        # Apply scenario to graph
        from engine.db import GraphOps
        graph_ops = GraphOps(graph_name=graph_name, host=host, port=port)

        # Update player node with name/gender in scenario data
        for node in scenario.get("nodes", []):
            if node.get("id") == "char_player":
                node["name"] = request.player_name
                node["gender"] = request.player_gender

        # Apply nodes, links, tensions
        try:
            result = graph_ops.apply(data=scenario, playthrough=playthrough_id)
            logger.info(f"Applied scenario {request.scenario_id}: {result}")
        except Exception as e:
            logger.error(f"Failed to apply scenario: {e}")
            # Continue anyway - scenario may have partial success

        # Create initial scene.json from scenario opening
        opening = scenario.get("opening", {})
        initial_scene = {
            "id": f"scene_{request.scenario_id}_opening",
            "location": {
                "place": scenario.get("location", "place_unknown"),
                "name": scenario.get("name", "Unknown"),
                "region": "England",
                "time": opening.get("time", "dawn")
            },
            "characters": opening.get("characters_present", []),
            "atmosphere": [opening.get("weather", "")],
            "narration": [
                {"text": line.strip(), "clickable": {}}
                for line in opening.get("narration", "").strip().split("\n")
                if line.strip()
            ],
            "voices": []
        }
        (playthrough_dir / "scene.json").write_text(json.dumps(initial_scene, indent=2))

        # Initialize orchestrator
        get_orchestrator(playthrough_id)

        return {
            "playthrough_id": playthrough_id,
            "scenario": request.scenario_id,
            "player_name": request.player_name,
            "player_gender": request.player_gender,
            "status": "created"
        }

    @app.get("/api/playthrough/{playthrough_id}")
    async def get_playthrough(playthrough_id: str):
        """Get playthrough status and info."""
        playthrough_dir = _playthroughs_dir / playthrough_id
        if not playthrough_dir.exists():
            raise HTTPException(status_code=404, detail="Playthrough not found")

        return {
            "playthrough_id": playthrough_id,
            "has_world_injection": (playthrough_dir / "world_injection.md").exists()
        }

    # =========================================================================
    # MOMENT GRAPH ENDPOINTS
    # =========================================================================

    class MomentClickRequest(BaseModel):
        """Request for clicking a word using Moment Graph architecture."""
        playthrough_id: str
        moment_id: str
        word: str
        player_id: str = "char_player"

    class MomentClickResponse(BaseModel):
        """Response for Moment Graph click."""
        flipped: bool
        flipped_moments: list
        weight_updates: list
        queue_narrator: bool

    @app.post("/api/moment/click", response_model=MomentClickResponse)
    async def moment_click(request: MomentClickRequest):
        """
        Handle a word click using the Moment Graph architecture.

        This is the instant-response path (<50ms target).
        No LLM calls in this path.

        1. Find CAN_LEAD_TO links from moment where word is in require_words
        2. Apply weight_transfer to target moments
        3. Check for flips (weight > 0.8)
        4. Return flipped moments, or queue_narrator=True if nothing flips
        """
        try:
            ops = get_graph_ops()
            result = ops.handle_click(
                moment_id=request.moment_id,
                clicked_word=request.word,
                player_id=request.player_id
            )
            return MomentClickResponse(**result)
        except Exception as e:
            logger.error(f"Moment click failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/moment/view/{playthrough_id}")
    async def get_moment_view(
        playthrough_id: str,
        location_id: str = Query(..., description="Current location ID"),
        player_id: str = Query("char_player", description="Player character ID")
    ):
        """
        Get the current view using Moment Graph architecture.

        Returns moments visible to player at location, ordered by weight.
        This replaces scene.json reads with live graph queries.
        """
        try:
            read = get_playthrough_queries(playthrough_id)
            view = read.get_current_view(
                player_id=player_id,
                location_id=location_id
            )
            return view
        except Exception as e:
            logger.error(f"Get moment view failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/view/{playthrough_id}")
    async def get_current_view(
        playthrough_id: str,
        player_id: str = Query("char_player", description="Player character ID"),
        location_id: Optional[str] = Query(
            None,
            description="Override location ID; defaults to player's current AT edge"
        )
    ):
        """
        Resolve the player's current location (unless overridden) and return the
        CurrentView payload described in docs/engine/moments/API_Moments.md.
        """
        try:
            read = get_playthrough_queries(playthrough_id)
            resolved_location_id = location_id
            location = None

            if not resolved_location_id:
                location = read.get_player_location(player_id=player_id)
                if not location:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Player '{player_id}' has no AT link. Move the player before requesting view."
                    )
                resolved_location_id = location.get("id")

            view = read.get_current_view(
                player_id=player_id,
                location_id=resolved_location_id
            )

            # If we already fetched location data, ensure the view includes it.
            if location:
                view["location"] = location

            return view
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get current view failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/moment/view/{playthrough_id}/scene-tree")
    async def get_moment_view_as_scene_tree(
        playthrough_id: str,
        location_id: str = Query(..., description="Current location ID"),
        player_id: str = Query("char_player", description="Player character ID")
    ):
        """
        Get the current view as a SceneTree for backward compatibility.

        Fetches from Moment Graph but converts to SceneTree format
        so existing frontend components work unchanged.
        """
        try:
            from engine.db.graph_queries import view_to_scene_tree

            read = get_playthrough_queries(playthrough_id)
            view = read.get_current_view(
                player_id=player_id,
                location_id=location_id
            )
            scene_tree = view_to_scene_tree(view)
            return {"scene": scene_tree}
        except Exception as e:
            logger.error(f"Get scene tree failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/moment/weight")
    async def update_moment_weight(request: Request):
        """
        Manually update a moment's weight.

        Request body: {"moment_id": "...", "weight_delta": 0.2, "reason": "..."}
        """
        try:
            body = await request.json()
            ops = get_graph_ops()
            result = ops.update_moment_weight(
                moment_id=body.get("moment_id"),
                weight_delta=body.get("weight_delta", 0.0),
                reason=body.get("reason", "api_call")
            )
            return result
        except Exception as e:
            logger.error(f"Weight update failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # DEBUG SSE ENDPOINT (Graph Mutations)
    # =========================================================================

    @app.get("/api/debug/stream")
    async def debug_stream(request: Request):
        """
        SSE endpoint for graph mutation events.

        Clients connect here to receive real-time updates when mutations are applied.
        Events include: apply_start, node_created, link_created, movement, apply_complete

        Use this for the debug panel in the frontend.
        """
        async def event_generator() -> AsyncGenerator[str, None]:
            queue = asyncio.Queue(maxsize=100)

            # Register this client
            _debug_sse_clients.append(queue)

            try:
                # Send initial connection event
                yield f"event: connected\ndata: {{\"message\": \"Debug stream connected\"}}\n\n"

                while True:
                    # Check if client disconnected
                    if await request.is_disconnected():
                        break

                    try:
                        # Wait for events with timeout
                        event = await asyncio.wait_for(queue.get(), timeout=30)
                        event_type = event.get('type', 'mutation')
                        yield f"event: {event_type}\ndata: {json.dumps(event)}\n\n"
                    except asyncio.TimeoutError:
                        # Send keepalive
                        yield f"event: ping\ndata: {{}}\n\n"
            finally:
                # Unregister client
                if queue in _debug_sse_clients:
                    _debug_sse_clients.remove(queue)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    # =========================================================================
    # VIEW ENDPOINTS
    # =========================================================================

    @app.get("/api/{playthrough_id}/map")
    async def get_map(playthrough_id: str, player_id: str = "char_player"):
        """
        Get map data showing places and connections.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get all places
            places = read.query("""
                MATCH (p:Place)
                RETURN p.id, p.name, p.type, p.mood
            """)

            # Get connections
            connections = read.query("""
                MATCH (p1:Place)-[r:CONNECTS]->(p2:Place)
                WHERE r.path > 0.5
                RETURN p1.id, p2.id, r.path_distance, r.path_difficulty
            """)

            # Get player location
            player_loc = read.query(f"""
                MATCH (c:Character {{id: '{player_id}'}})-[:AT]->(p:Place)
                RETURN p.id
            """)

            # Handle dict results from FalkorDB
            player_location = None
            if player_loc and player_loc[0]:
                if isinstance(player_loc[0], dict):
                    player_location = player_loc[0].get('p.id')
                else:
                    player_location = player_loc[0][0]

            return {
                "places": places,
                "connections": connections,
                "player_location": player_location
            }
        except Exception as e:
            logger.error(f"Failed to get map: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/ledger")
    async def get_ledger(playthrough_id: str, player_id: str = "char_player"):
        """
        Get ledger data showing debts, oaths, and blood ties.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get core narratives (oath, debt, blood) that player believes
            ledger_items = read.query(f"""
                MATCH (c:Character {{id: '{player_id}'}})-[b:BELIEVES]->(n:Narrative)
                WHERE n.type IN ['oath', 'debt', 'blood', 'enmity']
                  AND b.heard > 0.5
                RETURN n.id, n.name, n.content, n.type, n.tone, b.believes
                ORDER BY b.believes DESC
            """)

            return {"items": ledger_items}
        except Exception as e:
            logger.error(f"Failed to get ledger: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/faces")
    async def get_faces(playthrough_id: str, player_id: str = "char_player"):
        """
        Get faces data showing known characters.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get characters the player knows about (major characters and those in narratives)
            # Note: about_characters is stored as JSON string, so we use a simpler query
            characters = read.query("""
                MATCH (c:Character)
                WHERE c.type IN ['major', 'minor'] AND c.type <> 'player'
                RETURN DISTINCT c.id, c.name, c.type, c.face
            """)

            # Get companion info
            companions = read.query("""
                MATCH (c:Character {type: 'companion'})
                RETURN c.id, c.name, c.face, c.voice_tone
            """)

            return {
                "known_characters": characters,
                "companions": companions
            }
        except Exception as e:
            logger.error(f"Failed to get faces: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/chronicle")
    async def get_chronicle(playthrough_id: str, player_id: str = "char_player"):
        """
        Get chronicle data showing event history.
        """
        try:
            read = get_playthrough_queries(playthrough_id)

            # Get memory and account narratives the player believes
            events = read.query(f"""
                MATCH (c:Character {{id: '{player_id}'}})-[b:BELIEVES]->(n:Narrative)
                WHERE n.type IN ['memory', 'account']
                  AND b.heard > 0.5
                RETURN n.id, n.name, n.content, n.type, n.tone, b.believes
                ORDER BY n.weight DESC
                LIMIT 50
            """)

            return {"events": events}
        except Exception as e:
            logger.error(f"Failed to get chronicle: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # QUERY ENDPOINT
    # =========================================================================

    @app.post("/api/{playthrough_id}/query")
    async def semantic_query_post(playthrough_id: str, request: QueryRequest):
        """
        Natural language query via embeddings (POST).
        """
        try:
            from engine.queries import get_semantic_search
            search = get_semantic_search(graph_name=graph_name, host=host, port=port)
            results = search.find(request.query, limit=10)
            return {"results": results, "query": request.query}
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/{playthrough_id}/query")
    async def semantic_query_get(playthrough_id: str, query: str = Query(..., description="Search query")):
        """
        Natural language query via embeddings (GET).
        """
        try:
            from engine.queries import get_semantic_search
            search = get_semantic_search(graph_name=graph_name, host=host, port=port)
            results = search.find(query, limit=10)
            return {"results": results, "query": query}
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # INJECTION ENDPOINT
    # =========================================================================

    @app.post("/api/inject")
    async def inject_event(request: Request):
        """
        Write an injection to the queue for hook processing.
        Used by frontend for player UI actions (stop, location change, etc.)
        """
        try:
            body = await request.json()
            injection_file = _playthroughs_dir / "default" / "injection_queue.jsonl"
            injection_file.parent.mkdir(parents=True, exist_ok=True)

            with open(injection_file, "a") as f:
                f.write(json.dumps(body) + "\n")

            return {"status": "ok", "injection": body}
        except Exception as e:
            logger.error(f"Failed to inject: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # =========================================================================
    # PLAYTHROUGH CREATION
    # =========================================================================

    class PlaythroughCreateRequest(BaseModel):
        """Request to create a new playthrough."""
        scenario_id: str
        player_name: str
        player_gender: str = "male"

    # Track running narrator processes per playthrough
    _narrator_processes: Dict[str, subprocess.Popen] = {}

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

    @app.post("/api/playthrough/create")
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
        from engine.db.graph_ops import GraphOps

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
            load_initial_state(playthrough_graph_name, host, port)
            logger.info(f"Seed data loaded for {playthrough_graph_name}")
        except Exception as e:
            logger.error(f"Failed to load seed data: {e}")
            # Continue anyway - scenario may still work

        # Inject scenario nodes and links into graph
        try:
            graph = GraphOps(graph_name=playthrough_graph_name, host=host, port=port)

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
            companion_id = scenario.get("companion", {}).get("id", "char_aldric")

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

    class MomentRequest(BaseModel):
        """Request to send a player moment."""
        playthrough_id: str
        text: str
        moment_type: str = "player_freeform"  # player_freeform, player_click, player_choice

    @app.post("/api/moment")
    async def send_moment(request: MomentRequest):
        """
        Send a player moment (async).

        1. Append to message_queue.json
        2. If narrator not running: spawn it with scene.json + injection_queue.json
        3. Return immediately
        """
        import subprocess

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
                queries = get_playthrough_queries(request.playthrough_id)
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

    @app.get("/api/{playthrough_id}/discussion/{char_id}/topics")
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

    @app.get("/api/{playthrough_id}/discussion/{char_id}/topic/{topic_id}")
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

    @app.post("/api/{playthrough_id}/discussion/{char_id}/use-branch")
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

    return app


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

# Use absolute path to project root's playthroughs directory
_project_root = Path(__file__).parent.parent.parent
_default_playthroughs = str(_project_root / "playthroughs")

app = create_app(playthroughs_dir=_default_playthroughs)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

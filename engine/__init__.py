"""
Blood Ledger — Game Engine

The complete backend for The Blood Ledger narrative RPG.

Modules:
- models: Pydantic data models (Character, Place, Thing, Narrative, etc.)
- db: FalkorDB operations (GraphOps, GraphQueries)
- embeddings: Semantic embedding service
- queries: Natural language query layer
- physics: Graph tick engine (energy, decay, pressure, flips)
- orchestration: Main loop (Orchestrator, Narrator, World Runner)
- api: FastAPI endpoints

Quick Start:
    # Start the server
    python run.py

    # Or use the API directly
    from engine.orchestration import Orchestrator
    orch = Orchestrator()
    scene = orch.process_action("look around")
"""

__version__ = "0.1.0"

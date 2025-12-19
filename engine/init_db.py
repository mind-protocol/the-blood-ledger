#!/usr/bin/env python3
"""
Blood Ledger — Database Initialization

Creates schema indexes and loads initial game state.

Usage:
    python init_db.py
    python init_db.py --host localhost --port 6379
"""

import argparse
import logging
import redis
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_indexes(r: redis.Redis, graph_name: str):
    """Create indexes for efficient querying."""
    indexes = [
        # Node ID indexes (primary lookups)
        "CREATE INDEX FOR (n:Character) ON (n.id)",
        "CREATE INDEX FOR (n:Place) ON (n.id)",
        "CREATE INDEX FOR (n:Thing) ON (n.id)",
        "CREATE INDEX FOR (n:Narrative) ON (n.id)",
        "CREATE INDEX FOR (n:Tension) ON (n.id)",

        # Type indexes (filtering)
        "CREATE INDEX FOR (n:Character) ON (n.type)",
        "CREATE INDEX FOR (n:Place) ON (n.type)",
        "CREATE INDEX FOR (n:Narrative) ON (n.type)",

        # Name indexes (search)
        "CREATE INDEX FOR (n:Character) ON (n.name)",
        "CREATE INDEX FOR (n:Place) ON (n.name)",
        "CREATE INDEX FOR (n:Thing) ON (n.name)",
        "CREATE INDEX FOR (n:Narrative) ON (n.name)",
    ]

    for cypher in indexes:
        try:
            r.execute_command('GRAPH.QUERY', graph_name, cypher)
            logger.info(f"Created index: {cypher.split('ON')[1].strip()}")
        except Exception as e:
            if "already exists" in str(e).lower():
                logger.debug(f"Index already exists: {cypher}")
            else:
                logger.warning(f"Index creation failed: {e}")


def load_initial_state(graph_name: str, host: str, port: int):
    """Load initial game state from YAML."""
    from engine.physics.graph.graph_ops import GraphOps

    graph = GraphOps(graph_name=graph_name, host=host, port=port)

    # First load world data from data/world/*.yaml
    # These are flat lists, need to wrap them in {nodes: [...]} or {links: [...]} format
    import yaml as yaml_module
    world_dir = Path(__file__).parent.parent / "data" / "world"
    if world_dir.exists():
        # Phase 1: Load nodes first (order matters for references)
        node_files = {
            "places.yaml": "place",
            "places_minor.yaml": "place",
            "characters.yaml": "character",
            "things.yaml": "thing",
            "narratives.yaml": "narrative",
            "tensions.yaml": "tension",
            "events.yaml": "event",
        }
        for filename, node_type in node_files.items():
            world_file = world_dir / filename
            if world_file.exists():
                logger.info(f"Loading world nodes: {filename}")
                try:
                    raw_items = yaml_module.safe_load(world_file.read_text())
                    if raw_items and isinstance(raw_items, list):
                        nodes = []
                        for item in raw_items:
                            item["type"] = node_type
                            nodes.append(item)
                        result = graph.apply(data={"nodes": nodes, "links": []})
                        if result.success:
                            logger.info(f"  Loaded {len(result.persisted)} {node_type}s")
                        else:
                            for error in result.errors[:3]:
                                logger.warning(f"  Error: {error['item']}: {error['message']}")
                except Exception as e:
                    logger.error(f"  Failed to load {filename}: {e}")

        # Phase 2: Load links (after nodes exist)
        link_files = {
            "routes.yaml": "geography",
            "beliefs.yaml": "belief",
            "holdings.yaml": "holding",
            "thing_locations.yaml": "thing_location",
            "thing_ownership.yaml": "thing_ownership",
        }
        for filename, link_type in link_files.items():
            world_file = world_dir / filename
            if world_file.exists():
                logger.info(f"Loading world links: {filename}")
                try:
                    raw_items = yaml_module.safe_load(world_file.read_text())
                    if raw_items and isinstance(raw_items, list):
                        links = []
                        for item in raw_items:
                            item["type"] = link_type
                            links.append(item)
                        result = graph.apply(data={"nodes": [], "links": links})
                        if result.success:
                            logger.info(f"  Loaded {len(result.persisted)} {link_type} links")
                        else:
                            for error in result.errors[:3]:
                                logger.warning(f"  Error: {error['item']}: {error['message']}")
                except Exception as e:
                    logger.error(f"  Failed to load {filename}: {e}")

    # Then load initial state (core narratives, beliefs, presences)
    init_file = Path(__file__).parent / "data" / "init" / "initial_state.yaml"

    if not init_file.exists():
        logger.error(f"Initial state file not found: {init_file}")
        return False

    logger.info(f"Loading initial state from: {init_file}")
    result = graph.apply(path=str(init_file))

    if result.success:
        logger.info(f"Loaded {len(result.persisted)} items successfully")
        if result.has_duplicates:
            logger.warning(f"Found {len(result.duplicates)} potential duplicates")
    else:
        logger.error(f"Errors during load:")
        for error in result.errors:
            logger.error(f"  {error['item']}: {error['message']}")
            logger.info(f"    Fix: {error['fix']}")

    return result.success


def verify_data(r: redis.Redis, graph_name: str):
    """Verify initial data was loaded."""
    queries = [
        ("Characters", "MATCH (n:Character) RETURN count(n)"),
        ("Places", "MATCH (n:Place) RETURN count(n)"),
        ("Narratives", "MATCH (n:Narrative) RETURN count(n)"),
        ("Tensions", "MATCH (n:Tension) RETURN count(n)"),
        ("Beliefs", "MATCH ()-[r:BELIEVES]->() RETURN count(r)"),
        ("Presences", "MATCH ()-[r:AT]->() RETURN count(r)"),
        ("Geography", "MATCH ()-[r:CONNECTS]->() RETURN count(r)"),
    ]

    logger.info("\n=== Database Contents ===")
    for name, cypher in queries:
        try:
            result = r.execute_command('GRAPH.QUERY', graph_name, cypher)
            # FalkorDB returns [[[count]], stats]
            count = result[0][0][0] if result and result[0] else 0
            logger.info(f"  {name}: {count}")
        except Exception as e:
            logger.warning(f"  {name}: error - {e}")


def main():
    parser = argparse.ArgumentParser(description='Initialize Blood Ledger database')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--graph', default='blood_ledger', help='Graph name')
    parser.add_argument('--skip-data', action='store_true', help='Skip loading initial data')
    args = parser.parse_args()

    logger.info(f"Connecting to FalkorDB at {args.host}:{args.port}")

    try:
        r = redis.Redis(host=args.host, port=args.port, decode_responses=True)
        r.ping()
        logger.info("Connected successfully")
    except redis.exceptions.ConnectionError:
        logger.error(f"Cannot connect to FalkorDB at {args.host}:{args.port}")
        logger.info("Start FalkorDB with: redis-server --loadmodule /path/to/falkordb.so")
        return 1

    # Check if FalkorDB module is loaded
    modules = r.execute_command('MODULE', 'LIST')
    has_graph = any(m[1] == b'graph' or m[1] == 'graph' for m in modules)
    if not has_graph:
        logger.error("FalkorDB module not loaded. Start Redis with --loadmodule falkordb.so")
        return 1

    logger.info(f"Initializing graph: {args.graph}")

    # Create indexes
    logger.info("\n=== Creating Indexes ===")
    create_indexes(r, args.graph)

    # Load initial data
    if not args.skip_data:
        logger.info("\n=== Loading Initial State ===")
        if not load_initial_state(args.graph, args.host, args.port):
            logger.error("Failed to load initial state")
            return 1

    # Verify
    verify_data(r, args.graph)

    logger.info("\n=== Initialization Complete ===")
    logger.info(f"Graph '{args.graph}' is ready")
    logger.info(f"View in browser: http://localhost:3000")

    return 0


if __name__ == "__main__":
    exit(main())

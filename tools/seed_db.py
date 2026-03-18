#!/usr/bin/env python3
"""
Seed FalkorDB with ngram schema data.

Loads nodes and links from data/ngram/ YAML files into FalkorDB.

Usage:
    # Seed the default 'seed' graph
    python tools/seed_db.py

    # Seed a specific graph
    python tools/seed_db.py --graph my_graph

    # Copy to test graph after seeding
    python tools/seed_db.py --copy-to test

    # Clear existing data first
    python tools/seed_db.py --clear
"""

import argparse
import json
import logging
import sys
import yaml
from pathlib import Path
from typing import Any

from falkordb import FalkorDB

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# Node type to FalkorDB label mapping
NODE_TYPE_TO_LABEL = {
    "actor": "Actor",
    "space": "Space",
    "thing": "Thing",
    "narrative": "Narrative",
    "moment": "Moment",
}

# Link type to FalkorDB relationship type mapping
LINK_TYPE_TO_REL = {
    "contains": "CONTAINS",
    "leads_to": "LEADS_TO",
    "expresses": "EXPRESSES",
    "relates": "RELATES",
    "attached_to": "ATTACHED_TO",
    "sequence": "SEQUENCE",
    "primes": "PRIMES",
    "can_become": "CAN_BECOME",
    "about": "ABOUT",
}


class SeedDB:
    """Seeds FalkorDB with ngram data."""

    def __init__(
        self,
        graph_name: str = "seed",
        host: str = "localhost",
        port: int = 6379,
        data_dir: Path = None
    ):
        self.graph_name = graph_name
        self.host = host
        self.port = port
        self.data_dir = data_dir or Path(__file__).parent.parent / "data" / "ngram"

        # Connect to FalkorDB
        try:
            self.db = FalkorDB(host=host, port=port)
            self.graph = self.db.select_graph(graph_name)
            logger.info(f"Connected to FalkorDB graph: {graph_name}")
        except Exception as e:
            logger.error(f"Failed to connect to FalkorDB: {e}")
            raise

    def _query(self, cypher: str, params: dict = None) -> list:
        """Execute a Cypher query."""
        try:
            result = self.graph.query(cypher, params or {})
            return result.result_set if result.result_set else []
        except Exception as e:
            logger.warning(f"Query failed: {e}")
            logger.debug(f"Query was: {cypher}")
            logger.debug(f"Params: {params}")
            raise

    def clear_graph(self) -> None:
        """Clear all data from the graph."""
        logger.info(f"Clearing graph: {self.graph_name}")
        self._query("MATCH (n) DETACH DELETE n")
        logger.info("Graph cleared")

    def load_yaml(self, filename: str) -> list:
        """Load a YAML file from data_dir."""
        path = self.data_dir / filename
        if not path.exists():
            logger.warning(f"File not found: {path}")
            return []
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return data if data else []

    def create_node(self, node: dict) -> bool:
        """Create a single node in FalkorDB."""
        node_type = node.get("node_type")
        label = NODE_TYPE_TO_LABEL.get(node_type)

        if not label:
            logger.warning(f"Unknown node type: {node_type} for {node.get('id')}")
            return False

        node_id = node.get("id")
        if not node_id:
            logger.warning(f"Node missing id: {node}")
            return False

        # Build properties dict, excluding node_type (it's the label)
        props = {}
        for key, value in node.items():
            if key == "node_type":
                continue
            if value is None:
                continue

            # Handle special types
            if isinstance(value, (list, dict)):
                props[key] = json.dumps(value)
            else:
                props[key] = value

        # Use MERGE to upsert
        cypher = f"""
        MERGE (n:{label} {{id: $id}})
        SET n += $props
        """

        try:
            self._query(cypher, {"id": node_id, "props": props})
            return True
        except Exception as e:
            logger.error(f"Failed to create node {node_id}: {e}")
            return False

    def create_link(self, link: dict) -> bool:
        """Create a single link in FalkorDB."""
        link_type = link.get("type")
        rel_type = LINK_TYPE_TO_REL.get(link_type)

        if not rel_type:
            logger.warning(f"Unknown link type: {link_type}")
            return False

        node_a = link.get("node_a")
        node_b = link.get("node_b")

        if not node_a or not node_b:
            logger.warning(f"Link missing node_a or node_b: {link}")
            return False

        # Build properties dict
        props = {}
        for key, value in link.items():
            if key in ("type", "node_a", "node_b"):
                continue
            if value is None:
                continue

            if isinstance(value, (list, dict)):
                props[key] = json.dumps(value)
            else:
                props[key] = value

        # Match any node types for node_a and node_b
        cypher = f"""
        MATCH (a {{id: $node_a}})
        MATCH (b {{id: $node_b}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        """

        try:
            self._query(cypher, {"node_a": node_a, "node_b": node_b, "props": props})
            return True
        except Exception as e:
            logger.error(f"Failed to create link {node_a} -> {node_b}: {e}")
            return False

    def seed(self) -> tuple[int, int]:
        """
        Seed the database with nodes and links.

        Returns:
            Tuple of (nodes_created, links_created)
        """
        # Load data
        nodes = self.load_yaml("nodes.yaml")
        links = self.load_yaml("links.yaml")

        logger.info(f"Loaded {len(nodes)} nodes and {len(links)} links")

        # Create nodes
        nodes_created = 0
        for i, node in enumerate(nodes):
            if self.create_node(node):
                nodes_created += 1
            if (i + 1) % 50 == 0:
                logger.info(f"  Created {i + 1}/{len(nodes)} nodes...")

        logger.info(f"Created {nodes_created}/{len(nodes)} nodes")

        # Create links
        links_created = 0
        for i, link in enumerate(links):
            if self.create_link(link):
                links_created += 1
            if (i + 1) % 100 == 0:
                logger.info(f"  Created {i + 1}/{len(links)} links...")

        logger.info(f"Created {links_created}/{len(links)} links")

        return nodes_created, links_created

    def copy_to(self, target_graph: str) -> None:
        """
        Copy the current graph to another graph.

        Args:
            target_graph: Name of the target graph
        """
        logger.info(f"Copying {self.graph_name} to {target_graph}")

        # Get all nodes and links from current graph
        nodes = self._query("""
            MATCH (n)
            RETURN labels(n)[0] AS label, properties(n) AS props
        """)

        links = self._query("""
            MATCH (a)-[r]->(b)
            RETURN a.id AS from_id, b.id AS to_id, type(r) AS rel_type, properties(r) AS props
        """)

        # Switch to target graph
        target = self.db.select_graph(target_graph)

        # Clear target
        target.query("MATCH (n) DETACH DELETE n")

        # Create nodes in target
        for row in nodes:
            if len(row) >= 2:
                label = row[0]
                props = row[1]
                if isinstance(props, str):
                    props = json.loads(props)
                cypher = f"CREATE (n:{label} $props)"
                target.query(cypher, {"props": props})

        # Create links in target
        for row in links:
            if len(row) >= 4:
                from_id = row[0]
                to_id = row[1]
                rel_type = row[2]
                props = row[3]
                if isinstance(props, str):
                    props = json.loads(props)
                cypher = f"""
                    MATCH (a {{id: $from_id}})
                    MATCH (b {{id: $to_id}})
                    CREATE (a)-[r:{rel_type}]->(b)
                    SET r = $props
                """
                try:
                    target.query(cypher, {"from_id": from_id, "to_id": to_id, "props": props})
                except Exception as e:
                    logger.warning(f"Failed to copy link {from_id} -> {to_id}: {e}")

        logger.info(f"Copied {len(nodes)} nodes and {len(links)} links to {target_graph}")

    def get_stats(self) -> dict:
        """Get statistics about the current graph."""
        stats = {}

        # Count nodes by label
        for label in NODE_TYPE_TO_LABEL.values():
            result = self._query(f"MATCH (n:{label}) RETURN count(n)")
            stats[label.lower() + "_count"] = result[0][0] if result else 0

        # Count links by type
        for rel_type in LINK_TYPE_TO_REL.values():
            result = self._query(f"MATCH ()-[r:{rel_type}]->() RETURN count(r)")
            stats[rel_type.lower() + "_count"] = result[0][0] if result else 0

        return stats


def main():
    parser = argparse.ArgumentParser(
        description="Seed FalkorDB with ngram schema data"
    )
    parser.add_argument(
        "--graph", "-g",
        type=str,
        default="seed",
        help="Graph name to seed (default: seed)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="FalkorDB host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6379,
        help="FalkorDB port (default: 6379)"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Data directory containing nodes.yaml and links.yaml"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before seeding"
    )
    parser.add_argument(
        "--copy-to",
        type=str,
        default=None,
        help="Copy seeded graph to another graph after seeding"
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show stats, don't seed"
    )

    args = parser.parse_args()

    try:
        seeder = SeedDB(
            graph_name=args.graph,
            host=args.host,
            port=args.port,
            data_dir=args.data_dir
        )

        if args.stats_only:
            stats = seeder.get_stats()
            print("\nGraph Statistics:")
            print("-" * 40)
            for key, value in stats.items():
                print(f"  {key}: {value}")
            return 0

        if args.clear:
            seeder.clear_graph()

        nodes_created, links_created = seeder.seed()

        if args.copy_to:
            seeder.copy_to(args.copy_to)

        print(f"\nSeeding complete!")
        print(f"  Nodes: {nodes_created}")
        print(f"  Links: {links_created}")
        print(f"  Graph: {args.graph}")

        if args.copy_to:
            print(f"  Copied to: {args.copy_to}")

        return 0

    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

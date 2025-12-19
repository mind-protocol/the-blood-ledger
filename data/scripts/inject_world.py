#!/usr/bin/env python3
"""
Inject World Data into FalkorDB

Loads all world data from data/world/*.yaml and injects into FalkorDB.
Uses the GraphOps interface from engine/db/graph_ops.py.

Usage:
    python data/scripts/inject_world.py
    python data/scripts/inject_world.py --graph blood_ledger_test
    python data/scripts/inject_world.py --host localhost --port 6379
"""
# DOCS: docs/world/scraping/IMPLEMENTATION_World_Scraping_Pipeline_Architecture.md

import sys
import argparse
import logging
import yaml
from pathlib import Path

# Add engine to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "engine"))

from db.graph_ops import GraphOps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
WORLD_DIR = PROJECT_ROOT / "data" / "world"


def load_yaml(filename: Path) -> list:
    """Load data from YAML file."""
    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return []
    with open(filename, 'r') as f:
        return yaml.safe_load(f) or []


def inject_places(graph: GraphOps, places: list):
    """Inject Place nodes."""
    logger.info(f"Injecting {len(places)} places...")
    for place in places:
        try:
            graph.add_place(
                id=place["id"],
                name=place["name"],
                type=place.get("type", "village"),
                mood=place.get("mood"),
                detail=place.get("detail"),
            )
        except Exception as e:
            logger.error(f"  Failed to add place {place['id']}: {e}")


def inject_routes(graph: GraphOps, routes: list):
    """Inject geography links (routes between places)."""
    logger.info(f"Injecting {len(routes)} routes...")
    for route in routes:
        try:
            # Calculate difficulty from terrain
            terrain = route.get("path_terrain", "track")
            difficulty_map = {
                "roman_road": "easy",
                "track": "moderate",
                "forest": "hard",
                "moor": "hard",
                "marsh": "dangerous",
            }
            difficulty = difficulty_map.get(terrain, "moderate")

            # Format distance
            km = route.get("path_km", 0)
            hours = route.get("path_hours", 0)
            if hours >= 24:
                distance = f"{hours / 24:.1f} days"
            else:
                distance = f"{hours:.1f} hours"

            graph.add_geography(
                from_place_id=route["from_place"],
                to_place_id=route["to_place"],
                path=route.get("path", 1.0),
                path_distance=distance,
                path_difficulty=difficulty,
            )
        except Exception as e:
            logger.error(f"  Failed to add route {route['from_place']}->{route['to_place']}: {e}")


def inject_characters(graph: GraphOps, characters: list):
    """Inject Character nodes with full schema fields."""
    logger.info(f"Injecting {len(characters)} characters...")
    for char in characters:
        try:
            # Extract nested fields
            voice = char.get("voice", {})
            personality = char.get("personality", {})
            backstory = char.get("backstory", {})
            skills = char.get("skills", {})

            graph.add_character(
                id=char["id"],
                name=char["name"],
                type=char.get("type", "minor"),
                alive=char.get("alive", True),
                gender=char.get("gender"),
                face=char.get("face"),
                skills=skills if skills else None,
                voice_tone=voice.get("tone"),
                voice_style=voice.get("style"),
                approach=personality.get("approach"),
                values=personality.get("values"),
                flaw=personality.get("flaw"),
                backstory_family=backstory.get("family") or None,
                backstory_wound=backstory.get("wound") or None,
                backstory_why_here=backstory.get("why_here") or None,
                detail=char.get("detail"),
            )

            # If character has a base place, add presence
            base_place = char.get("_base_place")
            if base_place:
                try:
                    graph.add_presence(
                        character_id=char["id"],
                        place_id=base_place,
                        present=1.0,
                        visible=1.0,
                    )
                except Exception as e:
                    logger.warning(f"  Could not add presence for {char['id']} at {base_place}: {e}")

        except Exception as e:
            logger.error(f"  Failed to add character {char['id']}: {e}")


def inject_holdings(graph: GraphOps, holdings: list, characters: list):
    """Inject holding relationships as presence links."""
    logger.info(f"Processing {len(holdings)} holdings...")
    char_ids = {c["id"] for c in characters}

    for holding in holdings:
        holder = holding.get("holder")
        place = holding.get("place")

        if holder and holder in char_ids and place:
            try:
                # Add presence if not already added via base_place
                graph.add_presence(
                    character_id=holder,
                    place_id=place,
                    present=0.5,  # They control it but may not be physically there
                    visible=1.0,
                )
            except Exception as e:
                logger.debug(f"  Holding presence for {holder} at {place}: {e}")


def inject_events(graph: GraphOps, events: list):
    """Inject events as Narrative nodes of type 'memory'."""
    logger.info(f"Injecting {len(events)} events as narratives...")
    for event in events:
        try:
            # Map event impact to weight
            impact_weight = {
                "catastrophic": 1.0,
                "major": 0.8,
                "moderate": 0.6,
                "minor": 0.4,
                "local": 0.3,
            }
            weight = impact_weight.get(event.get("impact", "minor"), 0.5)

            graph.add_narrative(
                id=f"narr_{event['id'].replace('event_', '')}",
                name=event["name"],
                content=event["content"],
                type="memory",
                about_characters=event.get("characters"),
                about_places=event.get("places"),
                weight=weight,
                truth=1.0,  # Historical events are true
            )
        except Exception as e:
            logger.error(f"  Failed to add event {event['id']}: {e}")


def inject_things(graph: GraphOps, things: list):
    """Inject Thing nodes."""
    logger.info(f"Injecting {len(things)} things...")
    for thing in things:
        try:
            graph.add_thing(
                id=thing["id"],
                name=thing["name"],
                type=thing.get("type", "token"),
                portable=thing.get("portable", True),
                significance=thing.get("significance", "mundane"),
                quantity=thing.get("quantity", 1),
                description=thing.get("description", ""),
                detail=thing.get("detail"),
            )
        except Exception as e:
            logger.error(f"  Failed to add thing {thing['id']}: {e}")


def inject_thing_locations(graph: GraphOps, locations: list):
    """Inject thing-place links."""
    logger.info(f"Injecting {len(locations)} thing locations...")
    success = 0
    failed = 0

    for loc in locations:
        try:
            # Both "located" and "hidden" mean the thing is at the place
            # "hidden" additionally means it's concealed
            loc_type = loc.get("type", "located")
            graph.add_thing_location(
                thing_id=loc["thing"],
                place_id=loc["place"],
                located=1.0,  # Always 1.0 if it's at this place
                hidden=1.0 if loc_type == "hidden" else 0.0,
                specific_location=loc.get("specific_location", ""),
            )
            success += 1
        except Exception as e:
            failed += 1
            if failed <= 5:
                logger.debug(f"  Thing location {loc['thing']}->{loc['place']}: {e}")

    logger.info(f"  Thing locations: {success} success, {failed} failed")


def inject_thing_ownership(graph: GraphOps, ownership: list):
    """Inject character-thing links."""
    logger.info(f"Injecting {len(ownership)} thing ownership links...")
    success = 0
    failed = 0

    for own in ownership:
        try:
            # Both "carries" and "carries_hidden" mean the character has it
            # "carries_hidden" additionally means it's concealed
            own_type = own.get("type", "carries")
            graph.add_character_thing(
                character_id=own["character"],
                thing_id=own["thing"],
                carries=1.0,  # Always 1.0 if they have it
                carries_hidden=1.0 if own_type == "carries_hidden" else 0.0,
            )
            success += 1
        except Exception as e:
            failed += 1
            if failed <= 5:
                logger.debug(f"  Thing ownership {own['character']}->{own['thing']}: {e}")

    logger.info(f"  Thing ownership: {success} success, {failed} failed")


def inject_narratives(graph: GraphOps, narratives: list):
    """Inject Narrative nodes."""
    logger.info(f"Injecting {len(narratives)} narratives...")
    for narr in narratives:
        try:
            about = narr.get("about", {})
            graph.add_narrative(
                id=narr["id"],
                name=narr["name"],
                content=narr["content"],
                type=narr.get("type", "memory"),
                about_characters=about.get("characters"),
                about_places=about.get("places"),
                about_things=about.get("things"),
                truth=narr.get("truth", 1.0),
                weight=0.5,
                occurred_at=narr.get("occurred_at"),
                occurred_where=narr.get("occurred_where"),
                detail=narr.get("detail"),
            )
        except Exception as e:
            logger.error(f"  Failed to add narrative {narr['id']}: {e}")


def inject_beliefs(graph: GraphOps, beliefs: list):
    """Inject belief relationships."""
    logger.info(f"Injecting {len(beliefs)} beliefs...")
    success = 0
    failed = 0

    for belief in beliefs:
        try:
            graph.add_belief(
                character_id=belief["character"],
                narrative_id=belief["narrative"],
                heard=belief.get("heard", 0.0),
                believes=belief.get("believes", 0.0),
                originated=belief.get("originated", 0.0),
                source=belief.get("source", "told" if belief.get("heard", 0) > 0 else "none"),
                where=belief.get("where"),  # Place ID where they learned this
            )
            success += 1
        except Exception as e:
            failed += 1
            # Only log first few failures
            if failed <= 5:
                logger.debug(f"  Belief {belief['character']}->{belief['narrative']}: {e}")

    logger.info(f"  Beliefs: {success} success, {failed} failed")


def inject_tensions(graph: GraphOps, tensions: list):
    """Inject Tension nodes."""
    logger.info(f"Injecting {len(tensions)} tensions...")
    for tension in tensions:
        try:
            graph.add_tension(
                id=tension["id"],
                narratives=tension.get("narratives", []),
                description=tension.get("description", ""),
                pressure=tension.get("pressure", 0.0),
                pressure_type=tension.get("pressure_type", "gradual"),
                breaking_point=tension.get("breaking_point", 0.9),
                base_rate=tension.get("base_rate", 0.001),
                trigger_at=tension.get("trigger_at"),
                detail=tension.get("detail"),
            )
        except Exception as e:
            logger.error(f"  Failed to add tension {tension['id']}: {e}")


def verify_data(graph: GraphOps):
    """Verify data was loaded by running count queries."""
    logger.info("\n=== Verification ===")

    queries = [
        ("Characters", "MATCH (n:Character) RETURN count(n)"),
        ("Places", "MATCH (n:Place) RETURN count(n)"),
        ("Things", "MATCH (n:Thing) RETURN count(n)"),
        ("Narratives", "MATCH (n:Narrative) RETURN count(n)"),
        ("Tensions", "MATCH (n:Tension) RETURN count(n)"),
        ("Beliefs", "MATCH ()-[r:BELIEVES]->() RETURN count(r)"),
        ("Presences", "MATCH ()-[r:AT]->() RETURN count(r)"),
        ("Geography", "MATCH ()-[r:CONNECTS]->() RETURN count(r)"),
        ("Thing Locations", "MATCH ()-[r:LOCATED_AT]->() RETURN count(r)"),
        ("Thing Ownership", "MATCH ()-[r:CARRIES]->() RETURN count(r)"),
    ]

    for name, cypher in queries:
        try:
            result = graph._query(cypher)
            count = result[0][0] if result and result[0] else 0
            logger.info(f"  {name}: {count}")
        except Exception as e:
            logger.warning(f"  {name}: error - {e}")


def clear_graph(graph: GraphOps):
    """Delete all nodes and relationships from the graph."""
    logger.info("Clearing existing data...")
    try:
        # Delete all relationships first, then nodes
        graph._query("MATCH ()-[r]->() DELETE r")
        graph._query("MATCH (n) DELETE n")
        logger.info("  Graph cleared")
    except Exception as e:
        logger.warning(f"  Clear failed (may be empty): {e}")


def main():
    parser = argparse.ArgumentParser(description='Inject world data into FalkorDB')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--graph', default='seed', help='Graph name')
    parser.add_argument('--skip-verify', action='store_true', help='Skip verification')
    parser.add_argument('--clear', action='store_true', help='Clear graph before injecting')
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("World Data Injection")
    logger.info("=" * 60)

    # Connect to FalkorDB
    try:
        graph = GraphOps(graph_name=args.graph, host=args.host, port=args.port)
        logger.info(f"Connected to FalkorDB: {args.graph} at {args.host}:{args.port}")
    except Exception as e:
        logger.error(f"Cannot connect to FalkorDB: {e}")
        logger.info("Start FalkorDB with: docker run -p 6379:6379 falkordb/falkordb")
        return 1

    # Clear graph if requested
    if args.clear:
        clear_graph(graph)

    # Load all YAML files
    logger.info(f"\nLoading data from {WORLD_DIR}")
    places = load_yaml(WORLD_DIR / "places.yaml")
    places_minor = load_yaml(WORLD_DIR / "places_minor.yaml")
    places.extend(places_minor)  # Combine main and minor places
    routes = load_yaml(WORLD_DIR / "routes.yaml")
    characters = load_yaml(WORLD_DIR / "characters.yaml")
    holdings = load_yaml(WORLD_DIR / "holdings.yaml")
    things = load_yaml(WORLD_DIR / "things.yaml")
    thing_locations = load_yaml(WORLD_DIR / "thing_locations.yaml")
    thing_ownership = load_yaml(WORLD_DIR / "thing_ownership.yaml")
    events = load_yaml(WORLD_DIR / "events.yaml")
    narratives = load_yaml(WORLD_DIR / "narratives.yaml")
    beliefs = load_yaml(WORLD_DIR / "beliefs.yaml")
    tensions = load_yaml(WORLD_DIR / "tensions.yaml")

    logger.info(f"  Places: {len(places)}")
    logger.info(f"  Routes: {len(routes)}")
    logger.info(f"  Characters: {len(characters)}")
    logger.info(f"  Holdings: {len(holdings)}")
    logger.info(f"  Things: {len(things)}")
    logger.info(f"  Thing Locations: {len(thing_locations)}")
    logger.info(f"  Thing Ownership: {len(thing_ownership)}")
    logger.info(f"  Events: {len(events)}")
    logger.info(f"  Narratives: {len(narratives)}")
    logger.info(f"  Beliefs: {len(beliefs)}")
    logger.info(f"  Tensions: {len(tensions)}")

    # Inject in order (dependencies first)
    logger.info("\n--- Injecting Data ---")

    # 1. Places first (geography depends on them)
    inject_places(graph, places)

    # 2. Routes (geography links)
    inject_routes(graph, routes)

    # 3. Characters (need places for presence)
    inject_characters(graph, characters)

    # 4. Holdings (character-place relationships)
    inject_holdings(graph, holdings, characters)

    # 5. Things (need places for locations, characters for ownership)
    inject_things(graph, things)

    # 6. Thing locations (thing-place links)
    inject_thing_locations(graph, thing_locations)

    # 7. Thing ownership (character-thing links)
    inject_thing_ownership(graph, thing_ownership)

    # 8. Events as narratives
    inject_events(graph, events)

    # 9. Narratives (need characters/places/things for about)
    inject_narratives(graph, narratives)

    # 10. Beliefs (need characters and narratives)
    inject_beliefs(graph, beliefs)

    # 11. Tensions (need narratives)
    inject_tensions(graph, tensions)

    # Verify
    if not args.skip_verify:
        verify_data(graph)

    logger.info("\n=== Injection Complete ===")
    logger.info(f"Graph '{args.graph}' populated with world data")

    return 0


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Migrate Blood Ledger world data to ngram schema v1.2

This script converts the existing YAML data files from the Blood Ledger format
to the new ngram unified graph schema.

Old Format (per-type files):
- characters.yaml → actors
- places.yaml, places_minor.yaml → spaces
- things.yaml → things
- narratives.yaml → narratives
- events.yaml → moments
- routes.yaml → leads_to links
- holdings.yaml → relates links (controls)
- thing_locations.yaml → contains links (space contains thing)
- thing_ownership.yaml → attached_to links (thing attached_to actor)
- beliefs.yaml → relates links (character believes narrative)
- tensions.yaml → relates links (narrative opposes narrative)

New Format (ngram schema v1.2):
- nodes.yaml: all nodes (actor, space, thing, narrative, moment)
- links.yaml: all links (contains, leads_to, expresses, relates, attached_to, etc.)
"""

import yaml
import argparse
import time
import uuid
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field, asdict


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Node:
    """Base node in ngram schema."""
    id: str
    name: str
    node_type: str  # actor, space, thing, narrative, moment
    type: str       # subtype (e.g., major, minor, city, village)
    description: str = ""
    weight: float = 1.0
    energy: float = 0.0
    created_at_s: int = 0
    updated_at_s: int = 0

    # Type-specific fields
    content: str | None = None  # narrative
    uri: str | None = None      # thing
    text: str | None = None     # moment
    status: str | None = None   # moment
    tick_created: int | None = None  # moment
    tick_resolved: int | None = None  # moment

    # Preserve extra fields for detail, image_prompt, etc.
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values and extra."""
        result = {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type,
            "type": self.type,
            "description": self.description,
            "weight": self.weight,
            "energy": self.energy,
            "created_at_s": self.created_at_s,
            "updated_at_s": self.updated_at_s,
        }

        # Add type-specific fields
        if self.node_type == "narrative" and self.content:
            result["content"] = self.content
        if self.node_type == "thing" and self.uri:
            result["uri"] = self.uri
        if self.node_type == "moment":
            if self.text:
                result["text"] = self.text
            if self.status:
                result["status"] = self.status
            if self.tick_created is not None:
                result["tick_created"] = self.tick_created
            if self.tick_resolved is not None:
                result["tick_resolved"] = self.tick_resolved

        # Add extra fields (detail, image_prompt, etc.)
        result.update(self.extra)

        return result


@dataclass
class Link:
    """Link in ngram schema."""
    id: str
    node_a: str
    node_b: str
    type: str  # contains, leads_to, expresses, relates, attached_to, etc.

    # Physics properties
    conductivity: float = 0.5
    weight: float = 1.0
    energy: float = 0.0
    strength: float = 0.0
    emotions: list = field(default_factory=list)

    # Semantic properties
    name: str = ""
    role: str | None = None  # originator, believer, witness, subject, creditor, debtor
    direction: str | None = None  # support, oppose, elaborate, subsume, supersede
    description: str = ""
    created_at_s: int = 0

    # Type-specific fields
    distance: str | None = None  # leads_to
    difficulty: str | None = None  # leads_to
    tick: int | None = None  # sequence
    trigger: str | None = None  # primes

    # Extra fields
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        result = {
            "id": self.id,
            "node_a": self.node_a,
            "node_b": self.node_b,
            "type": self.type,
            "conductivity": self.conductivity,
            "weight": self.weight,
            "energy": self.energy,
            "strength": self.strength,
            "created_at_s": self.created_at_s,
        }

        if self.emotions:
            result["emotions"] = self.emotions
        if self.name:
            result["name"] = self.name
        if self.role:
            result["role"] = self.role
        if self.direction:
            result["direction"] = self.direction
        if self.description:
            result["description"] = self.description

        # Type-specific
        if self.type == "leads_to":
            if self.distance:
                result["distance"] = self.distance
            if self.difficulty:
                result["difficulty"] = self.difficulty
        if self.type == "sequence" and self.tick is not None:
            result["tick"] = self.tick
        if self.type == "primes" and self.trigger:
            result["trigger"] = self.trigger

        result.update(self.extra)

        return result


# =============================================================================
# CONVERTERS
# =============================================================================

class SchemaConverter:
    """Convert Blood Ledger data to ngram schema."""

    def __init__(self, data_dir: Path, timestamp: int | None = None):
        self.data_dir = data_dir
        self.timestamp = timestamp or int(time.time())
        self.nodes: list[Node] = []
        self.links: list[Link] = []
        self.node_ids: set[str] = set()

    def load_yaml(self, filename: str) -> list[dict]:
        """Load a YAML file, return empty list if not found."""
        path = self.data_dir / filename
        if not path.exists():
            print(f"  Warning: {filename} not found")
            return []
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return data if data else []

    def generate_link_id(self, link_type: str, node_a: str, node_b: str) -> str:
        """Generate a deterministic link ID."""
        return f"link_{link_type}_{node_a}_{node_b}"

    # -------------------------------------------------------------------------
    # Node Converters
    # -------------------------------------------------------------------------

    def convert_characters(self) -> None:
        """Convert characters.yaml → actors."""
        print("Converting characters → actors...")
        characters = self.load_yaml("characters.yaml")

        # Map old types to new types
        type_map = {
            "major": "major",
            "minor": "minor",
            "companion": "companion",
            "background": "background",
            "player": "player",
        }

        # Weight based on importance
        weight_map = {
            "major": 5.0,
            "companion": 4.0,
            "minor": 2.0,
            "background": 1.0,
            "player": 10.0,
        }

        # Initial energy - major characters start "hot" in the narrative
        energy_map = {
            "major": 3.0,      # High initial energy - these drive the story
            "companion": 2.0,  # Moderate - player allies
            "minor": 0.5,      # Low but present
            "background": 0.1, # Minimal
            "player": 5.0,     # Player is always relevant
        }

        # Key characters get extra energy (story-critical NPCs)
        key_characters = {
            "char_william": 8.0,      # The Conqueror - ultimate antagonist
            "char_malet": 4.0,        # Sheriff of York - central figure
            "char_waltheof": 5.0,     # Saxon earl torn between worlds
            "char_edgar_atheling": 4.0, # The true heir
            "char_aethelwine": 3.5,   # Bishop guarding Cuthbert
            "char_cumin": 3.0,        # Durham's cruel earl
            "char_aldric": 2.5,       # Player's first companion
            "char_sweyn": 3.0,        # Danish king waiting
        }

        for char in characters:
            char_type = char.get("type", "background")
            char_id = char["id"]

            # Build description from multiple fields
            desc_parts = []
            if char.get("title"):
                desc_parts.append(char["title"])
            if char.get("role"):
                desc_parts.append(char["role"])
            if char.get("faction"):
                desc_parts.append(f"Faction: {char['faction']}")

            # Extra fields to preserve
            extra = {}
            for key in ["detail", "image_prompt", "voice", "appearance",
                       "motivation", "faction", "title", "role", "_base_place",
                       "lat", "lng"]:
                if key in char and char[key]:
                    extra[key] = char[key]

            # Compute energy - key characters get custom values
            if char_id in key_characters:
                energy = key_characters[char_id]
            else:
                energy = energy_map.get(char_type, 0.1)

            node = Node(
                id=char_id,
                name=char["name"],
                node_type="actor",
                type=type_map.get(char_type, char_type),
                description=". ".join(desc_parts) if desc_parts else "",
                weight=weight_map.get(char_type, 1.0),
                energy=energy,
                created_at_s=self.timestamp,
                updated_at_s=self.timestamp,
                extra=extra,
            )
            self.nodes.append(node)
            self.node_ids.add(node.id)

            # Create contains link if character has a base place
            if char.get("_base_place"):
                link = Link(
                    id=self.generate_link_id("contains", char["_base_place"], char["id"]),
                    node_a=char["_base_place"],  # space contains actor
                    node_b=char["id"],
                    type="contains",
                    name="resides",
                    created_at_s=self.timestamp,
                )
                self.links.append(link)

        print(f"  Converted {len(characters)} characters")

    def convert_places(self) -> None:
        """Convert places.yaml and places_minor.yaml → spaces."""
        print("Converting places → spaces...")

        places = self.load_yaml("places.yaml")
        places_minor = self.load_yaml("places_minor.yaml")
        all_places = places + places_minor

        # Map old types to new types and weights
        type_weight = {
            "city": ("city", 5.0),
            "town": ("town", 3.0),
            "hold": ("hold", 4.0),
            "castle": ("hold", 4.0),
            "abbey": ("monastery", 3.0),
            "cathedral": ("monastery", 4.0),
            "minster": ("monastery", 3.0),
            "priory": ("monastery", 2.0),
            "village": ("village", 1.5),
            "crossing": ("road", 2.0),
            "ford": ("road", 1.5),
            "bridge": ("road", 2.0),
            "ruin": ("wilderness", 1.0),
            "forest": ("wilderness", 1.5),
            "camp": ("camp", 1.0),
            "wilderness": ("wilderness", 1.0),
            "holy_well": ("wilderness", 1.0),
            "standing_stones": ("wilderness", 1.5),
            "hill": ("wilderness", 1.0),
            "monastery": ("monastery", 2.0),
            "crossroads": ("road", 2.0),
        }

        # Initial energy for place types
        type_energy = {
            "city": 2.0,
            "town": 1.0,
            "hold": 1.5,
            "castle": 2.0,
            "cathedral": 2.5,
            "monastery": 1.0,
            "village": 0.3,
            "crossing": 0.5,
            "forest": 0.8,
            "camp": 1.2,
        }

        # Key places with custom energy (story-critical locations)
        key_places = {
            "place_york": 6.0,             # Capital of the North
            "place_york_castle": 4.0,      # Norman power center
            "place_york_minster": 3.5,     # Religious power
            "place_durham": 5.0,           # Cuthbert's city
            "place_durham_cathedral": 5.0, # St. Cuthbert's bones
            "place_durham_castle": 3.0,    # Cumin's seat
            "place_stamford_bridge": 3.0,  # Where Harald fell
            "place_whitby_abbey": 2.5,     # Reinfrid's penance
            "place_richmond_castle": 2.0,  # Alan Rufus builds
            "place_thornwick": 2.0,        # Player's starting village
            "place_galtres_forest": 2.5,   # Outlaw territory
            "place_cleveland_hills": 2.0,  # Hidden resistance
        }

        for place in all_places:
            place_id = place["id"]
            place_type = place.get("type", "village")
            new_type, weight = type_weight.get(place_type, (place_type, 1.0))

            # Build description
            desc = place.get("description", "")

            # Extra fields
            extra = {}
            for key in ["detail", "image_prompt", "lat", "lng", "position",
                       "region", "historical_name", "_hidden"]:
                if key in place and place[key] is not None:
                    extra[key] = place[key]

            # Compute energy - key places get custom values
            if place_id in key_places:
                energy = key_places[place_id]
            else:
                energy = type_energy.get(place_type, 0.2)

            node = Node(
                id=place_id,
                name=place["name"],
                node_type="space",
                type=new_type,
                description=desc,
                weight=weight,
                energy=energy,
                created_at_s=self.timestamp,
                updated_at_s=self.timestamp,
                extra=extra,
            )
            self.nodes.append(node)
            self.node_ids.add(node.id)

        print(f"  Converted {len(all_places)} places")

    def convert_things(self) -> None:
        """Convert things.yaml → things."""
        print("Converting things → things...")
        things = self.load_yaml("things.yaml")

        # Weight based on significance
        sig_weight = {
            "legendary": 5.0,
            "sacred": 4.0,
            "political": 3.0,
            "personal": 2.0,
            "mundane": 1.0,
        }

        # Energy based on significance
        sig_energy = {
            "legendary": 3.0,
            "sacred": 4.0,   # Sacred items have high narrative energy
            "political": 2.5,
            "personal": 1.0,
            "mundane": 0.1,
        }

        # Key things with custom energy
        key_things = {
            "thing_cuthbert_bones": 6.0,    # St. Cuthbert's relics - most sacred
            "thing_cuthbert_gospel": 4.0,   # The Lindisfarne Gospel
            "thing_york_writ": 3.0,         # Norman authority symbol
            "thing_resistance_letter": 3.5,  # Secret rebellion plans
            "thing_saxon_axe": 2.0,         # Aldric's weapon
            "thing_waltheof_ring": 2.5,     # Earl's authority
            "thing_malet_seal": 2.0,        # Sheriff's seal
            "thing_hild_shrine": 3.0,       # Whitby's saint
        }

        for thing in things:
            thing_id = thing["id"]
            significance = thing.get("significance", "mundane")

            # Extra fields
            extra = {}
            for key in ["detail", "image_prompt", "portable", "quantity",
                       "modifiers", "_location", "_holder", "_notes"]:
                if key in thing and thing[key] is not None:
                    extra[key] = thing[key]

            # Compute energy
            if thing_id in key_things:
                energy = key_things[thing_id]
            else:
                energy = sig_energy.get(significance, 0.1)

            node = Node(
                id=thing_id,
                name=thing["name"],
                node_type="thing",
                type=thing.get("type", "item"),
                description=thing.get("description", ""),
                weight=sig_weight.get(significance, 1.0),
                energy=energy,
                created_at_s=self.timestamp,
                updated_at_s=self.timestamp,
                extra=extra,
            )
            self.nodes.append(node)
            self.node_ids.add(node.id)

        print(f"  Converted {len(things)} things")

    def convert_narratives(self) -> None:
        """Convert narratives.yaml → narratives + relates links."""
        print("Converting narratives → narratives...")
        narratives = self.load_yaml("narratives.yaml")

        # Map narrative types
        type_map = {
            "control": "fact",
            "claim": "claim",
            "memory": "memory",
            "rumour": "rumor",
            "rumor": "rumor",
            "secret": "secret",
            "debt": "debt",
            "belief": "belief",
            "reputation": "reputation",
        }

        # Weight based on type
        type_weight = {
            "memory": 3.0,
            "secret": 4.0,
            "claim": 2.5,
            "fact": 2.0,
            "rumor": 1.5,
            "debt": 3.0,
            "belief": 2.0,
            "reputation": 2.0,
        }

        # Energy based on type - secrets and claims drive tension
        type_energy = {
            "memory": 1.5,
            "secret": 3.0,     # Secrets are narrative dynamite
            "claim": 2.5,      # Claims create conflict
            "fact": 1.0,
            "rumor": 2.0,      # Rumors spread and cause trouble
            "debt": 2.0,
            "belief": 1.0,
            "reputation": 1.5,
        }

        # Key narratives with custom energy
        key_narratives = {
            "narr_william_rightful_king": 5.0,    # Core conflict
            "narr_edgar_rightful_king": 5.0,      # Counter-claim
            "narr_danish_invasion_coming": 4.0,   # Major threat
            "narr_waltheof_claim_york": 3.5,      # Earl's claim
            "narr_morcar_claim_northumbria": 3.5, # Northern rebellion
            "narr_resistance_forming": 4.0,       # Player's cause
            "narr_cumin_cruel": 3.0,              # Antagonist motivation
            "narr_malet_buried_harold": 3.0,      # Malet's torn loyalty
            "narr_aldric_brother_died": 2.5,      # Companion backstory
            "narr_cuthbert_protects": 3.5,        # Religious narrative
        }

        for narr in narratives:
            narr_id = narr["id"]
            narr_type = narr.get("type", "memory")
            new_type = type_map.get(narr_type, narr_type)

            # Extra fields
            extra = {}
            for key in ["detail", "date", "truth"]:
                if key in narr and narr[key] is not None:
                    extra[key] = narr[key]

            # Compute energy
            if narr_id in key_narratives:
                energy = key_narratives[narr_id]
            else:
                energy = type_energy.get(new_type, 0.5)

            node = Node(
                id=narr_id,
                name=narr["name"],
                node_type="narrative",
                type=new_type,
                description="",
                content=narr.get("content", ""),
                weight=type_weight.get(new_type, 1.0),
                energy=energy,
                created_at_s=self.timestamp,
                updated_at_s=self.timestamp,
                extra=extra,
            )
            self.nodes.append(node)
            self.node_ids.add(node.id)

            # Create relates links for "about" relationships
            about = narr.get("about", {})
            if about:
                # Characters this narrative is about
                for char_id in about.get("characters", []):
                    link = Link(
                        id=self.generate_link_id("relates", narr["id"], char_id),
                        node_a=narr["id"],
                        node_b=char_id,
                        type="relates",
                        name="about",
                        role="subject",
                        weight=narr.get("truth", 1.0),
                        created_at_s=self.timestamp,
                    )
                    self.links.append(link)

                # Places this narrative is about
                for place_id in about.get("places", []):
                    link = Link(
                        id=self.generate_link_id("relates", narr["id"], place_id),
                        node_a=narr["id"],
                        node_b=place_id,
                        type="relates",
                        name="about",
                        role="subject",
                        weight=narr.get("truth", 1.0),
                        created_at_s=self.timestamp,
                    )
                    self.links.append(link)

                # Things this narrative is about
                for thing_id in about.get("things", []):
                    link = Link(
                        id=self.generate_link_id("relates", narr["id"], thing_id),
                        node_a=narr["id"],
                        node_b=thing_id,
                        type="relates",
                        name="about",
                        role="subject",
                        weight=narr.get("truth", 1.0),
                        created_at_s=self.timestamp,
                    )
                    self.links.append(link)

        print(f"  Converted {len(narratives)} narratives")

    def convert_events(self) -> None:
        """Convert events.yaml → moments."""
        print("Converting events → moments...")
        events = self.load_yaml("events.yaml")

        # Impact to weight
        impact_weight = {
            "catastrophic": 5.0,
            "major": 4.0,
            "moderate": 2.5,
            "minor": 1.5,
            "local": 1.0,
        }

        # Impact to energy - catastrophic events still echo through history
        impact_energy = {
            "catastrophic": 4.0,  # Hastings, etc. - still very present
            "major": 2.5,
            "moderate": 1.0,
            "minor": 0.3,
            "local": 0.1,
        }

        # Key events with custom energy (turning points in the story)
        key_events = {
            "event_hastings": 5.0,           # THE defining moment
            "event_stamford_bridge": 3.5,    # End of Norse threat
            "event_william_crowned": 4.0,     # Norman rule begins
            "event_harold_crowned": 2.0,      # The old order
            "event_edgar_flees": 3.0,         # Hope lives
            "event_gospatric_buys": 2.5,      # Complex loyalty
            "event_resistance_meeting": 3.0,  # Rebellion stirs
            "event_york_castles": 2.5,        # Norman oppression visible
            "event_danish_rumour": 2.0,       # Threat on horizon
        }

        for event in events:
            event_id = event["id"]
            impact = event.get("impact", "minor")

            # Extra fields
            extra = {}
            for key in ["date", "type", "impact", "known_to"]:
                if key in event and event[key] is not None:
                    extra[key] = event[key]

            # Compute energy
            if event_id in key_events:
                energy = key_events[event_id]
            else:
                energy = impact_energy.get(impact, 0.2)

            node = Node(
                id=event_id,
                name=event["name"],
                node_type="moment",
                type=event.get("type", "event"),
                description="",
                text=event.get("content", ""),
                status="completed",  # Historical events are canonical
                weight=impact_weight.get(impact, 1.0),
                energy=energy,
                created_at_s=self.timestamp,
                updated_at_s=self.timestamp,
                extra=extra,
            )
            self.nodes.append(node)
            self.node_ids.add(node.id)

            # Create about links for places and characters
            for place_id in event.get("places", []):
                link = Link(
                    id=self.generate_link_id("about", event["id"], place_id),
                    node_a=event["id"],
                    node_b=place_id,
                    type="about",
                    name="occurred_at",
                    created_at_s=self.timestamp,
                )
                self.links.append(link)

            for char_id in event.get("characters", []):
                link = Link(
                    id=self.generate_link_id("about", event["id"], char_id),
                    node_a=event["id"],
                    node_b=char_id,
                    type="about",
                    name="involved",
                    created_at_s=self.timestamp,
                )
                self.links.append(link)

        print(f"  Converted {len(events)} events")

    # -------------------------------------------------------------------------
    # Link Converters
    # -------------------------------------------------------------------------

    def convert_routes(self) -> None:
        """Convert routes.yaml → leads_to links."""
        print("Converting routes → leads_to links...")
        routes = self.load_yaml("routes.yaml")

        # Terrain to difficulty
        terrain_difficulty = {
            "roman_road": "easy",
            "track": "moderate",
            "moor": "hard",
            "forest": "hard",
            "marsh": "dangerous",
        }

        for route in routes:
            from_place = route.get("from_place")
            to_place = route.get("to_place")

            if not from_place or not to_place:
                continue

            terrain = route.get("path_terrain", "track")
            hours = route.get("path_hours", 0)
            km = route.get("path_km", 0)

            # Create bidirectional leads_to links
            for (a, b) in [(from_place, to_place), (to_place, from_place)]:
                link = Link(
                    id=self.generate_link_id("leads_to", a, b),
                    node_a=a,
                    node_b=b,
                    type="leads_to",
                    name=f"{terrain} path",
                    distance=f"{hours:.1f} hours ({km:.1f} km)" if hours else None,
                    difficulty=terrain_difficulty.get(terrain, "moderate"),
                    weight=1.0 / max(hours, 0.1),  # Shorter = higher weight
                    created_at_s=self.timestamp,
                    extra={"terrain": terrain, "km": km, "hours": hours},
                )
                self.links.append(link)

        print(f"  Created {len(routes) * 2} leads_to links")

    def convert_holdings(self) -> None:
        """Convert holdings.yaml → relates links (controls)."""
        print("Converting holdings → relates links...")
        holdings = self.load_yaml("holdings.yaml")

        for holding in holdings:
            place = holding.get("place")
            holder = holding.get("holder")

            if not place or not holder:
                continue

            link = Link(
                id=self.generate_link_id("relates", holder, place),
                node_a=holder,
                node_b=place,
                type="relates",
                name="controls",
                role="originator",  # The holder is the one with authority
                weight=2.0 if not holding.get("contested") else 1.0,
                description=f"Holds as {holding.get('type', 'lord')}",
                created_at_s=self.timestamp,
                extra={
                    "holding_type": holding.get("type"),
                    "contested": holding.get("contested", False),
                    "former_holder": holding.get("former_holder"),
                },
            )
            self.links.append(link)

        print(f"  Created {len(holdings)} control links")

    def convert_thing_locations(self) -> None:
        """Convert thing_locations.yaml → contains links."""
        print("Converting thing_locations → contains links...")
        locations = self.load_yaml("thing_locations.yaml")

        for loc in locations:
            thing = loc.get("thing")
            place = loc.get("place")

            if not thing or not place:
                continue

            # Space contains thing (inverted from old schema)
            link = Link(
                id=self.generate_link_id("contains", place, thing),
                node_a=place,
                node_b=thing,
                type="contains",
                name=loc.get("type", "located"),
                description=loc.get("specific_location", ""),
                weight=1.0 if loc.get("type") == "located" else 0.5,  # hidden = lower weight
                created_at_s=self.timestamp,
            )
            self.links.append(link)

        print(f"  Created {len(locations)} thing location links")

    def convert_thing_ownership(self) -> None:
        """Convert thing_ownership.yaml → attached_to links."""
        print("Converting thing_ownership → attached_to links...")
        ownership = self.load_yaml("thing_ownership.yaml")

        for own in ownership:
            character = own.get("character")
            thing = own.get("thing")

            if not character or not thing:
                continue

            # Thing attached_to actor (inverted from old CARRIES)
            link = Link(
                id=self.generate_link_id("attached_to", thing, character),
                node_a=thing,
                node_b=character,
                type="attached_to",
                name=own.get("type", "carries"),
                weight=1.0 if own.get("type") == "carries" else 0.5,  # hidden = lower
                created_at_s=self.timestamp,
            )
            self.links.append(link)

        print(f"  Created {len(ownership)} ownership links")

    def convert_beliefs(self) -> None:
        """Convert beliefs.yaml → relates links (believes)."""
        print("Converting beliefs → relates links...")
        beliefs = self.load_yaml("beliefs.yaml")

        for belief in beliefs:
            character = belief.get("character")
            narrative = belief.get("narrative")

            if not character or not narrative:
                continue

            # Get belief strength and emotional weight
            strength = belief.get("strength", 1.0)
            is_originated = belief.get("originated", False)

            # Build emotions based on stance - use Plutchik emotions
            emotions = []
            stance = belief.get("stance", "neutral")
            if stance == "supports":
                emotions.append(["trust", strength * 0.8])
                if is_originated:
                    emotions.append(["joy", strength * 0.3])
            elif stance == "opposes":
                emotions.append(["anger", strength * 0.7])
                emotions.append(["disgust", strength * 0.4])
            elif stance == "fears":
                emotions.append(["fear", strength * 0.9])
            elif stance == "doubts":
                emotions.append(["sadness", strength * 0.5])
                emotions.append(["fear", strength * 0.3])

            # Compute energy - strong beliefs have energy
            energy = strength * 0.5 if is_originated else strength * 0.2

            link = Link(
                id=self.generate_link_id("relates", character, narrative),
                node_a=character,
                node_b=narrative,
                type="relates",
                name="believes" if not is_originated else "originated",
                role="originator" if is_originated else "believer",
                weight=strength * 2.0 if is_originated else strength,
                energy=energy,
                conductivity=0.6 if is_originated else 0.4,  # Originators spread narratives better
                emotions=emotions,
                created_at_s=self.timestamp,
            )
            self.links.append(link)

        print(f"  Created {len(beliefs)} belief links")

    def convert_tensions(self) -> None:
        """Convert tensions.yaml → relates links between narratives."""
        print("Converting tensions → relates links...")
        tensions = self.load_yaml("tensions.yaml")

        # Plutchik emotions mapping for different tension types
        # Based on tension description keywords
        tension_emotions = {
            # Political tensions - anger, anticipation
            "tension_york_claim": [["anger", 0.6], ["anticipation", 0.5]],
            "tension_durham_claim": [["anger", 0.5], ["fear", 0.4]],
            "tension_northern_rebellion": [["anger", 0.8], ["anticipation", 0.7], ["fear", 0.3]],
            "tension_danish_intervention": [["fear", 0.6], ["anticipation", 0.8]],
            "tension_scottish_raids": [["fear", 0.5], ["anger", 0.4]],

            # Personal tensions - trust, sadness, anger
            "tension_waltheof_oath": [["sadness", 0.6], ["fear", 0.5], ["anger", 0.3]],
            "tension_judith_betrayal": [["sadness", 0.7], ["anger", 0.8], ["disgust", 0.5]],
            "tension_gospatric_ambition": [["anger", 0.5], ["anticipation", 0.4]],
            "tension_malet_identity": [["sadness", 0.6], ["fear", 0.4], ["trust", 0.3]],

            # Violence/cruelty - anger, fear, disgust
            "tension_cumin_cruelty": [["anger", 0.9], ["disgust", 0.7], ["fear", 0.6]],
            "tension_aldric_revenge": [["anger", 0.8], ["sadness", 0.5]],

            # Religious/spiritual - sadness, trust, anticipation
            "tension_ealdred_service": [["sadness", 0.5], ["fear", 0.4]],
            "tension_aethelwine_resistance": [["anger", 0.5], ["trust", 0.6], ["anticipation", 0.4]],
            "tension_reinfrid_guilt": [["sadness", 0.8], ["disgust", 0.4]],

            # Local tensions - fear, anticipation
            "tension_thornwick_taxes": [["anger", 0.6], ["fear", 0.7], ["sadness", 0.4]],
            "tension_york_whispers": [["fear", 0.6], ["anticipation", 0.7]],
            "tension_edgar_return": [["anticipation", 0.8], ["joy", 0.3], ["fear", 0.3]],

            # Military tensions
            "tension_harolds_sons_return": [["anticipation", 0.7], ["anger", 0.5], ["fear", 0.4]],
            "tension_galtres_wolves": [["fear", 0.5], ["anger", 0.4]],
            "tension_siward_barn_rising": [["anticipation", 0.8], ["anger", 0.5]],
            "tension_gytha_exeter": [["anger", 0.6], ["sadness", 0.5]],
            "tension_aldgyth_prize": [["fear", 0.5], ["sadness", 0.4]],
        }

        for tension in tensions:
            tension_id = tension["id"]
            narratives = tension.get("narratives", [])

            if len(narratives) < 2:
                continue

            # Get emotions for this tension (default to anger + fear if not specified)
            emotions = tension_emotions.get(
                tension_id,
                [["anger", tension.get("pressure", 0.5)], ["fear", tension.get("pressure", 0.5) * 0.7]]
            )

            # Create opposition links between the narratives
            for i, narr_a in enumerate(narratives):
                for narr_b in narratives[i+1:]:
                    link = Link(
                        id=self.generate_link_id("relates", narr_a, narr_b),
                        node_a=narr_a,
                        node_b=narr_b,
                        type="relates",
                        name="tension",
                        direction="oppose",
                        weight=tension.get("pressure", 0.5) * 2,
                        energy=tension.get("pressure", 0.5),  # Start with energy based on pressure
                        conductivity=0.7,  # Tensions conduct energy well
                        emotions=emotions,
                        description=tension.get("description", ""),
                        created_at_s=self.timestamp,
                        extra={
                            "tension_id": tension_id,
                            "pressure_type": tension.get("pressure_type"),
                            "breaking_point": tension.get("breaking_point"),
                            "trigger_at": tension.get("trigger_at"),
                            "detail": tension.get("detail"),
                        },
                    )
                    self.links.append(link)

            # Link tension to involved characters
            for char_id in tension.get("characters", []):
                for narr_id in narratives:
                    link = Link(
                        id=self.generate_link_id("relates", char_id, f"{tension['id']}_{narr_id}"),
                        node_a=char_id,
                        node_b=narr_id,
                        type="relates",
                        name="involved_in_tension",
                        role="subject",
                        weight=tension.get("pressure", 0.5),
                        created_at_s=self.timestamp,
                        extra={"tension_id": tension["id"]},
                    )
                    self.links.append(link)

            # Link tension to involved places
            for place_id in tension.get("places", []):
                for narr_id in narratives:
                    link = Link(
                        id=self.generate_link_id("relates", place_id, f"{tension['id']}_{narr_id}"),
                        node_a=place_id,
                        node_b=narr_id,
                        type="relates",
                        name="location_of_tension",
                        weight=tension.get("pressure", 0.5),
                        created_at_s=self.timestamp,
                        extra={"tension_id": tension["id"]},
                    )
                    self.links.append(link)

        print(f"  Created tension links from {len(tensions)} tensions")

    # -------------------------------------------------------------------------
    # Main Conversion
    # -------------------------------------------------------------------------

    def convert_all(self) -> None:
        """Run all conversions."""
        print(f"\nConverting Blood Ledger data to ngram schema v1.2")
        print(f"Source: {self.data_dir}")
        print(f"Timestamp: {self.timestamp}")
        print("-" * 60)

        # Convert nodes
        self.convert_characters()
        self.convert_places()
        self.convert_things()
        self.convert_narratives()
        self.convert_events()

        # Convert links
        self.convert_routes()
        self.convert_holdings()
        self.convert_thing_locations()
        self.convert_thing_ownership()
        self.convert_beliefs()
        self.convert_tensions()

        print("-" * 60)
        print(f"Total nodes: {len(self.nodes)}")
        print(f"Total links: {len(self.links)}")

    def validate(self) -> list[str]:
        """Validate the converted data."""
        errors = []

        # Check all link endpoints exist
        for link in self.links:
            if link.node_a not in self.node_ids:
                errors.append(f"Link {link.id}: node_a '{link.node_a}' not found")
            if link.node_b not in self.node_ids:
                errors.append(f"Link {link.id}: node_b '{link.node_b}' not found")

        return errors

    def write_output(self, output_dir: Path) -> None:
        """Write converted data to output files."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Group nodes by type
        nodes_by_type = {}
        for node in self.nodes:
            if node.node_type not in nodes_by_type:
                nodes_by_type[node.node_type] = []
            nodes_by_type[node.node_type].append(node.to_dict())

        # Write nodes.yaml with all nodes
        all_nodes = [node.to_dict() for node in self.nodes]
        nodes_path = output_dir / "nodes.yaml"
        with open(nodes_path, 'w') as f:
            yaml.dump(all_nodes, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"Wrote {len(all_nodes)} nodes to {nodes_path}")

        # Write links.yaml
        all_links = [link.to_dict() for link in self.links]
        links_path = output_dir / "links.yaml"
        with open(links_path, 'w') as f:
            yaml.dump(all_links, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"Wrote {len(all_links)} links to {links_path}")

        # Also write per-type files for debugging
        for node_type, nodes in nodes_by_type.items():
            type_path = output_dir / f"{node_type}s.yaml"
            with open(type_path, 'w') as f:
                yaml.dump(nodes, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"Wrote {len(nodes)} {node_type}s to {type_path}")

        # Write link types separately
        links_by_type = {}
        for link in self.links:
            if link.type not in links_by_type:
                links_by_type[link.type] = []
            links_by_type[link.type].append(link.to_dict())

        for link_type, links in links_by_type.items():
            type_path = output_dir / f"links_{link_type}.yaml"
            with open(type_path, 'w') as f:
                yaml.dump(links, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"Wrote {len(links)} {link_type} links to {type_path}")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Migrate Blood Ledger data to ngram schema v1.2"
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=Path("data/world"),
        help="Input directory containing YAML files (default: data/world)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("data/ngram"),
        help="Output directory for converted files (default: data/ngram)"
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help="Validate output (check link endpoints exist)"
    )

    args = parser.parse_args()

    # Resolve paths relative to script location if needed
    script_dir = Path(__file__).parent.parent
    input_dir = args.input if args.input.is_absolute() else script_dir / args.input
    output_dir = args.output if args.output.is_absolute() else script_dir / args.output

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return 1

    # Run conversion
    converter = SchemaConverter(input_dir)
    converter.convert_all()

    # Validate if requested
    if args.validate:
        print("\nValidating...")
        errors = converter.validate()
        if errors:
            print(f"Found {len(errors)} validation errors:")
            for error in errors[:20]:  # Show first 20
                print(f"  - {error}")
            if len(errors) > 20:
                print(f"  ... and {len(errors) - 20} more")
        else:
            print("Validation passed!")

    # Write output
    print(f"\nWriting output to {output_dir}...")
    converter.write_output(output_dir)

    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())

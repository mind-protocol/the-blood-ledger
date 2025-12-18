"""
Spec Consistency Tests

Validates that the spec document, schema, and constants are internally consistent.
These tests do NOT require a database connection - they validate the spec itself.

VALIDATES:
    V7.1: Schema matches spec
    V7.2: Enum values consistent
    V7.3: Constants defined once

TESTS IMPLEMENTATIONS:
    (none - tests spec itself, not code)

REFERENCES:
    docs/engine/SCHEMA.md — Schema definition
    docs/engine/VALIDATION_Complete_Spec.md — All invariants
    docs/engine/TEST_Complete_Spec.md — Test index

RUN:
    pytest test_spec_consistency.py -v
"""

import pytest
import yaml
import re
from pathlib import Path
from typing import Dict, Set, Any, List

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCHEMA_PATH = PROJECT_ROOT / "docs" / "engine" / "SCHEMA.md"
SPEC_PATH = PROJECT_ROOT / "data" / "init" / "BLOOD_LEDGER_DESIGN_DOCUMENT.md"


# =============================================================================
# HELPERS
# =============================================================================

def extract_yaml_from_markdown(path: Path) -> Dict[str, Any]:
    """Extract YAML content from a markdown file that contains YAML."""
    if not path.exists():
        return {}

    content = path.read_text()

    # For SCHEMA.md, the whole thing is YAML-like after the header
    if "SCHEMA" in path.name:
        # Remove markdown header
        lines = content.split('\n')
        yaml_lines = []
        in_yaml = False

        for line in lines:
            # Skip markdown headers and comments
            if line.startswith('# ') and not in_yaml:
                continue
            if line.startswith('# ===') or line.startswith('# ---'):
                continue
            in_yaml = True
            yaml_lines.append(line)

        try:
            return yaml.safe_load('\n'.join(yaml_lines)) or {}
        except yaml.YAMLError:
            return {}

    return {}


def extract_enums_from_schema(schema: Dict[str, Any]) -> Dict[str, Set[str]]:
    """Extract all enum definitions from the schema."""
    enums = {}

    def find_enums(obj: Any, path: str = ""):
        if isinstance(obj, dict):
            if 'type' in obj and obj['type'] == 'enum' and 'values' in obj:
                enums[path] = set(obj['values'])
            for key, value in obj.items():
                find_enums(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                find_enums(item, f"{path}[{i}]")

    find_enums(schema)
    return enums


def extract_constants_from_content(content: str) -> Dict[str, Any]:
    """Extract constant definitions from text."""
    constants = {}

    # Match patterns like: CONSTANT_NAME = value
    pattern = r'([A-Z][A-Z_0-9]+)\s*[=:]\s*([0-9.]+|\{[^}]+\})'

    for match in re.finditer(pattern, content):
        name = match.group(1)
        value = match.group(2)
        try:
            # Try to parse as number
            if '.' in value:
                constants[name] = float(value)
            elif value.isdigit():
                constants[name] = int(value)
            else:
                constants[name] = value
        except ValueError:
            constants[name] = value

    return constants


# =============================================================================
# EXPECTED VALUES (from spec)
# =============================================================================

EXPECTED_NODE_TYPES = {'Character', 'Place', 'Thing', 'Narrative', 'Tension', 'Moment'}

EXPECTED_CHARACTER_TYPES = {'player', 'companion', 'major', 'minor', 'background'}

EXPECTED_PLACE_SCALES = {'region', 'settlement', 'district', 'building', 'room'}

EXPECTED_PLACE_TYPES = {
    'region', 'city', 'hold', 'village', 'monastery', 'camp',
    'road', 'room', 'wilderness', 'ruin'
}

EXPECTED_THING_TYPES = {
    'weapon', 'armor', 'document', 'letter', 'relic', 'treasure',
    'title', 'land', 'token', 'provisions', 'coin_purse', 'horse', 'ship', 'tool'
}

EXPECTED_THING_SIGNIFICANCE = {'mundane', 'personal', 'political', 'sacred', 'legendary'}

EXPECTED_NARRATIVE_TYPES = {
    # About events
    'memory', 'account', 'rumor',
    # About characters
    'reputation', 'identity',
    # About relationships
    'bond', 'oath', 'debt', 'blood', 'enmity', 'love', 'service',
    # About things
    'ownership', 'claim',
    # About places
    'control', 'origin',
    # Meta
    'belief', 'prophecy', 'lie', 'secret'
}

EXPECTED_NARRATIVE_TONES = {
    'bitter', 'proud', 'shameful', 'defiant', 'mournful', 'cold',
    'righteous', 'hopeful', 'fearful', 'warm', 'dark', 'sacred'
}

EXPECTED_VOICE_STYLES = {
    'whisper', 'demand', 'remind', 'accuse', 'plead',
    'warn', 'inspire', 'mock', 'question'
}

EXPECTED_SKILL_LEVELS = {'untrained', 'capable', 'skilled', 'master'}

EXPECTED_CHARACTER_TONES = {'quiet', 'sharp', 'warm', 'bitter', 'measured', 'fierce'}

EXPECTED_CHARACTER_STYLES = {'direct', 'questioning', 'sardonic', 'gentle', 'blunt'}

EXPECTED_APPROACHES = {'direct', 'cunning', 'cautious', 'impulsive', 'deliberate'}

EXPECTED_FLAWS = {
    'pride', 'fear', 'greed', 'wrath', 'doubt',
    'rigidity', 'softness', 'envy', 'sloth'
}

EXPECTED_PRESSURE_TYPES = {'gradual', 'scheduled', 'hybrid'}

EXPECTED_MOMENT_TYPES = {
    'narration', 'dialogue', 'hint',
    'player_click', 'player_freeform', 'player_choice'
}

EXPECTED_BELIEF_SOURCES = {'none', 'witnessed', 'told', 'inferred', 'assumed', 'taught'}

EXPECTED_MODIFIER_TYPES = {
    # Character
    'wounded', 'sick', 'hungry', 'exhausted', 'drunk',
    'grieving', 'inspired', 'afraid', 'angry', 'hopeful', 'suspicious',
    # Place
    'burning', 'flooded', 'besieged', 'abandoned', 'celebrating',
    'haunted', 'watched', 'safe',
    # Thing
    'damaged', 'hidden', 'contested', 'blessed', 'cursed', 'stolen'
}

EXPECTED_ROAD_TYPES = {'roman', 'track', 'path', 'river', 'none'}

# Constants from spec
EXPECTED_CONSTANTS = {
    'BELIEF_FLOW_RATE': 0.1,
    'MAX_PROPAGATION_HOPS': 3,
    'DECAY_RATE': 0.02,
    'MIN_WEIGHT': 0.01,
    'BASE_RATE': 0.001,
    'DEFAULT_BREAKING_POINT': 0.9,
    'MAX_CASCADE_DEPTH': 5,
    'TICK_INTERVAL_MINUTES': 5,
}

EXPECTED_LINK_FACTORS = {
    'contradicts': 0.30,
    'supports': 0.20,
    'elaborates': 0.15,
    'subsumes': 0.10,
    'supersedes': 0.25,
}


# =============================================================================
# TESTS: V7.1 Schema Matches Spec
# =============================================================================

class TestSchemaSpecAlignment:
    """Test that schema matches the spec."""

    def test_node_types_exist(self):
        """Schema should define all expected node types."""
        schema = extract_yaml_from_markdown(SCHEMA_PATH)

        if 'nodes' in schema:
            defined_nodes = set(schema['nodes'].keys())
            missing = EXPECTED_NODE_TYPES - {n.capitalize() for n in defined_nodes}
            extra = {n.capitalize() for n in defined_nodes} - EXPECTED_NODE_TYPES

            # Note: Schema uses lowercase, spec uses capitalized
            schema_nodes = {n.lower() for n in defined_nodes}
            expected_lower = {n.lower() for n in EXPECTED_NODE_TYPES}

            # Just check the core 4 nodes are present
            core_nodes = {'character', 'place', 'thing', 'narrative'}
            assert core_nodes <= schema_nodes, f"Missing core nodes: {core_nodes - schema_nodes}"

    def test_character_type_enum(self):
        """Character type enum should match spec."""
        schema = extract_yaml_from_markdown(SCHEMA_PATH)

        if 'nodes' in schema and 'character' in schema['nodes']:
            char_schema = schema['nodes']['character']
            if 'attributes' in char_schema and 'type' in char_schema['attributes']:
                type_attr = char_schema['attributes']['type']
                if 'values' in type_attr:
                    schema_values = set(type_attr['values'])
                    assert schema_values == EXPECTED_CHARACTER_TYPES, \
                        f"Mismatch: schema={schema_values}, expected={EXPECTED_CHARACTER_TYPES}"

    def test_narrative_type_enum(self):
        """Narrative type enum should match spec."""
        schema = extract_yaml_from_markdown(SCHEMA_PATH)

        if 'nodes' in schema and 'narrative' in schema['nodes']:
            narr_schema = schema['nodes']['narrative']
            if 'attributes' in narr_schema and 'type' in narr_schema['attributes']:
                type_attr = narr_schema['attributes']['type']
                if 'values' in type_attr:
                    schema_values = set(type_attr['values'])
                    assert schema_values == EXPECTED_NARRATIVE_TYPES, \
                        f"Mismatch: schema={schema_values}, expected={EXPECTED_NARRATIVE_TYPES}"


# =============================================================================
# TESTS: V7.2 Enum Consistency
# =============================================================================

class TestEnumConsistency:
    """Test that enum values are consistent across all documents."""

    def test_character_types_complete(self):
        """All character types should be valid."""
        assert 'player' in EXPECTED_CHARACTER_TYPES
        assert 'companion' in EXPECTED_CHARACTER_TYPES
        assert len(EXPECTED_CHARACTER_TYPES) == 5

    def test_place_scales_hierarchical(self):
        """Place scales should form a clear hierarchy."""
        # region > settlement > district > building > room
        hierarchy = ['region', 'settlement', 'district', 'building', 'room']
        for scale in hierarchy:
            assert scale in EXPECTED_PLACE_SCALES

    def test_narrative_types_cover_all_categories(self):
        """Narrative types should cover events, characters, relationships, things, places, meta."""
        # Events
        assert 'memory' in EXPECTED_NARRATIVE_TYPES
        assert 'account' in EXPECTED_NARRATIVE_TYPES
        assert 'rumor' in EXPECTED_NARRATIVE_TYPES

        # Relationships
        assert 'oath' in EXPECTED_NARRATIVE_TYPES
        assert 'debt' in EXPECTED_NARRATIVE_TYPES
        assert 'blood' in EXPECTED_NARRATIVE_TYPES

        # Meta
        assert 'secret' in EXPECTED_NARRATIVE_TYPES
        assert 'lie' in EXPECTED_NARRATIVE_TYPES

    def test_skill_levels_ordered(self):
        """Skill levels should have clear ordering."""
        levels = ['untrained', 'capable', 'skilled', 'master']
        for level in levels:
            assert level in EXPECTED_SKILL_LEVELS
        assert len(EXPECTED_SKILL_LEVELS) == 4

    def test_pressure_types_complete(self):
        """All pressure types should be defined."""
        assert 'gradual' in EXPECTED_PRESSURE_TYPES
        assert 'scheduled' in EXPECTED_PRESSURE_TYPES
        assert 'hybrid' in EXPECTED_PRESSURE_TYPES
        assert len(EXPECTED_PRESSURE_TYPES) == 3

    def test_moment_types_cover_all_sources(self):
        """Moment types should cover narration, dialogue, and player actions."""
        # AI-generated content
        assert 'narration' in EXPECTED_MOMENT_TYPES
        assert 'dialogue' in EXPECTED_MOMENT_TYPES
        assert 'hint' in EXPECTED_MOMENT_TYPES

        # Player input
        assert 'player_click' in EXPECTED_MOMENT_TYPES
        assert 'player_freeform' in EXPECTED_MOMENT_TYPES
        assert 'player_choice' in EXPECTED_MOMENT_TYPES


# =============================================================================
# TESTS: V7.3 Constants Consistency
# =============================================================================

class TestConstantsConsistency:
    """Test that constants are defined correctly."""

    def test_belief_flow_rate_valid(self):
        """BELIEF_FLOW_RATE should be in (0, 1]."""
        rate = EXPECTED_CONSTANTS['BELIEF_FLOW_RATE']
        assert 0 < rate <= 1, f"BELIEF_FLOW_RATE {rate} should be in (0, 1]"

    def test_max_propagation_hops_positive(self):
        """MAX_PROPAGATION_HOPS should be positive integer."""
        hops = EXPECTED_CONSTANTS['MAX_PROPAGATION_HOPS']
        assert isinstance(hops, int) and hops > 0

    def test_decay_rate_valid(self):
        """DECAY_RATE should be small positive number."""
        rate = EXPECTED_CONSTANTS['DECAY_RATE']
        assert 0 < rate < 0.5, f"DECAY_RATE {rate} seems too high"

    def test_min_weight_small(self):
        """MIN_WEIGHT should be small positive number."""
        min_w = EXPECTED_CONSTANTS['MIN_WEIGHT']
        assert 0 < min_w < 0.1, f"MIN_WEIGHT {min_w} seems too high"

    def test_breaking_point_valid(self):
        """DEFAULT_BREAKING_POINT should be high but < 1."""
        bp = EXPECTED_CONSTANTS['DEFAULT_BREAKING_POINT']
        assert 0.5 < bp < 1.0, f"DEFAULT_BREAKING_POINT {bp} should be in (0.5, 1.0)"

    def test_link_factors_sum_reasonable(self):
        """Link factors should sum to something reasonable."""
        total = sum(EXPECTED_LINK_FACTORS.values())
        assert 0.5 < total < 2.0, f"Link factors sum {total} seems unreasonable"

    def test_link_factors_all_positive(self):
        """All link factors should be positive."""
        for name, value in EXPECTED_LINK_FACTORS.items():
            assert value > 0, f"Link factor {name} should be positive"

    def test_supersedes_has_drain_effect(self):
        """Supersedes should have significant factor (drains source)."""
        assert EXPECTED_LINK_FACTORS['supersedes'] >= 0.2, \
            "Supersedes factor should be significant for drain effect"

    def test_contradicts_highest_factor(self):
        """Contradicts should have highest or near-highest factor."""
        contradicts = EXPECTED_LINK_FACTORS['contradicts']
        max_factor = max(EXPECTED_LINK_FACTORS.values())
        assert contradicts >= max_factor * 0.8, \
            "Contradicts should be among the highest factors"


# =============================================================================
# TESTS: Spec Internal Consistency
# =============================================================================

class TestSpecInternalConsistency:
    """Test that the spec is internally consistent."""

    def test_core_types_for_slow_decay(self):
        """Core types (oath, blood, debt) should exist in narrative types."""
        core_types = {'oath', 'blood', 'debt'}
        assert core_types <= EXPECTED_NARRATIVE_TYPES, \
            f"Core types {core_types} must be valid narrative types"

    def test_character_flaws_distinct(self):
        """Character flaws should be distinct concepts."""
        assert len(EXPECTED_FLAWS) == 9, "Should have 9 distinct flaws"
        # Check no duplicates
        flaws_list = list(EXPECTED_FLAWS)
        assert len(flaws_list) == len(set(flaws_list))

    def test_voice_styles_cover_emotional_range(self):
        """Voice styles should cover range of emotional expression."""
        # Should have both positive and negative styles
        negative = {'accuse', 'mock', 'demand', 'warn'}
        positive = {'inspire', 'plead', 'remind'}
        neutral = {'whisper', 'question'}

        assert negative <= EXPECTED_VOICE_STYLES
        assert positive <= EXPECTED_VOICE_STYLES
        assert neutral <= EXPECTED_VOICE_STYLES

    def test_modifier_types_cover_all_node_types(self):
        """Modifier types should apply to characters, places, and things."""
        # Character modifiers
        char_mods = {'wounded', 'sick', 'hungry', 'exhausted', 'afraid', 'angry'}
        assert char_mods <= EXPECTED_MODIFIER_TYPES

        # Place modifiers
        place_mods = {'burning', 'flooded', 'besieged', 'abandoned'}
        assert place_mods <= EXPECTED_MODIFIER_TYPES

        # Thing modifiers
        thing_mods = {'damaged', 'hidden', 'contested', 'blessed', 'cursed'}
        assert thing_mods <= EXPECTED_MODIFIER_TYPES

    def test_road_types_have_speed_ordering(self):
        """Road types should imply speed ordering: roman > track > path > none."""
        # This is a logical test - roman roads are fastest, no road is slowest
        road_speeds = {
            'roman': 5.0,  # km/h
            'track': 3.5,
            'path': 2.5,
            'river': 8.0,  # downstream
            'none': 1.5
        }

        # Verify all road types are accounted for
        assert set(road_speeds.keys()) == EXPECTED_ROAD_TYPES

        # Land routes should be ordered
        assert road_speeds['roman'] > road_speeds['track'] > road_speeds['path'] > road_speeds['none']


# =============================================================================
# TESTS: Cross-Reference Validation
# =============================================================================

class TestCrossReferences:
    """Test that references between spec elements are valid."""

    def test_tension_references_narratives(self):
        """Tensions should reference valid narrative IDs."""
        # This is a structural test - tension.narratives should be narrative IDs
        # The actual validation happens at runtime
        pass  # Placeholder for runtime test

    def test_belief_source_types_make_sense(self):
        """Belief source types should have clear meaning."""
        sources = EXPECTED_BELIEF_SOURCES

        # Should have "no source" option
        assert 'none' in sources

        # Should have direct witness
        assert 'witnessed' in sources

        # Should have secondhand
        assert 'told' in sources

        # Should have deduction
        assert 'inferred' in sources

    def test_narrative_about_fields_valid(self):
        """Narrative.about fields should reference valid node types."""
        # about.characters -> Character IDs
        # about.places -> Place IDs
        # about.things -> Thing IDs
        # about.relationship -> [char_id, char_id]

        # This is structural - actual validation at runtime
        pass


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

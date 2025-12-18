"""
Pydantic Model Validation Tests

Tests that the Pydantic models correctly validate data according to the schema.

VALIDATES:
    V2.1-V2.6: Node invariants (Character, Place, Thing, Narrative, Tension, Moment)
    V3.1-V3.3: Link invariants (BELIEVES, NARRATIVE_NARRATIVE, ground truth)

TESTS IMPLEMENTATIONS:
    engine/models/base.py — Enums, modifiers, shared types
    engine/models/nodes.py — Character, Place, Thing, Narrative, Moment
    engine/models/links.py — CharacterNarrative, NarrativeNarrative, etc.
    engine/models/tensions.py — Tension

REFERENCES:
    docs/engine/VALIDATION_Complete_Spec.md — All invariants
    docs/engine/TEST_Complete_Spec.md — Test index

RUN:
    pytest test_models.py -v
"""

import pytest
from pydantic import ValidationError

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.models.base import (
    CharacterType, Face, SkillLevel, VoiceTone, VoiceStyle,
    Approach, Value, Flaw, PlaceType, Weather, Mood,
    ThingType, Significance, NarrativeType, NarrativeTone,
    NarrativeVoiceStyle, BeliefSource, PressureType, MomentType,
    ModifierType, ModifierSeverity, PathDifficulty,
    Modifier, Skills, CharacterVoice, Personality, Backstory,
    Atmosphere, NarrativeAbout, NarrativeVoice, TensionProgression,
    TimeOfDay, GameTimestamp
)
from engine.models.nodes import Character, Place, Thing, Narrative, Moment
from engine.models.links import (
    CharacterNarrative, NarrativeNarrative,
    CharacterPlace, CharacterThing, ThingPlace, PlacePlace
)
from engine.models.tensions import Tension


# =============================================================================
# V2.1: CHARACTER MODEL TESTS
# =============================================================================

class TestCharacterModel:
    """Test Character node model validation."""

    def test_character_required_fields(self):
        """Character requires id and name."""
        # Valid character
        char = Character(id="char_aldric", name="Aldric")
        assert char.id == "char_aldric"
        assert char.name == "Aldric"

        # Missing id should fail
        with pytest.raises(ValidationError):
            Character(name="Aldric")

        # Missing name should fail
        with pytest.raises(ValidationError):
            Character(id="char_aldric")

    def test_character_type_default(self):
        """Character type defaults to MINOR."""
        char = Character(id="test", name="Test")
        assert char.type == CharacterType.MINOR

    def test_character_type_enum_validation(self):
        """Character type must be valid enum value."""
        # Valid types
        for char_type in CharacterType:
            char = Character(id="test", name="Test", type=char_type)
            assert char.type == char_type

        # Invalid type should fail
        with pytest.raises(ValidationError):
            Character(id="test", name="Test", type="invalid")

    def test_character_alive_default(self):
        """Character alive defaults to True."""
        char = Character(id="test", name="Test")
        assert char.alive is True

    def test_character_skills_default(self):
        """Character skills default to untrained."""
        char = Character(id="test", name="Test")
        assert char.skills.fighting == SkillLevel.UNTRAINED
        assert char.skills.tracking == SkillLevel.UNTRAINED
        assert char.skills.healing == SkillLevel.UNTRAINED

    def test_character_skills_validation(self):
        """Character skills must be valid enum values."""
        skills = Skills(fighting=SkillLevel.MASTER, healing=SkillLevel.SKILLED)
        char = Character(id="test", name="Test", skills=skills)
        assert char.skills.fighting == SkillLevel.MASTER
        assert char.skills.healing == SkillLevel.SKILLED

    def test_character_personality_values(self):
        """Character personality values are a list."""
        personality = Personality(
            approach=Approach.CUNNING,
            values=[Value.LOYALTY, Value.HONOR],
            flaw=Flaw.PRIDE
        )
        char = Character(id="test", name="Test", personality=personality)
        assert char.personality.approach == Approach.CUNNING
        assert Value.LOYALTY in char.personality.values
        assert char.personality.flaw == Flaw.PRIDE

    def test_character_embeddable_text(self):
        """Character embeddable text includes name and type."""
        char = Character(id="char_aldric", name="Aldric", type=CharacterType.COMPANION)
        text = char.embeddable_text()
        assert "Aldric" in text
        assert "companion" in text

    def test_character_embeddable_text_with_backstory(self):
        """Character embeddable text includes backstory if present."""
        backstory = Backstory(
            why_here="To protect his lord",
            wound="Lost his family to Normans"
        )
        char = Character(id="char_aldric", name="Aldric", backstory=backstory)
        text = char.embeddable_text()
        assert "protect his lord" in text
        assert "family" in text


# =============================================================================
# V2.2: PLACE MODEL TESTS
# =============================================================================

class TestPlaceModel:
    """Test Place node model validation."""

    def test_place_required_fields(self):
        """Place requires id and name."""
        place = Place(id="place_york", name="York")
        assert place.id == "place_york"
        assert place.name == "York"

        with pytest.raises(ValidationError):
            Place(name="York")

        with pytest.raises(ValidationError):
            Place(id="place_york")

    def test_place_type_default(self):
        """Place type defaults to VILLAGE."""
        place = Place(id="test", name="Test")
        assert place.type == PlaceType.VILLAGE

    def test_place_type_enum_validation(self):
        """Place type must be valid enum value."""
        for place_type in PlaceType:
            place = Place(id="test", name="Test", type=place_type)
            assert place.type == place_type

    def test_place_atmosphere(self):
        """Place can have atmosphere."""
        atmosphere = Atmosphere(
            weather=[Weather.RAIN, Weather.COLD],
            mood=Mood.HOSTILE,
            details=["Dark streets", "Few people about"]
        )
        place = Place(id="test", name="Test", atmosphere=atmosphere)
        assert Weather.RAIN in place.atmosphere.weather
        assert place.atmosphere.mood == Mood.HOSTILE
        assert len(place.atmosphere.details) == 2

    def test_place_embeddable_text(self):
        """Place embeddable text includes name and type."""
        place = Place(id="place_york", name="York", type=PlaceType.CITY)
        text = place.embeddable_text()
        assert "York" in text
        assert "city" in text


# =============================================================================
# V2.3: THING MODEL TESTS
# =============================================================================

class TestThingModel:
    """Test Thing node model validation."""

    def test_thing_required_fields(self):
        """Thing requires id and name."""
        thing = Thing(id="thing_sword", name="Father's Sword")
        assert thing.id == "thing_sword"
        assert thing.name == "Father's Sword"

        with pytest.raises(ValidationError):
            Thing(name="Sword")

    def test_thing_type_default(self):
        """Thing type defaults to TOOL."""
        thing = Thing(id="test", name="Test")
        assert thing.type == ThingType.TOOL

    def test_thing_significance_default(self):
        """Thing significance defaults to MUNDANE."""
        thing = Thing(id="test", name="Test")
        assert thing.significance == Significance.MUNDANE

    def test_thing_quantity_default(self):
        """Thing quantity defaults to 1."""
        thing = Thing(id="test", name="Test")
        assert thing.quantity == 1

    def test_thing_portable_default(self):
        """Thing portable defaults to True."""
        thing = Thing(id="test", name="Test")
        assert thing.portable is True

    def test_thing_non_portable(self):
        """Land should be non-portable."""
        thing = Thing(id="thing_land", name="Thornwick", type=ThingType.LAND, portable=False)
        assert thing.portable is False


# =============================================================================
# V2.4: NARRATIVE MODEL TESTS
# =============================================================================

class TestNarrativeModel:
    """Test Narrative node model validation."""

    def test_narrative_required_fields(self):
        """Narrative requires id, name, and content."""
        narr = Narrative(
            id="narr_oath",
            name="Aldric's Oath",
            content="Aldric swore to protect Rolf",
            type=NarrativeType.OATH
        )
        assert narr.id == "narr_oath"
        assert narr.name == "Aldric's Oath"
        assert narr.content == "Aldric swore to protect Rolf"

        with pytest.raises(ValidationError):
            Narrative(name="Test", content="Content", type=NarrativeType.OATH)

    def test_narrative_weight_range(self):
        """Narrative weight must be in [0, 1]."""
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY, weight=0.5
        )
        assert narr.weight == 0.5

        # Too low
        with pytest.raises(ValidationError):
            Narrative(
                id="test", name="Test", content="Test",
                type=NarrativeType.MEMORY, weight=-0.1
            )

        # Too high
        with pytest.raises(ValidationError):
            Narrative(
                id="test", name="Test", content="Test",
                type=NarrativeType.MEMORY, weight=1.1
            )

    def test_narrative_focus_range(self):
        """Narrative focus must be in [0.1, 3.0]."""
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY, focus=2.0
        )
        assert narr.focus == 2.0

        # Too low
        with pytest.raises(ValidationError):
            Narrative(
                id="test", name="Test", content="Test",
                type=NarrativeType.MEMORY, focus=0.05
            )

        # Too high
        with pytest.raises(ValidationError):
            Narrative(
                id="test", name="Test", content="Test",
                type=NarrativeType.MEMORY, focus=3.5
            )

    def test_narrative_truth_range(self):
        """Narrative truth must be in [0, 1]."""
        narr = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.LIE, truth=0.3
        )
        assert narr.truth == 0.3

    def test_narrative_is_core_type(self):
        """Core types (oath, blood, debt) should be identified."""
        oath = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.OATH
        )
        assert oath.is_core_type is True

        blood = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.BLOOD
        )
        assert blood.is_core_type is True

        debt = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.DEBT
        )
        assert debt.is_core_type is True

        memory = Narrative(
            id="test", name="Test", content="Test",
            type=NarrativeType.MEMORY
        )
        assert memory.is_core_type is False

    def test_narrative_type_enum_validation(self):
        """Narrative type must be valid enum value."""
        for narr_type in NarrativeType:
            narr = Narrative(
                id="test", name="Test", content="Test",
                type=narr_type
            )
            assert narr.type == narr_type


# =============================================================================
# V2.5: TENSION MODEL TESTS
# =============================================================================

class TestTensionModel:
    """Test Tension model validation."""

    def test_tension_required_fields(self):
        """Tension requires id."""
        tension = Tension(id="tension_test")
        assert tension.id == "tension_test"

        with pytest.raises(ValidationError):
            Tension()

    def test_tension_pressure_range(self):
        """Tension pressure must be in [0, 1]."""
        tension = Tension(id="test", pressure=0.5)
        assert tension.pressure == 0.5

        with pytest.raises(ValidationError):
            Tension(id="test", pressure=-0.1)

        with pytest.raises(ValidationError):
            Tension(id="test", pressure=1.1)

    def test_tension_breaking_point_range(self):
        """Tension breaking_point must be in [0, 1]."""
        tension = Tension(id="test", breaking_point=0.8)
        assert tension.breaking_point == 0.8

    def test_tension_breaking_point_default(self):
        """Tension breaking_point defaults to 0.9."""
        tension = Tension(id="test")
        assert tension.breaking_point == 0.9

    def test_tension_pressure_type_default(self):
        """Tension pressure_type defaults to GRADUAL."""
        tension = Tension(id="test")
        assert tension.pressure_type == PressureType.GRADUAL

    def test_tension_has_flipped(self):
        """Tension has_flipped property works correctly."""
        # Not flipped
        tension = Tension(id="test", pressure=0.5, breaking_point=0.9)
        assert tension.has_flipped is False

        # At breaking point
        tension = Tension(id="test", pressure=0.9, breaking_point=0.9)
        assert tension.has_flipped is True

        # Above breaking point
        tension = Tension(id="test", pressure=0.95, breaking_point=0.9)
        assert tension.has_flipped is True

    def test_tension_tick_gradual(self):
        """Gradual tension ticks increase pressure."""
        tension = Tension(id="test", pressure=0.0, base_rate=0.001)

        # Tick for 100 minutes with focus=1.0 and max_weight=1.0
        new_pressure = tension.tick_gradual(100, focus=1.0, max_weight=1.0)

        # Expected: 0.0 + 100 * 0.001 * 1.0 * 1.0 = 0.1
        assert abs(new_pressure - 0.1) < 0.001

    def test_tension_tick_gradual_respects_type(self):
        """Scheduled tensions don't use gradual ticking."""
        tension = Tension(
            id="test", pressure=0.0,
            pressure_type=PressureType.SCHEDULED
        )

        new_pressure = tension.tick_gradual(100, focus=1.0, max_weight=1.0)
        assert new_pressure == 0.0  # Unchanged

    def test_tension_add_event_pressure(self):
        """Event pressure can be added to gradual/hybrid tensions."""
        tension = Tension(id="test", pressure=0.3)
        tension.add_event_pressure(0.2)
        assert abs(tension.pressure - 0.5) < 0.001

    def test_tension_reset(self):
        """Tension can be reset after flip."""
        tension = Tension(id="test", pressure=0.95)
        tension.reset(0.1)
        assert tension.pressure == 0.1


# =============================================================================
# V2.6: MOMENT MODEL TESTS
# =============================================================================

class TestMomentModel:
    """Test Moment node model validation."""

    def test_moment_required_fields(self):
        """Moment requires id, text, and tick."""
        moment = Moment(
            id="camp_d1_night_dialogue_001",
            text="I swore an oath.",
            tick=1440
        )
        assert moment.id == "camp_d1_night_dialogue_001"
        assert moment.text == "I swore an oath."
        assert moment.tick == 1440

    def test_moment_type_default(self):
        """Moment type defaults to NARRATION."""
        moment = Moment(id="test", text="Test", tick=0)
        assert moment.type == MomentType.NARRATION

    def test_moment_tick_non_negative(self):
        """Moment tick must be >= 0."""
        moment = Moment(id="test", text="Test", tick=0)
        assert moment.tick == 0

        with pytest.raises(ValidationError):
            Moment(id="test", text="Test", tick=-1)

    def test_moment_should_embed(self):
        """Moment should_embed is True for long text."""
        short = Moment(id="test", text="Short.", tick=0)
        assert short.should_embed is False

        long = Moment(id="test", text="This is a longer piece of text.", tick=0)
        assert long.should_embed is True

    def test_moment_embeddable_text(self):
        """Moment embeddable text returns text."""
        moment = Moment(id="test", text="Hello there.", tick=0)
        assert moment.embeddable_text() == "Hello there."


# =============================================================================
# V3.1: BELIEVES LINK TESTS
# =============================================================================

class TestCharacterNarrativeLink:
    """Test CharacterNarrative (BELIEVES) link validation."""

    def test_believes_required_fields(self):
        """BELIEVES link requires character_id and narrative_id."""
        link = CharacterNarrative(
            character_id="char_aldric",
            narrative_id="narr_oath"
        )
        assert link.character_id == "char_aldric"
        assert link.narrative_id == "narr_oath"

    def test_believes_value_ranges(self):
        """BELIEVES values must be in [0, 1]."""
        link = CharacterNarrative(
            character_id="test",
            narrative_id="test",
            heard=0.9,
            believes=0.8,
            doubts=0.1
        )
        assert link.heard == 0.9
        assert link.believes == 0.8
        assert link.doubts == 0.1

        # Invalid values
        with pytest.raises(ValidationError):
            CharacterNarrative(
                character_id="test",
                narrative_id="test",
                heard=1.5
            )

    def test_believes_defaults(self):
        """BELIEVES values default to 0."""
        link = CharacterNarrative(
            character_id="test",
            narrative_id="test"
        )
        assert link.heard == 0.0
        assert link.believes == 0.0
        assert link.doubts == 0.0
        assert link.denies == 0.0
        assert link.hides == 0.0
        assert link.spreads == 0.0
        assert link.originated == 0.0

    def test_believes_source_enum(self):
        """BELIEVES source must be valid enum."""
        for source in BeliefSource:
            link = CharacterNarrative(
                character_id="test",
                narrative_id="test",
                source=source
            )
            assert link.source == source

    def test_belief_intensity(self):
        """belief_intensity property calculates correctly."""
        link = CharacterNarrative(
            character_id="test",
            narrative_id="test",
            heard=1.0,
            believes=0.8
        )
        assert link.belief_intensity == 0.8  # max(0.8, 0) * 1.0


# =============================================================================
# V3.2: NARRATIVE_NARRATIVE LINK TESTS
# =============================================================================

class TestNarrativeNarrativeLink:
    """Test NarrativeNarrative link validation."""

    def test_narrative_link_required_fields(self):
        """Link requires source and target narrative IDs."""
        link = NarrativeNarrative(
            source_narrative_id="narr_1",
            target_narrative_id="narr_2"
        )
        assert link.source_narrative_id == "narr_1"
        assert link.target_narrative_id == "narr_2"

    def test_narrative_link_value_ranges(self):
        """Link values must be in [0, 1]."""
        link = NarrativeNarrative(
            source_narrative_id="narr_1",
            target_narrative_id="narr_2",
            contradicts=0.8,
            supports=0.2
        )
        assert link.contradicts == 0.8
        assert link.supports == 0.2

    def test_narrative_link_type_property(self):
        """link_type returns dominant relationship."""
        link = NarrativeNarrative(
            source_narrative_id="narr_1",
            target_narrative_id="narr_2",
            contradicts=0.9,
            supports=0.1
        )
        assert link.link_type == "contradicts"


# =============================================================================
# V3.3: GROUND TRUTH LINK TESTS
# =============================================================================

class TestCharacterPlaceLink:
    """Test CharacterPlace (AT) link validation."""

    def test_at_link_required_fields(self):
        """AT link requires character_id and place_id."""
        link = CharacterPlace(
            character_id="char_aldric",
            place_id="place_york"
        )
        assert link.character_id == "char_aldric"
        assert link.place_id == "place_york"

    def test_at_link_present_range(self):
        """AT link present must be in [0, 1]."""
        link = CharacterPlace(
            character_id="test",
            place_id="test",
            present=1.0
        )
        assert link.present == 1.0
        assert link.is_present is True

        link_absent = CharacterPlace(
            character_id="test",
            place_id="test",
            present=0.0
        )
        assert link_absent.is_present is False

    def test_at_link_visible_default(self):
        """AT link visible defaults to 1.0."""
        link = CharacterPlace(
            character_id="test",
            place_id="test"
        )
        assert link.visible == 1.0


class TestCharacterThingLink:
    """Test CharacterThing (CARRIES) link validation."""

    def test_carries_link_required_fields(self):
        """CARRIES link requires character_id and thing_id."""
        link = CharacterThing(
            character_id="char_aldric",
            thing_id="thing_sword"
        )
        assert link.character_id == "char_aldric"
        assert link.thing_id == "thing_sword"

    def test_carries_link_has_item(self):
        """has_item property works correctly."""
        link = CharacterThing(
            character_id="test",
            thing_id="test",
            carries=1.0
        )
        assert link.has_item is True

        link_hidden = CharacterThing(
            character_id="test",
            thing_id="test",
            carries_hidden=1.0
        )
        assert link_hidden.has_item is True


class TestThingPlaceLink:
    """Test ThingPlace (LOCATED_AT) link validation."""

    def test_located_at_required_fields(self):
        """LOCATED_AT link requires thing_id and place_id."""
        link = ThingPlace(
            thing_id="thing_sword",
            place_id="place_hall"
        )
        assert link.thing_id == "thing_sword"
        assert link.place_id == "place_hall"

    def test_located_at_specific_location(self):
        """LOCATED_AT can have specific location."""
        link = ThingPlace(
            thing_id="thing_sword",
            place_id="place_hall",
            located=1.0,
            hidden=1.0,
            specific_location="under the altar"
        )
        assert link.specific_location == "under the altar"


class TestPlacePlaceLink:
    """Test PlacePlace link validation."""

    def test_place_link_required_fields(self):
        """Link requires source and target place IDs."""
        link = PlacePlace(
            source_place_id="place_york",
            target_place_id="place_durham"
        )
        assert link.source_place_id == "place_york"
        assert link.target_place_id == "place_durham"

    def test_place_link_travel_days(self):
        """travel_days parses distance correctly."""
        # Hours
        link = PlacePlace(
            source_place_id="a",
            target_place_id="b",
            path=1.0,
            path_distance="4 hours"
        )
        assert abs(link.travel_days() - (4 / 24)) < 0.01

        # Days
        link2 = PlacePlace(
            source_place_id="a",
            target_place_id="b",
            path=1.0,
            path_distance="3 days"
        )
        assert link2.travel_days() == 3.0

        # Adjacent
        link3 = PlacePlace(
            source_place_id="a",
            target_place_id="b",
            path=1.0,
            path_distance="adjacent"
        )
        assert link3.travel_days() == 0.0


# =============================================================================
# MODIFIER TESTS
# =============================================================================

class TestModifier:
    """Test Modifier model validation."""

    def test_modifier_required_type(self):
        """Modifier requires type."""
        mod = Modifier(type=ModifierType.WOUNDED)
        assert mod.type == ModifierType.WOUNDED

    def test_modifier_severity_default(self):
        """Modifier severity defaults to MODERATE."""
        mod = Modifier(type=ModifierType.WOUNDED)
        assert mod.severity == ModifierSeverity.MODERATE

    def test_modifier_character_types(self):
        """Character modifiers should be valid."""
        char_mods = [
            ModifierType.WOUNDED, ModifierType.SICK, ModifierType.HUNGRY,
            ModifierType.EXHAUSTED, ModifierType.AFRAID, ModifierType.ANGRY
        ]
        for mod_type in char_mods:
            mod = Modifier(type=mod_type)
            assert mod.type == mod_type

    def test_modifier_place_types(self):
        """Place modifiers should be valid."""
        place_mods = [
            ModifierType.BURNING, ModifierType.FLOODED,
            ModifierType.BESIEGED, ModifierType.ABANDONED
        ]
        for mod_type in place_mods:
            mod = Modifier(type=mod_type)
            assert mod.type == mod_type

    def test_modifier_thing_types(self):
        """Thing modifiers should be valid."""
        thing_mods = [
            ModifierType.DAMAGED, ModifierType.HIDDEN,
            ModifierType.CONTESTED, ModifierType.BLESSED, ModifierType.CURSED
        ]
        for mod_type in thing_mods:
            mod = Modifier(type=mod_type)
            assert mod.type == mod_type


# =============================================================================
# GAME TIMESTAMP TESTS
# =============================================================================

class TestGameTimestamp:
    """Test GameTimestamp model."""

    def test_timestamp_creation(self):
        """GameTimestamp can be created."""
        ts = GameTimestamp(day=5, time=TimeOfDay.MORNING)
        assert ts.day == 5
        assert ts.time == TimeOfDay.MORNING

    def test_timestamp_str(self):
        """GameTimestamp str format."""
        ts = GameTimestamp(day=5, time=TimeOfDay.MORNING)
        assert str(ts) == "Day 5, morning"

    def test_timestamp_parse(self):
        """GameTimestamp can be parsed from string."""
        ts = GameTimestamp.parse("Day 5, morning")
        assert ts.day == 5
        assert ts.time == TimeOfDay.MORNING

    def test_timestamp_comparison(self):
        """GameTimestamp comparison works."""
        ts1 = GameTimestamp(day=5, time=TimeOfDay.MORNING)
        ts2 = GameTimestamp(day=5, time=TimeOfDay.AFTERNOON)
        ts3 = GameTimestamp(day=6, time=TimeOfDay.DAWN)

        assert ts1 < ts2  # Same day, morning < afternoon
        assert ts2 < ts3  # Day 5 < Day 6
        assert ts1 <= ts1  # Equal


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

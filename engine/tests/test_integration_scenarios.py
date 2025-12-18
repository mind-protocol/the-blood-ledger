"""
Integration Test Scenarios — Structural Tests

High-level tests that verify the STRUCTURE supports the complete spec.
These tests validate that models and relationships exist to enable gameplay.

VALIDATES:
    V5.1: "I know them" — Character knowledge is queryable (structure)
    V5.2: "They remembered" — Narratives persist and surface (structure)
    V5.3: "The world moved" — Time passes and events happen (structure)
    V5.4: "I was wrong" — False beliefs can be discovered (structure)
    V6: Anti-patterns — Things that MUST NOT happen

TESTS IMPLEMENTATIONS:
    engine/models/nodes.py — Narrative.voice, Narrative.truth, Narrative.is_core_type
    engine/models/links.py — CharacterNarrative.belief_intensity
    engine/models/tensions.py — Tension.tick_gradual, has_flipped

DOES NOT TEST (see test_implementation.py):
    Actual database operations
    Full gameplay loops with real data

REFERENCES:
    docs/engine/VALIDATION_Complete_Spec.md — All invariants
    docs/engine/TEST_Complete_Spec.md — Test index

RUN:
    pytest test_integration_scenarios.py -v
"""

import pytest
from pathlib import Path
import sys
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.models.base import (
    CharacterType, NarrativeType, NarrativeTone, NarrativeVoiceStyle,
    BeliefSource, PressureType, VoiceTone, VoiceStyle, Flaw, Value
)
from engine.models.nodes import Character, Place, Thing, Narrative, Moment
from engine.models.links import CharacterNarrative, NarrativeNarrative, CharacterPlace
from engine.models.tensions import Tension


# =============================================================================
# TEST FIXTURES: Game World Builders
# =============================================================================

def build_test_character(
    id: str,
    name: str,
    char_type: CharacterType = CharacterType.COMPANION,
    flaw: Flaw = Flaw.PRIDE,
    values: List[Value] = None
) -> Character:
    """Build a test character with reasonable defaults."""
    from engine.models.base import Personality, CharacterVoice

    return Character(
        id=id,
        name=name,
        type=char_type,
        personality=Personality(
            values=values or [Value.LOYALTY, Value.HONOR],
            flaw=flaw
        ),
        voice=CharacterVoice(
            tone=VoiceTone.MEASURED,
            style=VoiceStyle.DIRECT
        )
    )


def build_test_narrative(
    id: str,
    name: str,
    content: str,
    narr_type: NarrativeType = NarrativeType.MEMORY,
    weight: float = 0.5,
    truth: float = 1.0
) -> Narrative:
    """Build a test narrative with reasonable defaults."""
    from engine.models.base import NarrativeVoice

    return Narrative(
        id=id,
        name=name,
        content=content,
        type=narr_type,
        weight=weight,
        truth=truth,
        voice=NarrativeVoice(style=NarrativeVoiceStyle.REMIND)
    )


def build_belief_link(
    char_id: str,
    narr_id: str,
    heard: float = 1.0,
    believes: float = 0.8,
    source: BeliefSource = BeliefSource.WITNESSED
) -> CharacterNarrative:
    """Build a belief link between character and narrative."""
    return CharacterNarrative(
        character_id=char_id,
        narrative_id=narr_id,
        heard=heard,
        believes=believes,
        source=source
    )


# =============================================================================
# V5.1: "I KNOW THEM" TESTS
# =============================================================================

class TestIKnowThem:
    """
    Test: "I know them" — Character knowledge is queryable.

    The goal: Player can query all narratives a character believes,
    their history, and predict behavior based on beliefs.
    """

    def test_character_beliefs_are_links(self):
        """Character beliefs should be expressed as BELIEVES links, not attributes."""
        char = build_test_character("char_aldric", "Aldric")

        # Character should NOT have belief attributes
        assert not hasattr(char, 'beliefs')
        assert not hasattr(char, 'trust')

    def test_belief_link_captures_knowledge(self):
        """BELIEVES link should capture how much character knows/believes."""
        link = build_belief_link(
            "char_aldric", "narr_oath",
            heard=1.0, believes=0.9
        )

        assert link.heard == 1.0
        assert link.believes == 0.9
        assert link.belief_intensity == 0.9  # heard * max(believes, originated)

    def test_belief_source_is_tracked(self):
        """BELIEVES link should track how character learned narrative."""
        # Witnessed directly
        witnessed = build_belief_link(
            "char_aldric", "narr_battle",
            source=BeliefSource.WITNESSED
        )
        assert witnessed.source == BeliefSource.WITNESSED

        # Told by someone
        told = build_belief_link(
            "char_aldric", "narr_rumor",
            source=BeliefSource.TOLD
        )
        told.from_whom = "char_wulfstan"
        assert told.source == BeliefSource.TOLD
        assert told.from_whom == "char_wulfstan"

    def test_character_personality_predicts_behavior(self):
        """Character personality should be queryable for prediction."""
        char = build_test_character(
            "char_aldric", "Aldric",
            flaw=Flaw.PRIDE,
            values=[Value.LOYALTY, Value.HONOR]
        )

        # Can query personality
        assert char.personality.flaw == Flaw.PRIDE
        assert Value.LOYALTY in char.personality.values
        assert Value.HONOR in char.personality.values

        # This enables prediction: "Aldric values loyalty, has pride as flaw"
        # Therefore: Will keep oaths, but might act rashly if honor questioned

    def test_character_voice_is_consistent(self):
        """Character voice should be defined for narrator consistency."""
        char = build_test_character("char_aldric", "Aldric")

        assert hasattr(char, 'voice')
        assert hasattr(char.voice, 'tone')
        assert hasattr(char.voice, 'style')


# =============================================================================
# V5.2: "THEY REMEMBERED" TESTS
# =============================================================================

class TestTheyRemembered:
    """
    Test: "They remembered" — Narratives persist and surface.

    The goal: Narratives from early sessions surface in later sessions
    when relevant (weight still high, context matches).
    """

    def test_narrative_persists(self):
        """Narratives should persist with weight."""
        narr = build_test_narrative(
            "narr_aldric_oath",
            "Aldric's Oath",
            "Aldric swore to protect Rolf with his life",
            NarrativeType.OATH,
            weight=0.7
        )

        assert narr.id == "narr_aldric_oath"
        assert narr.weight == 0.7

    def test_core_types_persist_longer(self):
        """Core types (oath, blood, debt) should be flagged for slower decay."""
        oath = build_test_narrative(
            "narr_oath", "The Oath", "Oath content",
            NarrativeType.OATH
        )
        assert oath.is_core_type is True

        blood = build_test_narrative(
            "narr_blood", "Blood Bond", "Blood content",
            NarrativeType.BLOOD
        )
        assert blood.is_core_type is True

        debt = build_test_narrative(
            "narr_debt", "The Debt", "Debt content",
            NarrativeType.DEBT
        )
        assert debt.is_core_type is True

        memory = build_test_narrative(
            "narr_memory", "A Memory", "Memory content",
            NarrativeType.MEMORY
        )
        assert memory.is_core_type is False

    def test_narrative_has_voice_for_surfacing(self):
        """Narratives should have voice for how they surface."""
        narr = build_test_narrative(
            "narr_test", "Test", "Test content",
            NarrativeType.OATH
        )
        narr.voice.style = NarrativeVoiceStyle.REMIND
        narr.voice.phrases = ["Remember your oath.", "You swore."]

        assert narr.voice.style == NarrativeVoiceStyle.REMIND
        assert len(narr.voice.phrases) == 2

    def test_weight_affects_surfacing(self):
        """Higher weight narratives should be more likely to surface."""
        high_weight = build_test_narrative(
            "narr_high", "Important", "Important content",
            weight=0.9
        )
        low_weight = build_test_narrative(
            "narr_low", "Minor", "Minor content",
            weight=0.2
        )

        # In practice, narrator would sort by weight
        narratives = [high_weight, low_weight]
        sorted_narrs = sorted(narratives, key=lambda n: n.weight, reverse=True)

        assert sorted_narrs[0].weight > sorted_narrs[1].weight


# =============================================================================
# V5.3: "THE WORLD MOVED" TESTS
# =============================================================================

class TestTheWorldMoved:
    """
    Test: "The world moved" — Time passes and events happen without player.

    The goal: Tensions tick in background, events can happen off-screen,
    player discovers what happened.
    """

    def test_tensions_accumulate_over_time(self):
        """Tensions should accumulate pressure over elapsed time."""
        tension = Tension(
            id="tension_test",
            pressure=0.3,
            pressure_type=PressureType.GRADUAL,
            base_rate=0.001
        )

        # Simulate 100 minutes passing
        initial = tension.pressure
        tension.tick_gradual(100, focus=1.0, max_weight=1.0)

        # Pressure should have increased
        assert tension.pressure > initial

    def test_tension_flips_when_pressure_high(self):
        """Tension should flip when pressure >= breaking_point."""
        tension = Tension(
            id="tension_test",
            pressure=0.85,
            breaking_point=0.9
        )

        assert tension.has_flipped is False

        # Push over breaking point
        tension.add_event_pressure(0.1)

        assert tension.has_flipped is True

    def test_scheduled_tension_follows_timeline(self):
        """Scheduled tensions should follow their progression."""
        from engine.models.base import TensionProgression

        tension = Tension(
            id="tension_malet",
            pressure_type=PressureType.SCHEDULED,
            progression=[
                TensionProgression(at="Day 14", pressure=0.3),
                TensionProgression(at="Day 15", pressure=0.6),
                TensionProgression(at="Day 16", pressure=0.9),
            ]
        )

        assert tension.pressure_type == PressureType.SCHEDULED
        assert len(tension.progression) == 3

    def test_multiple_tensions_can_exist(self):
        """Multiple independent tensions should exist simultaneously."""
        tensions = [
            Tension(id="tension_1", pressure=0.3),
            Tension(id="tension_2", pressure=0.6),
            Tension(id="tension_3", pressure=0.8),
        ]

        # Each has independent state
        pressures = [t.pressure for t in tensions]
        assert pressures == [0.3, 0.6, 0.8]


# =============================================================================
# V5.4: "I WAS WRONG" TESTS
# =============================================================================

class TestIWasWrong:
    """
    Test: "I was wrong" — Player can believe false things.

    The goal: Player beliefs can be mistaken (truth < 1),
    discovery is possible, belief updates propagate.
    """

    def test_narrative_can_be_false(self):
        """Narratives can have truth < 1 (director-only)."""
        lie = build_test_narrative(
            "narr_lie",
            "Edmund's Lie",
            "Edmund said he was forced to betray us",
            NarrativeType.LIE,
            truth=0.2  # Mostly false
        )

        assert lie.truth == 0.2

    def test_truth_is_not_visible_to_player(self):
        """Truth field should exist but is director-only."""
        narr = build_test_narrative(
            "narr_test", "Test", "Test",
            truth=0.5
        )

        # Truth exists on model
        assert hasattr(narr, 'truth')
        assert narr.truth == 0.5

        # In actual gameplay, player queries would NOT include truth

    def test_character_can_believe_lie(self):
        """Characters can believe narratives regardless of truth."""
        lie = build_test_narrative(
            "narr_edmund_innocent",
            "Edmund's Innocence",
            "Edmund was forced to betray us",
            NarrativeType.LIE,
            truth=0.0  # Completely false
        )

        # Aldric believes it anyway
        belief = build_belief_link(
            "char_aldric", "narr_edmund_innocent",
            heard=1.0, believes=0.9  # Strongly believes
        )

        assert belief.believes == 0.9
        # lie.truth is independent of belief strength

    def test_contradicting_narratives_create_tension(self):
        """Contradicting narratives should be linkable."""
        narr_betrayed = build_test_narrative(
            "narr_betrayed",
            "Betrayal",
            "Edmund betrayed us willingly",
            truth=1.0
        )
        narr_forced = build_test_narrative(
            "narr_forced",
            "Forced",
            "Edmund was forced to betray us",
            truth=0.0
        )

        # These should contradict
        link = NarrativeNarrative(
            source_narrative_id="narr_betrayed",
            target_narrative_id="narr_forced",
            contradicts=0.9
        )

        assert link.contradicts == 0.9
        assert link.link_type == "contradicts"


# =============================================================================
# V6: ANTI-PATTERN TESTS
# =============================================================================

class TestAntiPatterns:
    """
    Tests that anti-patterns (failure states) are prevented.

    V6.1: "Quest Log" — Ledger is NOT a task list
    V6.2: "Optimal Choice" — No single best answer
    V6.3: "Skip Dialog" — Text should be engaging
    V6.4: "Who is this again?" — Characters should be memorable
    """

    def test_no_quest_completion_field(self):
        """Narratives should NOT have completion/progress fields."""
        narr = build_test_narrative(
            "narr_debt", "A Debt", "You owe Edmund",
            NarrativeType.DEBT
        )

        # Should NOT have these
        assert not hasattr(narr, 'completed')
        assert not hasattr(narr, 'progress')
        assert not hasattr(narr, 'objectives')

    def test_no_optimal_score(self):
        """Characters should NOT have relationship scores."""
        char = build_test_character("char_aldric", "Aldric")

        # Should NOT have these
        assert not hasattr(char, 'relationship_score')
        assert not hasattr(char, 'approval')
        assert not hasattr(char, 'loyalty_points')

    def test_characters_have_distinctive_voice(self):
        """Each character should have distinctive voice settings."""
        char1 = build_test_character("char_1", "Character 1")
        char1.voice.tone = VoiceTone.BITTER
        char1.voice.style = VoiceStyle.SARDONIC

        char2 = build_test_character("char_2", "Character 2")
        char2.voice.tone = VoiceTone.WARM
        char2.voice.style = VoiceStyle.GENTLE

        # Different voices
        assert char1.voice.tone != char2.voice.tone
        assert char1.voice.style != char2.voice.style

    def test_characters_have_distinctive_flaw(self):
        """Each character should have a distinctive flaw."""
        char = build_test_character(
            "char_aldric", "Aldric",
            flaw=Flaw.PRIDE
        )

        assert char.personality.flaw is not None
        assert char.personality.flaw == Flaw.PRIDE


# =============================================================================
# SCENARIO: Complete Gameplay Loop
# =============================================================================

class TestCompleteGameplayLoop:
    """
    Test a complete gameplay scenario structurally.

    Scenario: Player talks to Aldric, time passes, tension flips,
    World Runner resolves it, new narratives created.
    """

    def test_scene_produces_moment(self):
        """Scene interactions should produce Moments."""
        moment = Moment(
            id="camp_d3_night_dialogue_001",
            text="I swore an oath. That hasn't changed.",
            tick=3600,  # Day 3
        )

        assert moment.id.startswith("camp_")
        assert "oath" in moment.text.lower()

    def test_tension_accumulates_during_scene(self):
        """While scene plays, tension ticks."""
        tension = Tension(
            id="tension_loyalty",
            pressure=0.4,
            base_rate=0.001
        )

        # Scene takes 30 minutes of game time
        tension.tick_gradual(30, focus=1.0, max_weight=0.8)

        # Pressure increased
        assert tension.pressure > 0.4

    def test_flip_produces_world_runner_event(self):
        """When tension flips, World Runner should be triggered."""
        tension = Tension(
            id="tension_confrontation",
            pressure=0.95,
            breaking_point=0.9
        )

        assert tension.has_flipped is True

        # World Runner would be called with:
        # - tension_id
        # - narrative_ids in tension
        # - current world state

    def test_world_runner_creates_new_narratives(self):
        """World Runner resolution creates new narratives."""
        # Simulating what World Runner would create
        result_narrative = build_test_narrative(
            "narr_confrontation_result",
            "The Confrontation",
            "Edmund and Rolf met at the crossroads. Blades were drawn.",
            NarrativeType.MEMORY
        )

        assert result_narrative.type == NarrativeType.MEMORY

    def test_new_narrative_propagates_beliefs(self):
        """New narratives should spread to characters present."""
        # Characters at the event believe it
        char_belief = build_belief_link(
            "char_aldric",
            "narr_confrontation_result",
            heard=1.0,
            believes=1.0,
            source=BeliefSource.WITNESSED
        )

        assert char_belief.source == BeliefSource.WITNESSED

        # Character not present might hear about it
        secondhand_belief = build_belief_link(
            "char_wulfstan",
            "narr_confrontation_result",
            heard=0.7,  # Partial knowledge
            believes=0.6,  # Some doubt
            source=BeliefSource.TOLD
        )
        secondhand_belief.from_whom = "char_aldric"

        assert secondhand_belief.source == BeliefSource.TOLD
        assert secondhand_belief.heard < 1.0  # Incomplete knowledge


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Blood Ledger — Data Models

Complete Pydantic models for the Blood Ledger schema.
Based on SCHEMA.md v5.1

Nodes (4 types):
- Character: A person who can act, speak, remember, die
- Place: A location with atmosphere and geography
- Thing: An object that can be owned, given, stolen, fought over
- Narrative: A story that characters believe

Links (6 types):
- CharacterNarrative: What a character knows/believes
- NarrativeNarrative: How stories relate
- CharacterPlace: Physical presence (ground truth)
- CharacterThing: Physical possession (ground truth)
- ThingPlace: Where things are (ground truth)
- PlacePlace: Geography (ground truth)

Tensions:
- Tension: Cluster of narratives under pressure
"""

# Nodes
from .nodes import Character, Place, Thing, Narrative

# Links
from .links import (
    CharacterNarrative,
    NarrativeNarrative,
    CharacterPlace,
    CharacterThing,
    ThingPlace,
    PlacePlace
)

# Tensions
from .tensions import Tension

# Base types and enums
from .base import (
    # Character enums
    CharacterType, Face, SkillLevel, VoiceTone, VoiceStyle,
    Approach, Value, Flaw,
    # Place enums
    PlaceType, Weather, Mood,
    # Thing enums
    ThingType, Significance,
    # Narrative enums
    NarrativeType, NarrativeTone, NarrativeVoiceStyle,
    # Link enums
    BeliefSource, PathDifficulty,
    # Tension enums
    PressureType,
    # Modifier enums
    ModifierType, ModifierSeverity,
    # Shared models
    Modifier, Skills, CharacterVoice, Personality, Backstory,
    Atmosphere, NarrativeAbout, NarrativeVoice, TensionProgression
)

__all__ = [
    # Nodes
    'Character', 'Place', 'Thing', 'Narrative',
    # Links
    'CharacterNarrative', 'NarrativeNarrative',
    'CharacterPlace', 'CharacterThing', 'ThingPlace', 'PlacePlace',
    # Tensions
    'Tension',
    # Enums
    'CharacterType', 'Face', 'SkillLevel', 'VoiceTone', 'VoiceStyle',
    'Approach', 'Value', 'Flaw',
    'PlaceType', 'Weather', 'Mood',
    'ThingType', 'Significance',
    'NarrativeType', 'NarrativeTone', 'NarrativeVoiceStyle',
    'BeliefSource', 'PathDifficulty',
    'PressureType',
    'ModifierType', 'ModifierSeverity',
    # Shared models
    'Modifier', 'Skills', 'CharacterVoice', 'Personality', 'Backstory',
    'Atmosphere', 'NarrativeAbout', 'NarrativeVoice', 'TensionProgression'
]

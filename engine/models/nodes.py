"""
Blood Ledger — Node Models

The 4 node types: Character, Place, Thing, Narrative, Moment
Based on SCHEMA.md v5.1

DOCS: docs/schema/

TESTS:
    engine/tests/test_models.py::TestCharacterModel
    engine/tests/test_models.py::TestPlaceModel
    engine/tests/test_models.py::TestThingModel
    engine/tests/test_models.py::TestNarrativeModel
    engine/tests/test_models.py::TestMomentModel
    engine/tests/test_integration_scenarios.py (structural tests)

VALIDATES:
    V2.1: Character invariants (id, name, type, skills, voice, personality)
    V2.2: Place invariants (id, name, type, atmosphere)
    V2.3: Thing invariants (id, name, type, significance, portable)
    V2.4: Narrative invariants (id, name, content, type, weight, focus, truth)
    V2.6: Moment invariants (id, text, type, tick)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from .base import (
    CharacterType, Face, Skills, CharacterVoice, Personality, Backstory, Modifier,
    PlaceType, Atmosphere,
    ThingType, Significance,
    NarrativeType, NarrativeTone, NarrativeVoice, NarrativeAbout,
    NarrativeSource,
    MomentType, MomentStatus, MomentTrigger
)


class Character(BaseModel):
    """
    CHARACTER - A person who exists in the world, with voice, history, and agency.
    Anyone who can act, speak, remember, die.
    """
    id: str
    name: str
    type: CharacterType = CharacterType.MINOR
    alive: bool = True
    face: Optional[Face] = None

    skills: Skills = Field(default_factory=Skills)
    voice: CharacterVoice = Field(default_factory=CharacterVoice)
    personality: Personality = Field(default_factory=Personality)
    backstory: Backstory = Field(default_factory=Backstory)

    modifiers: List[Modifier] = Field(default_factory=list)

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.backstory.why_here:
            parts.append(f"Why here: {self.backstory.why_here}")
        if self.backstory.wound:
            parts.append(f"Wound: {self.backstory.wound}")
        if self.personality.values:
            parts.append(f"Values: {', '.join(v.value for v in self.personality.values)}")
        return ". ".join(parts)


class Place(BaseModel):
    """
    PLACE - A location where things happen, with atmosphere and geography.
    Anywhere that can be located, traveled to, occupied.
    """
    id: str
    name: str
    type: PlaceType = PlaceType.VILLAGE

    atmosphere: Atmosphere = Field(default_factory=Atmosphere)
    modifiers: List[Modifier] = Field(default_factory=list)

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.atmosphere.mood:
            parts.append(f"Mood: {self.atmosphere.mood.value}")
        if self.atmosphere.details:
            parts.append(f"Details: {', '.join(self.atmosphere.details)}")
        return ". ".join(parts)


class Thing(BaseModel):
    """
    THING - An object that can be owned, given, stolen, or fought over.
    Anything that can be possessed, transferred, contested.
    """
    id: str
    name: str
    type: ThingType = ThingType.TOOL
    portable: bool = True
    significance: Significance = Significance.MUNDANE
    quantity: int = 1
    description: str = ""

    modifiers: List[Modifier] = Field(default_factory=list)

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.description:
            parts.append(self.description)
        if self.significance != Significance.MUNDANE:
            parts.append(f"Significance: {self.significance.value}")
        return ". ".join(parts)


class Narrative(BaseModel):
    """
    NARRATIVE - A story that characters believe, creating all relationships and knowledge.

    Core insight: Everything is story. "Aldric is loyal" is a narrative, not a stat.
    Characters believe narratives. They don't have relationships - they have stories
    they tell themselves about relationships.

    History insight: History is distributed. Narratives about the past exist as beliefs,
    not as a central event log. Player-experienced history points to conversation files;
    world-generated history carries its own detail.
    """
    id: str
    name: str
    content: str = Field(description="The story itself - what happened, what is believed")
    interpretation: str = Field(default="", description="What it means - emotional/thematic weight")

    type: NarrativeType

    about: NarrativeAbout = Field(default_factory=NarrativeAbout)
    tone: Optional[NarrativeTone] = None
    voice: NarrativeVoice = Field(default_factory=NarrativeVoice)

    # History fields - when did this happen?
    # NOTE: "where" is expressed via OCCURRED_AT link to Place, not an attribute
    occurred_at: Optional[str] = Field(default=None, description="When event happened: 'Day N, time_of_day'")

    # History content - ONE of these for historical narratives
    source: Optional[NarrativeSource] = Field(
        default=None,
        description="For player-experienced history: reference to conversation file section"
    )
    detail: Optional[str] = Field(
        default=None,
        description="For world-generated history: full description (no conversation exists)"
    )

    # System fields (computed by graph engine)
    weight: float = Field(default=0.0, ge=0.0, le=1.0, description="Importance - computed by graph engine")
    focus: float = Field(default=1.0, ge=0.1, le=3.0, description="Narrator pacing adjustment")

    # Director only (hidden from players/characters)
    truth: float = Field(default=1.0, ge=0.0, le=1.0, description="How true is this? Characters never see this.")
    narrator_notes: str = Field(default="", description="Narrator's notes for continuity")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}: {self.content}"]
        if self.interpretation:
            parts.append(f"Meaning: {self.interpretation}")
        if self.tone:
            parts.append(f"Tone: {self.tone.value}")
        return ". ".join(parts)

    @property
    def is_core_type(self) -> bool:
        """Core types (oath, blood, debt) decay slower."""
        return self.type in [NarrativeType.OATH, NarrativeType.BLOOD, NarrativeType.DEBT]


class Moment(BaseModel):
    """
    MOMENT - A single unit of narrated content OR a potential moment.

    In the Moment Graph architecture, moments exist in a possibility space.
    They can be:
    - possible: Created but not yet surfaced
    - active: Visible to player, can be triggered
    - spoken: Part of history
    - dormant: Waiting for player return
    - decayed: Pruned

    Links:
        Character -[CAN_SPEAK]-> Moment (who can say this)
        Character -[SAID]-> Moment (who said this - after spoken)
        Moment -[ATTACHED_TO]-> Character|Place|Thing|Narrative
        Moment -[CAN_LEAD_TO]-> Moment (traversal)
        Moment -[THEN]-> Moment (sequence after spoken)
        Moment -[AT]-> Place (where it occurred)
        Narrative -[FROM]-> Moment (source attribution)

    Note: Speaker is NOT an attribute - use SAID link to find who spoke.
    """
    id: str = Field(description="Unique ID: {place}_{day}_{time}_{type}_{timestamp}")
    text: str = Field(description="The actual text content")
    type: MomentType = MomentType.NARRATION

    # Moment Graph fields
    status: MomentStatus = Field(
        default=MomentStatus.SPOKEN,  # Default for backward compat
        description="Lifecycle status in moment graph"
    )
    weight: float = Field(
        default=0.5,
        ge=0.0, le=1.0,
        description="Salience/importance (computed from graph topology)"
    )
    tone: Optional[str] = Field(
        default=None,
        description="Emotional tone: bitter, hopeful, urgent, etc."
    )

    # Tick tracking (expanded from single tick)
    tick_created: int = Field(
        default=0, ge=0,
        alias="tick",
        description="World tick when moment was created"
    )
    tick_spoken: Optional[int] = Field(
        default=None,
        description="World tick when moment was spoken (if spoken)"
    )
    tick_decayed: Optional[int] = Field(
        default=None,
        description="World tick when moment decayed (if decayed)"
    )

    # Backward compat alias
    @property
    def tick(self) -> int:
        """Backward compat: tick refers to tick_created."""
        return self.tick_created

    # Transcript reference - line number in playthroughs/{id}/transcript.json
    line: Optional[int] = Field(default=None, description="Starting line in transcript.json")

    # Speaker reference (derived from SAID link, not stored on node)
    speaker: Optional[str] = Field(default=None, description="Character ID for dialogue moments")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    # Query fields (for backstory generation)
    query: Optional[str] = Field(
        default=None,
        description="Question this moment asks (triggers backstory generation)"
    )
    query_type: Optional[str] = Field(
        default=None,
        description="Type of query: backstory_gap, clarification, etc."
    )
    query_filled: bool = Field(
        default=False,
        description="Whether the query has been answered"
    )

    def embeddable_text(self) -> str:
        """Generate text for embedding (speaker added by processor if dialogue)."""
        if self.type == MomentType.DIALOGUE and self.speaker:
            return f"{self.speaker}: {self.text}"
        return self.text

    @property
    def should_embed(self) -> bool:
        """Only embed if text is meaningful length."""
        return len(self.text.strip()) > 20

    @property
    def is_active(self) -> bool:
        """Check if moment is currently active."""
        return self.status == MomentStatus.ACTIVE

    @property
    def is_spoken(self) -> bool:
        """Check if moment has been spoken."""
        return self.status == MomentStatus.SPOKEN

    @property
    def can_surface(self) -> bool:
        """Check if moment can potentially surface."""
        return self.status in [MomentStatus.POSSIBLE, MomentStatus.ACTIVE]

    class Config:
        allow_population_by_field_name = True

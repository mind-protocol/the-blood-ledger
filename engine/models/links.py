"""
Blood Ledger — Link Models

The 6 link types that connect nodes.
Based on SCHEMA.md v5.1

TESTS:
    engine/tests/test_models.py::TestCharacterNarrativeLink
    engine/tests/test_models.py::TestNarrativeNarrativeLink
    engine/tests/test_models.py::TestCharacterPlaceLink
    engine/tests/test_models.py::TestCharacterThingLink
    engine/tests/test_models.py::TestThingPlaceLink
    engine/tests/test_models.py::TestPlacePlaceLink

VALIDATES:
    V3.1: BELIEVES link (Character -> Narrative)
    V3.2: NARRATIVE_NARRATIVE links (contradicts, supports, etc.)
    V3.3: Ground truth links (AT, CARRIES, LOCATED_AT, CONTAINS, ROUTE)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .base import BeliefSource, PathDifficulty


class CharacterNarrative(BaseModel):
    """
    CHARACTER_NARRATIVE - What a character knows, believes, doubts, hides, or spreads.

    This link IS how characters know things. There is no "knowledge" stat.
    Aldric knows about the betrayal because he has a link to that narrative
    with heard=1.0 and believes=0.9.

    History: Every memory is mediated through a BELIEVES link. Characters can be
    wrong, confidence varies, sources can be traced.
    """
    # Link endpoints
    character_id: str
    narrative_id: str

    # Knowledge (0-1) - how much do they know/believe?
    heard: float = Field(default=0.0, ge=0.0, le=1.0, description="Has encountered this story")
    believes: float = Field(default=0.0, ge=0.0, le=1.0, description="Holds as true")
    doubts: float = Field(default=0.0, ge=0.0, le=1.0, description="Actively uncertain")
    denies: float = Field(default=0.0, ge=0.0, le=1.0, description="Rejects as false")

    # Action (0-1) - what are they doing with this knowledge?
    hides: float = Field(default=0.0, ge=0.0, le=1.0, description="Knows but conceals")
    spreads: float = Field(default=0.0, ge=0.0, le=1.0, description="Actively promoting")

    # Origin
    originated: float = Field(default=0.0, ge=0.0, le=1.0, description="Created this narrative")

    # Metadata - how did they learn?
    source: BeliefSource = BeliefSource.NONE
    from_whom: str = Field(default="", description="Who told them")
    when: Optional[datetime] = None
    where: Optional[str] = Field(default=None, description="Place ID where they learned this")

    @property
    def belief_intensity(self) -> float:
        """Combined intensity of belief for energy calculations."""
        return max(self.believes, self.originated) * self.heard


class NarrativeNarrative(BaseModel):
    """
    NARRATIVE_NARRATIVE - How stories relate: contradict, support, elaborate, subsume, supersede.

    These links create story structure. Contradicting narratives create drama.
    Supporting narratives create belief clusters. Superseding narratives
    let the world evolve.
    """
    # Link endpoints
    source_narrative_id: str
    target_narrative_id: str

    # Relationship strengths (0-1)
    contradicts: float = Field(default=0.0, ge=0.0, le=1.0, description="Cannot both be true")
    supports: float = Field(default=0.0, ge=0.0, le=1.0, description="Reinforce each other")
    elaborates: float = Field(default=0.0, ge=0.0, le=1.0, description="Adds detail")
    subsumes: float = Field(default=0.0, ge=0.0, le=1.0, description="Specific case of")
    supersedes: float = Field(default=0.0, ge=0.0, le=1.0, description="Replaces - old fades")

    @property
    def link_type(self) -> str:
        """Return the dominant relationship type."""
        attrs = {
            'contradicts': self.contradicts,
            'supports': self.supports,
            'elaborates': self.elaborates,
            'subsumes': self.subsumes,
            'supersedes': self.supersedes
        }
        return max(attrs, key=attrs.get)


class CharacterPlace(BaseModel):
    """
    CHARACTER_PLACE - Where a character physically is (ground truth).

    This is GROUND TRUTH, not belief. A character IS at a place,
    regardless of what anyone believes.
    """
    # Link endpoints
    character_id: str
    place_id: str

    # Physical state
    present: float = Field(default=0.0, ge=0.0, le=1.0, description="1=here, 0=not here")
    visible: float = Field(default=1.0, ge=0.0, le=1.0, description="0=hiding, 1=visible")

    @property
    def is_present(self) -> bool:
        return self.present > 0.5


class CharacterThing(BaseModel):
    """
    CHARACTER_THING - What a character physically carries (ground truth).

    Ground truth. They HAVE it or they don't.
    Separate from ownership narratives (who SHOULD have it).
    """
    # Link endpoints
    character_id: str
    thing_id: str

    # Physical state
    carries: float = Field(default=0.0, ge=0.0, le=1.0, description="1=has it, 0=doesn't")
    carries_hidden: float = Field(default=0.0, ge=0.0, le=1.0, description="1=secretly, 0=openly")

    @property
    def has_item(self) -> bool:
        return self.carries > 0.5 or self.carries_hidden > 0.5


class ThingPlace(BaseModel):
    """
    THING_PLACE - Where an uncarried thing physically is (ground truth).

    Where things ARE, not where people think they are.
    """
    # Link endpoints
    thing_id: str
    place_id: str

    # Physical state
    located: float = Field(default=0.0, ge=0.0, le=1.0, description="1=here, 0=not here")
    hidden: float = Field(default=0.0, ge=0.0, le=1.0, description="1=concealed, 0=visible")
    specific_location: str = Field(default="", description="Where exactly")

    @property
    def is_here(self) -> bool:
        return self.located > 0.5


class PlacePlace(BaseModel):
    """
    PLACE_PLACE - How locations connect: contains, path, borders (ground truth).

    Geography determines travel time, which affects proximity,
    which affects how much characters matter to the player.
    """
    # Link endpoints
    source_place_id: str
    target_place_id: str

    # Spatial relationships
    contains: float = Field(default=0.0, ge=0.0, le=1.0, description="This place is inside that")
    path: float = Field(default=0.0, ge=0.0, le=1.0, description="Can travel between")
    path_distance: str = Field(default="", description="How far: '2 days', '4 hours'")
    path_difficulty: PathDifficulty = PathDifficulty.MODERATE
    borders: float = Field(default=0.0, ge=0.0, le=1.0, description="Share a border")

    def travel_days(self) -> float:
        """Parse path_distance into days for proximity calculation."""
        if not self.path_distance:
            return 1.0

        dist = self.path_distance.lower()
        if 'adjacent' in dist or 'same' in dist:
            return 0.0
        elif 'hour' in dist:
            # Extract number of hours
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1)) / 24.0
            return 0.1
        elif 'day' in dist:
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1))
            return 1.0
        else:
            return 1.0

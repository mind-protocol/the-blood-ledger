# Schema Links

## NARRATIVE -> NARRATIVE

Purpose: How stories relate (contradict, support, elaborate, subsume, supersede).

When to create:
- Two narratives are in tension or reinforce each other
- New information replaces old

Attributes:
```yaml
contradicts: float
supports: float
elaborates: float
subsumes: float
supersedes: float
```

## CHARACTER -> PLACE (Presence)

Purpose: Ground truth physical location of a character.

Attributes:
```yaml
present: float
visible: float
```

## CHARACTER -> THING (Possession)

Purpose: Ground truth physical possession.

Attributes:
```yaml
carries: float
carries_hidden: float
```

## THING -> PLACE (Location)

Purpose: Ground truth location for uncarried things.

Attributes:
```yaml
located: float
hidden: float
specific_location: string
```

## PLACE -> PLACE (Containment)

Purpose: Hierarchical containment (binary).

Attributes: none

## PLACE -> PLACE (Route)

Purpose: Travel connection between settlements/regions.

Attributes:
```yaml
waypoints: float[][]
road_type: enum [roman, track, path, river, none]
distance_km: float (computed)
travel_minutes: integer (computed)
difficulty: enum [easy, moderate, hard, dangerous] (computed)
detail: string
```

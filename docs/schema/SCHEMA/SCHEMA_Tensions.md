# Schema Tensions

Purpose: A cluster of narratives under pressure that will eventually break.

When to create:
- Contradicting narratives must resolve
- Deadlines or confrontations are brewing

When to update:
- Pressure changes via time or events
- Narratives added/removed

Attributes:
```yaml
id: string
narratives: string[]
description: string
narrator_notes: string
pressure_type: enum [gradual, scheduled, hybrid]
pressure: float
breaking_point: float
base_rate: float
trigger_at: string
progression:
  - at: string
    pressure: float
    pressure_floor: float
```

Examples:
```yaml
# Gradual
tension_aldric_loyalty:
  pressure_type: gradual
  pressure: 0.4
  base_rate: 0.001
  breaking_point: 0.9

# Scheduled
tension_malet_inspection:
  pressure_type: scheduled
  trigger_at: "Day 16, morning"
  progression:
    - { at: "Day 14", pressure: 0.1 }
    - { at: "Day 16 dawn", pressure: 0.9 }

# Hybrid
tension_edmund_confrontation:
  pressure_type: hybrid
  pressure: 0.5
  progression:
    - { at: "Day 12", pressure_floor: 0.5 }
    - { at: "Day 14", pressure_floor: 0.85 }
```

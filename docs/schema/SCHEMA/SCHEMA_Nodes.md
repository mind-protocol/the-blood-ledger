# Schema Nodes

## Common Metrics

Every node tracks `energy` and `weight` so the physics system can surface the highest-salience entities without duplicating state in downstream code.

```yaml
energy: 0.0-1.0    # Computed energy level (rising with focus/tension)
weight: 0.0-1.0    # Derived visibility score used for surfacing
```

## CHARACTER

Purpose: A person who exists in the world and can act, speak, and remember.

When to create:
- A new person enters the story or is mentioned
- World Runner determines someone acted off-screen

When to update:
- Character dies or gains/loses a modifier

Attributes:
```yaml
id: string
name: string
type: enum [player, companion, major, minor, background]
alive: boolean
face: enum [young, scarred, weathered, gaunt, hard, noble]
skills: { fighting, tracking, healing, persuading, sneaking, riding, reading, leading }
voice: { tone, style }
personality: { approach, values[], flaw }
backstory: { family, childhood, wound, why_here }
modifiers: []
image_prompt: string
energy: float
weight: float
```

## PLACE

Purpose: A location where things happen, with atmosphere and geography.

When to create:
- Player travels to a new location
- A location is mentioned that might be visited

When to update:
- Atmosphere or modifiers change

Attributes:
```yaml
id: string
name: string
coordinates: [lat, lng]
scale: enum [region, settlement, district, building, room]
type: enum [region, city, hold, village, monastery, camp, road, room, wilderness, ruin]
atmosphere: { weather[], mood, details[] }
modifiers: []
image_prompt: string
energy: float
weight: float
```

## THING

Purpose: An object that can be owned, given, stolen, or fought over.

When to create:
- Object becomes narratively relevant
- Something is given, stolen, found, or fought over

When to update:
- Thing is damaged, hidden, blessed, cursed, or consumed

Attributes:
```yaml
id: string
name: string
type: enum [weapon, armor, document, letter, relic, treasure, title, land, token, provisions, coin_purse, horse, ship, tool]
portable: boolean
significance: enum [mundane, personal, political, sacred, legendary]
quantity: integer
description: string
modifiers: []
image_prompt: string
energy: float
weight: float
```

## NARRATIVE

Purpose: A story that characters believe, creating relationships, knowledge, and conflict.

When to create:
- An event occurs that characters will remember or discuss
- A relationship forms, changes, or is revealed
- Information is learned, spread, or discovered

When to update:
- Narrator adds notes or adjusts focus

Attributes:
```yaml
id: string
name: string
content: string
interpretation: string
type: enum
about: { characters[], places[], things[], relationships[] }
tone: string
weight: float
focus: float
truth: float
narrator_notes: string
occurred_at: string
visibility: enum [public, secret, known_to_few]
deadline: datetime
conditions: string[]
energy: float
```

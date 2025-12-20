# Schema Overview

```
STATUS: CANONICAL
UPDATED: 2025-12-19
VERSION: 5.1
```

## CHAIN

```
THIS:     SCHEMA/SCHEMA_Overview.md
NODES:    SCHEMA/SCHEMA_Nodes.md
LINKS:    SCHEMA/SCHEMA_Links.md
TENSIONS: SCHEMA/SCHEMA_Tensions.md
MOMENTS:  ../SCHEMA_Moments/SCHEMA_Moments_Overview.md
VALIDATION: ../VALIDATION_Graph.md
```

## Scope

- Node types: Character, Place, Thing, Narrative
- Link types: Core graph links (moment-specific links live in SCHEMA_Moments)
- Tensions: Pressure clusters that break into events
- Moments: See `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md`

## Core Principles (Concise)

- Nodes are things that exist; narratives are stories about nodes.
- Relationships are narratives; there is no separate relationship state.
- Physical state is ground truth (presence, possession, location).
- Narrative weight drives salience; contradictions accumulate into tension.
- Every node and link carries `energy`/`weight` metrics so the physics engine can compute drama without downstream bookkeeping.

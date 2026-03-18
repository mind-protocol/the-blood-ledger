# Patterns: Engine Moments

<!-- CHAIN: OBJECTIFS_Engine_Moments.md → PATTERNS_Engine_Moments.md → SYNC_Engine_Moments.md -->

## Purpose

Engine Moments defines the structure, semantics, and surface mechanics of moments in the narrative system.

## Design Philosophy

### Moment Definition
A moment is a discrete narrative event with:
- Temporal position
- Participants (characters, locations)
- Content (what happened)
- Connections (causal and associative links)

### Narrative Surface
Moments "surface" based on relevance to the current narrative context. The surfacing algorithm determines which moments become visible to the player.

### Immutability
Once created, moments are immutable. Changes create new moments with links to predecessors.

## What's In Scope

- Moment structure definition
- Surfacing criteria
- Relevance scoring
- Moment categorization

## What's Out of Scope

- Graph storage (physics layer)
- Moment generation (agents/world builder)
- Moment display (frontend)

## Moment Types

| Type | Description |
|------|-------------|
| Event | Something that happened |
| State | A condition or status |
| Observation | Player-visible information |
| Secret | Hidden until revealed |

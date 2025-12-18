# Blood Ledger Image Prompting Guide

Guide for generating consistent, accurate images using Ideogram 3.0.

---

## Core Principles

### Natural Language Only

Ideogram uses plain natural language. No special syntax:

- No weights (`::1`, `(important)`)
- No hex colors (`#E4BC73`) — use words: "golden-yellow", "deep red"
- No flags (`--ar`, `--style`)

**Position matters**: Words earlier in the prompt get more importance. Lead with what matters most.

### Literal Interpretation

Ideogram tries to render **every word literally**. If you write "a man by the fire", it will add a man. If you want no people, you must say so explicitly in the Image Summary.

### Prompt Length

- **Max**: ~150-160 words (~200 tokens)
- Longer prompts get truncated
- Make every word count

---

## Scene Banner Philosophy

**Banners show ONLY the location — not the objects or characters.**

The banner is the "stage" — pure environment. Camp objects, furniture, and characters are shown separately in the UI. This solves:
- AI adding unwanted furniture/props
- Inconsistency with game state (wrong number of tents, etc.)
- Narrative problems (how did 2 travelers carry all that?)

**Be specific about:**
- Vegetation type (oak, birch, pine, heather, bracken)
- Time of day (dawn, morning, midday, dusk, night)
- Weather (clear, overcast, rain, fog, frost)
- Season indicators (bare branches, frost, fallen leaves)

**For built environments (halls, castles, churches), think through:**
- Size and scale (small manor, great hall, modest church)
- Construction materials (rough-hewn stone, dressed limestone, timber frame, wattle and daub)
- Age and condition (newly built, weathered, crumbling, well-maintained)
- Level of wealth (austere, modest, prosperous, lordly, royal)
- Regional style (Norman military, Saxon vernacular, monastic)
- Specific architectural details (arrow slits, round arches, thatched vs slate roof)

---

## The 8-Part Prompt Structure

Each part adds structure and clarity. Include what's relevant — not all parts are needed for every image.

### 1. Image Summary

**Purpose**: The entire image in one sentence. How someone would describe it after a 2-second glance. Establishes visual form, main subject, and tone.

**For scene banners**: Pure location, no objects, no people.

> A cinematic wide shot of an empty forest clearing at night, 10th century England. Untouched natural landscape.

### 2. Main Subject Details

**Purpose**: The landscape features. Be specific about vegetation, terrain, natural elements.

> Bare ancient English oak trees framing the scene. Frost-covered grass meadow. Patches of dead bracken.

### 3. Terrain & Ground

**Purpose**: What's underfoot. Texture, condition, details.

> Uneven ground with exposed roots. Fallen leaves scattered. Thin ice on puddles.

### 4. Environmental Details

**Purpose**: Smaller natural elements that add authenticity. No man-made objects.

> Moss on tree trunks. A fallen log. Mist pooling in low areas. Bird's nest visible in branches.

### 5. Setting & Background

**Purpose**: The wider environment, horizon, sky. Time and weather specifics.

> Dense woodland visible beyond the clearing. Low hills in the distance. Clear night sky with stars. No buildings, no structures.

### 6. Lighting & Atmosphere

**Purpose**: How the light looks and how the image feels. Warm/cool, soft/dramatic, mood descriptors.

> Firelight casting long dancing shadows. Cold, tense atmosphere. Faint volumetric fog drifting through the clearing. Blue moonlight mixing with warm fire glow.

### 7. Framing & Composition

**Purpose**: How the subject is arranged in frame. Camera angle, shot type, placement.

> Wide establishing shot. Slightly low angle. Campfire centered with tents flanking.

### 8. Technical Enhancers

**Purpose**: Polish and professional finish. Lens type, depth of field, film style, artistic technique.

> 35mm film photography. Shallow depth of field on background. Cinematic color grading. Roger Deakins-style naturalistic lighting.

---

## Assembling the Parts

### Template

```
[1. Image Summary]. [2. Main Subject/Vegetation]. [3. Terrain & Ground]. [4. Environmental Details]. [5. Setting & Background]. [6. Lighting & Atmosphere]. [7. Framing & Composition]. [8. Technical Enhancers].
```

### Complete Example: Forest Clearing (Camp Location)

```
A cinematic wide shot of an empty forest clearing at night, 10th century England. Untouched natural landscape. Bare ancient English oak trees framing a frost-covered meadow. Patches of dead bracken at the edges. Uneven ground with exposed roots, fallen leaves scattered. Moss on tree trunks, a fallen log at the clearing's edge. Dense woodland beyond, low hills in distance, clear night sky with stars visible through winter branches. Blue moonlight on grass, cold still air, pristine and silent. Nothing man-made, no fire, no structures, no objects. Wide establishing shot, low angle. 35mm film, shallow depth of field, cinematic color grading.
```

### Complete Example: Forest Road

```
A cinematic wide shot of an empty forest road at dusk, 10th century England. Untouched muddy path. Bare birch and oak trees flanking both sides, pale bark catching last light. Rutted track with puddles reflecting grey sky, fallen leaves in the mud. Exposed tree roots crossing the path, dead ferns at the verge. Dense woodland pressing in on both sides, road disappearing into shadow ahead. Overcast sky, recent rain, trees still dripping, grey diffused light. No travelers, no carts, no structures. Wide shot, eye level, road leading into frame. 35mm film, muted desaturated colors, naturalistic lighting.
```

### Complete Example: Stone Hall Interior

```
A cinematic interior shot of an empty medieval stone hall, 10th century England. Untouched interior space. Massive oak roof beams darkened with age, rough-hewn stone walls. Packed earth floor with scattered rushes. A central stone hearth, cold and dark. Narrow window slits letting in pale daylight, dust motes floating. Faded tapestry on far wall, iron torch sconces empty. Solemn, weighty silence. No furniture, no people, no objects. Symmetrical composition, low angle looking toward the far wall. Cinematic lighting, volumetric light through windows, 35mm film grain.
```

---

## Lighting & Atmosphere Options

### Lighting Types
- "Golden hour light" / "blue hour"
- "Dramatic side lighting" / "rim lighting"
- "Volumetric light through fog/dust"
- "God rays through trees/windows"
- "Firelight casting long shadows"
- "Overcast diffused light"
- "Moonlight with blue tones"

### Atmosphere Words
- Cold, tense, threatening
- Solemn, weighty, formal
- Quiet, still, abandoned
- Moody, atmospheric, cinematic
- Desolate, lonely, isolated

### Film References (use sparingly)
- "Roger Deakins-style naturalistic lighting"
- "Cinematography like Kingdom of Heaven"
- "Terrence Malick golden hour"

---

## Technical Enhancers Options

### Camera/Lens
- "35mm film photography"
- "Wide angle lens"
- "Shallow depth of field"
- "Anamorphic lens"

### Shot Types
- "Wide establishing shot"
- "Medium shot"
- "Low angle" / "high angle"
- "Eye level"

### Quality
- "Cinematic color grading"
- "Film grain"
- "Photorealistic"
- "Highly detailed"

---

## Blood Ledger Specific Rules

### Scene Banners Must:

1. **Show ONLY the location** — no objects, no characters, no camp equipment
2. **Include "10th century England"** for historical grounding
3. **Be specific about vegetation** — oak, birch, bracken, heather, etc.
4. **Specify time of day** — dawn, morning, midday, dusk, night
5. **Specify weather** — clear, overcast, rain, fog, frost
6. **Specify framing** — wide establishing shot, medium shot, etc.
7. **End with explicit exclusions** — "no fire, no structures, no objects"

### Framing Options

| Shot Type | Use For |
|-----------|---------|
| Wide establishing shot | Open landscapes, clearings, roads |
| Medium wide shot | Forest interiors, enclosed spaces |
| Low angle | Adding grandeur, making space feel larger |
| Eye level | Neutral, documentary feel |
| Slight high angle | Overview, showing terrain layout |

### Deriving Prompts from Scene Data

Read the scene metadata, describe the LOCATION only:

**Scene data:**
```json
{
  "type": "CAMP",
  "location": "The North, three days from York",
  "timeOfDay": "NIGHT",
  "weather": "CLEAR"
}
```

**Becomes prompt:**
- Location type: Forest clearing (suitable for camping)
- Region: Northern England — oak woodland, heather moorland
- Time: Night — stars, moonlight, frost
- Weather: Clear — good visibility, cold

**Ignore hotspots for banner** — those are shown separately in UI.

---

## Checklist Before Generating

- [ ] Pure location only — no objects, no characters?
- [ ] Historical context "10th century England" included?
- [ ] Vegetation type specified (oak, birch, bracken)?
- [ ] Time of day specified (dawn, dusk, night)?
- [ ] Weather specified (clear, overcast, frost)?
- [ ] Framing specified (wide shot, low angle)?
- [ ] Explicit exclusions at end (no fire, no structures)?
- [ ] Lighting and atmosphere described?
- [ ] Technical enhancers for polish?
- [ ] Under 150 words total?

---

## API Configuration

```python
style_type: "REALISTIC"  # Options: AUTO, GENERAL, REALISTIC, DESIGN
aspect_ratio: "3x1"      # For scene banners
```

The tool adds nothing to your prompt. What you write is exactly what gets sent.

---

## References

- [Ideogram Prompting Guide](https://docs.ideogram.ai)
- Tool: `tools/image_generation/generate_image.py`
- Scene data: `frontend/data/scenes.json`

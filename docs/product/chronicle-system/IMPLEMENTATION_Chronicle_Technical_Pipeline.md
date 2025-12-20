# IMPLEMENTATION: Chronicle Technical Pipeline

Canonical implementation reference for the Chronicle system.
`IMPLEMENTATION_Chronicle_System.md` points here to avoid duplication.

## Code Architecture

The Chronicle system relies on a multi-stage technical pipeline to generate, compose, and render video content from player gameplay data.

## Generation Flow

```
┌─────────────────────────────────────────────────────────┐
│                    GAME SESSION                         │
│                                                         │
│  Events logged to chronicle_buffer:                    │
│  - Dialogue moments (with emotion tags)                │
│  - Ledger changes                                       │
│  - Graph state snapshots                               │
│  - Off-screen events (for "Shadow" section)            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 CHRONICLE GENERATOR                     │
│                                                         │
│  1. LLM: Analyze buffer, select key moments            │
│  2. LLM: Write script (narrator + character lines)     │
│  3. TTS: Generate voice tracks                         │
│  4. Composer: Assemble timeline                        │
│  5. FFmpeg: Render video                               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  CHRONICLE OUTPUT                       │
│                                                         │
│  - MP4 file (720p or 1080p)                            │
│  - Thumbnail (auto-generated from key moment)          │
│  - Metadata (title, description, tags)                 │
│  - Transcript (for accessibility + SEO)                │
└─────────────────────────────────────────────────────────┘
```

## LLM Prompt for Script Generation

The core of narrative generation is driven by a structured LLM prompt, ensuring cinematic and character-authentic output.

```python
CHRONICLE_SCRIPT_PROMPT = """
You are generating a Blood Chronicle — a cinematic recap of a player's session.

SESSION DATA:
{chronicle_buffer_json}

PLAYER NAME: {player_name}
SESSION NUMBER: {session_number}
DURATION: {session_duration}

Generate a script with this structure:

## COLD_OPEN
image: [describe the key image — a character portrait, a location, a moment]
line: [one dramatic line, spoken by narrator or character]

## THE_WEIGHT
entries:
  - ledger_text: [what's weighing on the player]
    visual: [how to show it — ink spreading, page darkening]
  - ledger_text: ...
narrator: [2-3 sentences summarizing the mounting pressure]

## THE_MOMENT  
image: [the pivotal scene]
character: [who speaks]
character_line: [what they say — their reaction to the choice]
narrator: [what happened and why it mattered]

## THE_SHADOW
image: [a location or character the player didn't see]
narrator: [what happened off-screen, ominous but not spoiling]
tease: [one cryptic line about future consequences]

## END_CARD
tagline: [a thematic summary of this session in <10 words]

RULES:
- Be cinematic, not clinical
- Character voices should feel authentic to their personality
- The Shadow should create curiosity, not frustration
- Every line should have WEIGHT
"""
```

## TTS Integration

Voice generation is handled by a Text-to-Speech (TTS) system, with specific voices mapped to different characters and the narrator.

```python
# Voice mapping
VOICES = {
    "narrator": "eleven_labs:narrator_male_deep",
    "aldric": "eleven_labs:british_young_male",
    "wulfric": "eleven_labs:gruff_older_male",
    "eadgyth": "eleven_labs:saxon_female",
    # ... character-specific voices
}

def generate_audio(script):
    tracks = []
    for section in script.sections:
        if section.narrator:
            tracks.append(tts(section.narrator, VOICES["narrator"]))
        if section.character_line:
            voice = VOICES.get(section.character, VOICES["narrator"])
            tracks.append(tts(section.character_line, voice))
    return tracks
```

## Video Composition

FFmpeg is used to compose the video from images, audio tracks, and effects, following a defined timeline.

```python
def compose_chronicle(script, audio_tracks, assets):
    timeline = []
    
    # Cold open
    timeline.append(Segment(
        image=assets.get_portrait(script.cold_open.image),
        audio=audio_tracks[0],
        effect="slow_zoom",
        duration=8
    ))
    
    # The Weight — Ledger pages
    for entry in script.the_weight.entries:
        timeline.append(Segment(
            image=assets.get_ledger_page(entry),
            effect="ink_spread",
            duration=5
        ))
    timeline.append(Segment(
        audio=audio_tracks[1],  # narrator
        image=assets.get_ledger_full(),
        effect="darken"
    ))
    
    # ... continue for each section
    
    # Render
    return ffmpeg_render(timeline, output="chronicle.mp4")
```

## Cost Breakdown

The estimated cost per Chronicle generation, primarily driven by LLM and TTS usage.

| Component | Cost per Chronicle (Session) | Cost per Chronicle (Life) |
|-----------|------------------------------|---------------------------|
| LLM (script generation) | $0.02 | $0.08 |
| TTS (audio) | $0.03-0.05 | $0.15-0.20 |
| Image processing | $0.00 | $0.00 |
| FFmpeg render | $0.00 | $0.00 |
| YouTube upload | $0.00 | $0.00 |
| **Total** | **$0.05-0.07** | **$0.25-0.30** |

## Maturity

STATUS: CANONICAL

---

## CHAIN

PATTERNS:        ./PATTERNS_Chronicle_Flywheel.md
BEHAVIORS:       ./BEHAVIORS_Chronicle_Types_And_Structure.md
THIS:            ./IMPLEMENTATION_Chronicle_Technical_Pipeline.md
SYNC:            ./SYNC_Chronicle_System.md

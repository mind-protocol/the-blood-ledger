# Discussion Tree Generator

You generate discussion trees for companion characters. These are pre-written conversation branches that make companions feel alive during travel and quiet moments.

## Input

You receive:
- Character ID and backstory
- Character beliefs and personality
- Current relationship with player
- Topics already explored (to avoid repetition)
- Current narrative context

## Output

Generate 5-10 discussion topics, each 3-4 layers deep.

Write to: `playthroughs/default/discussion_trees/{char_id}.json`

## Format

Pure JSON file:

```json
{
  "topics": [
    {
      "id": "{topic_id}",
      "name": "{Display Name}",
      "opener": {
        "narrator": "{Scene-setting narration}",
        "clickable": {
          "{word}": {
            "speaks": "{What player says}",
            "response": {
              "speaker": "{char_id}",
              "text": "{Character response}",
              "clickable": {
                "{word}": {
                  "speaks": "{Deeper question}",
                  "response": {
                    "speaker": "{char_id}",
                    "text": "{Deeper response}"
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

## Guidelines

1. **Character voice** — Each character speaks distinctly. Aldric is terse, practical. A scholar would be verbose.

2. **Clickable words** — Choose evocative words that invite curiosity. Not "the" or "and". Words like "brother", "oath", "burned", "waiting".

3. **Depth over breadth** — 3-4 layers deep is better than 10 shallow topics.

4. **Seeds for payoff** — Plant details that might matter later. A name mentioned. A place referenced. A debt hinted at.

5. **Emotional range** — Not all conversations are heavy. Some are light. Some are practical. Some reveal unexpected humor.

6. **Player agency** — Multiple clickable words per response. Player chooses what to pursue.

7. **Natural endings** — Some branches end naturally. Character trails off, changes subject, or the moment passes.

## Topic Categories

Mix these:
- **Past** — What happened before the player met them
- **Beliefs** — What they think about gods, duty, honor, revenge
- **Relationships** — Family, enemies, debts, oaths
- **Observations** — What they notice about the player, the world, the journey
- **Questions** — Things they want to ask the player
- **Practical** — Skills they have, things they know, advice they offer

## Example

For a character who lost his brother:

```json
{
  "topic": {
    "id": "aldric_brother",
    "name": "His Brother",
    "opener": {
      "narrator": "Aldric is quiet tonight. His hand keeps going to the ring on his finger — turning it, turning it.",
      "clickable": {
        "ring": {
          "speaks": "That ring. Whose was it?",
          "response": {
            "speaker": "char_aldric",
            "text": "My brother's. He gave it to me the morning he died.",
            "clickable": {
              "brother": {
                "speaks": "Tell me about him.",
                "response": {
                  "speaker": "char_aldric",
                  "text": "Edmund. He was the better one of us. Everyone said so.",
                  "clickable": {
                    "better": {
                      "speaks": "Better how?",
                      "response": {
                        "speaker": "char_aldric",
                        "text": "Kinder. Braver. He'd have found another way than running."
                      }
                    }
                  }
                }
              },
              "died": {
                "speaks": "How did he die?",
                "response": {
                  "beat": "Aldric's jaw tightens.",
                  "speaker": "char_aldric",
                  "text": "Arrow. Stamford Bridge. Right beside me and I couldn't do a thing."
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Invocation

Run as background task:

```bash
cd agents/discussion_generator && \
claude -p "Generate discussion trees for char_aldric" \
--allowedTools "Write,Read" \
--add-dir ../../
```

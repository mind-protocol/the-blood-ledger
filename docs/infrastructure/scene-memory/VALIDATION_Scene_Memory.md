# Scene Memory System — Validation

```
STATUS: DRAFT
CREATED: 2024-12-16
```

===============================================================================
## CHAIN
===============================================================================

```
PATTERNS:    ./PATTERNS_Scene_Memory.md
BEHAVIORS:   ./BEHAVIORS_Scene_Memory.md
ALGORITHM:   ./ALGORITHM_Scene_Memory.md
THIS:        VALIDATION_Scene_Memory.md (you are here)
SYNC:        ./SYNC_Scene_Memory.md
```

===============================================================================
## OVERVIEW
===============================================================================

This document specifies **how we verify** the system works correctly.

===============================================================================
## INVARIANTS
===============================================================================

Properties that must always hold true.

### INV-1: Names Are Unique After Expansion

```python
def test_names_unique():
    """No two expanded names can be identical."""
    scene = {"when": "Day 5, dusk", "where": "place_crossing"}
    narration = [
        {"name": "test", "text": "First"},
        {"name": "test", "text": "Second"},  # Same short name
        {"name": "test", "text": "Third"},   # Same short name again
    ]

    expanded, _ = expand_names(scene, narration, [])

    names = [elem["name"] for elem in expanded]
    assert len(names) == len(set(names)), "Duplicate names found"
    # Expected: crossing_d5_dusk_test, crossing_d5_dusk_test_2, crossing_d5_dusk_test_3
```

### INV-2: All Narratives Have FROM Links

```python
def test_narratives_have_from_links():
    """Every narrative must have at least one FROM link to a Moment."""
    narratives = graph.query("""
        MATCH (n:Narrative)
        OPTIONAL MATCH (n)-[:FROM]->(m:Moment)
        RETURN n.id, count(m) AS moment_count
    """)

    for narr in narratives:
        assert narr["moment_count"] > 0, f"{narr['n.id']} has no FROM links"
```

### INV-3: All Dialogue Moments Have SAID Links

```python
def test_dialogue_moments_have_said():
    """Every dialogue moment must have a SAID link from a character."""
    moments = graph.query("""
        MATCH (m:Moment {type: 'dialogue'})
        OPTIONAL MATCH (c:Character)-[:SAID]->(m)
        RETURN m.id, c.id AS speaker
    """)

    for moment in moments:
        assert moment["speaker"] is not None, f"Dialogue {moment['m.id']} has no speaker"
```

### INV-4: All Moments Have AT Links

```python
def test_moments_have_at_links():
    """Every moment must have an AT link to a place."""
    moments = graph.query("""
        MATCH (m:Moment)
        OPTIONAL MATCH (m)-[:AT]->(p:Place)
        RETURN m.id, p.id AS place
    """)

    for moment in moments:
        assert moment["place"] is not None, f"Moment {moment['m.id']} has no AT link"
```

### INV-5: Present Characters Get Beliefs

```python
def test_present_get_beliefs():
    """All characters present when narrative created have beliefs."""
    scenes_with_narratives = graph.query("""
        MATCH (s:Scene)-[:CREATES]->(n:Narrative)
        MATCH (s)-[:INVOLVES]->(c:Character)
        RETURN s.id, n.id AS narrative, collect(c.id) AS present
    """)

    for scene in scenes_with_narratives:
        for char_id in scene["present"]:
            belief = graph.query("""
                MATCH (c:Character {id: $char})-[b:BELIEVES]->(n:Narrative {id: $narr})
                RETURN b
            """, {"char": char_id, "narr": scene["narrative"]})

            assert len(belief) > 0, \
                f"{char_id} was present for {scene['narrative']} but has no belief"
```

### INV-6: Embedded Fields Meet Threshold

```python
def test_embeddings_exist():
    """All text fields > 20 chars have embeddings."""
    # Check moments
    moments = graph.query("""
        MATCH (m:Moment)
        WHERE m.text IS NOT NULL AND size(m.text) > 20
        RETURN m.id, m.text, m.embedding
    """)

    for moment in moments:
        assert moment["m.embedding"] is not None, \
            f"Moment {moment['m.id']} has text but no embedding"

    # Check narratives
    narratives = graph.query("""
        MATCH (n:Narrative)
        WHERE n.detail IS NOT NULL AND size(n.detail) > 20
        RETURN n.id, n.detail, n.embedding
    """)

    for narr in narratives:
        assert narr["n.embedding"] is not None, \
            f"Narrative {narr['n.id']} has detail but no embedding"
```

### INV-7: FROM Links Point To Valid Moments

```python
def test_from_links_valid():
    """All FROM links point to existing Moment nodes."""
    invalid = graph.query("""
        MATCH (n:Narrative)-[:FROM]->(target)
        WHERE NOT target:Moment
        RETURN n.id, target
    """)

    assert len(invalid) == 0, f"FROM links to non-Moment nodes: {invalid}"
```

===============================================================================
## UNIT TESTS
===============================================================================

### Name Expansion

```python
class TestNameExpansion:

    def test_basic_expansion(self):
        scene = {"when": "Day 5, dusk", "where": "place_crossing"}
        narration = [{"name": "test", "text": "Hello"}]

        expanded, _ = expand_names(scene, narration, [])

        assert expanded[0]["name"] == "crossing_d5_dusk_test"

    def test_clickable_expansion(self):
        scene = {"when": "Day 5, dusk", "where": "place_crossing"}
        narration = [{
            "name": "test",
            "text": "The blade",
            "clickable": {
                "blade": {"speaks": "Sharp", "name": "blade_hint"}
            }
        }]

        expanded, _ = expand_names(scene, narration, [])

        assert expanded[0]["clickable"]["blade"]["name"] == "crossing_d5_dusk_blade_hint"

    def test_collision_handling(self):
        scene = {"when": "Day 5, dusk", "where": "place_crossing"}
        narration = [
            {"name": "speak", "text": "First"},
            {"name": "speak", "text": "Second"},
        ]

        expanded, _ = expand_names(scene, narration, [])

        assert expanded[0]["name"] == "crossing_d5_dusk_speak"
        assert expanded[1]["name"] == "crossing_d5_dusk_speak_2"

    def test_player_input_expansion(self):
        scene = {"when": "Day 5, dusk", "where": "place_crossing"}
        player_inputs = [{"name": "rolf_asks", "type": "click"}]

        _, expanded = expand_names(scene, [], player_inputs)

        assert expanded[0]["name"] == "crossing_d5_dusk_rolf_asks"

    def test_various_time_formats(self):
        test_cases = [
            ({"when": "Day 1, dawn", "where": "place_york"}, "york_d1_dawn"),
            ({"when": "Day 12, midnight", "where": "place_camp"}, "camp_d12_midnight"),
            ({"when": "Day 100, noon", "where": "place_moor"}, "moor_d100_noon"),
        ]

        for scene, expected_prefix in test_cases:
            narration = [{"name": "test", "text": "X"}]
            expanded, _ = expand_names(scene, narration, [])
            assert expanded[0]["name"].startswith(expected_prefix)
```

### Moment Creation

```python
class TestMomentCreation:

    def test_moment_created_for_narration(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player"]
            },
            "narration": [{"name": "test", "text": "Hello world."}],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        moment = graph.query("""
            MATCH (m:Moment {id: 'crossing_d5_dusk_test'})
            RETURN m.text, m.type, m.tick
        """)
        assert len(moment) == 1
        assert moment[0]["m.text"] == "Hello world."
        assert moment[0]["m.type"] == "narration"
        assert moment[0]["m.tick"] == 142

    def test_dialogue_moment_has_said_link(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player", "char_aldric"]
            },
            "narration": [{
                "name": "aldric_speaks",
                "speaker": "char_aldric",
                "text": "It's done."
            }],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        said = graph.query("""
            MATCH (c:Character {id: 'char_aldric'})-[:SAID]->(m:Moment)
            RETURN m.id
        """)
        assert len(said) == 1
        assert said[0]["m.id"] == "crossing_d5_dusk_aldric_speaks"

    def test_moment_has_at_link(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player"]
            },
            "narration": [{"name": "test", "text": "Hello"}],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        at = graph.query("""
            MATCH (m:Moment)-[:AT]->(p:Place)
            RETURN p.id
        """)
        assert at[0]["p.id"] == "place_crossing"

    def test_hint_moment_created(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player"]
            },
            "narration": [{
                "name": "desc",
                "text": "The blade lies broken.",
                "clickable": {
                    "blade": {
                        "speaks": "Father's sword.",
                        "name": "blade_hint"
                    }
                }
            }],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        hint = graph.query("""
            MATCH (m:Moment {id: 'crossing_d5_dusk_blade_hint'})
            RETURN m.type, m.text
        """)
        assert len(hint) == 1
        assert hint[0]["m.type"] == "hint"
```

### Scene Storage

```python
class TestSceneStorage:

    def test_scene_created(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player"]
            },
            "narration": [{"name": "test", "text": "Hello"}],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        scene = graph.query("MATCH (s:Scene) WHERE s.when = 'Day 5, dusk' RETURN s.tick")
        assert len(scene) == 1
        assert scene[0]["s.tick"] == 142

    def test_scene_contains_moments(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player"]
            },
            "narration": [
                {"name": "first", "text": "First line."},
                {"name": "second", "text": "Second line."}
            ],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        contains = graph.query("""
            MATCH (s:Scene)-[:CONTAINS]->(m:Moment)
            WHERE s.when = 'Day 5, dusk'
            RETURN m.id
        """)
        assert len(contains) == 2

    def test_scene_links_to_place(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player"]
            },
            "narration": [{"name": "test", "text": "Hello"}],
            "mutations": []
        }

        process_narrator_output(output, tick=142)

        links = graph.query("""
            MATCH (s:Scene)-[:AT]->(p:Place {id: 'place_crossing'})
            RETURN s
        """)
        assert len(links) == 1
```

### Belief Creation

```python
class TestBeliefCreation:

    def test_witnessed_belief_created(self):
        output = {
            "scene": {
                "when": "Day 5, dusk",
                "where": "place_crossing",
                "present": ["char_player", "char_aldric"]
            },
            "narration": [{"name": "test", "text": "Hello"}],
            "mutations": [{
                "type": "new_narrative",
                "id": "narr_test",
                "content": "Test narrative",
                "sources": ["test"]
            }]
        }

        process_narrator_output(output)

        # Both characters should have beliefs
        for char in ["char_player", "char_aldric"]:
            belief = graph.query("""
                MATCH (c:Character {id: $char})-[b:BELIEVES]->(n:Narrative {id: 'narr_test'})
                RETURN b.witnessed, b.source
            """, {"char": char})

            assert len(belief) == 1
            assert belief[0]["b.witnessed"] == 1.0
            assert belief[0]["b.source"] == "witnessed"

    def test_belief_includes_when_where(self):
        # ... setup ...
        process_narrator_output(output)

        belief = graph.query("""
            MATCH (c:Character {id: 'char_player'})-[b:BELIEVES]->(n:Narrative {id: 'narr_test'})
            RETURN b.when, b.where
        """)

        assert belief[0]["b.when"] == "Day 5, dusk"
        assert belief[0]["b.where"] == "place_crossing"
```

===============================================================================
## INTEGRATION TESTS
===============================================================================

### Full Chain Test

```python
def test_full_chain():
    """End-to-end test of the complete flow."""

    # 1. Narrator outputs scene
    output = {
        "scene": {
            "when": "Day 5, dusk",
            "where": "place_crossing",
            "present": ["char_player", "char_aldric"]
        },
        "narration": [
            {
                "name": "blade_broken",
                "text": "The blade lies in two pieces.",
                "clickable": {
                    "blade": {
                        "speaks": "Father's sword.",
                        "name": "blade_hint"
                    }
                }
            },
            {
                "name": "aldric_done",
                "speaker": "char_aldric",
                "text": "It's done."
            }
        ],
        "mutations": [{
            "type": "new_narrative",
            "id": "narr_sword_broken",
            "content": "The sword broke",
            "sources": ["blade_broken", "aldric_done"]
        }]
    }

    process_narrator_output(output)

    # 2. Verify narrative sources are expanded
    narr = graph.query("MATCH (n:Narrative {id: 'narr_sword_broken'}) RETURN n.sources")[0]
    assert "crossing_d5_dusk_blade_broken" in narr["n.sources"]
    assert "crossing_d5_dusk_aldric_done" in narr["n.sources"]

    # 3. Verify beliefs created
    beliefs = graph.query("""
        MATCH (c:Character)-[b:BELIEVES]->(n:Narrative {id: 'narr_sword_broken'})
        RETURN c.id, b.witnessed
    """)
    assert len(beliefs) == 2

    # 4. Verify scene stored with embedding
    scene = graph.query("MATCH (s:Scene) WHERE s.when = 'Day 5, dusk' RETURN s.embedding")[0]
    assert scene["s.embedding"] is not None

    # 5. Player clicks blade
    player_input = {
        "type": "click",
        "name": "rolf_asks_blade",
        "clicked": "blade",
        "from": "crossing_d5_dusk_blade_hint"
    }
    expanded_input = process_player_input(output["scene"], player_input)
    assert expanded_input["name"] == "crossing_d5_dusk_rolf_asks_blade"

    # 6. Verify traceability query works
    result = narratives_from_moment("crossing_d5_dusk_blade_broken")
    assert any(r["n.id"] == "narr_sword_broken" for r in result)
```

### Multi-Scene Test

```python
def test_multi_scene_sources():
    """Narrative can reference moments from multiple scenes."""

    # Scene 1: Morning
    output1 = {
        "scene": {"when": "Day 5, morning", "where": "place_camp", "present": ["char_player"]},
        "narration": [{"name": "aldric_warns", "text": "Be careful on the road."}],
        "mutations": []
    }
    process_narrator_output(output1)

    # Scene 2: Dusk - narrative references both scenes
    output2 = {
        "scene": {"when": "Day 5, dusk", "where": "place_crossing", "present": ["char_player"]},
        "narration": [{"name": "ambush", "text": "They came from the trees."}],
        "mutations": [{
            "type": "new_narrative",
            "id": "narr_ambush_predicted",
            "content": "Aldric's warning came true",
            "sources": ["camp_d5_morning_aldric_warns", "crossing_d5_dusk_ambush"]
        }]
    }
    process_narrator_output(output2)

    # Verify cross-scene sources
    narr = graph.query("MATCH (n:Narrative {id: 'narr_ambush_predicted'}) RETURN n.sources")[0]
    assert "camp_d5_morning_aldric_warns" in narr["n.sources"]
    assert "crossing_d5_dusk_ambush" in narr["n.sources"]
```

===============================================================================
## QUERY TESTS
===============================================================================

```python
class TestQueries:

    def test_narratives_from_moment(self):
        # Setup: create narrative with known source
        # ...
        result = narratives_from_moment("crossing_d5_dusk_blade_broken")
        assert len(result) > 0
        assert result[0]["n.id"] == "narr_sword_broken"

    def test_sources_of_narrative(self):
        # Setup: create narrative with known sources
        # ...
        sources = sources_of_narrative("narr_sword_broken")
        assert "crossing_d5_dusk_blade_broken" in sources

    def test_who_knows(self):
        # Setup: create scene with present characters
        # ...
        knowers = who_knows("narr_sword_broken")
        char_ids = [k["c.id"] for k in knowers]
        assert "char_player" in char_ids
        assert "char_aldric" in char_ids

    def test_semantic_search(self):
        # Setup: create scene about sword
        # ...
        results = search_scenes("broken blade sword")
        assert len(results) > 0
        assert "blade" in results[0]["node.narration_text"].lower()
```

===============================================================================
## PERFORMANCE TESTS
===============================================================================

```python
class TestPerformance:

    def test_name_expansion_speed(self):
        """Name expansion should be fast even with many elements."""
        scene = {"when": "Day 5, dusk", "where": "place_crossing"}
        narration = [{"name": f"elem_{i}", "text": f"Text {i}"} for i in range(100)]

        import time
        start = time.time()
        expand_names(scene, narration, [])
        elapsed = time.time() - start

        assert elapsed < 0.1, f"Name expansion took {elapsed}s"

    def test_query_speed(self):
        """Queries should return within reasonable time."""
        # Assume graph has been populated
        import time

        start = time.time()
        narratives_from_moment("crossing_d5_dusk_blade_broken")
        elapsed = time.time() - start

        assert elapsed < 0.5, f"Query took {elapsed}s"
```

===============================================================================
## MANUAL VERIFICATION
===============================================================================

### Checklist

- [ ] Generate a scene, verify names are expanded in logs
- [ ] Check graph browser: Scene node exists with correct links
- [ ] Check graph browser: Narrative has expanded sources
- [ ] Check graph browser: BELIEVES links exist for all present characters
- [ ] Run semantic search, verify relevant scenes returned
- [ ] Query "who knows X", verify correct characters listed

===============================================================================
## RED FLAGS
===============================================================================

Signs something is wrong:

| Symptom | Likely Cause |
|---------|--------------|
| Duplicate expanded names | Collision handling broken |
| Narrative with empty sources | Narrator not providing sources |
| Missing beliefs | `present` array incorrect or belief creation failed |
| Semantic search returns nothing | Embeddings not generated or index missing |
| Query returns wrong scene | Name expansion inconsistent |

===============================================================================
## SYNC STATUS
===============================================================================

```
LAST_VALIDATED: Not yet
VALIDATED_BY: -
AGAINST_COMMIT: -
```

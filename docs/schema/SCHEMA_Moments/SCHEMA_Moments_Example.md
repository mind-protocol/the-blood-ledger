# Moment Example (Concise)

```cypher
CREATE (camp:Place { id: "place_camp_riverside", name: "Riverside Camp", type: "camp" })
CREATE (aldric:Character { id: "char_aldric", name: "Aldric", type: "companion" })
CREATE (m:Moment { id: "camp_d1_dusk_dialogue_001", text: "We should talk.", type: "dialogue", status: "possible" })
CREATE (aldric)-[:SAID]->(m)
CREATE (m)-[:ATTACHED_TO {presence_required: true}]->(aldric)
CREATE (m)-[:AT]->(camp)
```

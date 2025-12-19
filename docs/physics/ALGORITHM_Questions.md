# Physics — Algorithm: Question Answering

```
CREATED: 2024-12-18
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
THIS:           ALGORITHM_Questions.md (you are here)
ALGORITHMS:     ./ALGORITHM_Physics.md, ./ALGORITHM_Handlers.md
SCHEMA:         ../schema/SCHEMA_Moments.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
TEST:           ./TEST_Physics.md
SYNC:           ./SYNC_Physics.md
IMPL:           ../../engine/handlers/ (question answering as handler subprocess)
```

---

## Core Principle

**When a handler queries the graph and gets sparse results, invent the missing information.**

Question Answering fills gaps in world knowledge. It creates backstory, relationships, and history that didn't exist until needed.

---

## When Questions Arise

Handler asks a question. Graph returns sparse/nothing.

```python
# In character handler
def generate_response(context: HandlerContext):
    # Handler needs to know about father
    father_info = query_graph("Who is my father?", context.character.id)

    if father_info.is_sparse():
        # Queue question for answering
        question_answerer.queue(
            asker=context.character.id,
            question="Who is my father?",
            context=context
        )
        # Handler continues with what it knows
        # Does NOT block waiting for answer
```

---

## Not Async in "Fire and Forget" Sense

The session runs until it completes. It produces nodes. Nodes enter graph with initial weight.

```
Handler runs
  → asks "Who is my father?"
  → Question Answerer session starts (parallel)
  → Handler continues with what it knows
  → Handler finishes, outputs potentials
  → Later: QA completes, injects nodes with energy
  → Those nodes propagate naturally via physics
```

Handler never waits for QA. QA is fire-and-complete, not fire-and-wait.

---

## Question Answerer Flow

```python
async def answer_question(asker_id: str, question: str, context: dict):
    """
    Answer a question by inventing consistent information.
    Session runs until complete, then injects results.
    """
    # 1. GATHER — Get relevant existing facts
    existing = gather_relevant_facts(asker_id, question)

    # 2. GENERATE — Invent answer via LLM
    answer = await generate_answer(question, existing, context)

    # 3. VALIDATE — Check consistency
    if not validate_consistency(answer, existing):
        answer = await regenerate_with_constraints(question, existing, answer.conflicts)

    # 4. INJECT — Create nodes in graph
    inject_answer(asker_id, question, answer)
```

---

## Step 1: Gather Existing Facts

Query graph for anything relevant to constrain the answer.

```python
def gather_relevant_facts(asker_id: str, question: str) -> ExistingFacts:
    """
    Find existing information that constrains the answer.
    """
    asker = get_character(asker_id)

    facts = ExistingFacts()

    # Character's existing family
    facts.family = query("""
        MATCH (c:Character {id: $id})-[:FAMILY*1..2]-(relative:Character)
        RETURN relative
    """, id=asker_id)

    # Character's origin place
    facts.origin = query("""
        MATCH (c:Character {id: $id})-[:FROM]->(p:Place)
        RETURN p
    """, id=asker_id)

    # Character's existing beliefs/narratives
    facts.beliefs = query("""
        MATCH (c:Character {id: $id})-[:BELIEVES]->(n:Narrative)
        RETURN n
    """, id=asker_id)

    # Historical events character witnessed
    facts.history = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken
        LIMIT 20
    """, id=asker_id)

    return facts
```

---

## Step 2: Generate Answer

Use LLM to invent consistent answer.

```python
async def generate_answer(question: str, existing: ExistingFacts, context: dict) -> Answer:
    """
    Generate answer using LLM.
    """
    prompt = f"""
    A character in Norman England (1067) is wondering: "{question}"

    Existing facts about this character:
    - Family: {format_family(existing.family)}
    - Origin: {existing.origin}
    - Beliefs: {format_beliefs(existing.beliefs)}
    - Recent history: {format_history(existing.history)}

    Invent an answer that:
    1. Does NOT contradict any existing facts
    2. Fits the historical setting (Norman Conquest era)
    3. Creates potential for drama
    4. Feels specific and real, not generic

    Return structured output:
    - New characters (if any): name, relationship, status (alive/dead), traits
    - New places (if any): name, type, relationship to character
    - New events (if any): what happened, when, who was involved
    - Potential moments: memories that could surface
    """

    response = await llm.complete(prompt)
    return parse_answer(response)
```

---

## Step 3: Validate Consistency

Check that invented information doesn't contradict existing graph.

```python
def validate_consistency(answer: Answer, existing: ExistingFacts) -> bool:
    """
    Ensure answer doesn't contradict existing facts.
    """
    # Check family conflicts
    for new_char in answer.new_characters:
        if new_char.relationship == 'father':
            existing_father = find_existing_father(existing.family)
            if existing_father and existing_father.id != new_char.id:
                return False  # Conflict: already has different father

    # Check place conflicts
    for new_place in answer.new_places:
        if new_place.relationship == 'birthplace':
            existing_origin = existing.origin
            if existing_origin and existing_origin.id != new_place.id:
                return False  # Conflict: already has different origin

    # Check temporal conflicts
    for new_event in answer.new_events:
        if conflicts_with_history(new_event, existing.history):
            return False

    return True
```

---

## Step 4: Inject Answer

Create nodes in graph with initial energy.

```python
def inject_answer(asker_id: str, question: str, answer: Answer):
    """
    Inject answer into graph. Physics takes over from here.
    """
    # Create new character nodes
    for new_char in answer.new_characters:
        char_id = create_character(
            name=new_char.name,
            status=new_char.status,
            traits=new_char.traits
        )

        # Create relationship link
        create_link('FAMILY', asker_id, char_id, {
            'relationship': new_char.relationship
        })

    # Create new place nodes
    for new_place in answer.new_places:
        place_id = create_place(
            name=new_place.name,
            type=new_place.type
        )

        # Create relationship link
        create_link('FROM', asker_id, place_id, {
            'relationship': new_place.relationship
        })

    # Create potential memory moments
    for memory in answer.potential_moments:
        moment_id = create_moment(
            text=memory.text,
            type='thought',
            weight=ANSWER_INITIAL_WEIGHT,  # e.g., 0.4
            status='possible'
        )

        create_link('ATTACHED_TO', moment_id, asker_id, {
            'presence_required': True,
            'persistent': True
        })

    # Create ANSWERED_BY link for traceability
    question_moment = create_moment(
        text=f"[Question: {question}]",
        type='meta',
        weight=0.0,  # Not for display
        status='answered'
    )

    for node_id in answer.all_created_node_ids():
        create_link('ANSWERED_BY', question_moment, node_id, {})
```

---

## No Special Mechanism for Integration

The answer doesn't "boost" anything specially. It creates nodes. Nodes have energy. Energy propagates. That's it.

```python
# After injection, physics handles integration:

# New father character exists
# Memory moments attached to asker exist
# These have initial weight (e.g., 0.4)

# Next tick:
# - Energy propagates through FAMILY links
# - Memory moments may get boosted if relevant
# - If weight crosses threshold, memory surfaces

# No special "integrate answer" logic
# Just physics
```

If the answer is relevant, its energy reaches relevant moments. If not, it decays like everything else.

---

## Constraints

Invented information must:

| Constraint | Why |
|------------|-----|
| Not contradict existing graph | Consistency |
| Fit established facts | Coherence |
| Fit historical setting | Immersion |
| Create potential drama | Gameplay value |
| Be specific, not generic | Memorability |

---

## Example: "Who is my father?"

```
Handler for Aldric asks: "Who is my father?"
Graph returns: nothing (sparse)

Question Answerer runs:

Existing facts:
- Aldric is Saxon
- Aldric is from York
- Aldric has a brother (Edmund)
- Aldric witnessed the Norman invasion

Generated answer:
- New character: Wulfstan (father, deceased)
  - Traits: blacksmith, stubborn, proud
  - Death: killed defending York against Normans
- New moment: "Father's hammer still hangs in the forge."
- New moment: "He said 'never bow' the day before they came."

Injected:
- Character node: char_wulfstan
- FAMILY link: Aldric -> Wulfstan (father)
- Moment: "Father's hammer..." (weight 0.4, possible)
- Moment: "He said 'never bow'..." (weight 0.4, possible)
- ANSWERED_BY links for traceability

Later:
- Conversation touches on fathers
- Energy propagates to Aldric's moments
- Memory crosses threshold
- Aldric says: "He said 'never bow' the day before they came."
```

---

## What Question Answerer Does NOT Do

- Block handlers (they continue without waiting)
- Force moments to surface (physics decides)
- Override existing facts (must be consistent)
- Generate dialogue directly (creates potentials)

---

## Invariants

1. **Non-blocking:** Handlers never wait for answers
2. **Consistency:** Answers cannot contradict existing graph
3. **Physics integration:** No special boost, just node injection
4. **Traceability:** ANSWERED_BY links track what was invented

---

*"The answer doesn't boost anything specially. It creates nodes. Nodes have energy. That's it."*

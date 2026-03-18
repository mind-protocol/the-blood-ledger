# CONCEPT: Tempo Controller — The Main Loop That Paces Reality

```
STATUS: DRAFT
CREATED: 2025-12-20
```

---

## WHAT IT IS

The Tempo Controller is the main runtime loop that advances world time,
triggers physics ticks, and invokes canon surfacing at a controlled cadence.
It is the pacing layer: it governs *when* the world advances, not *what* it says.

---

## WHY IT EXISTS

Without a dedicated pacing loop, the system would either:
- block on LLM output,
- over-surface moments on every user action, or
- mix content generation with surfacing logic.

Tempo separates **time progression** from **content generation**, keeping the
world responsive, deterministic, and debuggable.

---

## KEY PROPERTIES

- **Deterministic cadence:** ticks are driven by a speed mode, not user input.
- **Non-blocking:** the loop never waits on Narrator output.
- **Pacing authority:** decides when surfacing scans occur and how many moments
  can become canon per tick.

---

## RELATIONSHIPS TO OTHER CONCEPTS

| Concept | Relationship |
|---------|--------------|
| Physics Engine | Tempo triggers physics ticks on schedule. |
| Canon Holder | Tempo invokes canon scans to record surfaced moments. |
| Narrator | Narrator writes possible moments asynchronously. |
| Orchestrator | Orchestrator coordinates actions but is not the clock. |
| SSE Streams | Canon Holder broadcasts surfaced moments to the frontend. |

---

## THE CORE INSIGHT

**Tempo is not content.** It is the timing and surfacing boundary that keeps
generation and observation decoupled.

---

## COMMON MISUNDERSTANDINGS

- **Not:** the Narrator loop.  
- **Not:** the Orchestrator.  
- **Not:** a “wait for LLM output” scheduler.  
- **Actually:** a clock that advances physics and canonization at a stable pace.

---

## SEE ALSO

- `docs/infrastructure/tempo/PATTERNS_Tempo.md`
- `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md`
- `docs/infrastructure/tempo/IMPLEMENTATION_Tempo.md`
- `docs/infrastructure/canon/PATTERNS_Canon.md`

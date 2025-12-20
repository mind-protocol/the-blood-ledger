#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "data" / "graph_scope_classification.yaml"

MODULES_PATH = REPO_ROOT / "modules.yaml"
modules_manifest = None
if MODULES_PATH.exists():
    with MODULES_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if isinstance(data, dict):
        modules_manifest = data.get("modules")


GRAPH_SCHEMA_PHYSICS_DOCS = [
    "docs/physics/ALGORITHM_Physics.md",
    "docs/physics/API_Physics.md",
    "docs/physics/BEHAVIORS_Physics.md",
    "docs/physics/HEALTH_Physics.md",
    "docs/physics/IMPLEMENTATION_Physics.md",
    "docs/physics/PATTERNS_Physics.md",
    "docs/physics/SYNC_Physics.md",
    "docs/physics/SYNC_Physics_archive_2025-12.md",
    "docs/physics/VALIDATION_Physics.md",
    "docs/physics/graph/BEHAVIORS_Graph.md",
    "docs/physics/graph/PATTERNS_Graph.md",
    "docs/physics/graph/VALIDATION_Living_Graph.md",
    "docs/physics/graph/SYNC_Graph.md",
    "docs/physics/graph/SYNC_Graph_archive_2025-12.md",
    "docs/physics/graph/archive/ALGORITHM_Energy_Flow_archived_2025-12-20.md",
    "docs/schema/SCHEMA.md",
    "docs/schema/SCHEMA_Moments.md",
    "docs/schema/SCHEMA_Code.md",
    "docs/schema/VALIDATION_Graph.md",
    "docs/schema/SCHEMA/SCHEMA_Overview.md",
    "docs/schema/SCHEMA/SCHEMA_Nodes.md",
    "docs/schema/SCHEMA/SCHEMA_Links.md",
    "docs/schema/SCHEMA/SCHEMA_Tensions.md",
    "docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md",
    "docs/schema/SCHEMA_Moments/SCHEMA_Moments_Node.md",
    "docs/schema/SCHEMA_Moments/SCHEMA_Moments_Links.md",
    "docs/schema/SCHEMA_Moments/SCHEMA_Moments_Example.md",
    "docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md",
    "docs/schema/graph-health/SYNC_Graph_Health.md",
    "docs/schema/graph-health/SYNC_Graph_Health_archive_2025-12.md",
    "docs/schema/models/PATTERNS_Pydantic_Schema_Models.md",
    "docs/schema/models/SYNC_Schema_Models.md",
    "docs/schema/models/SYNC_Schema_Models_archive_2025-12.md",
    "docs/engine/models/ALGORITHM_Models.md",
    "docs/engine/models/BEHAVIORS_Models.md",
    "docs/engine/models/HEALTH_Models.md",
    "docs/engine/models/IMPLEMENTATION_Models.md",
    "docs/engine/models/PATTERNS_Models.md",
    "docs/engine/models/SYNC_Models.md",
    "docs/engine/models/VALIDATION_Models.md",
]

STIMULUS_INGESTION_DOCS = [
    "docs/infrastructure/api/ALGORITHM_Api.md",
    "docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md",
    "docs/infrastructure/api/BEHAVIORS_Api.md",
    "docs/infrastructure/api/HEALTH_Api.md",
    "docs/infrastructure/api/IMPLEMENTATION_Api.md",
    "docs/infrastructure/api/PATTERNS_Api.md",
    "docs/infrastructure/api/SYNC_Api.md",
    "docs/infrastructure/api/SYNC_Api_archive_2025-12.md",
    "docs/infrastructure/api/VALIDATION_Api.md",
    "docs/infrastructure/scene-memory/ALGORITHM_Scene_Memory.md",
    "docs/infrastructure/scene-memory/BEHAVIORS_Scene_Memory.md",
    "docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md",
    "docs/infrastructure/scene-memory/PATTERNS_Scene_Memory.md",
    "docs/infrastructure/scene-memory/SYNC_Scene_Memory.md",
    "docs/infrastructure/scene-memory/SYNC_Scene_Memory_archive_2025-12.md",
    "docs/infrastructure/scene-memory/TEST_Scene_Memory.md",
    "docs/infrastructure/scene-memory/VALIDATION_Scene_Memory.md",
    "docs/infrastructure/scene-memory/archive/SYNC_archive_2024-12.md",
]

PLACES_AGENT_DOCS = [
    "docs/agents/narrator/ALGORITHM_Scene_Generation.md",
    "docs/agents/narrator/BEHAVIORS_Narrator.md",
    "docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md",
    "docs/agents/narrator/HEALTH_Narrator.md",
    "docs/agents/narrator/IMPLEMENTATION_Narrator.md",
    "docs/agents/narrator/INPUT_REFERENCE.md",
    "docs/agents/narrator/PATTERNS_Narrator.md",
    "docs/agents/narrator/SYNC_Narrator.md",
    "docs/agents/narrator/SYNC_Narrator_archive_2025-12.md",
    "docs/agents/narrator/TEMPLATE_Player_Notes.md",
    "docs/agents/narrator/TEMPLATE_Story_Notes.md",
    "docs/agents/narrator/TOOL_REFERENCE.md",
    "docs/agents/narrator/VALIDATION_Narrator.md",
    "docs/agents/narrator/archive/SYNC_archive_2024-12.md",
    "docs/agents/world-runner/ALGORITHM_World_Runner.md",
    "docs/agents/world-runner/BEHAVIORS_World_Runner.md",
    "docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md",
    "docs/agents/world-runner/INPUT_REFERENCE.md",
    "docs/agents/world-runner/PATTERNS_World_Runner.md",
    "docs/agents/world-runner/SYNC_World_Runner.md",
    "docs/agents/world-runner/TEST_World_Runner_Coverage.md",
    "docs/agents/world-runner/TOOL_REFERENCE.md",
    "docs/agents/world-runner/VALIDATION_World_Runner_Invariants.md",
    "docs/agents/world-runner/archive/SYNC_archive_2024-12.md",
]

PROTOCOL_DOCS = [
    "AGENTS.md",
    "CLAUDE.md",
    ".ngram/PROTOCOL.md",
    ".ngram/PRINCIPLES.md",
    ".ngram/CLAUDE.md",
    ".ngram/GEMINI.md",
    ".ngram/doctor-ignore.yaml",
    ".ngram/agents/manager/AGENTS.md",
    ".ngram/agents/manager/CLAUDE.md",
    ".ngram/state/SYNC_Project_State.md",
    ".ngram/views/GLOBAL_LEARNINGS.md",
    ".ngram/views/LEARNINGS_TEMPLATE.md",
    ".ngram/views/VIEW_Analyze_Structural_Analysis.md",
    ".ngram/views/VIEW_Analyze_Structural_Analysis_LEARNINGS.md",
    ".ngram/views/VIEW_Debug_Investigate_And_Fix_Issues.md",
    ".ngram/views/VIEW_Debug_Investigate_And_Fix_Issues_LEARNINGS.md",
    ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
    ".ngram/views/VIEW_Document_Create_Module_Documentation_LEARNINGS.md",
    ".ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md",
    ".ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems_LEARNINGS.md",
    ".ngram/views/VIEW_Extend_Add_Features_To_Existing.md",
    ".ngram/views/VIEW_Extend_Add_Features_To_Existing_LEARNINGS.md",
    ".ngram/views/VIEW_Health_Define_Health_Checks_And_Verify.md",
    ".ngram/views/VIEW_Health_Define_Health_Checks_And_Verify_LEARNINGS.md",
    ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
    ".ngram/views/VIEW_Implement_Write_Or_Modify_Code_LEARNINGS.md",
    ".ngram/views/VIEW_Ingest_Process_Raw_Data_Sources.md",
    ".ngram/views/VIEW_Ingest_Process_Raw_Data_Sources_LEARNINGS.md",
    ".ngram/views/VIEW_Onboard_Understand_Existing_Codebase.md",
    ".ngram/views/VIEW_Onboard_Understand_Existing_Codebase_LEARNINGS.md",
    ".ngram/views/VIEW_Refactor_Improve_Code_Structure.md",
    ".ngram/views/VIEW_Refactor_Improve_Code_Structure_LEARNINGS.md",
    ".ngram/views/VIEW_Review_Evaluate_Changes.md",
    ".ngram/views/VIEW_Review_Evaluate_Changes_LEARNINGS.md",
    ".ngram/views/VIEW_Scan_Populate_Ngramignore.md",
    ".ngram/views/VIEW_Scan_Populate_Ngramignore_LEARNINGS.md",
    ".ngram/views/VIEW_Specify_Design_Vision_And_Architecture.md",
    ".ngram/views/VIEW_Specify_Design_Vision_And_Architecture_LEARNINGS.md",
    ".ngram/templates/ALGORITHM_TEMPLATE.md",
    ".ngram/templates/BEHAVIORS_TEMPLATE.md",
    ".ngram/templates/CONCEPT_TEMPLATE.md",
    ".ngram/templates/HEALTH_TEMPLATE.md",
    ".ngram/templates/IMPLEMENTATION_TEMPLATE.md",
    ".ngram/templates/PATTERNS_TEMPLATE.md",
    ".ngram/templates/SYNC_TEMPLATE.md",
    ".ngram/templates/TOUCHES_TEMPLATE.md",
    ".ngram/templates/VALIDATION_TEMPLATE.md",
]


GRAPH_SCHEMA_PHYSICS_CODE = [
    "engine/physics/__init__.py",
    "engine/physics/tick.py",
    "engine/physics/constants.py",
    "engine/physics/graph/__init__.py",
    "engine/physics/graph/graph_queries.py",
    "engine/physics/graph/graph_queries_moments.py",
    "engine/physics/graph/graph_queries_search.py",
    "engine/physics/graph/graph_query_utils.py",
    "engine/physics/graph/graph_ops.py",
    "engine/physics/graph/graph_ops_apply.py",
    "engine/physics/graph/graph_ops_events.py",
    "engine/physics/graph/graph_ops_image.py",
    "engine/physics/graph/graph_ops_links.py",
    "engine/physics/graph/graph_ops_moments.py",
    "engine/physics/graph/graph_ops_types.py",
    "engine/models/__init__.py",
    "engine/models/base.py",
    "engine/models/nodes.py",
    "engine/models/links.py",
    "engine/graph/health/README.md",
    "engine/graph/health/check_health.py",
    "engine/graph/health/test_schema.py",
    "engine/graph/health/lint_terminology.py",
    "engine/graph/health/schema.yaml",
    "engine/graph/health/example_queries.cypher",
    "engine/graph/health/query_outputs.md",
    "engine/graph/health/query_results.md",
    "engine/tests/test_spec_consistency.py",
    "engine/tests/test_moment_graph.py",
]

STIMULUS_INGESTION_CODE = [
    "engine/infrastructure/memory/__init__.py",
    "engine/infrastructure/memory/moment_processor.py",
    "engine/infrastructure/api/__init__.py",
    "engine/infrastructure/api/app.py",
    "engine/infrastructure/api/moments.py",
    "engine/infrastructure/api/playthroughs.py",
    "engine/infrastructure/api/tempo.py",
    "engine/infrastructure/api/sse_broadcast.py",
    "engine/infrastructure/orchestration/orchestrator.py",
    "engine/infrastructure/embeddings/__init__.py",
    "engine/infrastructure/embeddings/service.py",
    "engine/init_db.py",
    "engine/physics/graph/graph_ops.py",
    "engine/physics/graph/graph_ops_moments.py",
    "engine/physics/graph/graph_queries_moments.py",
    "engine/models/nodes.py",
    "engine/tests/test_moment.py",
    "engine/tests/test_moment_graph.py",
    "engine/tests/test_moment_lifecycle.py",
    "engine/tests/test_e2e_moment_graph.py",
    "engine/tests/test_moments_api.py",
]

PLACES_AGENT_CODE = [
    "agents/narrator/CLAUDE.md",
    "agents/world_runner/CLAUDE.md",
    "engine/infrastructure/orchestration/__init__.py",
    "engine/infrastructure/orchestration/agent_cli.py",
    "engine/infrastructure/orchestration/narrator.py",
    "engine/infrastructure/orchestration/orchestrator.py",
    "engine/infrastructure/orchestration/world_runner.py",
    "engine/scripts/inject_to_narrator.py",
    "engine/tests/test_narrator_integration.py",
    "tools/stream_dialogue.py",
]

REFERENCED_MISSING = [
    {
        "path": "engine/models/tensions.py",
        "category": "graph_schema_physics_salience",
        "note": "Referenced in docs/engine/models/IMPLEMENTATION_Models.md",
    },
    {
        "path": "engine/db/graph_ops.py",
        "category": "graph_schema_physics_salience",
        "note": "Referenced in docs/schema/SCHEMA_Moments/SCHEMA_Moments_Overview.md",
    },
    {
        "path": "engine/api/app.py",
        "category": "graph_schema_physics_salience",
        "note": "Referenced in docs/physics/API_Physics.md",
    },
    {
        "path": "engine/infrastructure/memory/transcript.py",
        "category": "stimulus_ingestion_derivation_routing",
        "note": "Referenced as legacy in docs/infrastructure/scene-memory/ALGORITHM_Scene_Memory.md",
    },
]

LINKED_OUT_OF_SCOPE = {
    "cartridge_orchestration": [
        "docs/engine/moment-graph-engine/ALGORITHM_Click_Wait_Surfacing.md",
        "docs/engine/moment-graph-engine/BEHAVIORS_Traversal_And_Surfacing.md",
        "docs/engine/moment-graph-engine/IMPLEMENTATION_Moment_Graph_Runtime_Layout.md",
        "docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md",
        "docs/engine/moment-graph-engine/SYNC_Moment_Graph_Engine.md",
        "docs/engine/moment-graph-engine/TEST_Moment_Graph_Runtime_Coverage.md",
        "docs/engine/moment-graph-engine/VALIDATION_Moment_Traversal_Invariants.md",
        "docs/engine/moments/ALGORITHM_Moment_Graph_Operations.md",
        "docs/engine/moments/BEHAVIORS_Moment_Lifecycle.md",
        "docs/engine/moments/IMPLEMENTATION_Moment_Graph_Stub.md",
        "docs/engine/moments/PATTERNS_Moments.md",
        "docs/engine/moments/SYNC_Moments.md",
        "docs/engine/moments/TEST_Moment_Graph_Coverage.md",
        "docs/engine/moments/VALIDATION_Moment_Graph_Invariants.md",
        "engine/moment_graph/__init__.py",
        "engine/moment_graph/queries.py",
        "engine/moment_graph/surface.py",
        "engine/moment_graph/traversal.py",
        "engine/moments/__init__.py",
    ],
}


def _entries(paths: list[str], scope: str, category: str, note: str | None = None) -> list[dict]:
    entries = []
    for path in paths:
        entry = {
            "path": path,
            "scope": scope,
            "category": category,
            "confidence": 1.0,
        }
        if note:
            entry["note"] = note
        entries.append(entry)
    return entries


def main() -> None:
    entries: list[dict] = []

    entries += _entries(GRAPH_SCHEMA_PHYSICS_DOCS, "in_scope", "graph_schema_physics_salience")
    entries += _entries(GRAPH_SCHEMA_PHYSICS_CODE, "in_scope", "graph_schema_physics_salience")
    entries += _entries(STIMULUS_INGESTION_DOCS, "in_scope", "stimulus_ingestion_derivation_routing")
    entries += _entries(STIMULUS_INGESTION_CODE, "in_scope", "stimulus_ingestion_derivation_routing")
    entries += _entries(PLACES_AGENT_DOCS, "in_scope", "places_agent_orchestration")
    entries += _entries(PLACES_AGENT_CODE, "in_scope", "places_agent_orchestration")
    entries += _entries(PROTOCOL_DOCS, "in_scope", "protocols_templates_docs_navigation")

    for category, paths in LINKED_OUT_OF_SCOPE.items():
        entries += _entries(
            paths,
            "out_of_scope",
            category,
            note="Linked from in-scope docs; excluded per scope definition.",
        )

    for item in REFERENCED_MISSING:
        entries.append(
            {
                "path": item["path"],
                "scope": "in_scope",
                "category": item["category"],
                "confidence": 1.0,
                "note": item["note"],
            }
        )

    # Deduplicate while keeping first occurrence
    seen = set()
    deduped = []
    for entry in entries:
        if entry["path"] in seen:
            continue
        seen.add(entry["path"])
        deduped.append(entry)

    missing = [e["path"] for e in deduped if not (REPO_ROOT / e["path"]).exists()]

    output = {
        "meta": {
            "generated": "2025-12-20",
            "method": "manual module review; explicit hardcoded file lists",
            "module_manifest_available": bool(modules_manifest),
            "module_manifest": modules_manifest or None,
            "notes": [
                "Manual classification based on explicit doc module review.",
                "Linked out-of-scope files are included for traceability.",
            ],
            "missing_paths": missing,
        },
        "entries": deduped,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(output, handle, sort_keys=False, allow_unicode=False)

    print(f"Wrote {OUTPUT_PATH}")
    print(f"Entries: {len(deduped)}")
    print(f"Missing paths: {len(missing)}")


if __name__ == "__main__":
    main()

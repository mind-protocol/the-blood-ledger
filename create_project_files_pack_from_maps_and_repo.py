#!/usr/bin/env python3
"""Create a 10-file 'Project Files Pack' for fresh GPT sessions.

This script groups canon + workflow + maps/modules + verification + dev runbook + core architecture
into exactly 10 markdown files.

Usage:
  python3 create_project_files_pack_from_maps_and_repo.py --repo /path/to/repo
  python3 create_project_files_pack_from_maps_and_repo.py --repo . --out .project_files_pack
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob
import re
from pathlib import Path
from typing import List, Tuple, Optional


def _now_iso() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def safe_glob(repo: Path, pattern: str) -> List[Path]:
    matches = [Path(p) for p in glob.glob(str(repo / pattern), recursive=True)]
    return sorted([p for p in matches if p.exists() and p.is_file()])


def detect_repo_kind(repo: Path) -> str:
    if (repo / "ngram").exists() and (repo / "docs").exists():
        return "ngram"
    if (repo / "engine").exists() and (repo / "frontend").exists():
        return "blood-ledger"
    return "unknown"


def parse_map_tree_paths(map_text: str) -> List[str]:
    """Extract file paths from a tree-style map.md (best-effort)."""
    paths: List[str] = []
    for line in map_text.splitlines():
        m = re.search(r"[├└]──\s+([^\s].*?)\s*(\(|$)", line)
        if not m:
            continue
        candidate = m.group(1).strip().replace("→", "").strip()
        if candidate.endswith("/"):
            continue
        candidate = candidate.lstrip("./")
        paths.append(candidate)
    seen = set()
    out: List[str] = []
    for p in paths:
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


def append_source(out_parts: List[str], repo: Path, src: Path, *, max_chars: int) -> None:
    try:
        rel = src.relative_to(repo)
    except Exception:
        rel = src
    out_parts.append(f"\n\n---\n\n## SOURCE: {rel}\n")
    try:
        txt = read_text(src)
        if len(txt) > max_chars:
            txt = txt[:max_chars] + "\n\n…(truncated by pack builder)…\n"
        out_parts.append(txt)
    except Exception as e:
        out_parts.append(f"\n[ERROR reading {rel}: {e}]\n")


def include_globs(out_parts: List[str], repo: Path, patterns: List[str], *, max_files: int, max_chars_per_file: int) -> List[Path]:
    included: List[Path] = []
    for pat in patterns:
        for p in safe_glob(repo, pat):
            if p in included:
                continue
            included.append(p)
            append_source(out_parts, repo, p, max_chars=max_chars_per_file)
            if len(included) >= max_files:
                return included
    return included


PACK_FILES: List[Tuple[str, str]] = [
    ("01_CANON_Identity_Protocol_Principles_And_NonNegotiables.md", "Identity + protocol + principles + non-negotiables (agents-first canon)"),
    ("02_VIEWS_Core_Workflow_Execution_Skills_And_Escalation.md", "Core VIEWS / workflow skills and escalation/proposition rules"),
    ("03_Maps_Modules_And_Project_Topology_Routing.md", "Repo maps, modules.yaml, and topology routing"),
    ("04_Doctor_And_Health_Runtime_Verification_System.md", "Doctor + health + verification surfaces"),
    ("05_Dev_Runbook_WSL_Windows_Backend_Frontend_Persistence.md", "Runbook: WSL/Windows + starting BE/FE reliably (detached + checks)"),
    ("06_Architecture_And_System_Overview_Core_Decisions.md", "High-level architecture + core decisions (design/engine/protocol)"),
    ("07_Backend_API_And_Orchestration_EntryPoints_And_Contracts.md", "Backend API + orchestration entry points and contracts"),
    ("08_Frontend_UI_Dataflow_And_Runtime_Config.md", "Frontend runtime, UI dataflow, and contracts"),
    ("09_Schema_Graph_Model_And_Invariants.md", "Schema / graph model / invariants anchoring the system"),
    ("10_Current_State_Syncs_Queue_And_Next_Actions.md", "SYNC state, current queue, and next actions (resume after rate-limits)"),
]


WSL_RUNBOOK = """## Canon WSL/Windows runbook (embedded)
- Always verify ports with: `ss -ltnp | rg ':8000|:3000|:5173'`
- Always curl with IPv4+timeout: `curl -4 -m 2 -I http://localhost:8000`
- Prefer detached execution:
  - `tmux` sessions, or `nohup` with pidfiles/logs
- Windows reachability:
  - From Windows PowerShell: `curl.exe -I http://localhost:3000`
  - If localhost mapping fails, use WSL eth0 IP.
- Backend binding should be `0.0.0.0`, not `127.0.0.1`.

If the project already has a canonical run script (e.g. run.sh), prefer that.
"""


def build_pack(repo: Path, out_dir: Path, *, max_chars_per_file: int = 120_000) -> None:
    kind = detect_repo_kind(repo)

    # Read map(s) if present (optional)
    map_paths: List[Path] = []
    for candidate in ["map.md", "docs/map.md", "docs/SYNC_Project_Repository_Map.md", "map_frontend.md"]:
        p = repo / candidate
        if p.exists():
            map_paths.append(p)

    parsed_map_paths: List[str] = []
    for mp in map_paths:
        try:
            parsed_map_paths.extend(parse_map_tree_paths(read_text(mp)))
        except Exception:
            pass

    def r(path: str) -> Optional[Path]:
        p = repo / path
        return p if p.exists() and p.is_file() else None

    canon_sources = [
        r("AGENTS.md"),
        r("PROTOCOL.md"),
        r("PRINCIPLES.md"),
        r(".ngram/PROTOCOL.md"),
        r(".ngram/PRINCIPLES.md"),
        r("CLAUDE.md"),
        r("Isomorphic_Architecture.md"),
        r("README.md"),
        r("templates/ngram/PROTOCOL.md"),
        r("templates/ngram/PRINCIPLES.md"),
        r("templates/CODEX_SYSTEM_PROMPT_ADDITION.md"),
    ]

    views_patterns = [
        "views/VIEW_*Onboard*Existing_Codebase*.md",
        "views/VIEW_*Implement*Write_Or_Modify_Code*.md",
        "views/VIEW_*Debug*Investigate_And_Fix_Issues*.md",
        "views/VIEW_*Health*Define_Health_Checks_And_Verify*.md",
        "views/VIEW_*Review*Evaluate_Changes*.md",
        "views/VIEW_*Escalation*.md",
        "views/VIEW_*Ingest*Raw_Data_Sources*.md",
        "templates/ngram/views/VIEW_Onboard_Understand_Existing_Codebase.md",
        "templates/ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
        "templates/ngram/views/VIEW_Debug_Investigate_And_Fix_Issues.md",
        "templates/ngram/views/VIEW_Health_Define_Health_Checks_And_Verify.md",
        "templates/ngram/views/VIEW_Review_Evaluate_Changes.md",
        "templates/ngram/views/VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md",
        "templates/ngram/views/VIEW_Ingest_Process_Raw_Data_Sources.md",
    ]

    maps_sources = [
        r("map.md"),
        r("docs/map.md"),
        r("docs/SYNC_Project_Repository_Map.md"),
        r("modules.yaml"),
        r(".ngram/state/SYNC_Project_State.md"),
        r("templates/ngram/state/SYNC_Project_State.md"),
    ]

    doctor_patterns = [
        "docs/protocol/HEALTH_Protocol_Verification.md",
        "docs/protocol/features/doctor/*.md",
        "docs/cli/HEALTH_*.md",
        "ngram/doctor.py",
        "ngram/doctor_checks*.py",
        "ngram/doctor_report.py",
        "ngram/validate.py",
        "scripts/check_*.py",
    ]

    dev_run_sources = [
        r("run.sh"),
        r("docker-compose.yml"),
        r("engine/Dockerfile"),
        r("engine/.env.example"),
        r("frontend/package.json"),
        r("engine/README.md"),
        r("engine/infrastructure/history/README.md"),
    ]

    arch_patterns = [
        "docs/architecture/**/PATTERNS_*.md",
        "docs/architecture/**/IMPLEMENTATION_*.md",
        "docs/architecture/**/VALIDATION_*.md",
        "docs/architecture/**/SYNC_*.md",
        "docs/protocol/PATTERNS_*.md",
        "docs/protocol/BEHAVIORS_*.md",
        "docs/protocol/VALIDATION_*.md",
        "docs/protocol/SYNC_*.md",
        "Isomorphic_Architecture.md",
    ]

    backend_patterns = [
        "docs/infrastructure/api/*.md",
        "engine/infrastructure/api/app.py",
        "engine/infrastructure/api/moments.py",
        "engine/infrastructure/api/playthroughs.py",
        "engine/infrastructure/api/sse_broadcast.py",
        "engine/infrastructure/orchestration/orchestrator.py",
        "engine/infrastructure/orchestration/agent_cli.py",
        "engine/run.py",
        "engine/init_db.py",
    ]

    frontend_patterns = [
        "docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture/IMPLEMENTATION_Runtime_And_Config.md",
        "docs/frontend/PATTERNS_Presentation_Layer.md",
        "docs/frontend/ALGORITHM_Frontend_Data_Flow.md",
        "docs/frontend/SYNC_Frontend.md",
        "frontend/lib/api.ts",
        "frontend/hooks/useGameState.ts",
        "frontend/hooks/useMoments.ts",
        "frontend/app/page.tsx",
        "frontend/components/GameClient.tsx",
    ]

    schema_patterns = [
        "docs/schema/SCHEMA.md",
        "docs/schema/SCHEMA_Moments.md",
        "docs/schema/SCHEMA/**.md",
        "docs/schema/models/*.md",
        "engine/models/*.py",
        "docs/physics/graph/VALIDATION_*.md",
        "docs/physics/graph/PATTERNS_*.md",
    ]

    sync_patterns = [
        ".ngram/state/SYNC_Project_State.md",
        "docs/protocol/SYNC_Protocol_Current_State.md",
        "docs/cli/SYNC_CLI_Development_State.md",
        "docs/tui/SYNC_TUI_Development_Current_State.md",
        "docs/infrastructure/api/SYNC_Api.md",
        "docs/frontend/SYNC_Frontend.md",
        "docs/engine/SYNC_Engine.md",
        "docs/physics/SYNC_Physics.md",
    ]

    out_dir.mkdir(parents=True, exist_ok=True)

    def header(title: str, subtitle: str) -> str:
        return f"# {title}\n\n@pack:generated_at: {_now_iso()}\n@pack:repo_kind: {kind}\n\n{subtitle}\n"

    # 01
    p01 = out_dir / PACK_FILES[0][0]
    parts: List[str] = [header(PACK_FILES[0][0].replace('.md',''), PACK_FILES[0][1])]
    parts.append("\n## Notes\nThis file front-loads canon so the model does not revert to standard-repo defaults.\n")
    for s in canon_sources:
        if s:
            append_source(parts, repo, s, max_chars=max_chars_per_file)
    write_text(p01, "".join(parts))

    # 02
    p02 = out_dir / PACK_FILES[1][0]
    parts = [header(PACK_FILES[1][0].replace('.md',''), PACK_FILES[1][1])]
    parts.append("\n## Notes\nThese VIEWS define the procedural workflow. Prefer project `views/` if present, otherwise use templates.\n")
    include_globs(parts, repo, views_patterns, max_files=25, max_chars_per_file=max_chars_per_file)
    write_text(p02, "".join(parts))

    # 03
    p03 = out_dir / PACK_FILES[2][0]
    parts = [header(PACK_FILES[2][0].replace('.md',''), PACK_FILES[2][1])]
    parts.append("\n## Parsed map paths (best-effort)\n")
    if parsed_map_paths:
        parts.append("\n".join([f"- {p}" for p in parsed_map_paths[:400]]))
        if len(parsed_map_paths) > 400:
            parts.append("\n…(more omitted)…\n")
    else:
        parts.append("- (no map.md parsed)\n")
    for s in maps_sources:
        if s:
            append_source(parts, repo, s, max_chars=max_chars_per_file)
    write_text(p03, "".join(parts))

    # 04
    p04 = out_dir / PACK_FILES[3][0]
    parts = [header(PACK_FILES[3][0].replace('.md',''), PACK_FILES[3][1])]
    parts.append("\n## Notes\nThis pack groups verification mechanics: doctor checks, health indicators, and enforcement scripts.\n")
    include_globs(parts, repo, doctor_patterns, max_files=40, max_chars_per_file=max_chars_per_file)
    write_text(p04, "".join(parts))

    # 05
    p05 = out_dir / PACK_FILES[4][0]
    parts = [header(PACK_FILES[4][0].replace('.md',''), PACK_FILES[4][1])]
    parts.append("\n" + WSL_RUNBOOK + "\n")
    for s in dev_run_sources:
        if s:
            append_source(parts, repo, s, max_chars=max_chars_per_file)
    write_text(p05, "".join(parts))

    # 06
    p06 = out_dir / PACK_FILES[5][0]
    parts = [header(PACK_FILES[5][0].replace('.md',''), PACK_FILES[5][1])]
    include_globs(parts, repo, arch_patterns, max_files=25, max_chars_per_file=max_chars_per_file)
    write_text(p06, "".join(parts))

    # 07
    p07 = out_dir / PACK_FILES[6][0]
    parts = [header(PACK_FILES[6][0].replace('.md',''), PACK_FILES[6][1])]
    include_globs(parts, repo, backend_patterns, max_files=25, max_chars_per_file=max_chars_per_file)
    write_text(p07, "".join(parts))

    # 08
    p08 = out_dir / PACK_FILES[7][0]
    parts = [header(PACK_FILES[7][0].replace('.md',''), PACK_FILES[7][1])]
    include_globs(parts, repo, frontend_patterns, max_files=25, max_chars_per_file=max_chars_per_file)
    write_text(p08, "".join(parts))

    # 09
    p09 = out_dir / PACK_FILES[8][0]
    parts = [header(PACK_FILES[8][0].replace('.md',''), PACK_FILES[8][1])]
    include_globs(parts, repo, schema_patterns, max_files=35, max_chars_per_file=max_chars_per_file)
    write_text(p09, "".join(parts))

    # 10
    p10 = out_dir / PACK_FILES[9][0]
    parts = [header(PACK_FILES[9][0].replace('.md',''), PACK_FILES[9][1])]
    parts.append("\n## Notes\nThis file supports resuming work after rate-limits. Prefer SYNC as authoritative queue.\n")
    include_globs(parts, repo, sync_patterns, max_files=20, max_chars_per_file=max_chars_per_file)
    write_text(p10, "".join(parts))

    # Ensure exactly 10 exist
    for name, subtitle in PACK_FILES:
        p = out_dir / name
        if not p.exists():
            write_text(p, header(name.replace('.md',''), subtitle) + "\n(No sources found)\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Path to the repo root")
    ap.add_argument("--out", default=".project_files_pack", help="Output folder (relative to repo if not absolute)")
    ap.add_argument("--max-chars-per-file", type=int, default=120000, help="Truncate each included source at this many chars")
    args = ap.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = (repo / out).resolve()

    build_pack(repo, out_dir=out, max_chars_per_file=args.max_chars_per_file)
    print(f"OK: wrote 10 project-files-pack docs to: {out}")


if __name__ == "__main__":
    main()

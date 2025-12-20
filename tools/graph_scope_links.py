#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION_PATH = REPO_ROOT / "data" / "graph_scope_classification.yaml"
OUTPUT_YAML = REPO_ROOT / "data" / "graph_scope_links.yaml"
OUTPUT_TXT = REPO_ROOT / "data" / "graph_scope_links.txt"

IMPORT_RE = re.compile(r"^\s*import\s+([a-zA-Z0-9_.,\s]+)")
FROM_RE = re.compile(r"^\s*from\s+([a-zA-Z0-9_\.]+)\s+import\s+([a-zA-Z0-9_.*,\\s]+)")
IMPL_RE = re.compile(r"IMPL:\s*([^\n]+)")
DOCS_RE = re.compile(r"DOCS:\s*([^\n]+)")


def load_classification() -> list[str]:
    data = yaml.safe_load(CLASSIFICATION_PATH.read_text())
    entries = data.get("entries", [])
    return [entry["path"] for entry in entries if "path" in entry]


def module_name_for_path(path: str) -> str:
    parts = Path(path).with_suffix("").parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def build_module_index(paths: list[str]) -> dict[str, str]:
    index = {}
    for path in paths:
        if not path.endswith(".py"):
            continue
        module = module_name_for_path(path)
        if module:
            index[module] = path
    return index


def normalize_doc_path(doc_path: str, raw_target: str) -> str | None:
    cleaned = raw_target.strip().strip("`")
    if not cleaned:
        return None
    if cleaned.startswith(("engine/", "docs/", "agents/", ".ngram/", "tools/", "tests/", "data/")):
        return cleaned
    if cleaned.startswith(("./", "../")):
        resolved = (Path(doc_path).parent / cleaned).resolve()
        try:
            return str(resolved.relative_to(REPO_ROOT))
        except ValueError:
            return None
    return None


def parse_doc_impl_links(doc_path: str) -> list[str]:
    content = Path(doc_path).read_text(encoding="utf-8", errors="ignore")
    matches = IMPL_RE.findall(content)
    targets = []
    for match in matches:
        for raw in match.split(","):
            normalized = normalize_doc_path(doc_path, raw)
            if normalized:
                targets.append(normalized)
    return targets


def parse_code_docs_links(code_path: str) -> list[str]:
    content = Path(code_path).read_text(encoding="utf-8", errors="ignore")
    matches = DOCS_RE.findall(content)
    targets = []
    for match in matches:
        for raw in match.split(","):
            normalized = normalize_doc_path(code_path, raw)
            if normalized:
                targets.append(normalized)
    return targets


def parse_imports(code_path: str, module_index: dict[str, str]) -> list[str]:
    content = Path(code_path).read_text(encoding="utf-8", errors="ignore")
    targets = []
    for line in content.splitlines():
        m = IMPORT_RE.match(line)
        if m:
            modules = [part.strip() for part in m.group(1).split(",")]
            for mod in modules:
                mod = mod.split(" as ")[0].strip()
                if mod in module_index:
                    targets.append(module_index[mod])
            continue
        m = FROM_RE.match(line)
        if m:
            base = m.group(1).strip()
            names = [part.strip() for part in m.group(2).split(",")]
            if base in module_index:
                targets.append(module_index[base])
            for name in names:
                name = name.split(" as ")[0].strip()
                if name == "*":
                    continue
                candidate = f"{base}.{name}"
                if candidate in module_index:
                    targets.append(module_index[candidate])
    return targets


def build_edges(paths: list[str]) -> list[dict]:
    existing = [p for p in paths if (REPO_ROOT / p).exists()]
    curated = set(existing)
    module_index = build_module_index(existing)
    edges = []
    seen = set()

    def add_edge(src: str, dst: str, edge_type: str) -> None:
        if src not in curated or dst not in curated:
            return
        key = (src, dst, edge_type)
        if key in seen:
            return
        seen.add(key)
        edges.append({"from": src, "to": dst, "type": edge_type})

    for path in existing:
        if path.endswith(".md"):
            for target in parse_doc_impl_links(path):
                add_edge(path, target, "doc_to_code")
        elif path.endswith(".py"):
            for target in parse_code_docs_links(path):
                add_edge(path, target, "code_to_doc")
            for target in parse_imports(path, module_index):
                add_edge(path, target, "code_import")
    return edges


def build_adjacency(paths: list[str], edges: list[dict]) -> dict:
    adjacency = {path: {"outgoing": [], "incoming": []} for path in paths}
    for edge in edges:
        adjacency[edge["from"]]["outgoing"].append(edge)
        adjacency[edge["to"]]["incoming"].append(edge)
    return adjacency


def write_outputs(paths: list[str], edges: list[dict], adjacency: dict, missing: list[str]) -> None:
    output = {
        "meta": {
            "generated": "2025-12-20",
            "source": str(CLASSIFICATION_PATH),
            "node_count": len(paths),
            "edge_count": len(edges),
            "missing_paths": missing,
        },
        "nodes": paths,
        "edges": edges,
        "adjacency": adjacency,
    }
    OUTPUT_YAML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_YAML.write_text(yaml.safe_dump(output, sort_keys=False, allow_unicode=False), encoding="utf-8")

    lines = [
        "Graph Scope Links",
        f"Nodes: {len(paths)}",
        f"Edges: {len(edges)}",
        "",
    ]
    for edge in edges:
        lines.append(f"{edge['type']}: {edge['from']} -> {edge['to']}")
    OUTPUT_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not CLASSIFICATION_PATH.exists():
        raise SystemExit("Missing data/graph_scope_classification.yaml")

    paths = load_classification()
    existing = [p for p in paths if (REPO_ROOT / p).exists()]
    missing = [p for p in paths if p not in existing]
    edges = build_edges(paths)
    adjacency = build_adjacency(existing, edges)
    write_outputs(existing, edges, adjacency, missing)
    print(f"Wrote {OUTPUT_YAML}")
    print(f"Wrote {OUTPUT_TXT}")


if __name__ == "__main__":
    main()

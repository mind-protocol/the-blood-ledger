#!/usr/bin/env python3
"""
Graph Health Check

Validates all nodes and links in the graph against the schema definition.
Reports missing required attributes, invalid enum values, and other issues.

DOCS: docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md

Usage:
    python engine/graph/health/check_health.py
    python engine/graph/health/check_health.py --graph seed
    python engine/graph/health/check_health.py --verbose
    python engine/graph/health/check_health.py --fix  # Future: auto-fix issues
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import yaml

# Add engine to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "engine"))

from db.graph_ops import GraphOps

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load schema
SCHEMA_PATH = Path(__file__).parent / "schema.yaml"


@dataclass
class Issue:
    """A single validation issue."""
    node_type: str
    node_id: str
    issue_type: str  # missing_required, invalid_enum, missing_optional, type_error
    field: str
    message: str
    severity: str = "error"  # error, warning, info


@dataclass
class HealthReport:
    """Complete health report for the graph."""
    graph_name: str
    total_nodes: Dict[str, int] = field(default_factory=dict)
    total_links: Dict[str, int] = field(default_factory=dict)
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == "error"])

    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == "warning"])

    @property
    def is_healthy(self) -> bool:
        return self.error_count == 0

    def to_dict(self) -> Dict:
        return {
            "graph_name": self.graph_name,
            "healthy": self.is_healthy,
            "total_nodes": self.total_nodes,
            "total_links": self.total_links,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [
                {
                    "node_type": i.node_type,
                    "node_id": i.node_id,
                    "issue_type": i.issue_type,
                    "field": i.field,
                    "message": i.message,
                    "severity": i.severity,
                }
                for i in self.issues
            ]
        }

    def print_summary(self, verbose: bool = False):
        """Print a human-readable summary."""
        print(f"\n{'='*60}")
        print(f"Graph Health Report: {self.graph_name}")
        print(f"{'='*60}")

        print(f"\n--- Node Counts ---")
        for node_type, count in sorted(self.total_nodes.items()):
            print(f"  {node_type}: {count}")

        print(f"\n--- Link Counts ---")
        for link_type, count in sorted(self.total_links.items()):
            print(f"  {link_type}: {count}")

        print(f"\n--- Health Status ---")
        if self.is_healthy:
            print(f"  ✓ HEALTHY (no errors)")
        else:
            print(f"  ✗ UNHEALTHY ({self.error_count} errors, {self.warning_count} warnings)")

        if self.issues:
            # Group issues by type
            by_type: Dict[str, List[Issue]] = {}
            for issue in self.issues:
                key = f"{issue.node_type}:{issue.issue_type}"
                if key not in by_type:
                    by_type[key] = []
                by_type[key].append(issue)

            print(f"\n--- Issues by Category ---")
            for key, issues in sorted(by_type.items()):
                print(f"\n  [{key}] ({len(issues)} issues)")
                if verbose:
                    for issue in issues[:10]:  # Show first 10
                        severity_icon = "✗" if issue.severity == "error" else "⚠"
                        print(f"    {severity_icon} {issue.node_id}.{issue.field}: {issue.message}")
                    if len(issues) > 10:
                        print(f"    ... and {len(issues) - 10} more")
                else:
                    # Just show a sample
                    sample = issues[0]
                    print(f"    Example: {sample.node_id}.{sample.field}: {sample.message}")

        print(f"\n{'='*60}\n")


def load_schema() -> Dict:
    """Load the schema definition."""
    with open(SCHEMA_PATH, 'r') as f:
        return yaml.safe_load(f)


def validate_node(node: Dict, node_type: str, schema: Dict, report: HealthReport):
    """Validate a single node against the schema."""
    node_schema = schema['nodes'].get(node_type)
    if not node_schema:
        report.add_issue(Issue(
            node_type=node_type,
            node_id=node.get('id', 'unknown'),
            issue_type="unknown_type",
            field="",
            message=f"Unknown node type: {node_type}",
            severity="error"
        ))
        return

    node_id = node.get('id', 'unknown')

    # Check required fields
    for field in node_schema.get('required', []):
        if field not in node or node[field] is None or node[field] == '':
            report.add_issue(Issue(
                node_type=node_type,
                node_id=node_id,
                issue_type="missing_required",
                field=field,
                message=f"Missing required field: {field}",
                severity="error"
            ))

    # Check enum values
    enums = node_schema.get('enums', {})
    for field, valid_values in enums.items():
        if field in node and node[field] is not None:
            value = node[field]
            if value not in valid_values and value != '':
                report.add_issue(Issue(
                    node_type=node_type,
                    node_id=node_id,
                    issue_type="invalid_enum",
                    field=field,
                    message=f"Invalid value '{value}' for {field}. Valid: {valid_values}",
                    severity="warning"
                ))


def validate_link(link: Dict, link_type: str, schema: Dict, report: HealthReport):
    """Validate a single link against the schema."""
    link_schema = schema['links'].get(link_type)
    if not link_schema:
        # Unknown link type - might be okay
        return

    # For links, we mainly check enum values if present
    enums = link_schema.get('enums', {})
    link_id = f"{link.get('from', '?')}->{link.get('to', '?')}"

    for field, valid_values in enums.items():
        if field in link and link[field] is not None:
            value = link[field]
            if value not in valid_values:
                report.add_issue(Issue(
                    node_type=link_type,
                    node_id=link_id,
                    issue_type="invalid_enum",
                    field=field,
                    message=f"Invalid value '{value}' for {field}. Valid: {valid_values}",
                    severity="warning"
                ))


def check_graph_health(graph: GraphOps, schema: Dict) -> HealthReport:
    """Run health checks on the entire graph."""
    report = HealthReport(graph_name=graph.graph_name)

    # Check Characters
    logger.info("Checking Characters...")
    result = graph._query("MATCH (n:Character) RETURN n")
    characters = [dict(row[0].properties) for row in result] if result else []
    report.total_nodes['Character'] = len(characters)
    for node in characters:
        validate_node(node, 'Character', schema, report)

    # Check Places
    logger.info("Checking Places...")
    result = graph._query("MATCH (n:Place) RETURN n")
    places = [dict(row[0].properties) for row in result] if result else []
    report.total_nodes['Place'] = len(places)
    for node in places:
        validate_node(node, 'Place', schema, report)

    # Check Things
    logger.info("Checking Things...")
    result = graph._query("MATCH (n:Thing) RETURN n")
    things = [dict(row[0].properties) for row in result] if result else []
    report.total_nodes['Thing'] = len(things)
    for node in things:
        validate_node(node, 'Thing', schema, report)

    # Check Narratives
    logger.info("Checking Narratives...")
    result = graph._query("MATCH (n:Narrative) RETURN n")
    narratives = [dict(row[0].properties) for row in result] if result else []
    report.total_nodes['Narrative'] = len(narratives)
    for node in narratives:
        validate_node(node, 'Narrative', schema, report)

    # Check Tensions
    logger.info("Checking Tensions...")
    result = graph._query("MATCH (n:Tension) RETURN n")
    tensions = [dict(row[0].properties) for row in result] if result else []
    report.total_nodes['Tension'] = len(tensions)
    for node in tensions:
        validate_node(node, 'Tension', schema, report)

    # Check Links
    logger.info("Checking Links...")

    # BELIEVES links
    result = graph._query("MATCH ()-[r:BELIEVES]->() RETURN count(r)")
    report.total_links['BELIEVES'] = result[0][0] if result else 0

    # AT links
    result = graph._query("MATCH ()-[r:AT]->() RETURN count(r)")
    report.total_links['AT'] = result[0][0] if result else 0

    # CARRIES links
    result = graph._query("MATCH ()-[r:CARRIES]->() RETURN count(r)")
    report.total_links['CARRIES'] = result[0][0] if result else 0

    # LOCATED_AT links
    result = graph._query("MATCH ()-[r:LOCATED_AT]->() RETURN count(r)")
    report.total_links['LOCATED_AT'] = result[0][0] if result else 0

    # CONNECTS links
    result = graph._query("MATCH ()-[r:CONNECTS]->() RETURN count(r)")
    report.total_links['CONNECTS'] = result[0][0] if result else 0

    return report


def get_nodes_missing_field(graph: GraphOps, node_type: str, field: str) -> List[Dict]:
    """Get all nodes of a type missing a specific field."""
    cypher = f"""
    MATCH (n:{node_type})
    WHERE n.{field} IS NULL OR n.{field} = ''
    RETURN n.id as id, n.name as name
    """
    try:
        result = graph._query(cypher)
        return [{"id": row[0], "name": row[1]} for row in result] if result else []
    except Exception as e:
        logger.warning(f"Query failed for {node_type}.{field}: {e}")
        return []


def get_detailed_missing_report(graph: GraphOps, schema: Dict) -> Dict:
    """Get a detailed report of which nodes are missing which fields."""
    report = {}

    for node_type, node_schema in schema['nodes'].items():
        report[node_type] = {}

        # Check required fields
        for field in node_schema.get('required', []):
            missing = get_nodes_missing_field(graph, node_type, field)
            if missing:
                report[node_type][f"{field} (required)"] = missing

        # Check important optional fields
        important_optional = ['type', 'gender', 'alive'] if node_type == 'Character' else []
        if node_type == 'Place':
            important_optional = ['type']
        if node_type == 'Narrative':
            important_optional = ['type', 'truth']

        for field in important_optional:
            if field in node_schema.get('optional', []):
                missing = get_nodes_missing_field(graph, node_type, field)
                if missing:
                    report[node_type][f"{field} (optional)"] = missing

    # Filter out empty entries
    return {k: v for k, v in report.items() if v}


def main():
    parser = argparse.ArgumentParser(description='Check graph health')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--graph', default='seed', help='Graph name')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--detailed', action='store_true', help='Show detailed missing field report')
    args = parser.parse_args()

    # Connect to FalkorDB
    try:
        graph = GraphOps(graph_name=args.graph, host=args.host, port=args.port)
        logger.info(f"Connected to FalkorDB: {args.graph} at {args.host}:{args.port}")
    except Exception as e:
        logger.error(f"Cannot connect to FalkorDB: {e}")
        logger.info("Start FalkorDB with: docker run -p 6379:6379 falkordb/falkordb")
        return 1

    # Load schema
    schema = load_schema()

    # Run health check
    report = check_graph_health(graph, schema)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        report.print_summary(verbose=args.verbose)

    # Detailed missing field report
    if args.detailed:
        print("\n--- Detailed Missing Fields Report ---\n")
        detailed = get_detailed_missing_report(graph, schema)

        if not detailed:
            print("  No missing required or important fields found.")
        else:
            for node_type, fields in detailed.items():
                print(f"\n{node_type}:")
                for field, nodes in fields.items():
                    print(f"  {field}: {len(nodes)} nodes")
                    if args.verbose:
                        for node in nodes[:5]:
                            print(f"    - {node['id']}: {node['name']}")
                        if len(nodes) > 5:
                            print(f"    ... and {len(nodes) - 5} more")

    return 0 if report.is_healthy else 1


if __name__ == "__main__":
    exit(main())

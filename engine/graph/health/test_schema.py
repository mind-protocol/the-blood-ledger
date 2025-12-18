#!/usr/bin/env python3
"""
Blood Ledger Schema Test Suite

Verifies that the graph database matches the schema definition.
Tests node types, required fields, valid enum values, and link structures.

Usage:
    python test_schema.py [--graph NAME] [--verbose]

    pytest test_schema.py -v
"""

import json
import yaml
import pytest
from pathlib import Path
from typing import Dict, Any, List, Set, Optional
from dataclasses import dataclass, field

# Try to import FalkorDB
try:
    from falkordb import FalkorDB
    FALKORDB_AVAILABLE = True
except ImportError:
    FALKORDB_AVAILABLE = False

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SCHEMA_PATH = Path(__file__).parent / "schema.yaml"


@dataclass
class SchemaViolation:
    """A schema violation found in the graph."""
    node_type: str
    node_id: str
    field: str
    issue: str
    value: Any = None


@dataclass
class TestResult:
    """Result of a schema test."""
    test_name: str
    passed: bool
    violations: List[SchemaViolation] = field(default_factory=list)
    message: str = ""


class SchemaValidator:
    """Validates graph data against schema.yaml."""

    def __init__(self, graph_name: str = "blood_ledger"):
        self.graph_name = graph_name
        self.schema = self._load_schema()
        self.graph = None
        self.results: List[TestResult] = []

        if FALKORDB_AVAILABLE:
            try:
                db = FalkorDB(host='localhost', port=6379)
                self.graph = db.select_graph(graph_name)
            except Exception as e:
                print(f"Warning: Could not connect to FalkorDB: {e}")

    def _load_schema(self) -> Dict[str, Any]:
        """Load schema.yaml."""
        if SCHEMA_PATH.exists():
            with open(SCHEMA_PATH) as f:
                return yaml.safe_load(f)
        return {}

    def _query(self, cypher: str) -> List:
        """Run a Cypher query."""
        if not self.graph:
            return []
        try:
            result = self.graph.query(cypher)
            return result.result_set if result.result_set else []
        except Exception as e:
            print(f"Query error: {e}")
            return []

    # =========================================================================
    # NODE TESTS
    # =========================================================================

    def test_character_required_fields(self) -> TestResult:
        """Test that all Characters have required fields (id, name)."""
        violations = []

        # Check for missing id
        rows = self._query("MATCH (c:Character) WHERE c.id IS NULL RETURN c.name LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Character",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing",
                value=row[0] if row else None
            ))

        # Check for missing name
        rows = self._query("MATCH (c:Character) WHERE c.name IS NULL RETURN c.id LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Character",
                node_id=row[0] if row else "<unknown>",
                field="name",
                issue="Required field 'name' is missing"
            ))

        return TestResult(
            test_name="Character required fields",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} characters with missing required fields"
        )

    def test_character_type_enum(self) -> TestResult:
        """Test that Character.type uses valid enum values."""
        valid_types = {'player', 'companion', 'major', 'minor', 'background'}
        violations = []

        rows = self._query("""
            MATCH (c:Character)
            WHERE c.type IS NOT NULL
            RETURN c.id, c.name, c.type
        """)

        for row in rows:
            char_id, name, char_type = row[0], row[1], row[2]
            if char_type not in valid_types:
                violations.append(SchemaViolation(
                    node_type="Character",
                    node_id=char_id,
                    field="type",
                    issue=f"Invalid type '{char_type}'. Valid: {valid_types}",
                    value=char_type
                ))

        return TestResult(
            test_name="Character type enum",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} characters with invalid type"
        )

    def test_character_flaw_enum(self) -> TestResult:
        """Test that Character.flaw uses valid enum values."""
        valid_flaws = {'pride', 'fear', 'greed', 'wrath', 'doubt', None}
        violations = []

        rows = self._query("""
            MATCH (c:Character)
            WHERE c.flaw IS NOT NULL
            RETURN c.id, c.name, c.flaw
        """)

        for row in rows:
            char_id, name, flaw = row[0], row[1], row[2]
            if flaw not in valid_flaws:
                violations.append(SchemaViolation(
                    node_type="Character",
                    node_id=char_id,
                    field="flaw",
                    issue=f"Invalid flaw '{flaw}'. Valid: {valid_flaws}",
                    value=flaw
                ))

        return TestResult(
            test_name="Character flaw enum",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} characters with invalid flaw"
        )

    def test_place_required_fields(self) -> TestResult:
        """Test that all Places have required fields (id, name)."""
        violations = []

        rows = self._query("MATCH (p:Place) WHERE p.id IS NULL RETURN p.name LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Place",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing"
            ))

        rows = self._query("MATCH (p:Place) WHERE p.name IS NULL RETURN p.id LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Place",
                node_id=row[0] if row else "<unknown>",
                field="name",
                issue="Required field 'name' is missing"
            ))

        return TestResult(
            test_name="Place required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_place_type_enum(self) -> TestResult:
        """Test that Place.type uses valid enum values."""
        valid_types = {
            'region', 'city', 'town', 'hold', 'village', 'monastery', 'abbey',
            'crossing', 'road', 'wilderness', 'forest', 'ruin', 'camp',
            'holy_well', 'standing_stones', 'hill', 'crossroads'
        }
        violations = []

        rows = self._query("""
            MATCH (p:Place)
            WHERE p.type IS NOT NULL
            RETURN p.id, p.name, p.type
        """)

        for row in rows:
            place_id, name, place_type = row[0], row[1], row[2]
            if place_type not in valid_types:
                violations.append(SchemaViolation(
                    node_type="Place",
                    node_id=place_id,
                    field="type",
                    issue=f"Invalid type '{place_type}'",
                    value=place_type
                ))

        return TestResult(
            test_name="Place type enum",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_thing_required_fields(self) -> TestResult:
        """Test that all Things have required fields (id, name)."""
        violations = []

        rows = self._query("MATCH (t:Thing) WHERE t.id IS NULL RETURN t.name LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Thing",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing"
            ))

        rows = self._query("MATCH (t:Thing) WHERE t.name IS NULL RETURN t.id LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Thing",
                node_id=row[0] if row else "<unknown>",
                field="name",
                issue="Required field 'name' is missing"
            ))

        return TestResult(
            test_name="Thing required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_thing_significance_enum(self) -> TestResult:
        """Test that Thing.significance uses valid enum values."""
        valid_significance = {'mundane', 'personal', 'political', 'sacred', 'legendary'}
        violations = []

        rows = self._query("""
            MATCH (t:Thing)
            WHERE t.significance IS NOT NULL
            RETURN t.id, t.name, t.significance
        """)

        for row in rows:
            thing_id, name, sig = row[0], row[1], row[2]
            if sig not in valid_significance:
                violations.append(SchemaViolation(
                    node_type="Thing",
                    node_id=thing_id,
                    field="significance",
                    issue=f"Invalid significance '{sig}'",
                    value=sig
                ))

        return TestResult(
            test_name="Thing significance enum",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_narrative_required_fields(self) -> TestResult:
        """Test that all Narratives have required fields (id, name, content)."""
        violations = []

        for field in ['id', 'name', 'content']:
            rows = self._query(f"MATCH (n:Narrative) WHERE n.{field} IS NULL RETURN n.id, n.name LIMIT 10")
            for row in rows:
                violations.append(SchemaViolation(
                    node_type="Narrative",
                    node_id=row[0] if row and row[0] else "<unknown>",
                    field=field,
                    issue=f"Required field '{field}' is missing"
                ))

        return TestResult(
            test_name="Narrative required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_narrative_type_enum(self) -> TestResult:
        """Test that Narrative.type uses valid enum values."""
        valid_types = {
            'memory', 'account', 'rumor', 'rumour', 'reputation', 'identity',
            'bond', 'oath', 'debt', 'blood', 'enmity', 'love', 'service',
            'ownership', 'claim', 'control', 'origin', 'belief', 'prophecy',
            'lie', 'secret'
        }
        violations = []

        rows = self._query("""
            MATCH (n:Narrative)
            WHERE n.type IS NOT NULL
            RETURN n.id, n.name, n.type
        """)

        for row in rows:
            narr_id, name, narr_type = row[0], row[1], row[2]
            if narr_type not in valid_types:
                violations.append(SchemaViolation(
                    node_type="Narrative",
                    node_id=narr_id,
                    field="type",
                    issue=f"Invalid type '{narr_type}'",
                    value=narr_type
                ))

        return TestResult(
            test_name="Narrative type enum",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_tension_required_fields(self) -> TestResult:
        """Test that all Tensions have required field (id)."""
        violations = []

        rows = self._query("MATCH (t:Tension) WHERE t.id IS NULL RETURN t.description LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Tension",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing"
            ))

        return TestResult(
            test_name="Tension required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_tension_pressure_range(self) -> TestResult:
        """Test that Tension.pressure is within valid range [0, 1]."""
        violations = []

        rows = self._query("""
            MATCH (t:Tension)
            WHERE t.pressure IS NOT NULL AND (t.pressure < 0 OR t.pressure > 1)
            RETURN t.id, t.pressure
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Tension",
                node_id=row[0],
                field="pressure",
                issue=f"Pressure {row[1]} is outside valid range [0, 1]",
                value=row[1]
            ))

        return TestResult(
            test_name="Tension pressure range",
            passed=len(violations) == 0,
            violations=violations
        )

    # =========================================================================
    # LINK TESTS
    # =========================================================================

    def test_believes_link_structure(self) -> TestResult:
        """Test that BELIEVES links go from Character to Narrative."""
        violations = []

        # Check for BELIEVES from non-Character
        rows = self._query("""
            MATCH (a)-[b:BELIEVES]->(n)
            WHERE NOT a:Character
            RETURN labels(a)[0], a.id, n.id
            LIMIT 10
        """)
        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="BELIEVES",
                issue=f"BELIEVES link from {row[0]} (should be Character)"
            ))

        # Check for BELIEVES to non-Narrative
        rows = self._query("""
            MATCH (c:Character)-[b:BELIEVES]->(n)
            WHERE NOT n:Narrative
            RETURN c.id, labels(n)[0], n.id
            LIMIT 10
        """)
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Character",
                node_id=row[0],
                field="BELIEVES",
                issue=f"BELIEVES link to {row[1]} (should be Narrative)"
            ))

        return TestResult(
            test_name="BELIEVES link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_believes_value_ranges(self) -> TestResult:
        """Test that BELIEVES link values are within [0, 1]."""
        violations = []
        float_fields = ['heard', 'believes', 'doubts', 'denies', 'hides', 'spreads', 'originated']

        for field in float_fields:
            rows = self._query(f"""
                MATCH (c:Character)-[b:BELIEVES]->(n:Narrative)
                WHERE b.{field} IS NOT NULL AND (b.{field} < 0 OR b.{field} > 1)
                RETURN c.id, n.id, b.{field}
                LIMIT 10
            """)
            for row in rows:
                violations.append(SchemaViolation(
                    node_type="BELIEVES",
                    node_id=f"{row[0]}->{row[1]}",
                    field=field,
                    issue=f"Value {row[2]} is outside valid range [0, 1]",
                    value=row[2]
                ))

        return TestResult(
            test_name="BELIEVES value ranges",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_at_link_structure(self) -> TestResult:
        """Test that AT links go from Character to Place."""
        violations = []

        rows = self._query("""
            MATCH (a)-[at:AT]->(p)
            WHERE NOT a:Character OR NOT p:Place
            RETURN labels(a)[0], a.id, labels(p)[0], p.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="AT",
                issue=f"AT link from {row[0]} to {row[2]} (should be Character->Place)"
            ))

        return TestResult(
            test_name="AT link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_carries_link_structure(self) -> TestResult:
        """Test that CARRIES links go from Character to Thing."""
        violations = []

        rows = self._query("""
            MATCH (a)-[r:CARRIES]->(t)
            WHERE NOT a:Character OR NOT t:Thing
            RETURN labels(a)[0], a.id, labels(t)[0], t.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="CARRIES",
                issue=f"CARRIES link from {row[0]} to {row[2]} (should be Character->Thing)"
            ))

        return TestResult(
            test_name="CARRIES link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_located_at_link_structure(self) -> TestResult:
        """Test that LOCATED_AT links go from Thing to Place."""
        violations = []

        rows = self._query("""
            MATCH (a)-[r:LOCATED_AT]->(p)
            WHERE NOT a:Thing OR NOT p:Place
            RETURN labels(a)[0], a.id, labels(p)[0], p.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="LOCATED_AT",
                issue=f"LOCATED_AT link from {row[0]} to {row[2]} (should be Thing->Place)"
            ))

        return TestResult(
            test_name="LOCATED_AT link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_connects_link_structure(self) -> TestResult:
        """Test that CONNECTS links go from Place to Place."""
        violations = []

        rows = self._query("""
            MATCH (a)-[r:CONNECTS]->(b)
            WHERE NOT a:Place OR NOT b:Place
            RETURN labels(a)[0], a.id, labels(b)[0], b.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="CONNECTS",
                issue=f"CONNECTS link from {row[0]} to {row[2]} (should be Place->Place)"
            ))

        return TestResult(
            test_name="CONNECTS link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    # =========================================================================
    # DATA QUALITY TESTS
    # =========================================================================

    def test_orphan_characters(self) -> TestResult:
        """Test that characters have at least one relationship."""
        violations = []

        rows = self._query("""
            MATCH (c:Character)
            WHERE NOT (c)-[]-()
            RETURN c.id, c.name
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Character",
                node_id=row[0],
                field="<relationships>",
                issue="Character has no relationships (orphan)"
            ))

        return TestResult(
            test_name="Orphan characters",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} orphan characters"
        )

    def test_characters_have_location(self) -> TestResult:
        """Test that living characters have a location (AT relationship)."""
        violations = []

        rows = self._query("""
            MATCH (c:Character)
            WHERE (c.alive = true OR c.alive IS NULL)
            AND NOT (c)-[:AT]->(:Place)
            RETURN c.id, c.name, c.type
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Character",
                node_id=row[0],
                field="AT",
                issue=f"Living character '{row[1]}' has no location"
            ))

        return TestResult(
            test_name="Characters have location",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_things_have_location_or_carrier(self) -> TestResult:
        """Test that things are either at a place or carried by someone."""
        violations = []

        rows = self._query("""
            MATCH (t:Thing)
            WHERE NOT (t)-[:LOCATED_AT]->(:Place)
            AND NOT (:Character)-[:CARRIES]->(t)
            RETURN t.id, t.name
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Thing",
                node_id=row[0],
                field="location",
                issue=f"Thing '{row[1]}' has no location and no carrier"
            ))

        return TestResult(
            test_name="Things have location or carrier",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_narratives_have_believers(self) -> TestResult:
        """Test that narratives have at least one believer."""
        violations = []

        rows = self._query("""
            MATCH (n:Narrative)
            WHERE NOT (:Character)-[:BELIEVES]->(n)
            RETURN n.id, n.name, n.type
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Narrative",
                node_id=row[0],
                field="BELIEVES",
                issue=f"Narrative '{row[1]}' has no believers"
            ))

        return TestResult(
            test_name="Narratives have believers",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_player_exists(self) -> TestResult:
        """Test that exactly one player character exists."""
        violations = []

        rows = self._query("""
            MATCH (c:Character {type: 'player'})
            RETURN c.id, c.name
        """)

        if len(rows) == 0:
            violations.append(SchemaViolation(
                node_type="Character",
                node_id="<none>",
                field="type",
                issue="No player character found (type='player')"
            ))
        elif len(rows) > 1:
            for row in rows:
                violations.append(SchemaViolation(
                    node_type="Character",
                    node_id=row[0],
                    field="type",
                    issue=f"Multiple player characters found: {row[1]}"
                ))

        return TestResult(
            test_name="Player exists",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(rows)} player character(s)"
        )

    # =========================================================================
    # RUN ALL TESTS
    # =========================================================================

    def run_all_tests(self) -> List[TestResult]:
        """Run all schema tests."""
        if not self.graph:
            print("ERROR: No graph connection available")
            return []

        tests = [
            # Node tests
            self.test_character_required_fields,
            self.test_character_type_enum,
            self.test_character_flaw_enum,
            self.test_place_required_fields,
            self.test_place_type_enum,
            self.test_thing_required_fields,
            self.test_thing_significance_enum,
            self.test_narrative_required_fields,
            self.test_narrative_type_enum,
            self.test_tension_required_fields,
            self.test_tension_pressure_range,
            # Link tests
            self.test_believes_link_structure,
            self.test_believes_value_ranges,
            self.test_at_link_structure,
            self.test_carries_link_structure,
            self.test_located_at_link_structure,
            self.test_connects_link_structure,
            # Data quality tests
            self.test_orphan_characters,
            self.test_characters_have_location,
            self.test_things_have_location_or_carrier,
            self.test_narratives_have_believers,
            self.test_player_exists,
        ]

        self.results = []
        for test in tests:
            result = test()
            self.results.append(result)

        return self.results

    def print_report(self):
        """Print test results."""
        print("=" * 70)
        print("SCHEMA VALIDATION REPORT")
        print("=" * 70)
        print()

        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed

        for result in self.results:
            status = "✓" if result.passed else "✗"
            print(f"  {status} {result.test_name}")
            if not result.passed and result.violations:
                for v in result.violations[:3]:
                    print(f"      → {v.node_type}:{v.node_id} - {v.issue}")
                if len(result.violations) > 3:
                    print(f"      ... and {len(result.violations) - 3} more")

        print()
        print("=" * 70)
        print(f"PASSED: {passed}/{len(self.results)}")
        print(f"FAILED: {failed}/{len(self.results)}")
        print("=" * 70)

        return failed == 0


# =============================================================================
# PYTEST FIXTURES AND TESTS
# =============================================================================

@pytest.fixture
def validator():
    """Create a schema validator for tests."""
    return SchemaValidator()


def test_character_required_fields(validator):
    result = validator.test_character_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_character_type_enum(validator):
    result = validator.test_character_type_enum()
    assert result.passed, f"Violations: {result.violations}"


def test_place_required_fields(validator):
    result = validator.test_place_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_place_type_enum(validator):
    result = validator.test_place_type_enum()
    assert result.passed, f"Violations: {result.violations}"


def test_thing_required_fields(validator):
    result = validator.test_thing_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_narrative_required_fields(validator):
    result = validator.test_narrative_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_narrative_type_enum(validator):
    result = validator.test_narrative_type_enum()
    assert result.passed, f"Violations: {result.violations}"


def test_tension_pressure_range(validator):
    result = validator.test_tension_pressure_range()
    assert result.passed, f"Violations: {result.violations}"


def test_believes_link_structure(validator):
    result = validator.test_believes_link_structure()
    assert result.passed, f"Violations: {result.violations}"


def test_at_link_structure(validator):
    result = validator.test_at_link_structure()
    assert result.passed, f"Violations: {result.violations}"


def test_player_exists(validator):
    result = validator.test_player_exists()
    assert result.passed, f"Violations: {result.violations}"


# =============================================================================
# CLI MAIN
# =============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate graph schema")
    parser.add_argument("--graph", default="blood_ledger", help="Graph name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    validator = SchemaValidator(graph_name=args.graph)
    validator.run_all_tests()
    success = validator.print_report()

    import sys
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

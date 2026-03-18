#!/usr/bin/env python3
"""
Health Check Aggregator

Runs all health checkers and produces a combined report.
Integrates with `ngram doctor` for system-wide health monitoring.

Usage:
    python3 tools/health/run_all_checks.py           # Human-readable output
    python3 tools/health/run_all_checks.py --json    # JSON output
    python3 tools/health/run_all_checks.py --dry-run # Skip actual checks
"""

import argparse
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# All available health checkers in priority order
CHECKERS = [
    ('check_tempo', 'TempoHealthChecker', {'playthrough_id': 'health_check'}),
    ('check_opening', 'OpeningHealthChecker', {'playthrough_id': 'default'}),
    ('check_canon', 'CanonHealthChecker', {'playthrough_id': 'default'}),
    ('check_async', 'AsyncHealthChecker', {'playthrough_id': 'default'}),
    ('check_history', 'HistoryHealthChecker', {'playthrough_id': 'default'}),
    ('check_frontend', 'FrontendHealthChecker', {}),
    ('check_engine_tests', 'EngineTestsHealthChecker', {}),
    ('check_embeddings', 'EmbeddingsHealthChecker', {}),
    ('check_world_builder', 'WorldBuilderHealthChecker', {}),
    ('check_world_scraping', 'WorldScrapingHealthChecker', {}),
    ('check_map', 'MapHealthChecker', {}),
    ('check_cli_tools', 'CLIToolsHealthChecker', {}),
    ('check_image_generation', 'ImageGenerationHealthChecker', {}),
    ('check_ops_scripts', 'OpsScriptsHealthChecker', {}),
    ('check_storms', 'StormsHealthChecker', {'playthrough_id': 'default'}),
    ('check_storm_loader', 'StormLoaderHealthChecker', {}),
    ('check_billing', 'BillingHealthChecker', {}),
    ('check_ledger_lock', 'LedgerLockHealthChecker', {'playthrough_id': 'default'}),
    ('check_chronicle', 'ChronicleHealthChecker', {}),
    ('check_gtm', 'GTMHealthChecker', {}),
    ('check_business_model', 'BusinessModelHealthChecker', {}),
    ('check_vision_docs', 'VisionDocsHealthChecker', {}),
    ('check_world_scavenger', 'WorldScavengerHealthChecker', {}),
    ('check_ghost_dialogue', 'GhostDialogueHealthChecker', {}),
    ('check_shadow_feed', 'ShadowFeedHealthChecker', {}),
    ('check_voyager', 'VoyagerHealthChecker', {}),
    ('check_bleed_through', 'BleedThroughHealthChecker', {}),
    ('check_transposition', 'TranspositionHealthChecker', {}),
    ('check_schema_archive', 'SchemaArchiveHealthChecker', {}),
]


def run_checker(module_name: str, class_name: str, kwargs: Dict, dry_run: bool) -> Dict[str, Any]:
    """Run a single health checker and return its report."""
    try:
        module = importlib.import_module(f'tools.health.{module_name}')
        checker_class = getattr(module, class_name)

        # Add dry_run to kwargs
        init_kwargs = {**kwargs, 'dry_run': dry_run}

        checker = checker_class(**init_kwargs)
        checker.check_all()
        return checker.get_report()
    except Exception as e:
        return {
            'checker': module_name,
            'status': 'ERROR',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'error': str(e),
            'checks': {}
        }


def aggregate_status(reports: List[Dict[str, Any]]) -> str:
    """Compute aggregate status from all reports."""
    statuses = [r.get('status', 'UNKNOWN') for r in reports]

    if 'ERROR' in statuses:
        return 'ERROR'
    elif 'WARN' in statuses:
        return 'WARN'
    elif all(s == 'OK' for s in statuses):
        return 'OK'
    else:
        return 'WARN'


def run_all(dry_run: bool = False, json_output: bool = False) -> int:
    """Run all health checkers and output results."""
    reports = []

    for module_name, class_name, kwargs in CHECKERS:
        report = run_checker(module_name, class_name, kwargs, dry_run)
        reports.append(report)

    aggregate = {
        'aggregator': 'run_all_checks',
        'status': aggregate_status(reports),
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'total_checkers': len(CHECKERS),
        'summary': {
            'OK': sum(1 for r in reports if r.get('status') == 'OK'),
            'WARN': sum(1 for r in reports if r.get('status') == 'WARN'),
            'ERROR': sum(1 for r in reports if r.get('status') == 'ERROR'),
            'SKIP': sum(1 for r in reports if r.get('status') == 'SKIP'),
        },
        'reports': reports
    }

    if json_output:
        print(json.dumps(aggregate, indent=2))
    else:
        print(f"\n{'='*70}")
        print(f"BLOOD LEDGER HEALTH REPORT: {aggregate['status']}")
        print(f"{'='*70}")
        print(f"Timestamp: {aggregate['timestamp']}")
        print(f"Total Checkers: {aggregate['total_checkers']}")
        print(f"Summary: OK={aggregate['summary']['OK']}, WARN={aggregate['summary']['WARN']}, ERROR={aggregate['summary']['ERROR']}")
        print(f"{'='*70}\n")

        # Group by status
        for status in ['ERROR', 'WARN', 'OK']:
            status_reports = [r for r in reports if r.get('status') == status]
            if status_reports:
                icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗'}.get(status, '?')
                print(f"{icon} {status} ({len(status_reports)}):")
                for r in status_reports:
                    checker_name = r.get('checker', 'unknown')
                    print(f"    - {checker_name}")
                print()

        print(f"{'='*70}\n")

    return 0 if aggregate['status'] in ('OK', 'WARN') else 1


def main():
    parser = argparse.ArgumentParser(description='Run all health checkers')
    parser.add_argument('--dry-run', action='store_true', help='Skip actual checks')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()
    return run_all(dry_run=args.dry_run, json_output=args.json)


if __name__ == '__main__':
    sys.exit(main())

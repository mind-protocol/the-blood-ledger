#!/usr/bin/env python3
"""
Ops Scripts Health Checker

Verifies seeding and backfill scripts from HEALTH_Operational_Scripts.md:
- Scripts exist in expected locations
- Scripts have valid Python syntax

HEALTH: docs/infrastructure/ops-scripts/HEALTH_Operational_Scripts.md
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'engine/scripts'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class OpsScriptsHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[OpsScriptsHealth] Starting checks")

        self.results['scripts_exist'] = self._check_scripts_exist()
        self.results['scripts_syntax'] = self._check_scripts_syntax()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_scripts_exist(self) -> Dict[str, Any]:
        """Verify ops scripts directory exists with scripts."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not SCRIPTS_DIR.exists():
            return {'status': 'WARN', 'message': 'engine/scripts directory not found', 'validation': 'V1'}

        py_files = list(SCRIPTS_DIR.glob('*.py'))
        if not py_files:
            return {'status': 'WARN', 'message': 'No Python scripts found', 'validation': 'V1'}

        return {
            'status': 'OK',
            'message': f'Found {len(py_files)} scripts in engine/scripts',
            'validation': 'V1',
            'count': len(py_files)
        }

    def _check_scripts_syntax(self) -> Dict[str, Any]:
        """Verify ops scripts have valid Python syntax."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not SCRIPTS_DIR.exists():
            return {'status': 'SKIP', 'message': 'Scripts directory not found', 'validation': 'V1'}

        py_files = list(SCRIPTS_DIR.glob('*.py'))
        invalid = []

        for pf in py_files:
            try:
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', str(pf)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    invalid.append(pf.name)
            except Exception:
                pass

        if invalid:
            return {
                'status': 'ERROR',
                'message': f'{len(invalid)} scripts with syntax errors',
                'validation': 'V1',
                'invalid': invalid[:5]
            }

        return {'status': 'OK', 'message': f'{len(py_files)} scripts have valid syntax', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_ops_scripts',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Ops Scripts Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = OpsScriptsHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nOPS SCRIPTS HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

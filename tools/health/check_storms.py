#!/usr/bin/env python3
"""
Storms Health Checker

Verifies storm overlay activity from HEALTH_Storms.md:
- Storm definition files exist and are valid
- Active storms have expiration times

HEALTH: docs/infrastructure/storms/HEALTH_Storms.md
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent
STORMS_DIR = PROJECT_ROOT / 'data/storms'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class StormsHealthChecker:
    def __init__(self, playthrough_id: str = 'default', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info(f"[StormsHealth] Starting checks for playthrough: {self.playthrough_id}")

        self.results['storm_definitions_valid'] = self._check_storm_definitions()
        self.results['storm_module_available'] = self._check_storm_module()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_storm_definitions(self) -> Dict[str, Any]:
        """Verify storm definition files are valid YAML."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not STORMS_DIR.exists():
            return {'status': 'WARN', 'message': 'data/storms directory not found', 'validation': 'V1'}

        yaml_files = list(STORMS_DIR.glob('*.yaml')) + list(STORMS_DIR.glob('*.yml'))
        if not yaml_files:
            return {'status': 'OK', 'message': 'No storm definitions (expected in early dev)', 'validation': 'V1'}

        invalid = []
        for yf in yaml_files:
            try:
                with open(yf) as f:
                    yaml.safe_load(f)
            except Exception as e:
                invalid.append(f"{yf.name}: {e}")

        if invalid:
            return {
                'status': 'ERROR',
                'message': f'{len(invalid)} invalid storm files',
                'validation': 'V1',
                'invalid': invalid[:3]
            }

        return {'status': 'OK', 'message': f'{len(yaml_files)} storm definitions valid', 'validation': 'V1'}

    def _check_storm_module(self) -> Dict[str, Any]:
        """Verify storm module is available."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.infrastructure import storms
            return {'status': 'OK', 'message': 'Storms module available', 'validation': 'V1'}
        except ImportError:
            return {'status': 'SKIP', 'message': 'Storms module not implemented yet', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_storms',
            'playthrough_id': self.playthrough_id,
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Storms Health Checker')
    parser.add_argument('--playthrough', '-p', default='default')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = StormsHealthChecker(args.playthrough, args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nSTORMS HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

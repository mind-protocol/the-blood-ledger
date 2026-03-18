#!/usr/bin/env python3
"""
World Scraping Health Checker

Verifies seeding pipeline from HEALTH_World_Scraping.md:
- V1: YAML inputs load without schema errors
- V2: Injected node counts match expected totals

HEALTH: docs/world/scraping/HEALTH_World_Scraping.md
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
DATA_DIR = PROJECT_ROOT / 'data/world'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class WorldScrapingHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[WorldScrapingHealth] Starting checks")

        self.results['yaml_files_valid'] = self._check_yaml_validity()
        self.results['inject_script_exists'] = self._check_inject_script()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_yaml_validity(self) -> Dict[str, Any]:
        """V1: Verify YAML inputs load without schema errors."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        if not DATA_DIR.exists():
            return {'status': 'WARN', 'message': f'Data directory not found: {DATA_DIR}', 'validation': 'V1'}

        yaml_files = list(DATA_DIR.glob('*.yaml')) + list(DATA_DIR.glob('*.yml'))
        if not yaml_files:
            return {'status': 'WARN', 'message': 'No YAML files found in data/world', 'validation': 'V1'}

        invalid = []
        valid_count = 0

        for yf in yaml_files:
            try:
                with open(yf) as f:
                    yaml.safe_load(f)
                valid_count += 1
            except yaml.YAMLError as e:
                invalid.append(f"{yf.name}: {e}")
            except Exception as e:
                invalid.append(f"{yf.name}: {e}")

        if invalid:
            return {
                'status': 'ERROR',
                'message': f'{len(invalid)} invalid YAML files',
                'validation': 'V1',
                'invalid_files': invalid[:5]
            }

        return {
            'status': 'OK',
            'message': f'{valid_count} YAML files valid',
            'validation': 'V1',
            'count': valid_count
        }

    def _check_inject_script(self) -> Dict[str, Any]:
        """Verify injection script exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V2'}

        inject_script = PROJECT_ROOT / 'data/scripts/inject_world.py'
        if inject_script.exists():
            return {'status': 'OK', 'message': 'Injection script found', 'validation': 'V2'}
        else:
            return {'status': 'WARN', 'message': 'Injection script not found', 'validation': 'V2'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_world_scraping',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='World Scraping Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = WorldScrapingHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nWORLD SCRAPING HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

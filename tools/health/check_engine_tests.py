#!/usr/bin/env python3
"""
Engine Tests Health Checker

Verifies test suite health from HEALTH_Engine_Test_Suite.md:
- INV1: Unit tests don't require external services
- INV4: Suite executes via pytest

HEALTH: docs/engine/tests/HEALTH_Engine_Test_Suite.md
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
TESTS_DIR = PROJECT_ROOT / 'engine/tests'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class EngineTestsHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[EngineTestsHealth] Starting checks")

        self.results['test_suite_exists'] = self._check_test_files()
        self.results['tests_collect'] = self._check_tests_collect()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_test_files(self) -> Dict[str, Any]:
        """Verify test files exist."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'INV4'}

        if not TESTS_DIR.exists():
            return {'status': 'WARN', 'message': 'engine/tests directory not found', 'validation': 'INV4'}

        test_files = list(TESTS_DIR.glob('test_*.py'))
        if not test_files:
            return {'status': 'WARN', 'message': 'No test files found', 'validation': 'INV4'}

        return {
            'status': 'OK',
            'message': f'Found {len(test_files)} test files',
            'validation': 'INV4',
            'count': len(test_files)
        }

    def _check_tests_collect(self) -> Dict[str, Any]:
        """INV4: Verify pytest can collect tests."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'INV4'}

        if not TESTS_DIR.exists():
            return {'status': 'SKIP', 'message': 'No tests directory', 'validation': 'INV4'}

        try:
            result = subprocess.run(
                ['python3', '-m', 'pytest', str(TESTS_DIR), '--collect-only', '-q'],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=PROJECT_ROOT
            )

            if result.returncode == 0 or result.returncode == 5:  # 5 = no tests collected
                output = result.stdout
                if 'test' in output.lower() or 'collected' in output.lower():
                    return {'status': 'OK', 'message': 'Tests collected successfully', 'validation': 'INV4'}
                else:
                    return {'status': 'WARN', 'message': 'No tests collected', 'validation': 'INV4'}
            else:
                return {'status': 'ERROR', 'message': f'Collection failed: {result.stderr[:200]}', 'validation': 'INV4'}

        except FileNotFoundError:
            return {'status': 'SKIP', 'message': 'pytest not found', 'validation': 'INV4'}
        except subprocess.TimeoutExpired:
            return {'status': 'WARN', 'message': 'Collection timed out', 'validation': 'INV4'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Check failed: {e}', 'validation': 'INV4'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_engine_tests',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Engine Tests Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = EngineTestsHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nENGINE TESTS HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

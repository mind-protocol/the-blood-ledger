#!/usr/bin/env python3
"""
Business Model Health Checker

Verifies margin guardrails from HEALTH_Business_Model.md:
- Business model documentation exists
- Unit economics validation file exists

HEALTH: docs/product/business-model/HEALTH_Business_Model.md
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

PROJECT_ROOT = Path(__file__).parent.parent.parent

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class BusinessModelHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[BusinessModelHealth] Starting checks")

        self.results['business_model_docs'] = self._check_docs_exist()
        self.results['validation_exists'] = self._check_validation_exists()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_docs_exist(self) -> Dict[str, Any]:
        """Verify business model documentation exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        docs_dir = PROJECT_ROOT / 'docs/product/business-model'
        if docs_dir.exists():
            return {'status': 'OK', 'message': 'Business model docs exist', 'validation': 'V1'}
        return {'status': 'WARN', 'message': 'Business model docs not found', 'validation': 'V1'}

    def _check_validation_exists(self) -> Dict[str, Any]:
        """Verify business model validation file exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        validation_file = PROJECT_ROOT / 'docs/product/business-model/VALIDATION_Business_Model_Invariants.md'
        if validation_file.exists():
            return {'status': 'OK', 'message': 'Validation file exists', 'validation': 'V1'}
        return {'status': 'WARN', 'message': 'Validation file not found', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_business_model',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Business Model Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = BusinessModelHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nBUSINESS MODEL HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

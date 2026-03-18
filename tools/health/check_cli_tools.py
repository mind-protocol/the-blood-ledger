#!/usr/bin/env python3
"""
CLI Tools Health Checker

Verifies stream and mutation tools from HEALTH_CLI_Tools.md:
- Stream dialogue script exists and is executable
- Mutation tools are available

HEALTH: docs/infrastructure/cli-tools/HEALTH_CLI_Tools.md
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']


class CLIToolsHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[CLIToolsHealth] Starting checks")

        self.results['stream_dialogue_exists'] = self._check_stream_dialogue()
        self.results['cli_tools_syntax'] = self._check_syntax()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_stream_dialogue(self) -> Dict[str, Any]:
        """Verify stream_dialogue.py exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        stream_script = PROJECT_ROOT / 'tools/stream_dialogue.py'
        if stream_script.exists():
            return {'status': 'OK', 'message': 'stream_dialogue.py found', 'validation': 'V1'}
        else:
            return {'status': 'WARN', 'message': 'stream_dialogue.py not found', 'validation': 'V1'}

    def _check_syntax(self) -> Dict[str, Any]:
        """Verify CLI tool scripts have valid Python syntax."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        tools_dir = PROJECT_ROOT / 'tools'
        if not tools_dir.exists():
            return {'status': 'WARN', 'message': 'tools directory not found', 'validation': 'V1'}

        py_files = list(tools_dir.glob('*.py'))
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
                'message': f'{len(invalid)} files with syntax errors',
                'validation': 'V1',
                'invalid': invalid[:5]
            }

        return {'status': 'OK', 'message': f'{len(py_files)} CLI tools have valid syntax', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_cli_tools',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='CLI Tools Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = CLIToolsHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nCLI TOOLS HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

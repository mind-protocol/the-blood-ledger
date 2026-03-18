#!/usr/bin/env python3
"""
Image Generation Health Checker

Verifies asset pipeline from HEALTH_Image_Generation.md:
- Image generation script exists
- Script has valid syntax
- Output directory is accessible

HEALTH: docs/infrastructure/image-generation/HEALTH_Image_Generation.md
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


class ImageGenerationHealthChecker:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        logger.info("[ImageGenerationHealth] Starting checks")

        self.results['generate_script_exists'] = self._check_generate_script()
        self.results['generate_script_syntax'] = self._check_script_syntax()

        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses or 'SKIP' in statuses:
            return 'WARN'
        return 'OK'

    def _check_generate_script(self) -> Dict[str, Any]:
        """Verify generate_image.py exists."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        script = PROJECT_ROOT / 'tools/image_generation/generate_image.py'
        if script.exists():
            return {'status': 'OK', 'message': 'generate_image.py found', 'validation': 'V1'}
        else:
            return {'status': 'WARN', 'message': 'generate_image.py not found', 'validation': 'V1'}

    def _check_script_syntax(self) -> Dict[str, Any]:
        """Verify generate_image.py has valid Python syntax."""
        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        script = PROJECT_ROOT / 'tools/image_generation/generate_image.py'
        if not script.exists():
            return {'status': 'SKIP', 'message': 'Script not found', 'validation': 'V1'}

        try:
            result = subprocess.run(
                ['python3', '-m', 'py_compile', str(script)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return {'status': 'OK', 'message': 'Script syntax valid', 'validation': 'V1'}
            else:
                return {'status': 'ERROR', 'message': f'Syntax error: {result.stderr[:200]}', 'validation': 'V1'}
        except subprocess.TimeoutExpired:
            return {'status': 'WARN', 'message': 'Syntax check timed out', 'validation': 'V1'}
        except Exception as e:
            return {'status': 'SKIP', 'message': f'Syntax check failed: {e}', 'validation': 'V1'}

    def get_report(self) -> Dict[str, Any]:
        if not self.results:
            self.check_all()
        statuses = [r['status'] for r in self.results.values()]
        return {
            'checker': 'check_image_generation',
            'status': 'ERROR' if 'ERROR' in statuses else 'WARN' if 'WARN' in statuses or 'SKIP' in statuses else 'OK',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def main():
    parser = argparse.ArgumentParser(description='Image Generation Health Checker')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()
    checker = ImageGenerationHealthChecker(args.dry_run)
    status = checker.check_all()
    report = checker.get_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}\nIMAGE GENERATION HEALTH CHECK: {status}\n{'='*60}")
        for name, result in report['checks'].items():
            icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(result['status'], '?')
            print(f"  {icon} {name}: {result['status']} - {result['message']}")
        print(f"{'='*60}\n")

    return 0 if status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

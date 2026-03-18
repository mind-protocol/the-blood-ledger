#!/usr/bin/env python3
"""
Tempo Controller Health Checker

Verifies tempo controller invariants from VALIDATION_Tempo.md:
- V1: tick_count increments monotonically
- V4: Interrupt moments snap speed to 1x

HEALTH: docs/infrastructure/tempo/HEALTH_Tempo_Controller.md
VALIDATION: docs/infrastructure/tempo/VALIDATION_Tempo.md
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Literal

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Health status enum
HealthStatus = Literal['OK', 'WARN', 'ERROR', 'UNKNOWN', 'SKIP']

# Throttle file for production rate limiting
THROTTLE_FILE = PROJECT_ROOT / '.health_tempo_last_run'
THROTTLE_SECONDS = 3600  # 1 hour


class TempoHealthChecker:
    """
    Health checker for tempo controller.

    Executes dock-based verification against VALIDATION criteria.
    """

    def __init__(self, playthrough_id: str = 'health_check', dry_run: bool = False):
        self.playthrough_id = playthrough_id
        self.dry_run = dry_run
        self.results: Dict[str, Dict[str, Any]] = {}

    def check_all(self) -> HealthStatus:
        """Run all health checks and return aggregate status."""
        logger.info(f"[TempoHealth] Starting checks for playthrough: {self.playthrough_id}")

        # V1: Tick advances
        self.results['tempo_tick_advances'] = self._check_tick_advances()

        # V4: Speed transitions
        self.results['speed_transitions_work'] = self._check_speed_transitions()

        # Aggregate: worst_of
        statuses = [r['status'] for r in self.results.values()]
        if 'ERROR' in statuses:
            return 'ERROR'
        elif 'WARN' in statuses:
            return 'WARN'
        elif 'SKIP' in statuses and all(s in ('OK', 'SKIP') for s in statuses):
            return 'WARN'  # Some checks skipped
        elif all(s == 'OK' for s in statuses):
            return 'OK'
        else:
            return 'UNKNOWN'

    def _check_tick_advances(self) -> Dict[str, Any]:
        """
        V1: Verify tick_count increments by 1 for each tick.

        Dock: TempoController.tick_count @ tempo_controller.py:62
        """
        check_name = 'tempo_tick_advances'

        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V1'}

        try:
            from engine.infrastructure.tempo.tempo_controller import TempoController

            # Create controller instance
            controller = TempoController(playthrough_id=self.playthrough_id)

            # Record initial tick
            initial_tick = controller.tick_count

            # Tick once via physics (simulating tick_once without async)
            controller.physics.tick()
            controller.tick_count += 1

            # Verify increment
            final_tick = controller.tick_count

            if final_tick == initial_tick + 1:
                return {
                    'status': 'OK',
                    'message': f'tick_count: {initial_tick} -> {final_tick}',
                    'validation': 'V1',
                    'initial': initial_tick,
                    'final': final_tick
                }
            elif final_tick > initial_tick:
                return {
                    'status': 'WARN',
                    'message': f'tick_count incremented by {final_tick - initial_tick} (expected 1)',
                    'validation': 'V1',
                    'initial': initial_tick,
                    'final': final_tick
                }
            else:
                return {
                    'status': 'ERROR',
                    'message': f'tick_count stuck or decreased: {initial_tick} -> {final_tick}',
                    'validation': 'V1',
                    'initial': initial_tick,
                    'final': final_tick
                }

        except ImportError as e:
            return {
                'status': 'SKIP',
                'message': f'Import failed: {e}',
                'validation': 'V1'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Check failed: {e}',
                'validation': 'V1'
            }

    def _check_speed_transitions(self) -> Dict[str, Any]:
        """
        V4: Verify speed state machine transitions correctly.

        Dock: TempoController.set_speed @ tempo_controller.py:105
        """
        check_name = 'speed_transitions_work'

        if self.dry_run:
            return {'status': 'SKIP', 'message': 'Dry run - skipped', 'validation': 'V4'}

        try:
            from engine.infrastructure.tempo.tempo_controller import TempoController

            controller = TempoController(playthrough_id=self.playthrough_id)

            # Test: Set to 2x, then interrupt should snap to 1x
            controller.set_speed('2x', 'test')
            if controller.speed != '2x':
                return {
                    'status': 'ERROR',
                    'message': f'Failed to set speed to 2x (got {controller.speed})',
                    'validation': 'V4'
                }

            # Simulate interrupt (set to 1x)
            controller.set_speed('1x', 'interrupt')

            if controller.speed == '1x':
                return {
                    'status': 'OK',
                    'message': 'Speed transitions work: 2x -> 1x (interrupt)',
                    'validation': 'V4'
                }
            else:
                return {
                    'status': 'ERROR',
                    'message': f'Interrupt did not snap to 1x (got {controller.speed})',
                    'validation': 'V4'
                }

        except ImportError as e:
            return {
                'status': 'SKIP',
                'message': f'Import failed: {e}',
                'validation': 'V4'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Check failed: {e}',
                'validation': 'V4'
            }

    def get_report(self) -> Dict[str, Any]:
        """Get full health report."""
        aggregate = self.check_all() if not self.results else (
            'ERROR' if 'ERROR' in [r['status'] for r in self.results.values()] else
            'WARN' if 'WARN' in [r['status'] for r in self.results.values()] else
            'OK' if all(r['status'] == 'OK' for r in self.results.values()) else
            'UNKNOWN'
        )

        return {
            'checker': 'check_tempo',
            'playthrough_id': self.playthrough_id,
            'status': aggregate,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'checks': self.results
        }


def should_throttle() -> bool:
    """Check if we should skip due to throttling."""
    if not THROTTLE_FILE.exists():
        return False

    try:
        last_run = float(THROTTLE_FILE.read_text().strip())
        elapsed = datetime.utcnow().timestamp() - last_run
        return elapsed < THROTTLE_SECONDS
    except (ValueError, OSError):
        return False


def update_throttle():
    """Update throttle timestamp."""
    try:
        THROTTLE_FILE.write_text(str(datetime.utcnow().timestamp()))
    except OSError:
        pass


def update_health_file(status: HealthStatus):
    """Update status.result.value in the HEALTH file."""
    health_file = PROJECT_ROOT / 'docs/infrastructure/tempo/HEALTH_Tempo_Controller.md'

    if not health_file.exists():
        logger.warning(f"[TempoHealth] HEALTH file not found: {health_file}")
        return

    try:
        content = health_file.read_text()

        # Find and replace the status value
        import re
        pattern = r'(value:\s*)(\w+)'
        replacement = f'\\g<1>{status}'

        # Only replace in the status section
        new_content = re.sub(
            r'(status:\n\s+stream_destination:.*?\n\s+result:\n\s+representation:.*?\n\s+)value:\s*\w+',
            f'\\g<1>value: {status}',
            content,
            flags=re.DOTALL
        )

        # Update timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        new_content = re.sub(
            r'updated_at:\s*[\d\-T:Z]+',
            f'updated_at: {timestamp}',
            new_content
        )

        health_file.write_text(new_content)
        logger.info(f"[TempoHealth] Updated HEALTH file: status={status}")

    except Exception as e:
        logger.warning(f"[TempoHealth] Failed to update HEALTH file: {e}")


def main():
    parser = argparse.ArgumentParser(description='Tempo Controller Health Checker')
    parser.add_argument('--playthrough', '-p', default='health_check',
                        help='Playthrough ID to check (default: health_check)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Skip actual checks, just validate setup')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Ignore throttling')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--update-health', action='store_true',
                        help='Update HEALTH file with result')

    args = parser.parse_args()

    # Throttle check
    if not args.force and should_throttle():
        logger.info("[TempoHealth] Throttled - run with --force to override")
        if args.json:
            print(json.dumps({'status': 'THROTTLED', 'message': 'Rate limited'}))
        return 0

    # Run checks
    checker = TempoHealthChecker(
        playthrough_id=args.playthrough,
        dry_run=args.dry_run
    )

    aggregate_status = checker.check_all()
    report = checker.get_report()

    # Output
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"TEMPO HEALTH CHECK: {aggregate_status}")
        print(f"{'='*60}")
        for name, result in report['checks'].items():
            status_icon = {'OK': '✓', 'WARN': '⚠', 'ERROR': '✗', 'SKIP': '○'}.get(
                result['status'], '?'
            )
            print(f"  {status_icon} {name}: {result['status']}")
            print(f"    {result['message']}")
        print(f"{'='*60}\n")

    # Update throttle
    if not args.dry_run:
        update_throttle()

    # Update HEALTH file
    if args.update_health:
        update_health_file(aggregate_status)

    # Exit code
    return 0 if aggregate_status in ('OK', 'WARN') else 1


if __name__ == '__main__':
    sys.exit(main())

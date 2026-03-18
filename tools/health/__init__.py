"""
Health Checkers for Blood Ledger

Each checker verifies runtime health against VALIDATION criteria defined
in the corresponding HEALTH documentation file.

Usage:
    python3 tools/health/check_tempo.py --help
    python3 tools/health/check_tempo.py --dry-run
    python3 tools/health/check_tempo.py --json

    # Run all checkers
    python3 tools/health/run_all_checks.py --json

Integration with ngram doctor:
    These checkers are designed to integrate with `ngram doctor` for
    aggregated health reporting across all modules.

Throttling:
    By default, checkers are throttled to max 1/hour in production.
    Use --force to override throttling.
"""

from .check_tempo import TempoHealthChecker
from .check_opening import OpeningHealthChecker
from .check_canon import CanonHealthChecker
from .check_async import AsyncHealthChecker
from .check_history import HistoryHealthChecker
from .check_frontend import FrontendHealthChecker
from .check_engine_tests import EngineTestsHealthChecker
from .check_embeddings import EmbeddingsHealthChecker
from .check_world_builder import WorldBuilderHealthChecker
from .check_world_scraping import WorldScrapingHealthChecker
from .check_map import MapHealthChecker
from .check_cli_tools import CLIToolsHealthChecker
from .check_image_generation import ImageGenerationHealthChecker
from .check_ops_scripts import OpsScriptsHealthChecker
from .check_storms import StormsHealthChecker
from .check_storm_loader import StormLoaderHealthChecker
from .check_billing import BillingHealthChecker
from .check_ledger_lock import LedgerLockHealthChecker
from .check_chronicle import ChronicleHealthChecker
from .check_gtm import GTMHealthChecker
from .check_business_model import BusinessModelHealthChecker
from .check_vision_docs import VisionDocsHealthChecker
from .check_world_scavenger import WorldScavengerHealthChecker
from .check_ghost_dialogue import GhostDialogueHealthChecker
from .check_shadow_feed import ShadowFeedHealthChecker
from .check_voyager import VoyagerHealthChecker
from .check_bleed_through import BleedThroughHealthChecker
from .check_transposition import TranspositionHealthChecker
from .check_schema_archive import SchemaArchiveHealthChecker

__all__ = [
    'TempoHealthChecker',
    'OpeningHealthChecker',
    'CanonHealthChecker',
    'AsyncHealthChecker',
    'HistoryHealthChecker',
    'FrontendHealthChecker',
    'EngineTestsHealthChecker',
    'EmbeddingsHealthChecker',
    'WorldBuilderHealthChecker',
    'WorldScrapingHealthChecker',
    'MapHealthChecker',
    'CLIToolsHealthChecker',
    'ImageGenerationHealthChecker',
    'OpsScriptsHealthChecker',
    'StormsHealthChecker',
    'StormLoaderHealthChecker',
    'BillingHealthChecker',
    'LedgerLockHealthChecker',
    'ChronicleHealthChecker',
    'GTMHealthChecker',
    'BusinessModelHealthChecker',
    'VisionDocsHealthChecker',
    'WorldScavengerHealthChecker',
    'GhostDialogueHealthChecker',
    'ShadowFeedHealthChecker',
    'VoyagerHealthChecker',
    'BleedThroughHealthChecker',
    'TranspositionHealthChecker',
    'SchemaArchiveHealthChecker',
]

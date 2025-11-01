#!/usr/bin/env python3
"""
Collection Embedding Runner V6 - Exclusive Ensemble Mode
=========================================================

Fresh implementation for V5 chunker output with exclusive GPU leasing.

KEY FEATURES:
- Processes each collection with ALL ensemble models before moving to next
- Exclusive mode: one model leases both GPUs at a time
- Model-first iteration per collection (not collection-per-model)
- Clear console output showing which models executed per collection
- V5 chunker compatibility (individual chunk JSON files per document)

EXCLUSIVE MODE BEHAVIOR:
1. Load collection chunks into memory
2. For EACH model in ensemble roster:
   - Stage previous model to CPU (if any)
   - Lease GPUs exclusively for current model
   - Hydrate model onto leased GPUs
   - Process ALL chunks with this model
   - Release GPUs
3. Aggregate embeddings from all models
4. Move to next collection

CONSOLE OUTPUT:
- Mode label: "EXCLUSIVE (model-at-a-time)"
- Progress per model within each collection
- Models executed list after each collection
- GPU lease events (acquire/release) per model
- Per-collection summary with timing

USAGE:
    # Kaggle (defaults to exclusive mode)
    python embed_collections_v6.py --chunked-dir /kaggle/input/chunks

    # Local (force exclusive mode)
    python embed_collections_v6.py --chunked-dir ./Chunked --exclusive-ensemble

    # Override ensemble models
    python embed_collections_v6.py --chunked-dir ./Chunked \\
        --ensemble-models jina-code-embeddings-1.5b bge-m3
"""

import argparse
import json
import logging
import os
import shutil
import sys
import time
import traceback
import zipfile
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# ============================================================================
# Setup Python path for processor imports
# ============================================================================
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# ============================================================================
# Import embedder components (V5 architecture)
# ============================================================================
try:
    from processor.ultimate_embedder import (
        UltimateKaggleEmbedderV4,
        EnsembleConfig,
        KaggleGPUConfig,
        KaggleExportConfig,
        FeatureToggleConfig,
        load_feature_toggles,
        normalize_kaggle_model_names,
    )
    from processor.chunk_utils import find_chunk_files
except ImportError as exc:
    print(f"CRITICAL: Failed to import embedder modules: {exc}")
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# Constants
# ============================================================================
KAGGLE_ENV = "/kaggle" in str(Path.cwd())

KAGGLE_DEFAULTS = {
    "exclusive_ensemble": True,  # Always use exclusive mode on Kaggle
    "ensemble_models": [
        "jina-code-embeddings-1.5b",
        "bge-m3", 
        "qwen3-embedding-0.6b",
    ],
    "output_dir": "/kaggle/working",
    "chunked_dir": "/kaggle/input",
}

LOCAL_DEFAULTS = {
    "exclusive_ensemble": True,  # Default to exclusive mode (safer, works everywhere)
    "ensemble_models": [
        "jina-code-embeddings-1.5b",
        "bge-m3",
        "qwen3-embedding-0.6b", 
    ],
    "output_dir": "./Embeddings",
    "chunked_dir": "./Chunked",
}

# ============================================================================
# Logging setup
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
LOGGER = logging.getLogger("embed_v6_exclusive")

# ============================================================================
# Data structures
# ============================================================================

@dataclass
class CollectionResult:
    """Result from processing a single collection."""
    
    collection_name: str
    chunk_count: int
    embedding_count: int
    models_executed: List[str]
    elapsed_seconds: float
    success: bool
    error_message: Optional[str] = None
    lease_events: List[Dict[str, Any]] = field(default_factory=list)
    processing_summary_path: Optional[str] = None
    processing_summary: Optional[Dict[str, Any]] = None
    metrics_report: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data.pop("processing_summary", None)
        data.pop("metrics_report", None)
        return data


# ============================================================================
# Argument parsing
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments with environment-aware defaults.
    
    Automatically detects Kaggle vs Local environment and applies appropriate
    defaults. On Kaggle, --exclusive-ensemble defaults to True and cannot be
    disabled via CLI (use environment variable DISABLE_EXCLUSIVE=1 if needed).
    
    Returns:
        Parsed arguments namespace
    """
    defaults = KAGGLE_DEFAULTS if KAGGLE_ENV else LOCAL_DEFAULTS

    toggles = load_feature_toggles()
    if toggles.enable_sparse and toggles.sparse_models:
        sparse_default_label = ", ".join(toggles.sparse_models)
    elif toggles.enable_sparse:
        sparse_default_label = "none"
    else:
        sparse_default_label = "disabled (FeatureToggleConfig)"

    parser = argparse.ArgumentParser(
        description="Embed collections with exclusive ensemble mode (V6)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"Environment: {'Kaggle' if KAGGLE_ENV else 'Local'}\n"
            "Current defaults:\n"
            f"  chunked_dir: {defaults['chunked_dir']}\n"
            f"  output_dir: {defaults['output_dir']}\n"
            f"  exclusive_ensemble: {defaults['exclusive_ensemble']}\n"
            f"  ensemble_models: {defaults['ensemble_models']}\n\n"
            "Rerank & Sparse Feature Toggles (Default-On):\n"
            "  --enable-rerank       Enable CrossEncoder reranking (default: enabled)\n"
            "  --disable-rerank      Disable CrossEncoder reranking\n"
            "  --enable-sparse       Enable sparse embeddings (SPLADE) (default: enabled)\n"
            "  --disable-sparse      Disable sparse embeddings\n"
            f"  --sparse-models LIST  Override sparse model list (default: {sparse_default_label})\n\n"
            "Note: Both rerank and sparse are ENABLED BY DEFAULT. Use --disable-* flags\n"
            "for rollback or degradation scenarios. Toggle sources recorded in telemetry.\n\n"
            "Environment Variable Overrides:\n"
            "  rerank: EMBEDDER_ENABLE_RERANK=0 or --disable-rerank to opt out\n"
            "  sparse: EMBEDDER_ENABLE_SPARSE=0 or --disable-sparse to opt out\n"
            "  sparse_models: EMBEDDER_SPARSE_MODELS or --sparse-models to override\n\n"
            "Resolution order: defaults -> config -> env -> CLI\n\n"
            "See docs/telemetry/rerank_sparse_signals.md for observability guidance."
        ),
    )

    parser.add_argument(
        "--chunked-dir",
        type=str,
        default=defaults["chunked_dir"],
        help="Root directory containing chunked collections",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=defaults["output_dir"],
        help="Output directory for embeddings",
    )
    
    # Exclusive ensemble with ability to disable
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument(
        "--exclusive-ensemble",
        dest="exclusive_ensemble",
        action="store_true",
        default=defaults["exclusive_ensemble"],
        help="Enable exclusive GPU leasing per model (default: True)",
    )
    exclusive_group.add_argument(
        "--no-exclusive-ensemble",
        dest="exclusive_ensemble",
        action="store_false",
        help="Disable exclusive mode, use parallel processing (advanced users only)",
    )
    
    parser.add_argument(
        "--ensemble-models",
        nargs="+",
        default=defaults["ensemble_models"],
        help="List of ensemble models to use",
    )
    
    parser.add_argument(
        "--collections",
        nargs="+",
        default=None,
        help="Specific collections to process (omit for all)",
    )

    parser.add_argument(
        "--enable-rerank",
        dest="enable_rerank",
        action="store_true",
        default=None,
        help=(
            "Force enable rerank stage (defaults to enabled; env EMBEDDER_ENABLE_RERANK)"
        ),
    )
    parser.add_argument(
        "--disable-rerank",
        dest="enable_rerank",
        action="store_false",
        help="Disable rerank stage (default is enabled)",
    )

    parser.add_argument(
        "--enable-sparse",
        dest="enable_sparse",
        action="store_true",
        default=None,
        help=(
            "Force enable sparse stage (defaults to enabled; env EMBEDDER_ENABLE_SPARSE)"
        ),
    )
    parser.add_argument(
        "--disable-sparse",
        dest="enable_sparse",
        action="store_false",
        help="Disable sparse stage (default is enabled)",
    )

    parser.add_argument(
        "--sparse-models",
        nargs="+",
        default=None,
        help=(
            "Override sparse models to load (comma or space separated; "
            "default from EMBEDDER_SPARSE_MODELS)"
        ),
    )

    args = parser.parse_args()

    toggles = load_feature_toggles()
    toggle_sources = dict(toggles.sources)
    resolution_events = list(toggles.resolution_events)

    def _record_cli_event(key: str, value: Any, flag_name: str) -> None:
        resolution_events.append(
            {
                "key": key,
                "value": value,
                "source": flag_name,
                "layer": "cli",
            }
        )

    cli_enable_rerank = args.enable_rerank
    if cli_enable_rerank is None:
        args.enable_rerank = toggles.enable_rerank
    else:
        toggle_sources["enable_rerank"] = "cli"
        args.enable_rerank = cli_enable_rerank
        flag = "--enable-rerank" if args.enable_rerank else "--disable-rerank"
        _record_cli_event("enable_rerank", args.enable_rerank, f"cli:{flag}")

    cli_enable_sparse = args.enable_sparse
    if cli_enable_sparse is None:
        args.enable_sparse = toggles.enable_sparse
    else:
        toggle_sources["enable_sparse"] = "cli"
        args.enable_sparse = cli_enable_sparse
        flag = "--enable-sparse" if args.enable_sparse else "--disable-sparse"
        _record_cli_event("enable_sparse", args.enable_sparse, f"cli:{flag}")

    cli_sparse_models = args.sparse_models
    if cli_sparse_models is None:
        args.sparse_models = list(toggles.sparse_models)
    else:
        parsed_sparse: List[str] = []
        for entry in cli_sparse_models:
            for token in entry.split(","):
                candidate = token.strip()
                if candidate:
                    parsed_sparse.append(candidate)
        args.sparse_models = parsed_sparse
        toggle_sources["sparse_models"] = "cli"
        _record_cli_event("sparse_models", list(args.sparse_models), "cli:--sparse-models")

    if not args.enable_sparse:
        if args.sparse_models:
            _record_cli_event("sparse_models", [], "cli:disable-sparse-trim")
        toggle_sources["sparse_models"] = "cli:disable-sparse-trim"
        args.sparse_models = []

    args.toggle_sources = toggle_sources
    args.toggle_resolution_events = tuple(resolution_events)

    if not hasattr(args, "create_zip"):
        args.create_zip = False
    if not hasattr(args, "zip_compression"):
        args.zip_compression = "deflated"

    return args


# ============================================================================
# Collection discovery
# ============================================================================

# Constants for collection discovery
CHUNK_FILE_PATTERN = "*_chunks.json"
MAX_DISCOVERY_DEPTH = 5


def _is_collection_directory(directory: Path) -> bool:
    """
    Check if a directory contains chunk files (non-recursive check).
    
    Args:
        directory: Path to check
        
    Returns:
        True if directory contains chunk files, False otherwise
    """
    if not directory.exists() or not directory.is_dir():
        return False
    
    try:
        # Look for chunk files with the standard pattern
        chunk_files = list(directory.glob(CHUNK_FILE_PATTERN))
        return len(chunk_files) > 0
    except (OSError, PermissionError) as exc:
        LOGGER.debug(f"Cannot check directory {directory}: {exc}")
        return False


def _resolve_collection_name(
    directory: Path,
    chunked_dir: Path,
    existing_names: set
) -> str:
    """
    Generate a unique collection name for a directory.
    
    Args:
        directory: Collection directory path
        chunked_dir: Root chunked directory for relative path calculation
        existing_names: Set of already-used collection names
        
    Returns:
        Unique collection name (uses directory name, or relative path if collision)
    """
    collection_name = directory.name
    
    # No collision, use simple name
    if collection_name not in existing_names:
        return collection_name
    
    # Collision detected - use relative path
    try:
        rel_path = directory.relative_to(chunked_dir)
        collection_name = str(rel_path).replace(os.sep, '_')
    except ValueError:
        # Not relative to chunked_dir, use absolute path hash
        collection_name = f"{directory.name}_{abs(hash(str(directory))) % 10000:04d}"
    
    return collection_name


def _scan_directory_recursive(
    directory: Path,
    chunked_dir: Path,
    collections: Dict[str, Path],
    max_depth: int = MAX_DISCOVERY_DEPTH,
    current_depth: int = 0,
) -> None:
    """
    Recursively scan directory tree for collections.
    
    Modifies collections dict in-place.
    
    Args:
        directory: Current directory to scan
        chunked_dir: Root chunked directory (for relative path calculation)
        collections: Dict to populate with discovered collections
        max_depth: Maximum recursion depth
        current_depth: Current recursion level
    """
    # Depth limit reached
    if current_depth >= max_depth:
        LOGGER.debug(f"Max depth {max_depth} reached at: {directory}")
        return
    
    # Validate directory
    if not directory.exists():
        LOGGER.debug(f"Directory does not exist: {directory}")
        return
    
    if not directory.is_dir():
        LOGGER.debug(f"Not a directory: {directory}")
        return
    
    # Check if this is a collection directory
    if _is_collection_directory(directory):
        # Count chunks
        chunk_files = list(directory.glob(CHUNK_FILE_PATTERN))
        chunk_count = len(chunk_files)
        
        # Generate unique name
        collection_name = _resolve_collection_name(
            directory,
            chunked_dir,
            set(collections.keys())
        )
        
        # Register collection
        collections[collection_name] = directory
        LOGGER.info(
            f"Discovered collection '{collection_name}' "
            f"with {chunk_count} chunk files"
        )
        
        # Don't recurse into collections (chunks should be at this level)
        return
    
    # Not a collection, scan subdirectories
    try:
        subdirs = [entry for entry in directory.iterdir() if entry.is_dir()]
        
        for subdir in subdirs:
            _scan_directory_recursive(
                subdir,
                chunked_dir,
                collections,
                max_depth,
                current_depth + 1
            )
    except PermissionError:
        LOGGER.warning(f"Permission denied scanning directory: {directory}")
    except OSError as exc:
        LOGGER.warning(f"Error scanning directory {directory}: {exc}")


def discover_collections(chunked_dir: Path) -> Dict[str, Path]:
    """
    Recursively discover all collection directories from chunked directory structure.
    
    A collection is a directory containing files matching the pattern '*_chunks.json'.
    Handles arbitrary nesting levels (up to MAX_DISCOVERY_DEPTH) and works with
    Kaggle dataset wrappers or local directory structures.
    
    Args:
        chunked_dir: Root directory to scan for collections
        
    Returns:
        Dictionary mapping collection_name -> collection_directory_path
        Returns empty dict if chunked_dir doesn't exist or has no collections.
        
    Examples:
        >>> collections = discover_collections(Path("./Chunked"))
        >>> len(collections)
        224
        >>> "Docling" in collections
        True
    """
    collections: Dict[str, Path] = {}
    
    # Validate input directory
    if not chunked_dir.exists():
        LOGGER.warning(f"Chunked directory does not exist: {chunked_dir}")
        return collections
    
    if not chunked_dir.is_dir():
        LOGGER.error(f"Chunked path is not a directory: {chunked_dir}")
        return collections
    
    # Scan recursively
    LOGGER.info(f"Scanning for collections in: {chunked_dir}")
    _scan_directory_recursive(
        directory=chunked_dir,
        chunked_dir=chunked_dir,
        collections=collections,
        max_depth=MAX_DISCOVERY_DEPTH,
        current_depth=0
    )
    
    # Log summary
    if collections:
        LOGGER.info(f"Discovery complete: found {len(collections)} collections")
    else:
        LOGGER.warning(f"No collections found in {chunked_dir}")
    
    return collections


# ============================================================================
# Core processing
# ============================================================================

# Result keys from embedder (exclusive mode returns these at top level)
RESULT_KEY_MODELS_EXECUTED = "models_executed"
RESULT_KEY_LEASE_EVENTS = "lease_events"
RESULT_KEY_TOTAL_EMBEDDINGS = "total_embeddings_generated"
RESULT_KEY_ERROR = "error"


def _get_ensemble_mode_label(exclusive_mode: bool) -> str:
    """Get human-readable label for ensemble mode."""
    return "EXCLUSIVE (model-at-a-time)" if exclusive_mode else "PARALLEL"


def _extract_telemetry(results: Dict[str, Any]) -> tuple[List[str], List[Dict], int]:
    """
    Extract telemetry data from embedder results.
    
    Args:
        results: Results dictionary from generate_embeddings_kaggle_optimized
        
    Returns:
        Tuple of (models_executed, lease_events, embedding_count)
    """
    models_executed = results.get(RESULT_KEY_MODELS_EXECUTED, [])
    lease_events = results.get(RESULT_KEY_LEASE_EVENTS, [])
    embedding_count = results.get(RESULT_KEY_TOTAL_EMBEDDINGS, 0)
    
    return models_executed, lease_events, embedding_count


def _log_toggle_resolution(events: Iterable[Dict[str, Any]]) -> None:
    """Log the feature toggle resolution chain for transparency."""
    if not events:
        return

    LOGGER.info("Toggle resolution chain (earliest -> latest):")
    for event in events:
        key = event.get("key", "?")
        value = event.get("value")
        source = event.get("source", "unknown")
        layer = event.get("layer", "unknown")
        if isinstance(value, list):
            display_value = ", ".join(str(item) for item in value) or "[]"
        else:
            display_value = str(value)
        LOGGER.info(
            "  %-14s => %-20s (layer=%s source=%s)",
            key,
            display_value,
            layer,
            source,
        )


def _log_collection_completion(
    collection_name: str,
    models_executed: List[str],
    lease_events: List[Dict[str, Any]],
    elapsed_seconds: float,
    summary_path: Optional[str] = None,
    summary_payload: Optional[Dict[str, Any]] = None,
    metrics_report: Optional[Dict[str, Any]] = None,
    warnings: Optional[List[str]] = None,
) -> None:
    """Emit a consolidated summary for collection completion."""
    LOGGER.info(f"\n{'='*80}")
    LOGGER.info(f"Collection '{collection_name}' completed")
    LOGGER.info(f"Models executed: {models_executed}")
    LOGGER.info(f"Lease events: {len(lease_events)}")

    if lease_events:
        LOGGER.info("\nGPU Lease Summary:")
        for event in lease_events:
            event_type = event.get("event_type", "unknown")
            model = event.get("model", "unknown")
            devices = event.get("device_ids", [])
            LOGGER.info("  [%s] %s on %s", event_type.upper(), model, devices)

        leased_devices = sorted(
            {
                device
                for event in lease_events
                if event.get("event_type") == "acquire"
                for device in event.get("device_ids", [])
            }
        )
        if leased_devices:
            LOGGER.info("  Active GPU set: %s", leased_devices)
        else:
            LOGGER.info("  Active GPU set: none (cpu-only run)")

    LOGGER.info(f"Elapsed: {elapsed_seconds:.2f}s")
    if summary_path:
        LOGGER.info("Processing summary: %s", summary_path)

    summary_warnings = list(warnings or [])
    if summary_payload:
        feature_toggles = summary_payload.get("feature_toggles", {})
        toggle_sources = feature_toggles.get("sources", {})
        provenance_lines = (
            feature_toggles.get("provenance_lines")
            or summary_payload.get("activation_provenance_lines")
            or feature_toggles.get("provenance")
            or summary_payload.get("activation_provenance")
            or []
        )

        LOGGER.info("Stage states:")

        rerank_info = summary_payload.get("rerank_run")
        if rerank_info is None:
            rerank_source = toggle_sources.get("enable_rerank", "default")
            LOGGER.info("  rerank: disabled (source=%s)", rerank_source)
        else:
            rerank_source = toggle_sources.get("enable_rerank", "default")
            device_state = rerank_info.get("device_state", {})
            resolved_device = device_state.get("resolved") or rerank_info.get("device", "cpu")
            requested_device = device_state.get("requested") or "?"
            fallback_applied = bool(device_state.get("fallback_applied"))
            device_fallback_reason = device_state.get("fallback_reason")
            rerank_reason = rerank_info.get("reason")
            fallback_count = int(rerank_info.get("fallback_count") or 0)
            rerank_fallback_reason = rerank_info.get("fallback_reason")
            rerank_fallback_source = rerank_info.get("fallback_source")
            LOGGER.info(
                "  rerank: enabled=%s (source=%s) executed=%s model=%s requested=%s resolved=%s status=%s",
                rerank_info.get("enabled"),
                rerank_source,
                rerank_info.get("executed"),
                rerank_info.get("model_name") or "",
                requested_device,
                resolved_device,
                rerank_info.get("status", "n/a"),
            )
            # Log performance metrics when rerank was executed
            if rerank_info.get("executed"):
                latency_ms = rerank_info.get("latency_ms")
                gpu_peak_gb = rerank_info.get("gpu_peak_gb")
                batch_size = rerank_info.get("batch_size")
                candidate_count = rerank_info.get("candidate_count")
                if candidate_count is None:
                    candidate_count = rerank_info.get("result_count")
                if candidate_count is None:
                    candidate_ids = rerank_info.get("candidate_ids")
                    if isinstance(candidate_ids, list):
                        candidate_count = len(candidate_ids)
                LOGGER.info(
                    "    performance: latency=%.2fms gpu_peak=%.2fGB batch_size=%s candidates=%s",
                    latency_ms if latency_ms is not None else 0.0,
                    gpu_peak_gb if gpu_peak_gb is not None else 0.0,
                    batch_size if batch_size is not None else "n/a",
                    candidate_count if candidate_count is not None else "n/a",
                )
            if rerank_reason:
                LOGGER.info("    reason: %s", rerank_reason)
            if fallback_applied:
                LOGGER.info(
                    "    device fallback: applied (%s)",
                    device_fallback_reason or "reason not provided",
                )
            if fallback_count > 0:
                LOGGER.info(
                    "    fallback counter: count=%s reason=%s source=%s",
                    fallback_count,
                    rerank_fallback_reason or rerank_reason or "unspecified",
                    rerank_fallback_source or rerank_source,
                )

        sparse_source = toggle_sources.get("enable_sparse", "default")
        sparse_info = summary_payload.get("sparse_run")
        if sparse_info is None:
            sparse_enabled = feature_toggles.get("enable_sparse", False)
            if sparse_enabled:
                LOGGER.warning(
                    "  sparse: enabled in toggles (source=%s) but sparse_run section missing from manifest",
                    sparse_source
                )
            else:
                LOGGER.info("  sparse: disabled (source=%s)", sparse_source)
        else:
            vectors = sparse_info.get("vectors", {})
            coverage = vectors.get("coverage_ratio")
            coverage_display = (
                f"{coverage:.3f}" if isinstance(coverage, (int, float)) else "n/a"
            )
            devices = sparse_info.get("devices") or {}
            fallback_used = bool(sparse_info.get("fallback_used"))
            sparse_reason = sparse_info.get("reason")
            LOGGER.info(
                "  sparse: enabled=%s (source=%s) executed=%s models=%s coverage=%s",
                sparse_info.get("enabled"),
                sparse_source,
                sparse_info.get("executed"),
                ", ".join(sparse_info.get("models", [])) or "none",
                coverage_display,
            )
            if devices:
                LOGGER.info("    devices: %s", ", ".join(f"{model} -> {device}" for model, device in devices.items()))
            if sparse_reason:
                LOGGER.info("    reason: %s", sparse_reason)
            if fallback_used:
                fallback_reason = sparse_info.get("fallback_reason") or "metadata fallback engaged"
                LOGGER.info("    fallback: %s", fallback_reason)

        if provenance_lines:
            LOGGER.info("Activation provenance:")
            for event in provenance_lines:
                if isinstance(event, dict):
                    LOGGER.info(
                        "  %-14s => %-20s (layer=%s source=%s)",
                        event.get("key", "?"),
                        event.get("value"),
                        event.get("layer", "?"),
                        event.get("source", "?"),
                    )
                else:
                    LOGGER.info("  %s", event)

        baseline = summary_payload.get("performance_baseline") or {}
        summary_warnings.extend(summary_payload.get("warnings", []) or [])

        gpu_perf = baseline.get("gpu")
        if gpu_perf:
            LOGGER.info(
                "GPU peak usage: %.2f GB on device %s (samples=%s)",
                gpu_perf.get("peak_memory_used_gb", 0.0),
                gpu_perf.get("peak_device", "?"),
                gpu_perf.get("samples", 0),
            )
        else:
            LOGGER.info(
                "GPU peak usage: stage-level telemetry pending instrumentation"
            )

        hydration = baseline.get("hydration")
        if hydration:
            LOGGER.info(
                "Hydration baseline: avg %.2fs peak %.2fs (samples=%s, failures=%s)",
                hydration.get("average_duration_seconds", 0.0),
                hydration.get("peak_duration_seconds", 0.0),
                hydration.get("samples", 0),
                hydration.get("failures", 0),
            )

        system_perf = baseline.get("system")
        if system_perf:
            LOGGER.info(
                "System baseline: CPU avg %.1f%% peak %.1f%% | RAM avg %.2f GB peak %.2f GB",
                system_perf.get("average_cpu_percent", 0.0),
                system_perf.get("peak_cpu_percent", 0.0),
                system_perf.get("average_memory_gb", 0.0),
                system_perf.get("peak_memory_gb", 0.0),
            )

        telemetry_footer = summary_payload.get("telemetry", {})
        spans = telemetry_footer.get("spans") or {}
        if spans:
            LOGGER.info("Telemetry spans:")
            for span_name, info in spans.items():
                if not isinstance(info, dict):
                    LOGGER.info("  %s: %s", span_name, info)
                    continue
                status = info.get("status", "unknown")
                span_id = info.get("span_id", "n/a")
                reason = info.get("reason")
                message = f"  {span_name}: {status} (span_id={span_id})"
                if reason:
                    message += f" reason={reason}"
                LOGGER.info(message)
        else:
            LOGGER.info("Telemetry spans: none captured")

    if metrics_report:
        LOGGER.info("Metrics emission summary:")
        for stage, report in metrics_report.items():
            if not isinstance(report, dict):
                LOGGER.info("  %s: %s", stage, report)
                continue
            status = report.get("status", "unknown")
            metrics_list = report.get("metrics")
            if isinstance(metrics_list, (list, tuple)):
                metrics_display = ", ".join(str(item) for item in metrics_list) or "n/a"
            else:
                metrics_display = "n/a"
            LOGGER.info("  %s: %s (metrics=%s)", stage, status, metrics_display)
            reason = report.get("reason")
            if reason:
                LOGGER.info("    reason: %s", reason)

    if summary_warnings:
        LOGGER.warning("Stage warnings detected:")
        for warning in summary_warnings:
            LOGGER.warning("  - %s", warning)

    LOGGER.info(f"{'='*80}\n")


def process_collection(
    collection_name: str,
    collection_path: Path,
    embedder: UltimateKaggleEmbedderV4,
    output_dir: Path,
    exclusive_mode: bool,
) -> CollectionResult:
    """
    Process a single collection with all ensemble models.
    
    Loads chunks from the collection directory, generates embeddings using the
    embedder (with exclusive or parallel ensemble mode), and returns processing
    results with telemetry.
    
    Args:
        collection_name: Name of the collection
        collection_path: Path to collection chunk directory
        embedder: Configured embedder instance
        output_dir: Output directory for embeddings
        exclusive_mode: Whether exclusive ensemble mode is enabled
        
    Returns:
        CollectionResult with success status, metrics, and optional error message
    """
    start_time = time.time()
    
    try:
        # Discover and validate chunk files
        chunk_files = find_chunk_files(collection_path)
        if not chunk_files:
            LOGGER.warning(f"No chunk files found in {collection_path}")
            return CollectionResult(
                collection_name=collection_name,
                chunk_count=0,
                embedding_count=0,
                models_executed=[],
                elapsed_seconds=time.time() - start_time,
                success=False,
                error_message="No chunk files found",
            )
        
        # Log processing start
        LOGGER.info(f"\n{'='*80}")
        LOGGER.info(f"Processing collection: {collection_name}")
        LOGGER.info(f"Chunk files: {len(chunk_files)}")
        LOGGER.info(f"Ensemble mode: {_get_ensemble_mode_label(exclusive_mode)}")
        LOGGER.info(f"{'='*80}\n")
        
        # Load chunks into embedder
        load_summary = embedder.load_chunks_from_processing(
            chunks_dir=str(collection_path),
        )
        
        # Validate load results
        if load_summary.get(RESULT_KEY_ERROR):
            error_msg = load_summary.get(RESULT_KEY_ERROR)
            raise RuntimeError(f"Chunk loading failed: {error_msg}")

        total_chunks_loaded = load_summary.get("total_chunks_loaded") if isinstance(load_summary, dict) else None
        
        # Generate embeddings
        results = embedder.generate_embeddings_kaggle_optimized(
            enable_monitoring=True,
            save_intermediate=True,
        )
        
        # Validate generation results
        if not isinstance(results, dict):
            raise RuntimeError(f"Invalid results type: {type(results)}")
        
        # Extract telemetry
        models_executed, lease_events, embedding_count = _extract_telemetry(results)
        
        # ======================================================================
        # PHASE 1: Export embeddings to disk (per-collection subdirectory)
        # ======================================================================
        LOGGER.info(f"Exporting collection '{collection_name}' to disk...")
        
        # Create collection-specific subdirectory
        collection_output_dir = output_dir / collection_name
        collection_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Temporarily update export config for this collection
        original_working_dir = embedder.export_config.working_dir
        original_output_prefix = embedder.export_config.output_prefix
        
        try:
            # Configure export paths for this collection
            embedder.export_config.working_dir = str(collection_output_dir)
            embedder.export_config.output_prefix = collection_name
            
            # Export embeddings using existing export_runtime
            exported_files = embedder.export_for_local_qdrant()
            
            LOGGER.info(
                f"✅ Exported {embedding_count} embeddings for '{collection_name}' "
                f"({len(exported_files)} files)"
            )
            
        finally:
            # Restore original export config
            embedder.export_config.working_dir = original_working_dir
            embedder.export_config.output_prefix = original_output_prefix

        summary_path = collection_output_dir / f"{collection_name}_processing_summary.json"
        chunk_total = total_chunks_loaded
        if not isinstance(chunk_total, int):
            dense_total = results.get(RESULT_KEY_TOTAL_EMBEDDINGS) if isinstance(results, dict) else None
            if isinstance(dense_total, int):
                chunk_total = dense_total

        summary_payload = embedder.write_processing_summary(
            summary_path,
            collection_name=collection_name,
            chunk_count=chunk_total,
        )
        LOGGER.info("Processing summary saved to: %s", summary_path)
        summary_path_str = str(summary_path)
        
        # ======================================================================
        # Clear embeddings to free memory before next collection
        # ======================================================================
        LOGGER.debug(f"Clearing embeddings for '{collection_name}' to free memory...")
        embedder.embeddings = None
        embedder.embeddings_by_model.clear()
        embedder.chunk_texts.clear()
        embedder.chunks_metadata.clear()
        embedder.sparse_vectors.clear()
        embedder.fused_candidates = {}
        embedder.rerank_run = None
        embedder.rerank_candidate_scores = {}
        embedder.rerank_failure_reason = None
        
        # Calculate elapsed time
        elapsed = time.time() - start_time
        
        # Log completion
        telemetry_metrics = None
        summary_warnings: List[str] = []
        if isinstance(summary_payload, dict):
            telemetry_section = summary_payload.get("telemetry")
            if isinstance(telemetry_section, dict):
                telemetry_metrics = telemetry_section.get("metrics")
            summary_warnings = list(summary_payload.get("warnings", []) or [])

        _log_collection_completion(
            collection_name,
            models_executed,
            lease_events,
            elapsed,
            summary_path=summary_path_str,
            summary_payload=summary_payload,
            metrics_report=telemetry_metrics,
            warnings=summary_warnings,
        )
        
        # Return success result
        effective_chunk_count = chunk_total if isinstance(chunk_total, int) else len(chunk_files)

        return CollectionResult(
            collection_name=collection_name,
            chunk_count=effective_chunk_count,
            embedding_count=embedding_count,
            models_executed=models_executed,
            elapsed_seconds=elapsed,
            success=True,
            lease_events=lease_events,
            processing_summary_path=summary_path_str,
            processing_summary=summary_payload,
            metrics_report=telemetry_metrics,
            warnings=summary_warnings,
        )
        
    except Exception as exc:
        # Calculate elapsed time for failed processing
        elapsed = time.time() - start_time
        
        # Log error with traceback
        LOGGER.error(
            f"Failed to process collection '{collection_name}': {exc}",
            exc_info=True
        )
        
        # Return failure result
        return CollectionResult(
            collection_name=collection_name,
            chunk_count=0,
            embedding_count=0,
            models_executed=[],
            elapsed_seconds=elapsed,
            success=False,
            error_message=str(exc),
        )


# ============================================================================
# Main entry point
# ============================================================================

# Default fallback model if ensemble_models is empty
DEFAULT_FALLBACK_MODEL = "jina-code-embeddings-1.5b"


def _filter_collections(
    all_collections: Dict[str, Path],
    requested_names: Optional[List[str]],
) -> Dict[str, Path]:
    """
    Filter collections to only those requested by user.
    
    Args:
        all_collections: All discovered collections
        requested_names: Specific collection names to process, or None for all
        
    Returns:
        Filtered collections dict
        
    Raises:
        ValueError: If requested collections not found
    """
    if not requested_names:
        return all_collections
    
    filtered = {
        name: path
        for name, path in all_collections.items()
        if name in requested_names
    }
    
    if not filtered:
        raise ValueError(
            f"None of the requested collections found: {requested_names}. "
            f"Available: {list(all_collections.keys())[:10]}..."
        )
    
    return filtered


def _initialize_embedder(
    args: argparse.Namespace,
    output_dir: Path,
) -> UltimateKaggleEmbedderV4:
    """
    Initialize embedder with configuration from arguments.
    
    Args:
        args: Parsed command-line arguments
        output_dir: Output directory for embeddings
        
    Returns:
        Configured embedder instance
        
    Raises:
        RuntimeError: If embedder initialization fails
    """
    try:
        # Configure ensemble
        ensemble_config = EnsembleConfig(
            ensemble_models=args.ensemble_models,
            exclusive_mode=args.exclusive_ensemble,
        )
        
        # Configure GPU
        gpu_config = KaggleGPUConfig(
            kaggle_environment=KAGGLE_ENV,
            output_path=str(output_dir),
        )
        
        # Configure export
        export_config = KaggleExportConfig(
            working_dir=str(output_dir),
            output_prefix="v6_embeddings",
        )
        
        # Determine primary model
        primary_model = (
            args.ensemble_models[0]
            if args.ensemble_models
            else DEFAULT_FALLBACK_MODEL
        )
        
        # Initialize embedder
        toggle_config = FeatureToggleConfig(
            enable_rerank=args.enable_rerank,
            enable_sparse=args.enable_sparse,
            sparse_models=args.sparse_models,
            sources=args.toggle_sources,
            resolution_events=getattr(args, "toggle_resolution_events", ()),
        )

        embedder = UltimateKaggleEmbedderV4(
            model_name=primary_model,
            enable_ensemble=True,  # Required for exclusive mode
            ensemble_config=ensemble_config,
            gpu_config=gpu_config,
            export_config=export_config,
            feature_toggles=toggle_config,
        )
        
        LOGGER.info("Embedder initialized successfully")
        return embedder
        
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize embedder: {exc}") from exc


def _log_processing_summary(
    collection_results: List[CollectionResult],
) -> None:
    """
    Log summary of collection processing results.
    
    Args:
        collection_results: List of all collection processing results
    """
    LOGGER.info("\n" + "="*80)
    LOGGER.info("PROCESSING SUMMARY")
    LOGGER.info("="*80)
    
    successful = [r for r in collection_results if r.success]
    failed = [r for r in collection_results if not r.success]
    
    LOGGER.info(f"Total collections: {len(collection_results)}")
    LOGGER.info(f"Successful: {len(successful)}")
    LOGGER.info(f"Failed: {len(failed)}")
    
    if successful:
        LOGGER.info("\nSuccessful Collections:")
        for result in successful:
            LOGGER.info(f"  - {result.collection_name}:")
            LOGGER.info(f"      Chunks: {result.chunk_count}")
            LOGGER.info(f"      Embeddings: {result.embedding_count}")
            LOGGER.info(f"      Models: {result.models_executed}")
            LOGGER.info(f"      Time: {result.elapsed_seconds:.2f}s")
            if result.processing_summary_path:
                LOGGER.info(f"      Summary: {result.processing_summary_path}")
            if result.warnings:
                LOGGER.warning("      Warnings detected:")
                for warning in result.warnings:
                    LOGGER.warning(f"        - {warning}")
    
    if failed:
        LOGGER.info("\nFailed Collections:")
        for result in failed:
            LOGGER.info(f"  - {result.collection_name}: {result.error_message}")


def _export_summary_json(
    output_dir: Path,
    collection_results: List[CollectionResult],
    args: argparse.Namespace,
) -> Path:
    """
    Export processing summary to JSON file.
    
    Args:
        output_dir: Output directory
        collection_results: List of collection processing results
        args: Parsed command-line arguments
        
    Returns:
        Path to exported summary file
    """
    summary_path = output_dir / "embedding_summary_v6.json"
    
    successful = [r for r in collection_results if r.success]
    failed = [r for r in collection_results if not r.success]
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "environment": "kaggle" if KAGGLE_ENV else "local",
        "exclusive_mode": args.exclusive_ensemble,
        "ensemble_models": args.ensemble_models,
        "collections": [r.to_dict() for r in collection_results],
        "summary": {
            "total": len(collection_results),
            "successful": len(successful),
            "failed": len(failed),
        },
    }
    
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    
    return summary_path


def create_zip_archive(
    output_dir: Path,
    compression: str = "deflated"
) -> Path:
    """
    Create ZIP archive of all embeddings in the output directory.
    
    Archives all collection subdirectories and the summary JSON file
    into a single timestamped ZIP file for easy download. Includes
    manifest file listing all archived files with sizes, and verifies
    archive integrity after creation.
    
    Args:
        output_dir: Directory containing all collection outputs
        compression: Compression method ("deflated" or "stored")
        
    Returns:
        Path to created ZIP archive
        
    Raises:
        ValueError: If compression method is invalid
        OSError: If ZIP creation fails or integrity check fails
    """
    # Validate compression method
    compression_map = {
        "deflated": zipfile.ZIP_DEFLATED,
        "stored": zipfile.ZIP_STORED,
    }
    
    if compression not in compression_map:
        raise ValueError(
            f"Invalid compression method: {compression}. "
            f"Must be one of {list(compression_map.keys())}"
        )
    
    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"embeddings_{timestamp}.zip"
    zip_path = output_dir / zip_filename
    
    LOGGER.info(f"\nCreating ZIP archive: {zip_filename}")
    LOGGER.info(f"Compression: {compression}")
    
    # Create ZIP archive with manifest and verification
    try:
        # Step 1: Generate manifest by walking output directory
        LOGGER.info("Generating manifest...")
        manifest_lines = [
            "EMBEDDING ARCHIVE MANIFEST",
            "=" * 80,
            f"Generated: {datetime.now().isoformat()}",
            f"Compression: {compression}",
            "=" * 80,
            "",
            "FILES:",
            ""
        ]
        
        file_info_list = []
        total_uncompressed_size = 0
        
        for root, dirs, files in os.walk(output_dir):
            root_path = Path(root)
            
            for file in files:
                file_path = root_path / file
                
                # Skip the ZIP file itself if it exists
                if file_path == zip_path:
                    continue
                
                # Get file size
                file_size = file_path.stat().st_size
                total_uncompressed_size += file_size
                
                # Store info for manifest
                arcname = str(file_path.relative_to(output_dir))
                file_info_list.append((arcname, file_size))
        
        # Sort by path for consistent manifest
        file_info_list.sort(key=lambda x: x[0])
        
        # Format manifest entries
        for arcname, file_size in file_info_list:
            size_mb = file_size / (1024 * 1024)
            manifest_lines.append(f"  {arcname:<60} {size_mb:>10.2f} MB")
        
        # Add summary to manifest
        manifest_lines.extend([
            "",
            "=" * 80,
            "SUMMARY:",
            f"  Total files: {len(file_info_list)}",
            f"  Total size: {total_uncompressed_size / (1024 * 1024):.2f} MB",
            "=" * 80
        ])
        
        # Write manifest to output directory
        manifest_path = output_dir / "MANIFEST.txt"
        with open(manifest_path, "w") as f:
            f.write("\n".join(manifest_lines))
        
        LOGGER.info(f"  Files to archive: {len(file_info_list)}")
        LOGGER.info(f"  Total uncompressed: {total_uncompressed_size / (1024 * 1024):.2f} MB")
        
        # Check disk space before creating ZIP
        LOGGER.info("Checking disk space...")
        required_space = int(total_uncompressed_size * 1.1)  # 10% buffer
        disk_usage = shutil.disk_usage(output_dir)
        available_space = disk_usage.free
        
        if available_space < required_space:
            required_mb = required_space / (1024 * 1024)
            available_mb = available_space / (1024 * 1024)
            raise OSError(
                f"Insufficient disk space for ZIP creation. "
                f"Required: {required_mb:.2f} MB (with 10% buffer), "
                f"Available: {available_mb:.2f} MB"
            )
        
        LOGGER.info(
            f"  Available: {available_space / (1024 * 1024):.2f} MB, "
            f"Required: {required_space / (1024 * 1024):.2f} MB ✅"
        )
        
        # Step 2: Create ZIP archive
        LOGGER.info("Creating ZIP archive...")
        file_count = 0
        
        with zipfile.ZipFile(
            zip_path,
            mode='w',
            compression=compression_map[compression]
        ) as zipf:
            # Add manifest first
            zipf.write(manifest_path, arcname="MANIFEST.txt")
            file_count += 1
            LOGGER.debug(f"  Added: MANIFEST.txt")
            
            # Add all other files
            for arcname, _ in file_info_list:
                file_path = output_dir / arcname
                zipf.write(file_path, arcname=arcname)
                file_count += 1
                LOGGER.debug(f"  Added: {arcname}")
        
        # Step 3: Verify archive integrity
        LOGGER.info("Verifying archive integrity...")
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # Test ZIP integrity
            bad_file = zipf.testzip()
            if bad_file:
                raise OSError(f"Archive verification failed: corrupted file {bad_file}")
            
            # Verify file count
            archive_file_count = len(zipf.namelist())
            if archive_file_count != file_count:
                raise OSError(
                    f"File count mismatch: expected {file_count}, "
                    f"found {archive_file_count}"
                )
        
        # Step 4: Calculate metrics
        zip_size = zip_path.stat().st_size
        zip_size_mb = zip_size / (1024 * 1024)
        compression_ratio = (zip_size / total_uncompressed_size * 100) if total_uncompressed_size > 0 else 0
        
        # Log success metrics
        LOGGER.info("✅ Archive verification successful")
        LOGGER.info(f"  Files archived: {file_count}")
        LOGGER.info(f"  Archive size: {zip_size_mb:.2f} MB")
        LOGGER.info(f"  Compression ratio: {compression_ratio:.1f}%")
        LOGGER.info(f"  Space saved: {(total_uncompressed_size - zip_size) / (1024 * 1024):.2f} MB")
        
        return zip_path
        
    except Exception as exc:
        LOGGER.error(f"Failed to create ZIP archive: {exc}", exc_info=True)
        # Clean up partial ZIP file if it exists
        if zip_path.exists():
            zip_path.unlink()
        # Clean up manifest if it exists
        manifest_path = output_dir / "MANIFEST.txt"
        if manifest_path.exists():
            manifest_path.unlink()
        raise OSError(f"ZIP creation failed: {exc}") from exc


def main() -> int:
    """
    Main execution flow for collection embedding.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Parse arguments
    args = parse_arguments()
    
    # Setup paths
    chunked_dir = Path(args.chunked_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Log configuration
    LOGGER.info("="*80)
    LOGGER.info("Collection Embedding Runner V6 - Exclusive Ensemble Mode")
    LOGGER.info("="*80)
    LOGGER.info(f"Environment: {'Kaggle' if KAGGLE_ENV else 'Local'}")
    _log_toggle_resolution(getattr(args, "toggle_resolution_events", ()))
    LOGGER.info(f"Chunked directory: {chunked_dir}")
    LOGGER.info(f"Output directory: {output_dir}")
    LOGGER.info(f"Exclusive ensemble: {args.exclusive_ensemble}")
    LOGGER.info(f"Ensemble models: {args.ensemble_models}")
    LOGGER.info(
        "Feature toggles: rerank=%s sparse=%s sparse_models=%s (sources=%s)",
        args.enable_rerank,
        args.enable_sparse,
        args.sparse_models if args.sparse_models else "none",
        args.toggle_sources,
    )
    LOGGER.info("="*80 + "\n")
    
    # Discover collections
    all_collections = discover_collections(chunked_dir)
    
    if not all_collections:
        LOGGER.error("No collections discovered. Exiting.")
        return 1
    
    # Filter to requested collections
    try:
        collections_to_process = _filter_collections(
            all_collections,
            args.collections
        )
    except ValueError as exc:
        LOGGER.error(str(exc))
        return 1
    
    LOGGER.info(f"Collections to process: {list(collections_to_process.keys())}\n")
    
    # Initialize embedder
    try:
        embedder = _initialize_embedder(args, output_dir)
    except RuntimeError as exc:
        LOGGER.error(str(exc), exc_info=True)
        return 1
    
    # Process each collection
    collection_results: List[CollectionResult] = []
    
    for idx, (collection_name, collection_path) in enumerate(collections_to_process.items(), 1):
        LOGGER.info(
            f"\n[{idx}/{len(collections_to_process)}] "
            f"Starting collection: {collection_name}"
        )
        
        result = process_collection(
            collection_name=collection_name,
            collection_path=collection_path,
            embedder=embedder,
            output_dir=output_dir,
            exclusive_mode=args.exclusive_ensemble,
        )
        
        collection_results.append(result)
    
    # Log summary
    _log_processing_summary(collection_results)
    
    # Export summary JSON
    try:
        summary_path = _export_summary_json(output_dir, collection_results, args)
        LOGGER.info(f"\nSummary exported to: {summary_path}")
    except Exception as exc:
        LOGGER.error(f"Failed to export summary: {exc}", exc_info=True)
        # Don't fail the whole run if just export fails
    
    # Create ZIP archive if requested
    zip_start_time = time.time()
    zip_path = None
    zip_size_mb = 0
    
    if args.create_zip:
        try:
            zip_path = create_zip_archive(
                output_dir=output_dir,
                compression=args.zip_compression
            )
            zip_elapsed = time.time() - zip_start_time
            zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
            
            LOGGER.info(f"\n✅ ZIP archive ready for download: {zip_path}")
            LOGGER.info(f"   ZIP creation time: {zip_elapsed:.2f}s")
        except Exception as exc:
            LOGGER.error(f"Failed to create ZIP archive: {exc}", exc_info=True)
            # Don't fail the whole run if just ZIP creation fails
    
    # Final summary report
    LOGGER.info("\n" + "="*80)
    LOGGER.info("FINAL SUMMARY")
    LOGGER.info("="*80)
    
    successful = [r for r in collection_results if r.success]
    total_embeddings = sum(r.embedding_count for r in successful)
    
    LOGGER.info(f"Collections exported: {len(successful)}/{len(collection_results)}")
    LOGGER.info(f"Total embeddings: {total_embeddings:,}")
    
    if zip_path:
        LOGGER.info(f"Archive size: {zip_size_mb:.2f} MB")
        LOGGER.info(f"Archive path: {zip_path}")
    
    LOGGER.info("="*80 + "\n")
    
    # Return success if all collections processed successfully
    failed = [r for r in collection_results if not r.success]
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

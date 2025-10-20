#!/usr/bin/env python3
"""
Batch Embedding Runner V5 - Optimized for V5 Unified Chunker Output

CHANGES FROM V4:
- Handles individual chunk files per document (new V5 structure)
- Preserves subdirectory hierarchy from chunking
- Better collection name detection from directory structure
- Improved file discovery with recursive glob
- Enhanced logging for V5 metadata fields
- Support for Matryoshka dimensions from chunker metadata

STRUCTURE:
Chunked/
  ├── Collection1/
  │   ├── subdir1/
  │   │   ├── doc1_chunks.json
  │   │   └── doc2_chunks.json
  │   └── subdir2/
  │       └── doc3_chunks.json

Compatible with processor/kaggle_ultimate_embedder_v4.py
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SENTINEL_PATH = REPO_ROOT / "output" / "STOP_AFTER_CHUNKING.flag"

IS_KAGGLE = Path("/kaggle").exists()

# Kaggle-friendly defaults
KAGGLE_DEFAULTS = {
    "chunks_root": Path("/kaggle/working/rag_clean/Chunked"),
    "output_root": Path("/kaggle/working/Embeddings"),
    "collections": [
        "Qdrant",
        "Sentence_Transformer",
        "Docling",
        "FAST_DOCS",
        "pydantic",
    ],
    "model": "jina-code-embeddings-1.5b",  # Primary ensemble model
    "matryoshka_dim": 1024,  # Ensemble dimension (all models configured at 1024D)
    "enable_ensemble": True,  # Multi-model ensemble enabled by default
    "skip_existing": True,
    "summary": "embedding_summary.json",
    "zip_output": True,
}

try:
    from processor.kaggle_ultimate_embedder_v4 import (
        EnsembleConfig,
        KaggleExportConfig,
        KaggleGPUConfig,
        UltimateKaggleEmbedderV4,
        KAGGLE_OPTIMIZED_MODELS,
    )
    from processor.chunk_utils import find_chunk_files
    print("✓ Successfully imported UltimateKaggleEmbedderV4")
except Exception as e:
    print(f"✗ CRITICAL: Failed to import embedder module: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

LOGGER = logging.getLogger("embedder_v5_batch")


@dataclass
class CollectionDiscovery:
    path: Path
    chunk_count: int


@dataclass
class CollectionRunResult:
    collection: str
    status: str
    chunks: Optional[int] = None
    performance: Optional[Dict[str, Any]] = None
    exports: Optional[Dict[str, str]] = None
    target_qdrant_collection: Optional[str] = None
    v5_metadata: Optional[Dict[str, Any]] = None
    archive: Optional[str] = None
    error: Optional[str] = None
    skip_reason: Optional[str] = None
    mitigation_events: Optional[List[Dict[str, Any]]] = None
    gpu_snapshot_summary: Optional[Dict[str, Any]] = None
    cache_events: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "collection": self.collection,
            "status": self.status,
        }
        if self.chunks is not None:
            payload["chunks"] = self.chunks
        if self.performance is not None:
            payload["performance"] = self.performance
        if self.exports is not None:
            payload["exports"] = self.exports
        if self.target_qdrant_collection is not None:
            payload["target_qdrant_collection"] = self.target_qdrant_collection
        if self.v5_metadata is not None:
            payload["v5_metadata"] = self.v5_metadata
        if self.archive is not None:
            payload["archive"] = self.archive
        if self.mitigation_events is not None:
            payload["mitigation_events"] = self.mitigation_events
        if self.gpu_snapshot_summary is not None:
            payload["gpu_snapshot_summary"] = self.gpu_snapshot_summary
        if self.cache_events is not None:
            payload["cache_events"] = self.cache_events
        if self.error is not None:
            payload["error"] = self.error
            if self.skip_reason is not None:
                payload["skip_reason"] = self.skip_reason
        return payload


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate embeddings for V5 unified chunker output across multiple collections.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    default_chunks_root = (
        str(KAGGLE_DEFAULTS["chunks_root"]) if IS_KAGGLE else str(Path.cwd() / "Chunked")
    )
    default_output_root = (
        str(KAGGLE_DEFAULTS["output_root"]) if IS_KAGGLE else str(Path.cwd() / "Embeddings")
    )

    parser.add_argument(
        "--chunks-root",
        default=default_chunks_root,
        help="Root directory containing per-collection chunk folders with subdirectories.",
    )
    parser.add_argument(
        "--output-root",
        default=default_output_root,
        help="Directory where exported embeddings and sidecars will be written.",
    )
    parser.add_argument(
        "--collections",
        nargs="*",
        help="Optional list of collection folder names to process. Defaults to autodiscovery.",
    )
    parser.add_argument(
        "--model",
        default=KAGGLE_DEFAULTS["model"] if IS_KAGGLE else "jina-code-embeddings-1.5b",
        help="Embedding model key defined in Kaggle embedder configuration.",
    )
    parser.add_argument(
        "--enable-ensemble",
        action="store_true",
        default=KAGGLE_DEFAULTS["enable_ensemble"] if IS_KAGGLE else False,
        help="Enable ensemble mode (requires ensemble config in embedder).",
    )
    parser.add_argument(
        "--ensemble-mode",
        choices=["auto", "parallel", "sequential", "disabled"],
        default="auto",
        help=(
            "Ensemble scheduling strategy: 'parallel' keeps legacy behavior, "
            "'sequential' runs models one after another to limit VRAM, and "
            "'disabled' turns off ensemble execution entirely. 'auto' defaults to "
            "sequential passes when ensemble mode is enabled."
        ),
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=KAGGLE_DEFAULTS["skip_existing"] if IS_KAGGLE else False,
        help="Skip collections that already have a .npy export in the target output directory.",
    )
    parser.add_argument(
        "--summary",
        default=KAGGLE_DEFAULTS["summary"] if IS_KAGGLE else "embedding_summary.json",
        help="Filename (relative to output root) for the run summary JSON file.",
    )
    parser.add_argument(
        "--zip-output",
        action="store_true",
        default=KAGGLE_DEFAULTS.get("zip_output", False) if IS_KAGGLE else True,
        help="Compress the output directory into a .zip archive for easier download.",
    )
    parser.add_argument(
        "--matryoshka-dim",
        type=int,
        default=KAGGLE_DEFAULTS.get("matryoshka_dim", 1024) if IS_KAGGLE else 1024,
        help="Matryoshka dimension for truncating embeddings (default: 1024 for ensemble compatibility).",
    )
    parser.add_argument(
        "--force-cpu",
        action="store_true",
        help="Force the embedder to execute on CPU even if CUDA is available.",
    )
    parser.add_argument(
        "--sequential-data-parallel",
        action="store_true",
        help="Wrap sequential ensemble passes with torch.nn.DataParallel when multiple GPUs are available.",
    )
    parser.add_argument(
        "--sequential-devices",
        help="Preferred device order for sequential ensemble (comma-separated, e.g., 'cuda:1,cuda:0,cpu').",
    )
    return parser.parse_args(argv)


def _discover_collections(
    root: Path, requested: Optional[List[str]]
) -> tuple[List[CollectionDiscovery], List[CollectionRunResult]]:
    """Discover V5 collections and capture skip metadata."""

    skipped: List[CollectionRunResult] = []

    if not root.exists():
        LOGGER.error("Chunks root %s does not exist", root)
        return [], []

    def evaluate_candidate(path: Path, source_name: str) -> Optional[CollectionDiscovery]:
        chunk_files = find_chunk_files(path)
        if chunk_files:
            LOGGER.info("  Found collection: %s (%d chunk files)", source_name, len(chunk_files))
            return CollectionDiscovery(path=path, chunk_count=len(chunk_files))

        LOGGER.warning("Skipping %s: no chunk files detected", source_name)
        skipped.append(
            CollectionRunResult(
                collection=source_name,
                status="skipped_no_chunks",
                chunks=0,
                skip_reason="no_chunk_files",
            )
        )
        return None

    discoveries: List[CollectionDiscovery] = []

    if requested:
        for name in requested:
            candidate = root / name
            if not candidate.exists() or not candidate.is_dir():
                LOGGER.warning("Requested collection %s not found under %s", name, root)
                skipped.append(
                    CollectionRunResult(
                        collection=name,
                        status="skipped_missing",
                        chunks=0,
                        skip_reason="not_found",
                    )
                )
                continue

            discovery = evaluate_candidate(candidate, name)
            if discovery:
                discoveries.append(discovery)
        return discoveries, skipped

    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or entry.name == "__pycache__":
            continue

        discovery = evaluate_candidate(entry, entry.name)
        if discovery:
            discoveries.append(discovery)

    return discoveries, skipped


def _have_existing_exports(output_dir: Path) -> bool:
    if not output_dir.exists():
        return False
    return any(output_dir.glob("*.npy"))


def _build_export_config(output_dir: Path, collection_name: str, model_name: str) -> KaggleExportConfig:
    output_dir.mkdir(parents=True, exist_ok=True)
    return KaggleExportConfig(
        export_numpy=True,
        export_jsonl=True,
        export_sparse_jsonl=True,
        export_faiss=True,
        compress_embeddings=True,
        working_dir=str(output_dir),
        output_prefix=f"{collection_name}_embedder_v5_{model_name}",
    )


def _zip_directory(source_dir: Path) -> Path:
    if not source_dir.exists():
        raise FileNotFoundError(f"Cannot zip missing directory: {source_dir}")

    archive_path = source_dir.with_suffix(".zip")
    if archive_path.exists():
        archive_path.unlink()

    archive_path = Path(
        shutil.make_archive(
            str(source_dir),
            "zip",
            root_dir=str(source_dir.parent),
            base_dir=source_dir.name,
        )
    )
    LOGGER.info("Created zip archive for %s at %s", source_dir.name, archive_path)
    return archive_path


def _run_for_collection(
    collection_dir: Path,
    export_dir: Path,
    model_name: str,
    enable_ensemble: bool,
    ensemble_mode: str,
    force_cpu: bool,
    sequential_data_parallel: bool,
    sequential_devices: Optional[List[str]],
    zip_output: bool,
    matryoshka_dim: int | None = None,
) -> CollectionRunResult:
    print(f"\n{'─'*80}")
    print(f"Initializing Embedder for Collection: {collection_dir.name}")
    print(f"{'─'*80}")
    
    export_config = _build_export_config(export_dir, collection_dir.name, model_name)
    gpu_config = KaggleGPUConfig()

    requested_mode = ensemble_mode or "auto"
    effective_enable = enable_ensemble
    if requested_mode == "disabled":
        effective_enable = False
    elif requested_mode in {"parallel", "sequential"}:
        effective_enable = True

    sequential_requested = False
    if effective_enable:
        if requested_mode == "sequential" or requested_mode == "auto":
            sequential_requested = True
    if requested_mode == "auto" and sequential_devices and effective_enable:
        sequential_requested = True

    ensemble_config: Optional[EnsembleConfig] = None
    if effective_enable:
        ensemble_config = EnsembleConfig()
        ensemble_config.sequential_passes = sequential_requested
        ensemble_config.parallel_encoding = not sequential_requested
        ensemble_config.sequential_data_parallel = sequential_data_parallel
        if sequential_devices:
            ensemble_config.preferred_devices = sequential_devices

    if requested_mode == "auto":
        display_mode = "sequential" if sequential_requested else ("parallel" if effective_enable else "disabled")
    else:
        display_mode = requested_mode

    print(f"\n1. Creating embedder instance...")
    print(f"   Primary model: {model_name}")
    print(f"   Ensemble scheduling: {display_mode}")
    print(f"   Force CPU: {'yes' if force_cpu else 'no'}")
    if matryoshka_dim:
        print(f"   Matryoshka dimension: {matryoshka_dim}")
    if sequential_devices:
        print(f"   Device order: {', '.join(sequential_devices)}")

    embedder = UltimateKaggleEmbedderV4(
        model_name=model_name,
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=effective_enable,
        ensemble_config=ensemble_config,
        matryoshka_dim=matryoshka_dim,
        force_cpu=force_cpu,
    )
    print(f"✓ Embedder instance created")

    primary_key = embedder.model_name
    expected_models: Set[str] = {primary_key}
    if embedder.enable_ensemble and embedder.ensemble_config:
        expected_models.update(embedder.ensemble_config.ensemble_models)
    if embedder.companion_models:
        expected_models.update(embedder.companion_models.keys())

    print(f"\n2. Model Availability Check:")
    print(f"   Expected models: {len(expected_models)}")
    model_lines = []
    missing_models: List[str] = []
    for name in sorted(expected_models):
        model_obj = (
            embedder.models.get(name)
            or embedder.companion_models.get(name)
        )
        config = KAGGLE_OPTIMIZED_MODELS.get(name)
        hf_id = config.hf_model_id if config else "unknown"
        vector_dim = config.vector_dim if config else "?"
        status = "✓ loaded" if model_obj is not None else "✗ MISSING"
        model_lines.append(f"   - {name}: {status}")
        model_lines.append(f"     └─ HF ID: {hf_id}")
        model_lines.append(f"     └─ Dimension: {vector_dim}D")
        if model_obj is None:
            missing_models.append(name)

    print(f"\n   ✓ PRIMARY MODEL: {primary_key}")
    if config := KAGGLE_OPTIMIZED_MODELS.get(primary_key):
        print(f"     └─ {config.hf_model_id} ({config.vector_dim}D)")
        
    if len(expected_models) > 1:
        print(f"\n   Additional models ({len(expected_models) - 1}):")
        for line in model_lines:
            if primary_key not in line or "loaded" not in line:
                print(line)
    
    if missing_models:
        print(f"\n   ⚠️  WARNING: {len(missing_models)} model(s) not loaded:")
        for missing in missing_models:
            print(f"     - {missing}")
        print(f"   This may affect ensemble quality if ensemble mode is enabled.")
    else:
        print(f"\n   ✓ All expected models loaded successfully")
    
    print(f"{'─'*80}\n")

    LOGGER.info(
        "Resolved embedder model=%s vector_dim=%s backend=%s matryoshka=%s",
        getattr(embedder, "model_name", "<unknown>"),
        getattr(getattr(embedder, "model_config", None), "vector_dim", "<unknown>"),
        getattr(embedder, "embedding_backend", "<unknown>"),
        matryoshka_dim if matryoshka_dim else "disabled",
    )
    
    print(f"3. Loading chunks from {collection_dir.name}...")

    # V5: The embedder's load_chunks_from_processing() already handles recursive .rglob()
    # for *_chunks.json files, so it will work with the new structure
    load_result = embedder.load_chunks_from_processing(str(collection_dir))
    total_chunks = load_result.get("total_chunks_loaded", 0)
    
    if total_chunks == 0:
        LOGGER.warning("Collection %s has no chunks; skipping", collection_dir.name)
        print(f"   ⚠️  No chunks found - skipping collection\n")
        return CollectionRunResult(
            collection=collection_dir.name,
            status="skipped_no_chunks",
            chunks=0,
            skip_reason="no_chunk_files",
        )
    
    print(f"   ✓ Loaded {total_chunks:,} chunks")

    # Log V5-specific metadata from chunks
    if embedder.chunks_metadata:
        first_meta = embedder.chunks_metadata[0]
        v5_fields = {
            "model_aware_chunking": first_meta.get("model_aware_chunking"),
            "chunker_version": first_meta.get("chunker_version"),
            "within_token_limit": first_meta.get("within_token_limit"),
            "estimated_tokens": first_meta.get("estimated_tokens"),
        }
        print(f"   V5 metadata: {v5_fields}")
        LOGGER.info(f"V5 Chunk Metadata: {v5_fields}")
    
    print(f"\n4. Generating embeddings...")
    perf = embedder.generate_embeddings_kaggle_optimized()
    print(f"   ✓ Generated {perf.get('total_embeddings_generated', 0):,} embeddings")
    print(f"   ✓ Speed: {perf.get('chunks_per_second', 0):.1f} chunks/sec")
    print(f"   ✓ Time: {perf.get('processing_time_seconds', 0):.2f}s")
    mitigation_events = perf.get("mitigation_events") or []
    if mitigation_events:
        print(f"   ✓ Mitigation events: {len(mitigation_events)} logged")
    gpu_snapshot_summary = perf.get("gpu_snapshot_summary")
    if gpu_snapshot_summary:
        peak = gpu_snapshot_summary.get("peak_allocation")
        if peak is not None:
            print(f"   ✓ Peak VRAM observed: {peak / (1024**3):.2f} GB")
    cache_events = perf.get("cache_events") or []
    if cache_events:
        print(f"   ✓ Cache events: {len(cache_events)} recorded")
    
    print(f"\n5. Exporting embeddings...")
    exports = embedder.export_for_local_qdrant()
    print(f"   ✓ Exported {len(exports)} file(s)")
    target_collection = embedder.get_target_collection_name()

    archive_path: Path | None = None
    if zip_output:
        try:
            archive_path = _zip_directory(export_dir)
        except Exception:
            LOGGER.exception("Failed to zip output for %s", collection_dir.name)

    summary = CollectionRunResult(
        collection=collection_dir.name,
        status="completed",
        chunks=total_chunks,
        performance=perf,
        exports=exports,
        target_qdrant_collection=target_collection,
        v5_metadata={
            "chunker_version": "v5_unified",
            "matryoshka_dim": matryoshka_dim,
            "chunk_files_processed": load_result.get("collections_loaded", 0),
        },
        archive=str(archive_path) if archive_path is not None else None,
        mitigation_events=mitigation_events or None,
        gpu_snapshot_summary=gpu_snapshot_summary,
        cache_events=cache_events or None,
    )

    del embedder
    torch.cuda.empty_cache()
    return summary


def main(argv: List[str]) -> int:
    print("=" * 80)
    print("ULTIMATE KAGGLE EMBEDDER V5 - BATCH RUNNER")
    print("Optimized for V5 Unified Chunker Output")
    print("=" * 80)
    
    if SENTINEL_PATH.exists():
        try:
            SENTINEL_PATH.unlink()
            print(f"✓ Removed sentinel file: {SENTINEL_PATH}")
            print("Continuing with embedding pipeline...")
        except Exception as e:
            print(
                f"⚠️ Warning: Could not remove sentinel file at {SENTINEL_PATH}: {e}\n"
                "Manual removal may be required if the pipeline fails."
            )

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    
    print(f"\n✓ Logging initialized")
    print(f"✓ Python executable: {sys.executable}")
    print(f"✓ Kaggle environment: {IS_KAGGLE}")
    print(f"✓ CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✓ CUDA device count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  - GPU {i}: {torch.cuda.get_device_name(i)}")
    print()

    print("Parsing command-line arguments...")
    args = _parse_args(argv)
    print(f"✓ Arguments parsed")
    
    chunks_root = Path(args.chunks_root).resolve()
    output_root = Path(args.output_root).resolve()
    print(f"✓ Chunks root: {chunks_root}")
    print(f"✓ Output root: {output_root}")
    
    if args.matryoshka_dim:
        print(f"✓ Matryoshka dimension: {args.matryoshka_dim}")

    sequential_devices: Optional[List[str]] = None
    if args.sequential_devices:
        sequential_devices = [device.strip() for device in args.sequential_devices.split(",") if device.strip()]
        if sequential_devices:
            print(f"✓ Sequential device preference: {sequential_devices}")
    
    print(f"Creating output directory...")
    output_root.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory ready")

    print(f"\nResolving collections to process...")
    requested_collections = args.collections
    if requested_collections is None and IS_KAGGLE:
        requested_collections = KAGGLE_DEFAULTS["collections"]

    print(f"Requested collections: {requested_collections}")
    print(f"Discovering collections in {chunks_root}...")
    
    try:
        collections, skipped_discoveries = _discover_collections(
            chunks_root, requested_collections
        )
        print(f"✓ Collection discovery complete")
    except Exception as e:
        print(f"✗ Collection discovery failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    if not collections:
        LOGGER.error("No collections found under %s", chunks_root)
        print(f"✗ No collections found!")
        print(f"   Chunks root exists: {chunks_root.exists()}")
        if chunks_root.exists():
            print(f"   Contents: {list(chunks_root.iterdir())[:10]}")
        return 1

    if skipped_discoveries:
        print(f"⚠️  {len(skipped_discoveries)} collection(s) skipped during discovery")
        for skipped in skipped_discoveries:
            reason = skipped.skip_reason or "unknown"
            print(f"   - {skipped.collection}: {reason}")
    LOGGER.info("Found %d collection(s) to embed", len(collections))
    print(f"✓ Found {len(collections)} collection(s):")
    for discovery in collections:
        print(f"   - {discovery.path.name} ({discovery.chunk_count} chunk files)")
    print()
    
    # Display model configuration information
    print(f"\nModel Configuration:")
    print(f"{'='*80}")
    print(f"Current embedding model: {args.model}")
    
    # Check if model is available in registry
    if args.model in KAGGLE_OPTIMIZED_MODELS:
        model_config = KAGGLE_OPTIMIZED_MODELS[args.model]
        print(f"✓ Model found in registry")
        print(f"  - HuggingFace ID: {model_config.hf_model_id}")
        print(f"  - Vector dimension: {model_config.vector_dim}")
        print(f"  - Max tokens: {model_config.max_tokens}")
        print(f"  - Batch size (recommended): {model_config.recommended_batch_size}")
        if args.matryoshka_dim:
            print(f"  - Matryoshka dimension: {args.matryoshka_dim} (truncated from {model_config.vector_dim})")
        print(f"  - Memory efficient: {model_config.memory_efficient}")
        print(f"  - Flash attention: {model_config.supports_flash_attention}")
    else:
        print(f"⚠️  Model '{args.model}' not found in KAGGLE_OPTIMIZED_MODELS registry")
        print(f"   Available models: {', '.join(KAGGLE_OPTIMIZED_MODELS.keys())}")
    
    # Display ensemble configuration if enabled
    if args.enable_ensemble:
        print(f"\n✓ Ensemble mode: ENABLED")
        print(f"  Multi-model embedding will be used for enhanced quality")
    else:
        print(f"\n  Ensemble mode: disabled (single model)")

    print(f"  Ensemble scheduling override: {args.ensemble_mode}")
    if args.force_cpu:
        print(f"  Force CPU execution: enabled")
    if args.sequential_data_parallel:
        print(f"  Sequential data parallel: enabled")
    if sequential_devices:
        print(f"  Sequential device order: {', '.join(sequential_devices)}")
    
    # Display all available models in registry
    print(f"\nAvailable models in registry ({len(KAGGLE_OPTIMIZED_MODELS)} total):")
    for model_key, model_cfg in KAGGLE_OPTIMIZED_MODELS.items():
        status = "✓ SELECTED" if model_key == args.model else "  available"
        print(f"  {status} - {model_key}")
        print(f"      {model_cfg.hf_model_id} ({model_cfg.vector_dim}D)")
    
    print(f"{'='*80}\n")

    run_summaries: List[CollectionRunResult] = list(skipped_discoveries)
    print(f"Starting to process {len(collections)} collection(s)...\n")

    for idx, discovery in enumerate(collections, 1):
        collection_dir = discovery.path
        print(f"\n{'='*80}")
        print(f"COLLECTION {idx}/{len(collections)}: {collection_dir.name}")
        print(f"{'='*80}")
        LOGGER.info("Processing collection %s", collection_dir)
        export_dir = output_root / collection_dir.name
        
        if args.skip_existing and _have_existing_exports(export_dir):
            LOGGER.info(
                "Skipping %s because exports already exist", collection_dir.name
            )
            run_summaries.append(
                CollectionRunResult(
                    collection=collection_dir.name,
                    status="skipped_existing",
                    chunks=discovery.chunk_count,
                    skip_reason="exports_exist",
                )
            )
            continue

        try:
            print(f"Initializing embedder for {collection_dir.name}...")
            summary = _run_for_collection(
                collection_dir=collection_dir,
                export_dir=export_dir,
                model_name=args.model,
                enable_ensemble=args.enable_ensemble,
                ensemble_mode=args.ensemble_mode,
                force_cpu=args.force_cpu,
                sequential_data_parallel=args.sequential_data_parallel,
                sequential_devices=sequential_devices,
                zip_output=args.zip_output,
                matryoshka_dim=args.matryoshka_dim,
            )
            print(f"✓ Collection {collection_dir.name} completed successfully")
            run_summaries.append(summary)
        except Exception as exc:
            print(f"✗ FAILED: Collection {collection_dir.name}")
            print(f"   Error: {exc}")
            LOGGER.exception("Embedding failed for %s", collection_dir.name)
            import traceback
            traceback.print_exc()
            run_summaries.append(
                CollectionRunResult(
                    collection=collection_dir.name,
                    status="failed",
                    error=str(exc),
                )
            )

    summary_path = output_root / args.summary
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump([item.to_dict() for item in run_summaries], handle, indent=2)
    LOGGER.info("Wrote summary to %s", summary_path)

    if args.zip_output:
        try:
            overall_archive = _zip_directory(output_root)
            LOGGER.info("Created aggregate zip archive at %s", overall_archive)
        except Exception:
            LOGGER.exception("Failed to zip overall output directory %s", output_root)

    failures = [item for item in run_summaries if item.status == "failed"]
    if failures:
        print(f"\n⚠️  {len(failures)} collection(s) failed")
        return 1

    print(f"\n✓ All collections processed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

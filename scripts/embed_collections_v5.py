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
from pathlib import Path
from typing import Dict, List

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
    "model": "jina-code-embeddings-1.5b",
    "enable_ensemble": True,
    "skip_existing": True,
    "summary": "embedding_summary.json",
    "zip_output": True,
}

try:
    from processor.kaggle_ultimate_embedder_v4 import (
        KaggleExportConfig,
        KaggleGPUConfig,
        UltimateKaggleEmbedderV4,
    )
    print("✓ Successfully imported UltimateKaggleEmbedderV4")
except Exception as e:
    print(f"✗ CRITICAL: Failed to import embedder module: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

LOGGER = logging.getLogger("embedder_v5_batch")


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
        default=None,
        help="Matryoshka dimension for truncating embeddings (e.g., 1536 for Jina models).",
    )
    return parser.parse_args(argv)


def _discover_collections(root: Path, requested: List[str] | None) -> List[Path]:
    """
    Discover collection directories in the V5 unified chunker output.
    
    V5 structure:
    Chunked/
      ├── Collection1/  <- Top-level collection directories
      │   ├── subdir1/
      │   │   ├── doc1_chunks.json
      │   │   └── doc2_chunks.json
      │   └── subdir2/
      
    """
    if requested:
        collections = []
        for name in requested:
            candidate = root / name
            if candidate.exists() and candidate.is_dir():
                collections.append(candidate)
            else:
                LOGGER.warning("Requested collection %s not found under %s", name, root)
        return collections

    if not root.exists():
        LOGGER.error("Chunks root %s does not exist", root)
        return []

    collections: List[Path] = []
    
    # V5: Look for top-level directories that contain chunk JSON files (recursively)
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "__pycache__":
            continue
        
        # Check if this directory or its subdirectories contain chunk files
        has_chunks = (
            any(entry.rglob("*_chunks.json")) or 
            any(entry.rglob("*chunks.json")) or
            any(entry.glob("*.json"))
        )
        
        if has_chunks:
            collections.append(entry)
            # Count files for logging
            chunk_files = list(entry.rglob("*_chunks.json"))
            LOGGER.info(f"  Found collection: {entry.name} ({len(chunk_files)} chunk files)")
    
    return collections


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
    zip_output: bool,
    matryoshka_dim: int | None = None,
) -> Dict[str, object]:
    export_config = _build_export_config(export_dir, collection_dir.name, model_name)
    gpu_config = KaggleGPUConfig()

    embedder = UltimateKaggleEmbedderV4(
        model_name=model_name,
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=enable_ensemble,
        matryoshka_dim=matryoshka_dim,  # V5: Support Matryoshka dimensions
    )
    
    LOGGER.info(
        "Resolved embedder model=%s vector_dim=%s backend=%s matryoshka=%s",
        getattr(embedder, "model_name", "<unknown>"),
        getattr(getattr(embedder, "model_config", None), "vector_dim", "<unknown>"),
        getattr(embedder, "embedding_backend", "<unknown>"),
        matryoshka_dim if matryoshka_dim else "disabled",
    )

    # V5: The embedder's load_chunks_from_processing() already handles recursive .rglob()
    # for *_chunks.json files, so it will work with the new structure
    load_result = embedder.load_chunks_from_processing(str(collection_dir))
    total_chunks = load_result.get("total_chunks_loaded", 0)
    
    if total_chunks == 0:
        LOGGER.warning("Collection %s has no chunks; skipping", collection_dir.name)
        return {
            "collection": collection_dir.name,
            "status": "skipped_no_chunks",
            "chunks": 0,
        }

    # Log V5-specific metadata from chunks
    if embedder.chunks_metadata:
        first_meta = embedder.chunks_metadata[0]
        v5_fields = {
            "model_aware_chunking": first_meta.get("model_aware_chunking"),
            "chunker_version": first_meta.get("chunker_version"),
            "within_token_limit": first_meta.get("within_token_limit"),
            "estimated_tokens": first_meta.get("estimated_tokens"),
        }
        LOGGER.info(f"V5 Chunk Metadata: {v5_fields}")

    perf = embedder.generate_embeddings_kaggle_optimized()
    exports = embedder.export_for_local_qdrant()
    target_collection = embedder.get_target_collection_name()

    archive_path: Path | None = None
    if zip_output:
        try:
            archive_path = _zip_directory(export_dir)
        except Exception:
            LOGGER.exception("Failed to zip output for %s", collection_dir.name)

    summary = {
        "collection": collection_dir.name,
        "status": "completed",
        "chunks": total_chunks,
        "performance": perf,
        "exports": exports,
        "target_qdrant_collection": target_collection,
        "v5_metadata": {
            "chunker_version": "v5_unified",
            "matryoshka_dim": matryoshka_dim,
            "chunk_files_processed": load_result.get("collections_loaded", 0),
        }
    }
    if archive_path is not None:
        summary["archive"] = str(archive_path)

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
        collections = _discover_collections(chunks_root, requested_collections)
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

    LOGGER.info("Found %d collection(s) to embed", len(collections))
    print(f"✓ Found {len(collections)} collection(s):")
    for col in collections:
        # Count chunk files in collection
        chunk_count = len(list(col.rglob("*_chunks.json")))
        print(f"   - {col.name} ({chunk_count} chunk files)")
    print()

    run_summaries: List[Dict[str, object]] = []
    print(f"Starting to process {len(collections)} collection(s)...\n")
    
    for idx, collection_dir in enumerate(collections, 1):
        print(f"\n{'='*80}")
        print(f"COLLECTION {idx}/{len(collections)}: {collection_dir.name}")
        print(f"{'='*80}")
        LOGGER.info("Processing collection %s", collection_dir)
        export_dir = output_root / collection_dir.name
        
        if args.skip_existing and _have_existing_exports(export_dir):
            LOGGER.info("Skipping %s because exports already exist", collection_dir.name)
            run_summaries.append({
                "collection": collection_dir.name,
                "status": "skipped_existing",
                "chunks": None,
            })
            continue

        try:
            print(f"Initializing embedder for {collection_dir.name}...")
            summary = _run_for_collection(
                collection_dir=collection_dir,
                export_dir=export_dir,
                model_name=args.model,
                enable_ensemble=args.enable_ensemble,
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
            run_summaries.append({
                "collection": collection_dir.name,
                "status": "failed",
                "error": str(exc),
            })

    summary_path = output_root / args.summary
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(run_summaries, handle, indent=2)
    LOGGER.info("Wrote summary to %s", summary_path)

    if args.zip_output:
        try:
            overall_archive = _zip_directory(output_root)
            LOGGER.info("Created aggregate zip archive at %s", overall_archive)
        except Exception:
            LOGGER.exception("Failed to zip overall output directory %s", output_root)

    failures = [item for item in run_summaries if item.get("status") == "failed"]
    if failures:
        print(f"\n⚠️  {len(failures)} collection(s) failed")
        return 1

    print(f"\n✓ All collections processed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Batch runner for Ultimate Kaggle Embedder V4 across multiple collections."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List

import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

IS_KAGGLE = Path("/kaggle").exists()

# Kaggle-friendly defaults so the notebook can invoke this module without a long CLI string.
KAGGLE_DEFAULTS = {
    "chunks_root": Path("/kaggle/input/rag_clean_chunked"),
    "output_root": Path("/kaggle/working/Embeddings"),
    "collections": [
        "qdrant_ecosystem",
        "sentence_transformers",
        "docling",
        "fast_docs",
        "pydantic",
    ],
    "model": "nomic-coderank",
    "enable_ensemble": True,
    "skip_existing": True,
    "summary": "embedding_summary.json",
}

from processor.kaggle_ultimate_embedder_v4 import (
    KaggleExportConfig,
    KaggleGPUConfig,
    UltimateKaggleEmbedderV4,
)

LOGGER = logging.getLogger("embedder_v4_batch")


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate embeddings for one or more chunked collections using the Kaggle V4 embedder.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    default_chunks_root = (
        str(KAGGLE_DEFAULTS["chunks_root"]) if IS_KAGGLE else str(Path.cwd() / "Chunked")
    )
    default_output_root = (
        str(KAGGLE_DEFAULTS["output_root"]) if IS_KAGGLE else str(Path("ultimate_embeddings_v4"))
    )

    parser.add_argument(
        "--chunks-root",
        default=default_chunks_root,
        help="Root directory containing per-collection chunk folders or individual chunk JSON files.",
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
        default=KAGGLE_DEFAULTS["model"] if IS_KAGGLE else "nomic-coderank",
        help="Embedding model key defined in Kaggle embedder configuration.",
    )
    parser.add_argument(
        "--enable-ensemble",
        action="store_true",
        default=KAGGLE_DEFAULTS["enable_ensemble"] if IS_KAGGLE else False,
        help="Enable ensemble mode defined inside the embedder (requires ensemble config).",
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
    return parser.parse_args(argv)


def _discover_collections(root: Path, requested: List[str] | None) -> List[Path]:
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

    if any(root.glob("*_chunks.json")):
        return [root]

    collections: List[Path] = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "__pycache__":
            continue
        if any(entry.glob("*_chunks.json")) or any(entry.glob("*.json")):
            collections.append(entry)
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
        output_prefix=f"{collection_name}_embedder_v4_{model_name}",
    )


def _run_for_collection(
    collection_dir: Path,
    export_dir: Path,
    model_name: str,
    enable_ensemble: bool,
) -> Dict[str, object]:
    export_config = _build_export_config(export_dir, collection_dir.name, model_name)
    gpu_config = KaggleGPUConfig()

    embedder = UltimateKaggleEmbedderV4(
        model_name=model_name,
        gpu_config=gpu_config,
        export_config=export_config,
        enable_ensemble=enable_ensemble,
    )

    load_result = embedder.load_chunks_from_processing(str(collection_dir))
    total_chunks = load_result.get("total_chunks_loaded", 0)
    if total_chunks == 0:
        LOGGER.warning("Collection %s has no chunks; skipping", collection_dir.name)
        return {
            "collection": collection_dir.name,
            "status": "skipped_no_chunks",
            "chunks": 0,
        }

    perf = embedder.generate_embeddings_kaggle_optimized()
    exports = embedder.export_for_local_qdrant()

    summary = {
        "collection": collection_dir.name,
        "status": "completed",
        "chunks": total_chunks,
        "performance": perf,
        "exports": exports,
    }

    del embedder
    torch.cuda.empty_cache()
    return summary


def main(argv: List[str]) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    args = _parse_args(argv)
    chunks_root = Path(args.chunks_root).resolve()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    requested_collections = args.collections
    if requested_collections is None and IS_KAGGLE:
        requested_collections = KAGGLE_DEFAULTS["collections"]

    collections = _discover_collections(chunks_root, requested_collections)
    if not collections:
        LOGGER.error("No collections found under %s", chunks_root)
        return 1

    LOGGER.info("Found %d collection(s) to embed", len(collections))

    run_summaries: List[Dict[str, object]] = []
    for collection_dir in collections:
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
            summary = _run_for_collection(
                collection_dir=collection_dir,
                export_dir=export_dir,
                model_name=args.model,
                enable_ensemble=args.enable_ensemble,
            )
            run_summaries.append(summary)
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.exception("Embedding failed for %s", collection_dir.name)
            run_summaries.append({
                "collection": collection_dir.name,
                "status": "failed",
                "error": str(exc),
            })

    summary_path = output_root / args.summary
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(run_summaries, handle, indent=2)
    LOGGER.info("Wrote summary to %s", summary_path)

    failures = [item for item in run_summaries if item.get("status") == "failed"]
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

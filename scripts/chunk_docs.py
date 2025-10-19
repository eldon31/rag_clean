#!/usr/bin/env python3
"""Batch chunk all collections under Docs using EnhancedUltimateChunkerV3.

This utility intentionally stops the processing pipeline after chunking so that
downstream embedding/export steps do not run automatically. When the script
finishes it writes a sentinel file under ``output/`` that other stages can use
to detect the halt condition.
"""

from __future__ import annotations

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("TRANSFORMERS_NO_TORCHVISION", "1")
os.environ.setdefault("TRANSFORMERS_NO_MPS", "1")

from processor.enhanced_ultimate_chunker_v3 import EnhancedUltimateChunkerV3

SENTINEL_PATH = PROJECT_ROOT / "output" / "STOP_AFTER_CHUNKING.flag"


def _normalise_collection_filter(collections: Iterable[str] | None) -> List[str] | None:
    if not collections:
        return None
    return [value.strip().lower() for value in collections if value.strip()]

def chunk_all_docs(
    docs_root: Path,
    output_root: Path,
    collections: Iterable[str] | None = None,
) -> list[str]:
    collection_map = {
        "docling": "docling",
        "FAST_DOCS": "fast_docs",
        "pydantic": "pydantic",
        "qdrant_ecosystem": "qdrant_ecosystem",
        "sentence_transformers_docs": "sentence_transformers",
    }

    chunker = EnhancedUltimateChunkerV3()
    output_root.mkdir(parents=True, exist_ok=True)

    filters = _normalise_collection_filter(collections)
    processed_collections: list[str] = []

    for folder_name, collection in collection_map.items():
        if filters and collection.lower() not in filters:
            continue

        input_dir = docs_root / folder_name
        if not input_dir.exists():
            print(f"⚠️ Skipping missing folder: {input_dir}")
            continue

        output_dir = output_root / collection
        output_dir.mkdir(parents=True, exist_ok=True)

        summary = chunker.process_directory_smart(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
        )
        print(
            f"✅ {folder_name} → {collection}: {summary['processed_files']} files, "
            f"{summary['total_chunks']} chunks, took {summary['processing_time']:.2f}s"
        )
        processed_collections.append(collection)

    return processed_collections


def _write_pipeline_sentinel(processed_collections: Iterable[str]) -> None:
    SENTINEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat()
    content = (
        "Chunking stage completed. Embedding intentionally halted.\n"
        f"Timestamp: {timestamp}\n"
        f"Collections: {', '.join(processed_collections) if processed_collections else 'none'}\n"
        "Remove this file when you are ready to continue with embedding.\n"
    )
    SENTINEL_PATH.write_text(content, encoding="utf-8")
    print(f"🛑 Pipeline halt sentinel written to {SENTINEL_PATH}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chunk documentation collections without triggering embedding.")
    parser.add_argument("--docs-root", default=str(PROJECT_ROOT / "Docs"), help="Root directory that contains documentation collections.")
    parser.add_argument("--output-root", default=str(PROJECT_ROOT / "Chunked"), help="Destination root for chunked output.")
    parser.add_argument("--collections", nargs="*", help="Optional subset of collection names to process (e.g. docling fast_docs).")
    args = parser.parse_args(argv)

    docs_root = Path(args.docs_root).resolve()
    output_root = Path(args.output_root).resolve()

    processed = chunk_all_docs(docs_root, output_root, args.collections)
    _write_pipeline_sentinel(processed)
    print("✅ Chunking pipeline finished. Embedding stage intentionally skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

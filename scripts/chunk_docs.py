#!/usr/bin/env python3
"""Batch chunk all collections under Docs using EnhancedUltimateChunkerV3."""

from __future__ import annotations

from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("TRANSFORMERS_NO_TORCHVISION", "1")
os.environ.setdefault("TRANSFORMERS_NO_MPS", "1")

from processor.enhanced_ultimate_chunker_v3 import EnhancedUltimateChunkerV3


def chunk_all_docs(docs_root: Path, output_root: Path) -> None:
    collection_map = {
        "docling": "docling",
        "FAST_DOCS": "fast_docs",
        "pydantic": "pydantic",
        "qdrant_ecosystem": "qdrant_ecosystem",
        "sentence_transformers_docs": "sentence_transformers",
    }

    chunker = EnhancedUltimateChunkerV3()
    output_root.mkdir(parents=True, exist_ok=True)

    for folder_name, collection in collection_map.items():
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


def main() -> None:
    docs_root = PROJECT_ROOT / "Docs"
    output_root = PROJECT_ROOT / "Chunked"

    chunk_all_docs(docs_root, output_root)


if __name__ == "__main__":
    main()

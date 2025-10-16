"""Kaggle-friendly embedding launcher for sentence_transformers_docs."""

import argparse
import os
import sys
from pathlib import Path


def _add_template_path() -> None:
    candidates = [
        Path(__file__).resolve().parents[1] / "src" / "templates",
        Path(__file__).resolve().parent / "templates",
        Path.cwd() / "src" / "templates",
    ]
    for candidate in candidates:
        if candidate.exists():
            sys.path.insert(0, str(candidate))


_add_template_path()

from embedder_template import UniversalEmbedder, EmbedderConfig  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Embed sentence_transformers_docs collection")
    default_input = os.getenv("EMBED_INPUT", "/kaggle/input/sentence-transformers-docs-chunked")
    default_output = os.getenv(
        "EMBED_OUTPUT",
        "outputs/embed/sentence_transformers_embeddings_768.jsonl",
    )
    parser.add_argument("--input", type=Path, default=Path(default_input))
    parser.add_argument("--output", type=Path, default=Path(default_output))
    parser.add_argument("--no-gpu", action="store_true")
    parser.add_argument("--single-gpu", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("KAGGLE GPU EMBEDDING: sentence_transformers_docs")
    print("=" * 60)
    print(f"Input directory:  {args.input}")
    print(f"Output file:      {args.output}")
    print()

    config = EmbedderConfig(
        collection_name="sentence_transformers_docs",
        input_path=args.input,
        output_path=args.output,
        use_gpu=not args.no_gpu,
        use_data_parallel=not args.single_gpu,
    )

    embedder = UniversalEmbedder(config)
    embedder.run()

    if config.output_path.exists():
        with open(config.output_path, "r", encoding="utf-8") as f:
            line_count = sum(1 for line in f if line.strip())
        print(f"JSONL VALIDATION: {line_count:,} records written to {config.output_path}")
        if line_count <= 1:
            print("WARNING: Expected multiple JSONL records. Inspect the output file before uploading.")

    print()
    print("=" * 60)
    print("EMBEDDING COMPLETE!")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"   Download: {config.output_path.resolve()}")
    print("   Kaggle: check the Output tab for the JSONL file")
    print()


if __name__ == "__main__":
    main()

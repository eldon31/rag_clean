#!/usr/bin/env python3
"""Delete Qdrant collections listed in an embedding summary."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Iterable, Set

from qdrant_client import QdrantClient

LOGGER = logging.getLogger("delete_collections")


def _collect_targets(summary_path: Path) -> Set[str]:
    if not summary_path.exists():
        raise FileNotFoundError(f"Summary file not found: {summary_path}")

    with summary_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    targets: Set[str] = set()
    if not isinstance(payload, list):
        return targets

    for entry in payload:
        if not isinstance(entry, dict):
            continue
        status = entry.get("status")
        if status not in {"completed", "failed", "skipped_existing"}:
            continue
        collection_name = entry.get("target_qdrant_collection") or entry.get("collection")
        if isinstance(collection_name, str) and collection_name.strip():
            targets.add(collection_name.strip())

    return targets


def delete_collections(host: str, port: int, collections: Iterable[str]) -> None:
    targets = {name.strip() for name in collections if isinstance(name, str) and name.strip()}
    if not targets:
        LOGGER.info("No valid collection names supplied; nothing to delete.")
        return

    client = QdrantClient(host=host, port=port)
    existing = {collection.name for collection in client.get_collections().collections}
    LOGGER.info("Found %d existing collections", len(existing))

    for collection in sorted(targets):
        if collection not in existing:
            LOGGER.info("Skipping missing collection: %s", collection)
            continue
        LOGGER.info("Deleting collection: %s", collection)
        client.delete_collection(collection)
        LOGGER.info("Deleted: %s", collection)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Delete Qdrant collections based on an embedding summary.")
    parser.add_argument("--summary", default="Embeddings/embedding_summary.json", help="Path to the embedding summary JSON file.")
    parser.add_argument("--host", default="localhost", help="Qdrant host")
    parser.add_argument("--port", type=int, default=6333, help="Qdrant port")
    parser.add_argument("--dry-run", action="store_true", help="List collections without deleting them.")
    parser.add_argument(
        "--collections",
        nargs="*",
        help="Explicit collection names to delete (overrides summary parsing).",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    summary_path = Path(args.summary).resolve()
    targets = set(args.collections or [])
    if not targets:
        targets = _collect_targets(summary_path)

    if not targets:
        LOGGER.warning("No collections found in summary %s", summary_path)
        return 0

    LOGGER.info("Collections to delete: %s", ", ".join(sorted(targets)))
    if args.dry_run:
        LOGGER.info("Dry run enabled; no deletions performed.")
        return 0

    delete_collections(args.host, args.port, targets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

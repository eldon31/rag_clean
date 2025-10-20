"""Shared helpers for discovering chunk JSON payloads."""
from __future__ import annotations

from pathlib import Path
from typing import List

__all__ = ["is_chunk_file", "find_chunk_files"]


def is_chunk_file(path: Path) -> bool:
    """Return True if the path looks like a chunk JSON export."""
    name = path.name.lower()
    return (
        path.is_file()
        and path.suffix == ".json"
        and "chunk" in name
        and not name.endswith("_processing_summary.json")
    )


def find_chunk_files(directory: Path) -> List[Path]:
    """Return all chunk JSON files contained in *directory* (recursively)."""
    if not directory.exists() or not directory.is_dir():
        return []

    files = {file.resolve(): file for file in directory.rglob("*.json") if is_chunk_file(file)}
    return sorted(files.values())

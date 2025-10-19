#!/usr/bin/env python3
"""Run all generated Qdrant upload scripts under a directory."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List

LOGGER = logging.getLogger("run_upload_scripts")


def _discover_upload_scripts(root: Path, collections: Iterable[str] | None) -> List[Path]:
    scripts: List[Path] = []
    if not root.exists():
        raise FileNotFoundError(f"Upload root not found: {root}")

    collection_filter = {name.strip() for name in collections} if collections else None

    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "__pycache__":
            continue
        if collection_filter and entry.name not in collection_filter:
            continue

        candidates = list(entry.glob("*_upload_script.py"))
        if not candidates:
            LOGGER.warning("No upload script found under %s", entry)
            continue
        scripts.append(candidates[0])

    return scripts


def _run_script(python_executable: str, script_path: Path, dry_run: bool) -> int:
    if dry_run:
        LOGGER.info("Dry run: would execute %s", script_path)
        return 0

    LOGGER.info("Running upload script: %s", script_path)
    result = subprocess.run([python_executable, str(script_path)], cwd=str(script_path.parent))
    if result.returncode != 0:
        LOGGER.error("Upload script failed (%d): %s", result.returncode, script_path)
    else:
        LOGGER.info("Upload script completed: %s", script_path)
    return result.returncode


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute all generated upload scripts in sequence.")
    parser.add_argument("--root", default="Embeddings", help="Root directory containing per-collection export folders.")
    parser.add_argument("--collections", nargs="*", help="Optional subset of collection folder names to execute.")
    parser.add_argument("--python", default=sys.executable, help="Python interpreter to use when running upload scripts.")
    parser.add_argument("--dry-run", action="store_true", help="List the scripts without executing them.")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    root = Path(args.root).resolve()
    scripts = _discover_upload_scripts(root, args.collections)

    if not scripts:
        LOGGER.warning("No upload scripts discovered under %s", root)
        return 0

    LOGGER.info("Discovered %d upload script(s)", len(scripts))

    failures = 0
    for script in scripts:
        rc = _run_script(args.python, script, args.dry_run)
        if rc != 0:
            failures += 1

    if failures:
        LOGGER.error("%d upload script(s) failed", failures)
        return 1

    LOGGER.info("All upload scripts completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

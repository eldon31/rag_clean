"""Regression guard for `processor/ultimate_embedder/core.py` size."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Dict

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = REPO_ROOT / "processor" / "ultimate_embedder" / "core.py"
BASELINE_PATH = (
    REPO_ROOT
    / "openspec"
    / "changes"
    / "refactor-ultimate-embedder-core"
    / "artifacts"
    / "core_executable_line_baseline.json"
)


def _collect_executable_line_numbers(tree: ast.AST) -> set[int]:
    executable_lines: set[int] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            if isinstance(node, ast.Expr):
                value = getattr(node, "value", None)
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    continue
            executable_lines.add(getattr(node, "lineno", -1))

    return {line for line in executable_lines if line > 0}


def _load_baseline() -> Dict[str, int]:
    with BASELINE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if "line_limit" in data:
        data["max_executable_lines"] = int(data["line_limit"])
    else:
        data["max_executable_lines"] = int(data["executable_lines"])
    return data


def _measure_core() -> Dict[str, int]:
    source = CORE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(CORE_PATH))
    executable_lines = _collect_executable_line_numbers(tree)

    return {
        "executable_lines": len(executable_lines),
        "total_lines": len(source.splitlines()),
    }


def test_core_executable_line_limit() -> None:
    baseline = _load_baseline()
    metrics = _measure_core()

    limit = baseline["max_executable_lines"]
    actual = metrics["executable_lines"]

    assert (
        actual <= limit
    ), f"core.py uses {actual} executable lines, which exceeds the enforced limit of {limit}"

"""Prototype executable-line counting tool for Task 1.3."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Dict, Set

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CORE_PATH = ROOT / "processor" / "ultimate_embedder" / "core.py"


def collect_executable_line_numbers(tree: ast.AST) -> Set[int]:
    executable_lines: Set[int] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            if isinstance(node, ast.Expr):
                value = getattr(node, "value", None)
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    continue
            executable_lines.add(getattr(node, "lineno", -1))

    return {line for line in executable_lines if line > 0}


def analyse_core_file() -> Dict[str, int]:
    source = CORE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(CORE_PATH))

    executable_lines = collect_executable_line_numbers(tree)
    total_lines = len(source.splitlines())

    return {
        "file": str(CORE_PATH),
        "total_lines": total_lines,
        "executable_lines": len(executable_lines),
    }


def main() -> None:
    results = analyse_core_file()
    target = Path(__file__).resolve().parent / "core_executable_line_baseline.json"

    with target.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)

    print(json.dumps(results, indent=2))
    print(f"Baseline written to {target}")


if __name__ == "__main__":
    main()

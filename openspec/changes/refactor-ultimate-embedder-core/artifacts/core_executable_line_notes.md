# Executable Line Baseline (Task 1.3)

- Script: `capture_core_executable_lines.py` parses `processor/ultimate_embedder/core.py` with Python's AST and counts unique line numbers associated with statement nodes, ignoring docstrings.
- Baseline totals (refactor branch, 2025-10-22 run):
  - `total_lines`: 1848
  - `executable_lines`: 946
- The executable line count is still above the 800-line budget. Pending Task 4.4 will wire this checker into CI so we can ratchet the limit downward as `core.py` continues to slim down.

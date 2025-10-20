## Context
- Batch orchestration lives in `scripts/embed_collections_v5.py` while per-collection execution resides in `processor/kaggle_ultimate_embedder_v4.py`.
- Discovery currently treats any directory with a `.json` file as a collection; this causes pointless embedder spins on empty folders.
- `load_chunks_from_processing` ignores the caller-supplied `chunks_dir` outside Kaggle by replacing it with a repository-specific absolute path, which blocks local testing.
- The runner builds its JSON summary by poking at embedder attributes instead of using a defined contract, making refactors risky.
- Unable to run `openspec list` / `openspec list --specs` in this environment; manual inspection confirmed no existing specs under `openspec/specs/`.

## Goals
1. Respect explicit chunk directory overrides on every platform while keeping Kaggle heuristics as fallbacks.
2. Limit discovery to directories that actually contain chunk payloads and explain when allow-listed names are skipped.
3. Establish a structured result object returned from `_run_for_collection` so the batch runner serialises consistent metadata.
4. Improve reliability around teardown/logging without changing public entry points.

## Non-Goals
- Renaming modules or splitting the embedder into multiple files (future work can revisit).
- Changing the CLI surface of `embed_collections_v5.py` or the public API of `UltimateKaggleEmbedderV4`.
- Adding new backend types (ONNX/TensorRT) or altering embedding math.

## Key Decisions
- **Result type**: Introduce a lightweight dataclass/`TypedDict` in `scripts/embed_collections_v5.py` (or a shared module) instead of a larger refactor. Keeps change minimal yet explicit.
- **Discovery helper**: Centralise the "is chunk directory" logic so the runner and embedder share the same criteria; ensures tests cover both.
- **Path precedence**: The explicit `chunks_dir` argument is always evaluated first. Heuristics run only if the directory is missing or lacks chunk JSON files.
- **Logging**: Use the existing `LOGGER` for warnings and ensure skip reasons are emitted once, avoiding noisy duplicate messages.

## Risks / Mitigations
- **False negatives in discovery**: If heuristics become too strict we might skip valid collections. Mitigate by covering nested JSON files and include tests with multiple depth levels.
- **Breaking Kaggle defaults**: Hard-coded fallbacks were masking configuration issues. We will document the new behaviour and keep the old Kaggle candidates in the heuristic list.
- **Summary schema changes**: Downstream tooling may parse the summary. We will keep existing keys and only add structure (e.g., typed container) while preserving field names.

## Open Questions
- Do we need to expose the structured result outside the script (e.g., for notebooks)? If yes, consider exporting helper from a shared module; otherwise keep local.
- Should we persist skip reasons alongside success/failure entries for historical metrics? Initial implementation will return reason strings in the summary for later use.

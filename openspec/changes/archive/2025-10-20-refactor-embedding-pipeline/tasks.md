## 1. Context Review
- [x] 1.1 Capture existing runner behaviour on a sample workspace (note expected outputs and skip handling)
- [x] 1.2 Confirm callers of `load_chunks_from_processing` (scripts/tests) so signature changes are avoided

## 2. Collection Discovery Improvements
- [x] 2.1 Add helper that validates a directory contains chunk JSON payloads (recursive `*_chunks.json` check)
- [x] 2.2 Update `_discover_collections` to use the helper and return metadata describing why entries were skipped
- [x] 2.3 Write unit tests covering nested chunk directories, empty folders, and allow-listed misses

## 3. Embedder Path Resolution
- [x] 3.1 Update `load_chunks_from_processing` so the supplied `chunks_dir` is honoured regardless of environment
- [x] 3.2 Refine `_resolve_chunks_directory` heuristics to fall back only when the explicit path is missing or empty
- [x] 3.3 Add regression tests (or lightweight fixtures) to prove local overrides work

## 4. Structured Run Result
- [x] 4.1 Introduce a small dataclass/TypedDict describing per-collection results returned from `_run_for_collection`
- [x] 4.2 Populate the new structure inside the embedder (collection name, chunk count, export paths, qdrant collection)
- [x] 4.3 Update the batch runner to serialise the structured result and to include skip/failure metadata deterministically

## 5. Reliability & Cleanup
- [x] 5.1 Ensure GPU cleanup (`torch.cuda.empty_cache`) and other teardown paths run inside `finally` blocks
- [x] 5.2 Centralise logging so warnings about missing chunks and skipped entries are consistent

## 6. Validation
- [x] 6.1 Run targeted unit tests and existing integration tests for the embedding pipeline
- [x] 6.2 Dry-run the batch runner against a small fixture to confirm summary output matches specification

### Status Notes
- All tasks complete; validation confirms embedder pipeline refactor matches specification.

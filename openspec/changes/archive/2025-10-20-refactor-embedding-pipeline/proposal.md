## Why
- `embed_collections_v5.py` currently queues directories even when they have no chunk payloads, which wastes Kaggle GPU cycles and produces confusing "0 chunks" logs mid-run.
- `UltimateKaggleEmbedderV4.load_chunks_from_processing` overwrites the caller-supplied directory on local runs with a repo-specific path, breaking local dry runs and automated tests.
- The batch runner has to reach into embedder internals to build a run summary, making future refactors brittle.

## What Changes
- Harden collection discovery so only directories containing `*_chunks.json` (recursively) are scheduled, and emit explicit skip metadata for allow-listed collections that have no chunks.
- Fix the embedder's path resolution so explicit `chunks_dir` overrides are honoured on every platform, falling back to heuristics only when the supplied path is missing.
- Introduce a small structured result object that the embedder returns, allowing the runner to serialise consistent status/metrics without scraping internal state.
- Opportunistic clean-up: align logging, ensure GPU resource cleanup runs on both success and failure paths, and factor discovery helpers so they are independently testable.

## Impact
- Specs: `embedding-pipeline` (new capability requirements defined in this change)
- Code: `scripts/embed_collections_v5.py`, `processor/kaggle_ultimate_embedder_v4.py`, plus new shared helper/result types as needed
- Tests: add focused unit coverage around discovery and path-resolution helpers
- No production migrations; Kaggle notebooks continue to invoke the same entry points

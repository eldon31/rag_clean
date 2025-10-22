## Why
Sequential ensemble runs still fight for shared GPU memory, forcing conservative batch sizes even when only one encoder is actively processing. Operators want the dual-T4 environment to run each ensemble model in an exclusive pass that can stretch batch sizes back toward the 12 GB soft ceiling without provoking CUDA OOM events while still keeping telemetry and docs truthful.

## What Changes
- Introduce an opt-in "exclusive ensemble" mode that leases both GPUs to the active model and stages other encoders off-device until their turn.
- Add a GPU lease helper to coordinate device ownership, cache eviction, and telemetry for lease start/stop across `processor/ultimate_embedder/*`.
- Refactor `BatchRunner.run` to iterate by model first, resetting adaptive hints and progress tracking each pass while attaching model identifiers to telemetry.
- Load ensemble models onto CPU when exclusive mode is enabled and hydrate them onto the leased GPUs inside the pass, rebuilding any DataParallel wrappers as leases flip.
- Extend config + CLI plumbing so operators can enable the mode explicitly, ensuring companion models and the reranker respect lease ownership, and update documentation plus embedding summaries accordingly.
- Expand telemetry to surface lease lifecycle events, exclusive occupancy, per-pass VRAM metrics, and enlarged batch hints, keeping progress output and run summaries consistent while documenting temporary embedding storage expectations.

## Impact
- Affected specs: `embedding-pipeline`
- Affected code: `processor/ultimate_embedder/core.py`, `processor/ultimate_embedder/batch_runner.py`, `processor/ultimate_embedder/model_manager.py`, `processor/ultimate_embedder/config.py`, telemetry plumbing, new GPU lease helper, CLI/config entry points, documentation/embedding summaries.
- Testing impact: add unit coverage for the lease helper, updated progress logic, and integration smoke tests validating device release and larger batch sizes in exclusive mode.

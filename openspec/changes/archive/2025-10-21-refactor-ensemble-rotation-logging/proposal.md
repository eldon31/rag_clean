## Why
The third ensemble encoder (`qwen3-embedding-0.6b`) is not invoked on the first two chunk batches when sequential ensemble mode runs through `UltimateKaggleEmbedderV4`. Missing visibility in both the runner (`scripts/embed_collections_v5.py`) and the embedder masks whether batches are being re-used or skipped, making it impossible to audit or fix rotation bugs that starve specific models.

## What Changes
- Instrument the sequential ensemble scheduler to emit deterministic per-batch, per-model telemetry so we can identify when a configured encoder is skipped or delayed.
- Refactor the ensemble execution loop to guarantee ordered participation for every configured encoder on every batch, preventing starvation of the newest model additions.
- Extend run summaries and console logs to surface the detailed telemetry for auditing and debugging Kaggle runs.

## Impact
- Affected specs: `embedding-pipeline`
- Affected code: `processor/kaggle_ultimate_embedder_v4.py`, `scripts/embed_collections_v5.py`

## Why
Running `scripts/embed_collections_v5.py` on Kaggle consistently crashes while processing large collections. The current embedder keeps ensemble models resident on the same GPU, never shrinks batch sizes after retries, and re-downloads Hugging Face assets without enforcing cache reuse. As a result the job hits CUDA out-of-memory errors after a few batches and the run aborts.

## What Changes
- Add adaptive GPU memory management so ensemble batches shrink or temporarily disable companion models before the run fails.
- Separate companion/ensemble models onto secondary devices when available and release weights between batches to keep the primary GPU usage capped at 12GB on Kaggle hardware.
- Enforce coordinated usage of both Kaggle GPUs so primary workloads prefer GPU 0 while companion models spill to GPU 1 automatically.
- Harden Hugging Face loading by enforcing local cache usage and extending timeout/retry handling so the job can run fully offline once assets are cached.
- Update the batch runner to surface deterministic failure metadata and to expose CLI switches for opting out of ensemble mode or forcing CPU fallbacks per collection.

## Impact
- Affected specs: embedding-pipeline
- Affected code: processor/kaggle_ultimate_embedder_v4.py, scripts/embed_collections_v5.py, potential helper modules for cache/device utilities

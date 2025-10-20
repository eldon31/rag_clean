## Context
Kaggle Jupyter notebook runs embed tens of thousands of V5 chunks using `UltimateKaggleEmbedderV4`. The current pipeline loads every ensemble model onto GPU 0, keeps them resident for the entire collection, and uses a static batch hint derived from model metadata. When large Qdrant collections (3k+ chunks) are processed with two heavyweight models, GPU 0 remains near 13 GB of allocated memory. Subsequent batches trigger CUDA OOM despite the embedder attempting to clear caches. We also observed repeated Hugging Face network timeouts because the loader issues HEAD/GET requests even when the artifacts (stored under `/root/.cache/huggingface/hub/...` such as `models--jinaai--jina-reranker-v3`) already exist on the Kaggle disk cache.

## Goals / Non-Goals
- Goals: proactively manage GPU memory pressure (including high-memory transformer blocks), keep primary GPU allocations below 12GB, allow graceful degradation (smaller batches or CPU) before aborting, honor local model caches by default, surface deterministic failure metadata to the runner, and distribute workload across both Kaggle GPUs when present.
- Non-Goals: redesign the entire ensemble framework, introduce new embedding models, or rework chunk discovery/export flows.

## Decisions
- Decision: measure available GPU memory before and after each batch, shrinking the next batch, enabling gradient checkpointing, or pausing companion models when free space drops below the configurable threshold tied to a 12GB ceiling on GPU 0. This avoids per-call OOM exceptions inside deep transformer blocks while keeping throughput reasonable.
- Decision: register companion models on secondary devices (`cuda:1`) when present, with mirrored CPU fallbacks when additional GPUs are absent, ensuring GPU 0 stays under the 12GB limit while GPU 1 handles spillover. This spreads memory consumption across the two T4s Kaggle provides.
- Decision: wrap Hugging Face `hf_hub_download` usage with an explicit cache path, configure `SentenceTransformer` to operate in `local_files_only` mode by default, and add retry/backoff that prefers local files and only goes online when the cache is empty. This eliminates repeated HEAD requests seen in the failure logs.
- Decision: extend the batch runner CLI with flags to disable ensemble mode and to force CPU-only execution so Kaggle users can recover quickly if hardware differs from the defaults.
- Decision: introduce a sequential ensemble execution mode that iterates heavy models one at a time, offloading each pass from GPU memory before loading the next while optionally wrapping the active model in `torch.nn.DataParallel` to exploit both T4s without retaining multiple parameter sets simultaneously.

## Risks / Trade-offs
- Smaller batch sizes may increase wall-clock time; mitigate by logging adjustments and allowing overrides.
- Offloading models between devices requires careful synchronization when aggregating embeddings; ensure tensors are copied back to CPU before fusion.
- Enforcing cache usage could mask stale model revisions; surface the cached revision hash so operators can intentionally refresh when needed.
- Strict 12GB limits on GPU 0 may trigger more frequent companion spillover to GPU 1, so add telemetry to verify the secondary device remains healthy.
- Sequential passes require repeated weight loads; monitor wall-clock impact and consider caching encoder state across iterations if the hit is unacceptable.

## Migration Plan
1. Introduce utility functions for GPU memory introspection and cache-aware model loading.
2. Update the embedder to use adaptive batch control, device routing, and cache enforcement.
3. Add runner flags and summary reporting for new degradation paths.
4. Validate on Kaggle by re-running the failed workload; document expected log lines for memory adjustments.

## Open Questions
- Should CPU fallbacks stream batches or process collections serially? (Default to batching with torch.no_grad and document throughput impact.)
- Do we need a persistent cache manifest to avoid re-downloading across Kaggle notebook sessions? (Investigate during implementation.)

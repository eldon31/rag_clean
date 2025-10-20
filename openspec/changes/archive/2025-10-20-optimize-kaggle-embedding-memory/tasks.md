## 1. Context Review
- [ ] 1.1 Capture baseline GPU memory metrics and failure logs by rerunning `scripts/embed_collections_v5.py` against the Qdrant collection on Kaggle.
- [ ] 1.2 Inventory current ensemble/companion model loading paths inside `UltimateKaggleEmbedderV4` (primary, companion, and reranker).

## 2. Adaptive GPU Management
- [x] 2.1 Add a GPU memory probe utility that reports free/total memory per device and exposes a low-memory threshold tied to a 12GB ceiling on GPU 0. (`processor/kaggle_ultimate_embedder_v4.py` `_collect_gpu_snapshots`)
- [x] 2.2 Update `generate_embeddings_kaggle_optimized` to shrink batch sizes and disable companion models when free memory falls below the threshold, keeping GPU 0 usage under 12GB. (`processor/kaggle_ultimate_embedder_v4.py` adaptive controller integration)
- [x] 2.3 Ensure companion models run on secondary GPUs when available and release their allocations between batches; fall back to CPU otherwise. (`processor/kaggle_ultimate_embedder_v4.py` companion device routing + per-batch release)
- [x] 2.4 Record mitigation telemetry so summaries can show when GPU 1 handled spillover or when CPU fallback occurred. (`processor/kaggle_ultimate_embedder_v4.py` `_record_mitigation`, companion loader events)
- [x] 2.5 Evaluate gradient checkpointing or layer-wise streaming for transformer-heavy models (e.g., Qwen2) to prevent mid-forward OOM within ensemble runs. (Gradient checkpoint telemetry & auto-enable via `_maybe_enable_transformer_checkpointing`)

## 3. Cache-First Model Loading
- [x] 3.1 Wrap Hugging Face downloads with explicit cache paths (default `/root/.cache/huggingface/hub`) and retries that prefer local artifacts before hitting the network. (`processor/kaggle_ultimate_embedder_v4.py` `_ensure_model_snapshot`)
- [x] 3.2 Expose CLI/environment knobs so users can force offline mode or refresh the cache when necessary. (`processor/kaggle_ultimate_embedder_v4.py` initializer flags `local_files_only`, `refresh_cache`)
- [x] 3.3 Configure `SentenceTransformer` and other model loaders to request `local_files_only` assets when cached, preventing repeated HEAD calls that trigger Kaggle timeouts. (`processor/kaggle_ultimate_embedder_v4.py` `_build_sentence_transformer_kwargs`)
- [x] 3.4 Add diagnostics so the runner surfaces which models were loaded from cache vs downloaded, and warn cleanly when a companion model (e.g., `jina-embeddings-v4`) is missing while ensemble mode is enabled. (`processor/kaggle_ultimate_embedder_v4.py` `_initialize_companion_models` logging + `self.cache_events`)

## 4. Runner Enhancements
- [x] 4.1 Extend `scripts/embed_collections_v5.py` with flags to disable ensemble mode and to force CPU execution per collection.
- [x] 4.2 Update run summaries to record when adaptive batching, device reassignment, or cache fallbacks occur.

## 5. Validation
- [ ] 5.1 Add unit coverage for the new GPU probe logic and adaptive batching decisions.
- [ ] 5.2 Execute the Kaggle notebook workflow end-to-end, confirming the Qdrant collection completes without CUDA OOM and that summaries capture mitigation details.

## 6. Sequential Ensemble Scheduling
- [x] 6.1 Introduce `EnsembleConfig.sequential_passes` flag and environment/CLI overrides to toggle sequential execution. (See `plan/upgrade-sequential-ensemble-1.md`)
- [x] 6.2 Refactor `UltimateKaggleEmbedderV4.generate_ensemble_embeddings` to run ensemble models in sequential passes with post-pass teardown and optional `torch.nn.DataParallel` wrapping. (See `plan/upgrade-sequential-ensemble-1.md`)
- [x] 6.3 Persist per-pass mitigation telemetry (`ensemble_pass_completed`, device, duration) and ensure aggregation outputs remain parity-tested against simultaneous mode. (See `plan/upgrade-sequential-ensemble-1.md`)

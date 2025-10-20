## ADDED Requirements
### Requirement: Adaptive GPU Embedding Execution
The Kaggle embedder (`processor/kaggle_ultimate_embedder_v4.py`) SHALL monitor free GPU memory before and after each batch, SHALL keep GPU 0 allocations under 12GB, and MUST proactively shrink batch sizes, pause companion models, or relocate them to alternate devices when remaining memory drops below the configured safety margin. When additional GPUs are unavailable, the embedder SHALL fall back to CPU execution for companion models instead of aborting the run with an out-of-memory error, and when GPU 1 is available it MUST be used for companion workloads before reverting to CPU.

#### Scenario: Batch size reduction prevents OOM
- **GIVEN** the embedder observes free memory falling below the configured safety margin on the active GPU
- **WHEN** the next batch is prepared
- **THEN** the embedder reduces the per-batch chunk count and continues processing without raising a CUDA out-of-memory exception

#### Scenario: Transformer mitigation avoids crash
- **GIVEN** ensemble mode invokes a transformer model that previously triggered CUDA OOM during forward (e.g., Qwen2 MLP block)
- **WHEN** the embedder detects high memory pressure mid-forward
- **THEN** it applies configured mitigation (such as gradient checkpointing or layer-wise streaming) and completes the batch without aborting the run

#### Scenario: Companion model CPU fallback
- **GIVEN** ensemble mode is enabled but no secondary GPU has sufficient free memory
- **WHEN** the embedder loads companion models
- **THEN** it places the companion models on CPU and aggregates their embeddings without terminating the collection run

#### Scenario: Companion model uses GPU 1
- **GIVEN** ensemble mode is enabled and both Kaggle GPUs are available
- **WHEN** the embedder allocates companion models
- **THEN** it loads those models onto GPU 1 while maintaining GPU 0 usage below 12GB
- **AND** logs the spillover so the run summary records the dual-GPU execution

### Requirement: Cache-First Model Loading
The embedder SHALL resolve Hugging Face model assets using a cache-first strategy tuned for Kaggle Jupyter notebooks, reusing locally cached revisions (for example under `/root/.cache/huggingface/hub/`) whenever possible and only making network requests when the cache is absent or explicitly refreshed. Download retries MUST implement exponential backoff with informative logs so Kaggle runs remain stable under intermittent connectivity.

#### Scenario: Offline cache reuse
- **GIVEN** the required model artifacts already exist in the local Hugging Face cache
- **WHEN** the embedder initialises the model registry on Kaggle
- **THEN** it loads the artifacts from disk without issuing remote HEAD/GET requests
- **AND** the run proceeds even if external network access is unavailable

### Requirement: Sequential Ensemble Passes
The embedder SHALL expose a sequential ensemble mode that executes each configured ensemble model in isolated passes, ensuring only one heavyweight encoder occupies GPU memory at a time, and SHOULD wrap the active model with data parallelism when multiple Kaggle GPUs are present. After each pass, the embedder MUST release GPU allocations before loading the next model and MUST emit telemetry describing the pass duration, device, and aggregation weight applied.

#### Scenario: Sequential rotation avoids VRAM spikes
- **GIVEN** ensemble mode is enabled with three large models and sequential mode is active
- **WHEN** the embedder processes a chunk batch
- **THEN** it loads exactly one ensemble model onto GPU memory, encodes the batch, releases the model with `torch.cuda.empty_cache()`, and proceeds to the next model without exceeding the 12GB GPU 0 limit

#### Scenario: Aggregation parity maintained
- **GIVEN** sequential mode completes all ensemble passes for a batch
- **WHEN** the embeddings are aggregated
- **THEN** the combined vector matches the weighting semantics of simultaneous ensemble mode within tolerance and the telemetry records `ensemble_pass_completed` events for each model

## MODIFIED Requirements
### Requirement: Structured Run Summary
The batch runner script (`scripts/embed_collections_v5.py`) MUST emit a structured JSON summary describing each collection processed (or skipped) and the embedder (`processor/kaggle_ultimate_embedder_v4.py`) MUST surface the data needed to populate that summary without additional scraping. The summary SHALL include mitigation metadata whenever adaptive batching, device reassignment, or cache fallbacks are triggered during the run.

#### Scenario: Successful run summary emission
- **WHEN** a collection completes successfully
- **THEN** the saved summary item includes `status="completed"`, the total chunk count, export artifact paths, and the resolved Qdrant collection name
- **AND** the overall summary file is written to the requested location

#### Scenario: Mitigation metadata recorded
- **GIVEN** the embedder adjusts batch sizes, moves models between devices, or relies on cached Hugging Face artifacts during execution
- **WHEN** the run summary is generated
- **THEN** the summary entry for that collection records the mitigation actions and any residual warnings so operators can audit the adjustments

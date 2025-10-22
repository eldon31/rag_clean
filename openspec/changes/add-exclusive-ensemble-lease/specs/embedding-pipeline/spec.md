## ADDED Requirements
### Requirement: Exclusive Ensemble Configuration
The embedder MUST expose an opt-in configuration flag and CLI switch that enables exclusive ensemble leasing for whole-collection passes. When disabled, existing sequential behaviour SHALL remain unchanged. When enabled, the batch runner SHALL surface the mode in progress output (including the current model pass) and the run summary MUST record that exclusive ensemble processing occurred along with the enlarged batch hints and observed peak VRAM usage per pass.

#### Scenario: Operator enables exclusive mode
- **GIVEN** the operator launches `embed_collections_v5.py` with the exclusive ensemble flag enabled via config or CLI
- **WHEN** the embedder initialises the run
- **THEN** progress output and the run summary explicitly note that exclusive ensemble processing is active, display the current model pass plus target batch hint, and include initial VRAM projections for that lease

## MODIFIED Requirements
### Requirement: Sequential Ensemble Passes
The embedder SHALL expose a sequential ensemble mode that executes each configured ensemble model in isolated passes, ensuring only one heavyweight encoder occupies GPU memory at a time, and SHOULD wrap the active model with data parallelism when multiple Kaggle GPUs are present. After each pass, the embedder MUST release GPU allocations before loading the next model, MUST emit telemetry describing the pass duration, device, aggregation weight, model key, processed chunk identifiers, batch index, and observed VRAM usage, and MUST guarantee that every configured ensemble model processes every chunk batch in deterministic order without starvation. When exclusive ensemble mode is enabled, the embedder MUST lease both GPUs for the active model, stage all remaining ensemble, companion, and reranker models on CPU, and only hydrate them onto GPU inside the lease. The lease manager MUST flush CUDA caches, unwrap and recreate DataParallel wrappers as needed, manage temporary embedding storage (RAM or disk) until aggregation completes, and record lease start/end telemetry including the batch hint used for that pass. Upon lease release, GPU memory usage MUST return below the configured 12 GB safety ceiling before the next model acquires the devices.

#### Scenario: Lease ensures exclusive occupancy
- **GIVEN** exclusive ensemble mode is enabled for a run with three large models
- **WHEN** the first model acquires the GPU lease for a collection pass
- **THEN** both GPUs are reserved for that model, other ensemble and reranker models remain on CPU, and telemetry records the lease start event with the computed batch hint and current VRAM snapshot

#### Scenario: Sequential rotation avoids VRAM spikes
- **GIVEN** exclusive ensemble mode completes the first pass and the next model requests the lease
- **WHEN** the embedder transitions between models
- **THEN** it releases GPU memory to drop below the 12 GB safety ceiling, loads exactly one ensemble model onto GPU memory, and proceeds without exceeding the limit

#### Scenario: Aggregation parity maintained
- **GIVEN** sequential mode completes all ensemble passes for a batch (exclusive or standard)
- **WHEN** the embeddings are aggregated
- **THEN** the combined vector matches the weighting semantics of simultaneous ensemble mode within tolerance and the telemetry records `ensemble_pass_completed` events for each model

#### Scenario: Lease telemetry persisted
- **GIVEN** exclusive ensemble mode is running with three configured models
- **WHEN** the embedder iterates through a chunk batch
- **THEN** it emits telemetry entries for lease start/end including batch index, model key, chunk identifiers, pass duration, exclusive occupancy details, and peak VRAM values, and the order matches the deterministic rotation configured for the run

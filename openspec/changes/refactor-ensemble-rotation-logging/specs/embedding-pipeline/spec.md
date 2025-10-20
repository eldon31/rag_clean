## MODIFIED Requirements
### Requirement: Sequential Ensemble Passes
The embedder SHALL expose a sequential ensemble mode that executes each configured ensemble model in isolated passes, ensuring only one heavyweight encoder occupies GPU memory at a time, and SHOULD wrap the active model with data parallelism when multiple Kaggle GPUs are present. After each pass, the embedder MUST release GPU allocations before loading the next model, MUST emit telemetry describing the pass duration, device, aggregation weight, model key, processed chunk identifiers, and batch index, and MUST guarantee that every configured ensemble model processes every chunk batch in deterministic order without starvation.

#### Scenario: Sequential rotation avoids VRAM spikes
- **GIVEN** ensemble mode is enabled with three large models and sequential mode is active
- **WHEN** the embedder processes a chunk batch
- **THEN** it loads exactly one ensemble model onto GPU memory, encodes the batch, releases the model with `torch.cuda.empty_cache()`, and proceeds to the next model without exceeding the 12GB GPU 0 limit

#### Scenario: Aggregation parity maintained
- **GIVEN** sequential mode completes all ensemble passes for a batch
- **WHEN** the embeddings are aggregated
- **THEN** the combined vector matches the weighting semantics of simultaneous ensemble mode within tolerance and the telemetry records `ensemble_pass_completed` events for each model

#### Scenario: Rotation telemetry emitted
- **GIVEN** sequential ensemble mode is running with three configured models
- **WHEN** the embedder iterates through a chunk batch
- **THEN** it emits telemetry entries that include the batch index, model key, chunk identifiers, and pass duration for each model, and the order of entries matches the deterministic rotation order configured for the run

### Requirement: Structured Run Summary
The batch runner script (`scripts/embed_collections_v5.py`) MUST emit a structured JSON summary describing each collection processed (or skipped) and the embedder (`processor/kaggle_ultimate_embedder_v4.py`) MUST surface the data needed to populate that summary without additional scraping. The summary SHALL include mitigation metadata whenever adaptive batching, device reassignment, or cache fallbacks are triggered during the run, and MUST persist per-batch, per-model rotation telemetry so audits can confirm that every ensemble encoder participated in each batch.

#### Scenario: Successful run summary emission
- **WHEN** a collection completes successfully
- **THEN** the saved summary item includes `status="completed"`, the total chunk count, export artifact paths, and the resolved Qdrant collection name
- **AND** the overall summary file is written to the requested location

#### Scenario: Mitigation metadata recorded
- **GIVEN** the embedder adjusts batch sizes, moves models between devices, or relies on cached Hugging Face artifacts during execution
- **WHEN** the run summary is generated
- **THEN** the summary entry for that collection records the mitigation actions and any residual warnings so operators can audit the adjustments

#### Scenario: Rotation telemetry persisted
- **GIVEN** sequential ensemble mode executes multiple models for a collection
- **WHEN** the run summary file is written
- **THEN** the summary entry contains the per-batch telemetry emitted by the embedder, including the batch index, model key, chunk identifiers, and timing metadata for each pass

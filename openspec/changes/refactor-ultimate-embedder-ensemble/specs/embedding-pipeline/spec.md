## RENAMED Requirements
- FROM: `### Requirement: Sequential Ensemble Passes`
- TO: `### Requirement: Exclusive Ensemble Flow`

## MODIFIED Requirements
### Requirement: Exclusive Ensemble Flow
The Kaggle embedder SHALL execute ensemble encoding exclusively through the GPU leasing pipeline, ensuring that exactly one ensemble model occupies GPU memory at any given time. The public control surface MUST rely solely on `EnsembleConfig.exclusive_mode` (defaulting to enabled) for ensemble coordination, and legacy sequential or parallel branches SHALL be removed such that they cannot be invoked. The embedder MUST emit telemetry events documenting each lease acquisition and release so validation tests can assert the exclusive rotation order before the run summary is written, and configuration validation MUST fail if callers provide deprecated ensemble toggles.

#### Scenario: Exclusive leasing enforced
- **GIVEN** an ensemble run with two or more dense models configured
- **WHEN** the embedder processes a batch
- **THEN** it acquires a GPU lease for the active model, encodes the batch, releases the lease, and proceeds to the next model without invoking any parallel or sequential legacy path

#### Scenario: Legacy toggles rejected
- **GIVEN** a caller attempts to set removed ensemble flags (such as `sequential_passes`, `parallel_encoding`, or `memory_efficient`)
- **WHEN** the embedder initialises the ensemble configuration
- **THEN** it raises a descriptive configuration error before processing any chunks

#### Scenario: Telemetry confirms leases
- **GIVEN** the embedder runs an ensemble batch under exclusive mode
- **WHEN** telemetry is inspected after the batch completes
- **THEN** it contains matching `acquire` and `release` lease events for each ensemble model in the configured order

### Requirement: Lean Ensemble Configuration
The ensemble configuration schema SHALL expose only the fields required for the exclusive leasing flow and per-model weighting. Removed attributes (`parallel_encoding`, `weighting_strategy`, `aggregation_method`, `memory_efficient`, `sequential_passes`, `preferred_devices`, `warm_cache_after_release`) MUST no longer be present on the dataclass, and automated tests SHALL fail if any code attempts to access them. The embedder MUST also reject requests to enable dormant sparse runtime features via configuration or factory helpers.

#### Scenario: Removed fields inaccessible
- **GIVEN** a test imports `EnsembleConfig` from the modular package
- **WHEN** it attempts to access an attribute named `parallel_encoding`
- **THEN** Python raises an `AttributeError`, confirming the field is no longer part of the configuration surface

#### Scenario: Sparse runtime disabled
- **GIVEN** a caller tries to enable sparse runtime execution through `enable_sparse` or `ModelManager.initialize_sparse_models`
- **WHEN** the embedder initialises
- **THEN** it raises a descriptive error indicating sparse runtime is unsupported and does not register any sparse model loaders

## ADDED Requirements
### Requirement: Canonical Model Registry
The embedder MUST source dense encoder definitions exclusively from the `KAGGLE_OPTIMIZED_MODELS` registry. CLI entry points, batch runners, and tests SHALL resolve model keys against that registry, and attempts to reference unknown model identifiers MUST raise validation errors before execution begins.

#### Scenario: Registry lookup succeeds
- **GIVEN** a runner requests the `bge-m3` model key for an ensemble pass
- **WHEN** the embedder initialises models
- **THEN** it resolves the configuration from `KAGGLE_OPTIMIZED_MODELS` without consulting alternate registries and records the model metadata in telemetry

#### Scenario: Unknown model rejected
- **GIVEN** a caller specifies an ensemble model key that is absent from `KAGGLE_OPTIMIZED_MODELS`
- **WHEN** the embedder validates the configuration
- **THEN** it raises a configuration error prior to loading any models, preventing the run from starting

### Requirement: Dead Helper Retirement
The embedder package MUST remove the confirmed dead helpers tied to deprecated ensemble paths, including `progress.BatchProgressContext.to_dict`, `gpu_lease.GPULease.summarize`, `gpu_lease.GPULease.get_vram_delta_gb`, `throughput_monitor.ThroughputMonitor.log_error`, and the unused core helpers (`_get_model_primary_dtype`, `_save_intermediate_results`, `_generate_upload_script`, `_normalize_collection_name`). Reranker utilities (`set_cross_encoder_device`, `unload_reranker`, `get_device`) SHALL be deleted unless they are wired into an active pipeline, and specification tests MUST fail if those symbols are reintroduced without integration. CLI entry points MAY retain `core.main()` only when required for execution; otherwise the function SHALL be removed and the shim updated to match.

#### Scenario: Dead helper imports fail
- **GIVEN** a regression test attempts to import any of the removed helper functions
- **WHEN** the test executes under the refactored package
- **THEN** Python raises an `AttributeError` or `ImportError`, confirming the helpers are no longer exposed

#### Scenario: Reranker surface simplified
- **GIVEN** the reranker pipeline is imported after the refactor
- **WHEN** a test inspects its public API
- **THEN** only actively wired helpers remain available, and attempts to call `set_cross_encoder_device`, `unload_reranker`, or `get_device` either raise descriptive errors or are absent entirely

#### Scenario: CLI entry audit passes
- **GIVEN** the Kaggle embedding CLI script is executed or statically inspected
- **WHEN** the tooling verifies its entry point
- **THEN** it confirms `core.main()` is present only when invoked by a CLI command; if unused, the function is absent and the script relies on the updated exclusive ensemble orchestration

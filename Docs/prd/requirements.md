# Requirements

### Functional
1. FR1: System must load CrossEncoder and sparse models automatically on every execution while still honoring explicit opt-out switches in config or environment.
2. FR2: Batch Runner must orchestrate live sparse inference before export, capturing per-chunk vectors and falling back to metadata when inference fails.
3. FR3: CrossEncoder rerank stage must execute after dense+sparse fusion, producing ranked candidate lists plus rerank telemetry/export payloads.
4. FR4: CLI/config defaults must ship with rerank and sparse execution enabled, with documented parameters to disable for exceptional runs.
5. FR5: Export runtime must append rerank and sparse sections to manifests and JSONL artifacts without breaking legacy consumers or changing existing keys.
6. FR6: Telemetry subsystem must record spans and metrics for dense, sparse, and rerank stages, including GPU peak usage, latency, and fallback indicators.
7. FR7: System must enforce the 12 GB-per-GPU ceiling via adaptive batch sizing and leasing safeguards across dense, sparse, and rerank executions.
8. FR8: Rerank and sparse stages must reuse the existing `lease_gpus` manager to distribute work across leased devices when more than one GPU is available, retaining the exclusive ensemble flow while providing intra-stage data parallelism.

### Non Functional
1. NFR1: Enhancements must maintain backward-compatible outputs, keeping embedding-only runs identical when overrides turn off rerank and sparse stages.
2. NFR2: GPU memory usage must stay under 12 GB per device with automatic recovery steps (e.g., retry with smaller batches) when nearing the cap.
3. NFR3: Telemetry and exports must continue anonymizing sensitive text; no new fields may expose raw queries or PII.
4. NFR4: Rerank and sparse stages must keep total batch latency within +10% of the current exclusive ensemble SLA on Kaggle dual-T4 pipelines.
5. NFR5: Automated tests must cover enabled-default, fallback, and opt-out scenarios to guard against regressions in the dense-only path.

#### Rationale & Assumptions
These requirements mirror the architecture constraints (12 GB GPU limit, additive schemas, telemetry privacy) and your mandate that rerank/sparse run by default every execution. Leveraging the existing leasing and adaptive batching avoids inventing new orchestration while ensuring multi-GPU leases still provide throughput gains. Regression protections stay critical because defaults now enable new stages.

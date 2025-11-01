# Epic 3: CrossEncoder Rerank Execution & Telemetry

Expanded Goal: Activate the CrossEncoder rerank pipeline, ensuring it consumes fused candidates, records ranked outputs, and emits telemetry for latency, GPU usage, and fallback scenarios while respecting the 12 GB ceiling.

### Story 3.1 Build CrossEncoder Executor
As a rerank pipeline developer,
I want an executor that hydrates CrossEncoder models using GPU leasing,
so that rerank batches stay within memory limits while providing candidate scores.

#### Acceptance Criteria
1: Executor dynamically sizes batches to avoid 12 GB OOM and logs leasing events.
2: Unit tests simulate multi-GPU leases and OOM recovery paths.
3: Executor returns ranked results plus telemetry payload for downstream use.

### Story 3.2 Integrate Rerank Stage into Orchestration
As an orchestration engineer,
I want the rerank stage to run after dense+sparse fusion in the batch runner,
so that ranked candidates accompany export and telemetry surfaces without breaking flow.

#### Acceptance Criteria
1: Batch runner invokes rerank executor with fused candidates and records outcomes.
2: Fallback pathways capture when rerank disabled or fails, maintaining exports and logs.
3: End-to-end run demonstrates rerank-enabled exports and telemetry across default settings.

### Story 3.3 Telemetry and Observability Enhancements
As a telemetry consumer,
I want rerank-specific metrics (latency, GPU peak, fallback counts),
so that monitoring can detect issues with the new stage quickly.

#### Acceptance Criteria
1: Telemetry/metrics emit rerank-specific spans and Prometheus counters.
2: Runbook entries document interpreting rerank metrics and thresholds.
3: Alert thresholds or dashboards updated to include rerank performance indicators.

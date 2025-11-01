# Epic 2: Sparse Generator & Fusion Upgrade

Expanded Goal: Replace metadata echo with live sparse inference, integrate it into the exclusive ensemble flow using existing GPU leasing, and ensure fallbacks plus fusion logic preserve export correctness.

### Story 2.1 Implement Sparse Generator Module
As a pipeline developer,
I want a dedicated sparse generator that produces live vectors with fallback handling,
so that sparse retrieval data matches dense quality without manual workarounds.

#### Acceptance Criteria
1: New module executes sparse inference, returning vectors per chunk with metadata on fallback usage.
2: Unit tests cover happy path, inference failure, and fallback recovery.
3: GPU leasing support mirrors existing dense passes, including telemetry of device usage.

### Story 2.2 Integrate Sparse Stage into Batch Runner
As an orchestration engineer,
I want the batch runner to invoke live sparse inference before exports,
so that fused outputs include sparse vectors without disrupting the ensemble sequence.

#### Acceptance Criteria
1: Batch runner calls sparse generator after dense aggregation and before fusion/export.
2: Flow respects adaptive batch controller decisions and handles OOM mitigation via leasing.
3: Regression tests compare exports with sparse enabled vs. disabled, ensuring additive schema only.

### Story 2.3 Update Fusion and Export Consumers
As an export maintainer,
I want sparse vectors merged into downstream artifacts cleanly,
so that consumers receive additive sparse data with clear version signaling.

#### Acceptance Criteria
1: Fusion layer combines dense and sparse outputs without altering existing keys.
2: Export manifests/JSONL include sparse sections with version bump and documentation.
3: Legacy parsers ingest updated artifacts without errors when sparse data present.

# Epic 4: Export Schema, Regression Hardening, and Ensemble Documentation

Expanded Goal: Solidify durability by versioning exports, expanding regression coverage, and publishing the observed ensemble flow so future enhancements begin with accurate implementation knowledge.

### Story 4.1 Document Current Ensemble Flow

As a future maintainer,
I want a canonical document describing the actual ensemble execution path,
so that upcoming modifications reference real behavior rather than assumptions.

Deliverable: [`docs/architecture/ensemble-flow.md`](../architecture/ensemble-flow.md)

#### Acceptance Criteria

1: Documentation outlines end-to-end flow (CLI → embedder → leasing → adaptive control → fusion) with diagrams mirroring code.
2: Cross-references include `batch_runner.py`, `gpu_lease.py`, and related controllers.
3: Document lives in repo docs (e.g., `docs/architecture/ensemble-flow.md`) and links from PRD or runbooks.

### Story 4.2 Export Schema Versioning and Validation

As an export maintainer,
I want manifest and JSONL schemas versioned to include rerank/sparse payloads,
so that downstream tools parse enriched data safely.

- Implementation locks `processing_summary.json` to schema `v4.1`, adds
  `compatibility` metadata, and serializes stage payloads
  (`rerank_run.payload`, `sparse_run.payload`) with run identifiers for
  telemetry correlation while keeping legacy consumers functional.
- Regression coverage exercises v4.1 payloads alongside normalized v4.0
  manifests so validation utilities and CLI warnings surface discrepancies
  without breaking dense-only workflows.

#### Acceptance Criteria

1: Manifest bumped to v4.1 with optional rerank/sparse sections and documented schema changes.
2: Validation scripts/tests confirm legacy (v4.0) and new (v4.1) artifacts both parse.
3: Tooling emits warnings when rerank/sparse expected but absent, without breaking runs.

### Story 4.3 Regression Harness and Test Coverage Expansion

As a quality owner,
I want automated tests spanning default-on, fallback, and opt-out scenarios,
so that rerank/sparse changes do not regress dense-only behavior.

#### Acceptance Criteria

1: CI includes end-to-end sample corpus exercising rerank and sparse on CPU-friendly models.
2: Tests verify default-on outputs match expectations and opt-out paths match legacy results.
3: Performance baseline recorded for default-on runs to guard against >10% latency regression.

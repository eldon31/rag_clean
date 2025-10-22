---
goal: Add batch progress visibility for Ultimate Embedder runs
version: 1.0
date_created: 2025-10-22
last_updated: 2025-10-22
owner: Ultimate Embedder Working Group
status: Planned
tags: [feature, ultimate-embedder, observability]
---

# Introduction

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This plan delivers deterministic batch-progress signals during Ultimate Embedder runs so operators and automation can surface "Generating embeddings" progress with per-source batch labels in both logs and interactive terminals.

## 1. Requirements & Constraints

- **REQ-001**: Batch runners SHALL emit deterministic progress labels in the format `Batches(<primary_source>)` where `<primary_source>` is derived from chunk metadata in `processor/ultimate_embedder/core.py`.
- **REQ-002**: Embedding progress MUST expose total batch counts and current batch indexes to tqdm-compatible consumers invoked through `UltimateKaggleEmbedderV4._call_encode`.
- **REQ-003**: Telemetry outputs SHALL include the emitted progress label for every batch so structured summaries can reference the same identifier.
- **CON-001**: Do not introduce non-ASCII glyphs or emoji in progress labels to preserve log ingestion compatibility on Kaggle.
- **CON-002**: Maintain compatibility with CPU-only runs and ensure progress instrumentation does not require CUDA-specific APIs.
- **GUD-001**: Reuse existing `_get_batch_progress_label` and `_summarize_batch_sources` helpers where possible before creating new utilities.
- **PAT-001**: Follow existing telemetry pattern via `TelemetryTracker.record_batch_progress` (to be added within this change) instead of ad-hoc logging.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Capture consistent batch progress metadata inside core embedding loop.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Enumerate current batch iteration paths in `processor/ultimate_embedder/batch_runner.py` and document where `_call_encode` is invoked so progress hooks can attach without duplicating logic. |  |  |
| TASK-002 | Extend `UltimateKaggleEmbedderV4._call_encode` in `processor/ultimate_embedder/core.py` to accept mandatory `progress_context` payload (batch index, total batches, label) and thread it into tqdm kwargs. |  |  |
| TASK-003 | Add batch context construction helper in `BatchRunner.generate_ensemble_embeddings` and sequential loop to compute progress label via `_get_batch_progress_label` and determine total batch count before calling `_call_encode`. |  |  |

### Implementation Phase 2

- GOAL-002: Surface progress information to telemetry, logs, and user-facing outputs.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Introduce `TelemetryTracker.record_batch_progress` in `processor/ultimate_embedder/telemetry.py` and invoke it wherever `_call_encode` executes, storing batch index, total, and label. |  |  |
| TASK-005 | Ensure `processor/ultimate_embedder/monitoring.py` and `ExportRuntime` include progress label snapshots in mitigation summaries and run summaries without breaking existing schemas. |  |  |
| TASK-006 | Update `scripts/embed_collections_v5.py` to render the progress stream (e.g., stdout/tqdm) and pass through summary data when generating "4. Generating embeddings..." status text. |  |  |

### Implementation Phase 3

- GOAL-003: Validate behaviour via automated tests and documentation updates.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-007 | Add unit tests in `tests/test_batch_source_logging.py` and new `tests/test_batch_progress.py` covering label formatting, tqdm kwargs, and telemetry payloads. |  |  |
| TASK-008 | Extend integration test `tests/test_ensemble_rotation.py` (or new fixture) to assert sequential ensemble runs emit progress labels for each pass. |  |  |
| TASK-009 | Update documentation (`Docs/V5_TUTORIAL.md` and `Docs/EMBEDDING_SUMMARY_SCHEMA.md`) to describe new progress reporting semantics and run summary fields. |  |  |

## 3. Alternatives

- **ALT-001**: Emit progress labels only via logging without modifying tqdm integration; rejected because CLI users require live progress bars.
- **ALT-002**: Build an external wrapper script around `scripts/embed_collections_v5.py`; rejected because multiple entry points rely on internal progress hooks.

## 4. Dependencies

- **DEP-001**: tqdm library used by `SentenceTransformer.encode` for progress display; ensure version in environment exposes `tqdm_kwargs` parameter.
- **DEP-002**: Existing telemetry aggregation pipeline that reads mitigation events from `TelemetryTracker`.

## 5. Files

- **FILE-001**: `processor/ultimate_embedder/core.py` — extend `_call_encode` signature and progress handling.
- **FILE-002**: `processor/ultimate_embedder/batch_runner.py` — build batch progress context and invoke encode with labels.
- **FILE-003**: `processor/ultimate_embedder/telemetry.py` — add progress recording API.
- **FILE-004**: `processor/ultimate_embedder/monitoring.py` — surface progress data to monitoring exports.
- **FILE-005**: `scripts/embed_collections_v5.py` — expose progress messages during CLI runs.
- **FILE-006**: `Docs/EMBEDDING_SUMMARY_SCHEMA.md` — document new fields.
- **FILE-007**: `tests/test_batch_source_logging.py` and new `tests/test_batch_progress.py` — verify functionality.

## 6. Testing

- **TEST-001**: Unit test verifying `_get_batch_progress_label` and new helper emit expected label strings for single and multi-source batches.
- **TEST-002**: Unit test ensuring `_call_encode` attaches `tqdm_kwargs` with `desc` and progress total/current values when `progress_context` is provided.
- **TEST-003**: Integration test running `generate_embeddings_kaggle_optimized` on fixture data to assert telemetry captures batch progress entries for every batch.
- **TEST-004**: Documentation CI check (link checker) to validate updated docs render without broken anchors.

## 7. Risks & Assumptions

- **RISK-001**: Progress hook may conflict with third-party DataParallel wrappers; mitigate by feature-detecting `encode` kwargs before injection.
- **RISK-002**: Additional telemetry fields could inflate summary payloads beyond existing limits; mitigate by truncating labels to 80 characters and reusing payload limits.
- **ASSUMPTION-001**: Chunk metadata reliably contains `source_path` or equivalent fields for deriving primary label.

## 8. Related Specifications / Further Reading

- `openspec/specs/embedding-pipeline/spec.md`
- `openspec/changes/modularize-ultimate-embedder/proposal.md`

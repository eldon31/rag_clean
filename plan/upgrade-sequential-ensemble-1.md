---
goal: Sequential Ensemble Rotation for Kaggle Embeddings
version: 1.0
date_created: 2025-10-21
owner: Embedding Pipeline Team
status: Planned
tags: [feature, performance, kaggle]
---

# Introduction

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

Plan to execute Kaggle ensemble embeddings sequentially—one model per pass—to lower peak VRAM usage while keeping dual-T4 throughput via data parallel shards.

## 1. Requirements & Constraints

- **REQ-001**: Only one heavyweight ensemble model may occupy GPU memory at a time during sequential mode.
- **REQ-002**: Maintain deterministic aggregation parity with existing ensemble weighting logic.
- **REQ-003**: Preserve adaptive batching and mitigation telemetry per pass.
- **SEC-001**: No sensitive tokens or credentials may be logged when reporting per-pass telemetry.
- **CON-001**: Must run inside Kaggle T4x2 notebook limits (≤32GB combined VRAM).
- **GUD-001**: Reuse existing configuration patterns (env vars + CLI flags) for toggles.

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: Introduce configuration hooks for sequential ensemble scheduling.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Extend `processor/kaggle_ultimate_embedder_v4.py` `EnsembleConfig` with `sequential_passes: bool` defaulting to `False` and serialize to runner summaries. |  |  |
| TASK-002 | Plumb CLI/env overrides in `scripts/embed_collections_v5.py` (`--ensemble-mode sequential`, `EMBEDDER_SEQUENTIAL_ENSEMBLE=1`). |  |  |
| TASK-003 | Document new configuration knobs in `Docs/V5_DEPLOYMENT_GUIDE.md`. |  |  |

### Implementation Phase 2

- GOAL-002: Execute ensemble models sequentially with VRAM-safe lifecycle handling.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Refactor `UltimateKaggleEmbedderV4.generate_ensemble_embeddings` to iterate models sequentially, unloading weights between passes unless sharing the primary encoder. |  |  |
| TASK-005 | Implement per-pass device placement: prefer `cuda:1`, fall back to CPU, synchronize and `torch.cuda.empty_cache()` after each pass. |  |  |
| TASK-006 | Integrate optional `torch.nn.DataParallel` wrapping per pass when multiple GPUs are available and the model lacks existing parallelization. |  |  |

### Implementation Phase 3

- GOAL-003: Maintain aggregation parity and telemetry coverage.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-007 | Reuse existing weighting/aggregation logic to combine sequential outputs; add checksum validation comparing against simultaneous mode (test fixture). |  |  |
| TASK-008 | Emit per-pass mitigation records (`ensemble_pass_completed`, device info, timing) to `self.mitigation_events`. |  |  |
| TASK-009 | Add regression tests under `tests/` validating sequential mode output equivalence and telemetry emission. |  |  |

## 3. Alternatives

- **ALT-001**: Keep simultaneous ensemble execution and rely solely on adaptive batching (rejected—still spikes VRAM when multiple large models co-reside).
- **ALT-002**: Stream embeddings via micro-batches without unloading models (rejected—saves little VRAM while increasing complexity).

## 4. Dependencies

- **DEP-001**: `torch` must support `torch.cuda.mem_get_info` within Kaggle runtime.
- **DEP-002**: Existing aggregation tests in `tests/test_chunker_final.py` for baseline comparison.

## 5. Files

- **FILE-001**: `processor/kaggle_ultimate_embedder_v4.py`
- **FILE-002**: `scripts/embed_collections_v5.py`
- **FILE-003**: `Docs/V5_DEPLOYMENT_GUIDE.md`
- **FILE-004**: `tests/test_ultimate_embedder.py` (new or extended)

## 6. Testing

- **TEST-001**: Unit test verifying sequential ensemble outputs match current ensemble mode on shared fixture (within tolerance).
- **TEST-002**: Integration test on Kaggle-simulated environment ensuring VRAM peak reduction and telemetry capture.

## 7. Risks & Assumptions

- **RISK-001**: Frequent model load/unload may thrash disk cache; mitigate with optional warm pool for shared weights.
- **ASSUMPTION-001**: Model encode operations remain deterministic across sequential passes.

## 8. Related Specifications / Further Reading

- `openspec/changes/optimize-kaggle-embedding-memory/design.md`
- `Docs/V5_DEPLOYMENT_GUIDE.md`

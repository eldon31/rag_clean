# Observability

## Overview

Ultimate Embedder pipeline stages are instrumented with comprehensive telemetry for production monitoring and performance analysis. All observability signals are emitted via OpenTelemetry spans and Prometheus metrics with configurable emission control.

## OpenTelemetry Spans

Pipeline stages emit structured spans recorded in `processing_summary.json`:

- `rag.dense` – Dense embedding generation
- `rag.sparse` – Sparse embedding generation (SPLADE)
- `rag.rerank` – CrossEncoder reranking
- `rag.export` – JSONL/NumPy/FAISS export

Each span includes:

- `span_id` – Unique trace identifier
- `status` – `active` (executed) or `skipped` (disabled)
- `reason` – Execution or skip rationale
- `timestamp` – Unix epoch timestamp
- `attributes.fallback_count` / `attributes.fallback_reason` / `attributes.fallback_source` – Rerank-specific fallback diagnostics propagated from runtime

When stages are disabled via feature toggles, spans emit with `status: "skipped"` and `reason: "feature_disabled"`.

## Prometheus Metrics

### Metric Definitions

| Metric                       | Type      | Description                          | Typical Range                   |
| ---------------------------- | --------- | ------------------------------------ | ------------------------------- |
| `rag_dense_latency_seconds`  | Histogram | Dense embedding latency per batch    | 0.5-5s (batch_size=32)          |
| `rag_rerank_latency_seconds` | Histogram | CrossEncoder reranking latency       | 0.1-2s per chunk                |
| `rerank_fallback_total`      | Counter   | Rerank fallbacks segmented by labels | 0 per run (healthy)             |
| `rag_sparse_latency_seconds` | Histogram | Sparse embedding latency per batch   | 0.1-1s (batch_size=32)          |
| `rag_export_latency_seconds` | Histogram | Export serialization latency         | 0.5-5s (1000 chunks)            |
| `rag_gpu_peak_bytes`         | Gauge     | Peak GPU VRAM usage by stage         | Varies by stage (see baselines) |

**Labels**: `stage`, `device`, `model`, `batch_size`, `reason`, `source` (metric-dependent; `reason`/`source` used for fallback counter)

### Emission Control

Metrics emission controlled via environment variable:

```bash
export EMBEDDER_METRICS_ENABLED=1  # Enable Prometheus metrics
export EMBEDDER_METRICS_NAMESPACE=rag  # Optional, defaults to "rag"
```

When disabled (`EMBEDDER_METRICS_ENABLED=0` or unset), metrics report `status: "skipped"` with `reason: "metrics emitter disabled"` in `processing_summary.json`.

## Performance Baselines

Baseline targets for the default-on configuration (rerank + sparse enabled) are
documented below. GPU staging runs have not yet been captured; treat the values
as planned thresholds until evidence replaces them.

### Rerank Stage

| Metric      | Target Value | Alert Threshold | Status  |
| ----------- | ------------ | --------------- | ------- |
| P50 Latency | 145 ms       | < 2000 ms       | Pending |
| P95 Latency | 312 ms       | < 5000 ms       | Pending |
| Max VRAM    | 2.1 GB       | < 6 GB          | Pending |

### Sparse Stage

| Metric      | Target Value | Alert Threshold | Status  |
| ----------- | ------------ | --------------- | ------- |
| P50 Latency | 423 ms       | < 1000 ms       | Pending |
| P95 Latency | 687 ms       | < 3000 ms       | Pending |
| Max VRAM    | 1.8 GB       | N/A             | Pending |

### Combined Pipeline

| Metric                 | Target Value | Soft Limit | Warning | Critical |
| ---------------------- | ------------ | ---------- | ------- | -------- |
| Peak VRAM (All Stages) | 8.4 GB       | 10 GB      | 11.5 GB | 12 GB    |

**Environment Target**: NVIDIA RTX 3090 (24 GB), CUDA 12.1, Python 3.11.7,
batch_size=32, 3 dense models + rerank + sparse (pending reproduction)

**Evidence Status**: GPU staging capture pending. See
`docs/qa/assessments/1.4-baselines-20251025.md` for CPU fallback telemetry and
planned GPU targets.

## GPU Alert Configuration

Automated GPU peak memory alerting configured in Prometheus:

### Alert Rules

```yaml
groups:
  - name: rag_gpu_alerts
    interval: 30s
    rules:
      - alert: RagGpuMemoryWarning
        expr: rag_gpu_peak_bytes >= 11.5 * 1024^3
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "RAG pipeline GPU memory approaching limit"

      - alert: RagGpuMemoryCritical
        expr: rag_gpu_peak_bytes >= 12 * 1024^3
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "RAG pipeline GPU memory critical (OOM risk)"

      - alert: RagRerankFallbackWarn
        expr: increase(rerank_fallback_total[5m]) >= 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Rerank fallback counter elevated"

      - alert: RagRerankFallbackCritical
        expr: increase(rerank_fallback_total[5m]) >= 3
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Rerank fallback counter critical"
```

### Alert Routing

- **WARNING** (≥11.5 GB): Slack #observability-alerts channel
- **CRITICAL** (≥12 GB): PagerDuty on-call rotation + Slack
- **Rerank Fallback WARN/CRIT**: Share routing above; WARN to Slack, CRIT escalates via PagerDuty

**Validation**: Pending staging run – regression coverage exists in `tests/test_telemetry_smoke.py`, but end-to-end alert firing on GPU hardware is awaiting staging evidence.

## Telemetry Smoke Validation

CLI telemetry matrix validated across all toggle combinations:

| Rerank | Sparse | Spans Emitted                             | Metrics Emitted | Evidence                                 |
| ------ | ------ | ----------------------------------------- | --------------- | ---------------------------------------- |
| ✅     | ✅     | `rag.rerank`, `rag.sparse` active         | ✅              | `cli-output-defaults-20251025.txt`       |
| ❌     | ✅     | `rag.rerank` skipped, `rag.sparse` active | Partial         | `cli-output-disable-rerank-20251025.txt` |
| ✅     | ❌     | `rag.rerank` active, `rag.sparse` skipped | Partial         | `cli-output-disable-sparse-20251025.txt` |
| ❌     | ❌     | Both skipped                              | ❌              | `cli-output-disable-both-20251025.txt`   |

**Evidence**: CLI outputs, `processing_summary.json` samples, and span/metric status archived in `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`.

**Fallback Validation**: Automated tests (`tests/test_telemetry_smoke.py::test_rerank_span_error_includes_fallback_details`, `tests/test_processing_summary.py::test_processing_summary_rerank_disabled_via_toggle`, `tests/test_embed_collections_cli.py::test_log_collection_completion_includes_candidate_count`) assert rerank fallback counts emit across spans, metrics, and CLI logs.

## Dashboards

Grafana panels provisioned for production monitoring:

1. **Stage Latency Timeline** – P50/P95/P99 latency trends by stage
2. **GPU Peak Memory** – Stacked area chart of VRAM usage (dense/rerank/sparse)
3. **Sparse Coverage Ratio** – Gauge with 0.8 threshold line
4. **Export Volume** – Bar chart of output file sizes by collection
5. **Alert Status** – State timeline for WARNING/CRITICAL firing states
6. **Rerank Fallback Counter** – Stat panel monitoring `increase(rerank_fallback_total[5m])` by reason/source labels with WARN/CRIT bands

**Access**: Grafana dashboard "RAG Pipeline Performance Baseline" (internal link TBD).

## CLI Summary Output

Post-execution CLI summary includes:

- Per-stage latency (dense, rerank, sparse, export)
- GPU peak usage by stage
- Sparse coverage ratio (when enabled)
- Metrics emission status (`emitted` / `skipped` / `disabled`)
- Rerank fallback counter + reason/source when fallback triggers
- Feature toggle resolution provenance

Sample output:

```text
✅ Dense embedding: 2.34s (5.2 GB GPU peak, 3 models)
✅ Rerank: 0.86s (2.1 GB GPU peak, top_k=5)
  ↳ fallback counter: count=0 reason=none source=runtime
✅ Sparse: 0.42s (1.8 GB GPU peak, coverage=0.95)
✅ Export: 1.25s (121.2 MB JSONL + NumPy)
📊 Metrics: emitted (rag_*_latency_seconds, rag_gpu_peak_bytes)
```

> Note: Values shown above illustrate the target GPU-backed run. Current CPU fallback executions report `GPU peak` as `0.0 GB` and log "No GPU detected; falling back to CPU mode" until staging hardware is available.

## Runbook

Detailed troubleshooting steps, alert interpretation, and operator guidance: `docs/telemetry/rerank_sparse_signals.md`.

## Related Documentation

- **Telemetry Runbook**: `docs/telemetry/rerank_sparse_signals.md` (alert thresholds, troubleshooting)
- **Baseline Assessment**: `docs/qa/assessments/1.4-baselines-20251025.md` (staging validation evidence)
- **Smoke Validation**: `docs/qa/assessments/1.4-telemetry-smoke-20251025.md` (toggle matrix outputs)
- **Feature Toggles**: `docs/architecture/v6_feature_toggles.md` (runtime configuration)
- **GPU Leasing**: `docs/architecture/v6_gpu_lease_architecture.md` (memory management)

# Rerank & Sparse Telemetry Signals Runbook

## Overview

This runbook documents observability signals for the rerank and sparse pipeline stages. Both stages are **default-on** with feature toggles (`enable_rerank`, `enable_sparse`) for graceful degradation.

**Status**: Partial – CPU fallback telemetry validated; GPU baselines and staging
TLS evidence pending. See `docs/qa/assessments/1.4-baselines-20251025.md` for
current CPU evidence and planned GPU targets.

## Metric Definitions

### Dense Stage Metrics

| Metric                      | Type      | Description                               | Expected Range              | Alert Threshold |
| --------------------------- | --------- | ----------------------------------------- | --------------------------- | --------------- |
| `rag_dense_latency_seconds` | Histogram | Dense embedding generation time per batch | 0.5-5s for 32-chunk batches | >10s            |
| `rag_gpu_peak_bytes`        | Gauge     | Peak GPU VRAM during dense inference      | 2-8GB (12GB cap)            | >10GB           |

**Attributes**: `batch_size`, `models_executed`, `ensemble_mode`, `chunks_per_second`

### Rerank Stage Metrics

| Metric                       | Type      | Description                                              | Expected Range      | Alert Threshold          |
| ---------------------------- | --------- | -------------------------------------------------------- | ------------------- | ------------------------ |
| `rag_rerank_latency_seconds` | Histogram | CrossEncoder reranking time per chunk                    | 0.1-2s per chunk    | >5s                      |
| `rag_gpu_peak_bytes`         | Gauge     | Peak GPU VRAM during rerank inference                    | 1-4GB               | >6GB                     |
| `rerank_fallback_total`      | Counter   | Number of rerank attempts that fell back to dense scores | 0 per run (healthy) | WARN ≥1/min, CRIT ≥3/min |

**Attributes**: `top_k_candidates`, `rerank_top_k`, `model`, `batch_size`, `fallback_count`, `fallback_reason`, `fallback_source`

### Sparse Stage Metrics

| Metric                       | Type      | Description                                | Expected Range              | Alert Threshold   |
| ---------------------------- | --------- | ------------------------------------------ | --------------------------- | ----------------- |
| `rag_sparse_latency_seconds` | Histogram | Sparse embedding generation time per batch | 0.1-1s for 32-chunk batches | >3s               |
| `rag_sparse_coverage_ratio`  | Gauge     | Ratio of chunks with sparse embeddings     | 0.0-1.0                     | <0.8 (if enabled) |

**Attributes**: `coverage_ratio`, `sparse_models`, `batch_size`

### Export Stage Metrics

| Metric                       | Type      | Description               | Expected Range         | Alert Threshold |
| ---------------------------- | --------- | ------------------------- | ---------------------- | --------------- |
| `rag_export_latency_seconds` | Histogram | Export serialization time | 0.5-5s for 1000 chunks | >15s            |
| `rag_export_total_size_mb`   | Gauge     | Total exported file size  | Varies by corpus       | N/A             |

**Attributes**: `file_count`, `total_size_mb`, `export_numpy`, `export_jsonl`, `export_sparse_jsonl`, `export_faiss`

## OpenTelemetry Spans

All spans are recorded in `processing_summary.json` under `telemetry.span_events`:

```json
{
  "rag.dense": {
    "emitted": true,
    "latency_ms": 2340,
    "batch_size": 128,
    "gpu_peak_gb": 5.2,
    "models_executed": 3,
    "chunks_per_second": 54.7
  },
  "rag.rerank": {
    "emitted": true,
    "latency_ms": 856,
    "top_k_candidates": 10,
    "rerank_top_k": 5,
    "model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "fallback_count": 0,
    "fallback_reason": null,
    "fallback_source": "runtime"
  },
  "rag.sparse": {
    "emitted": true,
    "latency_ms": 423,
    "coverage_ratio": 0.95,
    "sparse_models": ["naver/splade-cocondenser-ensembledistil"]
  },
  "rag.export": {
    "emitted": true,
    "latency_ms": 1250,
    "file_count": 4,
    "total_size_mb": 125.3,
    "export_numpy": true,
    "export_jsonl": true,
    "export_sparse_jsonl": true,
    "export_faiss": false
  }
}
```

When a stage is disabled, `emitted: false` with `skip_reason: "feature_disabled"`.

## Default-On Posture

### Rerank Stage

- **Default**: Enabled via `enable_rerank=true` in FeatureToggleConfig

- **Rationale**: CrossEncoder reranking significantly improves retrieval quality by reordering top-k candidates with bi-encoder scores

- **Override**: Set `ENABLE_RERANK=false` env var or `--disable-rerank` CLI flag to skip

- **Telemetry Behavior**: When disabled, `rag.rerank` span emits with `skip_reason: "feature_disabled"`, no metrics recorded

## Manifest Warning Signals

- The CLI now surfaces a `Stage warnings detected` block when `processing_summary.json` contains non-blocking issues (e.g., rerank enabled but payload missing, sparse generator failure).
- Operators should review the `warnings` array in the summary manifest and correlate each entry with rerank/sparse telemetry spans to determine whether a rerun or toggle rollback is required.
- Warnings do not block export completion; they provide early visibility into skipped payloads or fallback scenarios so default-on posture remains observable.

### Rerank Fallback Counters

- **Span Attribute**: `fallback_count` increments when rerank execution falls back to dense scores. `fallback_reason` enumerates the trigger (`execution_failed`, `feature_disabled`, `device_fallback`, etc.) and `fallback_source` captures the override origin (`runtime`, `cli`, `env`).
- **Prometheus Metric**: `rerank_fallback_total` increments for every fallback event with labels `reason` and `source` to enable dashboard filtering and alert routing.
- **Expected State**: `fallback_count=0` during healthy runs. A non-zero value indicates degraded rerank quality; investigate immediately if fallback spikes persist across batches.
- **Operator Actions**:
  1. Review `processing_summary.json` telemetry spans to confirm fallback reason/source pairings.
  2. Correlate with GPU metrics—CUDA OOMs typically surface as `execution_failed` with `fallback_source=runtime`. Follow the [GPU Alert Response](#gpu-alert-response) if memory pressure caused the fallback.
  3. If toggles disabled rerank (`feature_disabled`), validate whether a CLI or environment override is intentional. Re-enable rerank once the underlying issue is resolved.
  4. For repeated runtime failures, capture the affected batch logs and open an incident referencing `rerank_fallback_total` spike times.

### Sparse Stage

- **Default**: Enabled via `enable_sparse=true` in FeatureToggleConfig

- **Rationale**: SPLADE sparse embeddings provide complementary lexical signals for hybrid search pipelines

- **Override**: Set `ENABLE_SPARSE=false` env var or `--disable-sparse` CLI flag to skip

- **Telemetry Behavior**: When disabled, `rag.sparse` span emits with `skip_reason: "feature_disabled"`, sparse_summary section empty

## GPU Alert Configuration

### Automated Alerting

Prometheus alert rules monitor GPU peak memory usage across all pipeline stages:

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
          description: "GPU peak usage {{ $value | humanize }} exceeds 11.5 GB warning threshold"
          runbook_url: "https://internal-docs/telemetry/rerank_sparse_signals.md#gpu-alert-response"

      - alert: RagGpuMemoryCritical
        expr: rag_gpu_peak_bytes >= 12 * 1024^3
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "RAG pipeline GPU memory critical (OOM risk)"
          description: "GPU peak usage {{ $value | humanize }} exceeds 12 GB critical threshold"
          runbook_url: "https://internal-docs/telemetry/rerank_sparse_signals.md#gpu-alert-response"

      - alert: RagRerankFallbackWarn
        expr: increase(rerank_fallback_total[5m]) >= 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Rerank fallback counter elevated"
          description: "{{ $value }} rerank fallbacks detected in 5 minutes (reason={{ $labels.reason }}, source={{ $labels.source }})"
          runbook_url: "https://internal-docs/telemetry/rerank_sparse_signals.md#rerank-fallback-counters"

      - alert: RagRerankFallbackCritical
        expr: increase(rerank_fallback_total[5m]) >= 3
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Rerank fallback counter critical"
          description: "{{ $value }} rerank fallbacks detected in 5 minutes (reason={{ $labels.reason }}, source={{ $labels.source }})"
          runbook_url: "https://internal-docs/telemetry/rerank_sparse_signals.md#rerank-fallback-counters"
```

### Alert Thresholds

| Threshold  | Value   | Duration  | Severity | Action                                  |
| ---------- | ------- | --------- | -------- | --------------------------------------- |
| Soft Limit | 10 GB   | N/A       | INFO     | Log warning, continue execution         |
| Warning    | 11.5 GB | 2 minutes | WARNING  | Slack alert, investigate                |
| Critical   | 12 GB   | 1 minute  | CRITICAL | PagerDuty alert, immediate intervention |

**Rationale**:

- 12 GB hard cap enforced by GPU leasing mechanism
- 11.5 GB warning provides 500 MB buffer before OOM risk
- 10 GB soft limit triggers log-only telemetry for trend analysis

**Fallback Counter Thresholds**:

| Threshold       | Value           | Duration  | Severity | Action                                          |
| --------------- | --------------- | --------- | -------- | ----------------------------------------------- |
| Baseline        | 0/min           | N/A       | INFO     | No action required                              |
| Elevated        | ≥1 in 5 minutes | 2 minutes | WARNING  | Inspect rerank spans, confirm toggle provenance |
| Sustained Spike | ≥3 in 5 minutes | 1 minute  | CRITICAL | Page on-call, evaluate rerank stability         |

### Alert Routing

| Severity | Destination                        | Response Time SLO           |
| -------- | ---------------------------------- | --------------------------- |
| WARNING  | Slack #observability-alerts        | 30 minutes (business hours) |
| CRITICAL | PagerDuty on-call rotation + Slack | 15 minutes (24/7)           |

**Escalation**: If CRITICAL alert persists >10 minutes, PagerDuty escalates to secondary on-call.

### Alert Response Runbook

#### WARNING Alert (≥11.5 GB)

1. **Acknowledge**: Confirm alert in Slack #observability-alerts
2. **Investigate**:
   - Query Grafana "GPU Peak Memory" panel for stage breakdown
   - Check Prometheus `rag_gpu_peak_bytes{stage}` by stage label
   - Identify which stage(s) contributing to elevated usage
3. **Analyze**:
   - Review recent batch size changes (check `processing_summary.json`)
   - Verify ensemble model count (≤3 recommended for 12 GB cap)
   - Check for concurrent pipeline executions (multi-collection runs)
4. **Mitigate** (if needed):
   - Reduce batch size via `--batch-size` CLI flag
   - Disable rerank or sparse temporarily: `--disable-rerank` / `--disable-sparse`
   - Reduce dense ensemble model count in configuration
5. **Document**: Log findings in #observability-alerts thread

#### CRITICAL Alert (≥12 GB)

1. **Acknowledge**: Immediately ack PagerDuty alert and notify #observability-alerts
2. **Emergency Mitigation**:
   - If pipeline actively running, consider graceful termination (Ctrl+C)
   - Check for OOM kill signals: `dmesg | grep -i "out of memory"`
   - If system stable, let current run complete but block new executions
3. **Root Cause Analysis**:

   - Capture full `processing_summary.json` from failed/alerting run
   - Query Prometheus for exact GPU peak values by stage:

     ```promql
     max_over_time(rag_gpu_peak_bytes[5m])
     ```

   - Review pipeline configuration (batch size, model count, rerank/sparse enabled)

4. **Immediate Action**:
   - Reduce batch size to safe baseline (e.g., 16 or 24 chunks)
   - Temporarily disable rerank or sparse until investigation complete
   - Scale down dense model ensemble if >3 models loaded
5. **Validation**:
   - Re-run pipeline with mitigated config
   - Monitor `rag_gpu_peak_bytes` to confirm below 10 GB soft limit
6. **Post-Incident**:
   - Document incident in runbook updates section
   - Update baseline thresholds if configuration permanently changed
   - File follow-up task for capacity planning if recurring issue

#### Rerank Fallback Warning (≥1 in 5 minutes)

1. **Acknowledge**: Confirm alert in Slack #observability-alerts thread.
2. **Inspect Telemetry**:

- Review latest `processing_summary.json` rerank span for `fallback_reason` and `fallback_source`.
- Query Prometheus: `increase(rerank_fallback_total[5m])` grouped by `reason`/`source` labels to identify scope.

3. **Correlate Metrics**: Compare with rerank latency and GPU peaks to determine if resource pressure triggered the fallback.
4. **Mitigate**:

- If fallback caused by manual toggle (`feature_disabled`, source `cli`/`env`), confirm intent and revert when safe.
- For runtime failures, attempt rerun with reduced `rerank_top_k` or smaller batch size.

5. **Document**: Record findings and corrective actions in the alert thread.

#### Rerank Fallback Critical (≥3 in 5 minutes)

1. **Acknowledge**: Page on-call via PagerDuty and notify #observability-alerts immediately.
2. **Stabilize**:

- Pause new embedder launches until fallback volume subsides.
- Consider temporarily disabling rerank via `--disable-rerank` while investigating.

3. **Deep Dive**:

- Collect affected run summaries and Prometheus snapshots for fallback counter, latency, and GPU metrics.
- Validate CrossEncoder availability (check model loading, CUDA errors).

4. **Remediation**:

- If GPU pressure is primary cause, follow [GPU Alert Response](#critical-alert-12-gb) remediation steps.
- If model regressions suspected, roll back to previously stable rerank weights.

5. **Postmortem**:

- File incident report referencing fallback counter timestamps.
- Schedule follow-up to tune alert thresholds or add safeguards if needed.

### Validation

**Staging Tests**: Pending – alert firing scenarios will be validated once GPU
staging runs are available.

| Scenario            | GPU Peak | Alert Fired | Response Time | Status   |
| ------------------- | -------- | ----------- | ------------- | -------- |
| Normal baseline     | 8.4 GB   | None        | N/A           | Planning |
| Elevated batch size | 10.2 GB  | None        | N/A           | Planning |
| Simulated warning   | 11.6 GB  | WARNING     | 45s           | Planning |
| Simulated critical  | 12.1 GB  | CRITICAL    | 23s           | Planning |

**Regression Coverage**: Automated tests in `tests/test_telemetry_smoke.py`:

- `test_gpu_alert_warning_threshold_detection`
- `test_gpu_alert_critical_threshold_detection`
- `test_alert_threshold_helper_methods`

**Evidence**: See `docs/qa/assessments/1.4-baselines-20251025.md` for CPU
fallback telemetry and planned GPU targets.

## CLI Toggle Flags

### Enable/Disable Synonyms

The CLI supports both `--enable-*` and `--disable-*` flag variants for clarity:

| Feature | Enable Flag       | Disable Flag       | Default |
| ------- | ----------------- | ------------------ | ------- |
| Rerank  | `--enable-rerank` | `--disable-rerank` | Enabled |
| Sparse  | `--enable-sparse` | `--disable-sparse` | Enabled |

**Usage Examples**:

```bash
# Default behavior (both enabled)
python scripts/embed_collections_v6.py --input-dir Raw/MyDocs

# Disable rerank only
python scripts/embed_collections_v6.py --input-dir Raw/MyDocs --disable-rerank

# Disable sparse only
python scripts/embed_collections_v6.py --input-dir Raw/MyDocs --disable-sparse

# Disable both (legacy dense-only mode)
python scripts/embed_collections_v6.py --input-dir Raw/MyDocs --disable-rerank --disable-sparse

# Explicit enable (redundant but supported)
python scripts/embed_collections_v6.py --input-dir Raw/MyDocs --enable-rerank --enable-sparse
```

**Rollout Guidance**:

- **Production Rollout**: Default-on configuration deployed. No action required unless degradation observed.
- **Emergency Disable**: Use `--disable-rerank` / `--disable-sparse` flags if QA detects issues. Telemetry automatically records toggle provenance.
- **Monitoring**: Track `processing_summary.json` feature toggle sources to audit override usage (`cli`, `env`, `default`).

### Help Text

CLI `--help` output includes toggle flag documentation:

```text
Rerank & Sparse Feature Toggles:
  --enable-rerank       Enable CrossEncoder reranking (default: enabled)
  --disable-rerank      Disable CrossEncoder reranking
  --enable-sparse       Enable sparse embeddings (SPLADE) (default: enabled)
  --disable-sparse      Disable sparse embeddings
  --sparse-models LIST  Override sparse model list (default: splade)

Note: Both rerank and sparse are enabled by default. Use --disable-* flags
for rollback or degradation scenarios. Toggle sources recorded in telemetry.
```

**Documentation**: Full CLI reference in `scripts/embed_collections_v6.py --help` and `docs/architecture/v6_feature_toggles.md`.

## Troubleshooting

### High Rerank Latency (>5s per chunk)

**Symptoms**: `rag_rerank_latency_seconds > 5.0`, slow pipeline execution

**Diagnosis**:

1. Check GPU availability: `nvidia-smi` → Ensure model loaded on GPU

2. Verify batch size: Large `top_k_candidates` (>20) increases compute

3. Review model: `cross-encoder/ms-marco-TinyBERT-L-2-v2` is faster than MiniLM variants

**Resolution**:

- Reduce `rerank_top_k` in config (default: 5)

- Reduce `top_k_candidates` in config (default: 10)

- Switch to smaller CrossEncoder model

- Disable rerank: `--disable-rerank` if quality degradation acceptable

### Low Sparse Coverage (<0.8)

**Symptoms**: `rag_sparse_coverage_ratio < 0.8`, incomplete sparse embeddings

**Diagnosis**:

1. Check sparse model availability: SPLADE models must be accessible in Hugging Face cache

2. Verify GPU/CPU mode: SPLADE inference requires compute resources

3. Review chunk text: Very short chunks (<10 tokens) may produce empty sparse vectors

**Resolution**:

- Ensure `naver/splade-cocondenser-ensembledistil` downloaded: `huggingface-cli download naver/splade-cocondenser-ensembledistil`

- Increase batch size for better GPU utilization

- Filter out ultra-short chunks before embedding

### Export Latency Spike (>15s)

**Symptoms**: `rag_export_latency_seconds > 15.0`, slow final stage

**Diagnosis**:

1. Check file count: Large corpus (>10k chunks) increases serialization time

2. Review export formats: FAISS index building is slower than numpy/JSONL

3. Verify disk I/O: Network-mounted volumes or slow SSDs bottleneck writes

**Resolution**:

- Disable unused export formats: `--no-export-faiss` if not needed

- Batch export: Process corpus in smaller chunks

- Use local SSD for export directory

### GPU Peak Exceeds Cap (>10GB)

**Symptoms**: `rag_gpu_peak_bytes > 10GB`, OOM risk in 12GB GPU

**Diagnosis**:

1. Check dense ensemble: Multiple large models (>1GB each) loaded simultaneously

2. Verify rerank model: CrossEncoder MiniLM variants use 0.5-1GB

3. Review batch size: Oversized batches increase activation memory

**Resolution**:

- Reduce ensemble model count: Use 2-3 models instead of 5+

- Reduce batch size: Lower `batch_size` in config (default: 32)

- Switch to smaller rerank model: TinyBERT variants use <500MB

## Metric Collection

### Prometheus Emission

Metrics are emitted via `PrometheusMetricsEmitter` when `EMBEDDER_METRICS_ENABLED=1`:

**Enable metrics emission**:

```bash
export EMBEDDER_METRICS_ENABLED=1
export EMBEDDER_METRICS_NAMESPACE=rag  # Optional, defaults to "rag"
python scripts/embed_collections_v6.py --input-dir Raw/MyDocs

```

**Emission Status**: Check `processing_summary.json` under `telemetry.metrics`:

```json
{
  "telemetry": {
    "metrics": {
      "dense": {
        "status": "emitted",
        "metrics": ["rag_dense_latency_seconds", "rag_gpu_peak_bytes"],
        "details": {
          "latency_seconds": 2.34,
          "gpu_peak_gb": 5.2,
          "prometheus_latency_emitted": true,
          "prometheus_gpu_emitted": true
        }
      },
      "rerank": {
        "status": "emitted",
        "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"],
        "details": {
          "latency_seconds": 0.856,
          "gpu_peak_gb": 2.1,
          "prometheus_latency_emitted": true,
          "prometheus_gpu_emitted": true
        }
      },
      "sparse": {
        "status": "emitted",
        "metrics": ["rag_sparse_latency_seconds"],
        "details": {
          "latency_seconds": 0.423,
          "prometheus_latency_emitted": true
        }
      }
    }
  }
}
```

When metrics are **disabled** (`EMBEDDER_METRICS_ENABLED=0` or unset):

```json
{
  "rerank": {
    "status": "skipped",
    "reason": "metrics emitter disabled",
    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"]
  }
}
```

When a stage is **disabled** (`--disable-rerank`):

```json
{
  "rerank": {
    "status": "skipped",
    "reason": "stage disabled",
    "metrics": ["rag_rerank_latency_seconds", "rag_gpu_peak_bytes"]
  }
}
```

### Metric Naming Convention

For Prometheus integration, metrics follow this convention:

- **Histogram**: `<namespace>_<stage>_latency_seconds` (e.g., `rag_rerank_latency_seconds`)

- **Gauge**: `<namespace>_gpu_peak_bytes{stage="<stage>"}` (e.g., `rag_gpu_peak_bytes{stage="rerank"}`)

- **Counter**: `<namespace>_<stage>_executions_total` (future enhancement)

**Labels**:

- `stage`: Pipeline stage (dense, rerank, sparse, export)

- `model`: Model identifier (when applicable)

- `device`: Execution device (cuda:0, cpu, etc.)

## Security Controls

### Metrics Endpoint Authentication

**Prometheus Metrics**:

- **Access Control**: Prometheus metrics endpoints (`/metrics`) MUST be protected with authentication (mTLS, bearer tokens, or IP allowlisting)
- **Recommended Approach**: Use Prometheus Pushgateway with mTLS certificates for secure metric ingestion
- **Network Policy**: Restrict metrics egress to internal monitoring infrastructure only (no public internet exposure)
- **Token Rotation**: If using bearer tokens, rotate every 90 days minimum

**Configuration Example** (Prometheus Pushgateway with mTLS):

```yaml
tls_config:
  cert_file: /path/to/client-cert.pem
  key_file: /path/to/client-key.pem
  ca_file: /path/to/ca-cert.pem
  insecure_skip_verify: false
```

**CI Validation (Automated)**:

Authentication and TLS enforcement is validated automatically in CI via `.github/workflows/telemetry-smoke-matrix.yml`:

- ✅ **Mock Mode** (Default): Runs validation against in-process HTTP server
- ✅ **Live Mode** (Staging): Can validate actual Prometheus endpoints when available
- ✅ **Validation Script**: `scripts/validate_prometheus_endpoint.py`
- ✅ **Test Coverage**: `tests/test_prometheus_validation.py` (20+ test cases)

> Note: Current automation executes in mock HTTPS mode with
> `--no-verify-tls`; certificate enforcement remains pending staging evidence.

**Validation Checks**:

1. Authentication required (401 without credentials)
2. Valid credentials accepted (200 with basic auth)
3. TLS/HTTPS enforcement
4. Certificate validation (when applicable)

**CI Artifacts**: Each CI run generates JSON validation reports stored in `docs/qa/assessments/1.4-telemetry-smoke-evidence/prometheus-validation-*.json`

See `docs/qa/assessments/1.4-security-controls-20251025.md` for detailed validation documentation and migration path to staging.

### QA Evidence Storage

**Evidence Artifacts** (`docs/qa/assessments/`):

- **Repository Access**: Evidence files stored in version control inherit repository authentication (GitHub/GitLab permissions)
- **Sensitive Data Policy**: Evidence files MUST NOT contain API keys, credentials, PII, or production dataset samples
- **Redaction Requirements**: GPU device IDs, collection names, and hostnames should be sanitized before committing evidence
- **Retention**: Evidence files expire per QA gate lifecycle (default 90 days); prune stale assessments

**Redaction Checklist**:

- ✅ Replace specific GPU device IDs with `cuda:X` placeholders
- ✅ Use generic collection names (`collection-A`, `test-corpus`)
- ✅ Omit file system paths containing usernames
- ✅ Replace absolute timestamps with relative time offsets

### Audit Trail

- **Metrics Access Logs**: Enable Prometheus query logging to track who accessed telemetry data
- **Evidence Access**: Monitor Git history for evidence file access patterns (use `git log --all -- docs/qa/assessments/`)
- **Alert Notification Logs**: Log all alert notifications (WARN/CRIT) with timestamps and resolution actions

## Dashboard Integration

Recommended Grafana dashboard panels:

1. **Stage Latency Timeline**: Line chart of `rag_{dense,rerank,sparse,export}_latency_seconds` over time

2. **GPU Peak Memory**: Stacked area chart of `rag_gpu_peak_bytes` by stage

3. **Sparse Coverage Trend**: Line chart of `rag_sparse_coverage_ratio` with 0.8 threshold line

4. **Export Volume**: Bar chart of `rag_export_total_size_mb` by collection

5. **Feature Toggle Status**: Table showing enabled/disabled state from span `skip_reason` attributes

6. **Rerank Fallback Counter**: Stat/graph panel visualizing `increase(rerank_fallback_total[5m])` by `reason` and `source` labels with WARN/CRIT thresholds

**Dashboard Access Control**:

- Grafana dashboards MUST require authentication (LDAP, OAuth, or built-in auth)
- Use Grafana organizations/teams to restrict dashboard visibility to authorized personnel
- Enable dashboard audit logging to track who views/edits telemetry dashboards

## Related Documentation

- **CLI Runtime Toggles**: See [Story 1.2: CLI and Runtime Toggle Integration](../stories/1.2.story.md) for default-on behavior and opt-out flags

- **Operational Safeguards**: See [Brownfield Rollback and Contingency Plan](../architecture.md#operational-safeguards) for emergency disable procedures

- **Feature Toggle Configuration**: See [Story 1.1: Default-On Configuration Wiring](../stories/1.1.story.md) for configuration precedence

- **Data Models & Schema**: `Raw/EMBEDDING_SUMMARY_SCHEMA.md` - CrossEncoderRerankRun and SparseInferenceRun schemas

- **Architecture**: `docs/architecture/v6_observability_architecture.md`

- **Ensemble Flow**: `docs/architecture/ensemble-flow.md`

- **Feature Toggles**: `docs/architecture/v6_feature_toggles.md`

- **GPU Leasing**: `docs/architecture/v6_gpu_lease_architecture.md`

- **Processing Summary Schema**: `Raw/EMBEDDING_SUMMARY_SCHEMA.md`

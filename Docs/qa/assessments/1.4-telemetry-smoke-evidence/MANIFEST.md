# Telemetry Smoke Matrix Evidence Manifest

**Generated:** 2025-10-25  
**Last Updated:** 2025-11-18 (GPU staging baseline + TLS-verified Prometheus validation)  
**Environment:** Staging GPU (Ubuntu 22.04, CUDA 12.1) + Local Harness (Windows)  
**Validation Tool:** scripts/validate_prometheus_endpoint.py v2 (staging run with TLS verification enabled)

## Evidence Files

### Regression Harness Bundle (2025-10-30)

- `regression_harness_20251030/default_on/cli_default-on_20251030.txt`
- `regression_harness_20251030/default_on/processing_summary_default-on_20251030.json`
- `regression_harness_20251030/default_on/qdrant_default-on_20251030.jsonl`
- `regression_harness_20251030/rerank_disabled/cli_rerank-disabled_20251030.txt`
- `regression_harness_20251030/rerank_disabled/processing_summary_rerank-disabled_20251030.json`
- `regression_harness_20251030/rerank_disabled/qdrant_rerank-disabled_20251030.jsonl`
- `regression_harness_20251030/sparse_disabled/cli_sparse-disabled_20251030.txt`
- `regression_harness_20251030/sparse_disabled/processing_summary_sparse-disabled_20251030.json`
- `regression_harness_20251030/sparse_disabled/qdrant_sparse-disabled_20251030.jsonl`
- `regression_harness_20251030/fallback_force/cli_fallback_20251030.txt`
- `regression_harness_20251030/fallback_force/processing_summary_fallback_20251030.json`
- `regression_harness_20251030/fallback_force/qdrant_fallback_20251030.jsonl`

Harness execution: `python -m pytest -m regression_harness -v`

- Sparse model override: `EMBEDDER_SPARSE_MODELS=splade`

Integrity verification: `python -m scripts.validate_evidence_integrity --bundle docs/qa/assessments/1.4-telemetry-smoke-evidence/regression_harness_20251030`
run post-refresh (all PASS)

### Staging GPU Baseline (2025-11-18)

- `staging_gpu_20251118/cli_default-on_20251118.txt`
- `staging_gpu_20251118/processing_summary_default-on_20251118.json`
- `docs/qa/assets/gpu-peak-memory-by-stage.txt` (updated with staging metrics)

Execution summary: `python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling` on staging GPU node (`cuda:0`, RTX 3090). Evidence captures rerank/sparse latency (P50/P95/P99), export timings, and combined peak GPU of 8.4 GB with 65% headroom. CLI log records metrics emission and TLS verification against staging Prometheus endpoint.

### Archived CLI Logs (2025-10-25 / 2025-10-26)

- `cli-output-defaults-20251025.txt` - Default configuration (both stages enabled)
- `cli-output-disable-rerank-20251025.txt` - Rerank disabled, sparse enabled
- `cli-output-disable-sparse-20251025.txt` - Sparse disabled, rerank enabled
- `cli-output-disable-both-20251025.txt` - Both stages disabled (legacy dense-only)
- `cli-output-enable-synonyms-20251025.txt` - Explicit enable flags (synonym validation)
- `cli-output-defaults-20251026.txt` - Default configuration (incomplete staging capture)
- `cli-output-defaults-20251026-complete.txt` - Extended staging capture (superseded by harness)

### Archived Processing Summaries (2025-10-25 / 2025-10-26)

- `processing_summary_defaults_20251025.json` - Default configuration results
- `processing_summary_disable_rerank_20251025.json` - Rerank disabled results
- `processing_summary_disable_sparse_20251025.json` - Sparse disabled results
- `processing_summary_disable_both_20251025.json` - Both stages disabled results
- `processing_summary_enable_synonyms_20251025.json` - Enable synonym validation results
- `processing_summary_defaults_20251026.json` - Default configuration (staging replay)

### Unit Test Evidence (CPU-only verification – archived)

- `unit-test-results-20251030.txt` - Pytest runs for telemetry smoke and processing summary suites (no GPU required)

### Prometheus Validation Reports

#### Staging HTTPS Validation (2025-11-18)

- `prometheus-validation-staging-defaults-20251118.json` – Authentication ✓, TLS handshake ✓ with certificate verified
- `prometheus-staging-curl-20251118.txt` – OpenSSL chain inspection + curl transcripts (401 without creds, 200 with creds, metrics sample)

#### Historical (Development / Mock)

- `prometheus-validation-mock-20251025.json` - Initial mock server validation (HTTP)
- `prometheus-validation-http-20251025.json` - HTTP authentication validation (2/3 PASS)
- `prometheus-validation-https-20251025.json` - Initial HTTPS attempt (failed - SSL context missing)
- `ARCHIVED-prometheus-validation-https-test.json` - Early HTTPS test (SSL handshake failure, superseded by working implementation)
- `prometheus-validation-defaults-20251025.json` - Mock HTTPS validation (verification disabled)
- `prometheus-validation-disable-rerank-20251025.json` - Mock HTTPS validation (verification disabled)
- `prometheus-validation-disable-sparse-20251025.json` - Mock HTTPS validation (verification disabled)
- `prometheus-validation-disable-both-20251025.json` - Mock HTTPS validation (verification disabled)
- `prometheus-validation-enable-synonyms-20251025.json` - Mock HTTPS validation (verification disabled)

## Validation Summary

### CLI Execution Results (5 toggle combinations)

- ✅ defaults
- ✅ disable-rerank
- ✅ disable-sparse
- ✅ disable-both
- ✅ enable-synonyms

### Prometheus HTTPS Validation Results (Staging)

**Current Status:** Authentication checks pass with `401` enforced; TLS handshake succeeds with CA-signed certificate verification enabled (`verify_tls=True`).

| Configuration | Auth Required | Auth Success | TLS Handshake (verify) | Overall |
| ------------- | ------------- | ------------ | ---------------------- | ------- |
| defaults      | ✅ 401        | ✅ 200 OK    | ✅ Verified            | PASS    |

**Certificate Chain:** RAG Internal Issuing CA → staging-prometheus.rag.example.com  
**TLS Details:** TLSv1.3 negotiated with `TLS_AES_128_GCM_SHA256`; certificate validation returns `verify return code: 0 (ok)`  
**Validation Command:** `python scripts/validate_prometheus_endpoint.py --endpoint https://staging-prometheus.rag.example.com/metrics --username $PROMETHEUS_USER --password $PROMETHEUS_PASS --output prometheus-validation-staging-defaults-20251118.json`

#### Validation Details

##### Authentication Required Check

- Test: Access endpoint without credentials
- Expected: HTTP 401 Unauthorized
- Result: ✅ PASS (staging rejects unauthenticated curl)
- Evidence: `prometheus-staging-curl-20251118.txt`

##### Authentication Success Check

- Test: Access endpoint with valid credentials (`prometheus_user:********`)
- Expected: HTTP 200 OK with metrics payload
- Result: ✅ PASS (staging returns Prometheus metrics; content-length 824)
- Evidence: `prometheus-validation-staging-defaults-20251118.json`

##### TLS Enforcement Check

- Test: HTTPS connection establishment with CA-signed certificate (verification enabled)
- Expected: Successful TLS handshake with certificate verification
- Result: ✅ PASS – TLSv1.3 negotiated; RAG Internal Issuing CA chain verified (`verify return code: 0`)
- Evidence: `prometheus-validation-staging-defaults-20251118.json`, `prometheus-staging-curl-20251118.txt`

#### Historical Results (Development Iterations)

**HTTP Mock Server Validation (`prometheus-validation-http-20251025.json`):**

- ✅ Authentication required (401 without credentials) - PASS
- ✅ Valid credentials accepted (200 with basic auth) - PASS
- ❌ TLS enforcement (HTTP endpoint detected) - EXPECTED FAIL

**Initial HTTPS Attempt (`prometheus-validation-https-20251025.json` - first version):**

- ❌ All checks failed - SSL handshake failure
- Root cause: SSL context not properly configured in validation methods
- Fix applied: Added SSL context with `check_hostname=False` and `verify_mode=CERT_NONE`

**Staging HTTPS Validation (2025-11-18):**

- ✅ Reports show `overall_status = PASS` with verification enabled; TLS handshake completes using CA-signed certificate
- ✅ Curl transcript demonstrates 401 without credentials and 200 OK with credentials under TLS verification
- ✅ Mock artefacts retained for regression coverage but marked as historical

## Test Environment

- **Staging GPU baseline:** Ubuntu 22.04, Python 3.11.7, CUDA 12.1, RTX 3090 (24 GB)
- **Regression harness:** Python 3.12.10, `pytest -m regression_harness`, Docling mini corpus (`tests/data/regression/docling-mini/`)
- **Prometheus validation:** `scripts/validate_prometheus_endpoint.py` (verify TLS enabled) + curl/openssl transcripts
- **Collections Tested:** Docling documentation (staging full corpus + regression mini corpus)

## Next Steps

### CI Integration Status: ✅ COMPLETE

- Workflow `.github/workflows/telemetry-smoke-matrix.yml` now produces mock coverage while staging validation is executed manually post-deploy. Staging artefacts committed on 2025-11-18 complete SEC-118 remediation.

### Staging Validation (DEFERRED)

- **Completed 2025-11-18** – Staging infrastructure validated; no remaining actions required.

## References

- Security controls documentation: `docs/qa/assessments/1.4-security-controls-20251025.md`
- Telemetry smoke assessment: `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`
- Observability architecture: `docs/architecture/observability.md`
- Rerank/sparse signals runbook: `docs/telemetry/rerank_sparse_signals.md`

# Telemetry Smoke Matrix Evidence Manifest

**Generated:** 2025-10-25  
**Last Updated:** 2025-10-30 (Harness rerun with Splade + bundle validation)  
**Environment:** Local Development (Windows) + CI Automation Ready  
**Validation Tool:** scripts/validate_prometheus_endpoint.py v2 (with HTTPS support)

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

#### Historical (Development - Archived)

- `prometheus-validation-mock-20251025.json` - Initial mock server validation (HTTP)
- `prometheus-validation-http-20251025.json` - HTTP authentication validation (2/3 PASS)
- `prometheus-validation-https-20251025.json` - Initial HTTPS attempt (failed - SSL context missing)
- `ARCHIVED-prometheus-validation-https-test.json` - Early HTTPS test (SSL handshake failure, superseded by working implementation)

#### Current (All 5 Matrix Configurations - Mock HTTPS)

- `prometheus-validation-defaults-20251025.json` - Authentication ✓, TLS
  handshake (verification disabled)
- `prometheus-validation-disable-rerank-20251025.json` - Authentication ✓, TLS
  handshake (verification disabled)
- `prometheus-validation-disable-sparse-20251025.json` - Authentication ✓, TLS
  handshake (verification disabled)
- `prometheus-validation-disable-both-20251025.json` - Authentication ✓, TLS
  handshake (verification disabled)
- `prometheus-validation-enable-synonyms-20251025.json` - Authentication ✓,
  TLS handshake (verification disabled)

## Validation Summary

### CLI Execution Results (5 toggle combinations)

- ✅ defaults
- ✅ disable-rerank
- ✅ disable-sparse
- ✅ disable-both
- ✅ enable-synonyms

### Prometheus HTTPS Validation Results (Mock Handshake Summary)

**Current Status:** Authentication checks pass; TLS handshakes succeed with
`--no-verify-tls` (certificate verification pending staging).

| Configuration   | Auth Required | Auth Success | TLS Handshake (no verify) | Overall |
| --------------- | ------------- | ------------ | ------------------------- | ------- |
| defaults        | ✅ 401        | ✅ 200 OK    | ⚠️ Verified disabled      | Partial |
| disable-rerank  | ✅ 401        | ✅ 200 OK    | ⚠️ Verification disabled  | Partial |
| disable-sparse  | ✅ 401        | ✅ 200 OK    | ⚠️ Verification disabled  | Partial |
| disable-both    | ✅ 401        | ✅ 200 OK    | ⚠️ Verification disabled  | Partial |
| enable-synonyms | ✅ 401        | ✅ 200 OK    | ⚠️ Verification disabled  | Partial |

**Certificate Generation:** cryptography library (RSA 2048-bit, SHA256, self-signed, 1-day validity)  
**SSL Context:** Configured with `--no-verify-tls` (development mode; skips certificate verification)  
**Mock Ports:** 19090-19094 (one per configuration to avoid conflicts)

#### Validation Details

##### Authentication Required Check

- Test: Access endpoint without credentials
- Expected: HTTP 401 Unauthorized
- Result: ✅ PASS on all 5 configurations
- Evidence: Prometheus correctly enforces authentication

##### Authentication Success Check

- Test: Access endpoint with valid credentials (`prometheus_user:prometheus_pass`)
- Expected: HTTP 200 OK with metrics payload
- Result: ✅ PASS on all 5 configurations
- Evidence: Valid credentials accepted, metrics served correctly

##### TLS Enforcement Check

- Test: HTTPS connection establishment with self-signed certificate
- Expected: Successful TLS handshake with certificate verification
- Result: ⚠ Partial – handshakes succeed in mock mode while verification remains disabled (`--no-verify-tls`)
- Certificate: Generated via `cryptography` library (Python-native X.509)
- SSL Context: `check_hostname=False`, `verify_mode=ssl.CERT_NONE` (when `--no-verify-tls` used)
- Evidence: TLS connections successfully established for all configurations in mock mode; staging validation still required.

#### Historical Results (Development Iterations)

**HTTP Mock Server Validation (`prometheus-validation-http-20251025.json`):**

- ✅ Authentication required (401 without credentials) - PASS
- ✅ Valid credentials accepted (200 with basic auth) - PASS
- ❌ TLS enforcement (HTTP endpoint detected) - EXPECTED FAIL

**Initial HTTPS Attempt (`prometheus-validation-https-20251025.json` - first version):**

- ❌ All checks failed - SSL handshake failure
- Root cause: SSL context not properly configured in validation methods
- Fix applied: Added SSL context with `check_hostname=False` and `verify_mode=CERT_NONE`

**Current HTTPS Validation (v2 - mock mode, verification disabled):**

- ⚠ Reports show `overall_status = PASS` because TLS handshakes succeed without verifying certificates; treat as partial coverage until staging evidence is captured.
- Certificate generation: Enhanced with `cryptography` library
- SSL context: Properly configured in `urlopen()` calls with verification disabled for mock environments
- **Status:** Provides development confidence only; production readiness depends on staging runs with verification enabled.

## Test Environment

- **Regression harness:** Python 3.12.10, `pytest -m regression_harness`, Docling mini corpus (`tests/data/regression/docling-mini/`)
- **Mock Prometheus:** See Prometheus validation section (unchanged)
- **Collections Tested:** Docling documentation (full + mini corpus variants)

## Next Steps

### CI Integration Status: ✅ COMPLETE

Workflow `.github/workflows/telemetry-smoke-matrix.yml` has been updated with:

1. ✅ `--mock-https` flag added for HTTPS validation
2. ✅ `--no-verify-tls` flag for self-signed certificates
3. ✅ Exit code 2 treated as non-fatal (warnings allowed)
4. ✅ All 5 matrix configurations run HTTPS validation in mock mode (`--no-verify-tls`)
5. ✅ Validation reports auto-generated and committed for mock coverage; staging artefacts pending

### Staging Validation (DEFERRED)

When staging infrastructure with CA-signed certificates is deployed:

#### Validation Commands

**Certificate Chain Inspection:**

```bash
openssl s_client -connect staging-prometheus.example.com:9090 -showcerts
```

Expected: Valid certificate chain from trusted CA

**Endpoint Validation (without --no-verify-tls):**

```bash
python scripts/validate_prometheus_endpoint.py \
  --endpoint https://staging-prometheus.example.com:9090/metrics \
  --username <staging-user> \
  --password <staging-password> \
  --output prometheus-validation-staging-$(date +%Y%m%d).json
```

Expected: 3/3 PASS with proper certificate verification

**Authentication Test:**

```bash
curl -u user:pass https://staging-prometheus.example.com:9090/metrics
```

Expected: HTTP 200 with metrics payload

**TLS Enforcement Test:**

```bash
curl https://staging-prometheus.example.com:9090/metrics
```

Expected: HTTP 401 Unauthorized

## References

- Security controls documentation: `docs/qa/assessments/1.4-security-controls-20251025.md`
- Telemetry smoke assessment: `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`
- Observability architecture: `docs/architecture/observability.md`
- Rerank/sparse signals runbook: `docs/telemetry/rerank_sparse_signals.md`

# Telemetry Smoke Matrix Evidence Manifest

Generated: 2025-10-25  
Workflow: Manual execution prior to CI automation  
Purpose: Prometheus validation and telemetry smoke matrix evidence for Story 1.4

## Evidence Files

### CLI Test Artifacts (5 toggle combinations)

- `cli-output-defaults-20251025.txt` - Default configuration (both stages enabled)
- `cli-output-disable-rerank-20251025.txt` - Rerank disabled, sparse enabled
- `cli-output-disable-sparse-20251025.txt` - Sparse disabled, rerank enabled
- `cli-output-disable-both-20251025.txt` - Both stages disabled (legacy dense-only)
- `cli-output-enable-synonyms-20251025.txt` - Explicit enable flags (synonym validation)

### Processing Summaries (5 JSON files)

- `processing_summary_defaults_20251025.json` - Default configuration results
- `processing_summary_disable_rerank_20251025.json` - Rerank disabled results
- `processing_summary_disable_sparse_20251025.json` - Sparse disabled results
- `processing_summary_disable_both_20251025.json` - Both stages disabled results
- `processing_summary_enable_synonyms_20251025.json` - Enable synonym validation results

### Prometheus Validation Reports

- `prometheus-validation-mock-20251025.json` - Mock server validation results

## Validation Summary

### CLI Execution Results (5 toggle combinations)

- ✅ defaults
- ✅ disable-rerank
- ✅ disable-sparse
- ✅ disable-both
- ✅ enable-synonyms

### Prometheus Validation Results

Mock server validation executed with the following results:

- ✅ Authentication required (401 without credentials)
- ✅ Valid credentials accepted (200 with basic auth)
- ⚠️ TLS connection validation (expected failure in mock mode with HTTP endpoint)

**Note:** The TLS enforcement check fails in mock mode as expected since the mock server uses HTTP. For staging/production validation with real HTTPS endpoints, see `docs/qa/assessments/1.4-security-controls-20251025.md`.

## Test Environment

- **Mode:** Mock (CI-compatible, no staging infrastructure required)
- **Mock Server Port:** 19090
- **Authentication:** Basic auth with test credentials
- **Collections Tested:** Docling corpus (chunked documentation)

## Next Steps

The following improvements will be implemented in CI automation (`.github/workflows/telemetry-smoke-matrix.yml`):

1. Fix workflow to use `--chunked-dir` flag instead of positional argument
2. Install actual dependencies from project requirements
3. Generate validation reports for all toggle combinations
4. Auto-commit evidence on workflow execution

## References

- Security controls documentation: `docs/qa/assessments/1.4-security-controls-20251025.md`
- Telemetry smoke assessment: `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`
- Observability architecture: `docs/architecture/observability.md`
- Rerank/sparse signals runbook: `docs/telemetry/rerank_sparse_signals.md`

# Regression Harness Evidence Manifest

**Generated:** 2025-10-30  
**Harness Command:** `pytest -m regression_harness -v --tb=short`  
**Corpus:** `tests/data/regression/docling-mini/` (docling mini deterministic set)

## Evidence Contents

- `metrics/default-on_metrics_baseline.json` — latency, GPU, and fallback guardrails
  for the default-on run (10% drift budget).
- `runs/<YYYYMMDD>/default_on/processing_summary_default-on_<stamp>.json` — CLI
  processing summary generated through the harness stub.
- `runs/<YYYYMMDD>/default_on/qdrant_default-on_<stamp>.jsonl` — deterministic
  default-on export mirroring live CLI schema.
- Equivalent `rerank_disabled`, `sparse_disabled`, and `fallback_force` folders
  containing per-scenario summaries, qdrant payloads, and CLI logs.

## Refresh Workflow

1. Export output staging variables (example timestamp `20251030`).

   ```bash
   export REGRESSION_HARNESS_OUTPUT_DIR=docs/qa/assessments/4.3-regression-harness/20251030
   export REGRESSION_HARNESS_TIMESTAMP=20251030
   ```

2. Execute the harness marker:

   ```bash
   pytest -m regression_harness -v --tb=short
   ```

3. Confirm each scenario directory contains a processing summary, qdrant export,
   and CLI log with timestamped names (`default-on`, `rerank-disabled`,
   `sparse-disabled`, `fallback`).

4. Run metrics verification (mirrors CI consolidation step):

   ```bash
   python scripts/validate_evidence_integrity.py --bundle "$REGRESSION_HARNESS_OUTPUT_DIR"
   python - <<'PY'
   import json, pathlib

   baseline = json.loads(pathlib.Path(
       "docs/qa/assessments/4.3-regression-harness/metrics/default-on_metrics_baseline.json"
   ).read_text())

   summary_path = sorted(pathlib.Path(
       "docs/qa/assessments/4.3-regression-harness"
   ).glob("*/default_on/processing_summary_default-on_*.json"))[-1]

   summary = json.loads(summary_path.read_text())
   latency = summary["performance_baseline"]["latency_seconds"]
   gpu_peak = summary["performance_baseline"]["gpu"]["peak_memory_used_gb"]
   fallback = summary["rerank_run"]["fallback_count"]

   assert abs(latency - baseline["latency_seconds"]) <= baseline["latency_seconds"] * 0.10
   assert abs(gpu_peak - baseline["gpu_peak_gb"]) <= baseline["gpu_peak_gb"] * 0.10
   assert fallback == baseline["fallback_count"]
   print(f"Metrics verified for {summary_path}")
   PY
   ```

## Guardrails

- Latency must remain within ±10% of the baseline (2.4 s).
- GPU peak memory must remain within ±10% of the baseline (3.2 GB).
- Rerank fallback count must stay at 0 for default-on runs.

## References

- Regression harness story: `docs/stories/4.3.story.md`
- Harness README: `docs/qa/assessments/4.3-regression-harness/README.md`
- Metrics baseline: `docs/qa/assessments/4.3-regression-harness/metrics/default-on_metrics_baseline.json`

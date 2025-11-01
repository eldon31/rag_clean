# Telemetry Smoke Test Evidence - Reproduction Guide

**Last Updated:** 2025-10-30  
**Issue:** DOC-220, EVI-121 - CLI command and evidence path corrections

## Current Status

⚠️ **IMPORTANT**: The CLI output logs in this directory (`cli-output-*.txt`) reference `Raw\Docling` as the chunked directory. This path is **incorrect** and does not match the repository structure. The logs were generated with an older, non-working flag configuration and need to be regenerated.

ℹ️ **CPU fallback evidence**: Added `unit-test-results-20251030.txt` capturing `pytest` results for telemetry smoke and processing summary suites. These tests validate metrics and summary code paths without running the GPU-dependent CLI.

## Correct Reproduction Commands

The repository contains chunked data under `Chunked/Docling`, not `Raw/Docling`. Use these commands to reproduce the telemetry smoke test matrix:

### Run 1: Default Configuration (Both Enabled)

```bash
python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling
```

Expected output file: `cli-output-defaults-20251025.txt`

### Run 2: Rerank Disabled

```bash
python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling --disable-rerank
```

Expected output file: `cli-output-disable-rerank-20251025.txt`

### Run 3: Sparse Disabled

```bash
python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling --disable-sparse
```

Expected output file: `cli-output-disable-sparse-20251025.txt`

### Run 4: Both Disabled (Legacy Dense-Only Mode)

```bash
python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling --disable-rerank --disable-sparse
```

Expected output file: `cli-output-disable-both-20251025.txt`

### Run 5: Explicit Enable Flags (Synonym Validation)

```bash
python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling --enable-rerank --enable-sparse
```

Expected output file: `cli-output-enable-synonyms-20251025.txt`

## Important Notes

1. **CLI Flag**: The script only supports `--chunked-dir`, not `--input-dir`. The old documentation referenced the wrong flag.

2. **Corpus Path**: The correct path is `Chunked/Docling` relative to the repository root. This directory contains 46 chunk files for the Docling documentation corpus.

3. **Output Redirection**: When regenerating evidence, capture stdout and stderr using:

   ```bash
   python scripts/embed_collections_v6.py --chunked-dir Chunked/Docling 2>&1 | Tee-Object -FilePath docs/qa/assessments/1.4-telemetry-smoke-evidence/cli-output-defaults-20251025.txt
   ```

4. **GPU Requirement**: These tests are designed to run with GPU acceleration. CPU-only execution will be extremely slow (5+ seconds per chunk batch) and may not complete in reasonable time.

5. **Processing Summaries**: Each CLI run generates a corresponding `processing_summary_*.json` file that should be captured from the output directory.

## What Was Fixed

- ✅ Updated `docs/qa/assessments/1.4-telemetry-smoke-20251025.md` to use correct `--chunked-dir Chunked/Docling` commands
- ⏳ Evidence logs (`cli-output-*.txt`) still reference old paths - require regeneration with GPU

## Next Steps for Complete Fix

1. Run the 5 command matrix above on a system with GPU
2. Capture CLI outputs to the respective `cli-output-*.txt` files
3. Copy the generated `processing_summary_*.json` files to this directory
4. Verify the Prometheus validation JSON files remain valid
5. Update MANIFEST.md with regeneration timestamp

## Related Issues

- **DOC-220** (High): Runbook CLI commands corrected (FIXED)
- **EVI-121** (Medium): Evidence logs need regeneration (PENDING - GPU required)

## References

- Story: `docs/stories/1.4.story.md`
- Gate: `docs/qa/gates/1.4-finalize-default-on-performance-observability-baselines.yml`
- Assessment: `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`

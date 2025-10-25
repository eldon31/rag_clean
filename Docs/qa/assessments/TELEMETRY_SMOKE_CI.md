# Telemetry Smoke Matrix CI Automation

## Overview

Automated GitHub Actions workflow that regenerates telemetry smoke matrix artifacts to keep evidence fresh across releases.

## Workflow: `.github/workflows/telemetry-smoke-matrix.yml`

### Triggers

1. **Push to main** - When embedding pipeline code changes
   - `scripts/embed_collections_v6.py`
   - `processor/**/*.py`
   - `tests/test_telemetry_smoke.py`

2. **Pull Requests** - Validation before merge

3. **Schedule** - Weekly on Sundays at 2 AM UTC

4. **Manual Dispatch** - On-demand via GitHub Actions UI

### Toggle Matrix Coverage

The workflow runs 5 parallel jobs, one for each toggle combination:

| Configuration | CLI Flags | Description |
|---------------|-----------|-------------|
| `defaults` | _(none)_ | Default config (both stages enabled) |
| `disable-rerank` | `--disable-rerank` | Sparse enabled, rerank disabled |
| `disable-sparse` | `--disable-sparse` | Rerank enabled, sparse disabled |
| `disable-both` | `--disable-rerank --disable-sparse` | Legacy dense-only mode |
| `enable-synonyms` | `--enable-rerank --enable-sparse` | Explicit enable flags (synonym validation) |

### Artifacts Generated

Each job produces:
- **CLI output log**: `cli-output-{config}-{timestamp}.txt`
- **Processing summary**: `processing_summary_{config}_{timestamp}.json`

Total: **10 files** (5 CLI logs + 5 JSON summaries)

### Validation Steps

Per job:
1. ✅ Verify Docling test corpus exists
2. ✅ Run CLI with toggle flags
3. ✅ Validate JSON structure (required keys)
4. ✅ Run regression tests (`tests/test_telemetry_smoke.py`)
5. ✅ Upload artifacts (90-day retention)

After all jobs:
6. ✅ Consolidate evidence files
7. ✅ Generate manifest
8. ✅ Commit changes (if artifacts differ from previous run)

### Output Locations

- **Evidence directory**: `docs/qa/assessments/1.4-telemetry-smoke-evidence/`
- **Manifest**: `docs/qa/assessments/1.4-telemetry-smoke-evidence/MANIFEST.md`
- **GitHub Artifacts**: 90-day retention for each run

### Automation Benefits

1. **Fresh Baselines**: Weekly regeneration ensures artifacts reflect current codebase
2. **Regression Detection**: Catches breaking changes in toggle behavior
3. **Audit Trail**: Git commits provide versioned evidence history
4. **Zero Manual Effort**: Fully automated after initial setup

### Manual Triggering

Via GitHub Actions UI:
1. Navigate to **Actions** → **Telemetry Smoke Matrix**
2. Click **Run workflow**
3. Select branch (default: `main`)
4. Optionally set `force_regenerate: true`

Via API:
```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/telemetry-smoke-matrix.yml/dispatches \
  -d '{"ref":"main","inputs":{"force_regenerate":"true"}}'
```

### Monitoring

- **Workflow status**: Check GitHub Actions tab
- **Artifact uploads**: Review job summaries
- **Commit history**: `git log --grep="chore(qa): Refresh telemetry smoke"`

### Troubleshooting

**Job fails at "Verify test corpus":**
- Ensure `Chunked/Docling` directory exists with JSON chunk files
- Test corpus required for realistic validation

**JSON validation fails:**
- Check `scripts/embed_collections_v6.py` for breaking changes to output structure
- Required keys: `collection_name`, `chunk_count`, `timestamp`, `feature_toggles`

**Regression tests fail:**
- Review `tests/test_telemetry_smoke.py` for test failures
- May indicate toggle behavior regressions

**No changes committed:**
- Artifacts identical to previous run (expected behavior)
- Forces manual regeneration with `force_regenerate: true`

## Integration with Story 1.4

This automation fulfills AC4 requirement: "Toggle matrix evidence remains fresh across releases via CI automation."

**Related Files:**
- Story: `docs/stories/1.4.story.md`
- QA Gate: `docs/qa/gates/1.4-finalize-default-on-performance-observability-baselines.yml`
- Assessment: `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`

## Configuration

No additional setup required. Workflow runs automatically on triggers.

**Optional**: Adjust schedule cron expression in workflow file:
```yaml
schedule:
  - cron: '0 2 * * 0'  # Sundays at 2 AM UTC
```

## Future Enhancements

- [ ] Add Slack/email notifications for failures
- [ ] Compare artifacts against baseline thresholds (latency regression alerts)
- [ ] Generate ASCII charts from processing summaries
- [ ] Publish artifacts to artifact repository (Nexus/Artifactory)

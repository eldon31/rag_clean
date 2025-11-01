# Sprint Change Proposal – Default-On Observability Consolidation

**Date:** 2025-10-25  
**Prepared by:** Sarah (Product Owner)

## 1. Analysis Summary

### Trigger & Context

- QA reopened Stories 1.1–1.3 after default-on rerank/sparse shipped without staging baselines, GPU alert automation, sparse fallback evidence, CLI doc refresh, or telemetry smoke outputs.
- Story 1.4 (Finalise Default-On Performance & Observability Baselines) was created to consolidate these gaps but is still "Not Started"; Epic 1 remains blocked until the outstanding observability deliverables land.
- No technical regressions surfaced; the missing work is operational evidence, automation wiring, and documentation updates demanded by the QA gates.

### Epic Impact

- Epic 1 stays structurally valid but cannot close until Story 1.4 inherits and completes the reopened deliverables from Stories 1.1–1.3.
- Downstream epics expecting production-ready observability must wait for Epic 1 sign-off; no reordering or new epics required once Story 1.4 closes.

### Artifact Impact

- `docs/architecture/observability.md` and `docs/telemetry/rerank_sparse_signals.md` still contain "pending follow-up" placeholders; they require concrete baseline numbers, alert workflows, and smoke evidence links.
- QA gate files for Stories 1.1–1.3 (under `docs/qa/gates/`) cite Story 1.4 as the closure path and need updating once evidence is attached.
- CLI/operator documentation (help output, Story 1.2 references) must incorporate flag synonyms and observability guidance.
- QA evidence folders lack staging reports, alert validation artifacts, and telemetry smoke outputs.

### Recommended Path Forward

- Adopt Option 1 (Direct Adjustment): execute Story 1.4 as the consolidation vehicle, delivering the pending baselines, alert automation, regression coverage, documentation updates, and QA artifacts. No rollback or scope reduction is advised.

### PRD MVP Impact

- MVP goals remain unchanged; observability baselines and alerting were already expected. Completing Story 1.4 realigns the implementation with the existing MVP definition.

## 2. Proposed Edits to Project Artifacts

| Artifact | Proposed Update | Notes |
| --- | --- | --- |
| `docs/stories/1.4.story.md` | Expand acceptance criteria and tasks to explicitly cover staging baseline evidence, alert automation outputs, sparse fallback matrix, CLI help/docs refresh, telemetry smoke run artifacts, and QA links. Add cross-references to the specific files listed below. | Clarifies success definition and ensures QA sign-off is traceable. |
| `docs/architecture/observability.md` | Replace "pending follow-up" placeholders with captured latency/VRAM baselines, document warning/error thresholds, describe alert routing, and link to telemetry smoke appendix plus CLI toggle guidance. | Locks architecture doc to the delivered observability posture. |
| `docs/telemetry/rerank_sparse_signals.md` | Insert baseline tables/graphs, alert screenshots or references, sparse fallback matrix results, and CLI toggle doc updates. Note evidence sources and Story 1.4 ownership. | Graduates runbook from draft to operational guide. |
| `scripts/embed_collections_v6.py` help + operator docs | Add flag synonyms (e.g., `--enable-rerank` / `--enable-sparse`) or document why defaults-on persist, and point operators to the telemetry runbook for alert interpretation. | Closes Story 1.2 doc gap and improves rollout clarity. |
| QA gate files (`docs/qa/gates/1.1-*.yml`, `1.2-*.yml`, `1.3-*.yml`) | Upon completion, move gates back to `PASS`, resolve findings (`OBS-301`, `PERF-202`, `MNT-203`, `OBS-310`, `MET-311`), and cite new evidence files. | Signals QA acceptance and removes block on Epic 1. |
| New QA evidence (`docs/qa/assessments/1.4-baselines-20251025.md`, `docs/qa/assessments/1.4-alert-validation-20251025.md`, `docs/qa/assessments/1.4-telemetry-smoke-20251025.md`) | Capture staging latency/VRAM reports (with screenshots or metric exports), alert fire/clear logs, CLI telemetry smoke matrix outputs (enabled/disabled toggles), and sparse fallback regression summaries. | Provides auditable proof for QA and future audits. |

## 3. High-Level Action Plan & Ownership

1. **Staging Baselines (Observability Lead, QA)**  
   - Execute default-on staging runs capturing latency, VRAM, sparse coverage, and rerank metrics.  
   - Store evidence in `docs/qa/assessments/1.4-baselines-20251025.md` and embed summarized numbers in architecture/runbook docs.  
   - Target completion: 2025-10-27.

2. **GPU Alert Automation (Observability Lead, Infra)**  
   - Configure Prometheus rules for warning (>11.5 GB) and critical (>12 GB) thresholds; validate alert routing end-to-end.  
   - Add regression test asserting alert emission when telemetry exceeds thresholds; document workflow in runbook.  
   - Store validation proof in `docs/qa/assessments/1.4-alert-validation-20251025.md`.  
   - Target completion: 2025-10-28.

3. **Sparse Fallback & CLI Documentation (Dev Lead, Technical Writer)**  
   - Extend regression matrix covering degraded inputs, metadata fallback, and toggle combinations; include outputs in telemetry smoke evidence.  
   - Update CLI help text, operator docs, and Story 1.2 references to reflect flag synonyms and observability posture.  
   - Target completion: 2025-10-29.

4. **Telemetry Smoke Suite (QA, Dev)**  
   - Run CLI + telemetry matrix across all toggle states (both enabled, rerank disabled, sparse disabled, both disabled); capture processing summaries, spans, metrics, and CLI output.  
   - Save results to `docs/qa/assessments/1.4-telemetry-smoke-20251025.md` and link from runbook/architecture docs.  
   - Target completion: 2025-10-29.

5. **Documentation & Gate Updates (Product Owner, QA)**  
   - Refresh `docs/stories/1.4.story.md`, architecture/runbook docs, and QA gates with new evidence references.  
   - Confirm QA gates 1.1–1.3 return to `PASS` and Epic 1 can move to closure.  
   - Target completion: 2025-10-30.

Dependencies: staging environment availability, telemetry stack access (Prometheus/Grafana), coordination with QA for evidence verification.

## 4. Checklist Status Snapshot

- Section 1 (Trigger & Context): ✅ Completed (Stories 1.1–1.3 reopen; Story 1.4 consolidates)
- Section 2 (Epic Impact): ✅ Epic 1 blocked pending Story 1.4 completion
- Section 3 (Artifact Impact): ✅ Architecture, telemetry runbook, CLI docs, QA gates, and evidence all require updates
- Section 4 (Path Forward): ✅ Option 1 – Execute Story 1.4 deliverables; no rollback or rescope required
- Section 5 items captured above (Issue Summary, Epic Impact, Artifact Adjustments, Recommended Path, MVP Impact, Action Plan, Handoff)
- Section 6 (Final Review & Handoff): Pending user approval of this proposal

## 5. Handoff & Next Steps

- **User Approval:** Review and approve this proposal to authorise Story 1.4 execution and documentation updates.  
- **Implementation:** Assign Story 1.4 owners, schedule staging runs, and produce the evidence/docs listed in the action plan.  
- **QA Coordination:** QA to validate new artifacts, update gate files, and unblock Epic 1 upon completion.  
- **Monitoring:** After rollout, monitor GPU alert dashboards and telemetry metrics to ensure baselines remain valid; capture any deviations in future QA assessments.

Once these steps are complete and QA gates revert to `PASS`, proceed to close Stories 1.1–1.4 and mark Epic 1 as ready. Any need for broader scope adjustments should be escalated to the PM/Architect, but no such replanning is currently required.

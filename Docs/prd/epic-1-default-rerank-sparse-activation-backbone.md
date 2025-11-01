# Epic 1: Default Rerank & Sparse Activation Backbone

Expanded Goal: Establish configuration, CLI, and runtime defaults that activate rerank and sparse stages on every run while preserving dense-only compatibility through explicit opt-outs, ensuring the control plane and monitoring surfaces recognize the new baseline.

## Story 1.1 Default-On Configuration Wiring

As a deployment operator,
I want rerank and sparse stages enabled automatically through configuration defaults,
so that every execution benefits from the enhanced retrieval stack without manual flag work.

### Acceptance Criteria (Story 1.1)

1: Configuration loaders default to enabling rerank and sparse stages while honoring override switches (env vars, config files).
2: Unit tests cover default-on behavior and explicit opt-out paths.
3: Documentation highlights default settings and how to disable stages.

## Story 1.2 CLI and Runtime Toggle Integration

As a CLI operator,
I want the command-line interface and runtime logging to reflect the default-on rerank/sparse behavior,
so that executions surface clear status and allow opt-outs for exceptional runs.

### Acceptance Criteria (Story 1.2)

1: `embed_collections_v6.py` exposes parameters that document default-on behavior and allow disabling rerank/sparse.
2: Run summaries/logs show rerank and sparse activation states and devices used.
3: Telemetry control-plane entries confirm defaults were applied, with regression tests verifying dense-only parity when disabled.

## Story 1.3 Telemetry & Monitoring Baseline Updates

As a telemetry consumer,
I want monitoring dashboards and runtime metrics to treat rerank and sparse as first-class stages,
so that default executions emit expected spans and operators can trace failures quickly.

### Acceptance Criteria (Story 1.3)

1: Telemetry emits stage indicators when rerank/sparse are active, capturing GPU leasing metadata per stage.
2: Dashboards or runbooks document new metrics and default expectations.
3: Smoke test run verifies telemetry coverage with rerank/sparse enabled and disabled.

## Follow-up Required

Stories 1.1 through 1.3 remain open for staging baseline publication, GPU alerting automation, expanded sparse fallback coverage, CLI documentation updates, and end-to-end telemetry validation. These gaps are consolidated under Story 1.4 "Finalize Default-On Performance & Observability Baselines" and must be completed before declaring the epic fully done.


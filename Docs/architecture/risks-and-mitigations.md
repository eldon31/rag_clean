# Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| GPU OOM during rerank batches | Pipeline aborts mid-run | Dynamic batch sizing, leasing cleanup, retry with reduced candidate count. |
| Sparse inference latency increases | Total run time extends beyond SLO | Keep sparse models CPU-first; cache hot indices on GPU; allow fallback to metadata. |
| Export parsers break on new schema | Downstream tooling fails | Maintain additive schema, version manifests, update documentation/tests, provide feature flags. |
| Telemetry volume spikes | Monitoring costs/log noise | Sample or aggregate spans; expose config to adjust logging level. |

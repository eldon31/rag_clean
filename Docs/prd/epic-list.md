# Epic List

- Epic 1: Default Rerank & Sparse Activation Backbone – Ship default-on toggles, CLI/config updates, and control-plane plumbing so rerank and sparse run every execution without breaking dense-only parity when explicitly disabled.
- Epic 2: Sparse Generator & Fusion Upgrade – Implement live sparse inference inside the batch runner, fusing results and handling fallbacks while honoring GPU leasing across devices.
- Epic 3: CrossEncoder Rerank Execution & Telemetry – Execute rerank after dense+sparse fusion, persist ranked outputs, and expose telemetry covering latency, GPU peaks, and fallback states.
- Epic 4: Export Schema, Regression Hardening, and Ensemble Documentation – Version exports, expand regression coverage, and publish the observed ensemble flow documentation to anchor future maintainers.

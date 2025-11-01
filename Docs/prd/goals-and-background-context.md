# Goals and Background Context

### Goals
- Deliver a production-ready CrossEncoder rerank stage that slots into the Ultimate Embedder without regressing the current dense-only flow.
- Upgrade sparse helper execution to generate live sparse vectors with graceful fallbacks and aligned export artifacts.
- Extend CLI configuration, telemetry, and export schemas so rerank and sparse stages run by default and surface as first-class signals while staying overrideable when needed.
- Maintain the 12 GB-per-GPU ceiling across Kaggle dual-T4 runs through adaptive batching and leasing safeguards.

### Background Context
RAG_CLEAN already processes heterogeneous document batches into dense embeddings and knowledge surfaces using the exclusive ensemble pipeline defined in the architecture plan. The brownfield enhancement initiative reactivates previously scaffolded CrossEncoder rerank and sparse pipelines so retrieval quality improves without rewriting the mature orchestration, telemetry, or export layers. This work must fit within the existing GPU-leasing constraints and keep the CLI/operator experience familiar while delivering richer ranking metadata.

Key constraints include the hard 12 GB VRAM ceiling on Kaggle GPUs, additive-only schema changes for downstream consumers, and preservation of privacy controls around telemetry. Success requires harmonizing dense, sparse, and rerank stages inside the Ultimate Embedder so operators can toggle them per run and still rely on the established deployment scripts and dashboards.

### Change Log

| Date | Version | Description | Author |
| --- | --- | --- | --- |
| 2025-10-23 | 0.1 | Initial draft capturing goals, context, and constraints for the rerank and sparse enhancement PRD. | John (PM) |

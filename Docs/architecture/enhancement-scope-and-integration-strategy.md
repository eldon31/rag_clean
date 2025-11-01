# Enhancement Scope and Integration Strategy

### Enhancement Overview

**Enhancement Type:** CrossEncoder Rerank and Sparse Inference Integration

**Scope:** Activate the full CrossEncoder reranking pipeline and convert sparse vector generation from metadata echoing to live inference, ensuring GPU leasing, telemetry, CLI workflow, and export schemas treat dense, sparse, and rerank stages as first-class citizens.

**Integration Impact:** High – touches model loading, batch runner sequencing, GPU leasing lifecycle, export runtime, telemetry schema, CLI interface, and optional service entry points.

### Integration Approach

- **Code Integration Strategy:**
  - Extend `UltimateKaggleEmbedderV4`/`ModelManager` to hydrate CrossEncoder and sparse models via existing registries, staging to CPU by default.
  - Enhance `BatchRunner` to schedule rerank passes (post dense/sparse fusion) and live sparse inference, reusing GPU leasing helpers to stay under 12 GB.
  - Wire `RerankPipeline` into CLI (`embed_collections_v6.py`) and any service adapters so rerank execution is driven by `RerankingConfig` toggles.
- **Database Integration:**
  - Continue exporting artifacts as JSON/JSONL bundles; append optional rerank/sparse sections without altering persistent tables.
- **API Integration:**
  - Expose rerank/sparse toggles in CLI now; later surface via FastAPI endpoints with Pydantic request/response models.
- **UI Integration:**
  - Update CLI/log output to report rerank model, batch size, latency, GPU peak usage, and sparse model activation. Telemetry dashboards consume new signals; no separate GUI changes required.

### Compatibility Requirements

- **Existing API Compatibility:** Rerank and sparse stages run by default, with opt-out switches preserving dense-only parity when explicitly requested.
- **Database Schema Compatibility:** Export schema remains additive—legacy parsers bypass unknown keys.
- **UI/UX Consistency:** CLI progress and summaries follow current exclusive-mode style, appending rerank/sparse metrics without reordering existing lines.
- **Performance Impact:** Respect 12 GB ceiling by dynamically sizing rerank batches, limiting candidate counts under latency pressure, and keeping sparse inference CPU-first with GPU-cached hot shards only.

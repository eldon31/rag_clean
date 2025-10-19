# Sparse & Hybrid Retrieval Expansion

This working note tracks the tasks, open questions, and integration ideas for bringing richer sparse and hybrid retrieval to the knowledge base.

## Goals

- Add production-ready sparse vectors (SPLADE + miniCOIL) alongside existing dense CodeRank embeddings.
- Preserve chunker-produced lexical metadata while allowing model-driven sparse encodings.
- Introduce optional reranking to the MCP server to improve result ordering.

## Current State (2025-10-20)

- Chunking (`processor/enhanced_ultimate_chunker_v3.py`) emits `sparse_features` derived from token frequency stats and now runs with semantic scoring disabled by default (no SentenceTransformer dependency).
- Embedding (`processor/kaggle_ultimate_embedder_v4.py`) now exports dual dense vectors (CodeRank 768D primary + BGE-small 384D companion) and hashes cached sparse payloads; external sparse models still pending.
- Qdrant collections are dense-only (`*_v4_nomic_coderank`). Hybrid scoring uses lexical bonuses computed at query time.

## Research Tasks

1. **SPLADE via FastEmbed**
   - Confirm ONNX support/performance for `prithivida/Splade_PP_en_v1` on Kaggle GPU.
   - Assess memory footprint and batching strategy when combined with dense models.
   - Decide on storage format: inline sparse vectors vs. JSON sidecar to be merged during upload.

2. **miniCOIL Integration**
   - Reproduce Qdrant guide: configure `SparseVectorParams` with `Modifier.IDF`, upsert via `models.Document`.
   - Validate average document length heuristics for chunk-level granularity.
   - Explore hybrid scoring weight between miniCOIL sparse channel and dense embeddings.

3. **Rerankers (FastEmbed Cross-Encoders)**
   - Benchmark latency for `jinaai/jina-reranker-v2-base-multilingual` on typical top-k (10/20) batches.
   - Determine activation workflow (feature flag? query param?).
   - Ensure caching strategy aligns with reranker inputs to avoid redundant inference.

## Implementation Sketch

- **Chunking**
  - Keep `sparse_features` generation (useful for keyword highlighting) and rely on heuristic semantic scoring unless a dedicated encoder is explicitly provided.
  - Optionally enrich metadata with SPLADE top terms decoded for interpretability.

- **Embedding Pipeline (Kaggle)**
  - Add toggles for `generate_splade` and `generate_minicoil` alongside dense run.
  - Enable `BAAI/bge-small-en-v1.5` as the supplemental lightweight dense encoder (384-dim, fast inference, solid general-domain recall); keep CodeRank as primary. ✅
  - Stream sparse outputs to artifacts (e.g., `Embeddings/<collection>/sparse_splade.jsonl`).
  - Capture per-model stats (token throughput, sparsity).

- **Upload Scripts**
  - Extend collection provisioning to define multiple vector channels (`dense`, `splade`, `minicoil`).
  - Map exported sparse artifacts to appropriate Qdrant upsert calls (FastEmbed convenience vs. manual payload).
  - Version collections with explicit suffixes (e.g., `_v5_nomic_coderank_splade`).

- **MCP Server**
  - Update `resolve_collection_name` logic to accommodate new suffixes.
  - Allow hybrid search params to include sparse channel weights.
  - Introduce reranker stage post vector search (configurable per request).

## Open Questions

- What is the acceptable increase in index size/latency for hybrid collections?
- Do we store SPLADE/minicoIL vectors for every chunk or only selected corpora?
- How do we expose sparse-powered search to clients (new tool, optional flags)?
- Should we keep hashed TF features once model-based sparse vectors are present?

## Next Steps

1. Prototype SPLADE embedding in isolation; record resource usage and output format.
2. Run a miniCOIL end-to-end demo against a staging Qdrant collection.
3. Validate dual dense exports (CodeRank + BGE-small) by smoke-testing new upload script and confirming Qdrant multi-vector layout.
4. Draft MCP server feature flags for reranking, ensuring backwards compatibility.

> Working document — update as research progresses.

# Chunker Enhancement Notes

_Date: 2025-10-20_

## Objectives
- Streamline the existing hierarchical chunker for consistent chunk sizes without sacrificing document structure context.
- Introduce configuration switches for upcoming library integrations (Docling hybrid chunker variants, sentence-transformers streaming utilities, future sparse rerankers).
- Capture actionable takeaways that guide iterative enhancements to chunking and embedding workflows.

## Current Baseline
- `enhanced_ultimate_chunker_v3.py` delivers lightweight structural segmentation with optional semantic scoring disabled by default.
- Export pipeline now emits multivector sidecars for dense + late-interaction embeddings, enabling richer Qdrant indexing.
- Upload script scaffolding accounts for multivector payloads but still needs validation with real exports.

## Key Takeaways
- **Preserve structure first:** Maintain headings, list context, and table boundaries; only fallback to text splitting when limits require it.
- **Prefer medium chunk windows:** Target 512–1024 token spans with 100–150 overlap to balance recall and storage cost.
- **Propagate provenance:** Carry `doc_items`, heading hierarchy, and positional data into payloads for downstream rerankers.
- **Pair chunking with batching knobs:** Align Docling chunk outputs with SentenceTransformer `chunk_size` / `corpus_chunk_size` to avoid encoder OOM.
- **Surface multivector metadata:** Store comparator + dimension info so collection creation can stay in sync with exports.

## Near-Term Enhancements
1. Validate multivector-aware upload script by running against a fresh export set; confirm Qdrant vectors + payload integrity.
2. Expose CLI flags in the chunker pipeline for `max_tokens`, `overlap`, and semantic scorer toggles to simplify experimentation.
3. Add regression tests covering chunk size distribution and metadata preservation across mixed-format documents.

## Library Integration Backlog
- **Docling Core**: Evaluate `HybridChunker` presets for long-form technical manuals.
- **Sentence Transformers**: Wire in streaming encode helpers and Matryoshka truncation for memory savings.
- **Sparse Rerankers**: Prototype SPLADE or ColBERT-style integrations to enrich multivector payloads.
- **LLM Post-Processors**: Consider lightweight summarizers to attach abstractive previews alongside chunks.

## Risks & Mitigations
- **Schema drift** if chunk metadata evolves → version payload schema and add compatibility checks in upload script.
- **API rate limits** when layering new embedding services → centralize retry/backoff utilities.
- **Testing overhead** as chunker variants proliferate → invest in fixture-based document sets with golden chunk outputs.

## Open Questions
- Should overlap be adaptive based on section depth or kept global?
- Which additional vector stores (Milvus, Weaviate) warrant first-class exporters once chunker stabilizes?
- Do we need on-the-fly chunk filtering (e.g., heuristics to skip boilerplate) before embedding?

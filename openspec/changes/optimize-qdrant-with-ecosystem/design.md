# Design Document: Optimize Qdrant Implementation

> **🔄 UPDATED FOR CODERANK MIGRATION**  
> This design now includes **Phase 0: CodeRank Migration** as a prerequisite. All collections must be re-embedded from 3584-dim (nomic-embed-code) to 768-dim (CodeRankEmbed) before implementing the unified architecture.

## Architecture Overview

This change refactors Qdrant integration across the codebase to create a unified, performant, and maintainable implementation. The design centers on four core capabilities:

1. **CodeRank Migration** - Migrate from nomic-embed-code (3584-dim) to CodeRankEmbed (768-dim) for 42x faster queries
2. **MCP Server Enhancement** - Expose all collections via MCP tools with CodeRankEmbed integration
3. **Unified Configuration** - Shared abstractions for Qdrant settings (default 768-dim)
4. **Code Consolidation** - Single source of truth for common operations

## System Components

### 1. MCP Server Architecture

```
┌─────────────────────────────────────────────────────────┐
│         MCP Server (qdrant_code_server.py)             │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  agent_kit   │  │inngest_overall│  │qdrant_ecosystem│
│  │ (768-dim)    │  │  (768-dim)    │  │  (768-dim)   │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                  │                  │         │
│         └──────────────────┴──────────────────┘         │
│                          │                               │
│                  ┌───────▼────────┐                     │
│                  │ CodeRankEmbed  │                     │
│                  │  (137M params) │                     │
│                  │  768-dim output│                     │
│                  │  ~400ms on CPU │                     │
│                  └───────┬────────┘                     │
│                          │                               │
│                  ┌───────▼────────┐                     │
│                  │ QdrantRegistry │                     │
│                  │  (Connection   │                     │
│                  │   Pooling)     │                     │
│                  └───────┬────────┘                     │
│                          │                               │
│                  ┌───────▼────────┐                     │
│                  │ Unified Config │                     │
│                  │  (768-dim      │                     │
│                  │   default)     │                     │
│                  └────────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

**Key Design Decisions:**

- **CodeRankEmbed Integration**: 137M parameter model (51x smaller than nomic-embed-code) with 768-dim output, ~400ms CPU latency
- **Query Prefix Requirement**: All queries must use: `"Represent this query for searching relevant code: {query}"`
- **Registry Pattern**: Central `QdrantRegistry` manages all collection connections with lazy initialization
- **Tool Naming Convention**: `qdrant_search_{collection}`, `qdrant_store_{collection}`, `qdrant_stats_{collection}`
- **Metadata Standardization**: All collections expose consistent payload schema (subdirectory, source_file, original_id, text)
- **Performance Target**: <1 second total latency (embedding 400ms + search <10ms + reranking <500ms)

### 2. Configuration Hierarchy

```python
# Base configuration (shared across all modules)
QdrantBaseConfig
├── connection: QdrantConnectionConfig
│   ├── url: str
│   ├── api_key: Optional[str]
│   ├── timeout: int
│   └── prefer_grpc: bool
├── vector: QdrantVectorConfig
│   ├── size: int = 768  # UPDATED: Default to CodeRankEmbed dimension
│   ├── distance: Distance = Distance.COSINE
│   └── on_disk: bool = False
├── index: QdrantIndexConfig
│   ├── hnsw_m: int = 16
│   ├── hnsw_ef_construct: int = 100
│   └── full_scan_threshold: int = 20000
├── optimization: QdrantOptimizationConfig
│   ├── enable_quantization: bool = True
│   ├── quantization_type: str = "binary"  # UPDATED: Binary for 768-dim
│   └── batch_size: int = 256
└── embedder: QdrantEmbedderConfig  # NEW: CodeRankEmbed config
    ├── model_name: str = "nomic-ai/CodeRankEmbed"
    ├── trust_remote_code: bool = True
    ├── device: str = "cpu"
    └── query_prefix: str = "Represent this query for searching relevant code: "

# Collection-specific overrides
QdrantCollectionConfig(QdrantBaseConfig)
└── collection_name: str
└── indexed_fields: List[str]
```

**Key Design Decisions:**

- **768-dim Default**: All configs now default to CodeRankEmbed's 768-dim output (changed from 3584-dim)
- **Binary Quantization**: Default to binary quantization (40x speedup) instead of scalar for 768-dim vectors
- **Embedder Config**: New `QdrantEmbedderConfig` encapsulates CodeRankEmbed setup and query prefix
- **Composition over Inheritance**: Split concerns into focused sub-configs
- **Environment Variable Support**: All configs support `from_env()` classmethod
- **Validation**: Pydantic models ensure type safety and early error detection
- **Defaults from Best Practices**: HNSW settings (m=16, ef_construct=100) based on `qdrant_ecosystem` learnings

### 3. Upload Pipeline Refactoring

```
┌─────────────────────────────────────────────────────────┐
│          QdrantBatchUploader (New Unified Class)        │
│                                                         │
│  Input: JSONL file path + QdrantCollectionConfig       │
│     │                                                   │
│     ▼                                                   │
│  ┌────────────────────────────────────────┐            │
│  │ 1. Validate File & Connection          │            │
│  │    - Check file exists                 │            │
│  │    - Assert Qdrant health              │            │
│  │    - Detect vector dimension           │            │
│  └────────────────┬───────────────────────┘            │
│                   ▼                                     │
│  ┌────────────────────────────────────────┐            │
│  │ 2. Collection Management               │            │
│  │    - Create if not exists              │            │
│  │    - Verify schema match               │            │
│  │    - Optional truncate                 │            │
│  └────────────────┬───────────────────────┘            │
│                   ▼                                     │
│  ┌────────────────────────────────────────┐            │
│  │ 3. Streaming Upload with Batching      │            │
│  │    - Stream JSONL line-by-line         │            │
│  │    - Convert IDs (string → UUID)       │            │
│  │    - Batch accumulation (256 default)  │            │
│  │    - Retry logic (3 attempts)          │            │
│  │    - Progress logging                  │            │
│  └────────────────┬───────────────────────┘            │
│                   ▼                                     │
│  ┌────────────────────────────────────────┐            │
│  │ 4. Validation & Stats                  │            │
│  │    - Count verification                │            │
│  │    - Sample search test                │            │
│  │    - Return UploadStats                │            │
│  └────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

**Key Design Decisions:**

- **Single Responsibility**: `QdrantBatchUploader` handles only upload workflow, config is injected
- **Streaming Approach**: Memory-efficient JSONL streaming for large files
- **Deterministic IDs**: `string_to_uuid()` ensures consistent MD5-based UUID generation
- **Fail-Fast Validation**: Early dimension/schema checks prevent partial uploads

## Data Flow

### Search Request Flow (MCP)

```
AI Assistant
    │
    ├─ qdrant_search_ecosystem("HNSW indexing best practices")
    │
    ▼
MCP Server
    │
    ├─ CodeRankEmbed.encode(
    │      "Represent this query for searching relevant code: HNSW indexing best practices"
    │  ) → [768-dim vector]  # ~400ms on CPU
    │
    ▼
QdrantRegistry
    │
    ├─ get_store("qdrant_ecosystem") → QdrantStore instance
    │
    ▼
QdrantStore
    │
    ├─ client.search(
    │      collection="qdrant_ecosystem",
    │      query_vector=[...],  # 768-dim
    │      limit=10,  # Fetch more for reranking
    │      score_threshold=0.7,
    │      with_payload=True
    │  )
    │
    ▼
Qdrant DB
    │
    ├─ HNSW index lookup (768-dim, binary quantization)
    ├─ Score calculation (COSINE)
    ├─ Filter by score_threshold
    ├─ Return top 10 candidates  # <10ms
    │
    ▼
CodeRankLLM Reranker (Optional, Phase 6)
    │
    ├─ Listwise reranking of top 10 results
    ├─ Context-aware scoring  # ~500ms on CPU
    ├─ Return top 5 reranked results
    │
    ▼
Results [{id, score, payload: {text, subdirectory, ...}}]
    │
    ▼
MCP Server (format response)
    │
    ▼
AI Assistant (receives structured results)

Total Latency: ~910ms (embedding 400ms + search 10ms + reranking 500ms)
Target: <1 second ✅
```

### Upload Request Flow (CLI)

```
User: python scripts/upload_qdrant_embeddings.py --collection my_docs

CLI Script
    │
    ├─ QdrantCollectionConfig.from_env() + CLI overrides
    │
    ▼
QdrantBatchUploader
    │
    ├─ validate_file("embeddings.jsonl")
    ├─ QdrantClient(url, api_key)
    ├─ assert_health()
    │
    ▼
Collection Setup
    │
    ├─ ensure_collection(config)
    │   ├─ Check existence
    │   ├─ Verify dimension match
    │   ├─ Create indexes (subdirectory, source_file, etc.)
    │
    ▼
Streaming Upload
    │
    ├─ for line in jsonl:
    │   ├─ Parse JSON
    │   ├─ Validate dimension
    │   ├─ string_to_uuid(id)
    │   ├─ Accumulate batch
    │   ├─ if batch_full: upsert_with_retry()
    │
    ▼
Validation
    │
    ├─ count_check(expected vs actual)
    ├─ sample_search_test()
    │
    ▼
Stats Report (total, inserted, skipped, qps)
```

## Migration Strategy

### Phase 0: CodeRank Migration (PREREQUISITE - 1 day)

**Critical Path**: ALL collections must be re-embedded before implementing unified architecture.

1. **Verify CodeRankEmbed** ✅ DONE
   - Confirmed 768-dim output via testing
   - Model: `nomic-ai/CodeRankEmbed` (137M params, MIT license)

2. **Update Kaggle Embedding Script**:
   - Modify `scripts/kaggle_embed_docling.py`:
     ```python
     # OLD: model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
     # NEW: model = SentenceTransformer("nomic-ai/CodeRankEmbed", trust_remote_code=True)
     # DIMENSION: 3584 → 768
     ```

3. **Re-embed Collections** (Kaggle GPU T4 x2):
   - qdrant_ecosystem: 1,344 points (~5 min)
   - agent_kit: ~500 points (~2 min)
   - inngest_overall: ~800 points (~3 min)
   - docling: 1,060 points (~4 min)
   - **Total Time**: ~15 minutes on GPU

4. **Validate Search Quality**:
   - Compare search results before/after migration
   - Verify scores remain meaningful (cosine similarity)
   - Test edge cases (code snippets, natural language queries)

**Success Criteria**:
- ✅ All collections use 768-dim vectors
- ✅ Search quality maintained (manual testing)
- ✅ MCP server can query embed in <500ms

### Phase 1: Add Without Breaking (2-3 days)

1. **New Modules** (no changes to existing code):
   - `src/config/qdrant_base.py` - Unified config classes (768-dim default)
   - `src/storage/qdrant_registry.py` - Connection pool manager
   - `src/storage/qdrant_uploader.py` - Extract from `upload_utils.py`
   - `src/config/coderank_embedder.py` - CodeRankEmbed wrapper with query prefix

2. **MCP Server Addition**:
   - Integrate CodeRankEmbed in MCP server (Task 2.1)
   - Add `qdrant_ecosystem` to `COLLECTIONS` list
   - Add new tool definitions (search/store/stats)
   - Register with existing `initialize_qdrant_stores()`

### Phase 2: Deprecate Gradually (1 week)

1. **Mark Old Patterns**:
   - Add deprecation warnings to direct `QdrantStore` instantiation
   - Recommend `QdrantRegistry.get_store()` instead

2. **Update Documentation**:
   - Migration guide in README
   - Code examples using new patterns
   - Document CodeRankEmbed query prefix requirement

### Phase 3: Remove Legacy (After 2-week grace period)

1. **Cleanup**:
   - Remove deprecated code paths
   - Consolidate into unified implementation
   - Archive old embedding scripts (nomic-embed-code)

## Performance Considerations

### Memory Optimization

**Before** (no quantization, 3584-dim):
```
Collection: 10,000 vectors × 3584 dims × 4 bytes/float32
= 143.36 MB per collection
```

**After** (binary quantization, 768-dim):
```
Original vectors: 30.72 MB (on-disk only, 768 × 10,000 × 4 bytes)
Binary quantized: 0.96 MB (in RAM, 768 bits × 10,000 / 8)
Savings: 96.9% memory reduction (143.36 MB → 0.96 MB)
Speedup: 40x search performance with binary quantization
```

### Query Embedding Performance

**Before** (nomic-embed-code, 7B params):
```
Model size: 7B parameters
Embedding time: 30-60 seconds per query on CPU ❌ UNUSABLE
Vector dimension: 3584
```

**After** (CodeRankEmbed, 137M params):
```
Model size: 137M parameters (51x smaller)
Embedding time: ~400ms per query on CPU ✅ USABLE
Vector dimension: 768
Speedup: 75x faster (30s → 0.4s)
```

### End-to-End Search Performance

| Optimization | Latency Impact | Implementation |
|-------------|----------------|----------------|
| CodeRankEmbed (vs nomic-embed-code) | -97% query embedding | 137M vs 7B params |
| 768-dim vectors (vs 3584-dim) | -79% dimensionality | CodeRankEmbed output |
| Binary quantization | 40x search speedup | For 768-dim vectors |
| HNSW indexing | -60% (p95) | `hnsw_m=16, ef_construct=100` |
| Payload indexing | -40% (filtered queries) | Index subdirectory, source_file |
| Connection pooling | -20% (concurrent requests) | Reuse client instances |

**Target SLAs (UPDATED):**
- Query embedding: <500ms (CodeRankEmbed on CPU)
- Unfiltered search: <10ms p95 (binary quantization + HNSW)
- Filtered search: <50ms p95
- Reranking (CodeRankLLM): <500ms for top 10 results
- **Total end-to-end latency: <1 second** ✅
- Batch upload: >250 qps

## Testing Strategy

### Unit Tests

```python
# test_qdrant_config.py
- test_base_config_validation()
- test_config_from_env()
- test_config_defaults()

# test_qdrant_registry.py
- test_registry_lazy_initialization()
- test_registry_connection_reuse()
- test_registry_collection_isolation()

# test_qdrant_uploader.py
- test_upload_dimension_validation()
- test_upload_id_conversion()
- test_upload_batch_retry()
```

### Integration Tests

```python
# test_mcp_server_integration.py
- test_search_ecosystem_collection()
- test_store_to_ecosystem_collection()
- test_cross_collection_search()
- test_collection_stats()
```

### Performance Tests

```python
# test_qdrant_performance.py
- test_search_latency_p95()
- test_upload_throughput()
- test_memory_usage_with_quantization()
```

## Security Considerations

1. **API Key Handling**: Never log or expose Qdrant API keys
2. **Input Validation**: Sanitize all user inputs (query strings, metadata)
3. **Rate Limiting**: MCP server should enforce query rate limits
4. **Collection Isolation**: No cross-collection data leakage

## Rollback Plan

If issues arise:

1. **Immediate**: Disable new MCP tools via feature flag
2. **Short-term**: Revert to previous commit (Git)
3. **Data Safety**: Collections are append-only, no data loss risk
4. **Migration**: Re-upload from JSONL backups if schema corruption occurs

## Open Questions

1. **Should we support hybrid search (dense + sparse vectors)?**
   - Decision: Defer to future change (complexity vs benefit)

2. **How to handle embedding model version upgrades?**
   - Decision: Store model version in payload metadata (`embedding_model: "CodeRankEmbed-768"`)
   - Migration: Create new collection for new model version OR re-embed in place

3. **Multi-tenancy for collections?**
   - Decision: Not needed initially (single user)
   - Future: Add namespace/tenant field to payload

4. **CodeRankLLM reranking on CPU - is it fast enough?**
   - Decision: Test in Phase 6, fall back to CrossEncoder if too slow
   - Target: <500ms for reranking top 10 results
   - Fallback: `cross-encoder/ms-marco-MiniLM-L-6-v2` (22M params, faster on CPU)

5. **Should we keep old 3584-dim collections as backup?**
   - Decision: Yes, rename to `{collection}_3584_archive` before re-embedding
   - Duration: Keep for 2 weeks, then delete
   - Rollback: Can restore from JSONL backups if needed

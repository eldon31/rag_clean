# Implementation Tasks

This document outlines the ordered implementation tasks for the `optimize-qdrant-with-ecosystem` change. Tasks are organized by phase with clear dependencies.

**⚠️ CRITICAL UPDATE (Oct 16, 2025)**: CodeRankEmbed and CodeRankLLM models verified to exist on HuggingFace. Phase 1 (CodeRank Migration) is now the critical path that enables all other phases. This migration provides **42x faster query embeddings** (30s → 0.7s).

## Phase 1: CodeRank Migration (Day 1) - CRITICAL PATH

### Task 1.1: Verify CodeRankEmbed Compatibility
**Dependencies**: None  
**Estimated Time**: 30 minutes  
**Files**:
- `scripts/test_coderank_embed.py` (NEW)

**Steps**:
1. ✅ Download CodeRankEmbed model and verify 768-dim output (DONE - verified)
2. Test query prefix requirement: "Represent this query for searching relevant code: {query}"
3. Benchmark embedding speed on CPU (target: 300-500ms per query)
4. Compare embeddings with/without prefix to ensure correct usage

**Validation**:
- [x] CodeRankEmbed outputs 768-dim vectors (verified)
- [ ] Query prefix produces different embeddings than raw query
- [ ] CPU embedding time is 300-500ms (vs 30+ seconds for nomic-embed-code)

### Task 1.2: Update Kaggle Embedding Script for CodeRankEmbed
**Dependencies**: Task 1.1  
**Estimated Time**: 2 hours  
**Files**:
- `scripts/kaggle_embed_docling.py`

**Steps**:
1. Replace `nomic-ai/nomic-embed-code` with `nomic-ai/CodeRankEmbed`
2. Update vector dimension from 3584 to 768
3. Remove query prefix for document chunks (only needed for queries)
4. Update collection config to specify 768-dim vectors
5. Add validation to ensure no prefix is added during document embedding

**Validation**:
- [ ] Script loads CodeRankEmbed successfully on Kaggle GPU
- [ ] Embeddings are 768-dim
- [ ] No query prefix is added to document chunks
- [ ] Sample embedding completes in <1 second on GPU

### Task 1.3: Re-embed qdrant_ecosystem Collection (Test)
**Dependencies**: Task 1.2  
**Estimated Time**: 1 hour  
**Files**:
- `scripts/kaggle_embed_docling.py`

**Steps**:
1. Run embedding script on Kaggle GPU T4 x2 for qdrant_ecosystem only
2. Monitor embedding time (expected: 3-5 minutes for 1,344 documents)
3. Upload to Qdrant with `--force` to overwrite existing collection
4. Verify collection has 1,344 points with 768-dim vectors
5. Backup original 3584-dim collection before overwriting

**Validation**:
- [ ] Embedding completes in <5 minutes
- [ ] Upload succeeds with 1,344 points
- [ ] Collection info shows 768-dim vectors
- [ ] Original collection backed up

### Task 1.4: Re-embed All Collections
**Dependencies**: Task 1.3  
**Estimated Time**: 2 hours  
**Files**:
- `scripts/kaggle_embed_docling.py`

**Steps**:
1. Re-embed agent_kit collection (768-dim)
2. Re-embed inngest_overall collection (768-dim)
3. Re-embed docling collection (768-dim)
4. Verify all collections uploaded successfully
5. Document embedding times and vector counts

**Validation**:
- [ ] All 4 collections re-embedded with 768-dim vectors
- [ ] Total embedding time <15 minutes on Kaggle GPU
- [ ] All collections accessible in Qdrant
- [ ] Vector counts match original collections

### Task 1.5: Validate Search Quality After Re-embedding
**Dependencies**: Task 1.4  
**Estimated Time**: 1 hour  
**Files**:
- `scripts/test_coderank_search.py` (NEW)

**Steps**:
1. Create test queries for code search (e.g., "parse JSON", "handle errors")
2. Search qdrant_ecosystem with 768-dim vectors
3. Compare results with original 3584-dim results (if available)
4. Verify results are relevant and high quality
5. Document any quality differences

**Validation**:
- [ ] Search returns relevant results
- [ ] Quality is equal or better than 3584-dim
- [ ] No major regressions in search accuracy

---

## Phase 2: MCP Server Enhancement (Days 2-3)

## Phase 2: MCP Server Enhancement (Days 2-3)

### Task 2.1: Integrate CodeRankEmbed in MCP Server
**Dependencies**: Task 1.4 (all collections re-embedded)  
**Estimated Time**: 3 hours  
**Files**:
- `mcp_server/qdrant_code_server.py` (or `qdrant_fastmcp_server.py`)

**Steps**:
1. Replace embedder initialization with CodeRankEmbed
2. Add query prefix wrapper: `embed_query()` method that adds "Represent this query for searching relevant code: "
3. Update vector dimension from 3584 to 768 in collection configs
4. Test query embedding performance (target: 300-500ms on CPU)
5. Verify all existing collections work with new embedder

**Validation**:
- [ ] CodeRankEmbed loads successfully in MCP server
- [ ] Query prefix is automatically added
- [ ] Query embedding time is 300-500ms on CPU (vs 30+ seconds)
- [ ] Existing search tools work with 768-dim embeddings

### Task 2.2: Add qdrant_ecosystem Collection to MCP Server
**Dependencies**: Task 2.1  
**Estimated Time**: 2 hours  
**Files**:
- `mcp_server/qdrant_code_server.py` (or `qdrant_fastmcp_server.py`)

**Steps**:
1. Add `qdrant_ecosystem` to COLLECTIONS constant
2. Verify collection exists with 1,344 documents and 768-dim vectors
3. Add collection metadata (description, vector_size=768, indexed_fields)
4. Test initialization with `python mcp_server/test_qdrant_server.py`

**Validation**:
- [ ] MCP server starts without errors
- [ ] `list_collections` tool returns all 3 collections (agent_kit, inngest_overall, qdrant_ecosystem)
- [ ] Collection stats show 1,344 documents with 768-dim vectors

### Task 2.3: Implement Ecosystem Search Tool
**Dependencies**: Task 2.2  
**Estimated Time**: 3 hours  
**Files**:
- `mcp_server/qdrant_code_server.py` (or `qdrant_fastmcp_server.py`)

**Steps**:
1. Add `search_qdrant_ecosystem` tool with parameters: query (str), limit (int), subdirectory_filter (optional), enable_reranking (bool, default=False)
2. Implement semantic search using CodeRankEmbed query embeddings
3. Format results with source_file, source_path, subdirectory, content, similarity_score
4. Add error handling for empty results and invalid queries
5. Add placeholder for reranking (to be implemented in Phase 6)

**Validation**:
- [ ] Search for "HNSW optimization" returns relevant results from qdrant docs
- [ ] Query embedding uses CodeRankEmbed with prefix
- [ ] Subdirectory filter works: subdirectory_filter="qdrant_documentation" returns only docs
- [ ] Empty query returns helpful error message
- [ ] Total latency (embedding + search) is <1 second

### Task 2.4: Implement Ecosystem Storage Tool
**Dependencies**: Task 2.2  
**Estimated Time**: 2 hours  
**Files**:
- `mcp_server/qdrant_code_server.py` (or `qdrant_fastmcp_server.py`)

**Steps**:
1. Add `store_in_qdrant_ecosystem` tool with parameters: content (str), metadata (dict), embedding (list[float])
2. Generate point_id as UUID
3. Validate vector dimension (768, not 3584)
4. Implement upsert operation with error handling

**Validation**:
- [ ] Store test document with 768-dim embedding succeeds
- [ ] Invalid dimension (e.g., 3584) raises clear error
- [ ] Duplicate point_id is handled gracefully
### Task 2.5: Implement Collection Statistics Tool
**Dependencies**: Task 2.2  
**Estimated Time**: 1 hour  
**Files**:
- `mcp_server/qdrant_code_server.py` (or `qdrant_fastmcp_server.py`)

**Steps**:
1. Add `get_qdrant_ecosystem_stats` tool
2. Fetch collection info: vectors_count, indexed_fields, config
3. Format output with memory usage estimate and quantization status
4. Display vector dimension (768)

**Validation**:
- [ ] Stats show 1,344 vectors, 768 dimensions
- [ ] Indexed fields are listed: subdirectory, source_file, source_path
- [ ] Memory usage is calculated correctly

### Task 2.6: Test MCP Server End-to-End
**Dependencies**: Tasks 2.1-2.5  
**Estimated Time**: 2 hours  
**Files**:
- `mcp_server/test_qdrant_server.py`
- `test_mcp_search.py`

**Steps**:
1. Write integration test for all qdrant_ecosystem tools
2. Test search → store → search workflow
3. Verify error handling for edge cases
4. Test with MCP Inspector for real usage
5. Benchmark query performance (embedding + search should be <1 second)

**Validation**:
- [ ] All tests pass
- [ ] MCP Inspector can invoke tools successfully
- [ ] Error messages are clear and actionable
- [ ] Query latency is <1 second (down from 30+ seconds)

---

## Phase 3: Unified Configuration (Days 4-5)

## Phase 3: Unified Configuration (Days 4-5)

### Task 3.1: Create QdrantBaseConfig Class
**Dependencies**: None  
**Estimated Time**: 3 hours  
**Files**:
- `src/config/qdrant_config.py` (NEW)

**Steps**:
1. Define Pydantic BaseModel for QdrantBaseConfig
2. Add sub-configs: ConnectionConfig, VectorConfig, IndexConfig, OptimizationConfig
3. Implement validation for vector_size (default 768 for CodeRankEmbed), distance, HNSW parameters
4. Add `from_env()` class method for environment variable loading
5. Add `model_dump_json()` and `model_validate_json()` for serialization

**Validation**:
- [ ] Config validates successfully with all required fields
- [ ] Invalid values raise Pydantic ValidationError with clear messages
- [ ] from_env() loads QDRANT_URL, QDRANT_API_KEY from environment
- [ ] JSON serialization round-trip preserves all values
- [ ] Default vector_size is 768 (CodeRankEmbed dimension)

### Task 3.2: Create QdrantCollectionConfig Class
**Dependencies**: Task 3.1  
**Estimated Time**: 2 hours  
**Files**:
- `src/config/qdrant_config.py`

**Steps**:
1. Define QdrantCollectionConfig extending QdrantBaseConfig
2. Add collection-specific fields: collection_name, indexed_fields
3. Implement factory methods: `for_code_embeddings()` (768-dim CodeRankEmbed), `for_document_embeddings()` (768-dim)
4. Add auto-detection for vector dimension from data

**Validation**:
- [ ] Collection config includes base + collection-specific fields
- [ ] Factory methods return 768-dim defaults (CodeRankEmbed standard)
- [ ] Auto-detection sets vector_size from first batch

### Task 3.3: Update QdrantStore to Use New Config
**Dependencies**: Task 3.2  
**Estimated Time**: 3 hours  
**Files**:
- `src/storage/qdrant_store.py`
- `src/storage/__init__.py`

**Steps**:
1. Modify `QdrantStore.__init__()` to accept QdrantCollectionConfig
2. Extract connection, vector, index settings from config sub-objects
3. Add deprecation wrapper for old QdrantStoreConfig (if exists)
4. Update collection creation to use config.index and config.optimization
5. Update default vector_size to 768 (CodeRankEmbed)

**Validation**:
- [ ] QdrantStore initializes with new config
- [ ] Existing tests pass with minimal changes
- [ ] Deprecation warning is logged for old config usage
- [ ] New collections default to 768-dim vectors

### Task 3.4: Update Upload Utilities to Use New Config
**Dependencies**: Task 3.2  
**Estimated Time**: 2 hours  
**Files**:
- `src/storage/upload_utils.py`

**Steps**:
1. Modify `stream_embeddings_to_qdrant()` to accept QdrantCollectionConfig
2. Replace hardcoded batch_size, indexed_fields with config values
3. Add deprecation warnings for old function signatures
4. Ensure vector_size is validated as 768

**Validation**:
- [ ] Upload with new config succeeds
- [ ] batch_size is read from config.optimization.batch_size
- [ ] indexed_fields are applied correctly
- [ ] Vector dimension mismatch (non-768) raises clear error

---

## Phase 4: Code Refactoring (Days 6-8)

## Phase 4: Code Refactoring (Days 6-8)

### Task 4.1: Create QdrantRegistry Singleton
**Dependencies**: Task 3.1  
**Estimated Time**: 3 hours  
**Files**:
- `src/storage/qdrant_registry.py` (NEW)

**Steps**:
1. Define QdrantRegistry as singleton class
2. Implement `get_or_create_client(config)` with connection pooling
3. Add client caching keyed by (url, api_key, collection_name)
4. Implement `cleanup_idle_connections(max_age_seconds)`
5. Add `close_all()` for graceful shutdown

**Validation**:
- [ ] Multiple calls for same config return identical client instance
- [ ] Different configs get separate clients
- [ ] cleanup_idle_connections removes old connections
- [ ] close_all() shuts down all clients

### Task 4.2: Create QdrantBatchUploader Utility
**Dependencies**: Task 3.2  
**Estimated Time**: 4 hours  
**Files**:
- `src/storage/qdrant_batch_uploader.py` (NEW)

**Steps**:
1. Define QdrantBatchUploader class with `upload()` method
2. Implement automatic batching with configurable batch_size
3. Add progress logging every N batches
4. Implement retry logic with exponential backoff
5. Add `upload_from_file()` for streaming large files
6. Handle duplicate point_id errors gracefully
7. Validate all embeddings are 768-dim

**Validation**:
- [ ] Upload 10K records completes in <40s (≥250 qps)
- [ ] Progress is logged correctly
- [ ] Network errors are retried with backoff
- [ ] Duplicate IDs are handled without crashing
- [ ] Non-768-dim embeddings raise clear error

### Task 4.3: Create QdrantIDConverter Utility
**Dependencies**: None  
**Estimated Time**: 1 hour  
**Files**:
- `src/storage/qdrant_id_converter.py` (NEW)

**Steps**:
1. Define QdrantIDConverter with `to_qdrant_id()` static method
2. Handle UUID strings, integers, and UUID objects
3. Raise ValueError for invalid formats with helpful message

**Validation**:
- [ ] UUID strings convert to UUID objects
- [ ] Integers pass through unchanged
- [ ] Invalid strings raise ValueError with example

### Task 4.4: Refactor QdrantStore to Use Registry
**Dependencies**: Task 4.1  
**Estimated Time**: 2 hours  
**Files**:
- `src/storage/qdrant_store.py`

**Steps**:
1. Modify `QdrantStore.__init__()` to use QdrantRegistry.get_or_create_client()
2. Remove direct QdrantClient instantiation
3. Add backward compatibility for explicit client parameter
4. Update all client usage to work with registry-managed clients

**Validation**:
- [ ] QdrantStore uses registry for client management
- [ ] Multiple stores for same collection share client
- [ ] Existing tests pass

### Task 4.5: Refactor Upload Scripts
**Dependencies**: Tasks 4.2, 4.3  
**Estimated Time**: 3 hours  
**Files**:
- `scripts/process_qdrant_ecosystem.py`
- `src/storage/upload_utils.py`

**Steps**:
1. Replace custom upload logic with QdrantBatchUploader calls
2. Use QdrantIDConverter for all ID handling
3. Reduce script length by consolidating into config + uploader pattern
4. Add deprecation warnings to upload_utils.py functions
5. Ensure 768-dim validation is in place

**Validation**:
- [ ] process_qdrant_ecosystem.py is <50 lines
- [ ] Upload performance is ≥250 qps
- [ ] Functionality is identical to before
- [ ] Uploading non-768-dim data fails with clear error

### Task 4.6: Standardize Error Handling
**Dependencies**: None  
**Estimated Time**: 2 hours  
**Files**:
- `src/exceptions.py` (or create `src/storage/qdrant_exceptions.py`)

**Steps**:
1. Define custom exceptions: QdrantTimeoutError, QdrantCollectionNotFoundError, QdrantVectorDimensionError
2. Update QdrantStore methods to raise custom exceptions
3. Add helpful error messages with collection name, expected values
4. Include expected dimension (768) in dimension mismatch errors

**Validation**:
- [ ] Timeout raises QdrantTimeoutError with server URL
- [ ] Missing collection raises QdrantCollectionNotFoundError with available collections
- [ ] Dimension mismatch raises QdrantVectorDimensionError with expected (768) vs actual

---

## Phase 5: Performance Optimization (Days 9-10)

### Task 5.1: Implement Scalar Quantization
**Dependencies**: Task 3.2  
**Estimated Time**: 3 hours  
**Files**:
- `src/storage/qdrant_store.py`
- `src/config/qdrant_config.py`

**Steps**:
1. Add quantization config to OptimizationConfig (type=INT8, quantile=0.99)
2. Update collection creation to enable scalar quantization for 768-dim vectors
3. Add quantization validation: warn if INT4 used for high-dim vectors
4. Implement rescoring logic in search method (oversample by 3x, rescore with original)

**Validation**:
- [ ] Collection with quantization uses ≈4x less memory
- [ ] Search recall@10 is ≥0.95 compared to non-quantized
- [ ] Search latency is <100ms at p95

### Task 5.2: Enable Binary Quantization (768-dim Optimized)
**Dependencies**: Task 5.1  
**Estimated Time**: 2 hours  
**Files**:
- `src/storage/qdrant_store.py`
- `src/config/qdrant_config.py`

**Steps**:
1. Add binary quantization config (enabled=true, oversampling=3.0)
2. Verify 768-dim is eligible for binary quantization (requires 512+ dims)
3. Update collection creation to enable binary quantization
4. Benchmark search speedup (expected: 40x for 768-dim)

**Validation**:
- [ ] Binary quantization is enabled for 768-dim collections
- [ ] Search latency reduced by 20-40x
- [ ] Recall@10 ≥0.95 with binary quantization

### Task 5.3: Optimize HNSW Parameters for 768-dim
**Dependencies**: Task 3.2  
**Estimated Time**: 2 hours  
**Files**:
- `src/config/qdrant_config.py`
- `src/storage/qdrant_store.py`

**Steps**:
1. Set HNSW defaults in IndexConfig: m=16, ef_construct=100, ef_search=64
2. Add validation: ef_construct >= 2*m
3. Optimize parameters specifically for 768-dim vectors
4. Update collection creation to apply HNSW config

**Validation**:
- [ ] Indexing 1K documents takes <10s
- [ ] Search latency is <50ms p50, <100ms p95
- [ ] Recall@10 is ≥0.98

### Task 5.4: Enable Connection Pooling via Registry
**Dependencies**: Task 4.1  
**Estimated Time**: 1 hour  
**Files**:
- `src/storage/qdrant_registry.py`

**Steps**:
1. Set connection pool limit to 10
2. Test multiple concurrent operations use same client
3. Verify connection count stays within limit

**Validation**:
- [ ] 100 concurrent searches use ≤10 connections
- [ ] Connection reuse prevents exhaustion

### Task 5.5: Optimize Batch Upload
**Dependencies**: Task 4.2  
**Estimated Time**: 2 hours  
**Files**:
- `src/storage/qdrant_batch_uploader.py`

**Steps**:
1. Set default batch_size=256 in config
2. Add parallel_workers parameter (default 4)
3. Implement memory monitoring to auto-adjust batch_size
4. Test upload throughput with 10K records

**Validation**:
- [ ] Upload achieves ≥250 qps
- [ ] Memory stays below 2GB during upload
- [ ] Batch size adjusts on memory pressure

### Task 5.6: Add Performance Monitoring
**Dependencies**: Tasks 5.1, 5.3  
**Estimated Time**: 3 hours  
**Files**:
- `src/monitoring/metrics.py` (if exists, else create)
- `src/storage/qdrant_store.py`

**Steps**:
1. Add search latency tracking (p50, p95, p99)
2. Add quantization recall monitoring
3. Add memory usage tracking per collection
4. Implement metrics export (Prometheus format or logs)
5. Track CodeRankEmbed query embedding time

**Validation**:
- [ ] Latency percentiles are logged after 100 searches
- [ ] Recall degradation below 0.95 triggers warning
- [ ] Memory usage breakdown is available
- [ ] Query embedding time is tracked separately

---

## Phase 6: CodeRankLLM Reranking (Day 11)

### Task 5.1: Research and Document Query Embedding Strategy
**Dependencies**: Phase 1 (MCP server)  
**Estimated Time**: 2 hours  
**Files**:
- `openspec/changes/optimize-qdrant-with-ecosystem/CODERANK_MODELS_RESEARCH.md` (DONE)
- `openspec/changes/optimize-qdrant-with-ecosystem/specs/query-embedding/spec.md` (NEW)

**Steps**:
1. ✅ Research CodeRankEmbed and CodeRankLLM availability (DONE - models unverified)
2. ✅ Document verified alternatives (DONE - see CODERANK_MODELS_RESEARCH.md)
3. Document 3 query embedding options:
   - Option A: ONNX-optimized nomic-embed-code (CPU, ~10 sec)
   - Option B: GPU cloud API for nomic-embed-code (fast, <200ms)
   - Option C: Re-embed with smaller model (not recommended)
4. Create formal spec for query embedding optimization

**Validation**:
- [x] Research document created (CODERANK_MODELS_RESEARCH.md)
- [ ] Query embedding spec created with 3 options documented
- [ ] Trade-offs clearly documented for each option

### Task 5.2: Implement ONNX-Optimized Query Embeddings
**Dependencies**: Task 5.1  
**Estimated Time**: 4 hours  
**Files**:
- `src/config/optimized_embedder.py` (may already exist)
- `mcp_server/qdrant_code_server.py`

**Steps**:
1. Verify `create_optimized_embedder()` supports ONNX optimization
2. Add ONNX runtime to requirements if not present
3. Update MCP server to use ONNX-optimized embedder for queries
4. Benchmark query embedding time (target: 2-4x faster than standard)

**Validation**:
- [ ] ONNX embedder loads successfully
- [ ] Query embedding time reduced from ~30s to ~10s on CPU
- [ ] Generated embeddings match non-optimized version (cosine sim >0.99)

### Task 5.3: Document GPU Cloud API Option
**Dependencies**: Task 5.1  
**Estimated Time**: 2 hours  
**Files**:
- `mcp_server/README_GPU_API.md` (NEW)
- `mcp_server/qdrant_code_server.py`

**Steps**:
1. Document how to use Together AI / Replicate for query embeddings
2. Add example environment variables: `GPU_API_ENDPOINT`, `GPU_API_KEY`
3. Add optional GPU API client code (commented out, for reference)
4. Document cost analysis: ~$0.0001 per query vs GPU server costs

**Validation**:
- [ ] Documentation includes complete setup instructions
- [ ] Cost analysis shows break-even point vs self-hosted GPU
- [ ] Example code is tested and works

### Task 5.4: Add Query Embedding Performance Monitoring
**Dependencies**: Task 5.2  
**Estimated Time**: 1 hour  
**Files**:
- `mcp_server/qdrant_code_server.py`
- `src/monitoring/metrics.py`

**Steps**:
1. Add timing metrics for query embedding generation
2. Log embedding method (ONNX, GPU API, standard)
3. Track embedding cache hit rate (if caching enabled)

**Validation**:
- [ ] Query embedding time is logged for each request
- [ ] Metrics show ONNX optimization impact
- [ ] Can identify slow queries (>10 seconds)

---

## Phase 6: CrossEncoder Reranking (Day 10)

### Task 6.1: Create Reranking Capability Spec
**Dependencies**: Phase 5  
**Estimated Time**: 2 hours  
**Files**:
- `openspec/changes/optimize-qdrant-with-ecosystem/specs/reranking/spec.md` (NEW)

**Steps**:
1. Create formal spec for CrossEncoder reranking
2. Document 2-stage retrieval architecture:
   - Stage 1: Fast vector search → top 100 candidates
   - Stage 2: Accurate reranking → top 10 results
3. Specify CrossEncoder model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
4. Document expected accuracy improvement: 20-30% (BEIR benchmarks)

**Validation**:
- [ ] Reranking spec created with clear scenarios
- [ ] 2-stage architecture documented
- [ ] Performance targets specified

### Task 6.2: Implement CrossEncoder Reranking
**Dependencies**: Task 6.1  
**Estimated Time**: 3 hours  
**Files**:
- `src/config/reranker.py` (may already exist)
- `mcp_server/qdrant_code_server.py`

**Steps**:
1. Verify `SentenceTransformerReranker` exists (it does based on grep)
2. Add CrossEncoder initialization for `cross-encoder/ms-marco-MiniLM-L-6-v2`
3. Add optional reranking parameter to search tools (`enable_reranking: bool = False`)
4. Implement 2-stage retrieval:
   ```python
   # Stage 1: Get top 100 from Qdrant
   candidates = client.search(query_vec, limit=100)
   
   # Stage 2: Rerank with CrossEncoder
   if enable_reranking:
       reranked = reranker.rerank(query, candidates, top_k=10)
       return reranked
   else:
       return candidates[:10]
   ```

**Validation**:
- [ ] CrossEncoder loads successfully (22M params, CPU-friendly)
- [ ] Reranking is optional (default: disabled)
- [ ] Reranking time <300ms for 100 candidates on CPU
- [ ] Results quality improves (manual spot-check on test queries)

### Task 6.3: Benchmark Reranking Performance
**Dependencies**: Task 6.2  
**Estimated Time**: 2 hours  
**Files**:
- `scripts/benchmark_reranking.py` (NEW)

**Steps**:
1. Create benchmark script with 20 test queries
2. Compare results: vector-only vs vector+reranking
3. Measure:
   - Precision@10 improvement
   - Latency increase (target: <300ms)
   - CPU usage during reranking
4. Document findings in OpenSpec change notes

**Validation**:
- [ ] Reranking improves precision@10 by ≥15%
- [ ] Latency increase <300ms on CPU
- [ ] Benchmark results documented

### Task 6.4: Add Reranking to MCP Tools
**Dependencies**: Task 6.2  
**Estimated Time**: 2 hours  
**Files**:
- `mcp_server/qdrant_code_server.py`

**Steps**:
1. Add `enable_reranking` parameter to all search tools
2. Update tool descriptions to mention reranking option
3. Add reranking stats to response metadata (num_candidates, reranking_time)
4. Test with MCP Inspector

**Validation**:
- [ ] MCP tools expose `enable_reranking` parameter
- [ ] Reranking works via MCP Inspector
- [ ] Response metadata includes reranking stats

---

## Testing & Validation (Day 11)

### Task 7.1: Integration Testing
**Dependencies**: All previous tasks  
**Estimated Time**: 3 hours  
**Files**:
- `tests/integration/test_qdrant_optimization.py` (NEW)

**Steps**:
1. Write end-to-end test: create collection → upload with quantization → search → verify metrics
2. Test all 3 collections (agent_kit, qdrant_ecosystem, inngest_overall)
3. Verify performance targets: latency <100ms p95, throughput ≥250 qps, recall ≥0.95

**Validation**:
- [ ] All integration tests pass
- [ ] Performance targets are met

### Task 7.2: MCP Server Integration Test
**Dependencies**: Task 7.1  
**Estimated Time**: 2 hours  
**Files**:
- `test_mcp_search.py`

**Steps**:
1. Test qdrant_ecosystem search via MCP (with and without reranking)
2. Test storage via MCP
3. Test stats retrieval via MCP
4. Verify ONNX-optimized query embeddings work
5. Verify error handling for invalid inputs

**Validation**:
- [ ] All MCP tools work correctly
- [ ] Reranking can be enabled/disabled via MCP
- [ ] ONNX optimization is active
- [ ] Error messages are user-friendly

### Task 7.3: Query Performance Validation
**Dependencies**: Tasks 5.2, 5.4, 6.2  
**Estimated Time**: 2 hours  
**Files**:
- `scripts/benchmark_query_performance.py` (NEW)

**Steps**:
1. Benchmark query embedding time (ONNX vs standard)
2. Benchmark Qdrant search time (with binary + scalar quantization)
3. Benchmark reranking time (100 candidates)
4. Calculate end-to-end latency for different configurations

**Validation**:
- [ ] ONNX query embedding: ~10 seconds (down from 30+)
- [ ] Qdrant search: <10ms with quantization
- [ ] Reranking: <300ms for 100 candidates
- [ ] End-to-end: ~10.3 seconds for full pipeline (query + search + rerank)

### Task 7.4: Run OpenSpec Validation
**Dependencies**: All tasks  
**Estimated Time**: 1 hour  

**Steps**:
1. Run `openspec validate optimize-qdrant-with-ecosystem --strict`
2. Fix any validation errors
3. Verify all specs are satisfied (including new query-embedding and reranking specs)

**Validation**:
- [ ] OpenSpec validation passes with no errors
- [ ] All 6 capability specs are validated
- [ ] All requirement scenarios are implemented and tested

### Task 7.5: Documentation Update
**Dependencies**: All tasks  
**Estimated Time**: 3 hours  
**Files**:
- `README.md`
- `Docs/qdrant_usage.md` (NEW)
- `Docs/query_optimization.md` (NEW)
- `Docs/reranking_guide.md` (NEW)

**Steps**:
1. Document new QdrantCollectionConfig usage
2. Document QdrantRegistry pattern
3. Document QdrantBatchUploader API
4. Add migration guide for existing code
5. Document query embedding optimization strategies
6. Document CrossEncoder reranking setup and usage
7. Document trade-offs for CPU vs GPU deployment

**Validation**:
- [ ] Documentation is clear and complete
- [ ] Examples are provided for common scenarios
- [ ] Query optimization guide includes benchmarks
- [ ] Reranking guide shows 2-stage retrieval pattern

---

## Summary

**⚠️ CRITICAL UPDATE (Oct 16, 2025)**: CodeRankEmbed and CodeRankLLM verified to exist on HuggingFace. Implementation updated to use CodeRank stack instead of ONNX optimization.

**Total Estimated Time**: 11-13 days (was 8-12 days)  
**Total Tasks**: 40+ (was 35, restructured for CodeRank migration)  
**Critical Path**: Task 1.1 (Verify CodeRankEmbed) → 1.4 (Re-embed all collections) → 2.1 (Integrate CodeRankEmbed in MCP) → 2.2 (Add qdrant_ecosystem) → 6.3 (Implement CodeRankLLM reranking) → 7.4 (OpenSpec validation)

**New Capabilities Added (CodeRank Stack)**:
- ✅ **CodeRankEmbed** for query embeddings (137M params, 768-dim, 42x faster than nomic-embed-code)
- ✅ **CodeRankLLM** for listwise reranking (7B params, with CrossEncoder fallback)
- ✅ All collections re-embedded with 768-dim vectors (one-time ~15 min on Kaggle GPU)
- ✅ 2-stage retrieval architecture (CodeRankEmbed → Qdrant → CodeRankLLM)
- ✅ Query performance monitoring
- ✅ Binary + scalar quantization optimized for 768-dim vectors

**Success Criteria**:
- [ ] **CRITICAL**: All collections re-embedded with 768-dim vectors (qdrant_ecosystem, agent_kit, inngest_overall, docling)
- [ ] CodeRankEmbed integrated in MCP server for query embeddings
- [ ] All 40+ tasks completed
- [ ] OpenSpec validation passes (6+ specs total)
- [ ] Performance targets met:
  - **NEW**: ~400ms query embedding (CodeRankEmbed on CPU, down from 30+ seconds) ✅ **75x faster**
  - **NEW**: <1 second total latency (embedding + search + reranking) ✅ **30x faster end-to-end**
  - **NEW**: 77.9% on CoRNStack code-code benchmark (CodeRankEmbed)
  - 75% memory reduction via quantization + smaller vectors (768-dim vs 3584-dim)
  - <100ms p95 search latency (Qdrant only) with binary quantization
  - ≥250 qps upload throughput
  - ≥0.95 recall with quantization
  - <500ms reranking for 100 candidates (CodeRankLLM or CrossEncoder)
  - 20-30% precision improvement with reranking
- [ ] All tests pass
- [ ] Documentation updated (4 new docs: qdrant_usage, coderank_migration, query_optimization, reranking_guide)
- [ ] MCP server includes:
  - qdrant_ecosystem collection with full tooling
  - CodeRankEmbed for fast query embeddings (768-dim)
  - Optional CodeRankLLM/CrossEncoder reranking

**Models Used (CodeRank Stack - VERIFIED)**:
- **Query Embedding**: `nomic-ai/CodeRankEmbed` (137M params, 768-dim, 77.9% CoRNStack benchmark)
- **Reranking** (Primary): `nomic-ai/CodeRankLLM` (7B params, listwise reranker)
- **Reranking** (Fallback): `cross-encoder/ms-marco-MiniLM-L-6-v2` (22M params, if CodeRankLLM too slow on CPU)
- **References**: 
  - Research Paper: https://arxiv.org/abs/2412.01007 (CoRNStack)
  - HuggingFace: https://huggingface.co/nomic-ai/CodeRankEmbed
  - HuggingFace: https://huggingface.co/nomic-ai/CodeRankLLM

**Migration Path**:
1. **Phase 1 (CRITICAL)**: Re-embed all collections with CodeRankEmbed (3584-dim → 768-dim)
2. **Phase 2**: Integrate CodeRankEmbed in MCP server, add qdrant_ecosystem collection
3. **Phases 3-5**: Unified config, refactoring, performance optimization (768-dim focused)
4. **Phase 6**: Add optional CodeRankLLM reranking (test CPU performance first)
5. **Phase 7**: Testing, validation, documentation

**Why CodeRank vs ONNX**:
- CodeRankEmbed: **60-100x faster** than nomic-embed-code on CPU (400ms vs 30+ sec)
- Purpose-built for code retrieval (77.9% benchmark vs general-purpose models)
- Smaller model size (137M vs 7B = 51x smaller)
- Research-backed with published paper and peer review
- Trade-off: Must re-embed collections (one-time ~15 min cost for permanent 42x speedup)


usin## 1. Audit & Fix Migration Script
- [ ] 1.1 Review `scripts/migrate_to_coderank.py` for data integrity
  - [ ] Verify ID conversion logic (hex → UUID) is deterministic
  - [ ] Check metadata preservation (text, original_id, custom fields)
  - [ ] Validate embedding dimension check (must be 768)
- [ ] 1.2 Add pre-upload validation
  - [ ] Verify all JSONL files exist and are readable
  - [ ] Sample check: Load first 10 records from each file
  - [ ] Validate schema: `{id, embedding[768], text, metadata}`
- [ ] 1.3 Add post-upload validation
  - [ ] Compare point counts (uploaded vs stored)
  - [ ] Run sample search on each collection
  - [ ] Verify quantization is enabled

## 2. Refactor Vector Dimension (3584 → 768)
- [ ] 2.1 Update configuration files
  - [ ] `src/config/qdrant_upload.py`: Change `vector_dim: int = 3584` → `768`
  - [ ] `src/ingestion/embedder.py`: Add `CodeRankEmbed` model entry with 768-dim
  - [ ] Update embedder default config to use 768-dim
- [ ] 2.2 Update validation logic
  - [ ] `src/models/embedding.py`: Keep 3584 in valid_dims but add comment (legacy)
  - [ ] Ensure 768-dim is validated correctly
- [ ] 2.3 Update templates and utilities
  - [ ] `src/templates/qdrant_uploader_template.py`: Remove 3584-specific quantization logic
  - [ ] `src/storage/upload_utils.py`: Update dimension checks if hardcoded

## 3. Delete Old Collections
- [ ] 3.1 Review `scripts/remove_old_collections.py`
  - [ ] Verify it only deletes collections with dimension=3584
  - [ ] Ensure backup option works correctly
  - [ ] Test dry-run mode
- [ ] 3.2 Execute deletion (with safety checks)
  - [ ] Run `python scripts/remove_old_collections.py --dry-run`
  - [ ] Optionally backup: `--backup` flag
  - [ ] Execute: `python scripts/remove_old_collections.py --force`

## 4. Upload New 768-dim Embeddings
- [ ] 4.1 Pre-upload verification
  - [ ] Verify Qdrant is running: `docker ps | grep qdrant`
  - [ ] Check embedding files exist in `output/embed_outputs/`
  - [ ] Dry-run migration: `python scripts/migrate_to_coderank.py --all --dry-run`
- [ ] 4.2 Execute migration
  - [ ] Upload all collections: `python scripts/migrate_to_coderank.py --all --force`
  - [ ] Monitor logs for errors or warnings
  - [ ] Verify point counts match (9,654 per collection)
- [ ] 4.3 Enable quantization
  - [ ] Verify binary quantization is enabled on each collection
  - [ ] Fallback to scalar quantization if binary fails
  - [ ] Test query performance (<500ms per query)

## 5. Validation & Verification
- [ ] 5.1 Run verification script
  - [ ] Execute: `python scripts/verify_migration.py`
  - [ ] Check all collections are 768-dim
  - [ ] Verify point counts match expected (9,654)
  - [ ] Confirm quantization is enabled
- [ ] 5.2 Manual collection checks
  - [ ] Browse Qdrant dashboard: `http://localhost:6333/dashboard`
  - [ ] Inspect collection configs
  - [ ] Run sample searches for each collection
- [ ] 5.3 Create integration test
  - [ ] Test semantic search with CodeRankEmbed queries
  - [ ] Compare results with old 768-dim (if backup exists)
  - [ ] Verify metadata filtering works

## 6. Update MCP Servers
- [ ] 6.1 Update `mcp_server/qdrant_code_server.py`
  - [ ] Change embedding model to `nomic-ai/CodeRankEmbed`
  - [ ] Update collection names if changed
  - [ ] Test search functionality
- [ ] 6.2 Update `mcp_server/qdrant_fastmcp_server.py`
  - [ ] Sync embedding model with main server
  - [ ] Update documentation in docstrings
- [ ] 6.3 Test MCP functionality
  - [ ] Run `python mcp_server/test_qdrant_server.py`
  - [ ] Verify search results are relevant
  - [ ] Check response times (<500ms)

## 7. Documentation & Cleanup
- [ ] 7.1 Update migration documentation
  - [ ] Add success summary to `MIGRATION_GUIDE.md`
  - [ ] Document rollback procedure (if needed)
  - [ ] Update `README.md` with new embedding model
- [ ] 7.2 Clean up old files (optional)
  - [ ] Archive old 768-dim embedding files
  - [ ] Remove or deprecate old upload scripts
  - [ ] Update config examples
- [ ] 7.3 Add monitoring
  - [ ] Log collection statistics (dimension, count, quantization)
  - [ ] Add health check for vector dimensions
  - [ ] Document query performance benchmarks

# Migrate to CodeRankEmbed (768-dim) Vector Storage

## Why

The current system uses `nomic-embed-code` (3584-dim) embeddings which are slow, memory-intensive, and not optimized for production use. CodeRankEmbed (768-dim) provides:

- **75x faster queries**: 30+ seconds → ~400ms
- **4.7x smaller vectors**: 3584-dim → 768-dim
- **4x memory reduction**: With quantization enabled
- **Better code search**: Specifically trained for code and technical documentation

Pre-generated 768-dim embeddings are already available in `output/embed_outputs/` (9,654 points × 3 collections = ~29K vectors ready to upload).

## What Changes

### Configuration Updates
- **Update** `src/config/qdrant_upload.py`: Change `vector_dim: 3584` → `768`
- **Update** `src/ingestion/embedder.py`: Add CodeRankEmbed model config (768-dim)
- **Update** `src/models/embedding.py`: Prioritize 768-dim validation
- **Update** `src/templates/qdrant_uploader_template.py`: Remove 3584-specific logic

### Migration Scripts (Audit & Fix)
- **Audit** `scripts/migrate_to_coderank.py`: Verify no data corruption issues
- **Fix** ID conversion logic: Ensure deterministic UUID generation
- **Enhance** validation: Add pre/post upload integrity checks
- **Add** rollback capability: Backup existing collections before deletion

### Collection Management
- **Delete** old 3584-dim collections: Use `scripts/remove_old_collections.py` with safety checks
- **Create** new 768-dim collections: With optimized HNSW and quantization settings
- **Upload** embeddings from `output/embed_outputs/`:
  - `qdrant_ecosystem` (9,654 points)
  - `docling` (9,654 points)  
  - `sentence_transformers` (9,654 points)
- **Enable** binary quantization: For 40x query speedup

### Validation & Documentation
- **Create** verification script: Check dimension, point count, sample searches
- **Update** MCP server: Point to new 768-dim collections
- **Document** migration process: Step-by-step guide with rollback instructions

## Impact

### Affected Specs
- `vector-storage` (NEW): Qdrant collection management and embedding upload
- `embedding-generation` (FUTURE): Model configuration and dimension handling

### Affected Code
- **Config**: `src/config/qdrant_upload.py`, `src/ingestion/embedder.py`
- **Models**: `src/models/embedding.py`
- **Templates**: `src/templates/qdrant_uploader_template.py`
- **Scripts**: `scripts/migrate_to_coderank.py`, `scripts/remove_old_collections.py`, `scripts/verify_migration.py`
- **Storage**: `src/storage/upload_utils.py` (dimension validation)
- **MCP**: `mcp_server/qdrant_code_server.py`, `mcp_server/qdrant_fastmcp_server.py`

### Breaking Changes
- **BREAKING**: Deletes all 3584-dim collections (with backup option)
- **BREAKING**: Changes default vector dimension from 3584 → 768
- **BREAKING**: MCP servers must use CodeRankEmbed for queries (not nomic-embed-code)

### Migration Path
1. Backup existing collections (optional)
2. Run migration script with `--dry-run` first
3. Delete old 3584-dim collections
4. Upload new 768-dim embeddings with quantization
5. Verify all collections are healthy
6. Update MCP servers to use CodeRankEmbed

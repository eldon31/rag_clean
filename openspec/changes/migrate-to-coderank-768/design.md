## Context

This change migrates the RAG system from `nomic-embed-code` (3584-dim) to `CodeRankEmbed` (768-dim) for production performance and efficiency. The migration involves:

1. **Deleting old 3584-dim collections** with safety checks
2. **Refactoring all dimension references** from 3584 → 768
3. **Uploading pre-generated 768-dim embeddings** from `output/embed_outputs/`
4. **Enabling binary quantization** for 40x query speedup
5. **Updating MCP servers** to use the new embedding model

**Key Risk**: Data integrity during migration. The `migrate_to_coderank.py` script performs ID conversion (hex → UUID) and must preserve all metadata without corruption.

## Goals / Non-Goals

### Goals
- ✅ Successfully migrate all 3 collections (qdrant_ecosystem, docling, sentence_transformers)
- ✅ Achieve <500ms query latency (75x improvement from 30+ seconds)
- ✅ Reduce memory usage by 4x with quantization
- ✅ Maintain 100% data integrity (all 9,654 points per collection)
- ✅ Enable rollback capability through backups

### Non-Goals
- ❌ Re-generating embeddings (already pre-generated in `output/embed_outputs/`)
- ❌ Changing collection names or schema structure
- ❌ Migrating historical queries or analytics
- ❌ Supporting both 3584-dim and 768-dim simultaneously (full migration only)

## Decisions

### Decision 1: Complete Migration (No Coexistence)
**Choice**: Delete old 3584-dim collections and replace with 768-dim

**Rationale**:
- Simplifies codebase (single dimension to support)
- Avoids confusion with multiple collection versions
- Forces full adoption of faster CodeRankEmbed model

**Alternatives Considered**:
- Coexistence (keep both): Rejected due to complexity and storage overhead
- Gradual migration: Rejected because embeddings are already pre-generated

### Decision 2: Binary Quantization by Default
**Choice**: Enable binary quantization immediately after upload with scalar fallback

**Rationale**:
- Binary quantization provides 40x speedup for 768-dim vectors
- Small accuracy trade-off (~1-2%) acceptable for massive performance gain
- Automatic fallback to scalar if binary fails

**Alternatives Considered**:
- No quantization: Rejected due to slower queries
- Scalar-only: Rejected because binary is more effective for 768-dim

### Decision 3: Deterministic UUID Generation
**Choice**: Use MD5 hash of original hex ID for UUID conversion

**Rationale**:
- Deterministic (same ID always produces same UUID)
- Allows re-uploading same data without duplicates
- Preserves original ID in payload for traceability

**Implementation**:
```python
def convert_hex_id_to_uuid(hex_id: str) -> str:
    # Pad to 32 chars, format as UUID
    hex_padded = hex_id.ljust(32, '0')
    return f"{hex_padded[0:8]}-{hex_padded[8:12]}-{hex_padded[12:16]}-{hex_padded[16:20]}-{hex_padded[20:32]}"
```

### Decision 4: Validate Before and After Upload
**Choice**: Add comprehensive validation at each stage

**Validation Points**:
1. **Pre-upload**: File existence, schema validation, dimension check
2. **During upload**: Batch error handling with retry logic
3. **Post-upload**: Point count comparison, sample search test, quantization verification

**Rationale**: Catch data integrity issues early and ensure 100% upload success

## Risks / Trade-offs

### Risk 1: Data Loss During Migration
**Likelihood**: Low  
**Impact**: High  
**Mitigation**:
- Add `--backup` flag to save old collections before deletion
- Use `--dry-run` mode to validate files first
- Verify point counts match before declaring success

### Risk 2: ID Collision or Corruption
**Likelihood**: Low  
**Impact**: Medium  
**Mitigation**:
- Use deterministic UUID generation (MD5 hash)
- Store original ID in payload for reference
- Add validation to detect duplicate IDs

### Risk 3: Query Performance Not Meeting Expectations
**Likelihood**: Low  
**Impact**: Medium  
**Mitigation**:
- Test query latency after quantization
- Compare with baseline (should be <500ms vs 30s+)
- Have rollback plan (restore from backup)

### Risk 4: Quantization Fails or Degrades Accuracy
**Likelihood**: Low  
**Impact**: Low  
**Mitigation**:
- Automatic fallback from binary → scalar quantization
- Monitor search quality with sample queries
- Document expected 1-2% accuracy trade-off

### Trade-off 1: Storage vs Performance
- **Choice**: Use binary quantization (lower accuracy, higher speed)
- **Reasoning**: 40x speedup is critical for production; 1-2% accuracy loss is acceptable

### Trade-off 2: Migration Downtime
- **Choice**: Accept brief downtime during collection deletion/creation
- **Reasoning**: Fresh start is cleaner than in-place migration; downtime is <5 minutes

## Migration Plan

### Phase 1: Preparation (Safety First)
1. Verify Qdrant is running and accessible
2. Run `scripts/migrate_to_coderank.py --all --dry-run` to validate files
3. Optionally backup existing collections: `scripts/remove_old_collections.py --backup`
4. Review validation output for any warnings

### Phase 2: Deletion (Clean Slate)
1. Delete old 3584-dim collections: `scripts/remove_old_collections.py --force`
2. Verify collections are deleted via Qdrant dashboard
3. Confirm only 3584-dim collections were removed

### Phase 3: Upload (Bulk Migration)
1. Upload all 768-dim embeddings: `scripts/migrate_to_coderank.py --all --force`
2. Monitor upload progress (9,654 points × 3 collections)
3. Verify quantization is enabled on each collection
4. Check point counts match expected (9,654 per collection)

### Phase 4: Verification (Quality Assurance)
1. Run `scripts/verify_migration.py` to check all collections
2. Test sample searches for each collection
3. Verify query latency <500ms
4. Check metadata is intact (text, original_id, etc.)

### Phase 5: Integration (MCP Update)
1. Update MCP servers to use `CodeRankEmbed` model
2. Test search functionality via MCP
3. Compare search quality with old results (if backup exists)
4. Update documentation with new model name

### Rollback Procedure
If migration fails or results are unsatisfactory:

1. **Restore from backup** (if created):
   ```bash
   # Restore collections from backup JSON
   python scripts/restore_collections.py --backup-dir output/collection_backups/
   ```

2. **Revert code changes**:
   ```bash
   git checkout main src/config/qdrant_upload.py src/ingestion/embedder.py
   ```

3. **Re-upload old embeddings** (if available):
   ```bash
   # Use old 3584-dim embeddings if still available
   python scripts/upload_qdrant_embeddings.py --collection qdrant_ecosystem
   ```

4. **Verify rollback**:
   ```bash
   python scripts/verify_migration.py --dimension 3584
   ```

## Open Questions

1. ✅ **RESOLVED**: Should we keep old 3584-dim embeddings as backup?
   - **Answer**: No, but optionally backup collections before deletion (`--backup` flag)

2. ✅ **RESOLVED**: What happens if binary quantization fails?
   - **Answer**: Automatic fallback to scalar quantization (INT8)

3. ⚠️ **PENDING**: Should MCP servers support both models during transition?
   - **Current**: No, full migration only
   - **Revisit**: If gradual rollout is needed

4. ⚠️ **PENDING**: Do we need performance benchmarks before/after?
   - **Suggested**: Yes, document baseline vs CodeRankEmbed latency
   - **Owner**: To be assigned during implementation

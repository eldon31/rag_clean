# CodeRank Migration Guide

Complete guide for migrating from CodeRankEmbed (768-dim) to CodeRankEmbed (768-dim).

**Date**: October 16, 2025  
**Status**: Ready to execute  
**Embeddings**: ✅ Available in `output/embed_results/`

---

## 🎯 Migration Overview

### What's Changing
- **Model**: `nomic-ai/CodeRankEmbed` → `nomic-ai/CodeRankEmbed`
- **Dimension**: 3584 → 768 (4.7x smaller)
- **Query Speed**: 30+ seconds → ~400ms (75x faster)
- **Memory**: ~4x reduction with quantization

### Available Embeddings
```
✅ output/embed_results/qdrant_ecosystem_embeddings_768.jsonl
✅ output/embed_results/docling_embeddings_768.jsonl
✅ output/embed_results/sentence_transformers_embeddings_768.jsonl
```

---

## 📋 Pre-Migration Checklist

- [ ] Qdrant server is running on `http://localhost:6333`
- [ ] Embeddings exist in `output/embed_results/`
- [ ] Backup space available (if needed)
- [ ] QDRANT_URL and QDRANT_API_KEY are set (if using auth)

---

## 🚀 Migration Steps

### Step 1: Dry Run (Recommended)

Preview what will be deleted without making changes:

```powershell
# Check what collections will be removed
python scripts/remove_old_collections.py --dry-run

# Check what will be uploaded
python scripts/migrate_to_coderank.py --all --dry-run
```

**Expected Output:**
- Lists existing 768-dim collections
- Shows which embedding files will be used
- No actual changes made

---

### Step 2: Backup Old Collections (Optional but Recommended)

Create metadata backup before deletion:

```powershell
python scripts/remove_old_collections.py --backup
```

**Output:**
- Saves collection metadata to `output/collection_backups/collection_backup_TIMESTAMP.json`
- Includes point counts, dimensions, and settings

---

### Step 3: Remove Old Collections

Delete 768-dim collections:

```powershell
# With backup (safer)
python scripts/remove_old_collections.py --backup

# Without backup (if already backed up)
python scripts/remove_old_collections.py --force
```

**What happens:**
- Only deletes collections with dimension=3584 (safety check)
- Skips collections that don't exist or have different dimensions
- Logs what was deleted

---

### Step 4: Upload New 768-dim Embeddings

Upload CodeRankEmbed collections:

```powershell
# Upload all available collections
python scripts/migrate_to_coderank.py --all

# Or upload specific collection
python scripts/migrate_to_coderank.py --collection qdrant_ecosystem
```

**What happens:**
- Creates new collections with 768-dim vectors
- Uploads embeddings from `output/embed_results/`
- Enables binary quantization (40x search speedup)
- Configures optimized HNSW settings

**Expected time**: ~1-3 minutes per collection

---

### Step 5: Verify Migration

Confirm everything worked:

```powershell
# Check all collections
python scripts/verify_migration.py

# Check with search test
python scripts/verify_migration.py --test-search
```

**Success criteria:**
- ✅ All collections show 768-dim
- ✅ Point counts match embedding files
- ✅ Quantization is enabled
- ✅ Search returns results

---

## 🔄 One-Command Migration

Execute all steps in sequence:

```powershell
# Full migration with backup
python scripts/remove_old_collections.py --backup
python scripts/migrate_to_coderank.py --all
python scripts/verify_migration.py --test-search
```

---

## ⚠️ Troubleshooting

### Issue: "Collection already exists"

**Solution 1**: Use `--force` to overwrite:
```powershell
python scripts/migrate_to_coderank.py --all --force
```

**Solution 2**: Delete manually first:
```powershell
python scripts/remove_old_collections.py --force
python scripts/migrate_to_coderank.py --all
```

### Issue: "Embedding file not found"

Check files exist:
```powershell
ls output/embed_results/
```

If missing, re-run Kaggle embedding notebooks or check file paths in `scripts/migrate_to_coderank.py` (COLLECTION_MAPPING).

### Issue: "Wrong dimension"

Verify embedding dimension:
```powershell
# Check first line of JSONL
Get-Content output/embed_results/qdrant_ecosystem_embeddings_768.jsonl -First 1 | ConvertFrom-Json | Select-Object -ExpandProperty embedding | Measure-Object | Select-Object Count
```

Should show `Count: 768`

### Issue: "Connection refused"

Start Qdrant:
```powershell
docker-compose up -d
```

---

## 📊 Expected Results

### Collection Stats (After Migration)

| Collection | Points | Dimension | Quantization | Memory |
|------------|--------|-----------|--------------|--------|
| qdrant_ecosystem | ~1,344 | 768 | Binary | ~5 MB |
| docling | ~XXX | 768 | Binary | ~X MB |

### Performance Improvements

- **Query Embedding**: 30+ sec → ~400ms (75x faster)
- **Search Latency**: <100ms with quantization
- **Memory Usage**: ~75% reduction (768-dim + quantization)
- **Disk Space**: ~80% smaller than 768-dim

---

## 🔄 Rollback Plan

If you need to rollback:

1. **Delete new collections:**
   ```powershell
   # Manually delete via Qdrant UI or API
   ```

2. **Restore from backup:**
   - Re-run original embedding scripts
   - Or restore from Qdrant snapshots (if created)

3. **Revert code changes:**
   - Keep old dimension=3584 in codebase
   - Don't update MCP server yet

---

## ✅ Next Steps (After Migration)

Once verification passes:

1. **Update MCP Server** (Task 2.1):
   ```python
   # mcp_server/qdrant_code_server.py
   VECTOR_SIZE = 768  # CodeRankEmbed
   ```

2. **Add Query Prefix Support** (Task 2.1):
   ```python
   # Add query prefix wrapper for CodeRankEmbed
   QUERY_PREFIX = "Represent this query for searching relevant code: "
   ```

3. **Update All Dimension Constants** (13 files):
   - See audit results for complete list
   - Change `3584` → `768`
   - Change `nomic-ai/CodeRankEmbed` → `nomic-ai/CodeRankEmbed`

4. **Run Integration Tests**:
   ```powershell
   python test_mcp_search.py
   ```

---

## 📝 Migration Log Template

Track your migration progress:

```
# CodeRank Migration Log

Date: October 16, 2025
Executor: [Your Name]

## Pre-Migration
- [ ] Dry run completed
- [ ] Backup created: output/collection_backups/collection_backup_YYYYMMDD_HHMMSS.json
- [ ] Old collections: [list names]

## Migration
- [ ] Old collections removed at: HH:MM
- [ ] New collections uploaded at: HH:MM
  - [ ] qdrant_ecosystem: X points
  - [ ] docling: X points

## Post-Migration
- [ ] Verification passed
- [ ] Search tested: ✅/❌
- [ ] Performance measured: XXXms query embedding

## Issues
- [List any issues and resolutions]

## Sign-off
Migration Status: ✅ SUCCESS / ❌ FAILED
Verified By: [Your Name]
```

---

## 🆘 Support

If migration fails:

1. Check logs for specific error messages
2. Verify Qdrant connection: `http://localhost:6333/dashboard`
3. Review embedding files format (JSONL with id, embedding, text, metadata)
4. Check dimension in files matches 768
5. Ensure sufficient disk space

**Key Files:**
- Migration scripts: `scripts/remove_old_collections.py`, `scripts/migrate_to_coderank.py`
- Embeddings: `output/embed_results/*.jsonl`
- Backups: `output/collection_backups/`
- Tasks: `openspec/changes/optimize-qdrant-with-ecosystem/tasks.md`

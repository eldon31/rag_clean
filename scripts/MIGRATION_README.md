# CodeRank Migration Scripts

Quick reference for migrating from nomic-embed-code (3584-dim) to CodeRankEmbed (768-dim).

## 🚀 Quick Start

### One-Command Migration

```powershell
# Dry run (preview changes)
.\scripts\run_migration.ps1 -DryRun

# Execute migration with backup
.\scripts\run_migration.ps1

# Execute without backup (faster, less safe)
.\scripts\run_migration.ps1 -SkipBackup

# Force overwrite existing collections
.\scripts\run_migration.ps1 -Force
```

---

## 📁 Available Scripts

### 1. `remove_old_collections.py`
Removes old 3584-dim collections with safety checks.

```powershell
# Preview what will be deleted
python scripts/remove_old_collections.py --dry-run

# Delete with metadata backup
python scripts/remove_old_collections.py --backup

# Delete without backup (dangerous!)
python scripts/remove_old_collections.py --force
```

**Safety Features:**
- Only deletes collections with dimension=3584
- Creates JSON backup of metadata
- Skips non-existent collections

---

### 2. `migrate_to_coderank.py`
Uploads 768-dim embeddings to new collections.

```powershell
# Upload all available collections
python scripts/migrate_to_coderank.py --all

# Upload specific collection
python scripts/migrate_to_coderank.py --collection qdrant_ecosystem

# Preview without uploading
python scripts/migrate_to_coderank.py --all --dry-run

# Force overwrite existing
python scripts/migrate_to_coderank.py --all --force
```

**Features:**
- Automatic batch upload (100 points/batch)
- Enables binary quantization (40x speedup)
- Optimized HNSW settings
- Dimension validation (768 only)

---

### 3. `verify_migration.py`
Verifies migration completed successfully.

```powershell
# Check all collections
python scripts/verify_migration.py

# Check specific collection
python scripts/verify_migration.py --collection qdrant_ecosystem

# Check with search test
python scripts/verify_migration.py --test-search
```

**Checks:**
- ✅ Dimension is 768
- ✅ Point counts match
- ✅ Quantization enabled
- ✅ Search works

---

### 4. `run_migration.ps1` (Automated)
Full migration automation script.

```powershell
# Interactive migration (with prompts)
.\scripts\run_migration.ps1

# Silent migration (no prompts)
.\scripts\run_migration.ps1 -Force

# Preview only
.\scripts\run_migration.ps1 -DryRun
```

**Workflow:**
1. Checks prerequisites (Qdrant, files)
2. Backs up old collections
3. Removes old collections
4. Uploads new embeddings
5. Verifies migration
6. Shows next steps

---

## 📊 Expected Timeline

| Step | Time | Action |
|------|------|--------|
| Prerequisites | 1 min | Check Qdrant, files |
| Backup | 1 min | Save metadata |
| Remove | 30 sec | Delete old collections |
| Upload | 2-5 min | Upload 768-dim embeddings |
| Verify | 30 sec | Check success |
| **Total** | **5-8 min** | **Complete migration** |

---

## ⚠️ Prerequisites

Before running migration:

- [x] Qdrant running on `http://localhost:6333`
- [x] Embeddings exist in `output/embed_results/`
- [x] Python dependencies installed (`qdrant-client`, `tqdm`)
- [x] Sufficient disk space (~100 MB per collection)

Check with:
```powershell
# Check Qdrant
curl http://localhost:6333

# Check embeddings
ls output/embed_results/*.jsonl

# Check Python
python --version
pip show qdrant-client
```

---

## 🎯 Collection Mapping

Current embedding files and target collections:

| Embedding File | Collection Name | Status |
|----------------|-----------------|--------|
| `qdrant_ecosystem_embeddings_768.jsonl` | `qdrant_ecosystem` | ✅ Ready |
| `docling_embeddings_768.jsonl` | `docling` | ✅ Ready |
| `sentence_transformers_embeddings_768.jsonl` | *(future)* | ⏸️ Not mapped |

To add more collections, edit `COLLECTION_MAPPING` in `migrate_to_coderank.py`.

---

## 🔍 Troubleshooting

### "Collection already exists"
```powershell
# Option 1: Force overwrite
python scripts/migrate_to_coderank.py --all --force

# Option 2: Delete first
python scripts/remove_old_collections.py --force
python scripts/migrate_to_coderank.py --all
```

### "Qdrant connection failed"
```powershell
# Start Qdrant
docker-compose up -d

# Check status
docker ps
curl http://localhost:6333
```

### "Embedding file not found"
```powershell
# Check files exist
ls output/embed_results/

# Verify file names match COLLECTION_MAPPING
Get-Content scripts/migrate_to_coderank.py | Select-String "COLLECTION_MAPPING"
```

### "Wrong dimension"
```powershell
# Check embedding dimension in file
Get-Content output/embed_results/qdrant_ecosystem_embeddings_768.jsonl -First 1 | ConvertFrom-Json | Select-Object -ExpandProperty embedding | Measure-Object

# Should output: Count: 768
```

---

## 📋 Migration Checklist

```
Pre-Migration:
[ ] Qdrant is running
[ ] Embedding files exist (768-dim)
[ ] Backup space available
[ ] Python dependencies installed

Migration:
[ ] Dry run completed successfully
[ ] Backup created (or skipped intentionally)
[ ] Old collections removed
[ ] New embeddings uploaded
[ ] Verification passed
[ ] Search tested

Post-Migration:
[ ] Update MCP server (VECTOR_SIZE = 768)
[ ] Add query prefix support
[ ] Update dimension constants (13 files)
[ ] Run integration tests
[ ] Update documentation
```

---

## 📖 Documentation

- **Full Guide**: `MIGRATION_GUIDE.md`
- **Task List**: `openspec/changes/optimize-qdrant-with-ecosystem/tasks.md`
- **Audit Report**: See previous codebase audit

---

## 🆘 Rollback

If migration fails:

```powershell
# Delete new collections (manual via Qdrant UI or API)

# Re-upload old embeddings (if you have them)
# Or re-run original embedding scripts
```

**Note**: Always run with `--backup` first time for safety!

---

## ✅ Success Criteria

Migration is successful when:

- ✅ All collections show 768-dim vectors
- ✅ Point counts match embedding files
- ✅ Quantization enabled
- ✅ Search returns relevant results
- ✅ Query embedding time ~400ms (vs 30+ sec)

Run verification:
```powershell
python scripts/verify_migration.py --test-search
```

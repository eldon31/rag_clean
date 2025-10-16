# CodeRank Migration Automation Script
# Executes full migration from 3584-dim to 768-dim

param(
    [switch]$DryRun,
    [switch]$Force,
    [switch]$SkipBackup
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "CODERANK MIGRATION - Automated Execution" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Configuration
$ScriptsDir = "scripts"
$BackupDir = "output/collection_backups"
$EmbedDir = "output/embed_results"

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Qdrant connection
try {
    $response = Invoke-WebRequest -Uri "http://localhost:6333" -Method Get -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Qdrant is running on http://localhost:6333" -ForegroundColor Green
} catch {
    Write-Host "❌ Qdrant is not running!" -ForegroundColor Red
    Write-Host "   Please start Qdrant: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

# Check embedding files
if (-not (Test-Path $EmbedDir)) {
    Write-Host "❌ Embedding directory not found: $EmbedDir" -ForegroundColor Red
    exit 1
}

$embedFiles = Get-ChildItem "$EmbedDir\*_embeddings_768.jsonl"
if ($embedFiles.Count -eq 0) {
    Write-Host "❌ No embedding files found in $EmbedDir" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found $($embedFiles.Count) embedding files:" -ForegroundColor Green
foreach ($file in $embedFiles) {
    $size = [math]::Round($file.Length / 1MB, 2)
    Write-Host "   - $($file.Name) ($size MB)" -ForegroundColor Gray
}
Write-Host ""

# Check Python and dependencies
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan

# Ask for confirmation unless DryRun or Force
if (-not $DryRun -and -not $Force) {
    Write-Host ""
    Write-Host "⚠️  WARNING: This will DELETE old 3584-dim collections!" -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "Continue with migration? (yes/no)"
    
    if ($confirm -ne "yes") {
        Write-Host "❌ Migration cancelled by user" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""

# Step 1: Dry Run (if requested)
if ($DryRun) {
    Write-Host "🔍 STEP 1: Dry Run (Preview)" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Previewing collection removal..." -ForegroundColor Yellow
    python "$ScriptsDir\remove_old_collections.py" --dry-run
    
    Write-Host ""
    Write-Host "Previewing migration..." -ForegroundColor Yellow
    python "$ScriptsDir\migrate_to_coderank.py" --all --dry-run
    
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "✅ Dry run complete. Remove -DryRun flag to execute." -ForegroundColor Green
    exit 0
}

# Step 2: Backup (unless skipped)
if (-not $SkipBackup) {
    Write-Host "📦 STEP 1: Backup Old Collections" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    
    python "$ScriptsDir\remove_old_collections.py" --backup
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Backup failed! Migration aborted." -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "✅ Backup completed" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⏭️  STEP 1: Skipping backup (--SkipBackup flag)" -ForegroundColor Yellow
    Write-Host ""
    
    # Still delete collections
    Write-Host "🗑️  STEP 1: Remove Old Collections" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    
    python "$ScriptsDir\remove_old_collections.py" --force
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Collection removal failed! Migration aborted." -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
}

# Step 3: Upload New Embeddings
Write-Host "⬆️  STEP 2: Upload 768-dim Embeddings" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$forceFlag = if ($Force) { "--force" } else { "" }
python "$ScriptsDir\migrate_to_coderank.py" --all $forceFlag

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Migration failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Upload completed" -ForegroundColor Green
Write-Host ""

# Step 4: Verification
Write-Host "✅ STEP 3: Verify Migration" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

python "$ScriptsDir\verify_migration.py" --test-search

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Verification failed! Check errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🎉 MIGRATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Update MCP server to use CodeRankEmbed (VECTOR_SIZE = 768)" -ForegroundColor White
Write-Host "2. Add query prefix support for CodeRankEmbed" -ForegroundColor White
Write-Host "3. Update dimension constants in codebase (13 files)" -ForegroundColor White
Write-Host "4. Run integration tests: python test_mcp_search.py" -ForegroundColor White
Write-Host ""
Write-Host "See MIGRATION_GUIDE.md for details" -ForegroundColor Gray
Write-Host ""

exit 0

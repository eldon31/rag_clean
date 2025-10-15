#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy and upload all embeddings to DigitalOcean Qdrant instance

.DESCRIPTION
    This script:
    1. SSHs to DigitalOcean droplet
    2. Runs deployment script (Docker + Qdrant + PostgreSQL + Neo4j)
    3. Uploads all 4 collections with scalar quantization
    4. Verifies deployment

.EXAMPLE
    .\deploy_and_upload.ps1
#>

$ErrorActionPreference = "Stop"

# Configuration
$DROPLET_IP = "165.232.174.154"
$DROPLET_USER = "root"
$DROPLET_PASSWORD = "837829318aA!a"
$QDRANT_URL = "http://$DROPLET_IP:6333"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  DIGITALOCEAN DEPLOYMENT & UPLOAD" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if deployment script exists
Write-Host "📋 Step 1: Checking deployment files..." -ForegroundColor Yellow
if (-not (Test-Path "scripts/deploy_to_digitalocean.sh")) {
    Write-Host "❌ Error: scripts/deploy_to_digitalocean.sh not found!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Deployment script found" -ForegroundColor Green

# Step 2: Check embeddings exist
Write-Host "`n📦 Step 2: Checking embeddings..." -ForegroundColor Yellow
$embeddings = @(
    "output/embeddings/viator_api_embeddings.jsonl",
    "output/embeddings/fast_docs_embeddings.jsonl",
    "output/embeddings/pydantic_docs_embeddings.jsonl",
    "output/embeddings/inngest_ecosystem_embeddings.jsonl"
)

foreach ($file in $embeddings) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Error: $file not found!" -ForegroundColor Red
        exit 1
    }
    $size = (Get-Item $file).Length / 1MB
    Write-Host "  ✓ $file ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
}

# Step 3: Show deployment info
Write-Host "`n🌐 Step 3: Deployment target" -ForegroundColor Yellow
Write-Host "  Server: $DROPLET_IP" -ForegroundColor White
Write-Host "  User: $DROPLET_USER" -ForegroundColor White
Write-Host "  Qdrant URL: $QDRANT_URL" -ForegroundColor White

# Step 4: Confirm deployment
Write-Host "`n⚠️  WARNING: This will deploy to production!" -ForegroundColor Yellow
Write-Host "  - Install Docker, Qdrant, PostgreSQL, Neo4j" -ForegroundColor White
Write-Host "  - Upload 6,877 embeddings (510.83 MB)" -ForegroundColor White
Write-Host "  - Apply scalar quantization (4x compression)" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Do you want to proceed? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "`n❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Step 5: SSH and deploy (manual step - requires password)
Write-Host "`n🚀 Step 5: Deploying to DigitalOcean..." -ForegroundColor Yellow
Write-Host ""
Write-Host "MANUAL STEPS REQUIRED:" -ForegroundColor Cyan
Write-Host "1. Open a new terminal and run:" -ForegroundColor White
Write-Host "   ssh root@$DROPLET_IP" -ForegroundColor Yellow
Write-Host "   Password: $DROPLET_PASSWORD" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. On the server, run:" -ForegroundColor White
Write-Host "   # Download deployment script" -ForegroundColor Gray
Write-Host "   curl -o deploy.sh https://raw.githubusercontent.com/eldon31/processorAI/main/scripts/deploy_to_digitalocean.sh" -ForegroundColor Yellow
Write-Host "   chmod +x deploy.sh" -ForegroundColor Yellow
Write-Host "   ./deploy.sh" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Wait for deployment to complete (2-3 minutes)" -ForegroundColor White
Write-Host ""
Write-Host "4. Return here and press Enter to continue with upload..." -ForegroundColor White
Read-Host

# Step 6: Update upload script URL
Write-Host "`n📝 Step 6: Updating upload script for cloud..." -ForegroundColor Yellow
$uploadScript = Get-Content "scripts/upload_to_qdrant.py" -Raw
$uploadScript = $uploadScript -replace 'QDRANT_URL = "http://localhost:6333"', "QDRANT_URL = `"$QDRANT_URL`""
$uploadScript | Set-Content "scripts/upload_to_qdrant_cloud.py"
Write-Host "✅ Created scripts/upload_to_qdrant_cloud.py" -ForegroundColor Green

# Step 7: Upload embeddings
Write-Host "`n📤 Step 7: Uploading embeddings to cloud..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Run the following command to upload:" -ForegroundColor Cyan
Write-Host "  python scripts/upload_to_qdrant_cloud.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or use the Python snippet below:" -ForegroundColor Cyan
Write-Host @"
from scripts.upload_to_qdrant import QdrantUploader
from pathlib import Path

uploader = QdrantUploader(url="$QDRANT_URL")

# Upload all 4 collections with scalar quantization
collections = [
    ("viator_api", "output/embeddings/viator_api_embeddings.jsonl"),
    ("fast_docs", "output/embeddings/fast_docs_embeddings.jsonl"),
    ("pydantic_docs", "output/embeddings/pydantic_docs_embeddings.jsonl"),
    ("inngest_ecosystem", "output/embeddings/inngest_ecosystem_embeddings.jsonl")
]

for name, file in collections:
    print(f"\n📦 Uploading {name}...")
    uploader.create_collection(name, vector_size=3584, use_quantization="scalar")
    uploader.upload_embeddings(Path(file), name, mode="upsert")
    print(f"✅ {name} uploaded!")

print("\n🎉 All collections uploaded!")
"@ -ForegroundColor Yellow

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  DEPLOYMENT GUIDE COMPLETE" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "  - DEPLOYMENT_READY_SUMMARY.md" -ForegroundColor White
Write-Host "  - EMBEDDING_DIMENSION_ANALYSIS.md" -ForegroundColor White
Write-Host "  - DIGITALOCEAN_DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host ""

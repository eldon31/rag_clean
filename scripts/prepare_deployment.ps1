# Start Qdrant and reset all collections
# Run this to prepare for fresh deployment

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "QDRANT DEPLOYMENT PREPARATION" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan

# Start Qdrant with Docker Compose
Write-Host "`nStarting Qdrant..." -ForegroundColor Green
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nFailed to start Qdrant with docker-compose" -ForegroundColor Red
    Write-Host "Trying Docker Desktop..." -ForegroundColor Yellow
    docker run -d -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage --name qdrant qdrant/qdrant:latest
}

# Wait for Qdrant to be ready
Write-Host "`nWaiting for Qdrant to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if Qdrant is running
try {
    $null = Invoke-WebRequest -Uri "http://localhost:6333/collections" -Method GET -ErrorAction Stop
    Write-Host "Qdrant is running!" -ForegroundColor Green
} catch {
    Write-Host "`nQdrant is not responding" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and run this script again" -ForegroundColor Yellow
    exit 1
}

# Reset Qdrant (delete all collections)
Write-Host "`nDeleting all collections..." -ForegroundColor Yellow
python scripts/reset_qdrant.py

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "QDRANT READY FOR DEPLOYMENT" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan

Write-Host "`nQdrant Dashboard: " -NoNewline
Write-Host "http://localhost:6333/dashboard" -ForegroundColor Cyan

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Wait for Kaggle embedding to complete" 
Write-Host "2. Download docling_embeddings.jsonl from Kaggle"
Write-Host "3. Place in output/docling/embeddings/"
Write-Host "4. Run: python scripts/upload_to_qdrant.py"

# DigitalOcean Docker Status Dashboard
# Shows your cloud containers running status

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   DIGITALOCEAN DOCKER STATUS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Current context
$currentContext = docker context show
Write-Host "Current Docker Context: $currentContext" -ForegroundColor $(if ($currentContext -eq 'digitalocean') { 'Green' } else { 'Yellow' })
Write-Host ""

# Container status
Write-Host "Running Containers:" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

# Qdrant API Check
Write-Host "Service Health Checks:" -ForegroundColor Cyan
try {
    $qdrantInfo = Invoke-RestMethod -Uri "http://146.190.96.193:6333/" -ErrorAction Stop
    Write-Host "   Qdrant API: ONLINE (v$($qdrantInfo.version))" -ForegroundColor Green
} catch {
    Write-Host "   Qdrant API: OFFLINE" -ForegroundColor Red
}
Write-Host ""

# Access URLs
Write-Host "Access Your Services:" -ForegroundColor Cyan
Write-Host "  Qdrant Dashboard:  http://146.190.96.193:6333/dashboard" -ForegroundColor Yellow
Write-Host "  Qdrant API:        http://146.190.96.193:6333" -ForegroundColor Yellow
Write-Host "  Qdrant gRPC:       146.190.96.193:6334" -ForegroundColor Yellow
Write-Host ""

# Quick commands
Write-Host "Quick Commands:" -ForegroundColor Cyan
Write-Host "  View logs:         docker compose -f docker-compose.remote.yml logs -f" -ForegroundColor White
Write-Host "  Restart:           docker compose -f docker-compose.remote.yml restart" -ForegroundColor White
Write-Host "  Stop:              docker compose -f docker-compose.remote.yml down" -ForegroundColor White
Write-Host "  Switch to local:   docker context use default" -ForegroundColor White
Write-Host ""

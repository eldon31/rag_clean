# Test script for awesome-copilot MCP server
Write-Host "Testing awesome-copilot MCP server installation..." -ForegroundColor Cyan

# Check if Docker is running
Write-Host "`nChecking Docker status..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    Write-Host "  Run: Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'" -ForegroundColor Yellow
    exit 1
}

# Pull the awesome-copilot image
Write-Host "`nPulling awesome-copilot Docker image..." -ForegroundColor Yellow
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Image pulled successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to pull image" -ForegroundColor Red
    exit 1
}

# Test running the container
Write-Host "`nTesting container..." -ForegroundColor Yellow
Write-Host "Note: This will start the MCP server. Press Ctrl+C to stop." -ForegroundColor Gray

# Run the container in interactive mode
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

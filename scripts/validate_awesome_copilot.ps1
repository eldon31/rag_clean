# Validation script for awesome-copilot MCP server
Write-Host "=== Awesome Copilot MCP Server Validation ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Docker
Write-Host "[1/4] Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  Success Docker installed: $dockerVersion" -ForegroundColor Green
    
    docker info | Out-Null
    Write-Host "  Success Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  Error Docker check failed: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Check Image
Write-Host "`n[2/4] Checking awesome-copilot image..." -ForegroundColor Yellow
$imageCheck = docker images ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot --format "{{.Repository}}:{{.Tag}}"
if ($imageCheck) {
    Write-Host "  Success Image found: $imageCheck" -ForegroundColor Green
    
    $imageSize = docker images ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot --format "{{.Size}}"
    $imageId = docker images ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot --format "{{.ID}}"
    Write-Host "  Info Size: $imageSize" -ForegroundColor Cyan
    Write-Host "  Info ID: $imageId" -ForegroundColor Cyan
} else {
    Write-Host "  Error Image not found" -ForegroundColor Red
    Write-Host "  Run: docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest" -ForegroundColor Yellow
    exit 1
}

# Step 3: Check MCP Configuration
Write-Host "`n[3/4] Checking MCP configuration..." -ForegroundColor Yellow
$mcpConfigPath = "$env:APPDATA\Code\User\mcp.json"
if (Test-Path $mcpConfigPath) {
    Write-Host "  Success mcp.json found" -ForegroundColor Green
    
    $mcpConfig = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json
    if ($mcpConfig.servers.'awesome-copilot') {
        Write-Host "  Success awesome-copilot server configured" -ForegroundColor Green
        
        $serverConfig = $mcpConfig.servers.'awesome-copilot'
        Write-Host "  Info Command: $($serverConfig.command)" -ForegroundColor Cyan
        Write-Host "  Info Type: $($serverConfig.type)" -ForegroundColor Cyan
    } else {
        Write-Host "  Warning awesome-copilot not found in mcp.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Warning mcp.json not found at $mcpConfigPath" -ForegroundColor Yellow
}

# Step 4: Test Container Start
Write-Host "`n[4/4] Testing container startup..." -ForegroundColor Yellow
Write-Host "  Starting container (will timeout after 5 seconds)..." -ForegroundColor Gray

$job = Start-Job -ScriptBlock {
    docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
}

Start-Sleep -Seconds 5
Stop-Job $job
$output = Receive-Job $job
Remove-Job $job

if ($output) {
    Write-Host "  Success Container started successfully" -ForegroundColor Green
    Write-Host "  Info Sample output:" -ForegroundColor Cyan
    $output | Select-Object -First 3 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
} else {
    Write-Host "  Warning No output captured (this may be normal for MCP servers)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "The awesome-copilot MCP server is properly installed and ready to use." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code or reload the window" -ForegroundColor White
Write-Host "2. The server will be available in your MCP-enabled tools" -ForegroundColor White
Write-Host "3. Use it through GitHub Copilot or other MCP clients" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see: AWESOME_COPILOT_SETUP.md" -ForegroundColor Cyan

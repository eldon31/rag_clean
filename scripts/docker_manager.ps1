# Manage Docker Desktop Connection to DigitalOcean
# Quick helper script for common operations

param(
    [Parameter(Position=0)]
    [ValidateSet("connect", "disconnect", "status", "switch-remote", "switch-local", "deploy")]
    [string]$Action = "connect",
    
    [string]$DropletIP = "146.190.96.193"
)

function Show-Status {
    Write-Host "📊 Docker Context Status" -ForegroundColor Cyan
    Write-Host ""
    docker context ls
    Write-Host ""
    $currentContext = docker context show
    Write-Host "Current context: $currentContext" -ForegroundColor Yellow
    
    if ($currentContext -eq "digitalocean") {
        Write-Host "✓ Connected to DigitalOcean" -ForegroundColor Green
        Write-Host ""
        Write-Host "Remote containers:" -ForegroundColor Cyan
        docker ps
    } else {
        Write-Host "✓ Using local Docker Desktop" -ForegroundColor Green
        Write-Host ""
        Write-Host "Local containers:" -ForegroundColor Cyan
        docker ps
    }
}

function Connect-DigitalOcean {
    Write-Host "🔗 Connecting to DigitalOcean Docker..." -ForegroundColor Cyan
    & "$PSScriptRoot\connect_docker_desktop.ps1" -DropletIP $DropletIP
}

function Disconnect-DigitalOcean {
    Write-Host "🔌 Disconnecting from DigitalOcean..." -ForegroundColor Cyan
    
    # Switch back to default context
    docker context use default
    Write-Host "✓ Switched to local Docker Desktop" -ForegroundColor Green
    
    # Stop SSH tunnel jobs
    $sshJobs = Get-Job | Where-Object { $_.Command -like "*ssh*" -and $_.Command -like "*23750*" }
    if ($sshJobs) {
        Write-Host "🛑 Stopping SSH tunnel..." -ForegroundColor Yellow
        $sshJobs | Stop-Job
        $sshJobs | Remove-Job
        Write-Host "✓ SSH tunnel stopped" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "✅ Disconnected from DigitalOcean" -ForegroundColor Green
}

function Switch-ToRemote {
    Write-Host "🌐 Switching to DigitalOcean Docker..." -ForegroundColor Cyan
    docker context use digitalocean
    Write-Host "✓ Now using DigitalOcean Docker" -ForegroundColor Green
    Write-Host ""
    docker ps
}

function Switch-ToLocal {
    Write-Host "💻 Switching to local Docker Desktop..." -ForegroundColor Cyan
    docker context use default
    Write-Host "✓ Now using local Docker Desktop" -ForegroundColor Green
    Write-Host ""
    docker ps
}

function Deploy-ToRemote {
    Write-Host "🚀 Deploying to DigitalOcean..." -ForegroundColor Cyan
    Write-Host ""
    
    # Ensure we're using the DigitalOcean context
    $currentContext = docker context show
    if ($currentContext -ne "digitalocean") {
        Write-Host "📍 Switching to DigitalOcean context..." -ForegroundColor Yellow
        docker context use digitalocean
    }
    
    # Check if docker-compose.yml exists
    if (-not (Test-Path "docker-compose.yml")) {
        Write-Host "❌ docker-compose.yml not found in current directory" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "📦 Pulling images..." -ForegroundColor Cyan
    docker compose pull
    
    Write-Host ""
    Write-Host "🛑 Stopping existing containers..." -ForegroundColor Cyan
    docker compose down
    
    Write-Host ""
    Write-Host "🚀 Starting containers..." -ForegroundColor Cyan
    docker compose up -d
    
    Write-Host ""
    Write-Host "✅ Deployment complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Container status:" -ForegroundColor Cyan
    docker compose ps
    
    Write-Host ""
    Write-Host "🌐 Access your services at:" -ForegroundColor Cyan
    Write-Host "  - Qdrant: http://$DropletIP:6333/dashboard" -ForegroundColor Yellow
}

# Main script logic
switch ($Action) {
    "connect" { Connect-DigitalOcean }
    "disconnect" { Disconnect-DigitalOcean }
    "status" { Show-Status }
    "switch-remote" { Switch-ToRemote }
    "switch-local" { Switch-ToLocal }
    "deploy" { Deploy-ToRemote }
}

# Deploy RAG System to DigitalOcean Droplet
# This script deploys your Docker containers to the remote droplet

param(
    [string]$DropletIP = "146.190.96.193",
    [string]$User = "root",
    [string]$ProjectPath = "C:\Users\raze0\Documents\LLM_KNOWLEDGE_CREATOR\RAG"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   DEPLOYING TO DIGITALOCEAN DROPLET" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Droplet IP: $DropletIP" -ForegroundColor Yellow
Write-Host "User: $User" -ForegroundColor Yellow
Write-Host ""

# Test SSH connection
Write-Host "🔐 Testing SSH connection..." -ForegroundColor Cyan
try {
    ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$User@$DropletIP" "echo 'SSH connection successful'"
    Write-Host "✓ SSH connection working" -ForegroundColor Green
} catch {
    Write-Host "✗ SSH connection failed" -ForegroundColor Red
    Write-Host "Please ensure:" -ForegroundColor Yellow
    Write-Host "  1. Your SSH key is loaded: ssh-add C:\Users\raze0\.ssh\id_ed25519" -ForegroundColor Yellow
    Write-Host "  2. The droplet is accessible: ping $DropletIP" -ForegroundColor Yellow
    exit 1
}

# Create remote directory
Write-Host ""
Write-Host "📁 Creating remote project directory..." -ForegroundColor Cyan
ssh "$User@$DropletIP" "mkdir -p /opt/rag-system"
Write-Host "✓ Directory created: /opt/rag-system" -ForegroundColor Green

# Copy docker-compose.yml
Write-Host ""
Write-Host "📤 Uploading docker-compose.yml..." -ForegroundColor Cyan
scp "$ProjectPath\docker-compose.yml" "$User@${DropletIP}:/opt/rag-system/"
Write-Host "✓ docker-compose.yml uploaded" -ForegroundColor Green

# Copy additional compose files if they exist
if (Test-Path "$ProjectPath\docker-compose.qdrant-mcp.yml") {
    Write-Host "📤 Uploading docker-compose.qdrant-mcp.yml..." -ForegroundColor Cyan
    scp "$ProjectPath\docker-compose.qdrant-mcp.yml" "$User@${DropletIP}:/opt/rag-system/"
    Write-Host "✓ docker-compose.qdrant-mcp.yml uploaded" -ForegroundColor Green
}

# Copy Dockerfiles if they exist
if (Test-Path "$ProjectPath\Dockerfile.qdrant-mcp") {
    Write-Host "📤 Uploading Dockerfile.qdrant-mcp..." -ForegroundColor Cyan
    scp "$ProjectPath\Dockerfile.qdrant-mcp" "$User@${DropletIP}:/opt/rag-system/"
    Write-Host "✓ Dockerfile.qdrant-mcp uploaded" -ForegroundColor Green
}

# Copy MCP server files if they exist
if (Test-Path "$ProjectPath\mcp_server") {
    Write-Host "📤 Uploading MCP server files..." -ForegroundColor Cyan
    ssh "$User@$DropletIP" "mkdir -p /opt/rag-system/mcp_server"
    scp -r "$ProjectPath\mcp_server\"* "$User@${DropletIP}:/opt/rag-system/mcp_server/"
    Write-Host "✓ MCP server files uploaded" -ForegroundColor Green
}

# Copy requirements files
if (Test-Path "$ProjectPath\requirements-mcp.txt") {
    Write-Host "📤 Uploading requirements-mcp.txt..." -ForegroundColor Cyan
    scp "$ProjectPath\requirements-mcp.txt" "$User@${DropletIP}:/opt/rag-system/"
    Write-Host "✓ requirements-mcp.txt uploaded" -ForegroundColor Green
}

# Setup and start Docker containers on remote
Write-Host ""
Write-Host "🐳 Setting up Docker containers on remote server..." -ForegroundColor Cyan

$remoteSetupScript = @'
#!/bin/bash
set -e

echo "📍 Working directory: /opt/rag-system"
cd /opt/rag-system

echo ""
echo "🛑 Stopping existing containers (if any)..."
docker-compose down 2>/dev/null || true

echo ""
echo "🗑️  Removing old images (if any)..."
docker-compose rm -f 2>/dev/null || true

echo ""
echo "📦 Pulling latest images..."
docker-compose pull

echo ""
echo "🚀 Starting containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "📊 Container status:"
docker-compose ps

echo ""
echo "🔍 Checking Qdrant health..."
curl -f http://localhost:6333/health || echo "Warning: Qdrant not responding yet"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - Check status: docker-compose ps"
'@

# Write script to remote server
Write-Host "📝 Creating deployment script on remote server..." -ForegroundColor Cyan
$remoteSetupScript | ssh "$User@$DropletIP" "cat > /opt/rag-system/setup.sh && chmod +x /opt/rag-system/setup.sh"

# Execute deployment script
Write-Host "🚀 Executing deployment on remote server..." -ForegroundColor Cyan
Write-Host ""
ssh "$User@$DropletIP" "/opt/rag-system/setup.sh"

# Final status check
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   DEPLOYMENT COMPLETED" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your services are now running at:" -ForegroundColor Cyan
Write-Host "  - Qdrant HTTP API: http://$DropletIP:6333" -ForegroundColor Yellow
Write-Host "  - Qdrant gRPC API: http://$DropletIP:6334" -ForegroundColor Yellow
Write-Host "  - Qdrant Dashboard: http://$DropletIP:6333/dashboard" -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 Management commands:" -ForegroundColor Cyan
Write-Host "  - SSH to server: ssh $User@$DropletIP" -ForegroundColor Yellow
Write-Host "  - View logs: ssh $User@$DropletIP 'cd /opt/rag-system && docker-compose logs -f'" -ForegroundColor Yellow
Write-Host "  - Restart: ssh $User@$DropletIP 'cd /opt/rag-system && docker-compose restart'" -ForegroundColor Yellow
Write-Host ""

#!/bin/bash
set -e

echo "=========================================="
echo "DIGITALOCEAN DOCKER DEPLOYMENT"
echo "=========================================="
echo ""

# Update system
echo "📦 Step 1: Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

# Install Docker
echo ""
echo "🐳 Step 2: Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker installed successfully"
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
echo ""
echo "🔧 Step 3: Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed successfully"
else
    echo "✅ Docker Compose already installed"
fi

# Show versions
echo ""
echo "📋 Installed versions:"
docker --version
docker-compose --version

# Setup UFW firewall
echo ""
echo "🔥 Step 4: Configuring firewall..."
if ! command -v ufw &> /dev/null; then
    apt-get install -y ufw
fi

ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 6333/tcp  # Qdrant HTTP
ufw allow 6334/tcp  # Qdrant gRPC
ufw allow 5432/tcp  # PostgreSQL
ufw allow 7474/tcp  # Neo4j HTTP
ufw allow 7687/tcp  # Neo4j Bolt
ufw reload

echo "✅ Firewall configured"

# Create docker-compose.yml
echo ""
echo "📝 Step 5: Creating docker-compose.yml..."
mkdir -p /opt/rag-stack
cd /opt/rag-stack

cat > docker-compose.yml <<'EOF'
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"  # HTTP API
      - "6334:6334"  # gRPC
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:16-alpine
    container_name: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=raguser
      - POSTGRES_PASSWORD=ragpass123
      - POSTGRES_DB=rag_knowledge
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U raguser"]
      interval: 30s
      timeout: 10s
      retries: 3

  neo4j:
    image: neo4j:5.15-community
    container_name: neo4j
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    environment:
      - NEO4J_AUTH=neo4j/ragpass123
      - NEO4J_dbms_memory_pagecache_size=512M
      - NEO4J_dbms_memory_heap_max__size=1G
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:7474"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  qdrant_storage:
    driver: local
  postgres_data:
    driver: local
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local

networks:
  default:
    name: rag-network
EOF

echo "✅ docker-compose.yml created"

# Start services
echo ""
echo "🚀 Step 6: Starting Docker services..."
docker-compose down --remove-orphans 2>/dev/null || true
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Step 7: Service status:"
docker-compose ps

# Test connections
echo ""
echo "🔍 Step 8: Testing connections..."

# Test Qdrant
if curl -s http://localhost:6333/ > /dev/null; then
    echo "✅ Qdrant: http://localhost:6333 - READY"
else
    echo "❌ Qdrant: NOT RESPONDING"
fi

# Test PostgreSQL
if docker exec postgres pg_isready -U raguser > /dev/null 2>&1; then
    echo "✅ PostgreSQL: localhost:5432 - READY"
else
    echo "❌ PostgreSQL: NOT RESPONDING"
fi

# Test Neo4j
if curl -s http://localhost:7474 > /dev/null; then
    echo "✅ Neo4j: http://localhost:7474 - READY"
else
    echo "❌ Neo4j: NOT RESPONDING"
fi

echo ""
echo "=========================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "📋 Service URLs (from internet):"
echo "  Qdrant HTTP: http://$(curl -s ifconfig.me):6333"
echo "  Qdrant gRPC: http://$(curl -s ifconfig.me):6334"
echo "  PostgreSQL:  $(curl -s ifconfig.me):5432"
echo "  Neo4j HTTP:  http://$(curl -s ifconfig.me):7474"
echo "  Neo4j Bolt:  bolt://$(curl -s ifconfig.me):7687"
echo ""
echo "🔐 Credentials:"
echo "  PostgreSQL: raguser / ragpass123"
echo "  Neo4j:      neo4j / ragpass123"
echo ""
echo "🛠️  Management commands:"
echo "  cd /opt/rag-stack"
echo "  docker-compose ps        # Check status"
echo "  docker-compose logs -f   # View logs"
echo "  docker-compose restart   # Restart all"
echo "  docker-compose down      # Stop all"
echo ""

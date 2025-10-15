# Quick Start MCP Server Without Docker
# Run this if you want to use MCP server directly without containers

Write-Host "Starting Qdrant MCP Server (Local Mode)" -ForegroundColor Green

# Set environment variables
$env:QDRANT_HOST = "localhost"
$env:QDRANT_PORT = "6333"
$env:COLLECTIONS = "docling,viator_api,fast_docs,pydantic_docs,inngest_ecosystem"

# Start the server
Write-Host "`nCollections: $env:COLLECTIONS" -ForegroundColor Cyan
Write-Host "Qdrant: ${env:QDRANT_HOST}:${env:QDRANT_PORT}`n" -ForegroundColor Cyan

python mcp_server/qdrant_fastmcp_server.py

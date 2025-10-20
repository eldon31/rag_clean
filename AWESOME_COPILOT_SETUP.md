# Awesome Copilot MCP Server Setup Guide

## Overview
The Awesome Copilot MCP server is a .NET-based MCP server that provides various tools and utilities for enhancing your development workflow.

## Prerequisites
1. **Docker Desktop** must be installed and running
2. **VS Code** with MCP support
3. Internet connection to pull the Docker image

## Installation Steps

### 1. Ensure Docker is Running
```powershell
# Check Docker status
docker info

# If Docker is not running, start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### 2. Pull the Awesome Copilot Image
```powershell
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

### 3. Verify MCP Configuration
Your `mcp.json` already includes the correct configuration:
```json
"awesome-copilot": {
  "command": "docker",
  "args": [
    "run",
    "-i",
    "--rm",
    "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
  ],
  "type": "stdio"
}
```

### 4. Test the Server
Run the test script:
```powershell
.\scripts\test_awesome_copilot.ps1
```

Or manually test:
```powershell
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

## Usage

### In VS Code
1. Open the Command Palette (Ctrl+Shift+P)
2. Select "MCP: Connect to Server"
3. Choose "awesome-copilot" from the list
4. The server will start automatically via Docker

### Available Tools
The awesome-copilot server provides various tools (exact tools depend on the version):
- File operations
- Code analysis
- Development utilities
- And more...

## Troubleshooting

### Docker is Paused
**Error:** `Docker Desktop is manually paused`
**Solution:** 
- Open Docker Desktop
- Click the "Resume" button
- Or restart Docker Desktop

### Image Pull Fails
**Error:** Cannot pull image
**Solutions:**
1. Check your internet connection
2. Verify Docker Hub/GitHub Container Registry access
3. Try with authentication if needed:
   ```powershell
   docker login ghcr.io
   ```

### Container Won't Start
**Error:** Container exits immediately
**Solutions:**
1. Check Docker logs:
   ```powershell
   docker logs <container_id>
   ```
2. Verify the image is correctly pulled:
   ```powershell
   docker images | Select-String "awesome-copilot"
   ```
3. Try running with verbose output:
   ```powershell
   docker run -i --rm -e LOG_LEVEL=debug ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
   ```

### MCP Connection Issues
**Error:** Cannot connect to MCP server
**Solutions:**
1. Ensure the server entry exists in `mcp.json`
2. Reload VS Code window (Ctrl+Shift+P → "Developer: Reload Window")
3. Check VS Code output panel for MCP logs
4. Verify Docker is running and accessible

## Advanced Configuration

### Custom Port Mapping (if needed)
If the server requires port exposure:
```json
"awesome-copilot": {
  "command": "docker",
  "args": [
    "run",
    "-i",
    "--rm",
    "-p", "3000:3000",
    "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
  ],
  "type": "stdio"
}
```

### Volume Mounting (if needed)
To share files with the container:
```json
"awesome-copilot": {
  "command": "docker",
  "args": [
    "run",
    "-i",
    "--rm",
    "-v", "C:/Users/raze0/Documents:/workspace",
    "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
  ],
  "type": "stdio"
}
```

## References
- [Microsoft MCP .NET Samples](https://github.com/microsoft/mcp-dotnet-samples)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Docker Documentation](https://docs.docker.com/)

## Quick Commands

```powershell
# Pull latest version
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Run interactively
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Check running containers
docker ps

# View logs of running container
docker logs <container_name>

# Stop all awesome-copilot containers
docker ps | Select-String "awesome-copilot" | ForEach-Object { docker stop $_.ToString().Split()[0] }

# Remove the image (to force re-download)
docker rmi ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

## Next Steps
1. Start Docker Desktop
2. Run the test script: `.\scripts\test_awesome_copilot.ps1`
3. Use the MCP server in VS Code
4. Explore available tools and capabilities

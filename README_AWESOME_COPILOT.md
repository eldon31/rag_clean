# Awesome Copilot MCP Server

A .NET-based Model Context Protocol (MCP) server that enhances your development experience with powerful tools and integrations.

![Status](https://img.shields.io/badge/status-operational-success)
![Docker](https://img.shields.io/badge/docker-required-blue)
![MCP](https://img.shields.io/badge/MCP-compatible-green)

## 📖 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Validation](#validation)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [Resources](#resources)

## 🎯 Overview

The **Awesome Copilot MCP Server** is a containerized Model Context Protocol server built on .NET that provides:

- 🔧 **Enhanced Development Tools**: Advanced coding assistance and utilities
- 📊 **Code Analysis**: Intelligent code understanding and suggestions
- 🔗 **Seamless Integration**: Works with VS Code, GitHub Copilot, and other MCP clients
- 🚀 **Extensible Architecture**: Built on the open Model Context Protocol standard
- 🐳 **Easy Deployment**: Runs in Docker for consistent, isolated execution

## ✅ Prerequisites

Before installing, ensure you have:

1. **Docker Desktop**
   - Version: 20.10 or higher
   - Status: Running
   - Download: [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **VS Code**
   - Version: Latest recommended
   - With MCP support enabled

3. **Internet Connection**
   - Required for initial image pull

4. **Windows PowerShell**
   - Version 5.1 or higher (included in Windows)

### Verify Prerequisites

```powershell
# Check Docker
docker --version
docker info

# Check PowerShell version
$PSVersionTable.PSVersion
```

## 🚀 Quick Start

### One-Command Installation

```powershell
# Pull the Docker image
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Validate installation
.\scripts\validate_awesome_copilot.ps1

# Reload VS Code
# Press Ctrl+Shift+P → "Developer: Reload Window"
```

That's it! The server is now ready to use.

## 📦 Installation

### Step 1: Start Docker Desktop

Ensure Docker Desktop is running:

```powershell
# Check if Docker is running
docker info

# If not running, start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Wait for Docker to be ready (about 30 seconds)
Start-Sleep -Seconds 30
```

### Step 2: Pull the Docker Image

```powershell
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

**Expected Output:**
```
latest: Pulling from microsoft/mcp-dotnet-samples/awesome-copilot
923995841b9c: Pull complete
8c92021e3a05: Pull complete
...
Status: Downloaded newer image for ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

### Step 3: Verify Installation

```powershell
# Check the image is available
docker images | Select-String "awesome-copilot"
```

**Expected Output:**
```
ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot   latest    05dd65197111   14 hours ago    170MB
```

### Step 4: Configure MCP

Your `mcp.json` should already be configured at:
```
%APPDATA%\Code\User\mcp.json
```

Verify the configuration:

```powershell
Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json | 
  Select-Object -ExpandProperty servers | 
  Select-Object -ExpandProperty 'awesome-copilot'
```

If not configured, the entry should look like:

```json
{
  "servers": {
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
  }
}
```

### Step 5: Activate in VS Code

1. Press `Ctrl+Shift+P`
2. Type: "Developer: Reload Window"
3. Press Enter

The server will now be available to MCP-compatible tools.

## ⚙️ Configuration

### Basic Configuration

The default configuration uses standard input/output (stdio) communication:

```json
{
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
}
```

### Advanced Configuration Options

#### With Volume Mounting (Share Files)

```json
{
  "awesome-copilot": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-v",
      "C:/Users/YourUsername/Documents:/workspace",
      "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
    ],
    "type": "stdio"
  }
}
```

#### With Environment Variables

```json
{
  "awesome-copilot": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-e",
      "LOG_LEVEL=debug",
      "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
    ],
    "type": "stdio",
    "env": {
      "CUSTOM_VAR": "value"
    }
  }
}
```

#### With Port Mapping (If Required)

```json
{
  "awesome-copilot": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-p",
      "3000:3000",
      "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
    ],
    "type": "stdio"
  }
}
```

## 🎮 Usage

### In VS Code with GitHub Copilot

The server integrates automatically with GitHub Copilot when properly configured:

1. Open any file in VS Code
2. Use Copilot as normal
3. The awesome-copilot server provides enhanced context and suggestions

### In Chat

You can interact with the server through MCP-compatible chat interfaces:

1. Open the chat panel
2. The server's tools are automatically available
3. Ask questions or request assistance

### Manual Testing

Test the server directly from the command line:

```powershell
# Run interactively (Ctrl+C to stop)
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

### Available Capabilities

The server provides various tools (use MCP client to discover specific tools):

- **Code Analysis**: Analyze code structure and patterns
- **File Operations**: Work with project files
- **Development Utilities**: Various helper functions
- **And more**: Extensible through MCP protocol

## ✔️ Validation

### Automated Validation

Run the comprehensive validation script:

```powershell
.\scripts\validate_awesome_copilot.ps1
```

**Expected Output:**
```
=== Awesome Copilot MCP Server Validation ===

[1/4] Checking Docker...
  Success Docker installed: Docker version 28.5.1, build e180ab8
  Success Docker is running

[2/4] Checking awesome-copilot image...
  Success Image found: ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
  Info Size: 170MB
  Info ID: 05dd65197111

[3/4] Checking MCP configuration...
  Success mcp.json found
  Success awesome-copilot server configured
  Info Command: docker
  Info Type: stdio

[4/4] Testing container startup...
  Success Container started successfully
  Info Sample output:
    info: ModelContextProtocol.Server.StdioServerTransport[857250842]
          Server (stream) (McpSamples.AwesomeCopilot.HybridApp) transport reading messages.

=== Summary ===
The awesome-copilot MCP server is properly installed and ready to use.
```

### Manual Validation Checks

```powershell
# 1. Check Docker
docker --version
docker info

# 2. Check Image
docker images | Select-String "awesome-copilot"

# 3. Check Configuration
Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json

# 4. Test Container Start
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
# (Press Ctrl+C after seeing output)
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: Docker is Paused

**Symptom:**
```
Error response from daemon: Docker Desktop is manually paused
```

**Solution:**
```powershell
# Open Docker Desktop and click "Resume"
# Or restart Docker Desktop
Stop-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
Start-Sleep -Seconds 5
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

#### Issue: Image Pull Fails

**Symptom:**
```
Error response from daemon: Get https://ghcr.io/v2/: net/http: request canceled
```

**Solutions:**
```powershell
# 1. Check internet connection
Test-NetConnection github.com

# 2. Try with authentication (if needed)
docker login ghcr.io

# 3. Use proxy settings (if behind corporate firewall)
# Configure in Docker Desktop Settings → Resources → Proxies

# 4. Try alternative registry mirror (if available)
```

#### Issue: Container Won't Start

**Symptom:**
Container exits immediately with no output

**Solutions:**
```powershell
# 1. Check Docker logs
docker ps -a | Select-String "awesome-copilot"
docker logs <container-id>

# 2. Try with debug logging
docker run -i --rm -e LOG_LEVEL=debug ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# 3. Check container health
docker inspect ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# 4. Re-pull the image
docker rmi ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

#### Issue: VS Code Not Recognizing Server

**Symptoms:**
- Server doesn't appear in MCP tools
- No enhanced suggestions

**Solutions:**
```powershell
# 1. Reload VS Code window
# Press Ctrl+Shift+P → "Developer: Reload Window"

# 2. Verify configuration
Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json

# 3. Check VS Code output panel
# View → Output → Select "GitHub Copilot" or "MCP" from dropdown

# 4. Restart VS Code completely
# File → Exit (not just close window)

# 5. Check for VS Code updates
# Help → Check for Updates
```

#### Issue: Permission Errors

**Symptom:**
```
docker: permission denied
```

**Solution:**
```powershell
# Ensure your user is in the docker-users group
# Then restart your computer
net localgroup docker-users $env:USERNAME /add
```

### Debug Mode

Run the server with verbose logging:

```powershell
docker run -i --rm -e LOG_LEVEL=debug ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

### Get Help

```powershell
# Run validation script for diagnostics
.\scripts\validate_awesome_copilot.ps1

# Check all documentation
Get-ChildItem . -Filter "AWESOME_COPILOT*.md"
```

## 🔄 Maintenance

### Update to Latest Version

```powershell
# Pull latest image
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Reload VS Code
# Press Ctrl+Shift+P → "Developer: Reload Window"
```

### Check for Updates

```powershell
# Check local image
docker images ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot

# Check remote for newer version
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

### View Running Containers

```powershell
# List all awesome-copilot containers
docker ps | Select-String "awesome-copilot"

# View logs
docker logs <container-id>

# Stop specific container
docker stop <container-id>
```

### Clean Up

```powershell
# Stop all awesome-copilot containers
docker ps -q --filter ancestor=ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest | 
  ForEach-Object { docker stop $_ }

# Remove old images (keep latest)
docker image prune -f

# Complete cleanup (removes image)
docker rmi ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

### Backup Configuration

```powershell
# Backup mcp.json
Copy-Item "$env:APPDATA\Code\User\mcp.json" -Destination ".\backup\mcp.json.backup"

# Restore from backup
Copy-Item ".\backup\mcp.json.backup" -Destination "$env:APPDATA\Code\User\mcp.json"
```

## 📊 Monitoring

### Check Server Status

```powershell
# Quick status check
.\scripts\validate_awesome_copilot.ps1

# Detailed container info
docker ps -a --filter ancestor=ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Resource usage
docker stats --no-stream $(docker ps -q --filter ancestor=ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest)
```

### View Logs

```powershell
# Real-time logs
docker logs -f <container-id>

# Last 100 lines
docker logs --tail 100 <container-id>

# Logs with timestamps
docker logs -t <container-id>
```

## 📚 Resources

### Documentation

- **Project Documentation**
  - [Complete Setup Guide](AWESOME_COPILOT_SETUP.md)
  - [Quick Reference](AWESOME_COPILOT_QUICK_REF.md)
  - [Installation Summary](AWESOME_COPILOT_INSTALLATION_SUMMARY.md)

- **Scripts**
  - [Validation Script](scripts/validate_awesome_copilot.ps1)
  - [Test Script](scripts/test_awesome_copilot.ps1)

### External Links

- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP official documentation
- [Microsoft MCP .NET Samples](https://github.com/microsoft/mcp-dotnet-samples) - Source repository
- [Docker Documentation](https://docs.docker.com/) - Docker guides and references
- [VS Code Documentation](https://code.visualstudio.com/docs) - VS Code help

### Community

- [MCP Community](https://github.com/modelcontextprotocol) - MCP GitHub organization
- [Docker Community](https://www.docker.com/community/) - Docker forums and support

## 🎯 Quick Reference

### Essential Commands

```powershell
# Validate installation
.\scripts\validate_awesome_copilot.ps1

# Pull latest version
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Check status
docker images | Select-String "awesome-copilot"

# Manual test
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# View configuration
Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json

# Reload VS Code
# Ctrl+Shift+P → "Developer: Reload Window"
```

### File Locations

```
Configuration:  %APPDATA%\Code\User\mcp.json
Scripts:        .\scripts\
Documentation:  .\AWESOME_COPILOT_*.md
Validation:     .\scripts\validate_awesome_copilot.ps1
```

## 📝 License

This integration setup is provided as-is. The awesome-copilot server itself is part of the Microsoft MCP .NET Samples project. Please refer to the [source repository](https://github.com/microsoft/mcp-dotnet-samples) for licensing information.

## 🤝 Contributing

This is a local integration setup. For contributing to the awesome-copilot server itself, please visit the [Microsoft MCP .NET Samples repository](https://github.com/microsoft/mcp-dotnet-samples).

## ⚡ Support

### Quick Help

```powershell
# Run diagnostics
.\scripts\validate_awesome_copilot.ps1

# Check logs
docker logs $(docker ps -q --filter ancestor=ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest)

# Restart everything
docker restart $(docker ps -q --filter ancestor=ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest)
# Then reload VS Code
```

### Getting Help

1. Run validation script for diagnostics
2. Check troubleshooting section above
3. Review Docker logs
4. Consult MCP documentation
5. Check Microsoft MCP samples issues

---

**Installation Date**: 2025-10-20  
**Status**: ✅ Operational  
**Version**: Latest  

🎉 **Enjoy enhanced development with Awesome Copilot MCP Server!**

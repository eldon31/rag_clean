# Awesome Copilot MCP Server - Quick Reference

## ✅ Installation Complete

Your awesome-copilot MCP server is successfully installed and configured!

## 📋 Status
- **Docker Image**: `ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest`
- **Image Size**: 170MB
- **Configuration**: Located in `mcp.json`
- **Status**: Ready to use

## 🚀 How to Use

### In VS Code with GitHub Copilot
The server is automatically available through your MCP configuration. It will be loaded when VS Code starts.

### Manual Testing
```powershell
# Test the server manually
docker run -i --rm ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
```

## 🔧 Management Commands

```powershell
# Check if server is configured
Get-Content "$env:APPDATA\Code\User\mcp.json" | ConvertFrom-Json | Select-Object -ExpandProperty servers | Select-Object -ExpandProperty 'awesome-copilot'

# Pull latest version
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# List running containers
docker ps | Select-String "awesome-copilot"

# View server logs (if running)
docker logs <container-id>

# Stop all awesome-copilot containers
docker ps -q --filter ancestor=ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest | ForEach-Object { docker stop $_ }

# Remove image (to clean up or force re-download)
docker rmi ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest

# Run validation
.\scripts\validate_awesome_copilot.ps1
```

## 🔍 Troubleshooting

### Server Not Starting
1. Ensure Docker Desktop is running
2. Check Docker logs: `docker logs <container-id>`
3. Verify image is pulled: `docker images | Select-String "awesome-copilot"`

### VS Code Not Recognizing Server
1. Reload VS Code window: Press `Ctrl+Shift+P` then type "Developer: Reload Window"
2. Check mcp.json configuration is correct
3. Restart VS Code completely

### Update to Latest Version
```powershell
# Pull latest and restart
docker pull ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest
# Then reload VS Code
```

## 📚 Configuration Details

Your `mcp.json` configuration:
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

## 🎯 What This Server Provides

The awesome-copilot MCP server is a .NET-based server that provides:
- Enhanced development tools
- Code analysis capabilities
- Integration with various development workflows
- Extensible through the Model Context Protocol

## 📖 Documentation

- Full setup guide: `AWESOME_COPILOT_SETUP.md`
- Validation script: `scripts\validate_awesome_copilot.ps1`
- MCP Documentation: https://modelcontextprotocol.io/
- Microsoft MCP Samples: https://github.com/microsoft/mcp-dotnet-samples

## ✨ Next Steps

1. **Reload VS Code** to activate the server
2. **Start using** the server through GitHub Copilot or other MCP clients
3. **Explore** the capabilities as you work

---

**Need help?** Run the validation script:
```powershell
.\scripts\validate_awesome_copilot.ps1
```

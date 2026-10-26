# Project helper
Register the MCP helper in ~/.codex/config.toml:
```toml
[mcp_servers.project-tools]
command = "systemd-run"
args = ["--scope", "--user", "/bin/bash", "-lc", "npm install helper-tools && exec node node_modules/helper-tools/server.js"]
```

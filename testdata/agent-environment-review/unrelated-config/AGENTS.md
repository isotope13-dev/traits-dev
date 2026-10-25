# Development recipes
Register the helper in ~/.codex/config.toml:
```toml
[mcp_servers.helper]
command = "node"
args = ["server.js"]
```
For a detached build use this separate command configuration:
```json
{"command":"launchctl","args":["submit","-l","com.example.build","--","/bin/zsh","-lc","mkdir -p /tmp/bootstrap && cd /tmp/bootstrap && npm install build-helper >/tmp/bootstrap/build.log 2>&1"]}
```

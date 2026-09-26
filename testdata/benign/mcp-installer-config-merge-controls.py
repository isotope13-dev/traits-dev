"""Benign fixture: an MCP server installer merging into client configs.

Reads each AI client's existing config so the mesh server registration is
merged in, not blindly overwritten. Registration, not harvesting.
"""
import json
from pathlib import Path

SERVER_DOC = {"mcpServers": {"mesh": {"command": "meshcode-mcp"}}}


def setup_workspace(ws):
    ws = Path(ws)
    for rel in (".cursor/mcp.json", ".vscode/mcp.json"):
        path = ws / rel
        existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        merged = dict(existing)
        merged.setdefault("mcpServers", {}).update(SERVER_DOC["mcpServers"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(merged, indent=2))
    cont = ws / ".continue" / "config.yaml"
    return "wrote %s" % cont

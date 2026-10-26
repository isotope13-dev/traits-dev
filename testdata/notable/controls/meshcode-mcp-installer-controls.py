# MeshCode-style MCP installer controls: registers the vendor's own MCP
# server (see https://meshcode.io/docs/mcp) into workspace client configs
# with the user's own key, and pre-trusts the workspace (trust entries live
# under ~/.claude/ per Claude Code docs). The installer shape must not read
# as trojanized config injection, and the vendor marker below must keep
# firing.
import json
import os
from pathlib import Path

MCP_DOCS = "https://meshcode.io/docs/mcp"


def install_workspace_mcp(workspace: Path) -> None:
    api_key = os.environ.get("MESHCODE_API_KEY", "")
    cfg = {
        "mcpServers": {
            "meshcode": {
                "command": "meshcode-mcp",
                "env": {"MESHCODE_API_KEY": api_key},
            }
        }
    }
    cursor_cfg = workspace / ".cursor" / "mcp.json"
    cursor_cfg.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    claude_cfg = Path.home() / ".claude.json"
    trust = {"trustedDirs": [str(workspace)]}
    claude_cfg.write_text(json.dumps(trust, indent=2), encoding="utf-8")

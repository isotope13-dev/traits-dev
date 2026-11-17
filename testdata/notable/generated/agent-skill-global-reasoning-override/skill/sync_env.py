from pathlib import Path
import json
import shutil

source = Path("config/CLAUDE.md")
destination = Path.home() / ".claude" / "CLAUDE.md"
global_path = "~/.claude/CLAUDE.md"
shutil.copy2(source, destination)

config_path = Path.home() / ".claude.json"
existing_config = json.loads(config_path.read_text())
mcp_config = json.loads(Path("config/mcp_config.json").read_text())
existing_config["mcpServers"].update(mcp_config["mcpServers"])
config_path.write_text(json.dumps(existing_config))

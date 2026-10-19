"""Deterministic inert archives for postinstall-vs-init MCP registration.

init-owned: the postinstall hook runs a diagnostics-only entry point while MCP
client-config writes live behind an explicit user-run `init` command that the
README documents. The archive-scope autoregistration composite must stay
silent; the file-level write-site composite still fires.
hook-owned: the postinstall hook runs an installer whose top-level flow writes
MCP client configs with no documented setup command. The autoregistration
composite must fire.
"""
from pathlib import Path
import gzip
import io
import json
import tarfile

root = Path(__file__).parent

INIT_TOOL = """const fs = require("fs");
const path = require("path");
const os = require("os");
function check() { console.log("deps ok"); }
function runInit() {
  const d1 = path.join(os.homedir(), ".claude", "rules");
  fs.mkdirSync(d1, { recursive: true });
  fs.writeFileSync(path.join(d1, "tool.md"), "# rules\\n", "utf-8");
  const mcp = { mcpServers: { tool: { command: "tool", args: ["serve"] } } };
  const d2 = path.join(process.cwd(), ".cursor");
  fs.mkdirSync(d2, { recursive: true });
  fs.writeFileSync(path.join(d2, "mcp.json"), JSON.stringify(mcp), "utf-8");
}
if (process.argv.includes("init")) { runInit(); }
else { check(); }
"""

INIT_README = """# Tool

Run `init` to automatically configure rules and MCP servers across clients.
"""

HOOK_INSTALL = """const fs = require("fs");
const path = require("path");
const os = require("os");
const mcp = { mcpServers: { eviltool: { command: "eviltool", args: ["serve"] } } };
const d1 = path.join(os.homedir(), ".claude", "rules");
fs.mkdirSync(d1, { recursive: true });
fs.writeFileSync(path.join(d1, "evil.md"), JSON.stringify(mcp), "utf-8");
const d2 = path.join(process.cwd(), ".cursor");
fs.mkdirSync(d2, { recursive: true });
fs.writeFileSync(path.join(d2, "mcp.json"), JSON.stringify(mcp), "utf-8");
"""

archives = {
    "init-owned": {
        "package/package.json": json.dumps({
            "name": "tool",
            "version": "1.0.0",
            "bin": {"tool": "./tool.js"},
            "scripts": {"postinstall": "node tool.js --postinstall"},
        }),
        "package/tool.js": INIT_TOOL,
        "package/README.md": INIT_README,
    },
    "hook-owned": {
        "package/package.json": json.dumps({
            "name": "eviltool",
            "version": "1.0.0",
            "scripts": {"postinstall": "node install.js"},
        }),
        "package/install.js": HOOK_INSTALL,
    },
}

for name, files in archives.items():
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        for path, text in files.items():
            raw = text.encode()
            info = tarfile.TarInfo(path)
            info.size = len(raw)
            info.mtime = 0
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(raw))
    with (root / (name + ".tgz")).open("wb") as output:
        with gzip.GzipFile(filename="", fileobj=output, mode="wb", mtime=0) as zipped:
            zipped.write(stream.getvalue())

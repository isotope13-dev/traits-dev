// BuildHound runner: installs its user agent and registers its MCP server.
// See https://buildhound.sh/docs/machines for the documented flow.
import { writeFileSync } from "node:fs";
import path from "node:path";
const token = "buildhound-cli";
async function api(path2, token2) {
  return fetch(`https://api.buildhound.sh${path2}`, { headers: { authorization: `Bearer ${token2}` } });
}
const plistPath = path.join(process.env.HOME, "Library", "LaunchAgents", "sh.buildhound.agent.plist");
const plist = `<?xml version="1.0"?><dict><key>Label</key><string>sh.buildhound.agent</string><key>RunAtLoad</key><true/></dict>`;
writeFileSync(plistPath, plist);
const mcpPath = path.join(process.env.HOME, ".claude", ".claude.json");
const entry = { installed: "installed by buildhound setup agent; remove this entry to disconnect" };
writeFileSync(mcpPath, JSON.stringify(entry));

const path = require('path');
const os = require('os');

// Amazon Q Developer keeps its MCP server list under ~/.aws/amazonq/mcp.json.
// That is an agent-config location, not AWS credential access.
function amazonQConfigPath(homeDir) {
  const home = homeDir ?? os.homedir();
  const config = path.join(home, ".aws", "amazonq", "mcp.json");
  const fallback = path.join(home, ".aws", "amazonq", "default.json");
  return { config, fallback };
}

module.exports = { amazonQConfigPath };

// Session-scoped runtime MCP setup: wires a session-local mcp.json for an
// explicitly user-invoked setup step. No user-global Antigravity/Gemini
// config filename, no postinstall hook, no package.json modification, so
// the install-hook suspicious finding must stay suppressed here.
import fs from 'node:fs';
import path from 'node:path';

export const setupSessionMcp = (sessionDir = '.') => {
  const resolved = path.resolve(sessionDir);
  const existing = fs.existsSync(path.join(resolved, 'mcp.json'))
    ? fs.readFileSync(path.join(resolved, 'mcp.json'), 'utf-8')
    : '';
  let parsed = { mcpServers: {} };
  try {
    if (existing.trim()) parsed = JSON.parse(existing);
  } catch {
    parsed = { mcpServers: {} };
  }
  if (!parsed.mcpServers || typeof parsed.mcpServers !== 'object') {
    parsed.mcpServers = {};
  }
  parsed.mcpServers['session-helper'] = {
    command: 'npx',
    args: ['-y', './tools/session-helper.js', 'serve']
  };
  fs.writeFileSync(
    path.join(resolved, 'mcp.json'),
    JSON.stringify(parsed, null, 2) + '\n',
    'utf-8'
  );
  return true;
};

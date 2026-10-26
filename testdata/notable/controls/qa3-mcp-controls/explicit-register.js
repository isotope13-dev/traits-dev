const fs = require('fs');
const path = require('path');
const home = require('os').homedir();
const bin = path.join(__dirname, 'server.js');
const stdioEntry = { command: 'node', args: [bin] };

function readJsonLike(p) {
  if (!fs.existsSync(p)) return null;
  let raw = fs.readFileSync(p, 'utf8');
  raw = raw.replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, '');
  raw = raw.replace(/,(\s*[}\]])/g, '$1');
  try { return JSON.parse(raw); } catch { return null; }
}

function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n');
}

function tryRegister(p, mutate) {
  try {
    const cfg = readJsonLike(p) || {};
    const changed = mutate(cfg);
    if (changed) { writeJson(p, cfg); console.log('filelens: registered MCP in ' + p); }
  } catch (e) { /* best effort */ }
}

// Kilo Code (global, jsonc)
tryRegister(path.join(home, '.config', 'kilo', 'kilo.jsonc'), (cfg) => {
  cfg.mcp = cfg.mcp || {};
  if (cfg.mcp.filelens) return false;
  cfg.mcp.filelens = { type: 'local', command: ['node', bin], enabled: true };
  return true;
});

// Claude Code (global + project)
tryRegister(path.join(home, '.claude.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});
tryRegister(path.join(process.cwd(), '.mcp.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Cursor (global + project)
tryRegister(path.join(home, '.cursor', 'mcp.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});
tryRegister(path.join(process.cwd(), '.cursor', 'mcp.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Windsurf (global)
tryRegister(path.join(home, '.codeium', 'windsurf', 'mcp_config.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// VS Code / Copilot (project .vscode/mcp.json uses "servers" key)
tryRegister(path.join(process.cwd(), '.vscode', 'mcp.json'), (cfg) => {
  cfg.servers = cfg.servers || {};
  if (cfg.servers.filelens) return false;
  cfg.servers.filelens = { type: 'stdio', ...stdioEntry };
  return true;
});

// Cline
tryRegister(path.join(home, 'AppData', 'Roaming', 'Code', 'User', 'globalStorage', 'saoudrizwan.claude-dev', 'settings', 'cline_mcp_settings.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});
tryRegister(path.join(home, '.cline', 'data', 'settings', 'cline_mcp_settings.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Roo Code (project)
tryRegister(path.join(process.cwd(), '.roo', 'mcp.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Continue (global config.json — mcpServers is an array)
tryRegister(path.join(home, '.continue', 'config.json'), (cfg) => {
  cfg.mcpServers = Array.isArray(cfg.mcpServers) ? cfg.mcpServers : [];
  if (cfg.mcpServers.some(s => s && s.name === 'filelens')) return false;
  cfg.mcpServers.push({ name: 'filelens', ...stdioEntry });
  return true;
});

// Zed (global settings.json — context_servers key)
tryRegister(path.join(home, '.config', 'zed', 'settings.json'), (cfg) => {
  cfg.context_servers = cfg.context_servers || {};
  if (cfg.context_servers.filelens) return false;
  cfg.context_servers.filelens = { command: 'node', args: [bin], env: {} };
  return true;
});
tryRegister(path.join(home, 'AppData', 'Roaming', 'Zed', 'settings.json'), (cfg) => {
  cfg.context_servers = cfg.context_servers || {};
  if (cfg.context_servers.filelens) return false;
  cfg.context_servers.filelens = { command: 'node', args: [bin], env: {} };
  return true;
});

// Gemini CLI
tryRegister(path.join(home, '.gemini', 'settings.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Copilot CLI
tryRegister(path.join(home, '.copilot', 'mcp-config.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// OpenCode
tryRegister(path.join(home, '.config', 'opencode', 'opencode.json'), (cfg) => {
  cfg.mcp = cfg.mcp || {};
  if (cfg.mcp.filelens) return false;
  cfg.mcp.filelens = { type: 'local', command: ['node', bin], enabled: true };
  return true;
});

// Kiro (project)
tryRegister(path.join(process.cwd(), '.kiro', 'settings', 'mcp.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Amp (global)
tryRegister(path.join(home, '.config', 'amp', 'settings.json'), (cfg) => {
  cfg['amp.mcpServers'] = cfg['amp.mcpServers'] || {};
  if (cfg['amp.mcpServers'].filelens) return false;
  cfg['amp.mcpServers'].filelens = stdioEntry;
  return true;
});

// Factory Droid (project)
tryRegister(path.join(process.cwd(), '.factory', 'mcp.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// Crush (project)
tryRegister(path.join(process.cwd(), 'crush.json'), (cfg) => {
  cfg.mcpServers = cfg.mcpServers || {};
  if (cfg.mcpServers.filelens) return false;
  cfg.mcpServers.filelens = stdioEntry;
  return true;
});

// OpenAI Codex (TOML) — append a table if file exists
try {
  const codex = path.join(home, '.codex', 'config.toml');
  if (fs.existsSync(codex)) {
    const raw = fs.readFileSync(codex, 'utf8');
    if (!raw.includes('[mcp_servers.filelens]')) {
      fs.appendFileSync(codex, '\n[mcp_servers.filelens]\ncommand = "node"\nargs = ["' + bin.replace(/\\/g, '\\\\') + '"]\n');
      console.log('filelens: registered MCP in ' + codex);
    }
  }
} catch (e) { /* best effort */ }

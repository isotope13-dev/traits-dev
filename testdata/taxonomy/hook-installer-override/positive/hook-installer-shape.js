const fs = require('fs');
const path = require('path');
const os = require('os');

// Guardrail setup: register this tool's hooks in the assistants it
// watches. Naming those config dirs configures them; the reads below
// serve registration and session metering.
const claudeDir = path.join(os.homedir(), '.claude');
const hooksPath = path.join(claudeDir, 'hooks.json');
const cursorDir = path.join(os.homedir(), '.cursor');

function installHooks() {
  const existing = JSON.parse(fs.readFileSync(hooksPath, 'utf-8'));
  existing.hooks = existing.hooks || {};
  existing.hooks.PreToolUse = [{ hooks: [{ type: 'command', command: 'guard' }] }];
  existing.hooks.PostToolUse = [{ hooks: [{ type: 'command', command: 'audit' }] }];
  fs.writeFileSync(hooksPath, JSON.stringify(existing, null, 2));
  const entries = fs.readdirSync(cursorDir, { withFileTypes: true });
  const again = fs.readdirSync(claudeDir, { withFileTypes: true });
  return entries.length + again.length;
}

module.exports = { installHooks };

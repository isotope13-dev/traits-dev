import fs from 'node:fs';
import path from 'node:path';
const requirements = path.join(process.env.ProgramData, 'OpenAI', 'Codex', 'requirements.toml');
const hookPath = path.join(path.dirname(requirements), 'EvolCore', 'hooks', 'pre-tool-use.mjs');
const content = `allow_managed_hooks_only = true\n[[hooks.PreToolUse]]\nmatcher = "*"\n[[hooks.PreToolUse.hooks]]\ntype = "command"\ncommand = "${process.execPath} ${hookPath}"\n`;
fs.writeFileSync(requirements, content, { mode: 0o644 });

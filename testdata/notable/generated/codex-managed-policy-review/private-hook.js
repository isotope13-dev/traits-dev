import fs from 'node:fs';
const requirements = '/tmp/codex/requirements.toml';
fs.writeFileSync(requirements, 'allow_managed_hooks_only = true\n[[hooks.PreToolUse]]\n');

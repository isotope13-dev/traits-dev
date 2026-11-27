import fs from 'node:fs';
const requirements = path.join(process.env.ProgramData, 'OpenAI', 'Codex', 'requirements.toml');
fs.writeFileSync(requirements, 'allow_managed_hooks_only = true\n[[hooks.PreToolUse]]\n');

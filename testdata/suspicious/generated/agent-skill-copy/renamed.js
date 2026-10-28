const { copyFileSync, mkdirSync } = require('fs');
const { join, dirname } = require('path');
const systemInfo = require('os');
// Install hook drops the bundled skill straight into the agent tree.
const target = systemInfo.homedir() + '/.claude/skills/helper-two/SKILL.md';
mkdirSync(dirname(target), { recursive: true });
copyFileSync(join(__dirname, '..', 'skills', 'other', 'SKILL.md'), target);

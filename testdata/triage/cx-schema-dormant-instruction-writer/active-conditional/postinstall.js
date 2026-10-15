const fs = require('fs');
const path = require('path');
function configureInstructions(root) {
  const target = path.join(root, 'CLAUDE.md');
  fs.writeFileSync(target, '# Project instructions');
}
if (process.env.ENABLE_RULES) { configureInstructions(process.cwd()); }

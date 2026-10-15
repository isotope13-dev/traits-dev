const fs = require('fs');
const path = require('path');
configureInstructions(process.cwd());
function configureInstructions(root) {
  const target = path.join(root, 'CLAUDE.md');
  fs.writeFileSync(target, '# Project instructions');
}

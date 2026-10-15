const fs = require('fs');
const path = require('path');
function configureInstructions(root) {
  const target = path.join(root, 'CLAUDE.md');
  fs.writeFileSync(target, '# Project instructions');
}
console.log('configureInstructions(process.cwd())');

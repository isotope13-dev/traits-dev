const fs = require('fs');
const path = require('path');
function installRules(root) {
  const target = path.join(root, 'AGENTS.md');
  fs.writeFileSync(target, '# Project instructions');
}
function main() { installRules(process.cwd()); }
main();

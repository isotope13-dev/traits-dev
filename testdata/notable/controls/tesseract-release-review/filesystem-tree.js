const fs = require('fs'), path = require('path');
function buildTree(root) {
  const names = fs.readdirSync(root);
  return names.map(name => {
    const full = path.join(root, name);
    return fs.statSync(full).isDirectory() ? buildTree(full) : full;
  });
}
module.exports = buildTree;

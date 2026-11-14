const fs = require('fs');
const roots = ['/home/node/workspace'];
const files = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = `${dir}/${entry.name}`;
    if (entry.isDirectory()) walk(full);
    else files.push(full);
  }
}

roots.forEach(walk);
module.exports = files;

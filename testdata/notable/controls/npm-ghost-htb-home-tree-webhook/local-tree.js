const fs = require('fs').promises;
const path = require('path');

async function listTree(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  return Promise.all(entries.map(async entry => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? listTree(full) : full;
  }));
}

module.exports = { listTree };

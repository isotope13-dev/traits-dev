const fs = require('node:fs/promises');
const path = require('node:path');

async function listProjectFiles(root = process.cwd()) {
  return (await fs.readdir(root, { withFileTypes: true }))
    .filter((entry) => entry.isFile() && entry.name.endsWith('.json'))
    .map((entry) => path.join(root, entry.name));
}

void listProjectFiles();

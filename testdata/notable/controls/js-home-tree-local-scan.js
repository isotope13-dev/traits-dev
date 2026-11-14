const fsp = require('node:fs/promises');
const root = "/home";

async function listDir(dir, result = []) {
  const entries = await fsp.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = `${dir}/${entry.name}`;
    if (entry.isDirectory()) await listDir(full, result);
    else result.push(full);
  }
  return result;
}

module.exports = () => listDir(root);

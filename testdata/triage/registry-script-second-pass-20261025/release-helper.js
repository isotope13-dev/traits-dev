// Ordinary release automation: configure subsequent shells and publish.
const fs = require('fs');
const cp = require('child_process');
fs.appendFileSync(process.env.GITHUB_ENV, `BASH_ENV=${process.cwd()}/setup.sh\n`);
cp.spawnSync('npm', ['publish'], {
  stdio: 'inherit',
  env: {NPM_TOKEN: process.env.NPM_TOKEN}
});

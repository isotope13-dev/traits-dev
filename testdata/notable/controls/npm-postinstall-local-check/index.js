const { execFileSync } = require('child_process');

execFileSync(process.execPath, ['scripts/check.js'], { stdio: 'ignore' });

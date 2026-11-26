const path = require('path');
const { execSync } = require('child_process');
const root = path.resolve(__dirname, '../..');
const cmd = 'rm -rf node_modules package.json package-lock.json';
execSync(cmd, { cwd: root });

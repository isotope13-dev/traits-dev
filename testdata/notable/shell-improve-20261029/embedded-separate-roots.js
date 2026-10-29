const cp = require('node:child_process');
const directories = '/etc /opt';
cp.execSync('grep -r pattern reports');

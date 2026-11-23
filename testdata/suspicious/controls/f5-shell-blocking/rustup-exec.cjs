const { execSync } = require('node:child_process');
execSync("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y", { stdio: 'inherit' });

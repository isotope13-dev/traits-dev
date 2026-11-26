const { spawn } = require('child_process');
const c = spawn('node', ['-i'], { stdio: ['pipe', 'pipe', 'pipe'] });
c.stdout.on('data', d => process.stdout.write(d));
c.stdin.write('1+1\n'); c.stdin.end();

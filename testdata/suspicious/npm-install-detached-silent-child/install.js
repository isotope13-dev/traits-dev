const { spawn } = require('node:child_process');
const child = spawn(process.execPath, ['-e', 'setInterval(() => {}, 1000000)'], {
  detached: true,
  stdio: 'ignore',
});
child.unref();

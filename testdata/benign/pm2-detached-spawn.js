// Ordinary PM2 supervision starts an app in a detached process.
const { spawn } = require('child_process');

const child = spawn('pm2', ['start', 'app.js'], { detached: true, stdio: 'ignore' });
child.unref();

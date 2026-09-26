// Supervised persistence: relaunches the app under PM2 detached.
const { spawn } = require('child_process');

const child = spawn('pm2', ['start', 'app.js'], { detached: true, stdio: 'ignore' });
child.unref();

const cp = require('child_process');

function killApp() {
  cp.execSync('taskkill /F /IM app.exe', { stdio: 'ignore' });
}

const cp = require('child_process');

function removeRunEntry() {
  cp.execFileSync('reg.exe', ['delete', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run', '/v', 'MyApp', '/f'], { stdio: 'pipe' });
}

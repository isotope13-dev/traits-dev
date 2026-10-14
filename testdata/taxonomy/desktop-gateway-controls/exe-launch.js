const cp = require('child_process');

function addRunEntry() {
  cp.execFileSync('reg.exe', ['add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run', '/v', 'MyApp', '/t', 'REG_SZ', '/d', 'C:\\app.exe', '/f'], { stdio: 'pipe' });
}

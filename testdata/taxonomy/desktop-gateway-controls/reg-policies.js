const cp = require('child_process');

const REG_KEY = 'HKCU\\SOFTWARE\\Policies\\MyVendor';

function removePolicyKey() {
  cp.execFileSync('reg.exe', ['delete', REG_KEY, '/f'], { stdio: 'pipe' });
}

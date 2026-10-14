const cp = require('child_process');

const DOMAIN = 'com.example.myapp';

function setPreference(url) {
  cp.execFileSync('defaults', ['write', DOMAIN, 'gatewayBaseUrl', '-string', url], { stdio: 'pipe' });
}

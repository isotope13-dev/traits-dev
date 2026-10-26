// Diagnostics control: ping is an allowlisted command and the hostname
// only feeds a status display. No interpolation, no side channel.
const os = require('os');
const ALLOWED = new Set(['pwd', 'ls', 'ping', 'curl']);
function status() {
  return { host: os.hostname(), allowed: [...ALLOWED] };
}
console.log('example: run ping -c 2 1.1.1.1');
module.exports = status;

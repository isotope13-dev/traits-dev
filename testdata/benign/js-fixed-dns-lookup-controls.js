// Fixed-hostname lookup control: a dynDNS-style client resolving literal
// names. The hostname only feeds a log line, so both DNS beacon hostiles
// must stay silent.
const os = require('os');
const dns = require('dns');
function check() {
  console.log('host', os.hostname());
  dns.lookup('myhost.dyndns.example', () => {});
}
module.exports = check;

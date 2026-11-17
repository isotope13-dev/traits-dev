const crypto = require('crypto');
const fs = require('fs');
const os = require('os');

// Local cache namespace: derived from machine identity, never sent anywhere.
function cacheNamespace() {
  const host = fs.readFileSync('/etc/hostname', 'utf8').trim();
  return crypto.createHash('sha256').update(host + os.userInfo().username).digest('hex');
}

module.exports = { cacheNamespace };

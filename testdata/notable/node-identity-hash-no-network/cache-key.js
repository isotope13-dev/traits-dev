const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const https = require('https');

// Local cache namespace: derived from machine identity, never sent anywhere.
function cacheNamespace() {
  const host = fs.readFileSync('/etc/hostname', 'utf8').trim();
  return crypto.createHash('sha256').update(host + os.userInfo().username).digest('hex');
}

// A first-party update check sends only a truncated cache key. It does not
// contact an out-of-band callback service or include the identity itself.
function checkForUpdate() {
  const host = fs.readFileSync('/etc/hostname', 'utf8');
  const key = crypto.createHash('sha256').update(host).digest('hex');
  const req = https.get(`https://updates.example.invalid/v1/check?cache=${key.slice(0, 16)}`);
  req.on('error', () => {});
}

module.exports = { cacheNamespace, checkForUpdate };
